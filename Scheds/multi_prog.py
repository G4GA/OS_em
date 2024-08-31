"""
Multiprogramming showcase scheduler
"""

from .abs_sched import TemplateScheduler

class MultiprogrammingScheduler(TemplateScheduler):
    def start_queue(self):
        for process in self.proclist:
            process.run()
