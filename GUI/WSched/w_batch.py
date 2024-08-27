'''
Batch scheduler window
'''

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QVBoxLayout,
    QProgressBar,
)

from .w_sched import SchedWindow
from Scheds.batch import BatchScheduler
from Scheds.procsim import (
    ProcSim,
    PState
)

class BatchWindow(SchedWindow):
    def __init__(self, go_back_fn):
        self.__components = {
            'prog_bar_list': [],
            'scheduler': BatchScheduler(15)
        }
        super().__init__(QVBoxLayout())
        self._set_main_widgets('upper')
        self._set_main_widgets('lower')

        self._add_ctrl_bttn('Halt/Resume', self._halt_button_callback)
        self._add_ctrl_bttn('Return to main menu', go_back_fn)

        self.setWindowTitle("Batch Processing")

        self._load_style()

    @property
    def scheduler(self):
        return self.__components['scheduler']

    def add_progress_bar(self):
        for proc_sim in self.scheduler:
            prog_bar_dict = BatchWindow._set_progbar(proc_sim)

    @staticmethod
    def _set_progbar(proc_sim: ProcSim):
        progress_bar = QProgressBar()
        progress_bar.setMaximum(proc_sim.threshold)
        timer = QTimer()
        timer.timeout.connect(BatchWindow.update_bar)
        progress_bar.setMaximum(proc_sim.threshold)
        return {}

    @staticmethod
    def update_bar(prog_bar: QProgressBar, proc_sim:ProcSim):
        prog_bar.setValue(proc_sim.progress)

    def _upper(self):
        return self._components['upper']

    @property
    def _lower(self):
        return self._components['lower']

    def _add_ctrl_bttn(self, label, callback):
        bttn = QPushButton(label)
        bttn.clicked.connect(callback)
        self._lower['layout'].addWidget(bttn)

    def _halt_button_callback(self):
        pass

    def _set_main_widgets(self, side):
        widget = QWiget()
        layout = QVBoxLayout()

        widget.setLayout(layout)
        widget.setObjectName(side)
        self.main_layout.addWidget(widget)

        self._components[side] = {
            'widget': widget,
            'layout': layout,
        }

    def _load_style(self):
        style = ''
        with open('GUI/style/sched.css', 'r', encoding='utf-8') as file:
            style = file.read()
        self.setStyleSheet(style)
