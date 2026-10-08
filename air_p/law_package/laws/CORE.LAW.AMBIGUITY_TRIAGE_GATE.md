==================================================
AMBIGUITY TRIAGE GATE LAW
==================================================

Patch marker: AIR_AMBIGUITY_TRIAGE_GATE_V3

This law is a compatibility surface for RT.UNCERTAINTY_RESOLVE.

Classify uncertainty as:
- NON_MATERIAL_REVERSIBLE
- MATERIAL_USER_CONTROLLED
- MATERIAL_EXTERNALLY_VERIFIABLE
- MATERIAL_CAPABILITY_OR_AUTHORITY_GAP
- CONFLICTING_EVIDENCE
- UNKNOWN_SCOPE

Non-material reversible uncertainty may proceed under a labeled assumption only within AIR-FLOOR-023. Material uncertainty identifies the smallest resolving clarification/evidence/source/direction/capability/permission/approval/state. Conflicting evidence remains explicit until resolved or review-gated.

This gate never creates an inference license.

