"""
Module for FCFS Scheduling algorithm window
"""

from .w_pstate import PStateWindow
from Scheds.fcfs import FCFSScheduler

class FCFSWindow(PStateWindow):
    def __init__(self, go_back_fn):
        super().__init__(go_back_fn, FCFSScheduler)
