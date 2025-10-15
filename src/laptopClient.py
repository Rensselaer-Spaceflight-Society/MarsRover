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
        self.main_layout.addWidget(self.Q1,0,0)

        # Quad 2: Camera/Panorama
        self.Q2=QWidget()
        self.Q2=QVBoxLayout(self.Q2)
        self.main_layout.addWidget(self.Q2,0,2)

        # Quad 3: Soil Collection
        self.Q3=QWidget()
        self.quadrant3_layout=QVBoxLayout(self.Q3)
        self.main_layout.addWidget(self.Q3,2,0)

        # Quad 4: Custom Panel
        self.Q4=QWidget()
        self.quadrant4_layout=QVBoxLayout(self.Q4)
        self.main_layout.addWidget(self.Q4,2,2)

        # Center: Temp and Humidity Sensor Output
        self.center_widget = QWidget()
        self.center_layout = QVBoxLayout(self.center_widget)
        self.center_layout.addWidget(QLabel("Center: Sensor Readings"))
        self.main_layout.addWidget(self.center_widget, 1, 1) # Row 1, Col 1

        # Placeholder for spacing (optional, but good for visual separation)
        self.main_layout.setRowStretch(0, 1)
        self.main_layout.setRowStretch(1, 1)
        self.main_layout.setRowStretch(2, 1)
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 1)
        self.main_layout.setColumnStretch(2, 1)

        self.setup_quadrant1()
        self.setup_quadrant2()
        self.setup_quadrant3()
        self.setup_quadrant4()
        self.setup_center_sensors()

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
