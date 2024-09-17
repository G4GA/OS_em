"""
Module for process state and signaling showcase
"""
from threading import Thread
from functools import partial
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets  import QProgressBar
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt
from Scheds.procsim import PState
from Scheds.multi_prog import MultiprogrammingScheduler
from Scheds.procsim import ProcSim
from .w_sched import SchedWindow

class PStateWindow (SchedWindow):
    def __init__(self, go_back_fn):
        super().__init__(go_back_fn,
                         QVBoxLayout(),
                         MultiprogrammingScheduler(16),
                         override=True)
        self.setFixedSize(1500, 600)
        self.setWindowTitle('Process\' states and signaling')
        self._components['sched_thread'] = Thread(target=self.scheduler.start_queue)
        self._components['sched_thread'].start()
        self.add_progress_bar()

    def add_progress_bar(self) -> None:
        for index, proc_sim in enumerate(self.scheduler.proclist):
            prog_bar_dict = PStateWindow._set_progbar(proc_sim)
            widget = QWidget()
            layout = QVBoxLayout()
            halt_button = QPushButton('H/R')

            prog_bar_dict['prog_bar'].setObjectName('p_bar')
            halt_button.clicked.connect(partial(PStateWindow.halt_resume,index, self.scheduler.proclist))

            widget.setLayout(layout)

            layout.addWidget(prog_bar_dict['prog_bar'])
            layout.addWidget(halt_button)

            prog_info = {
                'widget': widget,
                'layout': layout,
                'h_button': halt_button,
                'p_bar_d': prog_bar_dict
            }

            self._components['prog_bar_list'].append(prog_info)
            self._upper['layout'].addWidget(widget)

    @staticmethod
    def halt_resume(proc_index, proc_list):
        proc_s = proc_list[proc_index]
        print(f'{proc_index} {proc_list}')
        if proc_s.state == PState.RUNNING.value:
            proc_s.state = PState.HALTED
        elif proc_s.state == PState.HALTED.value:
            proc_s.state = PState.RUNNING
