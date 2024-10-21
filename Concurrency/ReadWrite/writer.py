"""
Module for writer class
"""

from multiprocessing import Process
from multiprocessing import Value

from random import randint
from random import choice

from time import sleep

from os import getpid

from Concurrency.ProdCons.buffer import UPPER_BOUND
from Concurrency.ProdCons.buffer import LOWER_BOUND

class Writer:
    def __init__(self, buffer):
        w = Value('I', 0)
        wr = Value('I', 0)
        w_b = randint(1000, 10000)
        wr_b = randint(1000, 10000)
        self._components = {
            'buffer': buffer,
            'process': Process(target=Writer.start, args=(w,
                                                          wr,
                                                          buffer,
                                                          (w_b, wr_b))),
            'w_counter': w,
            'w_bound': w_b,
            'wr_counter': wr,
            'wr_bound': wr_b,
        }

    def start_process(self):
        self.process.start()

    @property
    def w_bound(self):
        return self._components['w_bound']

    @property
    def wr_bound(self):
        return self._components['wr_bound']

    @property
    def buffer(self):
        return self._components['buffer']

    @property
    def process(self):
        return self._components['process']

    @property
    def w_counter(self):
        return self._components['w_counter']

    @property
    def wr_counter(self):
        return self._components['wr_counter']

    @staticmethod
    def start(w, wr, buffer, bounds):
        w_b, wr_b = bounds
        while True:
            while w.value < w_b:
                sleep(0.001)
                w.value += 3
            w.value = 0
            Writer._write(buffer, wr, wr_b)


    @staticmethod
    def _write(buffer, wr, wr_b):
        value = Writer.choose_val(buffer)
        while wr.value < wr_b:
            sleep(0.001)
            wr.value += 3
        wr.value = 0
        value.value = randint(0, LOWER_BOUND)
        value.lock.release(getpid())

    @staticmethod
    def choose_val(buffer):
        return_val = choice(buffer.tuple)
        is_locked = return_val.lock.is_locked
        while is_locked:
            return_val = choice(buffer.tuple)
            is_locked = return_val.lock.is_locked
        return_val.lock.acquire(getpid())
        return return_val
