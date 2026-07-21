# Installed Boot Service

## Current status

Stage 3 moves boot behavior onto the shared installed-resource resolver and the reusable `vm4ai_air.boot.BootCompiler` service.

The service validates every declared kernel, starter, semantic-closure, Complete AIR Prompt Set, and module byte relationship before planning. It resolves dependency closure deterministically, rejects conflicting or unknown module identities, and uses a visible Complete AIR Prompt Set fallback for unknown triggers.

## Terminal commands

```bash
air boot validate
air boot validate --module AIR_RUNTIME_ENTRY_AND_ACTIVATION_V1
air boot plan --trigger NEW_PROJECT
air boot plan --trigger Q1_D_ORIENTATION
air boot compile --trigger CODING --trigger REPOSITORY --output air-bundle.md --receipt air-bundle.receipt.json
air boot compare --trigger CODING
air boot q1d
air boot contracts
air boot status
```

The compiled bundle is deterministic for the same package resource set and normalized trigger set. The optional receipt contains a timestamp and records the bundle digest separately.

## Compatibility path

`runtime/boot/tools/air-boot.py` remains as a thin v0.3.0 command adapter. It delegates to the same installed `air boot` services with an explicit authoring-source override; it no longer contains a second planner or validator implementation.

## Security and authority boundary

- Module loading is not execution authorization.
- Unknown triggers return `REVIEW` and use the Complete AIR Prompt Set fallback unless fallback is explicitly disabled.
- Compile receipts prove observed local bytes and a bundle digest only.
- MCP servers, Codex plugins, and other coding-tool adapters remain optional post-Stage-3 integrations.
- Handoff signing and local trust anchors remain Stage 4 work.
