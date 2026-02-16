# rover_control_panel.py
import sys
import os
import socket
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QSlider, QGroupBox, QFrame, QTextEdit,
    QLCDNumber, QSizePolicy, QSplitter, QStyle, QLineEdit, QDialog, QDialogButtonBox
)
from PySide6.QtGui import QPixmap, QFont, QAction, QIcon, QKeySequence, QShortcut
from PySide6.QtCore import Qt, QTimer, QSize

class ConnectionDialog(QDialog):
    """Dialog to get Raspberry Pi IP address"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connect to Rover")
        self.resize(350, 120)
        layout = QVBoxLayout()
        
        # IP input
        ip_layout = QHBoxLayout()
        ip_label = QLabel("Raspberry Pi IP:")
        self.ip_input = QLineEdit()
        self.ip_input.setText("spaceflight-pi.local")  #192.168.2.2
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)
        layout.addLayout(ip_layout)
        
        # Port input
        port_layout = QHBoxLayout()
        port_label = QLabel("Port:")
        self.port_input = QLineEdit()
        self.port_input.setText("65432")
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)
        layout.addLayout(port_layout)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_connection_info(self):
        return self.ip_input.text(), int(self.port_input.text())

class RoverControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rover Control Panel")
        self.resize(1200, 800)
        self.setMinimumSize(1000, 700)
        
        # Connection variables
        self.socket = None
        self.connected = False
        self.rover_ip = None
        self.rover_port = None

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QGridLayout(central)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(10)

        # Left column (controls & camera)
        left_col = QVBoxLayout()
        left_col.setSpacing(10)

        # --- Top-left: Rover directional controls + top view image ---
        movement_group = QGroupBox("Rover Movement")
        movement_layout = QGridLayout()
        movement_layout.setContentsMargins(8, 8, 8, 8)
        movement_layout.setSpacing(6)

        # Center image placeholder
        self.rover_top_label = QLabel()
        self.rover_top_label.setFixedSize(220, 160)
        self.rover_top_label.setAlignment(Qt.AlignCenter)
        self._load_pixmap_into_label(self.rover_top_label, "rover_top_view.png", fallback_text="Top View\n(No image)")

        btn_style = "padding:8px; font-weight:600;"
        self.btn_forward = QPushButton("▲")
        self.btn_forward.setToolTip("Move forward (W)")
        self.btn_forward.setFixedSize(64, 40)
        self.btn_forward.setStyleSheet(btn_style)
        self.btn_forward.clicked.connect(self.move_forward)
        self.btn_forward.pressed.connect(lambda: self.move_forward())
        self.btn_forward.released.connect(self.stop_movement)

        self.btn_backward = QPushButton("▼")
        self.btn_backward.setToolTip("Move backward (S)")
        self.btn_backward.setFixedSize(64, 40)
        self.btn_backward.setStyleSheet(btn_style)
        self.btn_backward.clicked.connect(self.move_backward)
        self.btn_backward.pressed.connect(lambda: self.move_backward())
        self.btn_backward.released.connect(self.stop_movement)

        self.btn_left = QPushButton("◄")
        self.btn_left.setToolTip("Turn left (A)")
        self.btn_left.setFixedSize(64, 40)
        self.btn_left.setStyleSheet(btn_style)
        self.btn_left.clicked.connect(self.move_left)
        self.btn_left.pressed.connect(lambda: self.move_left())
        self.btn_left.released.connect(self.stop_movement)

        self.btn_right = QPushButton("►")
        self.btn_right.setToolTip("Turn right (D)")
        self.btn_right.setFixedSize(64, 40)
        self.btn_right.setStyleSheet(btn_style)
        self.btn_right.clicked.connect(self.move_right)
        self.btn_right.pressed.connect(lambda: self.move_right())
        self.btn_right.released.connect(self.stop_movement)

        movement_layout.addWidget(self.btn_forward, 0, 1, alignment=Qt.AlignCenter)
        movement_layout.addWidget(self.btn_left, 1, 0)
        movement_layout.addWidget(self.rover_top_label, 1, 1)
        movement_layout.addWidget(self.btn_right, 1, 2)
        movement_layout.addWidget(self.btn_backward, 2, 1, alignment=Qt.AlignCenter)
        movement_group.setLayout(movement_layout)
        left_col.addWidget(movement_group)

        # --- Camera group ---
        camera_group = QGroupBox("Camera & Imaging")
        cam_layout = QVBoxLayout()
        cam_layout.setSpacing(8)
        self.camera_label = QLabel()
        self.camera_label.setFixedSize(420, 260)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("border:1px solid #888; border-radius:6px;")
        self._load_pixmap_into_label(self.camera_label, "rover_generic_image.png", fallback_text="Camera Preview\n(No image)")
        cam_layout.addWidget(self.camera_label, alignment=Qt.AlignCenter)

        cam_buttons = QHBoxLayout()
        self.btn_take_picture = QPushButton("Take Picture")
        self.btn_take_picture.clicked.connect(self.take_picture)
        self.btn_stream = QPushButton("Start Stream")
        self.btn_stream.setCheckable(True)
        self.btn_stream.toggled.connect(self.toggle_stream)
        cam_buttons.addWidget(self.btn_take_picture)
        cam_buttons.addWidget(self.btn_stream)
        cam_layout.addLayout(cam_buttons)
        camera_group.setLayout(cam_layout)
        left_col.addWidget(camera_group)

        # --- Rotation / Arm controls (bottom-left) ---
        arm_group = QGroupBox("Rotation / Elevation (Arm)")
        arm_layout = QHBoxLayout()
        arm_layout.setSpacing(8)
        # image
        self.arm_label = QLabel()
        self.arm_label.setFixedSize(180, 140)
        self.arm_label.setAlignment(Qt.AlignCenter)
        self._load_pixmap_into_label(self.arm_label, "soil_collection.png", fallback_text="Arm\n(No image)")
        arm_layout.addWidget(self.arm_label)
        # controls
        controls_v = QVBoxLayout()
        self.btn_cw = QPushButton("Rotate CW")
        self.btn_cw.clicked.connect(self.rotate_cw)
        self.btn_ccw = QPushButton("Rotate CCW")
        self.btn_ccw.clicked.connect(self.rotate_ccw)
        self.btn_up = QPushButton("Up")
        self.btn_up.clicked.connect(self.move_up)
        self.btn_zero = QPushButton("Zero")
        self.btn_zero.clicked.connect(self.set_zero)
        self.btn_down = QPushButton("Down")
        self.btn_down.clicked.connect(self.move_down)
        for w in (self.btn_cw, self.btn_ccw, self.btn_up, self.btn_zero, self.btn_down):
            w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        controls_v.addWidget(self.btn_cw)
        controls_v.addWidget(self.btn_ccw)
        controls_v.addWidget(self.btn_up)
        controls_v.addWidget(self.btn_zero)
        controls_v.addWidget(self.btn_down)
        arm_layout.addLayout(controls_v)
        arm_group.setLayout(arm_layout)
        left_col.addWidget(arm_group)

        # Place left_col into a container
        left_container = QWidget()
        left_container.setLayout(left_col)

        # Right column: telemetry, settings, logs
        right_col = QVBoxLayout()
        right_col.setSpacing(10)

        # Telemetry (center)
        telemetry_group = QGroupBox("Sensors & Settings")
        tel_layout = QGridLayout()
        tel_layout.setContentsMargins(8, 8, 8, 8)
        tel_layout.setSpacing(6)

        self.temp_lcd = QLCDNumber()
        self.temp_lcd.setDigitCount(6)
        self.hum_lcd = QLCDNumber()
        self.hum_lcd.setDigitCount(6)
        self.temp_label = QLabel("Temperature (°C)")
        self.hum_label = QLabel("Humidity (%)")
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.hum_label.setAlignment(Qt.AlignCenter)
        tel_layout.addWidget(self.temp_label, 0, 0)
        tel_layout.addWidget(self.hum_label, 0, 1)
        tel_layout.addWidget(self.temp_lcd, 1, 0)
        tel_layout.addWidget(self.hum_lcd, 1, 1)

        # Mode / speed / payload controls
        mode_label = QLabel("Mode")
        self.mode_dropdown = QComboBox()
        self.mode_dropdown.addItems(["Manual", "Auto (non-existent)"])
        self.mode_dropdown.currentIndexChanged.connect(self.select_mode)
        speed_label = QLabel("Speed")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(75)
        self.speed_slider.setToolTip("Adjust rover speed")
        self.speed_slider.valueChanged.connect(self.set_speed)
        payload_label = QLabel("Payload")
        self.payload_dropdown = QComboBox()
        self.payload_dropdown.addItems(["Retracted", "Deployed", "Error"])
        self.payload_dropdown.currentIndexChanged.connect(self.check_payload)
        tel_layout.addWidget(mode_label, 2, 0)
        tel_layout.addWidget(self.mode_dropdown, 2, 1)
        tel_layout.addWidget(speed_label, 3, 0)
        tel_layout.addWidget(self.speed_slider, 3, 1)
        tel_layout.addWidget(payload_label, 4, 0)
        tel_layout.addWidget(self.payload_dropdown, 4, 1)

        telemetry_group.setLayout(tel_layout)
        right_col.addWidget(telemetry_group)

        # Connection status box
        conn_group = QGroupBox("Connection")
        conn_layout = QVBoxLayout()
        
        status_layout = QHBoxLayout()
        status_label = QLabel("Status:")
        self.conn_status_label = QLabel("Disconnected")
        self.conn_status_label.setStyleSheet("color: red; font-weight: bold;")
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.conn_status_label)
        status_layout.addStretch()
        conn_layout.addLayout(status_layout)
        
        button_layout = QHBoxLayout()
        self.btn_connect = QPushButton("Connect")
        self.btn_connect.clicked.connect(self.connect_to_rover)
        self.btn_disconnect = QPushButton("Disconnect")
        self.btn_disconnect.clicked.connect(self.disconnect_from_rover)
        self.btn_disconnect.setEnabled(False)
        button_layout.addWidget(self.btn_connect)
        button_layout.addWidget(self.btn_disconnect)
        conn_layout.addLayout(button_layout)
        
        conn_group.setLayout(conn_layout)
        right_col.addWidget(conn_group)

        # Quick actions (only Emergency Stop)
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QVBoxLayout()

        self.btn_halt = QPushButton("EMERGENCY STOP")
        self.btn_halt.setStyleSheet("""
            QPushButton {
                background:#d9534f;
                color:white;
                font-weight:bold;
                font-size:24px;
                padding:30px;
                border-radius:10px;
            }
            QPushButton:pressed {
                background:#b52b27;
            }
        """)
        self.btn_halt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_halt.clicked.connect(self.emergency_stop)

        actions_layout.addWidget(self.btn_halt)
        actions_group.setLayout(actions_layout)
        right_col.addWidget(actions_group)

        # Logs
        logs_group = QGroupBox("System Log / Log File")
        logs_layout = QVBoxLayout()
        
        # Log display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        self.log_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        logs_layout.addWidget(self.log_text)
        
        # Command input area
        cmd_input_layout = QHBoxLayout()
        cmd_label = QLabel("Houston:")
        self.cmd_input = QLineEdit()
        self.cmd_input.returnPressed.connect(self.send_text_command)
        self.btn_send_cmd = QPushButton("Send")
        self.btn_send_cmd.clicked.connect(self.send_text_command)
        cmd_input_layout.addWidget(cmd_label)
        cmd_input_layout.addWidget(self.cmd_input)
        cmd_input_layout.addWidget(self.btn_send_cmd)
        logs_layout.addLayout(cmd_input_layout)
        
        # Help text
        help_label = QLabel("Cmds: F/R/L/R <speed % (20-100)> <dur. #>, S, TestConnect, Disconnect") #Forward, Backward, Left, Right + speed percentage (20-100) or Stop
        help_label.setStyleSheet("color: #666; font-size: 6pt; font-style: italic;")
        logs_layout.addWidget(help_label)
        
        logs_group.setLayout(logs_layout)
        right_col.addWidget(logs_group)

        right_container = QWidget()
        right_container.setLayout(right_col)

        # Splitter between left and right
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_container)
        splitter.addWidget(right_container)
        splitter.setSizes([700, 400])

        root_layout.addWidget(splitter, 0, 0, 3, 3)

        # Status bar
        self.status = self.statusBar()
        self.status.showMessage("Ready - Not Connected")

        # Timers for simulated sensors / camera stream
        self.sensor_timer = QTimer(self)
        self.sensor_timer.timeout.connect(self.update_sensors)
        self.sensor_timer.start(1500)

        self.stream_timer = QTimer(self)
        self.stream_timer.timeout.connect(self._stream_frame)
        self.stream_running = False

        # Keyboard shortcuts
        QShortcut(QKeySequence('W'), self, activated=self.move_forward)
        QShortcut(QKeySequence('S'), self, activated=self.move_backward)
        QShortcut(QKeySequence('A'), self, activated=self.move_left)
        QShortcut(QKeySequence('D'), self, activated=self.move_right)
        QShortcut(QKeySequence('Space'), self, activated=self.emergency_stop)

        # Styling
        self.setStyleSheet("""
            QGroupBox { font-weight:600; border:1px solid #ccc; border-radius:6px; margin-top:6px; }
            QGroupBox:title { subcontrol-origin: margin; left:10px; padding:0 3px 0 3px; }
        """)

        # Initial log
        self.log("UI initialized. Click 'Connect' to connect to rover.")

    # --- Connection methods ---
    def connect_to_rover(self):
        """Connect to Raspberry Pi"""
        dialog = ConnectionDialog(self)
        if dialog.exec():
            ip, port = dialog.get_connection_info()
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(5)
                self.socket.connect((ip, port))
                self.connected = True
                self.rover_ip = ip
                self.rover_port = port
                
                self.conn_status_label.setText(f"Connected to {ip}")
                self.conn_status_label.setStyleSheet("color: green; font-weight: bold;")
                self.btn_connect.setEnabled(False)
                self.btn_disconnect.setEnabled(True)
                self.status.showMessage(f"Connected to rover at {ip}:{port}")
                self.log(f"Connected to rover at {ip}:{port}")
            
            except Exception as e:
                self.log(f"Connection failed: {e}")
                self.status.showMessage(f"Connection failed: {e}")
                if self.socket:
                    self.socket.close()
                    self.socket = None
    
    def disconnect_from_rover(self):
        if self.socket:
            try:
                self.socket.sendall(b'Disconnect')  # Correct
                #self.socket.close()
            except:
                pass
            self.socket = None
        self.connected = False
        self.conn_status_label.setText("Disconnected")
        self.conn_status_label.setStyleSheet("color: red; font-weight: bold;")
        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)
        self.status.showMessage("Disconnected from rover")
        self.log("Disconnected from rover")
    
    def send_command(self, command, value=None):
        if not self.connected or not self.socket:
            self.log("Error: Not connected to rover")
            return False
        
        try:
            # Format command for your server
            if value is not None:
                message = f"{command} {value}"
            else:
                message = command
            
            self.socket.sendall(message.encode('utf-8'))
            
            # Wait for response
            response = self.socket.recv(1024).decode('utf-8').strip()
            self.log(f"Rover: {response}")
            return True
        
        except Exception as e:
            self.log(f"Error sending command: {e}")
            self.disconnect_from_rover()
            return False
    
    def send_text_command(self):
        text = self.cmd_input.text().strip()
        if not text:
            return
        
        self.log(f">> {text}")
        self.cmd_input.clear()
        
        if not self.connected or not self.socket:
            self.log("Error: Not connected to rover")
            return
        
        try:
            # Send raw text command to your server
            self.socket.sendall(text.encode('utf-8'))
            
            # Wait for response
            response = self.socket.recv(1024).decode('utf-8').strip()
            self.log(f"Rover: {response}")
            
            # Check if this was a Disconnect command
            if text.lower() == 'disconnect':
                self.disconnect_from_rover()
        
        except Exception as e:
            self.log(f"Error: {e}")
            self.disconnect_from_rover()

    # --- Utility functions ---
    def _load_pixmap_into_label(self, label, path, fallback_text="(No image)"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, path)

        if os.path.exists(full_path):
            pix = QPixmap(full_path)
            if not pix.isNull():
                label.setPixmap(pix.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                return
        label.setText(fallback_text)
        label.setStyleSheet("color:#666; font-style:italic; border:1px dashed #bbb; padding:8px;")

    def log(self, text):
        from datetime import datetime
        ts = datetime.now().strftime('%H:%M:%S')
        self.log_text.append(f"[{ts}] {text}")

    # --- Movement callbacks ---
    def move_forward(self):
        self.send_command('F')
        self.log("Command: Move forward")
    
    def move_backward(self):
        self.send_command('B')
        self.log("Command: Move backward")
    
    def move_left(self):
        self.send_command('L')
        self.log("Command: Turn left")
    
    def move_right(self):
        self.send_command('R')
        self.log("Command: Turn right")
    
    def stop_movement(self):
        self.send_command('S')
        self.log("Command: Stop Movement")

    # --- Camera ---
    def take_picture(self):
        path = "rover_mars.jpg"
        self._load_pixmap_into_label(self.camera_label, path, fallback_text="Captured (no file)")
        self.log(f"Picture taken -> {path}")

    def toggle_stream(self, checked):
        if checked:
            self.stream_running = True
            self.stream_timer.start(500)
            self.btn_stream.setText("Stop Stream")
            self.log("Camera stream started")
        else:
            self.stream_running = False
            self.stream_timer.stop()
            self.btn_stream.setText("Start Stream")
            self.log("Camera stream stopped")

    def _stream_frame(self):
        cur = self.camera_label.styleSheet()
        if "#88f" in cur:
            self.camera_label.setStyleSheet("border:1px solid #888; border-radius:6px;")
        else:
            self.camera_label.setStyleSheet("border:2px solid #88f; border-radius:6px;")

    # --- Arm / rotation ---
    def rotate_cw(self):
        self.log("Rotate arm clockwise")
    def rotate_ccw(self):
        self.log("Rotate arm counter-clockwise")
    def move_up(self):
        self.log("Arm up")
    def set_zero(self):
        self.log("Arm set to zero position")
    def move_down(self):
        self.log("Arm down")

    # --- Settings callbacks ---
    def select_mode(self, idx):
        self.log(f"Mode: {self.mode_dropdown.currentText()}")
    
    def set_speed(self, val):
        self.log(f"Speed set to {val}% (will apply on next movement command)")
    
    def check_payload(self, idx):
        self.log(f"Payload: {self.payload_dropdown.currentText()}")

    def emergency_stop(self):
        self.send_command('Stop')
        self.log("!!! EMERGENCY STOP ACTIVATED !!!")

    # --- Sensors ---
    def update_sensors(self):
        import random
        temp = round(random.uniform(23, 25), 1)
        hum = round(random.uniform(70, 75), 1)
        try:
            self.temp_lcd.display(f"{temp}")
            self.hum_lcd.display(f"{hum}")
        except Exception:
            self.temp_lcd.display(0)
            self.hum_lcd.display(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = RoverControlPanel()
    w.show()
    sys.exit(app.exec())