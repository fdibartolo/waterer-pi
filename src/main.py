from flask import Flask, jsonify, render_template, redirect, request
from os import environ
import datetime
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
  lines = file_manager.read()
  now = datetime.datetime.now()
  templateData = { 'status' : 'Online', 'log' : lines, 'server_datetime' : now.strftime('%b %d, %H:%Mhs') }
  if environ.get('AUTO_ENABLED') == 'True':
    templateData.update({'auto' : True, 'time' : environ.get('HOUR') + ':' + environ.get('MINUTE'), 'button_text' : 'Turn Off'})
  else:
    templateData.update({'auto' : False, 'button_text' : 'Turn On'})

  templateData.update({'is_watering' : environ.get('IS_WATERING') == 'True' })
  templateData.update({'time_area_1' : environ.get('TIME_AREA_1'), 'time_area_2' : environ.get('TIME_AREA_2')})

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

@app.route('/stop')
def stop_watering():
  environ['IS_WATERING'] = 'False'
  print("Stop IS_WATERING = False")
  return redirect('/', code=302)

@app.route('/toggle_auto')
def toggle_auto():
  if environ.get('AUTO_ENABLED') == 'True':
    environ['AUTO_ENABLED'] = 'False'
  else:
    environ['AUTO_ENABLED'] = 'True'
  return redirect('/', code=302)

@app.route('/set_areas_time', methods=['POST'])
def set_areas_time():
  print('setting area 1 watering time to ' + str(request.form['timeArea1']) + ' seconds')
  print('setting area 2 watering time to ' + str(request.form['timeArea2']) + ' seconds')
  environ['TIME_AREA_1'] = request.form['timeArea1']
  environ['TIME_AREA_2'] = request.form['timeArea2']
  return redirect('/', code=302)

# Shut down the scheduler & gpio when exiting the app
atexit.register(lambda: scheduler.shutdown())
atexit.register(lambda: waterer.shutdown())

if __name__ == '__main__':
  waterer.setup()
  waterer.init()
  scheduler = BackgroundScheduler()
  scheduler.add_job(schedule, 'interval', seconds=1)

  environ['IS_WATERING'] = 'False'
  print("Init IS_WATERING = False")

  if environ.get('AUTO_ENABLED') == 'True':
    hh = environ.get('HOUR')
    mm = environ.get('MINUTE')
    print('setting scheduler for automatic watering to ' + hh + ':' + mm + 'hs (UTC)')
    scheduler.add_job(auto_water, 'cron', day_of_week='mon-sun', hour=int(hh), minute=int(mm))

  scheduler.start()
  app.run(host='0.0.0.0', port=80)
