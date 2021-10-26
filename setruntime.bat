@echo off
SET CDIR=%~dp0
SET INCLUDE=%1\include;%INCLUDE%
SET LIB=%1\libs;%LIB%
SET PYTHON=%CDIR%runtime\python.exe
%PYTHON% %CDIR%temp\get-pip.py
%PYTHON% -m pip install %CDIR%temp\fasttext\fastText-master
%PYTHON% -m pip install -r %CDIR%requirements.txt