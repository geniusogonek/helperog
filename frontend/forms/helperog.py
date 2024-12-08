import threading

from PyQt6.QtWidgets import QPushButton, QMainWindow
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from utils.commands import listening
from pyaudio import PyAudio
from forms.settings import Settings
from forms.chat import Chat


class Helperog(QMainWindow):
    """Основной класс программы"""
    def __init__(self, app):
        super().__init__()
        self.setFixedSize(200, 300)
        self.setWindowTitle("Хелперог")
        self.app = app

        # Установка базового микрофона автоматически
        self.pyaudio = PyAudio()
        try:
            self.micro = self.pyaudio.get_default_input_device_info()["index"]
        except OSError:
            self.micro = 0

        # Создание потока для прослушивания
        self.listening_thread = threading.Thread(target=listening, args=(self,))
        self.listening_thread.start()

        self.state = 0
        self.stop = 0

        # Кнопка включения-выключения микрофона
        self.listenButton = QPushButton(self, icon=QIcon("src/micro_off.png"))
        self.listenButton.setIconSize(QSize(80, 80))
        self.listenButton.setGeometry(40, 40, 120, 120)
        self.listenButton.setStyleSheet("font-size: 25px")
        self.listenButton.clicked.connect(self.listen_handler)

        # Кнопка открытия настроек
        self.settingsButton = QPushButton(self)
        self.settingsButton.setText("Настройки")
        self.settingsButton.setGeometry(40, 200, 120, 30)
        self.settingsButton.clicked.connect(self.open_settings)

        # Кнопка открытия чата
        self.chatButton = QPushButton(self)
        self.chatButton.setText("Чат с ботом")
        self.chatButton.setGeometry(40, 240, 120, 30)
        self.chatButton.clicked.connect(self.open_chat)

    def open_chat(self):
        """Открытие чата"""
        self.chat = Chat(self)
        self.chat.show()
        self.hide()

    def open_settings(self):
        """Открытие настроек"""
        self.settings = Settings(self)
        self.settings.update_microphones()
        self.settings.show()
        self.hide()

    def set_token(self, token):
        with open("token.txt", "w") as file:
            file.write(token)

    def listen_handler(self):
        if self.state:
            self.state = 0 # Отключение прослушивания
            self.listenButton.setIcon(QIcon("src/micro_off.png"))
        else:
            self.listenButton.setIcon(QIcon("src/micro_on.png"))
            self.state = 1 # Включение прослушивания

    def stop_thread(self, code):
        self.stop = 1

    def stop_handler(self):
        self.app.exit()