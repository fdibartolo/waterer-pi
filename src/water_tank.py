try:
  import RPi.GPIO as GPIO
except ImportError:
  pass
import time
import random

class WaterTank:
  ULTRASONIC_TRIGGER = 15
  ULTRASONIC_ECHO = 16
  
  SENSOR_OFFSET = 12  # distance from sensor to tank top level (when 100% full) in cm
  EMPTY_DISTANCE = 107  # distance from sensor to tank bottom level (when considered empty) in cm
  
  def __init__(self):
    print(f"WATERTANK::starting as {type(self).__name__} mode...")

    # pinout setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(WaterTank.ULTRASONIC_TRIGGER, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(WaterTank.ULTRASONIC_ECHO, GPIO.IN)

    time.sleep(2)  # sensor settle time
    print("WATERTANK::ready!")

  def shutdown(self):
    GPIO.cleanup()
    print("WATERTANK::goodbye!")

  def __to_percentage(self, dist):
    if dist <= self.SENSOR_OFFSET:
      return 100
    elif dist >= self.EMPTY_DISTANCE:
      return 0
    else:
      percentage = 100 - ((dist - self.SENSOR_OFFSET)/(self.EMPTY_DISTANCE - self.SENSOR_OFFSET)*100)
      return round(percentage, 0)
    
  def measure_distance(self):
    GPIO.output(WaterTank.ULTRASONIC_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(WaterTank.ULTRASONIC_TRIGGER, GPIO.LOW)
    
    while GPIO.input(WaterTank.ULTRASONIC_ECHO) == 0:
      pulse_start = time.time()
      
    while GPIO.input(WaterTank.ULTRASONIC_ECHO) == 1:
      pulse_end = time.time()
      
    pulse_duration = pulse_end - pulse_start
    dist = pulse_duration * 17150  # in cm
    return self.__to_percentage(dist)
      
class WaterTankLocal:
  def __init__(self):
    print(f"WATERTANK::starting as {type(self).__name__} mode...")

  def measure_distance(self):
    return round(random.uniform(0, 100), 2) # dummy distance
    
  def shutdown(self):
    print("WATERTANK::(local) goodbye!")
