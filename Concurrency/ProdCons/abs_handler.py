"""
Module for handler abstract class
"""


from multiprocessing import Process
from multiprocessing import Value

from .buffer import Buffer


class Handler:
    def __init__(self, buffer:Buffer):
        self._components = {
            'buffer': buffer,
            'progress': Value('I', 0),
            'working': Value('b', False)
        }
        self._components['process'] = Process(target=self._p_method,
                                              args=(buffer,
                                                    self._components['progress'],
                                                    self._components['working']))
    @property
    def progress(self):
        return self._components['progress']

    @property
    def _buffer(self):
        return self._components['buffer']

    @property
    def working(self):
        return self._components['working'].value

    @working.setter
    def _working(self, new_value: bool):
        if isinstance(new_value, bool):
            self._components['working'] = new_value


    @property
    def proc(self):
        return self._components['process']

    @staticmethod
    def _p_method(buffer, progress, working):
        pass

    def start(self):
        self.proc.start()
