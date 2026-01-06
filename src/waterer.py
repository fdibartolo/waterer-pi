try:
  import RPi.GPIO as GPIO
except ImportError:
  pass
import time
import datetime
from os import environ as env

class Waterer:
  def __init__(self, file_manager):
    self.file_manager = file_manager

    # pinout setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.IN) # button
    GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW) # led
    GPIO.setup(7, GPIO.OUT, initial=GPIO.HIGH) # rele 1
    GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH) # rele 2

    print("WATERER::initializing...")
    GPIO.output(7, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    now = datetime.datetime.now()
    while (datetime.datetime.now() - now).seconds < 3:
      self.toggle_led()
    print("WATERER::ready!")

  def toggle_led(self):
    GPIO.output(11, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(11, GPIO.LOW)
    time.sleep(0.5)

  def shutdown(self):
    GPIO.cleanup()
    print("WATERER::goodbye!")

  def is_button_pressed(self):
    return (GPIO.input(3) == 0)

  def __isnt_stop_requested(self):
    return (env.get('IS_WATERING') == 'True')

  def water(self, source):
    env['IS_WATERING'] = 'True'
    print("Water IS_WATERING = True")
    self.file_manager.write(source)
    print("WATERER::triggered via " + source)
    print("WATERER::start watering area 1...")
    time_area_1 = int(env.get('TIME_AREA_1'))
    now = datetime.datetime.now()
    GPIO.output(7, GPIO.LOW)
    while self.__isnt_stop_requested() and ((datetime.datetime.now() - now).seconds < time_area_1):
      self.toggle_led()
    GPIO.output(7, GPIO.HIGH)

    print("WATERER::stop area 1 and start watering area 2...")
    time_area_2 = int(env.get('TIME_AREA_2'))
    now = datetime.datetime.now()
    GPIO.output(13, GPIO.LOW)
    while self.__isnt_stop_requested() and ((datetime.datetime.now() - now).seconds < time_area_2):
      self.toggle_led()
    GPIO.output(13, GPIO.HIGH)

    env['IS_WATERING'] = 'False'
    print("Water IS_WATERING = False")
    print("WATERER::stop watering!")

class WatererLocal:
  def __init__(self, file_manager):
    self.file_manager = file_manager
    print("WATERER::initializing local instance...")

  def is_button_pressed(self):
    return False

  def water(self, source):
    env['IS_WATERING'] = 'True'
    self.file_manager.write(source)
    print("WATERER::(local) triggered via " + source)
    print("WATERER::(local) start watering area 1...")
    time_area_1 = int(env.get('TIME_AREA_1'))
    now = datetime.datetime.now()
    while ((datetime.datetime.now() - now).seconds < time_area_1):
      print(".", end="", flush=True)
      time.sleep(1)

    print("\nWATERER::(local) stop area 1 and start watering area 2...")
    time_area_2 = int(env.get('TIME_AREA_2'))
    now = datetime.datetime.now()
    while ((datetime.datetime.now() - now).seconds < time_area_2):
      print(".", end="", flush=True)
      time.sleep(1)
      
    env['IS_WATERING'] = 'False'
    print("\nWATERER::(local) stop watering!")
    
  def toggle_led(self):
    print("WATERER::(local) toggle led")
    
  def shutdown(self):
    print("WATERER::(local) goodbye!")
