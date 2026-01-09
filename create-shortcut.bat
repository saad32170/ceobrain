@echo off
echo Creating desktop shortcut for CEO Personal OS...
powershell.exe -ExecutionPolicy Bypass -File "%~dp0create-shortcut.ps1"
pause
