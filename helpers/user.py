from io import BytesIO
from os.path import splitext
from re import sub

from django.core.files.images import ImageFile
from requests import get

from users.models import User


def format_photo_url(url: str) -> str:
    """Format the user's photo URL.

    Args:
        url (str): photo URL.

    Returns:
        str: formatted photo URL.
    """
    if not isinstance(url, str):
        raise TypeError('The URL must be a string.')
    new_url = 'https://suap.ifrn.edu.br' + sub(r'[0-9]{2,3}x[0-9]{3}\/', '', url)
    return new_url


def download_photo(url: str, user_registration: str) -> ImageFile:
    """Download the user's photo from a URL.

    Args:
        url (str): photo url.
        user_registration (str): user registration.

    Returns:
        ImageFile: user's photo.
    """
    if not isinstance(url, str):
        raise TypeError('The URL must be a string.')
    if not isinstance(user_registration, str):
        raise TypeError('The user registration must be a string.')
    photo_url = format_photo_url(url)
    photo_data = get(photo_url).content
    photo_name = user_registration + splitext(photo_url)[-1]
    photo = ImageFile(BytesIO(photo_data), photo_name)
    return photo


def set_permissions(
    user_registration: str,
    *,
    admin: bool = False,
    staff: bool = False,
    superuser: bool = False,
) -> None:
    if not isinstance(user_registration, str):
        raise TypeError('The user registration must be a string.')
    if not isinstance(admin, bool):
        raise TypeError('The admin must be a boolean.')
    if not isinstance(staff, bool):
        raise TypeError('The staff must be a boolean.')
    if not isinstance(superuser, bool):
        raise TypeError('The superuser must be a boolean.')
    user = User.objects.filter(registration=user_registration).first()
    if user is None:
        raise ValueError('This user registration does not exist.')
    setattr(user, 'is_admin', admin)
    setattr(user, 'is_staff', staff)
    setattr(user, 'is_superuser', superuser)
    user.save()
