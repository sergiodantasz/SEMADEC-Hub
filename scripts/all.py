from os import system
from sys import argv

system('python scripts/removemigrations.py')
system('python scripts/removedata.py')
system('python scripts/makemigrations.py')
system('python scripts/migrate.py')
system('python scripts/collectstatic.py')

if '-r' not in argv:
    system('python scripts/runserver.py')
