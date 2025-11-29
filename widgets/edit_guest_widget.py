from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from sql.db_sql import update_guest


class EditGuestWindow(QWidget):
    def __init__(self, guest_data, on_save_callback):
        super().__init__()
        self.on_save_callback = on_save_callback
        self.guest_id = guest_data["id"]

        self.setWindowTitle("Редактирование гостя")
        layout = QVBoxLayout()

        self.input_name = QLineEdit(guest_data["name"])
        self.input_surname = QLineEdit(guest_data["surname"])
        self.input_lastname = QLineEdit(guest_data["lastname"])
        self.input_phone = QLineEdit(str(guest_data["phone"]))

        layout.addWidget(QLabel("Имя"))
        layout.addWidget(self.input_name)

        layout.addWidget(QLabel("Фамилия"))
        layout.addWidget(self.input_surname)

        layout.addWidget(QLabel("Отчество"))
        layout.addWidget(self.input_lastname)

        layout.addWidget(QLabel("Телефон"))
        layout.addWidget(self.input_phone)

        btn_save = QPushButton("Сохранить")
        btn_save.clicked.connect(self.save_data)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def save_data(self):
        name = self.input_name.text()
        surname = self.input_surname.text()
        lastname = self.input_lastname.text()
        phone = self.input_phone.text()

        if not all([name, surname, lastname, phone]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        update_guest(self.guest_id, name, surname, lastname, phone)
        self.on_save_callback()
        self.close()
