'''
Batch scheduler window
'''
from threading import Thread
from PyQt6.QtWidgets import QVBoxLayout
from Scheds.procsim import PState
from Scheds.batch import BatchScheduler
from .w_sched import SchedWindow

class BatchWindow(SchedWindow):
    def __init__(self, go_back_fn):
        super().__init__(go_back_fn,QVBoxLayout(), BatchScheduler(15))

        self._components['sched_thread'] = Thread(target=self.scheduler.start_queue)

        self._add_ctrl_bttn('Halt/Resume', self._halt_button_callback)
        self._components['sched_thread'].start()

    def _halt_button_callback(self):
        print(f'current state: {self.scheduler.cur_proc.state} running state: {PState.RUNNING.value}')
        if self.scheduler.cur_proc.state == PState.RUNNING.value:
            self.scheduler.cur_proc.state = PState.HALTED
        elif self.scheduler.cur_proc.state == PState.HALTED.value:
            self.scheduler.cur_proc.state = PState.RUNNING

