# Start AIR — v2.5.0-preview.1

This is the shortest path from the current AIR Preview Foundation to a working project.

## New project

Attach all five current Foundation files:

1. `AIR_CORE_RUNTIME.md` — 2.5.0
2. `AIR_CONTROL_SURFACE.md` — 2.5.0
3. `AIR_GOV.md` — 2.3.0
4. `AIR_DEFAULT_STARTER_PROFILE.json` — 2.5.0
5. `AIR_HANDOFF_CARD_TEMPLATE.json` — schema 2.3.0

Then send:

```text
Start a new AIR project.
```

AIR validates the supplied Foundation and begins onboarding at Q1. The activation phrase selects the new-project bootstrap route but does not silently answer Q1.

## Import an existing non-AIR project

Load the same five-file Foundation and choose the import route at Q1. Supply the existing material as source input. AIR reconstructs the project contract from explicit evidence rather than inventing prior AIR state.

## Continue from an AIR Handoff Card

Load the current Foundation plus the populated `AIR_HANDOFF_CARD` from the prior AIR session. Choose the continuation route.

The receiving runtime validates the card and current source state before rebinding the nominated artifact. A Handoff Card transfers recorded state, not current execution authority or hidden model state.

## Current release boundary

`v2.5.0-preview.1` is a Preview / Development release. Static/integrity validation and targeted behavioral smoke have passed for the current repair surface; the broader repeated behavioral matrix is reserved for a Stable milestone.

See:

- [Release channel policy](RELEASE_CHANNEL_POLICY.md)
- [Validation evidence](VALIDATION_EVIDENCE_2.5.0-preview.1.md)
- [Bug reporting](BUG_REPORTING.md)
- [Compatibility](COMPATIBILITY.md)
- [Website get-started guide](https://vm4ai.com/get-started.html)

AIR remains prompt-compiled and host-model governed. It does not guarantee correctness or independently provide deterministic backend enforcement.
