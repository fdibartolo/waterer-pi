from flask import Flask, jsonify, render_template, redirect, request
import io
from os import environ as env
import datetime
import atexit
from waterer import Waterer, WatererLocal
from water_tank import WaterTank, WaterTankLocal
from file_manager import FileManager
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)

is_web_triggered = False

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

@app.route('/tank')
def tank():
  templateData = {
    'server_datetime' : datetime.datetime.now().strftime('%b %d, %H:%Mhs'),
    'is_filling' : False,
    'is_measuring' : env.get('IS_MEASURING') == 'True',
    'auto' : True,
    'time' : 60
  }
  return render_template('water_tank.html', **templateData)

@app.route('/measure_tank')
def measure_tank():
  if env.get('IS_MEASURING') == 'True':
    env['IS_MEASURING'] = 'False'
  else:
    env['TANK_LEVEL'] = "13"
    env['IS_MEASURING'] = 'True'
  return redirect('/tank', code=302)

@app.route('/get_tank_level')
def get_tank_level():
  if env.get('IS_MEASURING') == 'True':
    env['TANK_LEVEL'] = str(water_tank.measure_distance())
  return jsonify({'tank_level' : env.get('TANK_LEVEL')})

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
  env['IS_WATERING'] = 'True'
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
  print(f"Area 1 watering time set to {request.form['timeArea1']} seconds")
  print(f"Area 2 watering time set to {request.form['timeArea2']} seconds")
  env['TIME_AREA_1'] = request.form['timeArea1']
  env['TIME_AREA_2'] = request.form['timeArea2']
  return redirect('/', code=302)

@app.route('/set_water_schedule', methods=['POST'])
def set_water_schedule():
  env['HOUR'], env['MINUTE'] = request.form['schedule'].split(':')
  set_auto_water_scheduler()
  return redirect('/', code=302)

def schedule():
  global is_web_triggered
  if waterer.is_button_pressed():
    waterer.water('BUTTON')
  elif is_web_triggered:
    is_web_triggered = False
    waterer.water('WEB')

def auto_water():
  waterer.water('AUTO')

def init_env_vars_from(config):
  env['IS_WATERING'] = 'False'
  env['AUTO_ENABLED'] = config.get('auto_enabled', 'False')
  env['HOUR'] = config.get('scheduled_hour', '00')
  env['MINUTE'] = config.get('scheduled_minute', '00')
  env['TIME_AREA_1'] = config.get('time_area_1', '0')
  env['TIME_AREA_2'] = config.get('time_area_2', '0')
  env['IS_MEASURING'] = 'False'

def set_auto_water_scheduler():
  if scheduler.get_job('auto_water_job'):
    scheduler.remove_job('auto_water_job')
  print(f"Automatic watering scheduled to {env.get('HOUR')}:{env.get('MINUTE')} hs")
  scheduler.add_job(auto_water, 'cron', day_of_week='mon-sun', hour=int(env.get('HOUR')), minute=int(env.get('MINUTE')), id='auto_water_job')

def is_raspberrypi():
  try:
    with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
      if 'raspberry pi' in m.read().lower():
        return True
  except Exception:
    pass
  return False

def is_main_process():
  return not app.debug or env.get("WERKZEUG_RUN_MAIN") == "true"

# Shut down the scheduler & gpio when exiting the app (only from the main process to avoid multiple registrations in debug mode)
if is_main_process():
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
  water_tank = WaterTank() if is_raspberrypi() else WaterTankLocal()
  scheduler = BackgroundScheduler({'apscheduler.timezone': 'America/Argentina/Buenos_Aires'})
  scheduler.add_job(schedule, 'interval', seconds=1)

  config = file_manager.load_config()
  init_env_vars_from(config)

  if env.get('AUTO_ENABLED') == 'True':
    set_auto_water_scheduler()

  scheduler.start()
  app.run(host='0.0.0.0')
