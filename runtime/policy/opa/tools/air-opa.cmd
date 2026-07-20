@echo off
setlocal
where pwsh >nul 2>nul
if %errorlevel%==0 (
  pwsh -NoProfile -File "%~dp0air-opa.ps1" %*
  exit /b %errorlevel%
)
where powershell >nul 2>nul
if %errorlevel%==0 (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0air-opa.ps1" %*
  exit /b %errorlevel%
)
echo No supported PowerShell executable was found. Use the direct OPA CLI path or Git Bash/WSL with air-opa.sh. 1>&2
exit /b 3
