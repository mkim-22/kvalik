import sys

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from widgets.edit_booking import EditBookingWindow
from ui.admin_bookings_ui import Ui_Admin_Wind
from sql.db_sql import get_all_bookings, delete_booking, get_booking_by_id, update_booking, get_bookings_by_date_range, \
    get_guest_by_id, delete_guest, get_all_guests


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

        # --- Вкладка Гостей ---
        self.guests_model = QStandardItemModel()
        self.ui.table_guests.setModel(self.guests_model)

        self.ui.btn_add_guest.clicked.connect(self.open_add_guest_window)
        self.ui.btn_edit_guest.clicked.connect(self.edit_selected_guest)
        self.ui.btn_delete_guest.clicked.connect(self.delete_selected_guest)

        self.load_guests()

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

    # ================================
    # Загрузка гостей в таблицу
    # ================================
    def load_guests(self):
        guests = get_all_guests()

        headers = ["ID", "Имя", "Фамилия", "Отчество", "Телефон"]
        self.guests_model.setHorizontalHeaderLabels(headers)
        self.guests_model.removeRows(0, self.guests_model.rowCount())

        for g in guests:
            row = []
            for key in ["id", "name", "surname", "lastname", "phone"]:
                item = QStandardItem(str(g[key]))
                row.append(item)
            self.guests_model.appendRow(row)

    # Получаем индекс выбранной строки
    def get_selected_guest_row(self):
        indexes = self.ui.table_guests.selectionModel().selectedRows()
        if not indexes:
            return None
        return indexes[0].row()

    # ================================
    # Добавление гостя
    # ================================
    def open_add_guest_window(self):
        from widgets.add_guest_widget import AddGuestWindow
        self.add_guest_win = AddGuestWindow(self.load_guests)
        self.add_guest_win.show()

    # ================================
    # Редактирование
    # ================================
    def edit_selected_guest(self):
        row = self.get_selected_guest_row()
        if row is None:
            QMessageBox.warning(self, "Ошибка", "Выберите гостя!")
            return

        guest_id = int(self.guests_model.item(row, 0).text())
        guest = get_guest_by_id(guest_id)

        from widgets.edit_guest_widget import EditGuestWindow
        self.edit_guest_win = EditGuestWindow(guest, self.load_guests)
        self.edit_guest_win.show()

    # ================================
    # Удаление
    # ================================
    def delete_selected_guest(self):
        row = self.get_selected_guest_row()
        if row is None:
            QMessageBox.warning(self, "Ошибка", "Выберите гостя!")
            return

        guest_id = int(self.guests_model.item(row, 0).text())

        confirm = QMessageBox.question(
            self,
            "Удаление",
            f"Удалить гостя №{guest_id}?",
            QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            delete_guest(guest_id)
            self.load_guests()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminBookingsWindow()
    window.show()
    sys.exit(app.exec())
