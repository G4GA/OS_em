"""
Module for the buffering window class
"""

import math

from PyQt6.QtCore import (
    QTimer,
    Qt,
)

from PyQt6 import sip

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QProgressBar
)

from IOBuffering.buffering import StorageManager

from .abs_mem import AbsWindow
from .abs_mem import Container

class StorageContainer(Container):
    def __init__(self, manager):
        super().__init__(QHBoxLayout)

        new_components = {
            'manager': manager,
            'w_list': [],
            'p_bar_label': QLabel('Progress:'),
            'total_p_bar': QProgressBar(),
            'total_timer': QTimer()
        }

        template = {
            'widget': QWidget,
            'layout': QVBoxLayout,
            'name': QLabel,
            'table': QTableWidget
        }

        self._template = template
        self._components = {**self._components, **new_components}

        self._build_list()
        self._build_tp_bar()

    @property
    def manager(self):
        return self._components['manager']

    @property
    def w_list(self):
        return self._components['w_list']

    @property
    def total_p_bar(self):
        return self._components['total_p_bar']

    @property
    def total_timer(self):
        return self._components['total_timer']

    @property
    def p_bar_label(self):
        return self._components['p_bar_label']

    def _build_tp_bar(self):
        self.total_p_bar.setMaximum(self.manager.bound)
        self.total_p_bar.setFixedWidth(500)

        args = (self.total_timer, self.manager,
                self.total_p_bar)

        self.total_timer.timeout.connect(lambda: StorageContainer._update_bar(args))

        self.w_list[1]['layout'].addWidget(self.p_bar_label)
        self.w_list[1]['layout'].addWidget(self.total_p_bar)

        self.total_timer.start(20)

    @staticmethod
    def _update_bar(args):
        timer, manager, p_bar = args
        if not sip.isdeleted(p_bar):
            p_bar.setValue(manager.progress)
        else:
            timer.stop()

    def _build_template(self, table_data, name):
        w_dict = {}
        for key, value in self._template.items():
            w_dict[key] = value()

        widget  = w_dict['widget']
        layout  = w_dict['layout']
        wname  = w_dict['name']
        table  = w_dict['table']
        timer = QTimer()


        side = int(math.sqrt(self.manager.amount))


        table.setRowCount(side)
        table.setColumnCount(side)

        wname.setText(name)

        table_width = 500
        table_height = 300
        table.setFixedSize(table_width, table_height)

        cell_width = table_width // table.columnCount()
        cell_height = table_height // table.rowCount()

        for col in range(table.columnCount()):
            table.setColumnWidth(col, cell_width - 8)
        for row in range(table.rowCount()):
            table.setRowHeight(row, cell_height - 8)

        w_dict['timer'] = timer

        args = (table, table_data,
                timer, side)

        timer.timeout.connect(lambda: StorageContainer._update(args))
        timer.start(10)
        widget.setLayout(layout)
        layout.addWidget(wname)
        layout.addWidget(table)

        return w_dict

    @staticmethod
    def _update(args):
        table, table_data, timer, side = args
        counter = 0
        if not sip.isdeleted(table):
            for x in range(side):
                for y in range(side):
                    item = ''
                    try:
                        item = QTableWidgetItem(hex(table_data.values[counter]).upper())
                        item.setBackground(0x658147)
                    except IndexError:
                        item = QTableWidgetItem(hex(0))
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    table.setItem(x, y, item)
                    counter += 1
        else:
            timer.stop()

    def _build_list(self):
        usb = self._build_template(self.manager.usb, 'usb')
        buffer = self._build_template(self.manager.buffer, 'buffer')
        drive = self._build_template(self.manager.drive, 'drive')

        self.w_list.append(usb)
        self.w_list.append(buffer)
        self.w_list.append(drive)

        self._layout.addWidget(usb['widget'])
        self._layout.addWidget(buffer['widget'])
        self._layout.addWidget(drive['widget'])

class BufferingWindow(AbsWindow):
    def __init__(self, go_back_fn):
        super().__init__(go_back_fn)
        amount = 9
        manager = StorageManager(amount)
        self.setFixedWidth(1700)

        new_components = {
            'container': StorageContainer(manager),
            'p_bar': QProgressBar()
        }

        self._components = {**self._components, **new_components}

        self._set_container()
        manager.fill()

    @property
    def container(self):
        return self._components['container']

    def _set_container(self):
        self._upper['layout'].addWidget(self.container.widget)
