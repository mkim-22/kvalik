from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication
from ui.login_window_ui import Ui_login_window
from forms.admin_wind import AdminBookingsWindow
from forms.client_wind import ClientWind
from forms.manager_wind import ManagerWind
from sql.db_sql import get_login
import sys

class Login_win(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login_window()
        self.ui.setupUi(self)

        self.ui.login_button.clicked.connect(self.login)
        self.ui.reg_button.clicked.connect(self.open_register_window)

    def open_register_window(self):
        from widgets.reg_widget import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()


    def login(self):
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()

        ok, role = get_login(login, password)
        if ok:
            QMessageBox.information(self, "Success", f"Вход {role}")
            self.open_wind(role)
        else:
            QMessageBox.warning(self, "Mis", "Ошибка")



    def open_wind(self, role):
        if role == 'admin':
            self.new_wind = AdminBookingsWindow()
        elif role == 'manager':
            self.new_wind = ManagerWind()
        else:
            self.new_wind = ClientWind()

        self.new_wind.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login_win()
    window.show()
    sys.exit(app.exec())