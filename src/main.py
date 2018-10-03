from flask import Flask, jsonify, render_template, redirect
from os import environ
import time
import atexit
import waterer
import file_manager
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)

is_web_triggered = False

def schedule():
  global is_web_triggered
  if waterer.is_button_pressed():
    waterer.water('BUTTON')
  elif is_web_triggered:
    is_web_triggered = False
    waterer.water('WEB')

def auto_water():
  waterer.water('AUTO')

@app.route('/')
def home():
  p = environ.get('PASS')
  print(p)
  lines = file_manager.read()
  templateData = { 'status' : 'Online', 'log' : lines }
  return render_template('home.html', **templateData)

@app.route('/healthcheck')
def health_check():
  waterer.toggle_led()
  return jsonify({'health': 'good!'})

@app.route('/water')
def water():
  global is_web_triggered
  is_web_triggered = True
  return redirect('/', code=302)

# Shut down the scheduler & gpio when exiting the app
atexit.register(lambda: scheduler.shutdown())
atexit.register(lambda: waterer.shutdown())

if __name__ == '__main__':
  waterer.setup()
  waterer.init()
  scheduler = BackgroundScheduler(timezone=art)
  scheduler.add_job(schedule, 'interval', seconds=1)
  scheduler.add_job(auto_water, 'cron', day_of_week='mon-sun', hour=18, minute=30)
  scheduler.start()
  app.run(host='0.0.0.0', port=80)
