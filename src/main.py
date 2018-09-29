from flask import Flask, jsonify
from os import environ
import time
import atexit
import waterer
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)

def schedule():
  if waterer.is_button_pressed():
    waterer.water()

@app.route('/')
def hello_world():
  p = environ.get('PASS')
  print(p)
  return 'Welcome to Waterer!' + p

@app.route('/healthcheck')
def health_check():
  waterer.toggle_led()
  return jsonify({'health': 'good!'})

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
