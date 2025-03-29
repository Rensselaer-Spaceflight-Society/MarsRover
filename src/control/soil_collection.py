from ..motors.stepper_motor import DRV8825
from ..sensors.ultrasonic_sensor import Ultrasonic

class SoilCollector:
    def __init__(self, motor_pins, ultrasonic_pins):
        # Initialize the stepper motor and ultrasonic sensor
        self.scoop_motor = DRV8825(*motor_pins)
        self.ultrasonic_sensor = Ultrasonic(*ultrasonic_pins)
    
    def lower_scoop(self):
        # Lowers the scoop until it's near the ground
        print("Lowering scoop...")
        while True:
            distance = self.ultrasonic_sensor.get_distance()
            print(f"Distance to ground: {distance} cm")
            if distance <= 5: # Stop lowering when the scoop is 5 cm from the ground
                print("Scoop is near the ground.")
                break
            self.scoop_motor.step_down() # Move the motor to lower the scoop
    
    def collect_soil(self):
        # Performs a scooping motion
        print("Collecting soil...")
        for i in range(10): # Perform a back-and-forth motion
            self.scoop_motor.step_forward()
            self.scoop_motor.step_backward()
    
    def raise_scoop(self):
        # Raises the scoop back up
        print("Raising scoop...")
        for i in range(50): # Adjust the number of steps as needed
            self.scoop_motor.step_up()
    
    def collect_soil(self):
        # Main method to collect soil
        self.lower_scoop()
        self.scoop_soil()
        self.raise_scoop()

# Example usage
if __name__ == "__main__":
    motor_pins = (7, 8, 26, 19)
    ultrasonic_pins = (23, 24)

    soil_collector = SoilCollector(motor_pins, ultrasonic_pins)
    soil_collector.collect_soil()