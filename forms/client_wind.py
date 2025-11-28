import sys

from PyQt6.QtWidgets import QMainWindow, QApplication
from  ui.client_window_ui import Ui_login_window

class ClientWind(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_login_window()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = ClientWind()
    wind.show()
    sys.exit(app.exec())