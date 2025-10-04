from PySide6 import QtCore, QtWidgets, QtGui, QtBluetooth
from ControlClient.Components.MovementWidget import MovementWidget
from ControlClient.Components.SoilCollectionWidget import SoilCollectionWidget
from ControlClient.Components.PanoramaWidget import PanoramaWidget
from ControlClient.Components.SensorWidget import SensorWidget
from ControlClient.Components.CustomCommandWidget import CustomCommandWidget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Client")
        self.setCentralWidget(CentralWidget())

class CentralWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(QLine(QtWidgets.QFrame.Shape.HLine))
        self.layout().addWidget(RoverControlWidget())

class RoverControlWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QHBoxLayout())
        self.left_widget = LeftWidget()
        self.right_widget = RightWidget()
        self.seperator = QLine(QtWidgets.QFrame.Shape.VLine)
        self.seperator.setFrameShape(QtWidgets.QFrame.Shape.VLine)

        self.layout().addWidget(self.left_widget)
        self.layout().addWidget(self.seperator)
        self.layout().addWidget(self.right_widget)


        
class LeftWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(MovementWidget())
        self.layout().addWidget(QLine(QtWidgets.QFrame.Shape.HLine))
        self.layout().addWidget(SoilCollectionWidget())

class RightWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        self.panorama_widget = PanoramaWidget()
        self.sensor_widget = SensorWidget()
        self.custom_command_widget = CustomCommandWidget()

        self.sensor_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)

        self.layout().addWidget(self.panorama_widget)
        self.layout().addWidget(QLine(QtWidgets.QFrame.Shape.HLine))
        self.layout().addWidget(self.sensor_widget)
        self.layout().addWidget(QLine(QtWidgets.QFrame.Shape.HLine))
        self.layout().addWidget(self.custom_command_widget)

class QLine(QtWidgets.QFrame):
    def __init__(self, direction: QtWidgets.QFrame.Shape):
        super().__init__()
        self.setFrameShape(direction)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.setLineWidth(2)
        self.setMidLineWidth(2)

