# AI Agent Incident Case Study Plan

## Status

Deferred evidence track. It is not a Stage 3 implementation gate.

A July 2026 commentary video described reports of coding agents deleting files or databases, interpreting instructions too permissively, circumventing restrictions, taking destructive actions beyond task scope, and reporting results deceptively. Those claims must be traced to primary sources before AIR uses them publicly.

## Evidence method

For each incident:

1. Record the exact claim and timestamp from the commentary source.
2. Locate the original post, issue, system card, repository evidence, or vendor statement.
3. Separate confirmed facts, quoted claims, interpretation, and unresolved uncertainty.
4. Classify the failure: scope drift, over-permissive interpretation, destructive mutation, missing approval, privilege exposure, false completion, deceptive reporting, lost continuity, or missing recovery evidence.
5. Build a safe fixture that cannot affect real user data or production systems.
6. Run a baseline task and an AIR-controlled task under the same bounded environment.
7. Score the AIR result as `PREVENTED`, `DETECTED`, `CONTAINED`, `RECOVERED`, `ASSISTED`, or `NOT_COVERED`.
8. Publish the claim boundary and all reproduction limitations.

## AIR controls to test

- explicit approved and excluded scope;
- capability-specific default-deny authorization;
- current-step and continuation preservation;
- separate mutation, push, merge, release, publication, and destructive-action gates;
- evidence requirements before completion claims;
- deterministic boot and task packet transfer across tools;
- workspace isolation and rollback evidence;
- visible blockers and unknown-trigger fallback;
- no inference that host privileges are safe merely because they are available.

## Reproducible case pack

```text
case-studies/<incident>/
├── README.md
├── SOURCE_RECORD.json
├── BASELINE_TASK.md
├── AIR_TASK_PACKET.json
├── AIR_AUTHORIZATION_ENVELOPE.json
├── AIR_CONTINUATION_PACKET.json
├── fixture/
├── expected/
├── runs/baseline/
├── runs/air-controlled/
├── VERIFY.ps1
├── VERIFY.sh
└── CLAIM_BOUNDARY.md
```

The GitHub case pack is the evidence source. A vm4ai.com article and an X thread should summarize and link to it rather than replacing it.
