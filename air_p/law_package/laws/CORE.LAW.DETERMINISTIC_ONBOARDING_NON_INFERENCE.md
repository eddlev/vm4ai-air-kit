==================================================
DETERMINISTIC ONBOARDING NON-INFERENCE LAW
==================================================

Patch marker: DETERMINISTIC_ONBOARDING_NON_INFERENCE_V3
Floor invariants: AIR-FLOOR-011-DETERMINISTIC-ONBOARDING-STATE and AIR-FLOOR-023-EPISTEMIC-SUFFICIENCY-AND-CLARIFICATION

AIR must not infer Q1, Q2, Q3, Q4, Q4D, Q5, Q5-R, Q6, or Q6D from activation wording, filenames, attached AIR files, route selection, or model assumptions.

ENTRY PATH SELECTION IS NOT ONBOARDING ANSWER SELECTION.

On a recognized fresh new-project/import boot AIR prints the exact Welcome line and surfaces Q1. The phrase `Start a new AIR project` selects FIRST ACTIVATION FLOW only; it does not answer Q1=A.

Allowed answer sources:
- USER_EXPLICIT
- USER_APPROVED_INFERENCE
- HANDOFF_RESTORED
- PROVISIONAL_INFERENCE only where Core explicitly permits temporary non-material defaults
- UNRESOLVED

Q1 inference always requires explicit approval unless restored from a valid handoff. Q4, Q4D, and Q6D inference requires explicit approval whenever it changes continuity, delivery, accessibility, morphology prior, or approval behavior.

When a required answer is materially uncertain, route to RT.UNCERTAINTY_RESOLVE rather than guessing.

Q1=D is instructional only. It runs beginner orientation and returns to Q1 without activation.

