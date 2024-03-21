from secrets import SystemRandom
from string import ascii_letters, digits, punctuation


def generate_random_string(k: int = 64, *ignore) -> str:
    """Generate a string with random characters, including letters, digits and punctuation.

    Args:
        k (int, optional): length of the string. Defaults to 64.

    Returns:
        str: generated random string.
    """
    if not isinstance(k, int):
        raise TypeError('k must be an instance of int.')
    chars = ascii_letters + digits + punctuation
    for c in ignore:
        if c in chars:
            chars = chars.replace(c, '')
    chosen_chars = SystemRandom().choices(chars, k=k)
    secret_key = ''.join(chosen_chars)
    return secret_key
