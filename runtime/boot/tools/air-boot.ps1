param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& python (Join-Path $ScriptDir "air-boot.py") @Args
exit $LASTEXITCODE
