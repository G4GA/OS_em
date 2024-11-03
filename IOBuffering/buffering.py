"""
Module for buffering classes and utilities
"""

from random import randint

from threading import Thread
from multiprocessing import Value

from time import sleep

UPPER_STORAGE_BOUND = 5000
LOWER_STORAGE_BOUND = 4000

class StorageUnit:
    def __init__(self, amount):
        values = []
        args = (values, amount)
        self._components = {
            'values': values,
            'amount': amount,
        }

    @property
    def amount(self):
        return self._components['amount']

    @property
    def values(self):
        return self._components['values']

    def fill_values(self):
        for _ in range(self.amount):
            self.values.append(randint(LOWER_STORAGE_BOUND, UPPER_STORAGE_BOUND))

class StorageManager:
    def __init__(self, amount):
        usb = StorageUnit(amount)
        buffer = StorageUnit(amount)
        drive = StorageUnit(amount)
        bound = amount * 2
        self._progress = Value('I', 0)

        args = (usb, buffer, drive,
                amount, self._progress)

        self._components = {
            'usb': usb,
            'buffer': buffer,
            'drive': drive,
            'bound': bound,
            'amount': amount,
            'thread': Thread(target=StorageManager._target_fn, args=(args))
        }
        usb.fill_values()


    def fill(self):
        self.thread.start()

    @property
    def thread(self):
        return self._components['thread']

    @property
    def amount(self):
        return self._components['amount']

    @property
    def usb(self):
        return self._components['usb']

    @property
    def buffer(self):
        return self._components['buffer']

    @property
    def drive(self):
        return self._components['drive']

    @property
    def progress(self):
        return self._progress.value

    @progress.setter
    def progress(self, new_value):
        self._progress.value = new_value

    @property
    def bound(self):
        return self._components['bound']

    @staticmethod
    def _fill_storage_unit(counter, amount, buffer, storage):
        sleep(1.5)
        random_int = randint(1, int(amount - (amount / 2)))

        if len(buffer.values) + random_int > amount:
            random_int = amount - len(buffer.values)

        cur_len = len(buffer.values)
        for index in range(random_int):
                buffer.values.append(storage.values[index + cur_len])

        counter += random_int

        return counter

    @staticmethod
    def _target_fn(usb, buffer, drive, amount, counter):

        while len(buffer.values) < amount:
            counter.value = StorageManager._fill_storage_unit(counter.value, amount,
                                                   buffer, usb)

        while len(drive.values) < amount:
            counter.value = StorageManager._fill_storage_unit(counter.value, amount,
                                                   drive, buffer)


if __name__ == "__main__":
    manager = StorageManager(9)
    manager.fill()

    while manager.progress < manager.bound:
        sleep(1)
        print(manager.usb.values, manager.buffer.values, manager.drive.values)

