from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from sql.db_sql import add_guest


class AddGuestWindow(QWidget):
    def __init__(self, on_save_callback):
        super().__init__()
        self.on_save_callback = on_save_callback

        self.setWindowTitle("Добавление гостя")
        layout = QVBoxLayout()

        self.input_name = QLineEdit()
        self.input_surname = QLineEdit()
        self.input_lastname = QLineEdit()
        self.input_phone = QLineEdit()

        layout.addWidget(QLabel("Имя"))
        layout.addWidget(self.input_name)

        layout.addWidget(QLabel("Фамилия"))
        layout.addWidget(self.input_surname)

        layout.addWidget(QLabel("Отчество"))
        layout.addWidget(self.input_lastname)

        layout.addWidget(QLabel("Телефон"))
        layout.addWidget(self.input_phone)

        btn = QPushButton("Добавить")
        btn.clicked.connect(self.save_data)
        layout.addWidget(btn)

        self.setLayout(layout)

    def save_data(self):
        name = self.input_name.text()
        surname = self.input_surname.text()
        lastname = self.input_lastname.text()
        phone = self.input_phone.text()

        if not all([name, surname, lastname, phone]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        add_guest(name, surname, lastname, phone)
        self.on_save_callback()
        self.close()
