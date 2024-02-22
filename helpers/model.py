from typing import Any


def update_model_fields(
    obj, data: dict[str, Any], skip: tuple | list | None = None
) -> None:
    """Receive a model object and its updated values and perform an update.

    Args:
        obj: model registry with obsolete values.
        data (dict): a dict containing the new values.
        skip (tuple | list | None, optional): iterable containing fields to ignore. Defaults to None.
    """
    if not isinstance(data, dict):
        raise TypeError('The data must be a dict.')
    if not (isinstance(skip, (tuple, list)) or skip is None):
        raise TypeError('The skip must be a tuple, list or None.')
    if skip is None:
        skip = []
    for field in obj._meta.get_fields():
        field_name = field.name
        if field_name in skip:
            continue
        if not hasattr(field, 'value_to_string'):
            continue
        value = field.value_to_string(obj)
        new_value = data.get(field_name)
        if (value == 'None' or value is None) and new_value is None:
            continue
        if value != new_value:
            setattr(obj, field_name, new_value)
    obj.save()
