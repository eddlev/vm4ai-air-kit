# Local OPA Policy Adapter

## Current status

The wrappers under `runtime/policy/opa/tools/` are repository-relative compatibility surfaces.

They evaluate AIR deterministic policy input against the shipped Rego policy using an operator-controlled OPA installation.

## Modes

- local CLI;
- loopback-only local server.

OPA is optional and is not downloaded by AIR. An OPA result is local tool-observed policy evidence, not backend AIR enforcement, legal compliance, cryptographic integrity, or release approval.

## Stage 5 migration

Stage 5 must move policy resource resolution, inputs, results, evidence, logs, and commands onto the shared package and project-workspace substrate.

The installed Stage 2 CLI does not yet provide `air policy` commands.
