==================================================
NATIVE MEANING ALIGNMENT LITE LAW
==================================================

Patch marker: AIR_NATIVE_MEANING_ALIGNMENT_LITE_V3

Native Meaning Alignment Lite is a lightweight semantic-fidelity check inside RT.INPUT_TRANSLATE and AIR_MII_SEMANTIC_FIDELITY_V1. It compares resolved intended task center with AIR's translated task representation and evaluates coverage, coherence, ambiguity, semantic-loss risk, and typed semantic deltas at the INPUT_TO_INTENT / INTENT_TO_TASK boundaries.

It may return PASS, REVIEW, or REJECT for the affected translation and contributes to the parent semantic_fidelity_state. REVIEW/REJECT routes to RT.UNCERTAINTY_RESOLVE or correction. It does not independently authorize execution, replace the raw input, create a parallel alignment authority, or supersede the full intent-to-execution/output reconciliation required before material action or delivery.

