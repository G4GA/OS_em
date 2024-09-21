"""
Module for Round Robin Scheduler Algorithm
"""
from multiprocessing import Value
from time import sleep

from .procsim import ProcSim
from .procsim import PState

from .abs_sched import TemplateScheduler

class RRProcSim(ProcSim):
    def __init__(self):
        super().__init__()
        self._components['burst'] = Value('b', 0)

    @property
    def burst(self):
        return self._components['burst'].value

    @burst.setter
    def burst(self, new_value):
        self._components['burst'].value = new_value

    #Overriden method
    def _completion_tracker(self):
        self.state = PState.RUNNING
        while self.progress < self.threshold and self.state != PState.KILLED.value:
            if self.burst:
                sleep(0.01)
                if self.state == PState.RUNNING.value:
                    self._update()
        if self.state != PState.KILLED.value:
            self._components['state'].value = PState.COMPLETED.value

class RoundRobinScheduler(TemplateScheduler):
    def _fill_queue(self, amount):
        for _ in range(amount):
            self._components['proclist'].append(RRProcSim())

    def start_queue(self):
        for process in self._components['proclist']:
            process.run()
        while not self.__is_done():
            for process in self._components['proclist']:
                if process.state == PState.RUNNING.value:
                    process.burst = 1
                    sleep(0.02)
                    process.burst = 0

    def __is_done(self):
        completed = True
        for process in self._components['proclist']:
            if process.state not in (PState.COMPLETED.value, PState.KILLED.value):
                completed = False
        return completed

