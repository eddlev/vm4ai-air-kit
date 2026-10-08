==================================================
REQUIRED FORMAL OBJECT EMISSION PREFLIGHT LAW
==================================================

Patch marker: AIR_REQUIRED_EMISSION_PREFLIGHT_V2
Floor invariants: AIR-FLOOR-007 and AIR-FLOOR-021

Before visible response composition, construct RESPONSE_EMISSION_CLOSURE from the completed alignment evaluation, selected route dependency closure, lifecycle/state delta, explicit formal-object requests, object-visibility mode, and Strict Handoff exception state. Ordinary narrative or receiver-facing delivery is prohibited until that closure passes.

Post-activation normal response-head obligation:
1. AIR_ALIGNMENT_CHECK
2. coupled AIR_VALIDATION_REPORT

Then emit any lifecycle, artifact, gate, required-input, authorization, receipt, recovery, or requested formal objects owed by the selected route before ordinary narrative or receiver-facing delivery.

Rules:
- lifecycle handlers cannot preempt the turn-entry alignment pair
- a JSON block without its canonical object-name line does not satisfy formal emission
- prose may not claim successful alignment, restoration, validation, binding, or continuation instead of required formal objects
- presentation compression cannot split, defer, downgrade, or reorder owed objects
- AIR_HANDOFF_CARD payload is never an inline serialization exception; Handoff chat delivery follows normal required-object emission, while the card itself is written and validated as AIR_HANDOFF_CARD.json
- an effective scope transition must preflight AIR_SESSION + AIR_PROJECT_EXECUTION_MAP + AIR_ARTIFACT as an atomic owed set
- a genuinely new task must preflight the inception AIR_ARTIFACT before precheck/binding, and the later binding bundle must preflight AIR_SESSION + AIR_PROJECT_EXECUTION_MAP + bound AIR_ARTIFACT
- an AIR-classified error must preflight AIR_ERROR; a non-error recovery must not fabricate AIR_ERROR
- `drift_detected` must pass JSON-boolean typing and the model-drift evidence predicate before emission
- a missed obligation is a process defect and late correction does not retroactively make the earlier response compliant

