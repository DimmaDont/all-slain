@echo off

echo setting up...
python -m venv %~dp0\venv --upgrade-deps >NUL 2>NUL

echo downloading and installing dependencies...
%~dp0\venv\Scripts\python.exe -m pip install -U -e %~dp0[app] >NUL 2>NUL

%~dp0\venv\Scripts\python.exe %~dp0\main.py %*

exit /b
