try:
  import RPi.GPIO as GPIO
except ImportError:
  pass
import time
import datetime
from os import environ as env

class Waterer:
  BUTTON = 3
  STATUS_LED = 11
  RELE_1 = 7
  RELE_2 = 13
  
  def __init__(self, file_manager):
    self.file_manager = file_manager

    # pinout setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Waterer.BUTTON, GPIO.IN)
    GPIO.setup(Waterer.STATUS_LED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(Waterer.RELE_1, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(Waterer.RELE_2, GPIO.OUT, initial=GPIO.HIGH)

    print("WATERER::initializing...")
    GPIO.output(Waterer.RELE_1, GPIO.HIGH)
    GPIO.output(Waterer.RELE_2, GPIO.HIGH)
    now = datetime.datetime.now()
    while (datetime.datetime.now() - now).seconds < 3:
      self.toggle_led()
    print("WATERER::ready!")

  def toggle_led(self):
    GPIO.output(Waterer.STATUS_LED, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(Waterer.STATUS_LED, GPIO.LOW)
    time.sleep(0.5)

  def shutdown(self):
    GPIO.cleanup()
    print("WATERER::goodbye!")

  def is_button_pressed(self):
    return (GPIO.input(Waterer.BUTTON) == 0)

  def __isnt_stop_requested(self):
    return (env.get('IS_WATERING') == 'True')

  def water(self, source):
    env['IS_WATERING'] = 'True'
    print("Water IS_WATERING = True")
    self.file_manager.write_log(source)
    print("WATERER::triggered via " + source)
    print("WATERER::start watering area 1...")
    time_area_1 = int(env.get('TIME_AREA_1'))
    now = datetime.datetime.now()
    GPIO.output(Waterer.RELE_1, GPIO.LOW)
    while self.__isnt_stop_requested() and ((datetime.datetime.now() - now).seconds < time_area_1):
      self.toggle_led()
    GPIO.output(Waterer.RELE_1, GPIO.HIGH)

    print("WATERER::stop area 1 and start watering area 2...")
    time_area_2 = int(env.get('TIME_AREA_2'))
    now = datetime.datetime.now()
    GPIO.output(Waterer.RELE_2, GPIO.LOW)
    while self.__isnt_stop_requested() and ((datetime.datetime.now() - now).seconds < time_area_2):
      self.toggle_led()
    GPIO.output(Waterer.RELE_2, GPIO.HIGH)

    env['IS_WATERING'] = 'False'
    print("Water IS_WATERING = False")
    print("WATERER::stop watering!")

class WatererLocal:
  def __init__(self, file_manager):
    self.file_manager = file_manager
    print("WATERER::initializing local instance...")

  def is_button_pressed(self):
    return False

  def __isnt_stop_requested(self):
    return (env.get('IS_WATERING') == 'True')

  def water(self, source):
    env['IS_WATERING'] = 'True'
    self.file_manager.write_log(source)
    print("WATERER::(local) triggered via " + source)
    print("WATERER::(local) start watering area 1...")
    time_area_1 = int(env.get('TIME_AREA_1'))
    now = datetime.datetime.now()
    while self.__isnt_stop_requested() and ((datetime.datetime.now() - now).seconds < time_area_1):
      print(".", end="", flush=True)
      time.sleep(1)

    print("\nWATERER::(local) stop area 1 and start watering area 2...")
    time_area_2 = int(env.get('TIME_AREA_2'))
    now = datetime.datetime.now()
    while self.__isnt_stop_requested() and ((datetime.datetime.now() - now).seconds < time_area_2):
      print(".", end="", flush=True)
      time.sleep(1)
      
    env['IS_WATERING'] = 'False'
    print("\nWATERER::(local) stop watering!")
    
  def toggle_led(self):
    print("WATERER::(local) toggle led")
    
  def shutdown(self):
    print("WATERER::(local) goodbye!")
