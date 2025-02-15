from RPi import GPIO

class DRV8871:
    def __init__(self, in1_pin: int, in2_pin: int):
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)

    def clockwise(self):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)

    def counter_clockwise(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)
    
    def stop(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
    
    def cleanup(self):
        GPIO.cleanup()
    

        