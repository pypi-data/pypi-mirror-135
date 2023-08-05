from typing import Optional, Sequence, Union

from django.db.models import Model


def with_prefix(prefix: Optional[str], value: str) -> str:
    """Add prefix to string.

    If prefix is not empty, this function will add a
    prefix to a string, delimited by a white space.
    """
    prefix = prefix.strip() if prefix else ""
    if prefix:
        return f"{prefix} {value}"
    else:
        return value


def bulk_get_or_create(
    model: Model,
    objs: Sequence,
    attr: str,
    default_attrs: Optional[Union[Sequence[str], str]] = None,
    defaults: Optional[dict] = None,
) -> Sequence[Model]:
    """
    Do get_or_create on a list of values.

    :param model: Model on which get_or_create should be executed
    :param objs: List of values
    :param attr: Field of model which should be set
    :param default_attrs: One or more extra fields of model which also should be set to the value
    :param defaults: Extra fields of model which should be set to a specific value
    :return: List of instances
    """
    if not defaults:
        defaults = {}

    if not default_attrs:
        default_attrs = []

    if not isinstance(default_attrs, list):
        default_attrs = [default_attrs]

    attrs = default_attrs + [attr]

    qs = model.objects.filter(**{f"{attr}__in": objs})
    existing_values = qs.values_list(attr, flat=True)

    instances = [x for x in qs]
    for obj in objs:
        if obj in existing_values:
            continue

        kwargs = defaults
        for _attr in attrs:
            kwargs[_attr] = obj
        instance = model.objects.create(**kwargs)

        instances.append(instance)

    return instances
