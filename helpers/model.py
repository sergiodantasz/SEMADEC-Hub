from typing import Any


def get_object(model, *args, **kwargs) -> Any | None:
    """Receive a model, operations and query a object and return it.

    Args:
        model (Any): the queried object.

    Returns:
        Any | None: the object or None if it does not exist.
    """
    objects = model.objects.filter(*args, **kwargs)
    if not objects.exists():
        return
    return objects.first()
