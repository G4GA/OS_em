"""
Module for reader class
"""

from multiprocessing import Process
from multiprocessing import Value

from random import randint
from random import choice

from Concurrency.ProdCons.buffer import LOWER_BOUND

class Reader:
    def __init__(self, buffer):

        cur_value = Value('I', 0)
        is_reading = Value('b', False)
        progress = Value('I', 0)
        bound = randint(0, LOWER_BOUND)
        self._components = {
            'buffer': buffer,
            'process': Process(target=Reader._target_method, args=((cur_value,
                                                                    is_reading,
                                                                    progress,
                                                                    bound,
                                                                    buffer),)),
            'cur_value': cur_value,
            'is_reading': is_reading,
            'progress': progress,
            'bound': bound,
        }

    def start_process(self):
        self.process.start()

    @property
    def process(self):
        return self._components['process']

    @property
    def buffer(self):
        return self._components['buffer']

    @property
    def _proc(self):
        return self._components['process']

    @property
    def cur_value(self):
        return self._components['cur_value'].value

    @property
    def is_reading(self):
        return self._components['is_reading'].value

    @property
    def progress(self):
        return self._components['progress'].value

    @property
    def bound(self):
        return self._components['bound']

    @progress.setter
    def _progress(self, new_value):
        self._components['progress'].value = new_value

    @staticmethod
    def _target_method(ttuple):
        cur_value, is_reading, progress, bound, buffer = ttuple
        while True:
            is_locked = False
            while not is_locked:
                cur_value.value = choice(buffer.tuple)
            is_reading.value = True
