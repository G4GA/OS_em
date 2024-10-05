"""
Module for process state and signaling showcase
"""
from threading import Thread
from functools import partial
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets  import QProgressBar
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt
from Scheds.procsim import PState
from Scheds.multi_prog import MultiprogrammingScheduler
from Scheds.procsim import ProcSim
from .w_sched import SchedWindow

PROG_AMOUNT = 16

class PStateWindow (SchedWindow):
    def __init__(self, go_back_fn, sched):
        super().__init__(go_back_fn,
                         {'main':QVBoxLayout(), 'upper':QVBoxLayout()},
                         sched(PROG_AMOUNT),
                         override=True)
        self.setFixedSize(1500, 600)
        self._components['sched_thread'] = Thread(target=self.scheduler.start_queue)
        self._components['sched_thread'].start()


        self._upper['layout'].addWidget(self.add_progress_bar(self.scheduler)['widget'])

    def add_progress_bar(self, scheduler) -> None | dict:
        container = {'layout':QHBoxLayout(), 'widget': QWidget()}
        container['widget'].setLayout(container['layout'])
        p_list = []

        for index, proc_sim in enumerate(scheduler.proclist):
            prog_bar_dict = PStateWindow._set_progbar(proc_sim)
            widget = QWidget()
            layout = QVBoxLayout()
            halt_button = QPushButton('H/R')
            kill_button = QPushButton('Kill')
            bttn_tuple = (halt_button, kill_button)

            prog_bar_dict['prog_bar'].setObjectName('p_bar')
            halt_button.clicked.connect(partial(PStateWindow.halt_resume,
                                                      index,
                                                      scheduler.proclist))
            kill_button.clicked.connect(partial(PStateWindow.kill_p,
                                                      index,
                                                      scheduler.proclist,
                                                      bttn_tuple))

            widget.setLayout(layout)

            layout.addWidget(prog_bar_dict['prog_bar'])
            layout.addWidget(halt_button)
            layout.addWidget(kill_button)

            prog_info = {
                'widget': widget,
                'layout': layout,
                'h_button': halt_button,
                'k_button': kill_button,
                'p_bar_d': prog_bar_dict
            }

            p_list.append(prog_info)
            container['layout'].addWidget(widget)
        self._components['prog_bar_list'].append(p_list)
        return container

    @staticmethod
    def halt_resume(proc_index, proc_list):
        proc_s = proc_list[proc_index]
        if proc_s.state == PState.RUNNING.value:
            proc_s.state = PState.HALTED
        elif proc_s.state == PState.HALTED.value:
            proc_s.state = PState.RUNNING

    @staticmethod
    def kill_p(proc_index, proc_list, b_tuple):
        hb, kb = b_tuple
        proc_s = proc_list[proc_index]
        proc_s.state = PState.KILLED
        hb.setEnabled(False)
        kb.setEnabled(False)
