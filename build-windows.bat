@echo off
setlocal
cd /d "%~dp0"
set "CALCULATOR_PYTHON="
call :detect_python "py -3"
if not defined CALCULATOR_PYTHON call :detect_python "python"
if not defined CALCULATOR_PYTHON call :detect_python "python3"
if not defined CALCULATOR_PYTHON goto missing_python
echo Using Python: %CALCULATOR_PYTHON%
%CALCULATOR_PYTHON% -m venv .venv
if errorlevel 1 goto failure
.venv\Scripts\python.exe -c "import tkinter"
if errorlevel 1 goto missing_tk
.venv\Scripts\python.exe -m pip install pyinstaller==6.20.0
if errorlevel 1 goto failure
.venv\Scripts\python.exe -m unittest discover -s tests -v
if errorlevel 1 goto failure
.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm --onefile --windowed --name Calculator desktop.py
if errorlevel 1 goto failure
echo Created: %cd%\dist\Calculator.exe
if not defined CALCULATOR_BUILD_CI pause
exit /b 0
:detect_python
if defined CALCULATOR_PYTHON exit /b 0
%~1 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 exit /b 0
set "CALCULATOR_PYTHON=%~1"
exit /b 0
:missing_python
echo No usable Python 3.10+ was found via py, python, or python3.
echo Install Python from https://www.python.org/downloads/windows/
echo Enable "Add python.exe to PATH" and include Tcl/Tk during installation.
echo Then reopen this script. Python Launcher is optional.
goto failure
:missing_tk
echo Tcl/Tk is missing. Modify or reinstall Python with Tcl/Tk enabled.
goto failure
:failure
echo Build failed. See the error above.
if not defined CALCULATOR_BUILD_CI pause
exit /b 1
