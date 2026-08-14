# AIR Runtime Drift Hardening Mainline Review

Generated: 2026-08-04T21:00:00+02:00

## Decision

The uploaded drift-hardening proposal is **accepted with maintainer corrections** and rebased onto the current v2.2.1 mainline.

## Accepted controls

- one-shot material-action authorization
- bootstrap write lock
- artifact lease and invalidation
- exact resource scope pin
- pre-action authorization and post-action receipt pairing
- unbound prior-effect reconciliation without retrospective authorization
- pre-action, post-action, and final-delivery watchdog
- explicit prompt-layer versus gateway-enforcement boundary
- Grounding diagnostics for action/rule decoupling

## Mainline corrections

1. Added `AIR-FLOOR-018` so the interlock cannot be weakened by lower-precedence artifacts.
2. Advanced the Handoff schema to `2.1.0`; the candidate changed the schema while leaving it at `2.0.0`.
3. Preserved the Starter version-consistency fix and set both Starter version fields to `2.2.0`.
4. Resealed Capability Ecology, Grounding, and AI Governance against one final foundation.
5. Expanded the adversarial matrix from 18 to 23 cases.
6. Classified the executed 23-case run as structural policy simulation, not host-model or gateway enforcement evidence.

## Validation

173/173 summary-mode checks passed, including 23/23 deterministic policy scenarios.

## Boundary

This release strengthens prompt-side runtime discipline. It does not guarantee a host model will never skip the interlock. Atomic enforcement still requires a client, connector, MCP, or backend gateway that validates and consumes authorizations with tool calls.
