import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pd_database
from pres_drop_db import DbOperations
from pd_database_dialog import Ui_Dialog
"""
control script to manage pres_drop.db from a PyQt5 widget.
pd_database and pres_drop_db are inherited
"""


class DialogShow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DialogShow, self).__init__(parent)
        self.db = DbOperations()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def view_record(self, data):
        self.ui.fitting_name.setReadOnly(True)
        self.ui.fitting_name.setText(data[1])
        self.ui.friction_factor.setReadOnly(True)
        self.ui.friction_factor.setText(str(data[2]))
        self.ui.fitting_note.setReadOnly(True)
        self.ui.fitting_note.setPlainText(data[3])
        self.ui.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.ui.header.setText("View Record# " + str(data[0]))
        self.ui.buttonBox.accepted.connect(self.stop_view)

    def add_record(self):
        self.ui.header.setText("Add new record")
        self.ui.buttonBox.accepted.connect(self.stop_add)

    def change_record(self):
        self.ui.header.setText("Change record# " + "number")
        self.ui.buttonBox.accepted.connect(self.stop_editing)

    def stop_view(self):
        self.close()

    def stop_add(self):
        """
        Validate input, write new record to database and stop dialog
        """
        print("stop add record")
        self.close()

    def stop_editing(self):
        """"
        Validate input, write data to database and stop dialog
        """
        print("stop editing")
        self.close()


class DbFormExec:
    """
    Shows the form pd_database.py and populates the listbox with all fitting data from press_drop_db.
    For each buttons on pd_database.py a function is defined. See documentation iin each function.
    """
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        form = QtWidgets.QWidget()
        self.db = DbOperations()
        self.ui = pd_database.Ui_fittings_table_mainenance()
        self.ui.setupUi(form)

        self.refresh_form()

        # make connections
        self.ui.button_show_record.clicked.connect(self.show_item)
        self.ui.button_add_record.clicked.connect(self.add_item)
        self.ui.button_delete_record.clicked.connect(self.delete_item)
        self.ui.button_change_record.clicked.connect(self.change_item)
        self.ui.button_refresh.clicked.connect(self.refresh_database)
        self.ui.button_close.clicked.connect(self.close_window)

        form.show()
        sys.exit(app.exec_())

    def refresh_form(self):
        # set column with in tableWidget
        self.ui.table_fittings.setColumnWidth(0, 72)
        self.ui.table_fittings.setColumnWidth(1, 300)
        self.ui.table_fittings.setColumnWidth(2, 125)
        fitting_lst = self.db.fittings_list()
        error_code = fitting_lst[0]
        if error_code == 0:
            records = fitting_lst[1]
        else:
            records = []

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
        # data_returned = self.db.show_record(row_chosen)
        data_returned = self.db.fittings_get_one_record(row_chosen)[1]
        dialog = DialogShow()
        dialog.view_record(data_returned)
        dialog.exec()

    def add_item(self):
        dialog = DialogShow()
        dialog.add_record()
        dialog.exec()

    def delete_item(self):
        box = QtWidgets.QMessageBox()
        print(box.exec_())
        print("delete record dummy")

    def change_item(self):
        dialog = DialogShow()
        dialog.change_record()
        dialog.exec()

    def refresh_database(self):
        box = QtWidgets.QMessageBox()
        box.exec_()
        print("refresh database dummy")
        # print(self.db.refresh_database())  # the real code. Uncomment when programming of the warning is done

    @staticmethod
    def close_window():
        """Close the window. In future additional code can be added in case of closing the window"""
        QtWidgets.qApp.quit()


if __name__ == "__main__":
    DbFormExec()
