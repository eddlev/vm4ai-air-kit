==================================================
MII RISK PROPAGATION LAW
==================================================

Patch marker: AIR_MII_RISK_PROPAGATION_V1

COG.RISK_PROPAGATION upgrades adjacent blast-radius analysis into a dependency-aware consequence graph when material.

Risk contribution fields may include:
- originating action_or_decision
- direct_effects
- affected_assets_or_parties
- dependency_edges
- secondary_effects
- cascade_paths
- affected_scope
- impact
- likelihood when evidence supports assessment, otherwise UNKNOWN
- reversibility
- detectability
- propagation_depth
- containment
- control_strength
- evidence_quality
- residual_risk
- unknowns

Risk cognition informs the benchmark, AIR_GATE, action scope, rollback/recovery, and evidence requirements only after compilation into the bound artifact.

