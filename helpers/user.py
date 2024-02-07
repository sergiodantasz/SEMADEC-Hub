from re import sub


def format_photo_url(url: str) -> str:
    if not isinstance(url, str):
        raise TypeError('The URL must be a string.')
    new_url = 'https://suap.ifrn.edu.br' + sub(r'[0-9]{2,3}x[0-9]{3}\/', '', url)
    return new_url
