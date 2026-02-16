from .motors.dc_motor import DRV8871

LEFT_IN_1_PIN = 17
LEFT_IN_2_PIN = 18

LEFT_SIDE_MOTOR = DRV8871(in1_pin=LEFT_IN_1_PIN, in2_pin=LEFT_IN_2_PIN, pwm_freq=1000)

RIGHT_IN_1_PIN = 22
RIGHT_IN_2_PIN = 23

RIGHT_SIDE_MOTOR = DRV8871(in1_pin=RIGHT_IN_1_PIN, in2_pin=RIGHT_IN_2_PIN, pwm_freq=1000)

def setup():
    LEFT_SIDE_MOTOR.setup()
    RIGHT_SIDE_MOTOR.setup()

def forward(speed: float = 75.0) -> None:
    LEFT_SIDE_MOTOR.clockwise(speed)
    RIGHT_SIDE_MOTOR.clockwise(speed)

def backward(speed: float = 75.0) -> None:
    LEFT_SIDE_MOTOR.counter_clockwise(speed)
    RIGHT_SIDE_MOTOR.counter_clockwise(speed)

def left(speed: float = 75.0) -> None:
    LEFT_SIDE_MOTOR.counter_clockwise(speed)
    RIGHT_SIDE_MOTOR.clockwise(speed)

def right(speed: float = 75.0) -> None:
    LEFT_SIDE_MOTOR.clockwise(speed)
    RIGHT_SIDE_MOTOR.counter_clockwise(speed)

def stop() -> None:
    LEFT_SIDE_MOTOR.stop()
    RIGHT_SIDE_MOTOR.stop()

def cleanup() -> None:
    LEFT_SIDE_MOTOR.cleanup()
    RIGHT_SIDE_MOTOR.cleanup()

