"""
Moduler for Round Robin window scheduler
"""
from PyQt6.QtWidgets import QLabel
from Scheds.rr import RoundRobinScheduler
from Scheds.priority import PriorityScheduler

from .w_pstate import PStateWindow

class RRWindow(PStateWindow):
    def __init__(self, go_back_fn):
        super().__init__(go_back_fn, RoundRobinScheduler)

class PriorityWindow(PStateWindow):
    def __init__(self, go_back_fn):
        super().__init__(go_back_fn, PriorityScheduler, p_amount=24)
        self.setFixedWidth(1900)
        for info in self._components['prog_bar_list'][0]:
            label = QLabel()
            label.setText(f'Priority:\n{info["p_bar_d"]["proc_sim"].priority}')
            info['layout'].addWidget(label)
