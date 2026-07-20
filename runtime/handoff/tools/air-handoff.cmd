@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 "%SCRIPT_DIR%air-handoff.py" %*
  exit /b %ERRORLEVEL%
)
where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python "%SCRIPT_DIR%air-handoff.py" %*
  exit /b %ERRORLEVEL%
)
echo Python 3.11+ was not found. Prompt-native AIR remains available. 1>&2
exit /b 127
