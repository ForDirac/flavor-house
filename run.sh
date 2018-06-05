killall -9 python
. .venv/bin/activate
git pull
nohup python launcher.py &
echo SERVER GET STARTED
deactivate
