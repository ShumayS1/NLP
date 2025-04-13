import sys
from PyQt5.QtWidgets import QApplication
from gui.interface import CompatibilityApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompatibilityApp()
    window.show()
    sys.exit(app.exec())
