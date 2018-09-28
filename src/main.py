from flask import Flask
from os import environ
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)

def schedule():
  print('tick...')

@app.route('/')
def hello_world():

  p = environ.get('PASS')
  print(p)
  return 'Welcome to Waterer!' + p

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
  scheduler = BackgroundScheduler()
  scheduler.add_job(schedule, 'interval', seconds=3)
  scheduler.start()
  app.run(host='0.0.0.0', port=80)
