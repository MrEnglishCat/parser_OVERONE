import re
import sqlite3
import psycopg2
from .data_client import DataClient





class Parser_postgresql(DataClient):
    DB_NAME = "TEST"
    # DB_NAME = "test"
    USER = "postgres"
    PASSWORD = "postgres"
    HOST = "localhost"
    PORT = "5432"

    def connect_to_db(self):
        try:
            connection = psycopg2.connect(dbname=self.DB_NAME, user=self.USER, password=self.PASSWORD, host=self.HOST,
                                          port=self.PORT)
        except Exception as e:
            print(e)
            connection = False

        return connection

    def create_table_db(self, connection):
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (id serial PRIMARY KEY , link text, price NUMERIC(10, 4), description text, parse_date_time TIMESTAMP)")
            connection.commit()
        else:
            print(connection, 'ERROR CONNECTION TO DB!')

    def get_data_from_db(self, connection):
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {self.TABLE_NAME} ORDER BY price")
            data = cursor.fetchall()

            return data




class Parser_sqlite(DataClient):
    DB_NAME = "TEST"

    def connect_to_db(self):
        try:
            connection = sqlite3.connect("kufar.db")
        except:
            connection = False

        return connection



    def create_table_db(self, connection):
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (id INTEGER PRIMARY KEY, link text, price INTEGER, description text)")
            connection.commit()
        else:
            print(connection, 'ERROR CONNECTION TO DB!')




mebel = Parser_postgresql()
mebel.run()





