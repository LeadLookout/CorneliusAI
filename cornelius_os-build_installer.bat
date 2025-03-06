@echo off
echo Building cornelius executable...
pyinstaller cornelius.spec
echo Build completed.
echo Creating cornelius installer...
iscc cornelius_installer.iss
echo installer created.
pause
