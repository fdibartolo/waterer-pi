import RPi.GPIO as GPIO
import time
import datetime

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

def water(source):
  print("WATERER::triggered via " + source)
  print("WATERER::start watering area 1...")
  now = datetime.datetime.now()
  GPIO.output(7, GPIO.LOW)
  while (datetime.datetime.now() - now).seconds < 5:
    toggle_led()
  GPIO.output(7, GPIO.HIGH)

  print("WATERER::stop area 1 and start watering area 2...")
  now = datetime.datetime.now()
  GPIO.output(13, GPIO.LOW)
  while (datetime.datetime.now() - now).seconds < 10:
    toggle_led()
  GPIO.output(13, GPIO.HIGH)

  print("WATERER::stop watering!")

