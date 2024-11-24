from PyQt6.QtWidgets import QMainWindow, QPushButton, QDialog, QLineEdit, QComboBox, QLabel


class InputTokenDialog(QDialog):
    """Класс для отделения диалога от основного окна"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setFixedSize(200, 70)
        self.setWindowTitle("Токен")
        self.line_edit = QLineEdit(self)
        self.line_edit.setGeometry(10, 10, 180, 20)

        self.setTokenButton = QPushButton(self)
        self.setTokenButton.setText("Установить")
        self.setTokenButton.setGeometry(10, 40, 100, 20)
        self.setTokenButton.clicked.connect(self.save_config)

        self.exitButton = QPushButton(self)
        self.exitButton.setText("Выйти")
        self.exitButton.setGeometry(120, 40, 70, 20)
        self.exitButton.clicked.connect(self.close)

    def save_config(self):
        """Установка токена и защита от случайного нажатия"""
        token = self.line_edit.text()
        if token:
            self.parent().parent.set_token(token)


class Settings(QMainWindow):
    """Класс окна настроек"""
    def __init__(self, parent):
        super().__init__()
        self.setFixedSize(150, 180)
        self.setWindowTitle("Настройки")
        # Родительский класс - основное окно
        self.parent = parent

        # Создание экземпляра класса диалога
        self.dialog = InputTokenDialog(self)

        self.label = QLabel(self)
        self.label.setText("Настройки")
        self.label.setGeometry(10, 0, 130, 30)

        # Кнопка сохранения токена
        self.dialogButton = QPushButton(self)
        self.dialogButton.setText("Установить токен")
        self.dialogButton.setGeometry(10, 35, 130, 30)
        self.dialogButton.clicked.connect(self.dialog.open)

        # Получеие и заполнение списка микрофонов
        self.choiceMicro = QComboBox(self)
        self.choiceMicro.setGeometry(10, 85, 130, 30)

        # Кнопка выхода из настроек и сохранения выбранного микрофона
        self.returnButton = QPushButton(self)
        self.returnButton.setText("Сохранить")
        self.returnButton.setGeometry(10, 135, 130, 30)
        self.returnButton.clicked.connect(self.save_config)

    def save_config(self):
        """Сохранение индекса микрофона в родительский класс"""
        self.parent.show()
        self.parent.micro = self.choiceMicro.currentData()
        self.parent.setGeometry(300, 300, 300, 300)
        self.hide()

    def update_microphones(self):
        """Обновление списка микрофонов"""
        self.choiceMicro.clear()
        for i in range(self.parent.pyaudio.get_device_count()):
            self.choiceMicro.addItem(self.parent.pyaudio.get_device_info_by_index(i)["name"], i)
        self.choiceMicro.setCurrentIndex(self.parent.micro)