"""
Module for memory logic class
"""

from multiprocessing import Value
from multiprocessing import Process

from random import randint

from os import getpid

from time import sleep


STARTING_POS = 0x1000



class MemBuffer:
    def __init__(self, mem_size=25):
        self._components = {
            'm_list': [],
            'mem_size': mem_size,
            'alloc_amount': Value('I', 0),
            'block_size': int(0x1000),
        }
        self._init_mem()

#Set getters and setters
    @property
    def m_list(self):
        return self._components['m_list']

    @property
    def mem_size(self):
        return self._components['mem_size']

    @property
    def alloc_amount(self):
        return self._components['alloc_amount'].value

    @alloc_amount.setter
    def alloc_amount(self, new_value):
        self._components['alloc_amount'].value = new_value

    @property
    def block_size(self):
        return self._components['block_size']

    def _init_mem(self):
        for i in range(self.mem_size):
            address = STARTING_POS + (i * self.block_size)
            mem_block = tuple((address,
                              Value('I', 0)))

            self.m_list.append(mem_block)

    def allocate(self, amount, pid):
        rc = False, 0
        new_amount = self.alloc_amount + amount
        if new_amount < self.mem_size:
            for index in range(self.alloc_amount, new_amount):
                self.m_list[index][1].value = pid
            self.alloc_amount = new_amount
            rc = True, self.alloc_amount
        return rc

    def deallocate(self, pid):
        for addr in self.m_list:
            _, apid = addr
            if apid.value == pid:
                apid.value = 0

class MemProcess:
    def __init__(self, buffer: MemBuffer):
        size = randint(1, int(buffer.mem_size/5 + 3))
        addr = Value('I', 0)
        progress = Value('I', 0)
        bound = randint(2000, 10000)
        success = Value('b', True)
        self._components = {
            'proc': Process(target=MemProcess._target_fn, kwargs={'args':(addr, size,
                                                                          buffer, progress,
                                                                          bound, success)}),
            'buffer': buffer,
            'addr': addr,
            'size': size,
            'progress': progress,
            'bound': bound,
            'success': success
        }

    @property
    def proc(self):
        return self._components['proc']

    @property
    def _buffer(self):
        return self._components['buffer']

    @property
    def size(self):
        return self._components['size']

    @property
    def addr(self):
        return self._components['addr']

    @property
    def bound(self):
        return self._components['bound']

    @property
    def success(self):
        return self._components['success'].value

    @property
    def progress(self):
        return self._components['progress'].value

    def start_alloc(self):
        self.proc.start()

    @staticmethod
    def _target_fn(args:tuple):
        addr, size, buffer,\
        progress, bound, success = args

        while progress.value < bound / 3:
            progress.value += randint(1, 20)
            sleep(0.01)

        success.value, addr.value = buffer.allocate(size, getpid())
        sleep(0.01)

        if success.value:
            while progress.value < bound:
                progress.value += randint(1, 20)
                sleep(0.01)
            buffer.deallocate(getpid())

