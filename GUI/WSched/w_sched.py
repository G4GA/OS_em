"""
Parent class for scheduler GUI
"""

from threading import Thread

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QProgressBar,
)

from PyQt6.QtCore import (
    QTimer,
    Qt
)

from Scheds.procsim import (
    ProcSim,
    PState
)

class SchedWindow(QMainWindow):
    def __init__(self, go_back_fn, layout, scheduler, override=False):
        super().__init__()
        self._components = {
            'main_widget': QWidget(),
            'main_layout': layout,
            'prog_bar_list': [],
            'upper': {},
            'lower': {},
            'scheduler': scheduler,
            'sched_thread': '',
        }
        self._init_window()
        self._load_style()

        self._set_main_widgets('upper')
        self._set_main_widgets('lower')

        self._add_ctrl_bttn('Return to main menu', go_back_fn)

        self.setWindowTitle("Batch Processing")
        if not override:
            self.add_progress_bar()


    def add_progress_bar(self):
        for proc_sim in self.scheduler.proclist:
            prog_bar_dict = SchedWindow._set_progbar(proc_sim)
            self._upper['layout'].addWidget(prog_bar_dict['prog_bar'])
            self._components['prog_bar_list'].append(prog_bar_dict)

    @staticmethod
    def _set_progbar(proc_sim: ProcSim):
        progress_bar = QProgressBar()
        progress_bar.setMaximum(proc_sim.threshold)
        progress_bar.setOrientation(Qt.Orientation.Vertical)
        timer = QTimer()
        timer.timeout.connect(lambda:SchedWindow.update_bar(progress_bar, proc_sim))
        timer.start(10)

        return {'prog_bar': progress_bar, 'proc_sim': proc_sim, 'timer': timer}

    @staticmethod
    def update_bar(prog_bar: QProgressBar, proc_sim:ProcSim):
        if proc_sim.state == PState.RUNNING.value:
            prog_bar.setStyleSheet('#p_bar::chunk { background-color: green; }')
        elif proc_sim.state == PState.HALTED.value:
            prog_bar.setStyleSheet('#p_bar::chunk { background-color: yellow; }')
        elif proc_sim.state == PState.COMPLETED.value:
            prog_bar.setStyleSheet('#p_bar::chunk { background-color: #6C48C5; }')
        prog_bar.setValue(proc_sim.progress)

    @property
    def sched_thread(self) -> Thread:
        return self._components['sched_thread']

    @property
    def scheduler(self):
        return self._components['scheduler']

    @property
    def main_widget(self):
        return self._components['main_widget']

    @property
    def _upper(self):
        return self._components['upper']

    @property
    def _lower(self):
        return self._components['lower']

    @property
    def main_layout(self):
        return self._components['main_layout']

    def _add_ctrl_bttn(self, label, callback):
        bttn = QPushButton(label)
        bttn.clicked.connect(callback)
        self._lower['layout'].addWidget(bttn)

    def _init_window(self):
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def _load_style(self):
        style = ''
        with open('GUI/style/sched.css', 'r', encoding='utf-8') as file:
            style = file.read()
        self.setStyleSheet(style)

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
