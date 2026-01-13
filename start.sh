#!/bin/bash

echo "========================================================================"
echo "Starting Watering system..."
echo "========================================================================"

if [[ $1 == "-d" ]]; then # start as deamon
  echo "Starting as a deamon process..."
  nohup python src/main.py > /dev/null 2>&1 &
  MAIN_PID=$!

  echo -e "\nStarted! (PID $MAIN_PID)\n"
elif [[ $1 == "-v" ]]; then # start as debug mode ON
  FLASK_DEBUG=1 python src/main.py
else
  python src/main.py
fi
