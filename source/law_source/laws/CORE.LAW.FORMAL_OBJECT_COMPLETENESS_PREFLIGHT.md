==================================================
FORMAL OBJECT COMPLETENESS PREFLIGHT LAW
==================================================

Patch marker: AIR_FORMAL_OBJECT_COMPLETENESS_PREFLIGHT_V2

Before emission, validate each formal object against:
- canonical object registry and exact record_class
- common required fields
- current evaluation_basis where required
- object-specific required fields
- current route/state dependencies
- canonical enum/value constraints

Shortened or compact objects using reserved formal labels are invalid. AIR may use non-reserved presentation summaries, but if it names AIR_SESSION, AIR_ARTIFACT, AIR_GATE, AIR_REQUIRED_INPUT_REQUEST, or another formal object as emitted, the complete canonical object must be present.

AIR_ALIGNMENT_CHECK completeness is evaluated against AIR_CANONICAL_OBJECT_CONTRACTS_V4, against the current alignment evaluation schema.

