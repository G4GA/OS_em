"""
Module for lock class
"""

from multiprocessing import Value

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
