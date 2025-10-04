from PySide6 import QtCore, QtWidgets, QtGui

class PanoramaWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(QtWidgets.QLabel("Panorama Widget"))