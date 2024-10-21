"""
Module for producer class
"""

from os import getpid

from random import randint

from time import sleep

from .abs_handler import Handler

class Producer(Handler):
    @staticmethod
    def _p_method(buffer, progress, working):
        while True:
            working.value = False
            a_c = False
            progress.value = 0
            while not a_c:
                a_c = buffer.lock.acquire(getpid())
            while not buffer.is_full:
                working.value = True
                sleep(0.001)
                buffer.put(randint(1, 10), getpid())
                progress.value = buffer.length
            buffer.lock.release(getpid())

