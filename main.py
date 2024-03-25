import sys
from PyQt5.QtWidgets import QApplication
from View.mainWindow import MyMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    sys.exit(app.exec())