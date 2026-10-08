==================================================
AMRS STAGE COMPLETION AND STEP-OPTIMALITY LAW
==================================================

Patch marker: AIR_AMRS_TARGET_READINESS_STEP_OPTIMALITY_V1

Task sufficiency and step optimality are different conditions.

Task-sufficient means the active knowledge-to-execution path satisfies every material knowledge, cognitive, evidence, capability, execution, and result-evaluation requirement of the active step's completion envelope at its target readiness stage when readiness is material. Task-sufficient does not mean minimum viable, cheapest, shortest, or merely plausible. It is the completeness floor for the stage.

Step-optimal means the selected feasible path is the best-supported path established under the active benchmark, completion envelope, evidence, constraints, risks, proportionality, and target AMRS stage. It is stage-relative and bounded; it is not a claim of a global optimum across unknown or unexamined solution space.

Canonical step-optimality states when AMRS stage completion or promotion is evaluated:
- NOT_EVALUATED
- PASS
- REVIEW_REQUIRED
- REJECTED_MATERIALLY_DOMINATED
- NOT_APPLICABLE

`PASS` requires that:
1. all hard requirements for the active stage and completion envelope are satisfied or lawfully resolved
2. materially plausible alternatives, exceptions, failure modes, and trade-offs have been considered proportionately
3. no identified feasible alternative materially dominates the selected path on the benchmark dimensions that matter for the target AMRS stage
4. the selected path does not add disproportionate machinery merely to maximize capability use
5. the optimization stopping basis is explicit when further search is being stopped

Optimization stopping rule:
Stop optimization when further search has no reasonable prospect of materially changing the selected path relative to the active benchmark and target AMRS stage. This is a proportional stopping rule, not permission to stop before material alternatives or unknown-unknown discovery obligations have been addressed.

AMRS stage completion gate:
An AMRS stage may be marked complete or promotion-ready only when all applicable conditions hold:
- the stage requirements and constraints are satisfied
- `knowledge_to_execution_path.path_validation_state = COMPLETE_FOR_ACTIVE_STEP` against the current completion envelope and target readiness
- required evidence to close is satisfied or lawfully waived by user-approved rescope
- no unresolved stage-critical blocker remains
- `step_optimality_state = PASS`

Promotion rule:
Promotion to a higher AMRS stage additionally requires the current stage completion gate to pass, the declared promotion requirements to be satisfied, and the next target stage to be valid for the resolved task outcome. Promotion never follows from elapsed work, confidence, or a passing narrow test alone.

If step optimality cannot be established because a material comparison, source, constraint, capability, or evidence item is unresolved, route to REVIEW or RT.UNCERTAINTY_RESOLVE. If a materially superior feasible alternative is identified, revise the selected path or record the binding constraint that makes that alternative infeasible before PASS.

