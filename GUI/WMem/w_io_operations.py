"""
Module for io operations class
"""

from PyQt6.QtCore import (
    QTimer,
    Qt
)

from PyQt6 import sip

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QProgressBar
)

from IOBuffering.io_sim import Devices
from IOBuffering.io_sim import SignalType

from .abs_mem import AbsWindow
from .abs_mem import Container

SIGNAL_STR = {
    SignalType.WAITING.value: ('wait();'         , '#EEC759'),
    SignalType.BUFFER.value:  ('bufferSignal();' , '#7469B6'),
    SignalType.DIGITAL.value: ('digitalSignal();', '#4A628A'),
    SignalType.ANALOG.value:  ('analogSignal();' , '#EC8305')

}

class DeviceContainer(Container):
    def __init__(self, devices):
        super().__init__(QHBoxLayout)
        new_components = {
            'w_list': [],
            'devices': devices
        }
        template = {
            'widget': QWidget,
            'layout': QVBoxLayout,
            'name': QLabel,
            'signal': QLabel,
            'buffer_label': QLabel,
            'p_bar': QProgressBar,
        }
        self._template = template
        self._components = {**self._components, **new_components}

        self._build_list()

    @property
    def _w_list(self):
        return self._components['w_list']

    @property
    def _devices(self):
        return self._components['devices']

    def _build_template(self, device):
        w_dict = {}
        for key, value in self._template.items():
            w_dict[key] = value()

        widget  = w_dict['widget']
        layout  = w_dict['layout']
        name    = w_dict['name']
        signal  = w_dict['signal']
        b_label = w_dict['buffer_label']
        p_bar   = w_dict['p_bar']
        timer    = QTimer()
        w_dict['timer'] = timer

        args = (signal, p_bar,
                timer, device, widget)

        timer.timeout.connect(lambda: DeviceContainer._update(args))

        timer.start(20)

        name_style = \
        """
        color: black;
        background-color: #B7B7B7;
        border-radius: 5px;
        """

        widget.setLayout(layout)

        name.setText(device.name)
        name.setStyleSheet(name_style)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        signal.setText(self._get_sig_str(device.cur_signal)[0])
        signal.setStyleSheet('color: black;')

        b_label.setText('Buffer:')
        b_label.setStyleSheet('color: black;')

        p_bar.setMaximum(device.bound)
        p_bar.setStyleSheet('color: black;')

        layout.addWidget(name)
        layout.addWidget(signal)
        layout.addWidget(b_label)
        layout.addWidget(p_bar)

        return w_dict

    @staticmethod
    def _update(args):
        signal, p_bar, \
        timer, device, widget = args
        if not sip.isdeleted(widget):
            cur_sig = DeviceContainer._get_sig_str(device.cur_signal)
            signal.setText(cur_sig[0])
            widget.setStyleSheet(f'background-color: {cur_sig[1]};')
            p_bar.setValue(device.progress)
        else:
            timer.stop()
            if device.is_running:
                device.kill_process()

    def _build_list(self):
        for device in self._devices.devices:
            w_dict = self._build_template(device)
            self._layout.addWidget(w_dict['widget'])
            self._w_list.append((w_dict, device))

    @staticmethod
    def _get_sig_str(signal_t):
        return SIGNAL_STR[signal_t]

class OperationsIOWindow(AbsWindow):
    def __init__(self, go_back_fn):
        super().__init__(go_back_fn)
        devices = Devices()
        new_components = {
            'devices': devices,
            'container': DeviceContainer(devices)
        }

        self._components = {**self._components, **new_components}

        self._set_container()
        devices.start_q()

    @property
    def _container(self):
        return self._components['container']

    def _set_container(self):
        self._upper['layout'].addWidget(self._container.widget)


