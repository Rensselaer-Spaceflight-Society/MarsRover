from ControlClient.MainWindow import MainWindow
from PySide6 import QtCore, QtWidgets, QtGui
import sys

# Hello World

def main(argc: int, argv: list[str]) -> int:
    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    
    screen = app.primaryScreen()
    height, width = screen.size().toTuple()

    window.resize(height, width)
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
    