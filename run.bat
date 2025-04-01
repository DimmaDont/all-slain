@echo off

echo setting up...
python -m venv %~dp0\venv --upgrade-deps >NUL 2>NUL

echo downloading and installing dependencies...
%~dp0\venv\Scripts\python.exe -m pip install -U -r %~dp0\requirements.txt >NUL 2>NUL

%~dp0\venv\Scripts\python.exe %~dp0\allslain.py %*

exit /b
