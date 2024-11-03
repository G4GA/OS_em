"""
Module for io simluations
"""

from multiprocessing import (
    Process,
    Value
)

from enum import Enum

from time import sleep

from random import randint
from random import uniform

UPPER_IO_BOUND = 1000
LOWER_IO_BOUND = 500


class SignalType(Enum):
    WAITING = 0
    BUFFER = 1
    DIGITAL = 2
    ANALOG = 3


class Device:
    def __init__(self, name:str):
        bound = randint(LOWER_IO_BOUND, UPPER_IO_BOUND)
        progress = Value('I', 0)
        cur_signal = Value('I', 0)
        self._components = {
            'process': Process(target=Device._target_fn, args=(bound, progress, cur_signal)),
            'bound': bound,
            'progress': progress,
            'name': name,
            'cur_signal': cur_signal
        }

    def start_process(self):
        self._process.start()

    def kill_process(self):
        self._process.terminate()

    @property
    def _process(self):
        return self._components['process']

    @property
    def is_running(self):
        return self._components['process'].is_alive()

    @property
    def name(self):
        return self._components['name']

    @property
    def bound(self):
        return self._components['bound']

    @property
    def progress(self):
        return self._components['progress'].value

    @property
    def cur_signal(self):
        return self._components['cur_signal'].value

    @staticmethod
    def _target_fn(bound, progress, signal):
        while True:
            signal.value = SignalType.WAITING.value
            sleep(uniform(1, 3))
            signal.value = randint(SignalType.WAITING.value, SignalType.ANALOG.value)

            if signal.value == SignalType.BUFFER.value:
                while progress.value < bound:
                    sleep(0.01)
                    increment_value = randint(1, 5)

                    if progress.value + increment_value > bound:
                        progress.value = bound
                    else:
                        progress.value += increment_value

                progress.value = 0
            else:
                sleep(uniform(0.5, 2))

class Devices:
    def __init__(self):
        names_list = [
            'Monitor',
            'Mouse',
            'Keyboard',
            'Sensors',
            'Drive'
        ]

        self._components = {
            'names_list': names_list,
            'device_list': []
        }

        self.get_devices()

    def start_q(self):
        for device in self.devices:
            device.start_process()

    @property
    def devices(self):
        return self._components['device_list']

    @property
    def names(self):
        return self._components['names_list']

    def get_devices(self):
        for name in self.names:
            self.devices.append(Device(name))
