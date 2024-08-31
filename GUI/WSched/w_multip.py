'''
Multiprogramming showcase window
'''
from threading import Thread

from PyQt6.QtWidgets import (
    QVBoxLayout,
)

from Scheds.multi_prog import MultiprogrammingScheduler
from .w_sched import SchedWindow

class MultiprogrammingWindow(SchedWindow):
    def __init__(self, go_back_fn):
        super().__init__(go_back_fn, QVBoxLayout(), MultiprogrammingScheduler(15))
        self.setWindowTitle('Multiprogramming Window')
        self._components['sched_thread'] = Thread(target=self.scheduler.start_queue)
        self._components['sched_thread'].start()

