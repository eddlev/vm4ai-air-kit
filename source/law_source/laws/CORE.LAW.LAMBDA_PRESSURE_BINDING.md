==================================================
LAMBDA PRESSURE BINDING LAW
==================================================

Patch marker: AIR_LAMBDA_PRESSURE_BINDING_V3

Lambda pressure is a morphology control owned by RT.MORPHOLOGY_BIND. It may alter ambiguity tolerance, convergence timing, branch pruning, review strictness, and claim-boundary pressure for the active task or a specific MII node.

Each bound lambda state must identify:
- scope = TASK | COGNITIVE_NODE
- pressure level or bounded qualitative state
- convergence pressure
- review strictness
- branch-pruning rule
- claim-boundary effect
- observable effect trace

If no observable effect can be identified, classify lambda as UNBOUND_DECORATIVE. Prompt-layer lambda language must not be described as measured model-internal pressure without instrumentation.

