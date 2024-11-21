import sys
import threading

from PyQt6.QtWidgets import QPushButton, QMainWindow, QApplication
from utils.commands import listening
from pyaudio import PyAudio
from forms.settings import Settings
from forms.chat import Chat


class Helperog(QMainWindow):
    """Основной класс программы"""
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 300)
        self.setWindowTitle("Хелперог")

        # Установка базового микрофона автоматически
        self.pyaudio = PyAudio()
        self.micro = self.pyaudio.get_default_input_device_info()["index"]

        # Создание потока для прослушивания
        self.listening_thread = threading.Thread(target=listening, args=(self,))
        self.listening_thread.start()

        self.state = 0
        self.stop = 0

        # Кнопка включения-выключения микрофона
        self.listenButton = QPushButton(self)
        self.listenButton.setGeometry(60, 60, 80, 80)
        self.listenButton.setText("<>")
        self.listenButton.clicked.connect(self.listen_handler)

        # Кнопка открытия настроек
        self.settingsButton = QPushButton(self)
        self.settingsButton.setText("Настройки")
        self.settingsButton.setGeometry(40, 200, 120, 30)
        self.settingsButton.clicked.connect(self.open_settings)
        self.settings = Settings(self)

        # Кнопка открытия чата
        self.chatButton = QPushButton(self)
        self.chatButton.setText("Чат с ботом")
        self.chatButton.setGeometry(40, 240, 120, 30)
        self.chatButton.clicked.connect(self.open_chat)
        self.chat = Chat(self)

    def open_chat(self):
        """Открытие чата"""
        self.chat.show()
        self.hide()

    def open_settings(self):
        """Открытие настроек"""
        self.settings.update_microphones()
        self.settings.show()
        self.hide()

    def set_token(self, token):
        with open("token.txt", "w") as file:
            file.write(token)

    def listen_handler(self):
        if self.state:
            size = (60, 60, 80, 80)
            self.state = 0 # Отключение прослушивания
        else:
            size = (40, 40, 120, 120)
            self.state = 1 # Включение прослушивания
        self.listenButton.setGeometry(*size) # Изменение размеров кнопки для визуализации

    def stop_thread(self, code):
        self.stop = 1

    def stop_handler(self):
        app.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    helpog = Helperog()
    helpog.show()
    helpog.stop_thread(app.exec())
    sys.exit()