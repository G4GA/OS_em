'''
Batch scheduler window
'''

from PyQt6.QtCore import (
    QTimer,
    Qt
)
from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar,
)

from Scheds.procsim import (
    ProcSim,
    #PState
)

from threading import Thread

from Scheds.batch import BatchScheduler
from .w_sched import SchedWindow

class BatchWindow(SchedWindow):
    def __init__(self, go_back_fn):
        super().__init__(QVBoxLayout())
        self._components['prog_bar_list'] = []
        self._components['scheduler'] = BatchScheduler(15)
        self._components['upper'] = {}
        self._components['lower'] = {}
        self._components['sched_thread'] = Thread(target=self.scheduler.start_queue)

        self._set_main_widgets('upper')
        self._set_main_widgets('lower')

        self._add_ctrl_bttn('Halt/Resume', self._halt_button_callback)
        self._add_ctrl_bttn('Return to main menu', go_back_fn)

        self.setWindowTitle("Batch Processing")
        self.add_progress_bar()

        self.sched_thread.start()
        self._load_style()

    @property
    def sched_thread(self) -> Thread:
        return self._components['sched_thread']

    @property
    def scheduler(self) -> BatchScheduler:
        return self._components['scheduler']

    def add_progress_bar(self):
        for proc_sim in self.scheduler.proclist:
            prog_bar_dict = BatchWindow._set_progbar(proc_sim)
            self._upper['layout'].addWidget(prog_bar_dict['prog_bar'])
            self._components['prog_bar_list'].append(prog_bar_dict)

    @staticmethod
    def _set_progbar(proc_sim: ProcSim):
        progress_bar = QProgressBar()
        progress_bar.setMaximum(proc_sim.threshold)
        progress_bar.setOrientation(Qt.Orientation.Vertical)
        timer = QTimer()
        timer.timeout.connect(lambda:BatchWindow.update_bar(progress_bar, proc_sim))
        timer.start(10)

        return {'prog_bar': progress_bar, 'proc_sim': proc_sim, 'timer': timer}

    @staticmethod
    def update_bar(prog_bar: QProgressBar, proc_sim:ProcSim):
        prog_bar.setValue(proc_sim.progress)

    @property
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
        widget = QWidget()
        layout = QHBoxLayout()

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
