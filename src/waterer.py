import RPi.GPIO as GPIO
import time
import datetime

def setup():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(3, GPIO.IN) # button
  GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW) # led

def init():
  print("WATERER::initializing...")
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
  not GPIO.input(3)