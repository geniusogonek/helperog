from PyQt6.QtWidgets import QMainWindow, QPushButton, QDialog, QLineEdit, QComboBox, QLabel


class InputTokenDialog(QDialog):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setFixedSize(200, 70)
        self.line_edit = QLineEdit(self)
        self.line_edit.setGeometry(10, 10, 180, 20)

        self.btn = QPushButton(self)
        self.btn.setText("Установить")
        self.btn.setGeometry(50, 40, 100, 20)
        self.btn.clicked.connect(self.set_token)

    def set_token(self):
        self.parent().parent.set_token(self.line_edit.text())
        self.close()


class Settings(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setFixedSize(150, 180)

        self.parent = parent

        self.dialog = InputTokenDialog(self)

        self.label = QLabel(self)
        self.label.setText("Настройки")
        self.label.setGeometry(10, 0, 130, 30)

        self.dialogButton = QPushButton(self)
        self.dialogButton.setText("Установить токен")
        self.dialogButton.setGeometry(10, 35, 130, 30)
        self.dialogButton.clicked.connect(self.open_dialog)

        self.choiceMicro = QComboBox(self)
        for i in range(self.parent.pyaudio.get_device_count()):
            self.choiceMicro.addItem(self.parent.pyaudio.get_device_info_by_index(i)["name"], i)
        self.choiceMicro.setGeometry(10, 85, 130, 30)

        self.returnButton = QPushButton(self)
        self.returnButton.setText("Сохранить")
        self.returnButton.setGeometry(10, 135, 130, 30)
        self.returnButton.clicked.connect(self.open_main)

    def open_dialog(self):
        self.dialog.open()

    def open_main(self):
        self.parent.show()
        self.parent.setGeometry(300, 300, 300, 300)
        self.hide()