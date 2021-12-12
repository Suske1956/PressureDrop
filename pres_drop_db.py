import sqlite3


"""
This module contains all classes required to perform database operations.
November 07, 2021: first issue is finished. The module contains the constants required for sqlite database operation
and a class DbOperations. containing functions:
refresh_database    drops table fittings and created the table again. In case no database present yet there will be 
                    an error 'no such table: fittings' which is no problem since the table will created in the 
                    new database which will be created on connecting to the database. 
list_tables         gives a list of tables
fitting_add         add a record to the table fittings
fitting_remove      remove a record from the table fittings by rowid
fittings_list       gives a list of tuples containing the data in table fittings with rowid. 

note: since name is unique name can be used to remove a specific record as well. 
"""


"""
constants: consider changing the constants to make the database application more universal.
Approach can be moving the constants to a class with parameters for:  
database name       string
table name          string
fields              dictionary
From these variables the class generates the variables below which makes the class reusable for other tables.   
"""
DB_NAME = "pres_drop.db"
LIST_TABLES = """SELECT name FROM sqlite_master WHERE type='table';"""
DROP_TABLE_FITTINGS = """DROP TABLE fittings"""
CREATE_TABLE_FITTINGS = """CREATE TABLE fittings (
                            fitting_name TEXT NOT NULL UNIQUE,
                            fitting_friction_factor REAL NOT NULL,
                            fitting_notes TEXT);"""
FITTINGS_ADD_RECORD = """INSERT INTO fittings
                            (fitting_name, fitting_friction_factor, fitting_notes)
                            VALUES (?, ?, ?);"""
# van shopping list: """UPDATE products SET prod_required = ? WHERE rowid = ?"""
FITTINGS_CHANGE_RECORD = """ UPDATE fittings SET 
                             fitting_friction_factor = ?,
                             fitting_notes = ?
                             WHERE fitting_name = ?"""
FITTINGS_DELETE_ONE_RECORD = """DELETE FROM fittings WHERE rowid = ?"""
FITTINGS_GET_ALL_RECORDS = """SELECT rowid, * FROM fittings"""
FITTINGS_GET_ONE_RECORD = """SELECT rowid, * FROM fittings WHERE rowid = ?"""


class DbOperations:
    """
    This class contains functions to initiate a fresh database and populate it with the required tables.
    The functions can be used to refresh the database, in case of corrupted data.
    """
    def __init__(self):
        self.db_name = DB_NAME

    def refresh_database(self):
        """
        This function erases the current table and populates the database with a new table.
        If the database does not exist a new database is created. In that case an error is generated because the table
        fittings does not exist in the freshly created database.
        The database name is established in constant DB_NAME
        :return:
        result_errors - number of errors, int
        result_texts - list of strings
        """
        conn = None
        result_errors = 0
        result_texts = []
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(DROP_TABLE_FITTINGS)
            conn.commit()
            c.close()
            result_texts.append("table fittings removed")
        except sqlite3.Error as error:
            result_errors += 1
            result_texts.append(error)
        finally:
            if conn:
                conn.close()

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(CREATE_TABLE_FITTINGS)
            conn.commit()
            c.close()
            result_texts.append("table fittings created")
        except sqlite3.Error as error:
            result_errors += 1
            result_texts.append(error)
        finally:
            if conn:
                conn.close()
        return result_errors, result_texts

    def list_tables(self):
        """
        This function returns a tuple with a finish code (0 = no problem; 1 = error) and the output.
        Error code 0: it returns a list of the tables as established in DB_NAME. - (0, <list>)
        Error code 1 it returns the error as string. - (1, <error text>)
        :return:
        (finish_code, table_list)   (int, list) or, in case of an error (int, string)
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

    def fittings_change(self, change_tuple):
        """
        Change a record from the table fittings.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(FITTINGS_CHANGE_RECORD, change_tuple)
            conn.commit()
            c.close()
            finish_code = 0
            return_message = "record was changed successfully"
        except sqlite3.Error as error:
            finish_code = 1
            return_message = error
        finally:
            if conn:
                conn.close()
        return finish_code, return_message

    def fitting_add(self, add_tuple):
        """
        Add a record to the table fittings.
        name = name of the fitting. It should be unique - see constant CREATE_TABLE_FITTINGS.
        friction factor is a real number to be used in calculating the pressure drop.
        notes is a text field to store notes regarding the fitting.
        both name and friction factor must be filled out to add the record.
        param add_tuple: (fitting name - string, fitting friction factor - real,  notes - string)
        :return:
        (finish_code, return_message)
        """
        conn = None
        if add_tuple[0] == "" or add_tuple[1] == "":
            finish_code = 1
            return_message = "fields name and fiction factor must be filled"
        else:
            try:
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                c.execute(FITTINGS_ADD_RECORD, add_tuple)
                conn.commit()
                c.close()
                finish_code = 0
                return_message = "record added successfully"
            except sqlite3.Error as error:
                finish_code = 1
                return_message = error
            finally:
                if conn:
                    conn.close()
        return finish_code, return_message

    def fitting_remove(self, row_id):
        """
        removes a record from the table fittings
        finish_code = 0: no errors and 1 in case of an error
        finish text = message record was removed or error from sqlite3
        :param row_id: row id of the record to be removed
        :return: (finish_code, finish_text)
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(FITTINGS_DELETE_ONE_RECORD, (str(row_id),))
            conn.commit()
            c.close()
            finish_code = 0
            finish_text = "record with rowid: " + str(row_id) + " removed successfully"
        except sqlite3.Error as error:
            finish_code = 1
            finish_text = error
        finally:
            if conn:
                conn.close()
        return finish_code, finish_text

    def fittings_list(self):
        """
        Reads the table fittings and returns a tuple containing:
        - error code: 0 = no problems; 1 = error occurred.
        - all data as a list of tuples. Each tuple contains: row index, fitting name, friction factor, additional notes
        - error text  sqlite3 error or "no errors"
        :return:
        (finish code, data = list of tuples, error text)
        """
        conn = None
        finish_code = 0
        error_text = "no errors"
        records = None
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(FITTINGS_GET_ALL_RECORDS)
            records = c.fetchall()
            c.close()
        except sqlite3.Error as error:
            finish_code = 1
            error_text = error
        finally:
            if conn:
                conn.close()
        return finish_code, records, error_text

    def fittings_get_one_record(self, row_id):
        """
        Reads one record from the table fittings with the row id given.
        :return: a tuple of:  finish_code, record, error_text
        finish code: 0 - no error; 1 - SQLite error
        record: tuple - (rowid - integer, fitting name - string, friction factor - real, notes - string)
        SQLiter error: error text - string
        """
        conn = None
        record = None
        finish_code = 0
        error_text = "No error"
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(FITTINGS_GET_ONE_RECORD, (str(row_id), ))
            record = c.fetchone()
            c.close()
        except sqlite3.Error as error:
            finish_code = 1
            error_text = error
        finally:
            if conn:
                conn.close()
        return finish_code, record, error_text


# database = DbOperations()
# print(database.fitting_add("valve0", 12.5, "remarks"))


"""
database = DbOperations()
print(database.fittings_get_one_record(1))
print(database.refresh_database())
print(database.fitting_add("valve0", 12.5, "remarks"))
print(database.fitting_add("valve1", 12.5, "remarks"))
print(database.fitting_add("valve2", 12.5, "remarks"))
print(database.fitting_add("valve3", 12.5, "remarks"))
print(database.fitting_add("valve4", 12.5, "remarks"))
print(database.fitting_add("valve5", 12.5, "remarks"))
print(database.fitting_add("valve6", 12.5, "remarks"))
print(database.fitting_add("valve7", 12.5, "remarks"))
print(database.fitting_add("valve8", 12.5, "remarks"))
print(database.fitting_add("valve9", 12.5, "remarks"))
print(database.fitting_add("valve10", 12.5, "remarks"))
print(database.fittings_list())
print(database.fitting_remove(10))
print(database.fittings_list())
"""
