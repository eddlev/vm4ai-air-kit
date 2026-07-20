# Local Handoff Integrity Tool

**Path:** `runtime/handoff/tools/air-handoff.py`

## Purpose

Generate Ed25519 key material, manage a local trust store, sign handoff payloads, verify signatures and continuity, accept verified state into a local anchor, and run self-tests.

## Dependencies

Install the pinned requirements from `runtime/handoff/tools/requirements.txt` in an isolated environment.

## Typical flow

```bash
python runtime/handoff/tools/air-handoff.py --json keygen --private-key private.pem --public-key public.pem
python runtime/handoff/tools/air-handoff.py --json trust-add --trust-store trust.json --public-key public.pem --key-id local-key --project-id PROJECT --branch-id main --allow-genesis
python runtime/handoff/tools/air-handoff.py --json sign --handoff handoff.json --private-key private.pem --key-id local-key --output envelope.json
python runtime/handoff/tools/air-handoff.py --json verify --handoff handoff.json --envelope envelope.json --trust-store trust.json --anchor anchor.json --output result.json
python runtime/handoff/tools/air-handoff.py --json accept --handoff handoff.json --envelope envelope.json --trust-store trust.json --anchor anchor.json --receipt acceptance.json
```

## Security

Keep private keys outside the repository. Verification is read-only. `accept` advances local continuity state and should be performed only after review. A valid signature does not prove legal identity, source safety, or execution permission.
