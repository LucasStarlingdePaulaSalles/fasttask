import sqlite3
from sqlite3 import Error

import pathlib

class DB_Handler:
    def __init__(self):
        # @TODO: Change default DB file path to user's local directory
        default_db_file = str(pathlib.Path(__file__).parent.parent.parent.resolve()) + '/taskdb'
        self.conn = self._create_connection(default_db_file)

    def _create_connection(self, db_file):
        connection = None
        try:
            connection = sqlite3.connect(db_file)
            return connection
        except Error as e:
            print("Unable to connect to the database")
            print(e)
