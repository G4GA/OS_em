"""
Module for buffer and lock classes
"""

from multiprocessing import Value
from multiprocessing import Queue

from random import randint

UPPER_BOUND = 12_000
LOWER_BOUND = 4_000

class Lock():
    def __init__(self):
        self._components = {
            'islocked': Value('b', 0),
            'owner': Value('I', 0)
        }

    @property
    def is_locked(self):
        return self._components['islocked'].value

    @is_locked.setter
    def _lock_value(self, new_value):
        if isinstance(new_value, bool):
            self._components['islocked'].value = new_value

    @property
    def owner(self):
        return self._components['owner'].value

    @owner.setter
    def _owner(self, new_owner):
        self._components['owner'].value = new_owner

    def acquire(self, pid):
        acquired = False
        if not self.is_locked:
            if isinstance(pid, int) and not self._owner:
                self._owner = pid
                self._lock_value = True
                print('Lock ac')
                acquired = True

        return acquired


    def release(self, pid):
        if isinstance(pid, int):
            if self.is_locked:
                if pid == self._owner:
                    self._lock_value = False
                    self._owner = 0
                    print('lock rs')

class Buffer():
    def __init__(self, _type=int):
        self._components = {
            'queue': Queue(),
            'lock': Lock(),
            'size': randint(LOWER_BOUND, UPPER_BOUND),
            'is_full': Value('b', False),
            'is_empty': Value('b', True),
            'length': Value('I', 0),
            'type': _type
        }

    @property
    def _q(self):
        return self._components['queue']

    @property
    def lock(self):
        return self._components['lock']

    @property
    def length(self):
        return self._components['length'].value

    @length.setter
    def _length(self, new_value: int):
        if isinstance(new_value, int):
            self._components['length'].value = new_value

    @property
    def size(self):
        return self._components['size']

    @property
    def is_full(self):
        return self._components['is_full'].value

    @is_full.setter
    def _is_full(self, new_value: bool):
        if isinstance(new_value, bool):
            self._components['is_full'].value = new_value

    @property
    def is_empty(self):
        return self._components['is_empty'].value

    @is_empty.setter
    def _is_empty(self, new_value: bool):
        if isinstance(new_value, bool):
            self._components['is_empty'].value = new_value

    def check_bound(self):
        if self.length == 0:
            self._is_empty = True
        elif self.length == self.size:
            self._is_full = True
        else:
            self._is_full =  False
            self._is_empty = False


    def _increment(self):
        if not self.is_full:
            self._length += 1

    def _decrement(self):
        if not self.is_empty:
            self._length -= 1

    def put(self, value, pid):
        self.check_bound()
        if self.lock.is_locked:
            if pid == self.lock.owner:
                if not self.is_full:
                    self._increment()
                    self._q.put(value)

    def get(self, pid) -> None | int:
        self.check_bound()
        if self.lock.is_locked:
            if pid == self.lock.owner:
                if not self._is_empty:
                    self._decrement()
                    return self._q.get()

