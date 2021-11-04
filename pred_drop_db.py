import sqlite3


"""
This module contains all classes required to perform database operations.
"""


# constants - consider moving this section, or a part of it, to the user interface.
DB_NAME = "pres_drop.db"
LIST_TABLES = """SELECT name FROM sqlite_master WHERE type='table';"""


class DbOperations:
    """
    This class contains functions to initiate a fresh database and populate it with the required tables.
    The functions can be used to refresh the database, in case of corrupted data.
    """
    def __init__(self):
        self.db_name = DB_NAME

    def refresh_database(self):
        """
        This function erases the current database and starts a new one which is populated with the required table(s)
        The database name is established in constant DB_NAME
        todo: insert code
        :return: result text   -  string
        """
        pass

    def list_tables(self):
        """
        This function returns a tuple with a finish code (0 = no problem; 1 = error) and the output.
        Error code 0: it returns a list of the tables as established in DB_NAME. - (0, <list>)
        Error code 1 it returns the error as string. - (1, <error text>)
        :return:
        (finish_code, table_list)   (int, list) or (int, string)
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(LIST_TABLES)
            conn.commit()
            tables = (c.fetchall())
            c.close()
            return 0, tables
        except sqlite3.Error as error:
            return 1, error
        finally:
            if conn:
                conn.close()


database = DbOperations()
result = database.list_tables()
print(result)
