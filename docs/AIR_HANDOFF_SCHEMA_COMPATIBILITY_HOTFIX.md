# AIR Handoff Schema Compatibility Hotfix

## Defect

AIR Core Runtime v2.1.0 required `AIR_HANDOFF_CARD.schema_version = 2.0.0`, while the authoritative Handoff Card Template declared schema `2.1.0`. The mismatch correctly blocked activation before Q1, but the release itself was internally inconsistent.

The same template also retained `AIR_DEFAULT_STARTER_V2` at `PROMPT_VERSION: 2.0.0`, while the current Starter was newer.

## Resolution

- Core Runtime: `2.1.1`
- Control Surface: `2.1.1`
- Default Starter: `2.2.1`
- Handoff schema: remains `2.1.0`
- Specialist package integration: `2.3.1`

Core now requires the current Handoff schema instead of requesting a downgrade. Core, Control, Starter, and the Template carry an explicit cross-file equality check. All three specialist packages are resealed against the corrected foundation.

## Boundary

This is prompt-layer and tool-observed release validation. It does not establish backend enforcement or guarantee host-model adherence.
