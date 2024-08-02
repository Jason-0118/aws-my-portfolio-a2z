#!/bin/bash
echo ">>> display running processes"
ps -A

echo ">>> Dynamic view of processes"
top -b -n 1

echo ">>> Adjust process priority"
nice -n 19 vim &
ps -l

echo ">>> adjust running process priority"
PID=$(pgrep vim)
sudo renice -n 5 -p $PID
ps -l

echo ">>> terminate the vim process just launched"
pkill -9 vim
ps -l
