import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pd_database
import pres_drop_db
"""
control script to manage pres_drop.db from a PyQt5 widget.
pd_database and pres_drop_db are inherited

"""

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = pd_database.Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
