@echo off
echo Activating Python 3.12 Virtual Environment...
call venv312\Scripts\activate.bat
echo.
echo Virtual environment activated!
echo Python version: 
python --version
echo.
echo To start the service, run:
echo   python start.py
echo   or
echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo To deactivate, run: deactivate
echo.
cmd /k 