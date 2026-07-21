# Local Handoff Integrity Tool

## Current status

`runtime/handoff/tools/air-handoff.py` is the v0.3.0 repository-relative compatibility implementation.

It can generate Ed25519 key material, manage a local trust store, sign handoff payloads, verify signatures and continuity, accept verified state into a local anchor, and run self-tests.

## Security boundary

Private keys must remain outside repositories and ordinary project workspaces. The Stage 2 installed application reserves a global keystore boundary under the AIR data root.

Verification is read-only. `accept` advances continuity state only after review. A valid signature does not prove legal identity, source safety, semantic correctness, or execution permission.

## Stage 4 migration

Stage 4 must move handoff operations onto:

- the shared installed-resource resolver;
- the global keystore provider interface;
- per-project handoff, trust, signature, anchor, evidence, and receipt directories;
- unified `air handoff ...` terminal commands;
- migration and compatibility tests.

The legacy tool remains unchanged in Stage 2.
