# Local OPA Policy Adapter

**Paths:** `runtime/policy/opa/tools/`

## Purpose

Evaluate AIR deterministic policy input against the shipped Rego policy using a user-controlled local OPA installation.

## Modes

- Local CLI: no server and no network.
- Local loopback server: only `127.0.0.1`, `localhost`, or `[::1]`.

## Dependencies

OPA is optional and is not downloaded by AIR. The POSIX wrapper also uses Python 3 or jq for the result envelope. Windows wrappers use PowerShell or direct CLI delegation.

## Evidence

The result envelope records engine version, policy digest, input digest, timestamp, adapter version, and raw decision/error.

## Boundary

An OPA result is a local tool-observed policy evaluation. It is not backend AIR enforcement, legal compliance, cryptographic integrity, or release readiness.
