import RPi.GPIO as GPIO
import time

# GPIO pin numbers
STEP_PIN = 20  # Step GPIO pin
DIR_PIN = 21  # Direction GPIO pin
ENABLE_PIN = 16  # Enable GPIO pin (optional)

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)

# Function to enable the motor driver
def enable_motor():
    GPIO.output(ENABLE_PIN, GPIO.LOW)  # Enable motor driver (active low)

# Function to disable the motor driver
def disable_motor():
    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Disable motor driver

# Function to rotate stepper motor
def stepper_motor(steps, direction, delay):
    # Set direction
    GPIO.output(DIR_PIN, GPIO.HIGH if direction == 'cw' else GPIO.LOW)
    
    # Step through the motor
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(delay)  # Control speed by adjusting the delay
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(delay)

# Main program
if __name__ == "__main__":
    try:
        enable_motor()
        
        # Rotate motor 200 steps clockwise (1 revolution if 200 steps/rev motor)
        stepper_motor(2000, 'cw', 0.01)

        # Rotate motor 200 steps counterclockwise
        time.sleep(1)
        # stepper_motor(2000, 'ccw', 0.1)

    except KeyboardInterrupt:
        print("Program stopped")

    finally:
        disable_motor()
        GPIO.cleanup()
