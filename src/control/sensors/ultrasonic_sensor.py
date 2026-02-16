import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

print("Distance Measurement In Progress...")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("Waiting For Sensor To Settle...")
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO) == 0:
    pulse_start = time.time()

while GPIO.input(ECHO) == 1:
    pulse_end = time.time()

pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)

print("Distance:". distance, "cm")
GPIO.cleanup()

class Ultrasonic():
    def __init__(self, trig_pin: int,echo_pin: int):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trig_pin, False)
        time.sleep(2)

    def cleanup(self):
        GPIO.cleanup()

    def read(self) -> float:
        """
            Reads a value from the ultrasonic sensor

            Returns:
                float: The distance value from the ultrasonic sensor
        """
        GPIO.output(self.trig_pin, True)
        time.sleep(0.0001)
        GPIO.output(self.trig_pin, False)

        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
        
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        return round(distance, 2)

if __name__ == "__main_":
    sensor = Ultrasonic(trig_pin = 23, echo_pin = 24)
    try:
        while True:
            print(f"Distance: {sensor.read()} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped")
        sensor.cleanup()