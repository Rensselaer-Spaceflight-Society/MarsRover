import RPi.GPIO as GPIO
import time
DIR_PIN = 20  # Direction GPIO pin
STEP_PIN = 21


GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)

try:
    while True:
        print("Switching")
        GPIO.output(DIR_PIN, GPIO.HIGH)
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(4)
        print("Switching")
        GPIO.output(DIR_PIN, GPIO.LOW)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(4)
except:
    GPIO.output(DIR_PIN, GPIO.LOW)
    GPIO.cleanup()
