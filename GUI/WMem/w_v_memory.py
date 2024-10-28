"""
Module for virtual memory window class
"""

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QLabel,
    QVBoxLayout
)

from Memory.memory import MemBuffer

from .abs_mem import MemoryWindow
from .w_r_memory import RealMemContainer

class VirtualMemContainer(RealMemContainer):
    def __init__(self, buffer):
        super().__init__(buffer, QHBoxLayout)
        new_components = {
            'real_mem': {
                'name': QLabel('Real Memory'),
                'widget': QWidget(),
                'layout': QVBoxLayout(),
                'grid': {
                    'widget': QWidget(),
                    'layout': QGridLayout()
                }
            },
            'vir_mem': {
                'name': QLabel('Virutal Memory'),
                'widget': QWidget(),
                'layout': QVBoxLayout(),
                'grid': {
                    'widget': QWidget(),
                    'layout': QGridLayout()
                }
            }
        }

        self._components = {**self._components,
                            **new_components}
        self._init_mem_grid()
        self._build_list()

    @property
    def _real_mem(self):
        return self._components['real_mem']

    @property
    def _vir_mem(self):
        return self._components['vir_mem']

    def _init_grid(self, g_dict=None):
        widget = g_dict['widget']
        layout = g_dict['layout']
        name = g_dict['name']
        name.setFixedHeight(20)
        widget.setLayout(layout)

        g_widget = g_dict['grid']['widget']
        g_layout = g_dict['grid']['layout']
        g_widget.setLayout(g_layout)

        layout.addWidget(name)
        layout.addWidget(g_widget)

    def _init_mem_grid(self):
        real_mem = self._real_mem
        vir_mem = self._vir_mem
        self._init_grid(real_mem)
        self._init_grid(vir_mem)
        self._layout.addWidget(real_mem['widget'])
        self._layout.addWidget(vir_mem['widget'])

    def _build_list(self):
        counter = 0
        side = 5
        for x in range(side):
            for y in range(side):
                mem_block = self._buffer.m_list[counter]
                addr, _ = mem_block
                print(hex(addr))
                w_dict = self._build_template(mem_block)
                counter += 1

                self._real_mem['grid']['layout'].addWidget(w_dict['widget'], x, y)
                self.w_list.append((w_dict, mem_block))

        for x in range(side):
            for y in range(side):
                mem_block = self._buffer.m_list[counter]
                addr, _ = mem_block

                w_dict = self._build_template(mem_block)
                counter += 1

                self._vir_mem['grid']['layout'].addWidget(w_dict['widget'], x, y)
                self.w_list.append((w_dict, mem_block))

class VirtualMemoryWindow(MemoryWindow):
    def __init__(self, go_back_fn):
        buffer = MemBuffer(50)
        super().__init__(go_back_fn, 9, buffer)
        self.setFixedHeight(900)

        self._components['MemContainer'] = VirtualMemContainer(self._buffer)

        self._set_containers()

    @property
    def _mem_container(self):
        return self._components['MemContainer']

    def _set_containers(self):
        super()._set_containers()
        self._upper['layout'].addWidget(self._mem_container.widget)
