from os import system
from sys import argv

system('python scripts/removemigrations.py')
system('python scripts/removedata.py')

system('python manage.py makemigrations')
system('python manage.py migrate')
system('python manage.py collectstatic --no-input --clear')

if '-r' not in argv:
    system('python manage.py runserver')
