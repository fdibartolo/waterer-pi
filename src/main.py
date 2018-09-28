from flask import Flask
from os import environ
app = Flask(__name__)

@app.route('/')
def hello_world():

  p = environ.get('PASS')
  print(p)
  return 'Welcome to Waterer!' + p

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
