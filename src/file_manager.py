import datetime

file_path = '/data/last_run.txt'

def write(source):
  timestamp = datetime.datetime.now()
  f = open(file_path, 'w')
  f.write('Triggered via ' + source + ' on ' + timestamp.strftime('%b %d') + ' at ' + timestamp.strftime('%H:%M') + ' hs')
  f.close()

def read():
  f = open(file_path, 'r')
  content = f.readline()
  f.close()
  return content
