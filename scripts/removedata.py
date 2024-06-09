from pathlib import Path
from shutil import rmtree

BASE_DIR = Path(__file__).resolve().parent.parent


def remove_data(static: bool = True, media: bool = True, db: bool = True):
    rmtree(BASE_DIR / 'static', ignore_errors=True) if static else None
    rmtree(BASE_DIR / 'media', ignore_errors=True) if media else None
    (BASE_DIR / 'core' / 'db.sqlite3').unlink(missing_ok=True) if db else None


if __name__ == '__main__':
    remove_data()
