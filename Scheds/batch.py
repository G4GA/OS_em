"""
Batch processing algorithm implementation
"""

from .procsim import ProcSim

class BatchScheduler():

    def __init__(self, proc_amount):
        self.__components = {
            'proclist': [],
            'cur_proc': None
        }
        self.__fill_queue(proc_amount)

    def __fill_queue(self, amount):
        for _ in range(amount):
            self.__components['proclist'].append(ProcSim())

    @property
    def proclist(self):
        return self.__components['proclist']

    @property
    def cur_proc(self):
        return self.__components['cur_proc']

    @cur_proc.setter
    def _cur_proc(self, new_proc):
        self.__components['cur_proc'] = new_proc

    def start_queue(self):
        for process in self.__components['proclist']:
            self._cur_proc = process
            process.run()
            process.wait()
            print(f'Process: {process} state: {process.state}')
            print(f'Progress: {process.progress} threshold: {process.threshold}')


