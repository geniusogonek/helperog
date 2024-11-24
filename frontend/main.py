import sys

from PyQt6.QtWidgets import QApplication
from forms.loginregister import LoginWindow
from forms.helperog import Helperog


def main():
    app = QApplication(sys.argv)
    if sys.argv[-1] == "test":
        login = LoginWindow(app)
        login.show()
    else:
        helperog = Helperog(app)
        helperog.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()