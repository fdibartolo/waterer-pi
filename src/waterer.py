import RPi.GPIO as GPIO
import time
import datetime
import file_manager
from os import environ
from apscheduler.schedulers.background import BackgroundScheduler

def setup():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(3, GPIO.IN) # button
  GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW) # led
  GPIO.setup(7, GPIO.OUT, initial=GPIO.HIGH) # rele 1
  GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH) # rele 2

def init():
  print("WATERER::initializing...")
  GPIO.output(7, GPIO.HIGH)
  GPIO.output(13, GPIO.HIGH)
  now = datetime.datetime.now()
  while (datetime.datetime.now() - now).seconds < 3:
    toggle_led()
  print("WATERER::ready!")

def toggle_led():
  GPIO.output(11, GPIO.HIGH)
  time.sleep(0.5)
  GPIO.output(11, GPIO.LOW)
  time.sleep(0.5)

def shutdown():
  GPIO.cleanup()
  print("WATERER::goodbye!")

def is_button_pressed():
  return (GPIO.input(3) == 0)

def isnt_stop_requested():
  return (environ.get('IS_WATERING') == 'True')

def water(source):
  apscheduler.schedulers.base.BaseScheduler.pause_job()
  environ['IS_WATERING'] = 'True'
  print("Water IS_WATERING = True")
  file_manager.write(source)
  print("WATERER::triggered via " + source)
  print("WATERER::start watering area 1...")
  time_area_1 = int(environ.get('TIME_AREA_1'))
  now = datetime.datetime.now()
  GPIO.output(7, GPIO.LOW)
  while isnt_stop_requested() and ((datetime.datetime.now() - now).seconds < time_area_1):
    toggle_led()
  GPIO.output(7, GPIO.HIGH)

  print("WATERER::stop area 1 and start watering area 2...")
  time_area_2 = int(environ.get('TIME_AREA_2'))
  now = datetime.datetime.now()
  GPIO.output(13, GPIO.LOW)
  while isnt_stop_requested() and ((datetime.datetime.now() - now).seconds < time_area_2):
    toggle_led()
  GPIO.output(13, GPIO.HIGH)

  environ['IS_WATERING'] = 'False'
  print("Water IS_WATERING = False")
  print("WATERER::stop watering!")
  apscheduler.schedulers.base.BaseScheduler.resume_job()

