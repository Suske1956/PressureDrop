import sys
from PyQt5.QtWidgets import QDialog, QApplication, QDialogButtonBox, QWidget, QTableWidgetItem, QMessageBox, qApp
import pd_database
from pres_drop_db import DbOperations
from pd_database_dialog import Ui_Dialog
"""
control script to manage pres_drop.db from a PyQt5 widget.
pd_database and pres_drop_db are inherited
"""


class GeneralMethods:
    """
    Class of universal methods and function for
    """

    @staticmethod
    def show_message(text):
        box = QMessageBox()
        box.setWindowTitle("Message")
        box.setText(text)
        box.exec_()


class DialogShow(QDialog):
    """
    Dialog to view, add or change one record.
    The dialog is started from DbFormExec
    The dialog has access to the database to write the changes
    """
    def __init__(self, parent=None):
        super(DialogShow, self).__init__(parent)
        self.db = DbOperations()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.friction_factor.editingFinished.connect(self.validate_friction_factor)

    def validate_friction_factor(self):
        try:
            float(self.ui.friction_factor.text())
        except ValueError:
            GeneralMethods.show_message("Friction factor must be a number")
            self.ui.friction_factor.setFocus()
            self.ui.friction_factor.setText("")

    def validate_input(self):
        if self.ui.fitting_name.text() != "" and self.ui.friction_factor.text() != "":
            return True
        else:
            GeneralMethods.show_message("Name and Friction factor must be a filled out")
            return False

    def view_record(self, data):
        """
        View a record. The data from the record are collected in DbFormExec and transferred to this method.
        To be considered let this dialog get the data based on ID.
        All fields are set to read only to avoid editing.
        Connecting to a stop method is not required since one command is sufficient (self.stop)
        """
        self.ui.fitting_name.setReadOnly(True)
        self.ui.fitting_name.setText(data[1])
        self.ui.friction_factor.setReadOnly(True)
        self.ui.friction_factor.setText(str(data[2]))
        self.ui.fitting_note.setReadOnly(True)
        self.ui.fitting_note.setPlainText(data[3])
        self.ui.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.ui.header.setText("View Record# " + str(data[0]))
        self.ui.buttonBox.accepted.connect(self.close)

    def add_record(self):
        """
        Set up dialog for adding a record and connect ok button to stop method (process input)
        """
        self.ui.header.setText("Add new record")
        self.ui.buttonBox.accepted.connect(self.stop_add)

    def change_record(self, data):
        """
        Set up dialog to change a record. Connect to stop method.
        todo: get row id on starting the method read data from database and show them in the dialog.
        """
        self.ui.fitting_name.setReadOnly(True)
        self.ui.fitting_name.setText(data[1])
        self.ui.friction_factor.setText(str(data[2]))
        self.ui.fitting_note.setPlainText(data[3])
        self.ui.header.setText("Change record# " + str(data[0]))
        self.ui.buttonBox.accepted.connect(self.stop_editing)

    def stop_add(self):
        """
        Validate input, write new record to database and stop dialog
        """
        if self.validate_input():
            record_add = (self.ui.fitting_name.text(),
                          float(self.ui.friction_factor.text()),
                          self.ui.fitting_note.toPlainText())
            self.db.fitting_add(record_add)
            self.close()

    def stop_editing(self):
        """"
        Validate input, write data to database and stop dialog
        todo: write code to accomplish task.
        """
        print("stop editing")
        if self.validate_input():
            record_change = (float(self.ui.friction_factor.text()),
                             self.ui.fitting_note.toPlainText(),
                             self.ui.fitting_name.text())
            self.db.fittings_change(record_change)
            self.close()


class DbFormExec:
    """
    Shows the form pd_database.py and populates the listbox with all fitting data from press_drop_db.
    For each buttons on pd_database.py a function is defined. See documentation iin each function.
    """
    def __init__(self):
        app = QApplication(sys.argv)
        form = QWidget()
        self.db = DbOperations()
        self.ui = pd_database.Ui_fittings_table_mainenance()
        self.ui.setupUi(form)
        # set column width in table.
        self.ui.table_fittings.setColumnWidth(0, 72)
        self.ui.table_fittings.setColumnWidth(1, 300)
        self.ui.table_fittings.setColumnWidth(2, 125)

        # Populate table
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
        """
        Refresh the data in table_fittings using method fittings_list in pres_drop_db.py to get the data

        """
        # get data
        fitting_lst = self.db.fittings_list()
        error_code = fitting_lst[0]
        if error_code == 0:
            records = fitting_lst[1]
        else:
            records = []
            message = "Error while reading database message code: " + str(fitting_lst[2])
            GeneralMethods.show_message(message)

        # set number of rows in tableWidget
        self.ui.table_fittings.setRowCount(len(records))

        # populate tableWidget
        row = 0
        for record in records:
            self.ui.table_fittings.setItem(row, 0, QTableWidgetItem(str(record[0])))
            self.ui.table_fittings.setItem(row, 1, QTableWidgetItem(record[1]))
            self.ui.table_fittings.setItem(row, 2, QTableWidgetItem(str(record[2])))
            row += 1

    def show_item(self):
        """
        Shows the window pd_record.py with the data of the current item of the fittings list.
        todo: implement error handling for database errors.
        :return:
        """
        if self.ui.table_fittings.rowCount() > 0:  # avoid using method on empty table
            row_chosen = int(self.ui.table_fittings.item(self.ui.table_fittings.currentRow(), 0).text())
            data_returned = self.db.fittings_get_one_record(row_chosen)[1]
            dialog = DialogShow()
            dialog.view_record(data_returned)
            dialog.exec()
        else:
            GeneralMethods.show_message("Nothing to show")

    def add_item(self):
        dialog = DialogShow()
        dialog.add_record()
        dialog.exec()
        self.refresh_form()

    def delete_item(self):
        box = QMessageBox()
        print(box.exec_())
        print("delete record dummy")

    def change_item(self):
        if self.ui.table_fittings.rowCount() > 0:  # avoid using method on empty table
            row_chosen = int(self.ui.table_fittings.item(self.ui.table_fittings.currentRow(), 0).text())
            data_returned = self.db.fittings_get_one_record(row_chosen)[1]
            dialog = DialogShow()
            dialog.change_record(data_returned)
            dialog.exec()
            self.refresh_form()
        else:
            GeneralMethods.show_message("No records to change")

    def refresh_database(self):
        message_text = ""
        box = QMessageBox()
        box.setWindowTitle("Warning")
        box.setText("Are you sure you want to reset the database. All information will be lost!!")
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setDefaultButton(QMessageBox.No)
        box.setIcon(QMessageBox.Critical)
        box_value = box.exec_()
        if box_value == QMessageBox.Yes:
            output = self.db.refresh_database()
            if output[0] == 0:
                message_text = "Database was reset successfully"
        else:
            message_text = "Database reset failed"
        GeneralMethods.show_message(message_text)
        self.refresh_form()

    @staticmethod
    def close_window():
        """Close the window. In future additional code can be added in case of closing the window"""
        qApp.quit()


if __name__ == "__main__":
    DbFormExec()
