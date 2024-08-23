from .menu_window import MenuWindow
from .WSched.w_batch import BatchWindow

class WindowHandler():
    def __init__(self):
        self.__components = {
            'current_window': None
        }

    @property
    def __current_window(self):
        return self.__components['current_window']

    @__current_window.setter
    def __current_window(self, new_window):
        self.__components['current_window'] = new_window

    def start(self):
        self.__current_window = MenuWindow(self.close_menu)
        self.__current_window.show()

    def close_menu(self, option: str):
        self.__current_window.close()

        if option == 'batch':
            self.__current_window = BatchWindow(self.go_back_fn)

        self.__current_window.show()

    def go_back_fn(self):
        self.__current_window.close()

        self.__current_window = MenuWindow(self.close_menu)
        self.__current_window.show()

