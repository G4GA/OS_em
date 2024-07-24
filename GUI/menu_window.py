from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Setting internal attributes
        self.__components = {
            'main_layout': QGridLayout(),
            'main_widget': QWidget()
        }

        #window setting
        self.set_window()

        #Test Hello World label
        test_label = QLabel("Hello World")
        self.main_layout.addWidget(test_label)

    #define getters and setters
    @property
    def __main_layout(self):
        return self.__components['main_layout']

    @__main_layout.setter
    def __main_layout(self, main_layout: QWidget):
        self.__components['main_layout'] = main_layout

    @property
    def __main_widget(self):
        return self.__components['main_widget']

    @__main_widget.setter
    def __main_widget(self, main_widget: QWidget):
        self.__components['main_widget'] = main_widget

    def set_window(self):
        self.setWindowTitle("OS Visualization Tool")
        self.main_layout = QGridLayout()
        self.main_widget = QWidget()

        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

    def add_button(self):
        pass
