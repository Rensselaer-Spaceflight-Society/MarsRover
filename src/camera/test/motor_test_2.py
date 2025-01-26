import RPi.GPIO as GPIO
import time

# Define GPIO pins for the stepper motor (will be adjusted, probably!)
IN1 = 17 # Pin for IN1
IN2 = 27 # Pin for IN2
IN3 = 22 # Pin for IN3
IN4 = 23 # Pin for IN4

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

GPIO.cleanup()

# Set the pins as outputs
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Define the sequence for controlling the stepper motor
seq = [
    [1,0,0,0], # Step 1
    [1,1,0,0], # step 2
    [0,1,0,0], # Step 3
    [0,1,1,0], # Step 4
    [0,0,1,0], # Step 5
    [0,0,1,1], # Step 6
    [0,0,0,1], # Step 7
    [1,0,0,1] # Step 8
]

# Function to make the motor rotate one step
def step_motor(step):
    GPIO.output(IN1, seq[step][0])
    GPIO.output(IN2, seq[step][1])
    GPIO.output(IN3, seq[step][2])
    GPIO.output(IN4, seq[step][3])

# Function to rotate the motor clockwise for a set number of steps
def clockwise_rotate(steps, delay = 0.01):
    for i in range(steps):
        for step in range(8):
            step_motor(step)
            time.sleep(delay)

# Function to rotate the motor counter-clockwise for a set number of steps
def counter_clockwise_rotate(steps, delay = 0.01):
    for i in range(steps):
        for step in range(7,-1,-1):
            step_motor(step)
            time.sleep(delay)

try:
    while True:
        print("Rotating clockwise")
        clockwise_rotate(2000, 0.001) # Rotate clockwise 2000 steps (will be adjusted, probably!)
        time.sleep(1)
        print("Rotating counter-clockwise")
        counter_clockwise_rotate(2000, 0.001) # Rotate counter-clockwise 512 steps (will be adjusted, probably!)
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    GPIO.cleanup()