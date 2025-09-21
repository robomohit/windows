@echo off
title GameBoost Pro - Windows System Monitor and Gaming Optimizer
color 0A

echo.
echo ========================================================================
echo                   GAMEBOOT PRO - GAMING OPTIMIZER                      
echo                      Windows System Monitor                             
echo ========================================================================
echo.
echo    ^>^> Real Windows API Implementation ^<^<
echo    ^>^> 100%% Functional Gaming Optimization ^<^<
echo    ^>^> No Mocks - Real System Modifications ^<^<
echo.
echo ========================================================================
echo.

:: Check if running as Administrator
net session >nul 2>&1
if errorlevel 1 (
    echo [91m[CRITICAL][0m Administrator privileges required for full functionality!
    echo.
    echo [93mGameBoost Pro needs Administrator access to:[0m
    echo   ^> Modify process priorities and CPU affinity
    echo   ^> Apply registry optimizations for gaming
    echo   ^> Optimize network settings and DNS
    echo   ^> Stop/start Windows services
    echo   ^> Access Windows performance counters
    echo   ^> Apply power management settings
    echo.
    echo [96mTo run as Administrator:[0m
    echo   1. Right-click on this file
    echo   2. Select "Run as administrator"
    echo.
    set /p continue="Continue without admin privileges? (Some features disabled) [y/N]: "
    if /i not "!continue!"=="y" (
        echo.
        echo [91mExiting... Please run as Administrator for full functionality.[0m
        pause
        exit /b 1
    )
    echo.
    echo [93mWARNING: Running with limited functionality![0m
    echo.
)

:: Check Python installation
echo [96m[INFO][0m Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [91m[ERROR][0m Python is not installed or not in PATH!
    echo.
    echo [93mGameBoost Pro requires Python 3.8 or later.[0m
    echo Please install Python from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [92m[OK][0m Python %PYTHON_VERSION% detected

:: Check if we're in the correct directory
if not exist "main.py" (
    echo [91m[ERROR][0m main.py not found in current directory!
    echo Please ensure you're running this from the GameBoost Pro directory.
    echo.
    pause
    exit /b 1
)

if not exist "launcher.py" (
    echo [91m[ERROR][0m launcher.py not found in current directory!
    echo Please ensure you're running this from the GameBoost Pro directory.
    echo.
    pause
    exit /b 1
)

echo [92m[OK][0m GameBoost Pro files detected

:: Display system information
echo.
echo [96m[SYSTEM INFO][0m
echo [96m===============[0m
for /f "tokens=2*" %%i in ('reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v ProductName 2^>nul') do echo OS: %%j
for /f "tokens=2*" %%i in ('wmic cpu get name /value ^| find "="') do echo CPU: %%j
for /f "tokens=2*" %%i in ('wmic computersystem get TotalPhysicalMemory /value ^| find "="') do (
    set /a RAM_GB=%%j/1024/1024/1024
    echo RAM: !RAM_GB! GB
)
echo Computer: %COMPUTERNAME%
echo User: %USERNAME%
echo.

:: Check Windows version compatibility
for /f "tokens=3" %%i in ('reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v CurrentBuild 2^>nul') do set BUILD=%%i
if %BUILD% LSS 19041 (
    echo [93m[WARNING][0m Windows build %BUILD% detected.
    echo GameBoost Pro is optimized for Windows 10 version 2004 ^(build 19041^) or later.
    echo Some features may not work properly on older versions.
    echo.
)

:: Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

echo [96m[INFO][0m Starting GameBoost Pro launcher...
echo [96m[INFO][0m The launcher will automatically install missing dependencies.
echo.

:: Log startup information
echo %date% %time% - GameBoost Pro startup initiated >> logs\startup.log
echo %date% %time% - Python version: %PYTHON_VERSION% >> logs\startup.log
echo %date% %time% - Windows build: %BUILD% >> logs\startup.log
echo %date% %time% - User: %USERNAME% on %COMPUTERNAME% >> logs\startup.log

:: Run the launcher
python launcher.py

:: Check exit code
if errorlevel 1 (
    echo.
    echo [91m[ERROR][0m GameBoost Pro exited with error code %errorlevel%
    echo.
    echo [96mTroubleshooting steps:[0m
    echo 1. Ensure you have Administrator privileges
    echo 2. Check that all files are present
    echo 3. Verify Python installation
    echo 4. Check antivirus isn't blocking the application
    echo 5. Review logs\startup.log for details
    echo.
    echo %date% %time% - GameBoost Pro exited with error %errorlevel% >> logs\startup.log
    pause
    exit /b %errorlevel%
) else (
    echo.
    echo [92m[SUCCESS][0m GameBoost Pro completed successfully!
    echo %date% %time% - GameBoost Pro completed successfully >> logs\startup.log
)

echo.
echo [96mThank you for using GameBoost Pro![0m
echo For support, visit: https://github.com/gameboostpro/gameboostpro
echo.
pause