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
        self.add_button('Batch Processing', lambda: callback_fn('batch'))
        self.add_button('Multiprogramming showcase', lambda: callback_fn('multip'))
        self.add_button('Process States and Signaling', lambda: callback_fn('p_signal'))
        self.add_button('Round Robin Scheduler', lambda: callback_fn('rr_sched'))
        self.add_button('Firs Come First Served Scheduler', 
                        lambda: callback_fn('fcfs_sched'))
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
        for bttn in self.__bttn_list:
            self.main_layout.addWidget(bttn)

    def add_button(self, bttn_label: str, callback_fn):
        new_button = QPushButton(bttn_label)
        new_button.clicked.connect(callback_fn)

        self.__bttn_list.append(new_button)

