@echo off
setlocal
cd /d "%~dp0"
title CreatorLedger - Rahul Singh

echo.
echo ==========================================
echo       CreatorLedger - Local Demo
echo          Created by Rahul Singh
echo ==========================================
echo.

where py >nul 2>nul
if errorlevel 1 (
    echo Python Launcher was not found. Install Python 3.10 or newer from python.org.
    echo During installation, enable the Python launcher option.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -m venv .venv
    if errorlevel 1 goto :failed
)

echo Checking/installing dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :failed

echo.
echo Starting CreatorLedger. Keep this window open while using the app.
echo Open http://127.0.0.1:5000 in your browser.
echo This Flask project does not run through VS Code Live Server.
echo Press Ctrl+C to stop the app.
echo.
".venv\Scripts\python.exe" app.py
pause
exit /b 0

:failed
echo.
echo Setup failed. Check that Python is installed and the internet is available for Flask installation.
pause
exit /b 1
