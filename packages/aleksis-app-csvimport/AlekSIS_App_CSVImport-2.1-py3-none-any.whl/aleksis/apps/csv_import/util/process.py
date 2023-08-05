import logging
from typing import Optional

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext as _

import pandas
from pandas.errors import ParserError
from tqdm import tqdm

from aleksis.apps.csv_import.field_types import (
    DirectMappingFieldType,
    MatchFieldType,
    MultipleValuesFieldType,
    field_type_registry,
)
from aleksis.apps.csv_import.settings import FALSE_VALUES, TRUE_VALUES
from aleksis.core.models import Group, Person
from aleksis.core.util.celery_progress import ProgressRecorder

from ..models import ImportJob


@transaction.atomic
def import_csv(
    import_job: ImportJob,
    recorder: Optional[ProgressRecorder] = None,
) -> None:
    template = import_job.template
    model = template.content_type.model_class()
    school_term = import_job.school_term
    csv = import_job.data_file.open("rb")

    data_types = {}
    cols = []
    cols_for_multiple_fields = {}
    converters = {}
    match_field_types = []
    for field in template.fields.all():
        field_type = field.field_type_class
        column_name = field_type.get_column_name()

        # Get column header
        if issubclass(field_type, MultipleValuesFieldType):
            cols_for_multiple_fields.setdefault(field_type, [])
            cols_for_multiple_fields[field_type].append(column_name)

        # Get data type
        data_types[column_name] = field_type.get_data_type()

        if field_type.get_converter():
            converters[column_name] = field_type.get_converter()

        if issubclass(field_type, MatchFieldType):
            match_field_types.append((field_type.priority, field_type))

        # Prepare field type for import
        field_type.prepare(school_term)

        cols.append(column_name)
    match_field_types = sorted(match_field_types, key=lambda x: x[0])
    try:
        data = pandas.read_csv(
            csv,
            sep=template.parsed_separator,
            names=cols,
            header=0 if template.has_header_row else None,
            index_col=template.has_index_col,
            dtype=data_types,
            usecols=lambda k: not k.startswith("_"),
            keep_default_na=False,
            converters=converters,
            quotechar='"',
            encoding="utf-8-sig",
            true_values=TRUE_VALUES,
            false_values=FALSE_VALUES,
        )
    except ParserError as e:
        msg = _("There was an error while parsing the CSV file:\n{}").format(e)
        if recorder:
            recorder.add_message(messages.ERROR, msg)
        else:
            logging.error(msg)
        return

    # Exclude all empty rows
    data = data.where(data.notnull(), None)

    all_ok = True
    inactive_refs = []
    created_count = 0

    data_as_dict = data.transpose().to_dict().values()

    iterator = recorder.iterate(data_as_dict) if recorder else tqdm(data_as_dict)
    for row in iterator:
        # Build dict with all fields that should be directly updated
        update_dict = {}
        for key, value in row.items():
            if key in field_type_registry.field_types:
                field_type = field_type_registry.get_from_name(key)
                if issubclass(field_type, DirectMappingFieldType):
                    update_dict[field_type.get_db_field()] = value

        # Set alternatives for some fields
        for (
            field_type_origin,
            alternative_name,
        ) in field_type_registry.alternatives.items():
            if (
                model in field_type_origin.models
                and field_type_origin.name not in row
                and alternative_name in row
            ):
                update_dict[field_type_origin.name] = row[alternative_name]

        if template.group_type and model == Group:
            update_dict["group_type"] = template.group_type

        get_dict = {}
        match_field_found = False
        for (
            priority,
            match_field_type,
        ) in match_field_types:
            if match_field_found or match_field_type.name not in row:
                update_dict[match_field_type.get_db_field()] = row[match_field_type.name]
            elif match_field_type.name in row:
                get_dict[match_field_type.get_db_field()] = row[match_field_type.name]
                match_field_found = True

        if not match_field_found:
            raise ValueError(_("Missing unique reference."))

        if hasattr(model, "school_term") and school_term:
            get_dict["school_term"] = school_term

        created = False

        try:
            get_dict["defaults"] = update_dict

            instance, created = model.objects.update_or_create(**get_dict)

            # Get values for multiple fields
            values_for_multiple_fields = {}
            for field_type, cols_for_field_type in cols_for_multiple_fields.items():
                values_for_multiple_fields[field_type] = []
                for col in cols_for_field_type:
                    value = row[col]
                    values_for_multiple_fields[field_type].append(value)

                # Process
                field_type().process(instance, values_for_multiple_fields[field_type])

            # Process field types with custom logic
            for process_field_type in field_type_registry.process_field_types:
                if process_field_type.name in row:
                    try:
                        process_field_type().process(instance, row[process_field_type.name])
                    except RuntimeError as e:
                        if recorder:
                            recorder.add_message(messages.ERROR, str(e))
                        else:
                            logging.error(str(e))

            if template.group and isinstance(instance, Person):
                instance.member_of.add(template.group)

            if created:
                created_count += 1

        except (
            ValueError,
            ValidationError,
            model.MultipleObjectsReturned,
            model.DoesNotExist,
        ) as e:
            msg = _("Failed to import {verbose_name} {row}:\n{e}").format(
                verbose_name=model._meta.verbose_name, row=row, e=e
            )
            if recorder:
                recorder.add_message(
                    messages.ERROR,
                    msg,
                )
            else:
                logging.error(msg)
                all_ok = False

    if created_count:
        msg = _("{created_count} {verbose_name} were newly created.").format(
            created_count=created_count, verbose_name=model._meta.verbose_name_plural
        )
        if recorder:
            recorder.add_message(messages.SUCCESS, msg)
        else:
            logging.info(msg)

    if all_ok:
        msg = _("All {verbose_name} were imported successfully.").format(
            verbose_name=model._meta.verbose_name_plural
        )
        if recorder:
            recorder.add_message(messages.SUCCESS, msg)
        else:
            logging.info(msg)
    else:
        msg = _("Some {verbose_name} failed to be imported.").format(
            verbose_name=model._meta.verbose_name_plural
        )
        if recorder:
            recorder.add_message(messages.WARNING, msg)
        else:
            logging.warning(msg)
