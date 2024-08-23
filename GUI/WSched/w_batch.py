from PyQt6.QtWidgets import (
    #QLabel,
    QPushButton,
    QWidget,
    QVBoxLayout,
)
from .w_sched import SchedWindow

class BatchWindow(SchedWindow):
    def __init__(self, go_back_fn):
        super().__init__(QVBoxLayout())
        self._set_main_widgets('upper')
        self._set_main_widgets('lower')

        self._add_ctrl_bttn('Halt/Resume', self._halt_button_callback)
        self._add_ctrl_bttn('Return to main menu', go_back_fn)

        self.setWindowTitle("Batch Processing")

        self._load_style()

    @property
    def _upper(self):
        return self._components['upper']

    @property
    def _lower(self):
        return self._components['lower']

    def _add_ctrl_bttn(self, label, callback):
        bttn = QPushButton(label)
        bttn.clicked.connect(callback)
        self._lower['layout'].addWidget(bttn)

    def _halt_button_callback(self):
        pass

    def _set_main_widgets(self, side):
        widget = QWidget()
        layout = QVBoxLayout()

        widget.setLayout(layout)
        widget.setObjectName(side)
        self.main_layout.addWidget(widget)

        self._components[side] = {
            'widget': widget,
            'layout': layout,
        }

    def _load_style(self):
        style = ''
        with open('GUI/style/sched.css', 'r', encoding='utf-8') as file:
            style = file.read()
        self.setStyleSheet(style)
