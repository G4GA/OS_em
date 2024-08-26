"""
Process abstraction module
"""
'''
Process abstraction module
'''

from multiprocessing import Value
from multiprocessing import Process
from enum import Enum
from random import randint

class PState(Enum):
    READY = 0
    RUNNING = 1
    HALTED = 2
    COMPLETED = 3

class ProcSim():
    def __init__(self):
        self.__components = {
            'process': Process(target=self.completion_tracker),
            'state': Value('i', 0),
            'threshold': randint(7000, 20000),
            'progress':Value('i', 0)
        }

    @property
    def process(self):
        return self.__components['process']

    @property
    def progress(self):
        return self.__components['progress'].value

    @progress.setter
    def _progress(self, new_value):
        if self.__components['progress'].value >= self.__components['threshold']:
            self.__components['progress'].value = self.__components['threshold']
            self.__components['state'].value = PState.COMPLETED.value
        else:
            self.__components['progress'] = new_value

    @property
    def threshold(self):
        return self.__components['threshold']

    @property
    def state(self):
        return self.__components['state']

    @state.setter
    def state(self, new_state: PState):
        if new_state == PState.COMPLETED and self.process == self.threshold:
            self.__components['state'] = new_state.value
        elif new_state in (PState.RUNNING, PState.HALTED):
            self.__components['state'] = new_state.value

    def completion_tracker(self):
       pass 
