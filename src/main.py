from flask import Flask
from os import environ
import time
import atexit
import waterer
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)

def schedule():
  if waterer.button_pressed?:
    print('pressed!')

@app.route('/')
def hello_world():
  waterer.toggle_led()
  p = environ.get('PASS')
  print(p)
  return 'Welcome to Waterer!' + p

# Shut down the scheduler & gpio when exiting the app
atexit.register(lambda: scheduler.shutdown())
atexit.register(lambda: waterer.shutdown())

if __name__ == '__main__':
  waterer.setup()
  waterer.init()
  scheduler = BackgroundScheduler()
  scheduler.add_job(schedule, 'interval', seconds=1)
  scheduler.start()
  app.run(host='0.0.0.0', port=80)
