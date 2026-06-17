# AIR Grounding Method Pack - Method Execution State Review

`SYSTEM_DESIGNATION`: `AIR_GROUNDING_METHOD_PACK_METHOD_EXECUTION_STATE_REVIEW_V1`

`PROFILE_KIND`: `METHOD_PACK`

`profile_function_class`: `EXECUTION_METHOD_PACK`

`STATUS`: `GENERATED_PROMPT_SIDE_VALIDATED_AVAILABLE`

## Purpose

This Method Pack gives AIR Grounding Specialist a reusable review procedure for method-governed work.

Use it when `AIR_ARTIFACT.method`, `AIR_ARTIFACT.method_execution_state`, method-step gates, evidence logs, Method Pack promotion, Method Pack staleness, AIR_GATE interaction, or handoff preservation materially affect approval, closure, mutation, rescope, or claims.

It standardizes procedure. It does not govern Orbit 0, replace AIR_GATE, prove execution, or provide backend validation.

## May bind as

- `method_overlay`
- `procedure_pack`
- `referential_method_layer`

## Must not bind as

- `active_orbit_0_contract`
- `governing_specialist_profile`
- `domain_authority`
- `backend_validation_evidence`
- `empirical_improvement_proof`
- `execution_proof`

## Procedure

1. Identify whether `method_execution_state` is required.
2. Inspect method origin, active method id, active method step, and step states.
3. Review evidence log against `evidence_to_advance`.
4. Reconcile method-step gate with AIR_GATE and active contract requirements.
5. Review Method Pack staleness when dependencies are material.
6. Review Method Pack promotion only when proposed or materially relevant.
7. Produce closure, review, rejection, evidence-required, or rescope decision with one next allowed action.

## Definition of done

- Method execution state requirement classified.
- Active method step and step states reviewed when material.
- Evidence log checked against `evidence_to_advance`.
- `method_step_gate` and AIR_GATE interaction reconciled.
- Method Pack staleness reviewed when material.
- Method Pack promotion reviewed only when proposed or materially relevant.
- Decision posture and next allowed method action produced.

## Failure modes prevented

- treating a written method as proof that execution occurred
- using stale Method Packs for approval or claims
- skipping method evidence gates
- promoting one-off methods into dead-weight context
- allowing method-step gates to replace AIR_GATE
- losing active method state during handoff

## Claim boundary

This Method Pack standardizes review procedure only. It does not prove execution, backend validation, empirical improvement, compliance, safety, production readiness, or tool execution.

==================================================
AIR USER ALIGNMENT AND EXECUTION WORKFLOW METHOD PACK EXTENSION
==================================================
Patch marker: AIR_USER_ALIGNMENT_AND_EXECUTION_WORKFLOW_V1

Activation:
Use this extension when this Method Pack reviews method-governed output and the
selected delivery form materially affects implementation, approval, closure,
handoff, or user success.

Procedure addition:
8. Review output delivery form against user_execution_workflow when material.
   Produce a delivery-form decision: matches workflow / review required /
   approval required to change / not material.

Evidence to advance:
- user_execution_workflow mode and source authority
- working agreement summary
- explicit skip, defer, or provisional state when Q6/user alignment is not resolved
- explicit approval if the delivery mode changes from a binding workflow

Blocking effects:
- Do not approve method-governed output in a delivery form that conflicts with the
  active working agreement when the mismatch materially affects success.
- Do not treat delivery form as a user competence label.
- Do not let user execution workflow override AIR_GATE, active contract scope,
  evidence requirements, method-step gates, or method execution state.

Claim boundary:
This extension standardizes delivery-form review only. It does not prove execution,
backend validation, empirical improvement, compliance, safety, production readiness,
or user competence.

