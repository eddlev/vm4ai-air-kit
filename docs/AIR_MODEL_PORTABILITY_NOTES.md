# AIR Model Portability Notes

AIR is prompt-native and may behave differently across AI models, context limits, interfaces, and provider policies.

## Resource routes

- Use the Complete AIR Prompt Set when the interface can load the full canonical files.
- Use task-specific modular bundles only after Stage 3 repairs and validates their semantic closure.
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

Stage 2 validates the local package and resource substrate. Cross-model modular boot and Q1-D validation remain Stage 3 work.
