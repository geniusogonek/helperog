import sys

from PyQt6.QtWidgets import QApplication
from forms.loginregister import LoginWindow
from forms.helperog import Helperog


def main():
    app = QApplication(sys.argv)
    if sys.argv[-1] == "test":
        login = LoginWindow(app)
        login.show()
        login.helperog.stop_thread(app.exec())
        sys.exit()
    else:
        helperog = Helperog(app)
        helperog.show()
        helperog.stop_thread(app.exec())
        sys.exit()


if __name__ == "__main__":
    main()