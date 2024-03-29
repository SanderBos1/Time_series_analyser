set delete_vm=%1
set make_vm=%2
set directory=%CD%

cd %directory%

if %delete_vm%==True (
    del /s /q .\venv & rmdir /s /q .\venv 
)

if %make_vm%==True (
    python -m venv venv
)

Call ".\venv\Scripts\activate.bat"
pip.exe install -r ./requirements.txt

del /s /q .\ts_python\__pycache__ & rmdir /s /q .\ts_python\__pycache__ 
del /s /q .\ts_config\__pycache__ & rmdir /s /q .\ts_config\__pycache__ 
del /s /q .\ts_app\__pycache__ & rmdir /s /q .\ts_app\__pycache__ 
del /s /q .\flask_session & rmdir /s /q .\ts_app\flask_session

flask run