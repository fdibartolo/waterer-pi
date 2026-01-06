import datetime
import os.path

class FileManager:
  def __init__(self, path):
    self.file_path = path
    
    if not os.path.isfile(self.file_path):
      open(self.file_path, 'w').close()

  def write(self, source):
    timestamp = datetime.datetime.now()
    line = 'Triggered via ' + source + ' on ' + timestamp.strftime('%b %d') + ' at ' + timestamp.strftime('%H:%M') + ' hs\n'

    if not os.path.isfile(self.file_path):
      open(self.file_path, 'w').close()

    f = open(self.file_path, 'r')
    lines = f.readlines()
    f.close()

    if len(lines) >= 3:
      lines.pop(len(lines)-1)    

    lines.insert(0, line)
    f = open(self.file_path, 'w')
    f.writelines(lines)
    f.close()

  def read(self):
    f = open(self.file_path, 'r')
    content = f.readlines()
    f.close()
    return content
