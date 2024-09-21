"""
Module for FCFS Scheduling Algorithm
"""
from random import randint
from time import sleep

from .procsim import ProcSim
from .procsim import PState

from .abs_sched import TemplateScheduler

class FCFSProcSim(ProcSim):
    def __init__(self, p_list, index):
        super().__init__()
        self._components['p_list'] = p_list
        self._components['p_index'] = index

    @property
    def p_list(self):
        return self._components['p_list']

    @property
    def index(self):
        return self._components['p_index']

    @staticmethod
    def _update_p(progress):
        return progress + randint(8, 450)

    def _completion_tracker(self):
        self.state = PState.RUNNING
        while self.progress < self.threshold and self.state != PState.KILLED.value:
            sleep(0.1)
            if self.state == PState.RUNNING.value:
                new_p = FCFSProcSim._update_p(self.progress)
                if new_p < self.threshold:
                    self._progress = new_p
                else:
                    if self.missing_process():
                        pass
                    else:
                        self._progress = new_p
        print('sdf')
        if self.state != PState.KILLED:
            self._components['state'].value = PState.COMPLETED.value

    def missing_process(self):
        missing = False
        for i in range(self.index):
            if self.p_list[i].state in (PState.RUNNING.value, PState.HALTED.value):
                missing = True

        return missing

class FCFSScheduler(TemplateScheduler):
    def _fill_queue(self, amount):
        for index in range(amount):
            self._components['proclist'].append(FCFSProcSim(self._components['proclist'],
                                                       index))
    def start_queue(self):
        for process in self.proclist:
            process.run()




