from io import BytesIO
from random import randint

import requests
from django.core.files.images import ImageFile


def generate_placeholder() -> ImageFile:
    """Generate a placeholder image with random dimensions.
    Returns:
        ImageFile: A Django's ImageFile object.
    """
    image_name = 'placeholder.jpg'
    width = randint(100, 5000)
    height = randint(100, 5000)
    image = requests.get(
        f'https://placehold.co/{width}x{height}/22C55E/052E16.jpg'
    ).content
    object = ImageFile(BytesIO(image), image_name)
    return object
