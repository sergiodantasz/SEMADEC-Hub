from pathlib import Path
from shutil import rmtree

BASE_DIR = Path(__file__).resolve().parent.parent

rmtree(BASE_DIR / 'static', ignore_errors=True)
rmtree(BASE_DIR / 'media', ignore_errors=True)
# remove database
