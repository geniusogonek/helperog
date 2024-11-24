import sys

from PyQt6.QtWidgets import QApplication
from forms.helperog import Helperog


def main():
    app = QApplication(sys.argv)
    helperog = Helperog(app)
    helperog.show()
    helperog.stop_thread(app.exec())
    sys.exit()


if __name__ == "__main__":
    main()
