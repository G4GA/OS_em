"""
Module for multi_q sheduler window
"""

from Scheds.fcfs import FCFSScheduler
from Scheds.rr import RoundRobinScheduler
from threading import Thread
from .w_pstate import PStateWindow
from .w_pstate import PROG_AMOUNT

class MultiQWindow (PStateWindow):
    def __init__(self, go_back_fn, sched):
        rr = RoundRobinScheduler(PROG_AMOUNT)
        fcfs = FCFSScheduler(PROG_AMOUNT)
        fcfs_t = Thread(target=fcfs.start_queue)
        rr_t = Thread(target=rr.start_queue)

        super().__init__(go_back_fn, sched)

        self._upper['layout'].addWidget(self.add_progress_bar(fcfs)['widget'])
        self._upper['layout'].addWidget(self.add_progress_bar(rr)['widget'])

        fcfs_t.start()
        rr_t.start()

