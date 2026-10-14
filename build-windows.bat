@echo off
setlocal
cd /d "%~dp0"
py -3 -m venv .venv
if errorlevel 1 goto failure
.venv\Scripts\python.exe -m pip install pyinstaller==6.20.0
if errorlevel 1 goto failure
.venv\Scripts\python.exe -m unittest discover -s tests -v
if errorlevel 1 goto failure
.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm --onefile --windowed --name Calculator desktop.py
if errorlevel 1 goto failure
echo Created: %cd%\dist\Calculator.exe
pause
exit /b 0
:failure
echo Build failed. See the error above.
pause
exit /b 1
