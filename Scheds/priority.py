"""
Module for priority Round Robin Scheduler
"""
from time import sleep
from random import randint

from .procsim import PState

from .rr import RRProcSim
from .rr import RoundRobinScheduler

class PriorityProcess(RRProcSim):
    def __init__(self, priority: int):
        super().__init__()
        self._components['priority'] = priority

    @property
    def priority(self) -> int:
        return self._components['priority']

    def _completion_tracker(self):
        self.state = PState.RUNNING
        while self.progress < self.threshold and self.state != PState.KILLED.value:
            if self.burst:
                sleep(0.05 / (self.priority * 5)) #Este es el quantum
                if self.state == PState.RUNNING.value:
                    self._update()
        if self.state != PState.KILLED.value:
            self._components['state'].value = PState.COMPLETED.value

class PriorityScheduler(RoundRobinScheduler):
    def _fill_queue(self, amount):
        for _ in range(amount):
            self._components['proclist'].append(PriorityProcess(randint(1, 5)))

