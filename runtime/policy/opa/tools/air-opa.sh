#!/usr/bin/env bash
set -euo pipefail
command_name="${1:-eval}"; shift || true
OPA_BIN="${OPA_BIN:-opa}"
OPA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
POLICY="${AIR_OPA_POLICY:-$OPA_DIR/../deterministic/AIR DETERMINISTIC POLICY PACK.rego}"
TESTS="${AIR_OPA_TESTS:-$OPA_DIR/../deterministic/AIR DETERMINISTIC POLICY PACK TESTS.rego}"
ADDRESS="${AIR_OPA_ADDRESS:-127.0.0.1:8181}"
assert_loopback() { case "$1" in 127.0.0.1:8181|localhost:8181|'[::1]:8181') ;; *) echo 'NON_LOOPBACK_ENDPOINT: WS5.1 permits loopback only.' >&2; exit 4;; esac; }
hash_file() { if command -v sha256sum >/dev/null; then sha256sum "$1"|awk '{print $1}'; elif command -v shasum >/dev/null; then shasum -a 256 "$1"|awk '{print $1}'; elif command -v openssl >/dev/null; then openssl dgst -sha256 "$1"|awk '{print $NF}'; else echo 'No SHA-256 tool found.' >&2; exit 5; fi; }
case "$command_name" in
 eval)
  input="${1:?input JSON path required}"; output="${2:-air-policy-result.json}"
  command -v "$OPA_BIN" >/dev/null || { echo 'ENGINE_UNAVAILABLE: OPA not found.' >&2; exit 3; }
  raw="$(mktemp)"; trap 'rm -f "$raw"' EXIT
  "$OPA_BIN" eval --strict --format=json --data "$POLICY" --input "$input" 'data.air.deterministic_policy.decision' >"$raw"
  pd="$(hash_file "$POLICY")"; id="$(hash_file "$input")"; ver="$($OPA_BIN version --format json | sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
  if command -v python3 >/dev/null; then
    python3 - "$raw" "$output" "$pd" "$id" "$ver" <<'PY2'
import json,sys,datetime
raw=json.load(open(sys.argv[1])); rows=raw.get('result') or []
if not rows: raise SystemExit('UNDEFINED_RESULT: no OPA result')
d=rows[0]['expressions'][0]['value']; d.update(policy_digest=sys.argv[3],input_digest=sys.argv[4],mode='TOOL_EVALUATED',tool_evaluated=True)
d['engine']={'name':'OPA','version':sys.argv[5],'invocation':'LOCAL_CLI','evaluated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
d['adapter']={'id':'AIR_LOCAL_OPA_POLICY_ADAPTER_V1','version':'1.0.0'}; d['raw_result']=raw
json.dump(d,open(sys.argv[2],'w'),indent=2); open(sys.argv[2],'a').write('\n')
PY2
  elif command -v jq >/dev/null; then
    ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    jq --arg pd "$pd" --arg id "$id" --arg ver "$ver" --arg ts "$ts" '.result[0].expressions[0].value + {policy_digest:$pd,input_digest:$id,mode:"TOOL_EVALUATED",tool_evaluated:true,engine:{name:"OPA",version:$ver,invocation:"LOCAL_CLI",evaluated_at_utc:$ts},adapter:{id:"AIR_LOCAL_OPA_POLICY_ADAPTER_V1",version:"1.0.0"},raw_result:.}' "$raw" >"$output"
  else echo 'Wrapper needs python3 or jq for the canonical result envelope. Direct OPA CLI remains available.' >&2; exit 6; fi
  printf '%s\n' "$output";;
 test) "$OPA_BIN" test --fail-on-empty --format=json --coverage "$POLICY" "$TESTS";;
 server-start) assert_loopback "$ADDRESS"; exec "$OPA_BIN" run --server --addr "$ADDRESS" "$POLICY";;
 server-health) assert_loopback "$ADDRESS"; command -v curl >/dev/null || { echo 'curl required for health check.' >&2; exit 7; }; curl --fail --silent "http://$ADDRESS/health?bundles";;
 server-stop) echo 'Run the server in its own terminal and stop it with Ctrl+C. No persistent service is installed.' >&2; exit 2;;
 *) echo 'Usage: air-opa.sh eval INPUT [OUTPUT] | test | server-start | server-health | server-stop' >&2; exit 2;;
esac
