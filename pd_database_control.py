import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pd_database
import pd_database_record
from pres_drop_db import DbOperations
from pd_database_dialog import Ui_Dialog
"""
control script to manage pres_drop.db from a PyQt5 widget.
pd_database and pres_drop_db are inherited
"""


class DatabaseOperations:
    """
    class performing all database operations required
    """
    def __init__(self):
        self.db = DbOperations()

    def list_records(self):
        """
        Generates and returns a list of all records from the table fittings. in case of a SQLite error nothing will
        be returned.
        todo: action in case error_code = 1  ==> show popup error message with error text
        :return: fitting_lst[1]  list of tuples with (for each record): rowid; fitting name; friction factor
        """

        fitting_lst = self.db.fittings_list()
        error_code = fitting_lst[0]
        if error_code == 0:
            return fitting_lst[1]

    def show_record(self, _id):
        """
        Get the data from row id _id
        """
        data_returned = self.db.fittings_get_one_record(_id)
        return data_returned[1]


class DialogShow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DialogShow, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def view_record(self, _name, _factor, _notes):
        self.ui.fitting_name.setEnabled(False)
        self.ui.fitting_name.setText(_name)
        self.ui.friction_factor.setEnabled(False)
        self.ui.friction_factor.setText(_factor)
        self.ui.fitting_note.setEnabled(False)
        self.ui.fitting_note.setPlainText(_notes)
        self.ui.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.ui.header.setText("View Record")
        # self.ui.buttonBox.accepted.connect(self.ok_clicked)  # here not required

    def ok_clicked(self):
        print("ok clicked")


class DbFormExec:
    """
    Shows the form pd_database.py and populates the listbox with all fitting data from press_drop_db.
    For each buttons on pd_database.py a function is defined. See documentation iin each function.
    """
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        form = QtWidgets.QWidget()
        self.db = DatabaseOperations()
        self.ui = pd_database.Ui_fittings_table_mainenance()
        self.ui.setupUi(form)

        self.refresh_form()

        # make connections
        self.ui.button_show_record.clicked.connect(self.show_item)
        self.ui.button_close.clicked.connect(self.close_window)

        form.show()
        sys.exit(app.exec_())

    def refresh_form(self):
        # set column with in tableWidget
        self.ui.table_fittings.setColumnWidth(0, 72)
        self.ui.table_fittings.setColumnWidth(1, 300)
        self.ui.table_fittings.setColumnWidth(2, 125)

        # get list of records
        records = self.db.list_records()

        # set number of rows in tableWidget
        self.ui.table_fittings.setRowCount(len(records))

        # populate tableWidget
        row = 0
        for record in records:
            self.ui.table_fittings.setItem(row, 0, QtWidgets.QTableWidgetItem(str(record[0])))
            self.ui.table_fittings.setItem(row, 1, QtWidgets.QTableWidgetItem(record[1]))
            self.ui.table_fittings.setItem(row, 2, QtWidgets.QTableWidgetItem(str(record[2])))
            row += 1

    def show_item(self):
        """
        Shows the window pd_record.py with the data of the current item of the fittings list.
        todo: implement error handling
        :return:
        """
        row_chosen = int(self.ui.table_fittings.item(self.ui.table_fittings.currentRow(), 0).text())
        data_returned = self.db.show_record(row_chosen)
        _name = data_returned[1]
        _factor = str(data_returned[2])
        _notes = data_returned[3]

        dialog = DialogShow()
        dialog.view_record(_name, _factor, _notes)

        dialog.exec()

    def add_item(self):
        pass

    def delete_item(self):
        pass

    def change_item(self):
        pass

    def refresh_database(self):
        pass

    @staticmethod
    def close_window():
        """Close the window. In future additional code can be added in case of closing the window"""
        QtWidgets.qApp.quit()


if __name__ == "__main__":
    DbFormExec()
