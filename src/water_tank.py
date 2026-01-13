try:
  import RPi.GPIO as GPIO
except ImportError:
  pass
import time
import random

class WaterTank:
  ULTRASONIC_TRIGGER = 15
  ULTRASONIC_ECHO = 16
  
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

  def measure_distance(self):
    GPIO.output(WaterTank.ULTRASONIC_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(WaterTank.ULTRASONIC_TRIGGER, GPIO.LOW)
    
    while GPIO.input(WaterTank.ULTRASONIC_ECHO) == 0:
      pulse_start = time.time()
      
    while GPIO.input(WaterTank.ULTRASONIC_ECHO) == 1:
      pulse_end = time.time()
      
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # in cm
    return round(distance, 2)
      
class WaterTankLocal:
  def __init__(self):
    print(f"WATERTANK::starting as {type(self).__name__} mode...")

  def measure_distance(self):
    return round(random.uniform(0, 100), 2) # dummy distance
    
  def shutdown(self):
    print("WATERTANK::(local) goodbye!")
