import sqlite3
import os
from sqlite3 import Error


class SqlTable():
    def __init__(self):
        self.path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\webfeature.db"
        self.create_db(self.path)

    @staticmethod
    def create_db(directory):
        try:
            connection = sqlite3.connect(directory)
        except Error as e:
            print(e)
        finally:
            connection.close()

    def create_tb(self):
        create_query = "CREATE TABLE IF NOT EXIST features (" \
                       "Url varchar(255)," \
                       ""
