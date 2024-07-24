from PyQt6.QtWidgets import QMainWindow

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #window setting
        self.setWindow()

    def setWindow(self):
        self.setWindowTitle("OS Visualization Tool")
