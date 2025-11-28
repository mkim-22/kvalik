
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_login_window(object):
    def setupUi(self, login_window):
        login_window.setObjectName("login_window")
        login_window.resize(519, 397)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=login_window)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(110, 70, 331, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.login_input = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.login_input.setObjectName("login_input")
        self.verticalLayout.addWidget(self.login_input)
        self.password_input = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("password_input")
        self.verticalLayout.addWidget(self.password_input)
        self.login_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.login_button.setObjectName("login_button")
        self.verticalLayout.addWidget(self.login_button)
        self.reg_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.reg_button.setObjectName("reg_button")
        self.verticalLayout.addWidget(self.reg_button)


        self.retranslateUi(login_window)
        QtCore.QMetaObject.connectSlotsByName(login_window)

    def retranslateUi(self, login_window):
        _translate = QtCore.QCoreApplication.translate
        login_window.setWindowTitle(_translate("login_window", "Form"))
        self.label.setText(_translate("login_window", "Авторизация"))
        self.login_button.setText(_translate("login_window", "Войти"))
        self.reg_button.setText(_translate("login_window", "Регистрация"))
