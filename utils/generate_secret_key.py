from re import sub
from secrets import SystemRandom
from string import ascii_letters, digits, punctuation


def generate_secret_key(k: int = 64) -> str:
    """Generate a secret key for a Django project.

    Args:
        k (int, optional): length of the secret key. Defaults to 64.

    Returns:
        str: secret key.
    """
    if not isinstance(k, int):
        raise TypeError('k must be an instance of int.')
    chars = ascii_letters + digits + sub(r'["\']', '', punctuation)
    chosen_chars = SystemRandom().choices(chars, k=k)
    secret_key = ''.join(chosen_chars)
    return secret_key


if __name__ == '__main__':
    generate_secret_key()
