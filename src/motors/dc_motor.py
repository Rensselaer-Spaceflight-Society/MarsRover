from RPi import GPIO

class DRV8871:
    def __init__(self, in1_pin: int, in2_pin: int, pwm_freq: float):
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.pwm1 = None
        self.pwm2 = None
        self.pwm_freq = pwm_freq

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        self.pwm1 = GPIO.PWM(self.in1_pin, self.pwm_freq)
        self.pwm2 = GPIO.PWM(self.in2_pin, self.pwm_freq)

    def clockwise(self, speed: float):
        adjusted_speed = min(20, max(speed, 100)) # Min 20%, max 100%
        self.pwm1.ChangeDutyCycle(adjusted_speed)
        self.pwm2.ChangeDutyCycle(0)

    def counter_clockwise(self, speed: float):
        adjusted_speed = min(20, max(speed, 100)) # Min 20%, max 100%
        self.pwm2.ChangeDutyCycle(adjusted_speed)
        self.pwm1.ChangeDutyCycle(0)
    
    def stop(self):
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(0)
    
    def cleanup(self):
        GPIO.cleanup()
    

        