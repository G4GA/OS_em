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
    QTimer
)

from Concurrency.ProdCons.buffer import Buffer
from Concurrency.ProdCons.producer import Producer
from Concurrency.ProdCons.consumer import Consumer

IMAGE_HEIGHT = 50
IMAGE_WIDHT = 60

class ProdConsWindow(QMainWindow):
    def __init__(self, go_back_fn, layouts):
        super().__init__()
        buffer = Buffer()
        self._components = {
            'pixmap_dict': {
                'green': QPixmap('./GUI/WConc/green_semaphor.png'),
                'red': QPixmap('./GUI/WConc/red_semaphor.png'),
            },
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
                                 'p_bar': QProgressBar(),
                                 'timer': QTimer()
                             },
                             'handler': Producer(buffer)},

                'consumer': {'widget': QWidget(),
                             'layout': QVBoxLayout(),
                             'w_dict': {
                                 'name': QLabel('Consumer'),
                                 'picture': QLabel(),
                                 'p_bar': QProgressBar(),
                                 'timer': QTimer()
                             },
                             'handler': Consumer(buffer)}
            },
            'buffer': {
                'widget': QWidget(),
                'layout': QVBoxLayout(),
                'w_dict': {
                         'name': QLabel('Buffer'),
                         'p_bar': QProgressBar(),
                         'timer': QTimer()
                     },
                'handler': buffer
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

    @property
    def green(self):
        return self._components['pixmap_dict']['green']

    @property
    def red(self):
        return self._components['pixmap_dict']['red']

    def _set_p_bar(self):
        self._set_buffer_p_bar()
        self._set_pc_bar(self.producer)
        self._set_pc_bar(self.consumer)

    def _set_pc_bar(self, h_dict):
        pbar = h_dict['w_dict']['p_bar']
        handler = h_dict['handler']
        timer = h_dict['w_dict']['timer']
        timer.timeout.connect(lambda: self._update_p_bar(pbar, h_dict))
        timer.start(50)
        handler.start()
        pbar.setMaximum(self.buffer['handler'].size)

    def _update_p_bar(self, p_bar, handler):
        if handler['handler'].working:
            handler['w_dict']['picture'].setPixmap(self.green)
        else:
            handler['w_dict']['picture'].setPixmap(self.red)

        p_bar.setValue(handler['handler'].progress.value)

    def _set_buffer_p_bar(self):
        pbar = self.buffer['w_dict']['p_bar']
        handler = self.buffer['handler']
        timer = self.buffer['w_dict']['timer']

        pbar.setMaximum(handler.size)

        timer.timeout.connect(lambda: self._update_b_bar(pbar))
        timer.start(50)

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
        self.set_ps(self.producer, layout, self.green)
        self.set_ps(self.consumer, layout, self.red)

    def set_ps(self, ps, p_layout, pxmap):
        widget = ps['widget']
        layout = ps['layout']
        picture = ps['w_dict']['picture']

        widget.setLayout(layout)
        layout.addWidget(ps['w_dict']['name'])

        picture.setPixmap(pxmap)
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

    def _update_b_bar(self, p_bar):
        p_bar.setValue(self.buffer['handler'].length)

