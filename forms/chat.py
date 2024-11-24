from PyQt6.QtWidgets import QMainWindow, QPlainTextEdit, QLineEdit, QPushButton
from utils.elsetextcommand import elsetext
from database.database import Database


db = Database()


class Chat(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setFixedSize(250, 390)
        self.setWindowTitle("Чат")
        self.parent = parent

        self.chat = QPlainTextEdit(self)
        self.chat.setGeometry(10, 10, 230, 300)
        self.chat.setReadOnly(True)

        self.messageEdit = QLineEdit(self)
        self.messageEdit.setGeometry(10, 320, 195, 25)

        self.sendButton = QPushButton(self)
        self.sendButton.setGeometry(215, 320, 25, 25)
        self.sendButton.setText("↪")
        self.sendButton.clicked.connect(self.send_message)

        self.returnButton = QPushButton(self)
        self.returnButton.setGeometry(10, 355, 230, 25)
        self.returnButton.setText("Вернуться")
        self.returnButton.clicked.connect(self.open_main)

    def add_row(self, author, text):
        self.chat.setPlainText(f"{self.chat.toPlainText()}{author}: {text}\n")

    def send_message(self):
        text = self.messageEdit.text()
        self.messageEdit.clear()
        self.add_row("Вы", text)
        request, answer, is_num = elsetext(text)
        if is_num is not None:
            db.add_request(request, answer, is_num)
        self.add_row("Нейросеть", answer)

    def open_main(self):
        self.parent.show()
        self.hide()