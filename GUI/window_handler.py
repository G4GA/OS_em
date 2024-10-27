'''
Window handler module
'''
from PyQt6.QtWidgets import (
    QHBoxLayout
)
from Scheds.multi_prog import MultiprogrammingScheduler

from .menu_window import MenuWindow

from .WSched.w_batch import BatchWindow
from .WSched.w_multip import MultiprogrammingWindow
from .WSched.w_pstate import PStateWindow
from .WSched.w_rr import RRWindow
from .WSched.w_rr import PriorityWindow
from .WSched.w_fcfs import FCFSWindow
from .WSched.w_multiq import MultiQWindow

from .WConc.w_producer_consumer import ProdConsWindow
from .WConc.w_reader_writer import ReaderWriterWindow

from .WMem.w_r_memory import RealMemoryWindow
from .WMem.w_v_memory import VirtualMemoryWindow

class WindowHandler():
    def __init__(self):
        self.__components = {
            'current_window': None
        }

    @property
    def __current_window(self):
        return self.__components['current_window']

    @__current_window.setter
    def __current_window(self, new_window):
        self.__components['current_window'] = new_window

    def start(self):
        self.__current_window = MenuWindow(self.close_menu)
        self.__current_window.show()

    def close_menu(self, option: str):
        self.__current_window.close()

        if option == 'batch':
            self.__current_window = BatchWindow(self.go_back_fn)
        elif option == 'multip':
            self.__current_window = MultiprogrammingWindow(self.go_back_fn)
        elif option == 'p_signal':
            self.__current_window = PStateWindow(self.go_back_fn, MultiprogrammingScheduler)
        elif option == 'rr_sched':
            self.__current_window = RRWindow(self.go_back_fn)
        elif option == 'fcfs_sched':
            self.__current_window = FCFSWindow(self.go_back_fn)
        elif option == 'multiq':
            self.__current_window = MultiQWindow(self.go_back_fn, MultiprogrammingScheduler)
        elif option == 'priority':
            self.__current_window = PriorityWindow(self.go_back_fn)
        elif option == 'producer_c':
            self.__current_window = ProdConsWindow(self.go_back_fn,
                                                   {'upper': QHBoxLayout, 'lower': QHBoxLayout})
        elif option == 'read_write':
            self.__current_window = ReaderWriterWindow(self.go_back_fn)
        elif option == 'r_mem':
            self.__current_window = RealMemoryWindow(self.go_back_fn)
        elif option == 'v_mem':
            self.__current_window = VirtualMemoryWindow(self.go_back_fn)

        self.__current_window.show()

    def go_back_fn(self):
        self.__current_window.close()

        self.__current_window = MenuWindow(self.close_menu)
        self.__current_window.show()

