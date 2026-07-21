# AIR Model Portability Notes

AIR is prompt-native and may behave differently across AI models, context limits, interfaces, and provider policies.

## Resource routes

- Use the Complete AIR Prompt Set when the interface can load the full canonical files.
- Use task-specific modular bundles produced by `air boot` after local validation passes. Keep the Complete AIR Prompt Set available as the visible fallback.
- Use installed-resource materialization when a local package resource must be attached to an interface.

## Portability evidence

A model is not considered compatible merely because it accepts the files or produces AIR-shaped JSON.

Test at least:

- deterministic Q1 branch behaviour;
- complete Q1-D orientation;
- onboarding sequence;
- active-step preservation;
- blockers and evidence gates;
- handoff restoration;
- no false backend or repository claims;
- receiver-facing delivery behaviour.

## Current boundary

Stage 3 validates deterministic local bundle construction and complete Q1-D semantic closure. Cross-model behavioral equivalence still requires empirical host-by-host testing; a valid bundle is not itself compatibility proof.
