"""
Module for consumer class
"""
from os import getpid

from time import sleep

from .abs_handler import Handler
class Consumer(Handler):
    @staticmethod
    def _p_method(buffer, progress, working):
        while True:
            working.value = False
            a_c = False
            progress.value = 0
            while not a_c:
                a_c = buffer.lock.acquire(getpid())
            while not buffer.is_empty:
                working.value = True
                sleep(0.001)
                buffer.get(getpid())
                progress.value = buffer.size - buffer.length
            buffer.lock.release(getpid())
