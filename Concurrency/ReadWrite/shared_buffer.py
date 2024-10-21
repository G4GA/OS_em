"""
Module for shared buffer
"""

from multiprocessing import Value

from Concurrency.lock import Lock

class SharedValue:
    def __init__(self):
        self._components = {
            'value': Value('I', 0),
            'lock': Lock()
        }

    @property
    def value(self):
        return self._components['value'].value

    @value.setter
    def value(self, new_value):
        self._components['value'].value = new_value

    @property
    def lock(self):
        return self._components['lock']

class SharedBuffer:
    def __init__(self):
        self._components = {
            'tuple': tuple(SharedValue() for _ in range (15))
        }
        print(self._components['tuple'])

    @property
    def tuple(self):
        return self._components['tuple']
