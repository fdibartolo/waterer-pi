import datetime
import os.path

file_path = '/data/last_run.txt'

def write(source):
  timestamp = datetime.datetime.now()
  line = 'Triggered via ' + source + ' on ' + timestamp.strftime('%b %d') + ' at ' + timestamp.strftime('%H:%M') + ' hs\n'

  if not os.path.isfile(file_path):
    open(file_path, 'w').close()

  f = open(file_path, 'r')
  lines = f.readlines()
  f.close()

  if len(lines) >= 3:
    lines.pop(len(lines)-1)    

  lines.insert(0, line)
  f = open(file_path, 'w')
  f.writelines(lines)
  f.close()

def read():
  f = open(file_path, 'r')
  content = f.readlines()
  f.close()
  return content
