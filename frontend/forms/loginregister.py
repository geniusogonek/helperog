import  sys

from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel, QMainWindow, QApplication
from forms.helperog import Helperog

class LoginWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app

        self.setFixedSize(240, 310)
        self.setWindowTitle("Авторизация")

        self.label = QLabel(self)
        self.label.setText("Авторизация")
        self.label.setGeometry(75, 10, 140, 30)

        self.getUsername = QLineEdit(self)
        self.getUsername.setGeometry(50, 50, 140, 30)
        self.getUsername.setPlaceholderText("Имя пользователя")

        self.getPassword = QLineEdit(self)
        self.getPassword.setGeometry(50, 100, 140, 30)
        self.getPassword.setPlaceholderText("Пароль")

        self.loginButton = QPushButton(self)
        self.loginButton.setGeometry(50, 150, 140, 30)
        self.loginButton.setText("Вход")
        self.loginButton.clicked.connect(self.login)

        self.toRegisterButton = QPushButton(self)
        self.toRegisterButton.setGeometry(50, 200, 140, 30)
        self.toRegisterButton.setText("Нет аккаунта?")
        self.toRegisterButton.clicked.connect(self.open_register)

        self.skipButton = QPushButton(self)
        self.skipButton.setGeometry(50, 250, 140, 30)
        self.skipButton.setText("Пропустить")
        self.skipButton.clicked.connect(self.open_main)

        self.main = Helperog(self.app)

    def open_main(self):
        self.main.show()
        self.hide()

    def open_register(self):
        self.register = RegisterWindow(self)
        self.register.show()
        self.hide()

    def login(self):
        

class RegisterWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setFixedSize(240, 310)
        self.setWindowTitle("Регистрация")

        self.label = QLabel(self)
        self.label.setText("Регистрация")
        self.label.setGeometry(75, 10, 140, 30)

        self.getUsername = QLineEdit(self)
        self.getUsername.setGeometry(50, 50, 140, 30)
        self.getUsername.setPlaceholderText("Имя пользователя")

        self.getPassword = QLineEdit(self)
        self.getPassword.setGeometry(50, 100, 140, 30)
        self.getPassword.setPlaceholderText("Пароль")

        self.registerButton = QPushButton(self)
        self.registerButton.setGeometry(50, 150, 140, 30)
        self.registerButton.setText("Регистрация")

        self.toLoginButton = QPushButton(self)
        self.toLoginButton.setGeometry(50, 200, 140, 30)
        self.toLoginButton.setText("Есть аккаунта?")
        self.toLoginButton.clicked.connect(self.open_login)

        self.skipButton = QPushButton(self)
        self.skipButton.setGeometry(50, 250, 140, 30)
        self.skipButton.setText("Пропустить")
        self.skipButton.clicked.connect(self.open_main)

    def open_main(self):
        self.main = Helperog(self.parent.app)
        self.main.show()
        self.hide()

    def open_login(self):
        self.parent.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LoginWindow(app)
    ex.show()
    sys.exit(app.exec())