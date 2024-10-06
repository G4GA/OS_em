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
                             'w_list': [],
                             'pixmap': QPixmap('./GUI/WConc/green_semaphor.png')},

                'consumer': {'widget': QWidget(),
                             'layout': QVBoxLayout(),
                             'w_list': [],
                             'pixmap': QPixmap('./GUI/WConc/red_semaphor.png')}
            },
            'buffer': {
                'widget': QWidget(),
                'layout': QVBoxLayout(),
                'w_list': []
            },
            'go_back_bttn': QPushButton('Return to main menu')
        }
        self._init_window()

        self._init_bttns(go_back_fn)

        self.setWindowTitle('Angel Damian Raul Garcia Guevara')
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

    def set_prod_cons(self):
        self.prod_cons['widget'].setLayout(self.prod_cons['layout'])
        self._upper['layout'].addWidget(self.prod_cons['widget'])

    def set_PS(self, cons_pro, pc_str):
        cons_pro['widget'].setLayout(cons_pro['layout'])
        self.prod_cons['layout'].addWidget(cons_pro['widget'])
        p_label = QLabel()
        p_label.setPixmap(cons_pro['pixmap'])
        p_label.setFixedSize(IMAGE_WIDHT, IMAGE_HEIGHT)
        p_label.setScaledContents(True)
        name_label = QLabel(pc_str)
        progress_bar = QProgressBar()
        progress_bar.setOrientation(Qt.Orientation.Horizontal)

        cons_pro['layout'].addWidget(name_label)
        cons_pro['layout'].addWidget(p_label)
        cons_pro['layout'].addWidget(progress_bar)
        cons_pro['w_list'].append(name_label)
        cons_pro['w_list'].append(p_label)

    def _set_upper_lower(self):
        self._upper['widget'].setLayout(self._upper['layout'])
        self._lower['widget'].setLayout(self._lower['layout'])

        self._upper['widget'].setObjectName('upper')
        self._lower['widget'].setObjectName('lower')

        self.main_layout.addWidget(self._upper['widget'])
        self.main_layout.addWidget(self._lower['widget'])

    def _init_bttns(self, go_back_fn):
        self._lower['layout'].addWidget(self.go_back_bttn)
        self.go_back_bttn.clicked.connect(go_back_fn)

    def _init_buffer(self):
        self.buffer['widget'].setLayout(self.buffer['layout'])
        label = QLabel('Buffer')
        p_bar = QProgressBar()
        p_bar.setOrientation(Qt.Orientation.Horizontal)
        self.buffer['layout'].addWidget(label)
        self.buffer['layout'].addWidget(p_bar)
        self._upper['layout'].addWidget(self.buffer['widget'])

    def _init_window(self):
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self._set_upper_lower()
        self.set_prod_cons()
        self.set_PS(self.producer, 'Producer')
        self.set_PS(self.consumer, 'Consumer')
        self._init_buffer()

    def _load_style(self):
        style = ''
        with open('GUI/style/sched.css', 'r', encoding='utf-8') as file:
            style = file.read()
        self.setStyleSheet(style)



