# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PD_Dialog_helpabout.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 400)
        Dialog.setMaximumSize(QtCore.QSize(400, 400))
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Netherlands))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 340, 340, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.Text = QtWidgets.QLabel(Dialog)
        self.Text.setGeometry(QtCore.QRect(40, 30, 340, 300))
        self.Text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Text.setObjectName("Text")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Help about"))
        self.Text.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Pressure Drop</span></p><p><br/></p><p>A simple pressure drop calculator written in Python</p><p>Author: Frans van Genesen<br/>Date: May 22 - 2021</p><p>Version 1.0</p><p><br/></p><p>License: GNU GENERAL PUBLIC LICENSE Version 3</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

