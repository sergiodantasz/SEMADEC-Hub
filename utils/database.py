from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from mysql.connector import connect
from mysql.connector.errors import DatabaseError, ProgrammingError

DOTENV_PATH = Path(__file__).parent.parent / '.env'

load_dotenv(DOTENV_PATH, override=True)


class DB:
    def __init__(self) -> None:
        self.name = getenv('DB_NAME', '')
        self.user = getenv('DB_USER', '')
        self.password = getenv('DB_PASSWORD', '')
        self.host = getenv('DB_HOST', '')
        self.__connection, self.__cursor = self.connect()

    def connect(self):
        """Connect to the database and return the connection and cursor. If the database does not exists, sys is used."""
        try:
            connection = connect(
                database=self.name,
                user=self.user,
                password=self.password,
                host=self.host
            )
        except ProgrammingError:
            connection = connect(
                database='sys',
                user=self.user,
                password=self.password,
                host=self.host
            )
        print(f'The connection was started ({connection.database}).')
        return connection, connection.cursor(buffered=True)

    def create_database(self) -> None:
        """Create the database."""
        operation = f'CREATE DATABASE {self.name};'
        try:
            self.__cursor.execute(operation)
            self.__connection.commit()
            print('The database was created.')
            self.__connection, self.__cursor = self.connect()
        except DatabaseError:
            print('The database already exists.')

    def drop_database(self) -> None:
        """Drop the database."""
        operation = f'DROP DATABASE {self.name};'
        try:
            self.__cursor.execute(operation)
            self.__connection.commit()
            print('The database was dropped.')
            self.__connection, self.__cursor = self.connect()
        except DatabaseError:
            print('The database does not exists.')


if __name__ == '__main__':
    database = DB()
    while True:
        print('1. Create database')
        print('2. Drop database')
        print('3. Exit')
        option = input('> ')
        if option == '1':
            database.create_database()
        elif option == '2':
            database.drop_database()
        elif option == '3':
            break
        else:
            print('Option unavailable.')
