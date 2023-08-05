import re
from typing import Any, Callable, Optional, Sequence, Tuple, Type, Union
from uuid import uuid4

from django.apps import apps
from django.db.models import Model
from django.utils.translation import gettext as _

from aleksis.apps.csv_import.util.class_range_helpers import (
    get_classes_per_grade,
    get_classes_per_short_name,
    parse_class_range,
)
from aleksis.apps.csv_import.util.converters import converter_registry
from aleksis.apps.csv_import.util.import_helpers import bulk_get_or_create, with_prefix
from aleksis.core.models import Group, Person, SchoolTerm
from aleksis.core.util.core_helpers import get_site_preferences


class FieldType:
    name: str = ""
    verbose_name: str = ""
    models: Sequence = []
    data_type: type = str
    converter: Optional[Union[str, Sequence[str]]] = None
    alternative: Optional[str] = None
    args: Optional[dict] = None

    @classmethod
    def get_data_type(cls) -> type:
        return cls.data_type

    @classmethod
    def get_converter(cls) -> Callable[[Any], Any]:
        converters_pre = cls.get_args().get("converter_pre", [])
        if isinstance(converters_pre, str):
            converters_pre = [converters_pre]
        converters_post = cls.get_args().get("converter_post", [])
        if isinstance(converters_post, str):
            converters_post = [converters_post]
        converters = cls.converter
        if converters is None:
            converters = []
        elif isinstance(converters, str):
            converters = [converters]
        converters = converters_pre + converters + converters_post

        funcs = [converter_registry.get_from_name(name) for name in converters]

        def _converter_chain(val: Any) -> Any:
            new_val = val
            for func in funcs:
                new_val = func(new_val)
            return new_val

        return _converter_chain

    @classmethod
    def get_alternative(cls) -> Optional[str]:
        return cls.alternative

    @classmethod
    def get_args(cls) -> dict:
        return cls.args or {}

    @classmethod
    def get_column_name(cls) -> str:
        return cls.name

    @classmethod
    def is_model_valid(cls, model: Model) -> bool:
        if not cls.models:
            return True
        return model in cls.models

    @classmethod
    def prepare(cls, school_term: SchoolTerm):
        cls.school_term = school_term


class MatchFieldType(FieldType):
    """Field type for getting an instance."""

    db_field: str = ""
    priority: int = 1

    @classmethod
    def get_db_field(cls):
        if cls.get_args().get("db_field"):
            return cls.get_args()["db_field"]
        return cls.db_field

    @classmethod
    def get_priority(cls):
        return cls.get_args().get("priority", "") or cls.priority


class DirectMappingFieldType(FieldType):
    """Set value directly in DB."""

    db_field: str = ""

    @classmethod
    def get_db_field(cls):
        if cls.get_args().get("db_field"):
            return cls.get_args()["db_field"]
        return cls.db_field

    @classmethod
    def get_column_name(cls):
        return cls.get_db_field()


class ProcessFieldType(FieldType):
    """Field type with custom logic for importing."""

    def process(self, instance: Model, value):
        pass


class RegExFieldType(ProcessFieldType):
    """Field type with custom logic for importing."""

    data_type = str
    reg_ex: str = ""

    @classmethod
    def get_reg_ex(cls):
        return cls.reg_ex or cls.get_args().get("reg_ex", "")

    def process(self, instance: Model, value):
        match = re.fullmatch(self.get_reg_ex(), value)
        if match:
            for key, item in match.groupdict().items():
                setattr(instance, key, item)
            instance.save()


class MultipleValuesFieldType(ProcessFieldType):
    """Has multiple columns."""

    def process(self, instance: Model, values: Sequence):
        pass

    @classmethod
    def get_column_name(cls) -> str:
        return f"{cls.name}_{uuid4()}"


class FieldTypeRegistry:
    def __init__(self):
        self.field_types = {}
        self.allowed_field_types_for_models = {}
        self.allowed_field_types_for_all_models = set()
        self.alternatives = {}
        self.match_field_types = []
        self.process_field_types = []

    def register(self, field_type: Type[FieldType]):
        """Add new `FieldType` to registry.

        Can be used as decorator, too.
        """
        if field_type.name in self.field_types:
            raise ValueError(f"The field type {field_type.name} is already registered.")
        self.field_types[field_type.name] = field_type

        if not field_type.models:
            self.allowed_field_types_for_all_models.add(field_type)
        else:
            for model in field_type.models:
                self.allowed_field_types_for_models.setdefault(model, []).append(field_type)

        if field_type.get_alternative():
            self.alternatives[field_type] = field_type.get_alternative()

        if issubclass(field_type, MatchFieldType):
            self.match_field_types.append((field_type.priority, field_type))

        if issubclass(field_type, ProcessFieldType):
            self.process_field_types.append(field_type)

        return field_type

    def get_from_name(self, name: str) -> FieldType:
        """Get `FieldType` by its name."""
        return self.field_types[name]

    @property
    def choices(self) -> Sequence[Tuple[str, str]]:
        """Return choices in Django format."""
        return [(f.name, f.verbose_name) for f in self.field_types.values()]

    @property
    def unique_references_by_priority(self) -> Sequence[FieldType]:
        return sorted(self.match_field_types)


field_type_registry = FieldTypeRegistry()


@field_type_registry.register
class UniqueReferenceFieldType(MatchFieldType):
    name = "unique_reference"
    verbose_name = _("Unique reference")
    models = [Person, Group]
    db_field = "import_ref_csv"
    priority = 10


@field_type_registry.register
class NameFieldType(DirectMappingFieldType):
    name = "name"
    verbose_name = _("Name")
    models = [Group]
    db_field = "name"
    alternative = "short_name"


@field_type_registry.register
class FirstNameFieldType(DirectMappingFieldType):
    name = "first_name"
    verbose_name = _("First name")
    models = [Person]
    db_field = "first_name"


@field_type_registry.register
class LastNameFieldType(DirectMappingFieldType):
    name = "last_name"
    verbose_name = _("Last name")
    models = [Person]
    db_field = "last_name"


@field_type_registry.register
class AdditionalNameFieldType(DirectMappingFieldType):
    name = "additional_name"
    verbose_name = _("Additional name")
    models = [Person]
    db_field = "additional_name"


@field_type_registry.register
class ShortNameFieldType(MatchFieldType):
    name = "short_name"
    verbose_name = _("Short name")
    models = [Person, Group]
    priority = 8
    db_field = "short_name"
    alternative = "name"


@field_type_registry.register
class EmailFieldType(MatchFieldType):
    name = "email"
    verbose_name = _("Email")
    models = [Person]
    db_field = "email"
    priority = 12

    @classmethod
    def get_converter(cls) -> Optional[Callable]:
        if "email_domain" in cls.get_args():

            def add_domain_to_email(value: str) -> str:
                if "@" in value:
                    return value
                else:
                    return f"{value}@{cls.get_args()['email_domain']}"

            return add_domain_to_email
        return super().get_converter()


@field_type_registry.register
class DateOfBirthFieldType(DirectMappingFieldType):
    name = "date_of_birth"
    verbose_name = _("Date of birth")
    models = [Person]
    db_field = "date_of_birth"
    converter = "parse_date"


@field_type_registry.register
class SexFieldType(DirectMappingFieldType):
    name = "sex"
    verbose_name = _("Sex")
    models = [Person]
    db_field = "sex"
    converter = "parse_sex"


@field_type_registry.register
class StreetFieldType(DirectMappingFieldType):
    name = "street"
    verbose_name = _("Street")
    models = [Person]
    db_field = "street"


@field_type_registry.register
class HouseNumberFieldType(DirectMappingFieldType):
    name = "housenumber"
    verbose_name = _("Housenumber")
    models = [Person]
    db_field = "housenumber"


@field_type_registry.register
class StreetAndHouseNumberFieldType(RegExFieldType):
    name = "street_housenumber"
    verbose_name = _("Street and housenumber")
    models = [Person]
    reg_ex = r"^(?P<street>[\w\s]{3,})\s+(?P<housenumber>\d+\s*[a-zA-Z]*)$"


@field_type_registry.register
class PostalCodeFieldType(DirectMappingFieldType):
    name = "postal_code"
    verbose_name = _("Postal code")
    models = [Person]
    db_field = "postal_code"


@field_type_registry.register
class PlaceFieldType(DirectMappingFieldType):
    name = "place"
    verbose_name = _("Place")
    models = [Person]
    db_field = "place"


@field_type_registry.register
class PhoneNumberFieldType(DirectMappingFieldType):
    name = "phone_number"
    verbose_name = _("Phone number")
    models = [Person]
    db_field = "phone_number"
    converter = "parse_phone_number"


@field_type_registry.register
class MobileNumberFieldType(DirectMappingFieldType):
    name = "mobile_number"
    verbose_name = _("Mobile number")
    models = [Person]
    db_field = "mobile_number"
    converter = "parse_phone_number"


@field_type_registry.register
class IgnoreFieldType(FieldType):
    name = "ignore"
    verbose_name = _("Ignore data in this field")
    models = [Person, Group]

    @classmethod
    def get_column_name(cls) -> str:
        return f"_ignore_{uuid4()}"


@field_type_registry.register
class DepartmentsFieldType(ProcessFieldType):
    name = "departments"
    verbose_name = _("Comma-seperated list of departments")
    models = [Person]
    converter = "parse_comma_separated_data"

    def process(self, instance: Model, value):
        with_chronos = apps.is_installed("aleksis.apps.chronos")
        if with_chronos:
            Subject = apps.get_model("chronos", "Subject")

        group_type = get_site_preferences()["csv_import__group_type_departments"]
        group_prefix = get_site_preferences()["csv_import__group_prefix_departments"]

        groups = []
        for subject_name in value:
            if with_chronos:
                # Get department subject
                subject, __ = Subject.objects.get_or_create(
                    short_name=subject_name, defaults={"name": subject_name}
                )
                name = subject.name
                short_name = subject.short_name
            else:
                name = subject_name
                short_name = subject_name

            # Get department group
            group, __ = Group.objects.get_or_create(
                group_type=group_type,
                short_name=short_name,
                defaults={"name": with_prefix(group_prefix, name)},
            )
            if with_chronos:
                group.subject = subject
            group.save()

            groups.append(group)

        instance.member_of.add(*groups)


@field_type_registry.register
class GroupSubjectByShortNameFieldType(ProcessFieldType):
    name = "group_subject_short_name"
    verbose_name = _("Short name of the subject")
    models = [Group]

    def process(self, instance: Model, value):
        with_chronos = apps.is_installed("aleksis.apps.chronos")
        if with_chronos:
            Subject = apps.get_model("chronos", "Subject")
            subject, __ = Subject.objects.get_or_create(short_name=value, defaults={"name": value})
            instance.subject = subject
            instance.save()


@field_type_registry.register
class ClassRangeFieldType(ProcessFieldType):
    name = "class_range"
    verbose_name = _("Class range (e. g. 7a-d)")
    models = [Group]

    @classmethod
    def prepare(cls, school_term: SchoolTerm):
        """Prefetch class groups."""
        cls.classes_per_short_name = get_classes_per_short_name(school_term)
        cls.classes_per_grade = get_classes_per_grade(cls.classes_per_short_name.keys())

    def process(self, instance: Model, value):
        classes = parse_class_range(
            self.classes_per_short_name,
            self.classes_per_grade,
            value,
        )
        instance.parent_groups.set(classes)


@field_type_registry.register
class PrimaryGroupByShortNameFieldType(ProcessFieldType):
    name = "primary_group_short_name"
    verbose_name = _("Short name of the person's primary group")
    models = [Person]

    def process(self, instance: Model, value):
        group, __ = Group.objects.get_or_create(
            short_name=value, school_term=self.school_term, defaults={"name": value}
        )
        instance.primary_group = group
        instance.member_of.add(group)
        instance.save()


@field_type_registry.register
class PrimaryGroupOwnerByShortNameFieldType(ProcessFieldType):
    name = "primary_group_owner_short_name"
    verbose_name = _("Short name of an owner of the person's primary group")
    models = [Person]

    def process(self, instance: Model, value):
        if instance.primary_group:
            owners = Person.objects.filter(short_name=value)
            instance.primary_group.owners.set(owners)


@field_type_registry.register
class GroupOwnerByShortNameFieldType(MultipleValuesFieldType):
    name = "group_owner_short_name"
    verbose_name = _("Short name of a single group owner")
    models = [Group]

    def process(self, instance: Model, values: Sequence):
        group_owners = bulk_get_or_create(
            Person,
            values,
            attr="short_name",
            default_attrs="last_name",
            defaults={"first_name": "?"},
        )
        instance.owners.set(group_owners)


@field_type_registry.register
class GroupMembershipByShortNameFieldType(MultipleValuesFieldType):
    name = "group_membership_short_name"
    verbose_name = _("Short name of the group the person is a member of")

    models = [Person]

    def process(self, instance: Model, values: Sequence):
        groups = Group.objects.filter(short_name__in=values, school_term=self.school_term)
        instance.member_of.add(*groups)


@field_type_registry.register
class ChildByUniqueReference(ProcessFieldType):
    name = "child_by_unique_reference"
    verbose_name = _("Child by unique reference (from students import)")
    models = [Person]

    def process(self, instance: Model, value):
        child = Person.objects.get(import_ref_csv=value)
        instance.children.add(child)
