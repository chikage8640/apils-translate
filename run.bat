@echo off
set current_dir=%~dp0
echo Updating SSL certificate.
%current_dir%runtime\python.exe -m pip install -U certifi
echo Runnning Program.py
%current_dir%runtime\python.exe %current_dir%program.py
pause