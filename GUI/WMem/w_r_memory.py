"""
Module for real memory window class
"""

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QLabel
)

from PyQt6.QtCore import (
    QTimer
)

from PyQt6 import sip

from time import sleep

from random import choice

import math

from Memory.memory import MemBuffer

from .abs_mem import MemoryWindow
from .abs_mem import Container

from enum import Enum

class Colors(Enum):
    DARK_PEACH = "#DC0083"
    SLATE_BLUE = "#DC5F00"
    TEAL_GREEN = "#7469B6"
    FOG_GREY = "#0A6847"
    CHARCOAL = "#3A4750"
    DUSTY_TEAL = "#5D737E"
    WINE_RED = "#7C3A2D"
    MAUVE_PURPLE = "#806D7A"
    DUSTY_ROSE = "#A26769"
    BURNT_TERRACOTTA = "#E07A5F"

class ColorAssigner:
    def __init__(self):
        self.color_map = {}  # Stores {pid: color}
        self.available_colors = list(Colors)  # All colors

    def get_color(self, pid):
        # Check if the PID already has an assigned color
        if pid not in self.color_map:
            if self.available_colors:
                color = self.available_colors.pop(0)  # Assign next available color
                self.color_map[pid] = color
            else:
                # If out of unique colors, reassign randomly (or any other desired behavior)
                color = choice(list(Colors))
                self.color_map[pid] = color
        return self.color_map[pid].value

class RealMemContainer(Container):
    def __init__(self, buffer, layout=QVBoxLayout):
        super().__init__(layout)
        new_components = {
            'name': QLabel('Memory'),
            'buffer': buffer,
            'grid': {
                'widget': QWidget(),
                'layout': QGridLayout()
            },
            'w_list': []
        }

        template = {
            'widget': QWidget,
            'layout': QVBoxLayout,
            'addr': QLabel,
            'owner': QLabel
        }

        self._template = template
        self.color = ColorAssigner()

        self._components = {**self._components,
                            **new_components}

        if layout == QVBoxLayout:
            self._init_grid()
            self._build_list()
            self._add_local()

    @property
    def _grid(self):
        return self._components['grid']

    @property
    def _name(self):
        return self._components['name']

    @property
    def _buffer(self):
        return self._components['buffer']

    @property
    def w_list(self):
        return self._components['w_list']

    def _init_grid(self, g_dict=None):
        _ = g_dict
        self._grid['widget'].setLayout(self._grid['layout'])

    def _add_local(self):
        self._name.setFixedHeight(20)
        self._layout.addWidget(self._name)
        self._layout.addWidget(self._grid['widget'])

    def _build_template(self, mem_block):
        addr_val, _ = mem_block
        w_dict = {}
        for key, value in self._template.items():
            w_dict[key] = value()
        widget = w_dict['widget']
        layout = w_dict['layout']
        addr = w_dict['addr']
        owner = w_dict['owner']
        timer = QTimer()
        w_dict['timer'] = timer

        timer.timeout.connect(lambda: RealMemContainer._timer_fn((owner,
                                                                       mem_block,
                                                                       widget,
                                                                       timer,
                                                                       self.color)))

        sleep(.001)
        timer.start(10)

        widget.setLayout(layout)

        addr.setText(f'{hex(addr_val).upper()}')
        layout.addWidget(addr)

        layout.addWidget(owner)

        return w_dict

    @staticmethod
    def _timer_fn(args):
        owner, mem_block, widget, timer, color = args
        _, pid = mem_block
        if not sip.isdeleted(owner):
            owner.setText(f'PID: {hex(pid.value).upper()}')
            if pid.value:
                cur_color = color.get_color(pid.value)
                widget.setStyleSheet(f'background-color:{cur_color};')
            else:
                widget.setStyleSheet('')
        else:
            timer.stop()

    def _build_list(self):
        counter = 0
        side = int(math.sqrt(self._buffer.mem_size))
        for x in range(side):
            for y in range(side):
                mem_block = self._buffer.m_list[counter]
                addr, _ = mem_block

                print(hex(addr))
                w_dict = self._build_template(mem_block)
                counter += 1

                self._grid['layout'].addWidget(w_dict['widget'], x, y)
                self.w_list.append((w_dict, mem_block))

class RealMemoryWindow(MemoryWindow):
    def __init__(self, go_back_fn):
        buffer = MemBuffer()
        super().__init__(go_back_fn, 7, buffer)
        self._components['MemContainer'] = RealMemContainer(self._buffer)

        self._set_containers()

    @property
    def _mem_container(self):
        return self._components['MemContainer']

    def _set_containers(self):
        super()._set_containers()
        self._upper['layout'].addWidget(self._mem_container.widget)
