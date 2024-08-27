"""
Batch processing algorithm implementation
"""

from .procsim import ProcSim

class BatchScheduler():

    def __init__(self, proc_amount):
        self.__components = {
            'proclist': []
        }
        self.__fill_queue(proc_amount)

    def __fill_queue(self, amount):
        for _ in range(amount):
            self.__components['proclist'].append(ProcSim())

    @property
    def proclist(self):
        return self.__components['proclist']

    def start_queue(self):
        for process in self.__components['process']:
            process.run()
            process.wait()

