"""
Module for producer consumer window class
"""

from re import T
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
                             'w_dict': {
                                 'name': QLabel('Producer'),
                                 'picture': QLabel(),
                                 'p_bar': QProgressBar()
                             },
                             'pixmap': QPixmap('./GUI/WConc/green_semaphor.png')},

                'consumer': {'widget': QWidget(),
                             'layout': QVBoxLayout(),
                             'w_dict': {
                                 'name': QLabel('Consumer'),
                                 'picture': QLabel(),
                                 'p_bar': QProgressBar()
                             },
                             'pixmap': QPixmap('./GUI/WConc/red_semaphor.png')}
            },
            'buffer': {
                'widget': QWidget(),
                'layout': QVBoxLayout(),
                'w_dict': {
                         'name': QLabel('Buffer'),
                         'p_bar': QProgressBar()
                     },
            },
            'go_back_bttn': QPushButton('Return to main menu')
        }

        self._init_window()
        self._set_go_back_bttn(go_back_fn)

        self._load_style()

    def _init_window(self):
        #Set window view and name
        self.setWindowTitle('Angel Damian Raul Garcia Guevara')
        self.setFixedWidth(700)

        self._set_main_w()
        self._set_ul()
        self._set_inner_w()
        self._set_buffer()

        self._set_p_bar()

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

    def _set_p_bar(self):
        #TODO Here Implement the timers for the each p_bar
        pass

    def _set_go_back_bttn(self, go_back_fn):
        self.go_back_bttn.clicked.connect(go_back_fn)
        self._lower['layout'].addWidget(self.go_back_bttn)

    def _set_buffer(self):
        widget = self.buffer['widget']
        layout = self.buffer['layout']
        w_dict = self.buffer['w_dict']

        widget.setLayout(layout)
        widget.setFixedHeight(100)

        layout.addWidget(w_dict['name'])
        layout.addWidget(w_dict['p_bar'])

        self._upper['layout'].addWidget(widget)

    def _set_inner_w(self):
        widget = self.prod_cons['widget']
        layout = self.prod_cons['layout']
        widget.setLayout(layout)
        self._upper['layout'].addWidget(widget)
        self.set_ps(self.producer, layout)
        self.set_ps(self.consumer, layout)

    def set_ps(self, ps, p_layout):
        widget = ps['widget']
        layout = ps['layout']
        picture = ps['w_dict']['picture']

        widget.setLayout(layout)
        layout.addWidget(ps['w_dict']['name'])

        picture.setPixmap(ps['pixmap'])
        picture.setFixedSize(50, 90)
        picture.setScaledContents(True)
        layout.addWidget(picture)

        layout.addWidget(ps['w_dict']['p_bar'])
        p_layout.addWidget(widget)

    def _set_ul(self):
        self._set_vside_w(self._upper)
        self._set_vside_w(self._lower)

    def _set_vside_w(self, side_w):
        widget = side_w['widget']
        widget.setLayout(side_w['layout'])
        widget.setObjectName('sidev')
        self.main_layout.addWidget(widget)

    def _set_main_w(self):
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def _load_style(self):
        style = ''
        with open('GUI/style/sched.css', 'r', encoding='utf-8') as file:
            style = file.read()
        self.setStyleSheet(style)

