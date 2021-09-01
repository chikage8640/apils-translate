@echo off
set current_dir=%~dp0
bitsadmin /transfer model_download "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin" %current_dir%lid.176.bin
bitsadmin /transfer runtime_download "https://www.python.org/ftp/python/3.9.7/python-3.9.7-embed-amd64.zip" %current_dir%python.zip
call powershell -command "Expand-Archive -Path %current_dir%python.zip -DestinationPath %current_dir%runtime"
del %current_dir%\python.zip
bitsadmin /transfer getpyp_download "https://bootstrap.pypa.io/get-pip.py" %current_dir%runtime\get-pip.py
cd %current_dir%\runtime
(echo import site) >> python39._pth
python get-pip.py
del get-pip.py
SET INCLUDE=%LOCALAPPDATA%\Programs\Python\Python39\include;%INCLUDE%
SET LIB=%LOCALAPPDATA%\Programs\Python\Python39\libs;%LIB%
python -m pip install -r %current_dir%requirements.txt
pause