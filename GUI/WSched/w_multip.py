'''
Multiprogramming showcase window
'''

from PyQt6.QtWidgets import (
    QVBoxLayout,
)

from .w_sched import SchedWindow

class MultiprogrammingWindow(SchedWindow):
    def __init__(self, go_back_fn):
        super().__init__(QVBoxLayout())

