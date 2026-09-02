# AIR Release Channel Policy

AIR uses separate **Preview** and **Stable** release channels so validation rigor can scale with the claim being made without freezing active development.

## Preview / Development

Preview releases are intended for active users, contributors, integration experiments, and field feedback.

A preview should normally require:

1. successful static/integrity validation for the changed release surface;
2. targeted regression tests for the components actually changed;
3. a small core behavioral smoke set covering boot, continuity/handoff, fail-closed behavior, and any directly affected runtime semantics;
4. truthful disclosure of missing evidence and known limitations;
5. no unresolved defect known to make ordinary preview use materially unsafe or structurally invalid.

Preview releases may be published while broader behavioral validation remains ongoing. They must not be described as stable, universally compatible, or fully behaviorally certified.

## Stable

Stable releases carry a stronger claim and therefore require broader evidence.

A stable milestone should include:

1. full applicable static validation;
2. the complete release-critical behavioral suite;
3. repeated independent/fresh or equivalently isolated model runs where stability is claimed;
4. zero unresolved critical unstable cases;
5. closure or explicit disposition of material field-reported regressions;
6. reproducibility and evidence records sufficient to explain the release decision.

## Change-sensitive validation

AIR does not require every preview patch to rerun every historical behavioral case.

Validation should be selected by change impact:

- always run the core preview smoke;
- run direct regression cases for changed Foundation/runtime semantics;
- run affected Specialist/package tests when Specialist closure changes;
- expand to adjacent cases when dependency or blast-radius analysis indicates risk;
- run the full matrix at stable milestones.

## Field evidence

Real-world use is a first-class development signal, but field reports are not automatically equivalent to controlled validation.

Field observations should record, when available:

- AIR version/release channel,
- provider/model,
- host/platform,
- relevant tool availability,
- exact reproduction sequence,
- visible output,
- and whether the behavior is reproducible.

Fast patching is encouraged, but bug frequency itself is not a success metric. The desired signal is active use, transparent issue handling, and disciplined regression closure.
