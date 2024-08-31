"""
Batch processing algorithm implementation
"""

from .procsim import ProcSim
from .abs_sched import TemplateScheduler

class BatchScheduler(TemplateScheduler):
    def start_queue(self):
        for process in self._components['proclist']:
            self._cur_proc = process
            process.run()
            process.wait()

