from .w_sched import WinScheduler

class BatchWindow(WinScheduler):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Batch Processing")
