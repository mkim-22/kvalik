import sys

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QMessageBox

from forms.edit_booking import EditBookingWindow
from ui.admin_bookings_ui import Ui_Admin_Wind
from sql.db_sql import get_all_bookings, delete_booking, get_booking_by_id, update_booking, get_bookings_by_date_range


class AdminBookingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Admin_Wind()
        self.ui.setupUi(self)

        self.setWindowTitle("Бронирования — Администратор")

        # --- Используем таблицу из UI-файла ---
        self.table = self.ui.bookings_table

        # --- Модель таблицы ---
        self.model = QStandardItemModel()
        self.table.setModel(self.model)

        self.ui.btn_edit.clicked.connect(self.edit_selected_booking)
        self.ui.btn_delete.clicked.connect(self.delete_selected_booking)

        self.ui.btn_filter.clicked.connect(self.filter_by_dates)
        self.ui.btn_show_all.clicked.connect(self.load_bookings)

        # --- Загружаем данные ---
        self.load_bookings()


    # ==========================================================
    # Заполняем таблицу из БД (первый базовый вариант)
    # ==========================================================
    def load_bookings(self):
        bookings = get_all_bookings()

        # Заголовки
        headers = ["ID", "Guest ID", "Room ID", "Check-In", "Check-Out", "Status", "Price"]
        self.model.setHorizontalHeaderLabels(headers)

        self.model.removeRows(0, self.model.rowCount())

        # Добавляем строки
        for row_data in bookings:
            row = []
            for key in ["id", "guest_id", "room_id", "check_in", "check_out", "status", "price"]:
                item = QStandardItem(str(row_data[key]))
                row.append(item)

            self.model.appendRow(row)


    # Научим окно узнавать выделенную строку
    def get_selected_row(self):
        indexes = self.ui.bookings_table.selectionModel().selectedRows()
        if not indexes:
            return None
        return indexes[0].row()


    # функция удаления
    def delete_selected_booking(self):
        row = self.get_selected_row()
        if row is None:
            QMessageBox.warning(self, "Ошибка", "Выберите запись!")
            return

        booking_id = int(self.model.item(row, 0).text())  # 0-й столбец = ID

        confirm = QMessageBox.question(
            self,
            "Удаление",
            f"Удалить бронь №{booking_id}?",
            QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            if delete_booking(booking_id):
                QMessageBox.information(self, "Успех", "Бронь удалена.")
                self.load_bookings()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить бронь.")

    # Редактирование
    def edit_selected_booking(self):
        row = self.get_selected_row()
        if row is None:
            QMessageBox.warning(self, "Ошибка", "Выберите запись!")
            return

        booking_id = int(self.model.item(row, 0).text())
        booking = get_booking_by_id(booking_id)

        def on_save(room_id, price):
            update_booking(booking_id, room_id, price)
            self.load_bookings()

        self.edit_window = EditBookingWindow(booking, on_save)
        self.edit_window.show()


    # фильтр
    def filter_by_dates(self):
        date_from = self.ui.date_from.date().toString("yyyy-MM-dd")
        date_to = self.ui.date_to.date().toString("yyyy-MM-dd")

        if date_from > date_to:
            QMessageBox.warning(self, "Ошибка", "Дата начала больше даты окончания!")
            return

        bookings = get_bookings_by_date_range(date_from, date_to)

        # Очищаем модель
        self.model.removeRows(0, self.model.rowCount())

        # Заполняем таблицу
        for row_data in bookings:
            row = []
            for key in ["id", "guest_id", "room_id", "check_in", "check_out", "status", "price"]:
                item = QStandardItem(str(row_data[key]))
                row.append(item)
            self.model.appendRow(row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminBookingsWindow()
    window.show()
    sys.exit(app.exec())
