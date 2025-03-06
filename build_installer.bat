@echo off
echo Building Cornelius installer...

:: Set the path to your PyInstaller executable (if it's not in your system PATH)
set "PYINSTALLER_PATH=venv\Scripts\pyinstaller.exe"  

:: Run PyInstaller
%PYINSTALLER_PATH% --onefile --noconsole --name cornelius cornelius.spec

:: Check for errors
if %errorlevel% neq 0 (
    echo ERROR: PyInstaller failed.
    pause
    exit /b %errorlevel%
)

echo Installer built successfully.  Output is in the 'dist' folder.
pause