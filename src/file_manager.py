import datetime
import json
import os.path

class FileManager:
  def __init__(self, log_file, config_file):
    self.log_file_path = log_file
    self.config_file_path = config_file
    
    if not os.path.isfile(self.log_file_path):
      open(self.log_file_path, 'w').close()

    if not os.path.isfile(self.config_file_path):
      open(self.config_file_path, 'w').close()

  def write_log(self, source):
    timestamp = datetime.datetime.now()
    line = f"Triggered via {source} on {timestamp.strftime('%b %d')} at {timestamp.strftime('%H:%M')} hs\n"

    f = open(self.log_file_path, 'r')
    lines = f.readlines()
    f.close()

    if len(lines) >= 3:
      lines.pop(len(lines)-1)    

    lines.insert(0, line)
    f = open(self.log_file_path, 'w')
    f.writelines(lines)
    f.close()

  def read_log(self):
    f = open(self.log_file_path, 'r')
    content = f.readlines()
    f.close()
    return content

  def load_config(self):
    with open(self.config_file_path, 'r') as f:
      config = json.load(f)
    return config
  
  def save_config(self, config):
    with open(self.config_file_path, 'w') as f:
      json.dump(config, f, indent=2)
