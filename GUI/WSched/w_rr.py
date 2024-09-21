"""
Moduler for Round Robin window scheduler
"""
from .w_pstate import PStateWindow
from Scheds.rr import RoundRobinScheduler

class RRWindow(PStateWindow):
    def __init__(self, go_back_fn):
        super().__init__(go_back_fn, RoundRobinScheduler)

