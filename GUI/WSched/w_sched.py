from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
)

class SchedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__components = {
            'main_widget': QWidget(),
            'main_layout': QVBoxLayout()
        }

    @property
    def main_widget(self):
        return self.__components['main_widget']

    @property
    def main_layout(self):
        return self.__components['main_layout']

    def _init_window(self):
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

