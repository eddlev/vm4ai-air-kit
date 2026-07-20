# Artifact Lifecycle Reference

The shared lifecycle is:

`INTAKE -> SOURCE_PLAN -> BUILD_PLAN -> CONSTRUCTION -> STRUCTURAL_VALIDATION -> SEMANTIC_VALIDATION -> CROSS_FILE_VALIDATION -> REGRESSION_VALIDATION -> ASSURANCE_REVIEW -> APPROVAL_REQUIRED -> APPROVED_FOR_BINDING -> RELEASE_READY -> RELEASED`

`BLOCKED` and `DEPRECATED` are explicit states.

A state name is declared execution state, not proof that work occurred. Later states require evidence or a recorded bounded waiver. Generated artifacts cannot approve or bind themselves.
