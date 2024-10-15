from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton

class MenuWindow(QMainWindow):
    def __init__(self, callback_fn):
        super().__init__()
            # Setting internal attributes
        self.__components = {
            'main_layout': QGridLayout(),
            'main_widget': QWidget(),
            'bttn_list': []
        }

        #Add test button
        self.add_button('Batch Processing',
                        lambda: callback_fn('batch'),
                        'sched')
        self.add_button('Multiprogramming showcase',
                        lambda: callback_fn('multip'),
                        'sched')
        self.add_button('Process States and Signaling',
                        lambda: callback_fn('p_signal'),
                        'sched')
        self.add_button('Round Robin Scheduler',
                        lambda: callback_fn('rr_sched'),
                        'sched')
        self.add_button('Firs Come First Served Scheduler',
                        lambda: callback_fn('fcfs_sched'),
                        'sched')
        self.add_button('Multi Queue Scheduler',
                        lambda: callback_fn('multiq'),
                        'sched')
        self.add_button('Priority Scheduler',
                        lambda: callback_fn('priority'),
                        'sched')
        self.add_button('Producer-Consumer',
                        lambda: callback_fn('producer_c'),
                        'concurrency')
        self.add_button('Readers Writers',
                        lambda: callback_fn('read_write'),
                        'concurrency')
        #window setting
        self.set_window()

    #define getters and setters
    @property
    def __bttn_list(self):
        return self.__components['bttn_list']

    @__bttn_list.setter
    def __bttn_list(self, new_list: list):
        self.__components['bttn_list'] = new_list

    @property
    def __main_layout(self):
        return self.__components['main_layout']

    @__main_layout.setter
    def __main_layout(self, main_layout: QWidget):
        self.__components['main_layout'] = main_layout

    @property
    def __main_widget(self):
        return self.__components['main_widget']

    @__main_widget.setter
    def __main_widget(self, main_widget: QWidget):
        self.__components['main_widget'] = main_widget

    def set_window(self):
        self.setWindowTitle("OS Visualization Tool")
        self.main_layout = QGridLayout()
        self.main_widget = QWidget()

        self.main_widget.setLayout(self.main_layout)

        self.__show_bttns()

        self.setCentralWidget(self.main_widget)

    def __show_bttns(self):
            sched_counter = 0
            concurrency_counter = 0
            for bttn, label in self.__bttn_list:
                if label == 'sched':
                    self.main_layout.addWidget(bttn, sched_counter, 0)
                    sched_counter = sched_counter + 1
                elif label == 'concurrency':
                    self.main_layout.addWidget(bttn, concurrency_counter, 1)
                    concurrency_counter = concurrency_counter + 1

    def add_button(self, bttn_label: str, callback_fn, label):
        new_button = QPushButton(bttn_label)
        new_button.clicked.connect(callback_fn)

        self.__bttn_list.append((new_button, label))

