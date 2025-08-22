@echo off
REM ErlViz GUI Launcher Script for Windows
REM This script activates the virtual environment and starts the ErlViz GUI
REM
REM Copyright (c) 2025 David Leon (leondavi)
REM Licensed under the MIT License - see LICENSE file for details.

setlocal enabledelayedexpansion

echo ============================================================
echo                     ErlViz GUI Launcher                    
echo ============================================================

REM Get the directory of this script
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if virtual environment exists
if not exist "venv" (
    echo Error: Virtual environment not found!
    echo Please run the setup script first:
    echo   python setup.py
    pause
    exit /b 1
)

REM Check if virtual environment activation script exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment activation script not found!
    echo Please recreate the virtual environment:
    echo   python setup.py
    pause
    exit /b 1
)

echo ✓ Virtual environment found

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if ErlViz is properly installed
python -c "import erlviz" >nul 2>&1
if errorlevel 1 (
    echo Error: ErlViz not properly installed!
    echo Please run the setup script:
    echo   python setup.py
    pause
    exit /b 1
)

echo ✓ ErlViz installation verified

REM Check for system dependencies
echo Checking system dependencies...

REM Check for Graphviz
where dot >nul 2>&1
if errorlevel 1 (
    echo Warning: Graphviz 'dot' command not found in PATH
    echo Graph generation may not work properly.
    echo To install Graphviz:
    echo   1. Download from: https://graphviz.org/download/
    echo   2. Install and add to PATH
    echo   3. Or use: choco install graphviz (if you have Chocolatey)
    echo   4. Or use: winget install graphviz (Windows 10/11)
    echo.
) else (
    for /f "tokens=*" %%i in ('dot -V 2^>^&1') do echo ✓ Graphviz found: %%i
)

REM Launch ErlViz GUI
echo Starting ErlViz GUI...
echo Note: The GUI window may take a few seconds to appear.
echo To close ErlViz, use Ctrl+C in this terminal or close the GUI window.
echo.

REM Start the GUI
python main.py

echo ErlViz GUI closed.
pause
