from PySide6 import QtCore, QtWidgets, QtGui

class MovementWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        
        self.forwardButton = QtWidgets.QPushButton("Forward")
        self.backwardButton = QtWidgets.QPushButton("Backward")
        self.central_widget = CentralWidget()

        self.layout().addWidget(self.forwardButton)
        self.layout().addWidget(self.central_widget)
        self.layout().addWidget(self.backwardButton)
        

class CentralWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QHBoxLayout())

        self.rover_picture = QtWidgets.QLabel()
        self.rover_picture.setPixmap(QtGui.QPixmap("placeholder.jpg"))

        self.leftButton = QtWidgets.QPushButton("Left")
        self.rightButton = QtWidgets.QPushButton("Right")

        self.layout().addWidget(self.leftButton)
        self.layout().addWidget(self.rover_picture)
        self.layout().addWidget(self.rightButton)
