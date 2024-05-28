from os import remove
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def remove_migrations() -> None:
    """Remove all files in the "migrations" folders, with the exception of __init__.py"""
    all_files = list(BASE_DIR.glob('apps/*/migrations/*.py'))
    files_to_exclude = filter(lambda x: x.name != '__init__.py', all_files)
    for file in files_to_exclude:
        remove(file)
        print(f'File removed: {file.relative_to(BASE_DIR)}')


if __name__ == '__main__':
    remove_migrations()
