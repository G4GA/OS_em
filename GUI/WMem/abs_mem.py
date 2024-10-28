"""
Module for parent abstract memory window class
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
)

from PyQt6.QtCore import (
    QTimer
)

from PyQt6 import sip

from Memory.memory import MemProcess
from Memory.memory import MemBuffer

class Container:
    def __init__(self, layout):
        self._components = {
            'main': {
                'widget': QWidget(),
                'layout': layout(),
            },
            'template': {}
        }
        self._init_main()

    @property
    def widget(self):
        return self._components['main']['widget']

    @property
    def _layout(self):
        return self._components['main']['layout']

    @property
    def _template(self):
        return self._components['template']

    @_template.setter
    def _template(self, template):
        if isinstance(template, dict):
            self._components['template'] = template

    def _init_main(self):
        self.widget.setLayout(self._layout)

class PContainer(Container):
    def __init__(self, buffer, amount):
        super().__init__(QVBoxLayout)
        new_components = {
            'w_list': [],
            'buffer': buffer,
            'amount': amount,
            'name': QLabel('Process List')
        }
        template = {
            'widget': QWidget,
            'layout': QVBoxLayout,
            'process_n': QLabel,
            'p_bar': QProgressBar,
            'status': QLabel
        }

        self._components = {**self._components, **new_components}
        self._template = template

        self._layout.addWidget(self._components['name'])

        self._build_list()

    @property
    def buffer(self):
        return self._components['buffer']

    @property
    def amount(self):
        return self._components['amount']

    @property
    def w_list(self):
        return self._components['w_list']

    def _build_template(self):
        w_dict = {}
        for key, value in self._template.items():
            w_dict[key] = value()

        #Set widgets for template
        #Define variables
        p = MemProcess(self.buffer)
        p.start_alloc()
        widget = w_dict['widget']
        layout = w_dict['layout']
        process_n = w_dict['process_n']
        p_bar = w_dict['p_bar']
        status = w_dict['status']
        timer = QTimer()

        args = (p,
                p_bar,
                status,
                timer)

        timer.timeout.connect(lambda:PContainer.timer_fn(args))
        timer.start(20)

        w_dict['timer'] = timer

        #set widget and layout
        widget.setLayout(layout)

        process_n.setText(f'Process: {hex(p.proc.pid).upper()}')
        layout.addWidget(process_n)

        p_bar.setMaximum(p.bound)
        layout.addWidget(p_bar)

        status_str = self.get_status(p)
        status.setText(status_str)
        layout.addWidget(status)

        return (w_dict, p)

    def _build_list(self):
        for index in range(self.amount):
            _ = index
            w_dict, proc = self._build_template()
            self._layout.addWidget(w_dict['widget'])
            self.w_list.append(tuple((w_dict, proc)))

    @staticmethod
    def get_status(p):
        return 'Running' if p.success else 'Aborted'

    @staticmethod
    def timer_fn(args):
        p, p_bar, status, timer = args
        if not sip.isdeleted(p_bar):
            p_bar.setValue(p.progress)
            status.setText(PContainer.get_status(p))
        else:
            p.proc.terminate()
            timer.stop()

class MemoryWindow(QMainWindow):
    def __init__(self, go_back_fn, p_amount, buffer):
        super().__init__()
        self.setWindowTitle('Angel Damian Raul Garcia Guevara')
        self._components = {
            'main': {
                'widget': QWidget(),
                'layout': QVBoxLayout()
            },
            'upper': {
                'widget': QWidget(),
                'layout': QHBoxLayout()
            },
            'lower': {
                'widget': QWidget(),
                'layout': QVBoxLayout()
            },
            'buffer': buffer,
            'PContainer': PContainer(buffer, p_amount),
            'gb_bttn': QPushButton('Return to main menu')
        }

        self._init_main_widgets()
        self._init_go_back_bttn(go_back_fn)

    @property
    def _main(self):
        return self._components['main']

    @property
    def _upper(self):
        return self._components['upper']

    @property
    def _lower(self):
        return self._components['lower']

    @property
    def _gb_bttn(self):
        return self._components['gb_bttn']

    @property
    def _PContainer(self):
        return self._components['PContainer']

    @property
    def _buffer(self):
        return self._components['buffer']

    def _init_go_back_bttn(self, go_back_fn):
        self._gb_bttn.clicked.connect(go_back_fn)
        self._lower['layout'].addWidget(self._gb_bttn)

    @staticmethod
    def add_comp(comp_dict, method):
        widget = comp_dict['widget']
        layout = comp_dict['layout']

        widget.setLayout(layout)
        method(widget)

    def _set_containers(self):
        self._upper['layout'].addWidget(self._PContainer.widget)

    def _init_main_widgets(self):
        m_layout_fn = self._main['layout'].addWidget
        self.add_comp(self._main, self.setCentralWidget)
        self.add_comp(self._upper, m_layout_fn)
        self.add_comp(self._lower, m_layout_fn)

        self._load_style()

    def _load_style(self):
        self._upper['widget'].setObjectName('sidev')
        self._lower['widget'].setObjectName('sidev')
        style = ''
        with open('GUI/style/sched.css', 'r', encoding='utf-8') as file:
            style = file.read()
        self.setStyleSheet(style)
