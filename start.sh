#!/bin/bash

echo "========================================================================"
echo "Starting Watering system..."
echo "========================================================================"

if [[ $1 == "-d" ]]; then # start as deamon
  echo "Starting as a deamon process..."
  nohup python src/main.py > /dev/null 2>&1 &
  MAIN_PID=$!

  echo -e "\nStarted! (PID $MAIN_PID)\n"
else
  python src/main.py
fi
