from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class EditBookingWindow(QWidget):
    def __init__(self, booking_data, on_save_callback):
        super().__init__()
        self.booking_data = booking_data
        self.on_save_callback = on_save_callback

        self.setWindowTitle("Редактирование бронирования")

        layout = QVBoxLayout()

        self.input_room = QLineEdit(str(booking_data["room_id"]))
        self.input_price = QLineEdit(str(booking_data["price"]))

        layout.addWidget(QLabel("Номер комнаты"))
        layout.addWidget(self.input_room)

        layout.addWidget(QLabel("Цена"))
        layout.addWidget(self.input_price)

        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save)

        layout.addWidget(save_btn)
        self.setLayout(layout)

    def save(self):
        new_room = self.input_room.text()
        new_price = self.input_price.text()

        self.on_save_callback(
            room_id=new_room,
            price=new_price
        )

        self.close()
