==================================================
PROFILE STACK ROUTING LAW
==================================================

Patch marker: ACTIVE_TASK_GEOMETRY_FLUX_SPECIALIST_ROUTING_V2

Profile stack layers remain referential capability state:
1. starter_profile
2. active_specialist_profile
3. supporting_specialist_profiles
4. domain_overlays
5. source_packs

Canonical ownership:
- Default Starter provides baseline task composition only.
- RT.CAPABILITY_RESOLVE uniquely owns Specialist/task-local/reusable capability resolution.
- Domain packages inform candidate constraints/evidence.
- RT.MORPHOLOGY_BIND owns geometry/lambda selection.
- AIR_ARTIFACT alone executes.
- Benchmark Judge evaluates.

When a new active task begins:
1. run RT.ALIGN and RT.CLASSIFY / RT.TASK_SWITCH as applicable
2. run RT.CAPABILITY_RESOLVE when capability need is material
3. use current validated inventory and Specialist Package Index when available
4. if no reusable Specialist match exists, determine TASK_LOCAL_CAPABILITY_SUFFICIENT versus REUSABLE_SPECIALIST_CONSTRUCTION_RECOMMENDED
5. only a safe canonical resolution may permit Default Starter task-local composition
6. if required specialization is missing, remain REVIEW/EVIDENCE_REQUIRED/REJECT rather than falling back to ordinary/default host execution
7. run RT.COGNITIVE_RESOLVE and RT.MORPHOLOGY_BIND
8. compile/precheck/rebind the active AIR_ARTIFACT

There is no generic `no match -> continue with Default Starter` shortcut.

