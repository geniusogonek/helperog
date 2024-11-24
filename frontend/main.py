import sys

from PyQt6.QtWidgets import QApplication
from forms.loginregister import LoginWindow


def main():
    app = QApplication(sys.argv)
    login = LoginWindow(app)
    login.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
