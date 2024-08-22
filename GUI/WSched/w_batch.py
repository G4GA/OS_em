from .w_sched import SchedWindow
from PyQt6.QtWidgets import (
    QLabel
)

class BatchWindow(SchedWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Batch Processing")

        self.test_label = QLabel('Testing')
        self.main_layout.addWidget(self.test_label)

        self.main_widget.setStyleSheet('background-color: blue')
