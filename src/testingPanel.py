import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QComboBox, QLineEdit)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QTimer

class RoverControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rover Control Panel")
        self.setGeometry(100, 100, 1200, 800) # Increased window size

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QGridLayout(self.central_widget)

        # Quadrant 1: Top Left (Rover Top View + Directional Controls)
        self.quadrant1_widget = QWidget()
        self.quadrant1_layout = QVBoxLayout(self.quadrant1_widget)
        self.quadrant1_layout.addWidget(QLabel("Top Left: Rover Movement"))
        self.main_layout.addWidget(self.quadrant1_widget, 0, 0) # Row 0, Col 0

        # Quadrant 2: Top Right (Camera Capture + Display)
        self.quadrant2_widget = QWidget()
        self.quadrant2_layout = QVBoxLayout(self.quadrant2_widget)
        self.quadrant2_layout.addWidget(QLabel("Top Right: Camera"))
        self.main_layout.addWidget(self.quadrant2_widget, 0, 2) # Row 0, Col 2

        # Quadrant 3: Bottom Left (Another Image + CW/CCW + Up/Zero/Down)
        self.quadrant3_widget = QWidget()
        self.quadrant3_layout = QVBoxLayout(self.quadrant3_widget)
        self.quadrant3_layout.addWidget(QLabel("Bottom Left: Rotation/Elevation"))
        self.main_layout.addWidget(self.quadrant3_widget, 2, 0) # Row 2, Col 0

        # Quadrant 4: Bottom Right (Custom Control Panel)
        self.quadrant4_widget = QWidget()
        self.quadrant4_layout = QVBoxLayout(self.quadrant4_widget)
        self.quadrant4_layout.addWidget(QLabel("Bottom Right: Custom Controls"))
        self.main_layout.addWidget(self.quadrant4_widget, 2, 2) # Row 2, Col 2

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

    def setup_quadrant1(self):
        layout = QVBoxLayout()

        # Rover image
        rover_image_label = QLabel()
        pixmap = QPixmap("rover_top_view.png") # Changed path for local execution
        rover_image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        rover_image_label.setAlignment(Qt.AlignCenter)

        # Directional controls
        control_layout = QGridLayout()
        self.btn_forward = QPushButton("Forward")
        self.btn_forward.clicked.connect(self.move_forward)
        self.btn_backward = QPushButton("Backward")
        self.btn_backward.clicked.connect(self.move_backward)
        self.btn_left = QPushButton("Left")
        self.btn_left.clicked.connect(self.move_left)
        self.btn_right = QPushButton("Right")
        self.btn_right.clicked.connect(self.move_right)

        control_layout.addWidget(self.btn_forward, 0, 1) # Top
        control_layout.addWidget(self.btn_left, 1, 0)    # Left
        control_layout.addWidget(rover_image_label, 1, 1) # Center image
        control_layout.addWidget(self.btn_right, 1, 2)   # Right
        control_layout.addWidget(self.btn_backward, 2, 1) # Bottom

        layout.addLayout(control_layout)
        self.quadrant1_layout.addLayout(layout)

    def move_forward(self):
        print("Moving Forward")
        # Generic function for moving forward

    def move_backward(self):
        print("Moving Backward")
        # Generic function for moving backward

    def move_left(self):
        print("Moving Left")
        # Generic function for moving left

    def move_right(self):
        print("Moving Right")
        # Generic function for moving right


    def setup_quadrant2(self):
        layout = QVBoxLayout()

        self.camera_display_label = QLabel("Camera Feed / Captured Image")
        self.camera_display_label.setAlignment(Qt.AlignCenter)
        self.camera_display_label.setFixedSize(300, 200) # Placeholder size
        self.camera_display_label.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.camera_display_label)

        self.btn_take_picture = QPushButton("Take Picture")
        self.btn_take_picture.clicked.connect(self.take_picture)
        layout.addWidget(self.btn_take_picture)

        self.quadrant2_layout.addLayout(layout)

    def take_picture(self):
        print("Taking picture...")
        # Simulate saving an image and displaying it
        # In a real scenario, this would capture from a camera and save to a file
        captured_image_path = "rover_generic_image.png" # Changed path for local execution
        self.display_image(captured_image_path)
        print(f"Picture saved to {captured_image_path}")

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.camera_display_label.setPixmap(pixmap.scaled(self.camera_display_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.camera_display_label.setText("Error loading image")

    def setup_quadrant3(self):
        layout = QHBoxLayout()

        # Image
        generic_image_label = QLabel()
        pixmap = QPixmap("rover_generic_image.png") # Changed path for local execution
        generic_image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        generic_image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(generic_image_label)

        # CW/CCW buttons
        rotation_layout = QVBoxLayout()
        self.btn_cw = QPushButton("CW")
        self.btn_cw.clicked.connect(self.rotate_cw)
        self.btn_ccw = QPushButton("CCW")
        self.btn_ccw.clicked.connect(self.rotate_ccw)
        rotation_layout.addWidget(self.btn_cw)
        rotation_layout.addWidget(self.btn_ccw)
        layout.addLayout(rotation_layout)

        # Up/Zero/Down buttons
        elevation_layout = QVBoxLayout()
        self.btn_up = QPushButton("Up")
        self.btn_up.clicked.connect(self.move_up)
        self.btn_zero = QPushButton("Zero")
        self.btn_zero.clicked.connect(self.set_zero)
        self.btn_down = QPushButton("Down")
        self.btn_down.clicked.connect(self.move_down)
        elevation_layout.addWidget(self.btn_up)
        elevation_layout.addWidget(self.btn_zero)
        elevation_layout.addWidget(self.btn_down)
        layout.addLayout(elevation_layout)

        self.quadrant3_layout.addLayout(layout)

    def rotate_cw(self):
        print("Rotating Clockwise")
        # Generic function for rotating clockwise

    def rotate_ccw(self):
        print("Rotating Counter-Clockwise")
        # Generic function for rotating counter-clockwise

    def move_up(self):
        print("Moving Up")
        # Generic function for moving up

    def set_zero(self):
        print("Setting to Zero Position")
        # Generic function for setting to zero position

    def move_down(self):
        print("Moving Down")
        # Generic function for moving down


    def setup_quadrant4(self):
        layout = QVBoxLayout()

        # Dropdown 1
        layout.addWidget(QLabel("Mode Selection:"))
        self.mode_dropdown = QComboBox()
        self.mode_dropdown.addItems(["Manual", "Autonomous", "Semi-Autonomous"])
        self.mode_dropdown.currentIndexChanged.connect(self.select_mode)
        layout.addWidget(self.mode_dropdown)

        # Dropdown 2
        layout.addWidget(QLabel("Speed Setting:"))
        self.speed_dropdown = QComboBox()
        self.speed_dropdown.addItems(["Slow", "Medium", "Fast"])
        self.speed_dropdown.currentIndexChanged.connect(self.set_speed)
        layout.addWidget(self.speed_dropdown)

        # Dropdown 3
        layout.addWidget(QLabel("Payload Status:"))
        self.payload_dropdown = QComboBox()
        self.payload_dropdown.addItems(["Deployed", "Retracted", "Error"])
        self.payload_dropdown.currentIndexChanged.connect(self.check_payload)
        layout.addWidget(self.payload_dropdown)

        # Generic Action Button
        self.btn_apply_settings = QPushButton("Apply Settings")
        self.btn_apply_settings.clicked.connect(self.apply_settings)
        layout.addWidget(self.btn_apply_settings)

        self.quadrant4_layout.addLayout(layout)

    def select_mode(self, index):
        mode = self.mode_dropdown.currentText()
        print(f"Mode selected: {mode}")
        # Generic function for mode selection

    def set_speed(self, index):
        speed = self.speed_dropdown.currentText()
        print(f"Speed set to: {speed}")
        # Generic function for speed setting

    def check_payload(self, index):
        status = self.payload_dropdown.currentText()
        print(f"Payload status: {status}")
        # Generic function for payload status

    def apply_settings(self):
        print("Applying custom settings...")
        # Generic function for applying settings


    def setup_center_sensors(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.temp_label = QLabel("Temperature: -- °C")
        self.temp_label.setFont(QFont("Arial", 24))
        self.temp_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.temp_label)

        self.humidity_label = QLabel("Humidity: -- %")
        self.humidity_label.setFont(QFont("Arial", 24))
        self.humidity_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.humidity_label)

        self.center_layout.addLayout(layout)

        # Simulate sensor updates
        self.sensor_timer = QTimer(self)
        self.sensor_timer.timeout.connect(self.update_sensors)
        self.sensor_timer.start(2000) # Update every 2 seconds

    def update_sensors(self):
        import random
        temp = round(random.uniform(-20, 40), 1) # -20 to 40 Celsius
        humidity = round(random.uniform(0, 100), 1) # 0 to 100 percent
        self.temp_label.setText(f"Temperature: {temp} °C")
        self.humidity_label.setText(f"Humidity: {humidity} %")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoverControlPanel()
    window.show()
    sys.exit(app.exec())
