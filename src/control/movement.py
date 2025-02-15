from ..motors.dc_motor import DRV8871

LEFT_IN_1_PIN = 7
LEFT_IN_2_PIN = 8

LEFT_SIDE_MOTOR = DRV8871(in1_pin=LEFT_IN_1_PIN, in2_pin=LEFT_IN_2_PIN)

RIGHT_IN_1_PIN = 26
RIGHT_IN_2_PIN = 19

RIGHT_SIDE_MOTOR = DRV8871(in1_pin=RIGHT_IN_1_PIN, in2_pin=RIGHT_IN_2_PIN)

LEFT_SIDE_MOTOR.setup()
RIGHT_SIDE_MOTOR.setup()

def forward() -> None:
    LEFT_SIDE_MOTOR.clockwise()
    RIGHT_SIDE_MOTOR.clockwise()

def backward() -> None:
    LEFT_SIDE_MOTOR.counter_clockwise()
    RIGHT_SIDE_MOTOR.counter_clockwise()

def left() -> None:
    LEFT_SIDE_MOTOR.counter_clockwise()
    RIGHT_SIDE_MOTOR.clockwise()

def right() -> None:
    LEFT_SIDE_MOTOR.clockwise()
    RIGHT_SIDE_MOTOR.counter_clockwise()

def stop() -> None:
    LEFT_SIDE_MOTOR.stop()
    RIGHT_SIDE_MOTOR.stop()

def cleanup() -> None:
    LEFT_SIDE_MOTOR.cleanup()
    RIGHT_SIDE_MOTOR.cleanup()

