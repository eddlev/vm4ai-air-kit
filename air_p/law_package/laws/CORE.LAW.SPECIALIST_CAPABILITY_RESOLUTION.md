==================================================
SPECIALIST CAPABILITY RESOLUTION ROUTER
==================================================
Patch marker: AIR_SPECIALIST_CAPABILITY_RESOLUTION_ROUTER_V1
Floor invariant: AIR-FLOOR-016-REQUIRED-INPUT-AND-ARTIFACT-ACQUISITION

Purpose:
AIR must convert a specialization-caused benchmark or capability deficiency into a deterministic acquisition or construction route instead of leaving the user to infer which Specialist file or package is needed.

Trigger boundary:
Run this router:
- during capability-layer need detection before artifact precheck when a material specialization gap is already visible
- during ARTIFACT_PRECHECK when APPROVE is withheld because task-specific specialist judgment, evaluation logic, domain-operational strategy, or reusable execution constraints are missing
- during OUTPUT_REVIEW when REVIEW or REJECT identifies insufficient specialization as a material cause

Do NOT trigger this router merely because approval_state = REVIEW or REJECT. Missing evidence, permissions, sources, user intent, ordinary ambiguity, invalid files, unsafe scope, or execution failure must use their own resolving route unless a distinct specialization gap also exists.

Specialization gap states:
- NONE
- SUSPECTED
- EXISTING_SPECIALIST_MATCH
- EXISTING_SPECIALIST_REQUIRED_MISSING
- TASK_LOCAL_CAPABILITY_SUFFICIENT
- REUSABLE_SPECIALIST_CONSTRUCTION_RECOMMENDED
- CAPABILITY_ECOLOGY_REQUIRED_MISSING
- UNRESOLVED

Resolution sequence:
1. Identify the missing capability or judgment and why the current benchmark/artifact cannot safely or adequately supply it.
2. Check current validated session/package inventory for a matching Specialist.
3. Check the current validated AIR_SPECIALIST_PACKAGE_INDEX when available.
4. If a matching validated Specialist package exists but is not available in the session, request the exact canonical package or component set under Required Input acquisition. Do not ask generically for \"a specialist file\" when an exact package identity is known.
5. After receipt, validate identity, version, hash, compatibility, task fit, package completeness, and authority boundaries before selection. Attachment alone never binds.
6. If no matching reusable Specialist exists, determine whether the gap is task-local or merits reusable Specialist construction.
7. TASK_LOCAL_CAPABILITY_SUFFICIENT: represent the missing capability directly in the task-scoped synthetic role, domain/source requirements, method, and execution benchmark. Do not create a permanent Specialist merely to solve a one-off capability gap.
8. REUSABLE_SPECIALIST_CONSTRUCTION_RECOMMENDED when one or more are material:
   - repeated distinctive workflow or method sequencing
   - domain-specific risk gates, escalation, or decision behavior
   - recurring evaluation logic or output contract
   - specialized evidence reconciliation, review posture, or proportionality decisions
   - portability across tasks/projects would materially reduce drift or rework
9. When reusable construction is warranted, route to AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2 as the canonical Specialist-construction capability.
10. If that package is unavailable, request the complete package:
   - AIR_DOMAIN_CAPABILITY_REGISTRY.json
   - AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json
   - AIR_CAPABILITY_ECOLOGY_ARCHITECT.json
   - AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json
   - AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json
11. Upload/availability does not itself authorize Specialist generation. Generation requires the explicit approval required by Capability Layer Need Detection law.
12. Capability Ecology may construct a candidate SPECIALIST_CAPABILITY_PROFILE or determine that task-local capability composition is sufficient. The candidate remains non-operative until schema validation, compatibility validation, approval, and compilation into the bound Orbit 0 AIR_ARTIFACT.
13. If the current task cannot meet its benchmark without the missing Specialist, keep the affected task/action in REVIEW, EVIDENCE_REQUIRED, or REJECT as appropriate until resolution. Do not continue as ordinary/default host execution.

Artifact interaction:
- A Specialist acquired or created for the same task is a material artifact input change and requires the current AIR_ARTIFACT to be revised/prechecked/emitted/rebound as required by Core.
- A new task boundary still requires a new task AIR_ARTIFACT under the New Task Execution Binding Barrier; specialist resolution never transfers execution authority across tasks.

