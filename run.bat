@echo off

echo setting up...
python -m venv venv

echo downloading and installing dependencies...
venv\Scripts\python.exe -m pip install -U -r requirements.txt >NUL 2>NUL

venv\Scripts\python.exe allslain.py

pause
