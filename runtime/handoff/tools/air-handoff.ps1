$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Tool = Join-Path $ScriptDir "air-handoff.py"
$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) { $Python = Get-Command py -ErrorAction SilentlyContinue }
if (-not $Python) {
  Write-Error "Python 3.11+ was not found. Prompt-native AIR remains available."
  exit 127
}
if ($Python.Name -eq "py.exe" -or $Python.Name -eq "py") {
  & $Python.Source -3 $Tool @args
} else {
  & $Python.Source $Tool @args
}
exit $LASTEXITCODE
