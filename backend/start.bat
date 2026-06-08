@echo off
echo ========================================
echo  Property Management System - Backend
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    venv\Scripts\pip install -r requirements.txt
)

echo Starting backend server...
venv\Scripts\python run.py
pause
