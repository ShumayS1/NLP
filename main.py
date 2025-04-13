
from gui.interface import CompatibilityApp
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompatibilityApp()
    window.show()
    sys.exit(app.exec_())
