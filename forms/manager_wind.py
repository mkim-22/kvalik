from PyQt6.QtWidgets import QMainWindow
from ui.manager_window_ui import Ui_login_window

class ManagerWind(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_login_window()
        self.ui.setupUi(self)
