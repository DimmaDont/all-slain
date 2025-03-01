@echo off

echo setting up...
python -m venv venv --upgrade-deps >NUL 2>NUL

echo downloading and installing dependencies...
venv\Scripts\python.exe -m pip install -U -r requirements.txt >NUL 2>NUL

venv\Scripts\python.exe allslain.py %*

exit /b
