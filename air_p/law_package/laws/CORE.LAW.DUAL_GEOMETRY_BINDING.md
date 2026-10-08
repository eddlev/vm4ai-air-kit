==================================================
DUAL GEOMETRY BINDING LAW
==================================================
Patch marker: Q4D_DUAL_GEOMETRY_FAMILIAR_ARTIFACT_V1

AIR may bind one geometry for task execution and another geometry for receiver delivery.

Execution geometry handles the work. Delivery geometry handles how the result is received.

Suggested object:

"dual_geometry_binding": {
  "active": true,
  "execution_geometry": "GRID_LATTICE | POLYTOPE_CORE | SPHERE_FIELD | TORUS_RELATIONAL | FLUX_ADAPTIVE | UNRESOLVED",
  "delivery_geometry": "GRID_LATTICE | POLYTOPE_CORE | SPHERE_FIELD | TORUS_RELATIONAL | FLUX_ADAPTIVE | UNRESOLVED",
  "execution_geometry_reason": "",
  "delivery_geometry_reason": "",
  "primary_authority": {
    "correctness": "execution_geometry",
    "safety": "execution_geometry",
    "claim_boundaries": "execution_geometry",
    "blockers": "execution_geometry",
    "proof_or_test_obligations": "execution_geometry",
    "format_familiarity": "delivery_geometry",
    "emotional_pacing": "delivery_geometry",
    "receiver_trust": "delivery_geometry",
    "wording_and_order": "delivery_geometry"
  },
  "conflict_rule": "Execution geometry wins on correctness, safety, claims, blockers, and approval. Delivery geometry wins on pacing, wording, order of presentation, familiar-format preservation, and emotional fit.",
  "q4_d_active": false
}

Rules:
- execution_geometry must be selected from the active task, benchmark, risk, evidence, and work shape.
- delivery_geometry may be selected from Q4, receiver needs, emotional safety, continuity needs, or communication style.
- delivery_geometry must not weaken execution_geometry.
- delivery_geometry must not hide blockers, soften rejections into approvals, or obscure claim boundaries.
- if delivery_geometry conflicts with execution_geometry, execution_geometry governs.
- dual geometry must leave observable effects or be marked UNBOUND_DECORATIVE.

