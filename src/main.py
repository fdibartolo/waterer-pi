from flask import Flask, jsonify, render_template, redirect, request
import io
from os import environ as env
import datetime
import atexit
from waterer import Waterer, WatererLocal
from file_manager import FileManager
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
  templateData = {
    'log' : file_manager.read_log(),
    'server_datetime' : datetime.datetime.now().strftime('%b %d, %H:%Mhs'),
    'is_watering' : env.get('IS_WATERING') == 'True',
    'auto' : env.get('AUTO_ENABLED') == 'True',
    'time' : f"{env.get('HOUR')}:{env.get('MINUTE')}",
    'time_area_1' : env.get('TIME_AREA_1'),
    'time_area_2' : env.get('TIME_AREA_2')
  }
  return render_template('home.html', **templateData)

@app.route('/healthcheck')
def health_check():
  waterer.toggle_led()
  return redirect('/', code=302)

@app.route('/get_datetime')
def get_datetime():
  return jsonify({'server_datetime' : datetime.datetime.now().strftime('%b %d, %H:%Mhs')})

@app.route('/water')
def water():
  global is_web_triggered
  is_web_triggered = True
  return redirect('/', code=302)

@app.route('/stop')
def stop_watering():
  env['IS_WATERING'] = 'False'
  print("Stop IS_WATERING = False")
  return redirect('/', code=302)

@app.route('/toggle_auto')
def toggle_auto():
  if env.get('AUTO_ENABLED') == 'True':
    env['AUTO_ENABLED'] = 'False'
    scheduler.remove_job('auto_water_job')
  else:
    env['AUTO_ENABLED'] = 'True'
    set_auto_water_scheduler()
  return redirect('/', code=302)

@app.route('/set_areas_time', methods=['POST'])
def set_areas_time():
  print('setting area 1 watering time to ' + str(request.form['timeArea1']) + ' seconds')
  print('setting area 2 watering time to ' + str(request.form['timeArea2']) + ' seconds')
  env['TIME_AREA_1'] = request.form['timeArea1']
  env['TIME_AREA_2'] = request.form['timeArea2']
  return redirect('/', code=302)

@app.route('/set_water_schedule', methods=['POST'])
def set_water_schedule():
  env['HOUR'], env['MINUTE'] = request.form['schedule'].split(':')
  set_auto_water_scheduler()
  return redirect('/', code=302)

def is_raspberrypi():
  try:
    with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
      if 'raspberry pi' in m.read().lower():
        return True
  except Exception:
    pass
  return False

def init_env_vars_from(config):
  env['IS_WATERING'] = 'False'
  env['AUTO_ENABLED'] = config.get('auto_enabled', 'False')
  env['HOUR'] = config.get('scheduled_hour', '00')
  env['MINUTE'] = config.get('scheduled_minute', '00')
  env['TIME_AREA_1'] = config.get('time_area_1', '0')
  env['TIME_AREA_2'] = config.get('time_area_2', '0')

def set_auto_water_scheduler():
  if scheduler.get_job('auto_water_job'):
    scheduler.remove_job('auto_water_job')
  print(f"setting scheduler for automatic watering to {env.get('HOUR')}:{env.get('MINUTE')} hs")
  scheduler.add_job(auto_water, 'cron', day_of_week='mon-sun', hour=int(env.get('HOUR')), minute=int(env.get('MINUTE')), id='auto_water_job')

# Shut down the scheduler & gpio when exiting the app
atexit.register(lambda: scheduler.shutdown())
atexit.register(lambda: file_manager.save_config({
  'auto_enabled': env.get('AUTO_ENABLED'),
  'scheduled_hour': env.get('HOUR'),
  'scheduled_minute': env.get('MINUTE'),
  'time_area_1': env.get('TIME_AREA_1'),
  'time_area_2': env.get('TIME_AREA_2')
}))
atexit.register(lambda: waterer.shutdown())

if __name__ == '__main__':
  file_manager = FileManager(log_file='./last_run.txt', config_file='./config.json')
  waterer = Waterer(file_manager) if is_raspberrypi() else WatererLocal(file_manager)
  scheduler = BackgroundScheduler({'apscheduler.timezone': 'America/Argentina/Buenos_Aires'})
  scheduler.add_job(schedule, 'interval', seconds=1)

  config = file_manager.load_config()
  init_env_vars_from(config)

  if env.get('AUTO_ENABLED') == 'True':
    set_auto_water_scheduler()

  scheduler.start()
  app.run(host='0.0.0.0', port=80)
