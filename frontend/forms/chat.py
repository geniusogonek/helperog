import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QLineEdit,
    QPushButton,
)

from utils.elsetextcommand import elsetext
from database.database import Database

db = Database()


class Message(QWidget):
    def __init__(self, message, sender="Вы"):
        super().__init__()

        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.label.setStyleSheet("""
            background-color: rgba(0, 128, 255, 100);
            color: white;
            padding: 8px;
            border-radius:
            12px;
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.setMaximumHeight(200)

        if sender == "Вы":
            self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.label.setStyleSheet(
                self.label.styleSheet() + "\nbackground-color: rgba(50, 205, 50, 150);")
        else:
            self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)


class Chat(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setFixedSize(400, 600)
        self.setWindowTitle("Чат")
        self.parent = parent

        central_widget = QWidget()
        self.setCentralWidget(central_widget)


        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.ensureVisible(0, 0)

        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout()
        self.messages_container.setLayout(self.messages_layout)
        self.scroll_area.setWidget(self.messages_container)

        self.message_edit = QLineEdit()
        self.message_edit.setPlaceholderText("Введите сообщение...")

        self.send_button = QPushButton("Отправить")
        self.send_button.clicked.connect(self.send_message)

        self.return_button = QPushButton("Вернуться")
        self.return_button.clicked.connect(self.open_main)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)

        central_widget.setLayout(main_layout)

        input_layout = QHBoxLayout()

        input_layout.addWidget(self.message_edit)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.return_button)

    def add_message(self, author, text):
        message = Message(text, author)
        self.messages_layout.addWidget(message)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def send_message(self):
        text = self.message_edit.text()
        if text.strip():
            self.message_edit.clear()
            self.add_message("Вы", text)
            request, answer, is_num = elsetext(text)
            if is_num is not None:
                db.add_request(request, answer, is_num)
            self.add_message("Нейросеть", answer)

    def open_main(self):
        self.parent.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_window = Chat()
    chat_window.show()
    sys.exit(app.exec())