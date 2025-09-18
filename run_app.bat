@echo off
title GameBoost Pro Launcher
echo ==========================================
echo    GameBoost Pro - Gaming Optimizer
echo ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from python.org
    pause
    exit /b 1
)

:: Check if we're running as administrator
net session >nul 2>&1
if errorlevel 1 (
    echo Warning: Not running as Administrator
    echo Some features may not work properly
    echo.
    echo To run as Administrator:
    echo 1. Right-click on this file
    echo 2. Select "Run as administrator"
    echo.
    set /p choice="Continue anyway? (y/n): "
    if /i not "%choice%"=="y" exit /b 1
)

echo Starting GameBoost Pro...
echo.

:: Try to run with launcher first (handles dependencies)
if exist launcher.py (
    python launcher.py
) else if exist main.py (
    python main.py
) else (
    echo Error: Application files not found
    echo Please ensure launcher.py or main.py exists in this directory
    pause
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)