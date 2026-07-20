[CmdletBinding()]
param(
  [ValidateSet('eval','test','server-start','server-stop','server-health')][string]$Command = 'eval',
  [string]$InputPath,
  [string]$OutputPath = 'air-policy-result.json',
  [string]$OpaPath = 'opa',
  [string]$PolicyPath = (Join-Path $PSScriptRoot '..\..\deterministic\AIR DETERMINISTIC POLICY PACK.rego'),
  [string]$TestPath = (Join-Path $PSScriptRoot '..\..\deterministic\AIR DETERMINISTIC POLICY PACK TESTS.rego'),
  [string]$Address = '127.0.0.1:8181'
)
$ErrorActionPreference = 'Stop'
$AdapterId = 'AIR_LOCAL_OPA_POLICY_ADAPTER_V1'
$AdapterVersion = '1.0.0'
function Assert-Loopback([string]$Value) {
  if ($Value -notin @('127.0.0.1:8181','localhost:8181','[::1]:8181')) { throw 'NON_LOOPBACK_ENDPOINT: WS5.1 permits loopback only.' }
}
function Get-OpaVersion { (& $OpaPath version --format json | ConvertFrom-Json).version }
function Invoke-AirEval {
  if (-not $InputPath) { throw 'InputPath is required for eval.' }
  $inputFull=(Resolve-Path $InputPath).Path; $policyFull=(Resolve-Path $PolicyPath).Path
  $inputDigest=(Get-FileHash -Algorithm SHA256 $inputFull).Hash.ToLowerInvariant()
  $policyDigest=(Get-FileHash -Algorithm SHA256 $policyFull).Hash.ToLowerInvariant()
  $version=Get-OpaVersion; $timestamp=(Get-Date).ToUniversalTime().ToString('o')
  $raw=& $OpaPath eval --strict --format=json --data $policyFull --input $inputFull 'data.air.deterministic_policy.decision'
  if ($LASTEXITCODE -ne 0) { throw 'EVALUATION_ERROR: opa eval failed.' }
  $parsed=$raw | ConvertFrom-Json
  if (-not $parsed.result -or $parsed.result.Count -eq 0) { throw 'UNDEFINED_RESULT: no OPA result.' }
  $decision=$parsed.result[0].expressions[0].value
  $decision.policy_digest=$policyDigest; $decision.input_digest=$inputDigest
  $decision.mode='TOOL_EVALUATED'; $decision.tool_evaluated=$true
  $decision | Add-Member -NotePropertyName engine -NotePropertyValue ([ordered]@{name='OPA';version=$version;invocation='LOCAL_CLI';evaluated_at_utc=$timestamp}) -Force
  $decision | Add-Member -NotePropertyName adapter -NotePropertyValue ([ordered]@{id=$AdapterId;version=$AdapterVersion}) -Force
  $decision | Add-Member -NotePropertyName raw_result -NotePropertyValue $parsed -Force
  $decision | ConvertTo-Json -Depth 30 | Set-Content -Encoding UTF8 $OutputPath
  Write-Output $OutputPath
}
switch ($Command) {
  'eval' { Invoke-AirEval }
  'test' { & $OpaPath test --fail-on-empty --format=json --coverage $PolicyPath $TestPath; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE } }
  'server-start' { Assert-Loopback $Address; & $OpaPath run --server --addr $Address $PolicyPath }
  'server-stop' { Write-Error 'Start the local server in its own terminal and stop it with Ctrl+C. No persistent service is installed.' }
  'server-health' { Assert-Loopback $Address; Invoke-RestMethod -Uri ("http://$Address/health?bundles") -Method Get }
}
