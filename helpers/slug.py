from random import SystemRandom
from string import ascii_letters, digits

from django.utils.text import slugify


def generate_random_characters(k: int = 5) -> str:
    """Generate a string of k random characters.

    Args:
        k (int, optional): string size. Defaults to 5.

    Returns:
        str: string with random characters.
    """
    return ''.join(SystemRandom().choices(ascii_letters + digits, k=k))


def generate_slug(string: str, k: int = 5) -> str:
    """Generate a slug.

    Args:
        string (str): string used to generate the slug.
        k (int, optional): string size. Defaults to 5.

    Returns:
        str: slug.
    """
    if k == 0:
        return str(slugify(string))
    return str(slugify(string)) + '-' + generate_random_characters(k)


def generate_dynamic_slug(instance, field: str) -> str:
    """Generate a dynamic slug.

    Args:
        instance: model instance.
        field (str): base field used to generate the slug.

    Returns:
        str: dynamic slug.
    """
    model = instance.__class__
    field_value = getattr(instance, field)
    slug = generate_slug(field_value, 0)
    k = 1
    while True:
        data = model.objects.filter(slug=slug)
        if len(data) == 0:
            break
        slug = generate_slug(field_value, k)
        k += 1
    return slug
