from pathlib import Path
from shutil import rmtree

BASE_DIR = Path(__file__).resolve().parent.parent


def remove_data(static: bool = True, media: bool = True, db: bool = True):
    """Remove static and media dirs and db.sqlite3 file."""
    if static:
        rmtree(BASE_DIR / 'static', ignore_errors=True)
    if media:
        rmtree(BASE_DIR / 'media', ignore_errors=True)
    if db:
        (BASE_DIR / 'core' / 'db.sqlite3').unlink(missing_ok=True)


if __name__ == '__main__':
    remove_data()
