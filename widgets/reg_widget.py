from PyQt6.QtWidgets import QWidget, QMessageBox
from ui.register_window_ui import Ui_RegisterWindow
from sql.db_sql import register_new_client


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RegisterWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Регистрация клиента")

        self.ui.btn_register.clicked.connect(self.register_user)

    def register_user(self):
        name = self.ui.input_name.text().strip()
        surname = self.ui.input_surname.text().strip()
        lastname = self.ui.input_lastname.text().strip()
        phone = self.ui.input_phone.text().strip()
        login = self.ui.input_login.text().strip()
        password = self.ui.input_password.text().strip()

        # --- Проверка заполнения ---
        if not all([name, surname, lastname, phone, login, password]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        # --- Передаём в DB слой ---
        ok, message = register_new_client(
            name, surname, lastname, phone, login, password
        )

        if ok:
            QMessageBox.information(self, "Успех", message)
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", message)