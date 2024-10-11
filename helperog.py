import sys
import threading

from PyQt6 import QtCore
from PyQt6.QtWidgets import QPushButton, QMainWindow, QApplication
from commands import listening




class Helperog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.listening_thread = threading.Thread(target=listening, args=(self,))
        self.listening_thread.start()
        self.state = 0
        self.stop = 0
        self.setWindowTitle("Хелперог")
        self.setFixedSize(120, 120)

        self.listenButton = QPushButton(self)
        self.listenButton.setGeometry(QtCore.QRect(40, 40, 40, 40))
        self.listenButton.setText("<>")
        self.listenButton.clicked.connect(self.listen_handler)

    def listen_handler(self):
        if self.state:
            size = (40, 40, 40, 40)
            self.state = 0
        else:
            size = (20, 20, 80, 80)
            self.state = 1
        self.listenButton.setGeometry(*size)

    def stop_thread(self, code):
        self.stop = 1

    def stop_handler(self):
        app.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    helpog = Helperog()
    helpog.show()
    helpog.stop_thread(app.exec())