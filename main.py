from GUI.menu_window import MenuWindow
from PyQt6.QtWidgets import QApplication
from GUI.window_handler import WindowHandler

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w_handler = WindowHandler()
    w_handler.start()

    app.exec()

