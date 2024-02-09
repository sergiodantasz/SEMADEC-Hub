from os import remove, walk
from os.path import join
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def remove_migrations() -> None:
    """Remove all files in the "migrations" folders, with the exception of __init__.py"""
    for root, dirs, files in walk(BASE_DIR):
        if root.endswith('migrations') and 'venv' not in root:
            for file in files:
                if file == '__init__.py':
                    continue
                file_path = join(root, file)
                remove(file_path)
                print(f'File removed: {file_path}')
