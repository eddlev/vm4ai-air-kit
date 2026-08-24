# Start AIR

This is the shortest path from the AIR download to a working project.

If you downloaded `AIR-core.zip`, this file is included with the current five-file foundation.

## New project

Attach all five foundation files to a capable AI session:

1. `AIR_CORE_RUNTIME.md`
2. `AIR_CONTROL_SURFACE.md`
3. `AIR_GOV.md`
4. `AIR_DEFAULT_STARTER_PROFILE.json`
5. `AIR_HANDOFF_CARD_TEMPLATE.json`

Then send:

```text
Start a new AIR project.
```

AIR validates the supplied foundation and begins onboarding at Q1. The activation phrase does not silently answer Q1.

## Import an existing non-AIR project

Load the same five-file foundation, then choose the import route when AIR asks Q1. Supply the existing project material you want AIR to treat as source input.

AIR should reconstruct the project contract from explicit evidence rather than pretending a prior AIR state exists.

## Continue from an AIR Handoff Card

Load:

- the complete current five-file foundation, and
- the populated `AIR_HANDOFF_CARD` from the previous AIR session.

Choose the Handoff continuation route. The receiving AIR runtime validates the transfer state and rebinds the active project state before material execution resumes.

A Handoff Card carries recorded AIR state. It does not transfer hidden model state or guarantee byte-for-byte identical inference.

## What onboarding is configuring

AIR onboarding is not a personality quiz. It binds how the project should be worked.

- **Q1 — project state:** new project, imported non-AIR project, AIR Handoff continuation, or orientation.
- **Q2 — checking rigor:** how aggressively AIR should verify and challenge the work.
- **Q3 — ambiguity handling:** whether AIR should stop early for ambiguity or tolerate more exploration.
- **Q4 — continuity / delivery style:** how the work should maintain structure, tone, or creative continuity. `Q4=D` activates the neurodivergent delivery modifier; Q4D then preserves the underlying continuity style.
- **Q5 — work definition:** what you are actually trying to accomplish, including material constraints and sources.
- **Q6 — working contract:** responsibility split, output/delivery form, approval boundaries, stopping conditions, assumptions, and how strongly AIR should challenge you.
- **Q6D — delivery calibration:** when the neurodivergent modifier is active, AIR can calibrate pacing, chunking, side-track handling, important-information presentation, momentum support, voice-to-text handling, memory support, and managed breaks.

Neurodivergent delivery changes interaction, not the evidentiary or governance standard. It does not reduce truth, scope, approval, safety, artifact-binding, or formal-object requirements.

## Load-integrity note

The complete required files must fit in the host interface without truncation. Provider/model context windows, attachment handling, and tokenization differ, so AIR does not claim one universal token threshold.

If a required file is partial, truncated, mixed-version, or otherwise fails the runtime's integrity checks, do not treat the session as a valid AIR boot.

## Useful next links

- [Get started](https://vm4ai.com/get-started.html)
- [Use-case onboarding patterns and Q5/Q6 examples](https://vm4ai.com/use-cases.html)
- [How AIR works](https://vm4ai.com/how-it-works.html)
- [Technical documentation](https://vm4ai.com/air-docs.html)
- [GitHub Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions)

AIR is prompt-based and host-model governed. It adds explicit structure and continuity; it does not guarantee correctness or independently provide deterministic backend enforcement.
