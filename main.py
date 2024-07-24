from GUI.menu_window import MenuWindow
from PyQt6.QtWidgets import QApplication

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    init_window = MenuWindow()

    init_window.show()

    app.exec()
