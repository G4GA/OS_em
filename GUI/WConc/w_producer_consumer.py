"""
Module for producer consumer window class
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QProgressBar
)

from PyQt6.QtGui import QPixmap

from PyQt6.QtCore import (
    Qt
)

IMAGE_HEIGHT = 50
IMAGE_WIDHT = 60

class ProdConsWindow(QMainWindow):
    def __init__(self, go_back_fn, layouts):
        super().__init__()
        self._components = {
            'main': {
                'widget': QWidget(),
                'layout': QVBoxLayout()
            },
            'upper': {
                'widget': QWidget(),
                'layout': layouts['upper']()
            },
            'lower': {
                'widget': QWidget(),
                'layout': layouts['lower']()
            },
            'prod_cons': {
                'widget': QWidget(),
                'layout': QVBoxLayout(),
                'producer': {'widget': QWidget(),
                             'layout': QVBoxLayout(),
                             'w_dict': {},
                             'pixmap': QPixmap('./GUI/WConc/green_semaphor.png')},

                'consumer': {'widget': QWidget(),
                             'layout': QVBoxLayout(),
                             'w_dict': {},
                             'pixmap': QPixmap('./GUI/WConc/red_semaphor.png')}
            },
            'buffer': {
                'widget': QWidget(),
                'layout': QVBoxLayout(),
                'w_list': []
            },
            'go_back_bttn': QPushButton('Return to main menu')
        }

        self._load_style()

    @property
    def main_widget(self):
        return self._components['main']['widget']

    @property
    def main_layout(self):
        return self._components['main']['layout']

    @property
    def _upper(self):
        return self._components['upper']

    @property
    def _lower(self):
        return self._components['lower']

    @property
    def prod_cons(self):
        return self._components['prod_cons']

    @property
    def producer(self):
        return self._components['prod_cons']['producer']

    @property
    def consumer(self):
        return self._components['prod_cons']['consumer']

    @property
    def buffer(self):
        return self._components['buffer']

    @property
    def go_back_bttn(self):
        return self._components['go_back_bttn']

    def _load_style(self):
        style = ''
        with open('GUI/style/sched.css', 'r', encoding='utf-8') as file:
            style = file.read()
        self.setStyleSheet(style)



