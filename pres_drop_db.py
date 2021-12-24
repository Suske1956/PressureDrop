import sqlite3

"""
This module contains all classes required to perform database operations on table fittings.
It contains one class: DbOperations containing all methods required. 
"""

"""
Examples to use the methods: 
# load the class DbOperations
database = DbOperations()

# get the information from one with id = 1
print(database.fittings_get_one_record(1))

# change record with rowid = 2
change_tuple = ("testdb1", 12.3, "dit is de test", 2)
print(database.fittings_change(change_tuple))

# add record to the database
print(database.fitting_add("valve0", 12.5, "remarks"))

# get a list of records in the database
print(database.fittings_list())

# remove record with rowid = 10
print(database.fitting_remove(10))

# drop table fittings, create table fittings again and load standard values from
# FITTINGS_STANDARD_TUPLE.
print(database.refresh_database())
"""

"""
This module is specific for database "pres_drop.db" with table "fittings" and fields. 
to move to a more universal module the database- and table names can be set during initiation of the module. 
The same goes for the SQLite commands needed to maintain the database and last, but not least the tuple
holding the standard fields. The constants will be removed from this module and replaced by variables in the class. 
"""

# constants
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
FITTINGS_CHANGE_RECORD = """ UPDATE fittings SET 
                             fitting_name = ?,
                             fitting_friction_factor = ?,
                             fitting_notes = ?
                             WHERE rowid = ?"""
FITTINGS_DELETE_ONE_RECORD = """DELETE FROM fittings WHERE rowid = ?"""
FITTINGS_GET_ALL_RECORDS = """SELECT rowid, * FROM fittings"""
FITTINGS_GET_ONE_RECORD = """SELECT rowid, * FROM fittings WHERE rowid = ?"""
# fittings standard list ref Bohl pages 144 ....
FITTINGS_STANDARD_TUPLE = (("Globe valve straight", 4, "standard item"),
                           ("Globe valve angle", 3, "standard item"),
                           ("Globe valve 45°", 1, "standard item"),
                           ("Bend, 90° R/d = 1", 0.3, "standard item"),
                           ("Bend, 90° R/d = 2", 0.2, "standard item"))


class DbOperations:
    """
    This class contains functions to initiate a fresh database and populate it with the required tables.
    The functions can be used to refresh the database, in case of corrupted data.
    """

    def __init__(self):
        self.db_name = DB_NAME

    def refresh_database(self):

        """
        This function drops the current table fittings and a new table.
        If the database does not exist a new database is created. In that case an error is generated because the table
        fittings does not exist in the freshly created database.
        The database name is established in constant DB_NAME
        Next the table is populated with the standard records from FITTINGS_STANDARD_TUPLE
        :return:        (result_errors - integer - - number of errors,
                        result_texts - list of strings representing the result of the several actions)
        """
        conn = None
        result_errors = 0
        result_texts = []

        # drop table fittings
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

        # create new table fittings
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

        # populate table with standard values
        for fitting in FITTINGS_STANDARD_TUPLE:
            result = self.fitting_add(fitting)
            result_errors = result_errors + result[0]
            result_texts.append(result[1])
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

    def fitting_change(self, change_tuple):
        """
        Change a record from the table fittings.
        change_tuple:   (<name> -  string,
                         <friction factor> - real,
                         <notes> - string,
                         <rowid> - integer)
        :return:         (finish_code - integer - 0 = no error, 1 = error,
                         return_message - string)
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
            return_message = str(error)
        finally:
            if conn:
                conn.close()
        return finish_code, return_message

    def fitting_add(self, add_tuple):
        """
        Add a record to the table fittings.
        add_tuple   (<name of the fitting> - string - must be unique,
                    <friction factor> - real,
                    <notes> - string)
        :return:     (finish_code - integer - 0 = no error; 1 =error,
                    return_message - string)
        """

        conn = None
        # check if required data are available.
        if add_tuple[0] == "" or add_tuple[1] == "":
            finish_code = 1
            return_message = "fields name and fiction factor must be filled"
        else:
            # add record
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
                return_message = str(error)
            finally:
                if conn:
                    conn.close()
        return finish_code, return_message

    def fitting_remove(self, row_id):
        """
        removes a record from the table fittings
        row_id: integer, row id of the record to be removed
        :return:    (finish_code - integer - 0 = no error; 1 =error,
                    return_message - string)
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
        :return:    (finish_code - integer - 0 = no error; 1 - error occurred,
                    records - list of tuples, containing the data,
                    error_text - string)
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

    def fitting_get_record(self, row_id):
        """
        Reads one record from the table fittings.
        row_id: integer - row id of the row to be read.
        :return:    (finish_code - integer - 0 = no errors; 1 = error occurred,
                    record - tuple - data of the record, None in case of an error
                    error_text - string)
        """
        conn = None
        record = None
        finish_code = 0
        error_text = "No error"
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(FITTINGS_GET_ONE_RECORD, (str(row_id),))
            record = c.fetchone()
            c.close()
        except sqlite3.Error as error:
            finish_code = 1
            error_text = str(error)
        finally:
            if conn:
                conn.close()
            if record is None:
                finish_code = 1
                error_text = "No record data"
        return finish_code, record, error_text
