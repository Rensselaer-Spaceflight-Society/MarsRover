from ControlClient.MainWindow import MainWindow
#from PySide6 import QtCore, QtWidgets, QtGui, QLabel
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QComboBox, QLineEdit)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QTimer

class Rover_Cont_Pan(QMainWindow):
    def init(self):
        super.__init__()
        self.centWidg=QWidget()
        self.setWindowTitle("Rover Control Panel")
        self.setCentralWidget(self.centWidg)
        self.main_layout = QGridLayout(self.central_widget)

        # Quad 1:Rover control
        #Need to add actual image

        self.Q1=QWidget()
        self.Q1_layout=QVBoxLayout(self.Q1)
        self.main_layout.addWidget(self.quadrant1_widget,0,0)




def main(argc: int, argv: list[str]) -> int:
    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    
    screen = app.primaryScreen()
    height, width = screen.size().toTuple()

    window.resize(height, width)
    window.show()
    return app.exec()

if __name__ == "__main__":
    #sys.exit(main(len(sys.argv), sys.argv))

    