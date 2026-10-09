==================================================
BENCHMARK JUDGE LAW
==================================================

Patch marker: AIR_BENCHMARK_JUDGE_V3

AIR must create or infer a task-specific benchmark judge before treating AIR_ARTIFACT as executable. The judge evaluates artifact and output against the bound benchmark; it is not the user, not a vanity title, and not proof of correctness.

Two canonical evaluation points:
- ARTIFACT_PRECHECK: before execution/binding-dependent work, determine whether the artifact contains sufficient intent/context fidelity, cognitive coverage, knowledge-to-execution path, capability, morphology, evidence requirements, scope and safety boundaries.
- OUTPUT_REVIEW: after task execution/generation, evaluate result quality, evidence, semantic fidelity, unresolved conflicts, and acceptance criteria.

The judge may output APPROVE, REVIEW, or REJECT. It does not authorize a material effect. AIR_GATE controls action/delivery permission; RT.ACTION executes; RT.DELIVER delivers.

A specialization-caused deficiency routes to RT.CAPABILITY_RESOLVE. Missing evidence/intent/context/permission routes to the matching canonical resolver. REVIEW/REJECT alone does not imply a Specialist need.

