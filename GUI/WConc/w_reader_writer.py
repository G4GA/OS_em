"""
Module for Reader Writer window class
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
)

from PyQt6.QtCore import (
    QTimer,
)

from PyQt6 import sip
from Concurrency.ReadWrite.writer import Writer
from Concurrency.ReadWrite.reader import Reader
from Concurrency.ReadWrite.shared_buffer import SharedBuffer

class Container:
    def __init__(self, qty=0):
        self._components = {
            'widget': QWidget(),
            'layout': QHBoxLayout(),
            'inst_list': [],
            'template': {}
        }
        self._init_widget()

    @property
    def handler(self):
        return self._components['handler']

    @property
    def widget(self):
        return self._components['widget']

    @property
    def _layout(self):
        return self._components['layout']

    @property
    def inst_list(self):
        return self._components['inst_list']

    @property
    def _template(self):
        return self._components['template']

    @property
    def buffer(self):
        return self._components['buffer']

    def _update_container(self, args=None):
        pass

    def _build_template(self):
        return any

    def _build_list(self, qty=0):
        pass

    def _init_widget(self):
        self.widget.setLayout(self._layout)

class WriterContainer(Container):
    def __init__(self, buffer, qty):
        super().__init__(qty)

        template = {
            'widget': QWidget,
            'layout': QVBoxLayout,
            'name': QLabel,
            'p_bar': QProgressBar,
            'wr_bar': QProgressBar,
            'timer': QTimer
        }
        self._components['buffer'] = buffer
        self._components['template'] = template
        self._build_list(qty)
        for obj, _ in self.inst_list:
            obj.start_process()

    def _update_container(self, args=None):
        p_bar, wr_bar, writer, timer = args

        if not sip.isdeleted(p_bar):
            p_bar.setValue(writer.w_counter.value)
            wr_bar.setValue(writer.wr_counter.value)
        else:
            timer.stop()
            writer.process.terminate()

    def _build_template(self):
        cur_temp = {}
        for key, value in self._template.items():
            cur_temp[key] = value()

        writer = Writer(self.buffer)

        p_bar = cur_temp['p_bar']
        p_bar.setMaximum(writer.w_bound)
        wr_bar = cur_temp['wr_bar']
        wr_bar.setMaximum(writer.wr_bound)

        widget = cur_temp['widget']
        layout = cur_temp['layout']
        timer = cur_temp['timer']

        timer.timeout.connect(lambda: self._update_container((p_bar, wr_bar, writer, timer)))
        timer.start(20)

        widget.setLayout(layout)
        layout.addWidget(cur_temp['name'])
        layout.addWidget(cur_temp['p_bar'])
        layout.addWidget(cur_temp['wr_bar'])

        return (cur_temp, writer)

    def _build_list(self, qty=0):
        for index in range(qty):
            w_dict, writer = self._build_template()
            w_dict['name'].setText(f'#{index}')


            self.inst_list.append((writer, w_dict))
            self._layout.addWidget(w_dict['widget'])

class BufferContainer(Container):
    def __init__(self, buffer):
        super().__init__()

        template = {
            'value': QLabel,
            'timer': QTimer
        }
        self._components['stsht'] = \
        """background-color:#8FD14F;
        margin: 0;
        text-align: center;
        color: #343131;
        border-color: #343131;
        border-radius: 5px;"""

        self._components['template'] = template
        self._components['buffer'] = buffer

        self._build_list()

    @property
    def STYLE_SHEET(self):
        return self._components['stsht']

    def _update_container(self, args=None):
        value, label, timer = args
        if not sip.isdeleted(label):
            label.setText(f'[{hex(value.value)}]')
            if value.lock.is_locked:
                label.setStyleSheet('background-color: #F95454;')
            else:
                label.setStyleSheet('background-color: #8FD14F;')
        else:
            timer.stop()

    def _build_template(self):
        cur_temp = {}
        for key, value in self._template.items():
            cur_temp[key] = value()
            if not isinstance(cur_temp[key], QTimer):
                cur_temp[key].setStyleSheet(self.STYLE_SHEET)
                cur_temp[key].setFixedSize(50,50)

        layout = self._layout

        layout.addWidget(cur_temp['value'])

        return cur_temp

    def _build_list(self, qty=0):
        _ = qty
        for shared_value in self.buffer.tuple:
            b_dict = self._build_template()

            b_dict['value'].setText(f'[{hex(shared_value.value)}]')
            timer = b_dict['timer']
            timer.timeout.connect(lambda sh=shared_value, b_dict=b_dict['value']: \
                                            self._update_container((sh, b_dict, timer)))
            timer.start(20)

            self.inst_list.append((shared_value, b_dict))


class ReaderContainer(Container):
    def __init__(self, buffer, qty):
        super().__init__(qty)
        template = {
            'widget': QWidget,
            'layout': QVBoxLayout,
            'name': QLabel,
            'p_bar': QProgressBar,
            'r_value': QLabel,
            'timer': QTimer
        }

        self._components['template'] = template
        self._components['buffer'] = buffer

        self._build_list(qty)
        for obj, _ in self.inst_list:
            obj.start_process()

    def _update_container(self, args=None):
        p_bar, r_value, reader, timer, widget = args
        if not sip.isdeleted(p_bar):
            p_bar.setValue(reader.progress)
            r_value.setText(f'{hex(reader.cur_value)}')
            if reader.is_reading:
                widget.setStyleSheet('background-color: #387478;')
            else:
                widget.setStyleSheet('background-color: #626F47;')
        else:
            timer.stop()
            reader.process.terminate()

    def _build_template(self):
        cur_temp = {}
        for key, value in self._template.items():
            cur_temp[key] = value()

        widget = cur_temp['widget']
        layout = cur_temp['layout']
        p_bar = cur_temp['p_bar']
        r_value = cur_temp['r_value']
        timer = cur_temp['timer']

        reader = Reader(self.buffer)

        timer.timeout.connect(lambda: self._update_container((p_bar,
                                                              r_value,
                                                              reader,
                                                              timer,
                                                              widget)))
        timer.start(20)

        p_bar.setMaximum(reader.bound)

        widget.setLayout(layout)
        layout.addWidget(cur_temp['name'])
        layout.addWidget(p_bar)
        layout.addWidget(r_value)

        return (cur_temp, reader)

    def _build_list(self, qty=0):
        for index in range(qty):
            r_dict, reader = self._build_template()
            r_dict['name'].setText(f'Reader #{index}')
            self.inst_list.append((reader, r_dict))
            self._layout.addWidget(r_dict['widget'])

class ReaderWriterWindow(QMainWindow):
    def __init__(self, go_back_fn):
        super().__init__()
        buffer = SharedBuffer()
        self.setFixedWidth(1900)
        self._components = {
            'main': {
                'widget': QWidget(),
                'layout': QVBoxLayout()
            },
            'upper': {
                'widget': QWidget(),
                'layout': QVBoxLayout()
            },
            'lower': {
                'widget': QWidget(),
            'layout': QVBoxLayout()
            },
            'back_bttn': QPushButton('Return to main menu'),
            'writers': {
                'main': {
                    'widget': QWidget(),
                    'layout': QVBoxLayout(),
                    'name': QLabel('Writers:')
                },
                'container': WriterContainer(buffer, 22)
            },
            'buffer': {
                'main': {
                    'widget': QWidget(),
                    'layout': QVBoxLayout(),
                    'name': QLabel('Buffer:')
                },
                'container': BufferContainer(buffer)
            },
            'readers': {
                'main': {
                    'widget': QWidget(),
                    'layout': QVBoxLayout(),
                    'name': QLabel('Readers:')
                },
                'container': ReaderContainer(buffer, 15)
            },
        }

        self._init_window(go_back_fn)
        self._set_containers()
        self._load_style()

    @property
    def _main(self):
        return self._components['main']

    @property
    def _upper(self):
        return self._components['upper']

    @property
    def _lower(self):
        return self._components['lower']

    @property
    def _writers(self):
        return self._components['writers']

    @property
    def _buffer(self):
        return self._components['buffer']

    @property
    def _readers(self):
        return self._components['readers']

    @property
    def writer_container(self):
        return self._components['writers']['container']

    @writer_container.setter
    def _writer_container(self, new_value):
        self._components['writers']['container'] = new_value

    @property
    def buffer_container(self):
        return self._components['buffer']['container']

    @buffer_container.setter
    def _buffer_container(self, new_value):
        if self._is_valid_container(new_value):
            self._components['buffer']['container'] = new_value

    @property
    def reader_container(self):
        return self._components['readers']['container']

    @reader_container.setter
    def _reader_contaier(self, new_value):
        if self._is_valid_container(new_value):
            self._components['readers']['container'] = new_value

    @staticmethod
    def _init_widgets(comp_dict, add_widget):
        widget = comp_dict['widget']
        layout = comp_dict['layout']

        widget.setLayout(layout)

        add_widget(widget)

    @staticmethod
    def _is_valid_container(container):
        is_valid = False
        if container in (WriterContainer, BufferContainer, ReaderContainer):
            is_valid = True

        return is_valid

    def _set_back_bttn(self, go_back_fn):
        bttn = self._components['back_bttn']
        bttn.clicked.connect(go_back_fn)

        self._lower['layout'].addWidget(bttn)

    def _set_containers(self):
        self._writers['main']['layout'].addWidget(self.writer_container.widget)
        self._buffer['main']['layout'].addWidget(self.buffer_container.widget)
        self._readers['main']['layout'].addWidget(self.reader_container.widget)

    def _init_all_widgets(self):
        main_layout_fn = self._main['layout'].addWidget
        upper_layout_fn = self._upper['layout'].addWidget

        self._init_widgets(self._main, self.setCentralWidget)
        self._init_widgets(self._upper, main_layout_fn)
        self._init_widgets(self._lower, main_layout_fn)
        self._init_widgets(self._writers['main'], upper_layout_fn)
        self._init_widgets(self._buffer['main'], upper_layout_fn)
        self._init_widgets(self._readers['main'], upper_layout_fn)

    def _init_labels(self):
        self._writers['main']['layout'].addWidget(self._writers['main']['name'])
        self._buffer['main']['layout'].addWidget(self._buffer['main']['name'])
        self._readers['main']['layout'].addWidget(self._readers['main']['name'])

    def _init_window(self, go_back_fn):

        self._init_all_widgets()
        self._init_labels()

        self._set_back_bttn(go_back_fn)

    def _load_style(self):
        self._upper['widget'].setObjectName('sidev')
        self._lower['widget'].setObjectName('sidev')
        style = ''
        with open('GUI/style/sched.css', 'r', encoding='utf-8') as file:
            style = file.read()
        self.setStyleSheet(style)

