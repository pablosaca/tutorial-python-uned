import sqlite3
import pandas as pd


class DataBaseProject:
    def __init__(self, db_name):
        self.db_name = db_name

        self.connection = None  # se ccrea al conectar la database

    def db_connect(self):
        """
        Connect to data base. If there is not a database, it is created
        :param db_name: str
        :return None
        """
        self.connection = sqlite3.connect(f"{self.db_name}.db")

    def write_table(self, df: pd.DataFrame, table_name: str, if_exists: str = "replace"):
        """

        :param df: pd.DataFrame
        :param table_name: str
        :param if_exists: str
        :return None:
        """
        if self.connection is not None:
            df.to_sql(table_name, self.connection, if_exists=if_exists, index=False)
        else:
            raise RuntimeError("No database connection. You must connect to the database previously")
