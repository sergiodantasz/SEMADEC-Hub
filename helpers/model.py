from os.path import split
from typing import Any

from home.models import Collection
from users.models import User


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


def is_owner(user: User, registry: Any) -> bool:
    """Receive a user object and a registry and validate is this user created this registry.

    Args:
        user (User): the user object.
        registry (Any): the registry.

    Returns:
        bool: True if user created the registry, otherwise False.
    """
    return user == registry.administrator


def generate_collection_cover_path(instance: Collection, filename: str) -> str:
    """Generate cover path of a collection depending on its type.

    Args:
        instance (Collection): collection instance.
        filename (str): file name.

    Returns:
        str: cover path based on the collection type.
    """
    _, filename = split(filename)
    return f'collections/{instance.collection_type}/covers/{filename}'
