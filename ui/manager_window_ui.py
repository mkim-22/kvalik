from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_login_window(object):
    def setupUi(self, login_window):
        login_window.setObjectName("login_window")
        login_window.resize(519, 397)

        self.retranslateUi(login_window)
        QtCore.QMetaObject.connectSlotsByName(login_window)

    def retranslateUi(self, login_window):
        _translate = QtCore.QCoreApplication.translate
        login_window.setWindowTitle(_translate("login_window", "Form"))