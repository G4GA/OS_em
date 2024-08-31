"""
Template class for scheduler implementation
"""

from .procsim import ProcSim

class TemplateScheduler():
    def __init__(self, proc_amount):
        self._components = {
            'proclist': [],
            'cur_proc': None
        }
        self.__fill_queue(proc_amount)

    def __fill_queue(self, amount):
        for _ in range(amount):
            self._components['proclist'].append(ProcSim())

    @property
    def proclist(self):
        return self._components['proclist']

    @property
    def cur_proc(self):
        return self._components['cur_proc']

    @cur_proc.setter
    def _cur_proc(self, new_proc):
        self._components['cur_proc'] = new_proc

    def start_queue(self):
        pass
