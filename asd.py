import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QApplication
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class AdminBookingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Бронирования — Администратор")

        # Основной layout
        layout = QVBoxLayout()

        # ---- Панель кнопок ----
        btn_layout = QHBoxLayout()

        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")

        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)

        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)

        layout.addLayout(btn_layout)

        # ---- Таблица ----
        self.table = QTableView()
        layout.addWidget(self.table)

        # ---- Модель ----
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "ID", "Гость", "Комната", "Заезд", "Выезд", "Статус", "Цена"
        ])
        self.table.setModel(self.model)

        # ---- Реакция на выбор строки ----
        self.table.selectionModel().selectionChanged.connect(self.on_row_selected)

        self.setLayout(layout)


    def on_row_selected(self, selected, deselected):
        indexes = self.table.selectionModel().selectedRows()
        if indexes:
            self.btn_edit.setEnabled(True)
            self.btn_delete.setEnabled(True)
        else:
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminBookingsWindow()
    window.show()
    sys.exit(app.exec())