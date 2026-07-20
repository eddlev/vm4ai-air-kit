@echo off
setlocal
python "%~dp0air-boot.py" %*
exit /b %ERRORLEVEL%
