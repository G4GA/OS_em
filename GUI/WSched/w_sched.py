"""
Parent class for scheduler GUI
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
)

class SchedWindow(QMainWindow):
    def __init__(self, layout):
        super().__init__()
        self._components = {
            'main_widget': QWidget(),
            'main_layout': layout,
        }

        self._init_window()

    @property
    def main_widget(self):
        return self._components['main_widget']

    @property
    def main_layout(self):
        return self._components['main_layout']

    def _init_window(self):
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
