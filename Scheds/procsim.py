"""
Process abstraction module
"""

from multiprocessing import Value
from multiprocessing import Process
from enum import Enum
from random import randint
from time import sleep

class PState(Enum):
    READY = 0
    RUNNING = 1
    HALTED = 2
    KILLED = 3
    COMPLETED = 4

class ProcSim():
    def __init__(self):
        self._components = {
            'process': Process(target=self._completion_tracker),
            'state': Value('i', 0),
            'threshold': randint(7000, 20000),
            'progress':Value('i', 0)
        }

    def run(self):
        self._process.start()

    def wait(self):
        self._process.join()

    @property
    def _process(self):
        return self._components['process']

    @property
    def progress(self):
        return self._components['progress'].value

    @progress.setter
    def _progress(self, new_value):
        if  new_value >= self._components['threshold']:
            self._components['progress'].value = self._components['threshold']
        else:
            self._components['progress'].value = new_value

    @property
    def threshold(self):
        return self._components['threshold']

    @property
    def state(self):
        return self._components['state'].value

    @state.setter
    def state(self, new_state: PState):
        if new_state == PState.COMPLETED and self._process == self.threshold:
            self._components['state'].value = new_state.value
        elif new_state in (PState.RUNNING, PState.HALTED, PState.KILLED):
            self._components['state'].value = new_state.value

    def _update(self):
        my_randint = randint(8, 450)
        self._progress = self.progress + my_randint

    def _completion_tracker(self):
        self.state = PState.RUNNING
        while self.progress < self.threshold and self.state != PState.KILLED:
            sleep(0.1)
            if self.state == PState.RUNNING.value:
                self._update()
        if self.state != PState.KILLED:
            self._components['state'].value = PState.COMPLETED.value
