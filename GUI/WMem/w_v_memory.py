"""
Module for virtual memory window class
"""

from .abs_mem import MemoryWindow

class VirtualMemoryWindow(MemoryWindow):
    def __init__(self):
        super().__init__()
