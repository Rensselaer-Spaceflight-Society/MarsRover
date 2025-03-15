from PySide6 import QtCore, QtWidgets, QtGui

class SoilCollectionWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(QtWidgets.QLabel("Soil Collection Widget"))