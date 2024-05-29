from os import system
from sys import argv

from removedata import remove_data
from removemigrations import remove_migrations

if __name__ == '__main__':
    remove_migrations()
    remove_data()

    system('python manage.py makemigrations')
    system('python manage.py migrate')
    system('python manage.py collectstatic --no-input --clear')

    if '-r' not in argv:
        system('python manage.py runserver')
