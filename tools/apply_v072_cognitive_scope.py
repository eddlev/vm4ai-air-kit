from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

OLD_FOUNDATION = 'AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006'
NEW_FOUNDATION = 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'
OLD_SHORT = 'AIR_2_6_1_OBJECT_CONTRACT_SET_006'
NEW_SHORT = 'AIR_2_6_2_OBJECT_CONTRACT_SET_007'
OLD_SET = 'OBJECT_CONTRACT_SET_006'
NEW_SET = 'OBJECT_CONTRACT_SET_007'
FLOOR_028 = 'AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION'
HISTORY_KEYS = {
    'source_baseline', 'mainline_release_binding', 't7_change_record',
    'historical_release_catalogs', 'source_candidate_manifest', 'change_history',
    'release_history', 'historical_records',
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old == new:
        return text
    if old in text:
        if text.count(old) != 1:
            raise SystemExit(f'{label}: expected one anchor, found {text.count(old)}')
        return text.replace(old, new, 1)
    if new in text:
        return text
    raise SystemExit(f'{label}: missing old/new anchor')


def insert_before(text: str, anchor: str, block: str, marker: str, label: str) -> str:
    if marker in text:
        return text
    if anchor not in text:
        raise SystemExit(f'{label}: insertion anchor missing')
    return text.replace(anchor, block + '\n' + anchor, 1)


def historical(path: tuple[str, ...]) -> bool:
    return any(p in HISTORY_KEYS or p.startswith('historical_') for p in path)


def current_transform(obj: Any, path: tuple[str, ...] = ()) -> Any:
    if historical(path):
        return obj
    if isinstance(obj, dict):
        return {k: current_transform(v, path + (str(k),)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [current_transform(v, path + (str(i),)) for i, v in enumerate(obj)]
    if isinstance(obj, str):
        s = obj.replace(OLD_FOUNDATION, NEW_FOUNDATION)
        s = s.replace(OLD_SHORT, NEW_SHORT)
        s = s.replace(OLD_SET, NEW_SET)
        s = s.replace('PASS_SET_006_EXACT_RECEIPTS', 'PASS_SET_007_EXACT_RECEIPTS')
        return s
    return obj


def update_dependency_versions(obj: Any, path: tuple[str, ...] = ()) -> None:
    if historical(path):
        return
    if isinstance(obj, dict):
        filename = obj.get('filename') or obj.get('canonical_filename')
        versions = {
            'AIR_CORE_RUNTIME.md': '2.6.2',
            'AIR_CONTROL_SURFACE.md': '2.6.2',
            'AIR_GOV.md': '2.3.2',
            'AIR_DEFAULT_STARTER_PROFILE.json': '2.6.2',
            'AIR_HANDOFF_CARD_TEMPLATE.json': '2.3.0',
            'AIR_RUNTIME_ROUTE_MAP.json': '1.2.1',
        }
        if filename in versions:
            for key in ('version', 'prompt_version', 'PROMPT_VERSION', 'component_version'):
                if key in obj:
                    obj[key] = versions[filename]
            if filename == 'AIR_HANDOFF_CARD_TEMPLATE.json' and 'card_revision' in obj:
                obj['card_revision'] = 18
        tv = obj.get('target_foundation_versions')
        if isinstance(tv, dict):
            for k, v in [
                ('core', '2.6.2'), ('control', '2.6.2'), ('governance', '2.3.2'),
                ('starter', '2.6.2'), ('handoff_schema', '2.3.0')
            ]:
                if k in tv:
                    tv[k] = v
        for k, v in obj.items():
            update_dependency_versions(v, path + (str(k),))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            update_dependency_versions(v, path + (str(i),))


def append_benchmark_requirement(obj: Any) -> bool:
    if isinstance(obj, list):
        if any(isinstance(x, dict) and x.get('id') == 'REQ-MII-CONTRIBUTION-BOUNDARY' for x in obj):
            if not any(isinstance(x, dict) and x.get('id') == 'REQ-COGNITIVE-SCOPE-AUTHORITY-ISOLATION' for x in obj):
                obj.append({
                    'id': 'REQ-COGNITIVE-SCOPE-AUTHORITY-ISOLATION',
                    'plane': 'AIR_ARTIFACT_EXECUTION_BENCHMARK_PROFILE',
                    'condition': 'COGNITIVE_PROCESSING_OR_CONTRIBUTIONS_ARE_MATERIAL',
                    'fields': ['cognitive_scope'],
                    'source_law': FLOOR_028,
                    'failure_behavior': 'HOLD_COGNITIVE_OUTPUT_NONOPERATIVE_OR_RT_RECOVERY_ON_COGNITIVE_AUTHORITY_ESCAPE',
                })
            return True
        return any(append_benchmark_requirement(v) for v in obj)
    if isinstance(obj, dict):
        found = False
        for v in obj.values():
            found = append_benchmark_requirement(v) or found
        return found
    return False


def patch_core(root: Path) -> None:
    p = root / 'prompts/AIR_CORE_RUNTIME.md'
    t = p.read_text(encoding='utf-8')
    t = replace_once(t, 'PROMPT_VERSION: 2.6.1', 'PROMPT_VERSION: 2.6.2', 'Core version')
    floor27 = '- AIR-FLOOR-027-FAILURE-MODE-LEARNING-AND-RETRY: every evidenced execution failure that can materially affect a retry or structurally matching task is captured as a typed AIR_FAILURE_MODE_RECORD. Before a retry, iteration, or exact applicability match, AIR must query the active failure-mode registry and compile applicable corrective constraints into the bound Artifact benchmark. Failure records are evidence/constraint inputs only, never positive execution authority; uncertain root cause remains uncertain; successful retest retains the record for regression; handoff preserves the registry as non-authorizing continuation state; bound Specialist packages participate through Core and may propose failure observations but may not mutate the registry directly.\n'
    floor28 = floor27 + '- AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION: cognition may operate only inside the current Artifact-declared cognitive scope; cognitive output has no direct authority to mutate deterministic control state. Control may invoke cognition through declared scope, cognition may return candidate contributions to validation, and only validated contributions may enter Artifact/task state through an explicit declared ingestion boundary. Any attempted cognitive mutation of protected control state fails closed as COGNITIVE_AUTHORITY_ESCAPE.\n'
    if FLOOR_028 not in t:
        t = replace_once(t, floor27, floor28, 'Core floor 028')

    law = '''==================================================
COGNITIVE SCOPE AUTHORITY ISOLATION LAW
==================================================

Patch marker: AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1
Floor invariant: AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION

Purpose:
AIR may use deep, adaptive cognition without allowing cognitive conclusions to become deterministic control state by implication, convenience, confidence, or semantic similarity.

Canonical scope owner:
- AIR_ARTIFACT.execution_benchmark_profile.cognitive_scope

A material cognitive scope declares at least:
- scope_id
- objective
- scope_state
- permitted_input_refs
- permitted_route_ids
- permitted_cognitive_operations
- candidate_output_class
- protected_control_state_classes
- validation_ingress_contract
- uncertainty_behavior
- invalidation_triggers

Authority graph:
- CONTROL_TO_COGNITION = DECLARED_SCOPE_ONLY
- COGNITION_TO_CONTROL = PROHIBITED
- COGNITION_TO_VALIDATION = CANDIDATE_CONTRIBUTION_ONLY
- VALIDATED_CONTRIBUTION_TO_ARTIFACT_OR_TASK = EXPLICIT_DECLARED_INGESTION_ONLY

Protected control state includes at minimum:
- current task identity and Artifact revision identity
- Orbit placement and Artifact binding state
- deterministic route inputs, consequences, ordering, outputs, and pass/fail state
- approval scope identity, fingerprint, token state, and approval resolution
- AIR_GATE, AIR_ACTION_AUTHORIZATION, AIR_ACTION_RECEIPT, and authority-ledger state
- Artifact lease and resource scope pin
- surfaced-object provenance and historical authority state
- Handoff restoration/executable authority
- failure-mode registry authority and applicability state

Rules:
1. RT.COGNITIVE_RESOLVE may execute only against the current declared cognitive scope when cognition is material.
2. MII nodes, Specialists, translators, methods, heuristics, remembered context, and model judgment may produce candidate contributions inside that scope. They may not directly write protected control state.
3. Confidence, semantic equivalence, apparent user intent, optimization pressure, or successful task output cannot upgrade a cognitive contribution into control authority.
4. Cognitive contributions cross into deterministic state only at an explicit ingestion step named by the active benchmark/contract and only after the declared validation rule accepts the contribution.
5. HOLD, REVIEW, REJECTED, unresolved, stale, out-of-scope, or validation-failed contributions remain non-operative.
6. A scope change, Artifact revision change, task change, protected-control-state dependency change, or source/evidence invalidation makes the prior cognitive scope stale according to its invalidation triggers.
7. Handoff may preserve scope identity and contribution references only as non-authorizing continuation input. Restoration requires current-session validation and Artifact rebinding before operative reuse.
8. An attempted direct cognitive mutation of protected control state is COGNITIVE_AUTHORITY_ESCAPE: fail closed before effect when possible, enter RT.RECOVERY, and evaluate reusable failure capture. If an external effect already occurred, preserve effect truth without retroactive AIR authority.

Hidden-reasoning boundary:
This contract governs declared objectives, inputs, outputs, evidence, validation, and authority boundaries. It neither requests nor claims access to private chain of thought, latent state, or hidden reasoning traces.
'''
    anchor = '==================================================\nDETERMINISTIC PIPELINE NON-INFERENCE LAW\n==================================================\n'
    t = insert_before(t, anchor, law, 'AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1', 'Core cognitive law')

    old_route = '''[AIR_ROUTE]
id=RT.COGNITIVE_RESOLVE
semantic_owner=AIR_CORE_RUNTIME
trigger=task/input requires cognitive processing for benchmark execution
trigger_authority=NON_OPERATIVE_DESCRIPTION
control_event_ref=CE-RT-COGNITIVE_RESOLVE
requires=DEP.CANONICAL_INTENT;DEP.ACTIVE_CONTEXT;DEP.SOURCE_EVIDENCE_STATE;DEP.COMPLETION_ENVELOPE_RESOLVED;DEP.TARGET_READINESS_RESOLVED_WHEN_MATERIAL
produces=MII_COGNITIVE_ROUTE_SET;MII_CONTRIBUTIONS;MII_FUSION_STATE
allowed_next=RT.MORPHOLOGY_BIND|RT.UNCERTAINTY_RESOLVE|RT.ACTION|RT.DELIVER
invalidates=PRIOR_COGNITIVE_COVERAGE_WHEN_INPUT_OR_TASK_CHANGED
does_not_bypass=AIR-FLOOR-015;AIR-FLOOR-022;AIR-FLOOR-023;AIR-FLOOR-024
failure_route=RT.UNCERTAINTY_RESOLVE
'''
    new_route = '''[AIR_ROUTE]
id=RT.COGNITIVE_RESOLVE
semantic_owner=AIR_CORE_RUNTIME
trigger=task/input requires cognitive processing for benchmark execution
trigger_authority=NON_OPERATIVE_DESCRIPTION
control_event_ref=CE-RT-COGNITIVE_RESOLVE
requires=DEP.CANONICAL_INTENT;DEP.ACTIVE_CONTEXT;DEP.SOURCE_EVIDENCE_STATE;DEP.COMPLETION_ENVELOPE_RESOLVED;DEP.TARGET_READINESS_RESOLVED_WHEN_MATERIAL;DEP.COGNITIVE_SCOPE_DECLARED
produces=MII_COGNITIVE_ROUTE_SET;MII_CONTRIBUTIONS;MII_FUSION_STATE;COGNITIVE_SCOPE_CANDIDATE_CONTRIBUTIONS
allowed_next=RT.MORPHOLOGY_BIND|RT.UNCERTAINTY_RESOLVE|RT.ACTION|RT.DELIVER
invalidates=PRIOR_COGNITIVE_COVERAGE_WHEN_INPUT_OR_TASK_OR_SCOPE_CHANGED
does_not_bypass=AIR-FLOOR-015;AIR-FLOOR-022;AIR-FLOOR-023;AIR-FLOOR-024;AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION
cognitive_scope_contract=AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1
cognitive_scope_owner=AIR_ARTIFACT.execution_benchmark_profile.cognitive_scope
cognition_to_control=PROHIBITED
cognition_to_validation=CANDIDATE_CONTRIBUTION_ONLY
validated_ingestion=EXPLICIT_DECLARED_INGESTION_ONLY
failure_route=RT.UNCERTAINTY_RESOLVE
'''
    t = replace_once(t, old_route, new_route, 'Core RT.COGNITIVE_RESOLVE')
    p.write_text(t, encoding='utf-8')


def patch_control(root: Path) -> None:
    p = root / 'prompts/AIR_CONTROL_SURFACE.md'
    t = p.read_text(encoding='utf-8')
    t = replace_once(t, 'PROMPT_VERSION: 2.6.1', 'PROMPT_VERSION: 2.6.2', 'Control version')
    block = '''==================================================
COGNITIVE SCOPE AUTHORITY ISOLATION SURFACE LAW
==================================================

Patch marker: AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_SURFACE_V1
Floor invariant: AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION

Control renders the Core-owned cognitive scope when its boundary is material. It does not create a second cognitive authority system.

When material, the visible surface may show the scope objective, permitted input classes/routes/operations, candidate contribution state, validation-ingress state, held/rejected contribution references, and the protected control-state boundary. Do not expose or request private chain of thought.

A cognitive conclusion, however confident or useful, must never be rendered as if it directly changed task identity, Artifact/Orbit binding, deterministic route state, approval, Gate/Authorization/Receipt state, lease/scope pin, surfaced provenance, Handoff authority, or failure-registry authority. Those changes require their own Core-owned deterministic transition.

If COGNITIVE_AUTHORITY_ESCAPE is detected, show the affected protected state, keep the cognitive contribution non-operative, fail closed for the affected effect, and enter the Core recovery/failure-capture path. A validated contribution may be described as ingested only after the explicit declared ingestion boundary has accepted it.
'''
    anchor = '==================================================\nAMBIGUITY INTAKE POSTURE LAW\n==================================================\n'
    t = insert_before(t, anchor, block, 'AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_SURFACE_V1', 'Control cognitive surface')
    p.write_text(t, encoding='utf-8')


def patch_governance(root: Path) -> None:
    p = root / 'prompts/AIR_GOV.md'
    t = p.read_text(encoding='utf-8')
    t = replace_once(t, 'PROMPT_VERSION: 2.3.1', 'PROMPT_VERSION: 2.3.2', 'Governance version')
    block = '''==================================================
GOVERNANCE COGNITIVE SCOPE AUTHORITY ISOLATION LAW
==================================================

Patch marker: AIR_GOVERNANCE_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1
Floor invariant: AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION

Governance analysis may participate in a Core-declared cognitive scope as candidate contribution only. Governance findings, framework interpretations, risk judgments, policy mappings, or approval recommendations may not directly mutate protected Core control state.

A governance cognitive contribution becomes usable by a deterministic Core pipeline only through the active scope's explicit validation-ingress contract and declared ingestion boundary. Missing, stale, held, REVIEW, rejected, or out-of-scope contributions remain non-operative. Governance cannot authorize its own ingestion or redefine the protected-state set.
'''
    anchor = '==================================================\nGOVERNANCE EVIDENCE AND PRESENTATION SEPARATION LAW\n==================================================\n'
    t = insert_before(t, anchor, block, 'AIR_GOVERNANCE_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1', 'Governance cognitive boundary')
    p.write_text(t, encoding='utf-8')


def patch_starter(root: Path) -> None:
    p = root / 'prompts/AIR_DEFAULT_STARTER_PROFILE.json'
    o = load(p)
    o['PROMPT_VERSION'] = '2.6.2'
    fvc = o['validation_contract']['deterministic_contract_registry']['foundation_prompt_version_contract']
    fvc['CORE'] = '2.6.2'; fvc['CONTROL'] = '2.6.2'; fvc['GOVERNANCE'] = '2.3.2'
    floors = o['authority_contract']['floor_invariants_required']
    if FLOOR_028 not in floors:
        floors.append(FLOOR_028)

    cc = o['compiler_contract']
    cc['cognitive_scope_authority_isolation'] = {
        'required': True,
        'semantic_owner': 'AIR_CORE_RUNTIME_V2',
        'core_patch_marker': 'AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1',
        'floor_invariant': FLOOR_028,
        'scope_owner_path': 'AIR_ARTIFACT.execution_benchmark_profile.cognitive_scope',
        'control_to_cognition': 'DECLARED_SCOPE_ONLY',
        'cognition_to_control': 'PROHIBITED',
        'cognition_to_validation': 'CANDIDATE_CONTRIBUTION_ONLY',
        'validated_contribution_ingress': 'EXPLICIT_DECLARED_INGESTION_ONLY',
        'candidate_output_authority': 'NONE',
        'authority_escape_failure_class': 'COGNITIVE_AUTHORITY_ESCAPE',
        'protected_control_state_classes': [
            'TASK_AND_ARTIFACT_IDENTITY', 'ORBIT_AND_ARTIFACT_BINDING',
            'DETERMINISTIC_ROUTE_STATE', 'APPROVAL_SCOPE_AND_RESOLUTION',
            'GATE_AUTHORIZATION_RECEIPT_AND_AUTHORITY_LEDGER', 'LEASE_AND_RESOURCE_SCOPE_PIN',
            'SURFACED_OBJECT_PROVENANCE', 'HANDOFF_EXECUTION_OR_RESTORATION_AUTHORITY',
            'FAILURE_MODE_REGISTRY_AUTHORITY'
        ],
        'handoff_restore_authority': 'NONE_REVALIDATE_AND_REBIND',
        'hidden_reasoning_boundary': 'NO_PRIVATE_CHAIN_OF_THOUGHT_ACCESS_OR_EXPOSURE_CLAIMED',
    }
    mii = cc['mii_cognitive_routing']
    mii['cognitive_scope_authority_isolation_ref'] = 'AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1'
    mii['scope_owner_path'] = 'AIR_ARTIFACT.execution_benchmark_profile.cognitive_scope'
    mii['cognition_to_control'] = 'PROHIBITED'
    mii['validated_ingestion'] = 'EXPLICIT_DECLARED_INGESTION_ONLY'
    if not append_benchmark_requirement(o):
        raise SystemExit('Starter: REQ-MII-CONTRIBUTION-BOUNDARY anchor not found')

    events = {e['route_id']: e for e in cc['runtime_control_event_registry']['events']}
    cg = events['RT.COGNITIVE_RESOLVE']['guards']
    guard = {'operator': 'STATE_EQUALS', 'path': 'COGNITIVE_SCOPE_DECLARATION_STATE', 'expected': 'DECLARED_CURRENT'}
    if guard not in cg:
        cg.append(guard)

    dcr = o['validation_contract']['deterministic_contract_registry']
    checks = dcr['checks']
    ids = {c['check_id'] for c in checks}
    if 'DC-STARTER-FLOOR-028' not in ids:
        checks.append({
            'check_id': 'DC-STARTER-FLOOR-028',
            'operator': 'JSON_ARRAY_CONTAINS_LITERAL',
            'on_failure': 'FAIL_CLOSED',
            'file': 'prompts/AIR_DEFAULT_STARTER_PROFILE.json',
            'left': {'file': 'prompts/AIR_DEFAULT_STARTER_PROFILE.json', 'path': '$.authority_contract.floor_invariants_required'},
            'expected': FLOOR_028,
        })
    if 'DC-CORE-FLOOR-028' not in ids:
        checks.append({
            'check_id': 'DC-CORE-FLOOR-028',
            'operator': 'TEXT_CONTAINS_LITERAL',
            'on_failure': 'FAIL_CLOSED',
            'file': 'prompts/AIR_CORE_RUNTIME.md',
            'expected': FLOOR_028,
        })
    n = len(checks)
    cov = dcr['coverage_contract']
    cov['declared_check_count'] = n
    cov['implemented_check_count_required'] = n
    cov['executed_check_count_required'] = n
    if n != 82:
        raise SystemExit(f'Starter deterministic check count expected 82 after patch, got {n}')
    dump(p, o)


def patch_handoff(root: Path) -> None:
    p = root / 'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'
    doc = load(p); h = doc['AIR_HANDOFF_CARD']
    h['card_revision'] = 18
    h['profile_stack']['starter_profile']['PROMPT_VERSION'] = '2.6.2'
    h['governance_state']['governance_supplement_version'] = '2.3.2'
    h['execution_state']['cognitive_scope_state'] = {
        'scope_id': None,
        'scope_state': 'UNVALIDATED_BOOTSTRAP_INPUT',
        'scope_owner_artifact_ref': None,
        'objective': None,
        'permitted_input_refs': [],
        'permitted_route_ids': [],
        'permitted_cognitive_operations': [],
        'protected_control_state_classes': [],
        'candidate_contribution_refs': [],
        'validated_contribution_refs': [],
        'held_or_rejected_contribution_refs': [],
        'validation_ingress_state': 'NOT_EVALUATED',
        'positive_execution_authority': 'NONE',
        'restoration_rule': 'Restore declared scope identity and contribution references only as non-authorizing continuation input. Revalidate current task/Artifact scope, inputs, protected control state, contribution availability, and validation-ingress eligibility before operative reuse; never reconstruct hidden reasoning or infer prior control authority from a contribution.'
    }
    h['mii_state']['cognitive_scope_ref'] = 'AIR_HANDOFF_CARD.execution_state.cognitive_scope_state'

    sm = h['schema_manifest']
    scm = sm['schema_compatibility_contract']
    scm['card_revision_compatibility'] = 'REV18_SCHEMA_2_3_0_WITH_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_AND_MIGRATION_FROM_REV17_REV16_REV15_REV14_REV13_AND_SCHEMA_2_2_0_REV12_AND_EARLIER'
    scm['rev17_to_rev18_migration_contract_ref'] = 'AIR_HANDOFF_CARD.schema_manifest.revision_migration_contracts.REV17_TO_REV18'
    sm['revision_migration_contracts']['REV17_TO_REV18'] = {
        'source_schema_version': '2.3.0',
        'source_card_revision': 17,
        'target_schema_version': '2.3.0',
        'target_card_revision': 18,
        'apply_before_current_required_carrier_check': True,
        'nested_additions': {
            'execution_state': ['cognitive_scope_state'],
            'mii_state': ['cognitive_scope_ref']
        },
        'cognitive_scope_migration_rule': 'ADD_SAFE_NONAUTHORIZING_UNVALIDATED_SCOPE_DEFAULTS; PRESERVE_ONLY_EXPLICIT_SUPPORTED_CONTRIBUTION_REFERENCES; NEVER_RECONSTRUCT_HIDDEN_REASONING_OR_CONTROL_AUTHORITY',
        'history_synthesis': 'PROHIBITED'
    }
    cr = h['migration_state']['compatibility_rules']
    cr['v2_3_rev17_to_rev18_cognitive_scope_authority_isolation'] = 'Rev17 cards remain valid schema-2.3.0 migration input. Add the cognitive-scope carrier with non-authorizing unresolved defaults and a stable MII reference. Preserve explicit supported contribution references only; do not reconstruct hidden reasoning, validated ingestion, or control authority. Require current HANDOFF_RESTORE alignment and Artifact rebinding.'
    h['migration_state']['revision_migration_path'] = None
    dump(p, doc)


def patch_readme(root: Path) -> None:
    p = root / 'README.md'; t = p.read_text(encoding='utf-8')
    marker = '**Cognitive scope authority isolation.**'
    if marker not in t:
        anchor = '### Best practices\n'
        block = ('**Cognitive scope authority isolation.** AIR v0.7.2 keeps adaptive reasoning inside the current task Artifact\'s declared cognitive scope. Cognitive findings are candidate contributions, not control state: they cannot directly change task/Artifact identity, deterministic routing, approval, Gate/Authorization/Receipt state, lease/scope pin, Handoff authority, or failure-registry authority. A contribution becomes operative only after the declared validation and ingestion boundary accepts it. This is an authority boundary, not a request for or exposure of private chain of thought.\n\n')
        if anchor not in t:
            raise SystemExit('README Best practices anchor missing')
        t = t.replace(anchor, anchor + '\n' + block, 1)
    p.write_text(t, encoding='utf-8')


def patch_fixtures(root: Path) -> None:
    p = root / 'tests/air_contract_fixtures.json'; o = current_transform(load(p))
    o['fixture_set'] = 'AIR_SET007_REGRESSION_FIXTURES_V1'
    o['foundation_identity'] = NEW_FOUNDATION
    o['cognitive_scope_authority_cases'] = [
        {'id':'CSA-01-DIRECT-TASK-IDENTITY-MUTATION','kind':'NEGATIVE','invalid_if':'cognitive contribution directly changes current task or Artifact identity'},
        {'id':'CSA-02-DIRECT-ORBIT-BINDING-MUTATION','kind':'NEGATIVE','invalid_if':'cognitive contribution directly changes Orbit placement or binding state'},
        {'id':'CSA-03-DIRECT-APPROVAL-MUTATION','kind':'NEGATIVE','invalid_if':'cognitive conclusion creates, changes, or consumes approval scope/token state'},
        {'id':'CSA-04-DIRECT-GATE-AUTH-RECEIPT-MUTATION','kind':'NEGATIVE','invalid_if':'cognition directly creates or changes Gate Authorization Receipt or authority-ledger state'},
        {'id':'CSA-05-DIRECT-LEASE-SCOPE-PIN-MUTATION','kind':'NEGATIVE','invalid_if':'cognition directly changes Artifact lease or resource scope pin'},
        {'id':'CSA-06-DETERMINISTIC-ROUTE-REORDER','kind':'NEGATIVE','invalid_if':'cognitive optimization reorders or supplies deterministic route state'},
        {'id':'CSA-07-SURFACED-PROVENANCE-MUTATION','kind':'NEGATIVE','invalid_if':'cognitive output fabricates or mutates surfaced-object provenance'},
        {'id':'CSA-08-FAILURE-REGISTRY-MUTATION','kind':'NEGATIVE','invalid_if':'cognitive output directly mutates failure-mode registry authority/applicability'},
        {'id':'CSA-P01-VALIDATED-EXPLICIT-INGESTION','kind':'POSITIVE','valid_when':'in-scope candidate contribution passes declared validation and enters task/Artifact state only through explicit ingestion'},
        {'id':'CSA-P02-HANDOFF-NONAUTHORITY','kind':'POSITIVE','valid_when':'Handoff preserves scope/contribution refs as non-authorizing input and current session revalidates before reuse'}
    ]
    dump(p, o)

    p = root / 'tests/deterministic_contract_inventory.json'; inv = current_transform(load(p))
    inv['inventory_id'] = 'AIR_SET007_DETERMINISTIC_CONTRACT_INVENTORY_V1'
    inv['foundation_identity'] = NEW_FOUNDATION
    inv['typed_deterministic_check_count'] = 82
    inv['r072_cognitive_scope_added_coverage'] = [
        FLOOR_028 + ' required in Starter authority contract',
        FLOOR_028 + ' required in Core canonical floor registry'
    ]
    dump(p, inv)

    p = root / 'tests/r1_remediation_fixtures.json'; r1 = load(p)
    for x in r1['positive_cases']:
        if x['id'] == 'R1-P01-DETERMINISTIC-SETS': x['expect'] = 'Core closed set == Core deterministic metadata == Starter set == Route Map set == 10 routes'
        if x['id'] == 'R1-P06-FOUNDATION-REGISTRY': x['expect'] = '82 declared/implemented/executed typed checks, zero gaps, including Floor 028 Core and Starter membership'
    if not any(x.get('id') == 'R1-N15-COGNITIVE-SCOPE-FLOOR-MISSING' for x in r1['negative_cases']):
        r1['negative_cases'].append({'id':'R1-N15-COGNITIVE-SCOPE-FLOOR-MISSING','mutation':'remove AIR-FLOOR-028 canonical identifier from Core','must_fail':'DC-CORE-FLOOR-028'})
    dump(p, r1)

    p = root / 'tests/r3_remediation_fixtures.json'; r3 = load(p)
    for x in r3['positive_cases']:
        if x['id'] == 'R3-P03-REV15-MIGRATION': x['expect'] = 'published v0.7.0 rev15 card migrates through rev16 and rev17 to rev18 before current carrier checks without fabricated history or cognitive authority'
    r3['negative_cases'] = [f'R3-N{i:02d}-' for i in range(1, 19)]
    dump(p, r3)


def patch_migration_tool(root: Path) -> None:
    p = root / 'tools/migrate_air_handoff.py'; t = p.read_text(encoding='utf-8')
    if 'def migrate_rev17_to_rev18' not in t:
        anchor = '\ndef migrate_to_current(doc: dict[str,Any], current_template_doc: dict[str,Any])->dict[str,Any]:\n'
        fn = r'''

def migrate_rev17_to_rev18(doc: dict[str,Any], current_template_doc: dict[str,Any])->dict[str,Any]:
    if set(doc)!= {'AIR_HANDOFF_CARD'}: raise MigrationError('expected exactly one AIR_HANDOFF_CARD root')
    if set(current_template_doc)!= {'AIR_HANDOFF_CARD'}: raise MigrationError('current template root invalid')
    src=doc['AIR_HANDOFF_CARD']; tmpl=current_template_doc['AIR_HANDOFF_CARD']
    if src.get('schema_version')!='2.3.0' or src.get('SCHEMA_VERSION')!='2.3.0': raise MigrationError('source is not schema 2.3.0')
    if src.get('card_revision')!=17: raise MigrationError('source card_revision is not 17')
    contract=tmpl.get('schema_manifest',{}).get('revision_migration_contracts',{}).get('REV17_TO_REV18')
    if not contract or contract.get('apply_before_current_required_carrier_check') is not True: raise MigrationError('current rev18 migration contract missing')
    out=copy.deepcopy(doc); c=out['AIR_HANDOFF_CARD']; c['card_revision']=18
    c.setdefault('execution_state',{}).setdefault('cognitive_scope_state',copy.deepcopy(tmpl['execution_state']['cognitive_scope_state']))
    c.setdefault('mii_state',{}).setdefault('cognitive_scope_ref',tmpl['mii_state']['cognitive_scope_ref'])
    cs=c['execution_state']['cognitive_scope_state']
    if not isinstance(cs,dict): raise MigrationError('cognitive_scope_state is not an object')
    cs['positive_execution_authority']='NONE'
    if cs.get('scope_state') not in (None,'UNVALIDATED_BOOTSTRAP_INPUT'):
        cs['scope_state']='UNVALIDATED_BOOTSTRAP_INPUT'
    cs['validation_ingress_state']='NOT_EVALUATED'
    old_ms=c.get('migration_state') if isinstance(c.get('migration_state'),dict) else {}
    ms=copy.deepcopy(tmpl['migration_state'])
    if isinstance(old_ms,dict):
        for k in ['legacy_q4_c_state','legacy_q4_d_state','legacy_prompt_mode_state','legacy_orbit_state','legacy_active_contract_state','legacy_governance_state','unresolved_legacy_states','legacy_history_state']:
            if k in old_ms: ms[k]=copy.deepcopy(old_ms[k])
    ms['source_schema_version']='2.3.0'; ms['source_card_revision']=17; ms['migration_required']=True
    ms['migration_decision']='MIGRATED_REV17_TO_REV18_PENDING_CURRENT_ALIGNMENT_REBINDING_AND_COGNITIVE_SCOPE_REVALIDATION'
    ms['revision_migration_path']='REV17_TO_REV18'
    ms['source_schema_manifest_sha256']=canonical_sha(src.get('schema_manifest',{}))
    c['migration_state']=ms; c['schema_manifest']=copy.deepcopy(tmpl['schema_manifest'])
    required=set(tmpl['schema_manifest']['required_fields']); missing=sorted(required-set(c))
    if missing: raise MigrationError('rev17 input missing current required root carriers after declared migration: '+', '.join(missing))
    return out
'''
        if anchor not in t:
            raise SystemExit('migration insertion anchor missing')
        t = t.replace(anchor, fn + anchor, 1)
    old = '''def migrate_to_current(doc: dict[str,Any], current_template_doc: dict[str,Any])->dict[str,Any]:
    rev=doc.get('AIR_HANDOFF_CARD',{}).get('card_revision')
    if rev==15:
        mid=migrate_rev15_to_rev16(doc,current_template_doc)
        return migrate_rev16_to_rev17(mid,current_template_doc)
    if rev==16:
        return migrate_rev16_to_rev17(doc,current_template_doc)
    if rev==17:
        return copy.deepcopy(doc)
    raise MigrationError(f'unsupported source card_revision {rev!r}')
'''
    new = '''def migrate_to_current(doc: dict[str,Any], current_template_doc: dict[str,Any])->dict[str,Any]:
    rev=doc.get('AIR_HANDOFF_CARD',{}).get('card_revision')
    if rev==15:
        mid=migrate_rev15_to_rev16(doc,current_template_doc)
        mid2=migrate_rev16_to_rev17(mid,current_template_doc)
        return migrate_rev17_to_rev18(mid2,current_template_doc)
    if rev==16:
        mid=migrate_rev16_to_rev17(doc,current_template_doc)
        return migrate_rev17_to_rev18(mid,current_template_doc)
    if rev==17:
        return migrate_rev17_to_rev18(doc,current_template_doc)
    if rev==18:
        return copy.deepcopy(doc)
    raise MigrationError(f'unsupported source card_revision {rev!r}')
'''
    t = replace_once(t, old, new, 'migrate_to_current rev18')
    p.write_text(t, encoding='utf-8')


def patch_r1_validator(root: Path) -> None:
    p = root / 'tools/validate_air_r1_remediation.py'; t = p.read_text(encoding='utf-8')
    t = replace_once(t, "req(n==80,f'expected 80 deterministic checks, got {n}')", "req(n==82,f'expected 82 deterministic checks, got {n}')", 'R1 check count')
    old = "for x in ['DC-VERSION-CORE','DC-VERSION-CONTROL','DC-VERSION-GOV','DC-KIND-STARTER','DC-FUNCTION-CLASS-STARTER','DC-FILENAME-STARTER','DC-STRICT-JSON-STARTER','DC-STRICT-JSON-HANDOFF','DC-FOUNDATION-MANIFEST-EXACT','DC-FOUNDATION-NORMALIZED-COLLISION']:\n        req(x in ids,f'missing deterministic check {x}')"
    new = "for x in ['DC-VERSION-CORE','DC-VERSION-CONTROL','DC-VERSION-GOV','DC-KIND-STARTER','DC-FUNCTION-CLASS-STARTER','DC-FILENAME-STARTER','DC-STRICT-JSON-STARTER','DC-STRICT-JSON-HANDOFF','DC-FOUNDATION-MANIFEST-EXACT','DC-FOUNDATION-NORMALIZED-COLLISION','DC-STARTER-FLOOR-028','DC-CORE-FLOOR-028']:\n        req(x in ids,f'missing deterministic check {x}')"
    t = replace_once(t, old, new, 'R1 floor028 check ids')
    p.write_text(t, encoding='utf-8')


def patch_boot_validator(root: Path) -> None:
    p = root / 'tools/validate_air_boot.py'; t = p.read_text(encoding='utf-8')
    t = replace_once(t, "require(executed == 80, f'R1 deterministic boot registry expected 80 checks, got {executed}')", "require(executed == 82, f'R1 deterministic boot registry expected 82 checks, got {executed}')", 'boot check count')
    p.write_text(t, encoding='utf-8')


def patch_release_validator(root: Path) -> None:
    p = root / 'tools/validate_air_release.py'; t = p.read_text(encoding='utf-8')
    reps = [
        ("EXPECTED_FOUNDATION_ID = 'AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006'", "EXPECTED_FOUNDATION_ID = 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'"),
        ("EXPECTED_ROUTE_MAP_VERSION = '1.2.0'", "EXPECTED_ROUTE_MAP_VERSION = '1.2.1'"),
        ("EXPECTED_INDEX_VERSION = '1.3.1'", "EXPECTED_INDEX_VERSION = '1.3.2'"),
        ('EXPECTED_HANDOFF_CARD_REVISION = 17', 'EXPECTED_HANDOFF_CARD_REVISION = 18'),
        ("'AIR_CORE_RUNTIME.md': '2.6.1'", "'AIR_CORE_RUNTIME.md': '2.6.2'"),
        ("'AIR_CONTROL_SURFACE.md': '2.6.1'", "'AIR_CONTROL_SURFACE.md': '2.6.2'"),
        ("'AIR_GOV.md': '2.3.1'", "'AIR_GOV.md': '2.3.2'"),
        ("'AIR_DEFAULT_STARTER_PROFILE.json': '2.6.1'", "'AIR_DEFAULT_STARTER_PROFILE.json': '2.6.2'"),
        ("'AIR_RUNTIME_ROUTE_MAP.json': '1.2.0'", "'AIR_RUNTIME_ROUTE_MAP.json': '1.2.1'"),
        ("R7_INDEX_COMPLETENESS = 'COMPLETE_FOR_AIR_2_6_1_OBJECT_CONTRACT_SET_006_V072_CANDIDATE_SPECIALIST_CATALOG'", "R7_INDEX_COMPLETENESS = 'COMPLETE_FOR_AIR_2_6_2_OBJECT_CONTRACT_SET_007_V072_CANDIDATE_SPECIALIST_CATALOG'"),
        ("R7_STATIC_PASS = 'PASS_R7_DETERMINISTIC_STATIC_SUITE'", "R7_STATIC_PASS = 'PASS_R7_DETERMINISTIC_STATIC_SUITE'"),
        ("require('PROMPT_VERSION: 2.6.1' in core", "require('PROMPT_VERSION: 2.6.2' in core"),
        ("require('PROMPT_VERSION: 2.6.1' in control", "require('PROMPT_VERSION: 2.6.2' in control"),
        ("require('PROMPT_VERSION: 2.3.1' in gov", "require('PROMPT_VERSION: 2.3.2' in gov"),
        ("require(starter['PROMPT_VERSION'] == '2.6.1'", "require(starter['PROMPT_VERSION'] == '2.6.2'"),
        ("AIR_SET006_DETERMINISTIC_CONTRACT_INVENTORY_V1", "AIR_SET007_DETERMINISTIC_CONTRACT_INVENTORY_V1"),
        ("AIR_SET006_REGRESSION_FIXTURES_V1", "AIR_SET007_REGRESSION_FIXTURES_V1"),
    ]
    for old, new in reps:
        if old != new:
            t = replace_once(t, old, new, 'release validator '+old[:32])
    marker = "    require('Patch marker: AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1' in control, 'missing v0.7.2 primary response surface law')\n"
    extra = marker + "    require('Patch marker: AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1' in core, 'missing cognitive scope authority isolation law')\n    require('Patch marker: AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_SURFACE_V1' in control, 'missing cognitive scope surface law')\n    require('Patch marker: AIR_GOVERNANCE_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1' in gov, 'missing governance cognitive scope law')\n    require(starter.get('compiler_contract', {}).get('cognitive_scope_authority_isolation', {}).get('required') is True, 'Starter cognitive scope contract missing')\n"
    if 'missing cognitive scope authority isolation law' not in t:
        t = replace_once(t, marker, extra, 'release cognitive checks')
    p.write_text(t, encoding='utf-8')


def patch_r7_validator(root: Path) -> None:
    p = root / 'tools/validate_air_r7_remediation.py'; t = p.read_text(encoding='utf-8')
    t = t.replace(OLD_FOUNDATION, NEW_FOUNDATION).replace(OLD_SHORT, NEW_SHORT).replace(OLD_SET, NEW_SET)
    stale = "    req('OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_AIR_2_5_0_MII_CANDIDATE_SET_005' not in v,f'{p}:{\".\".join(loc)} old operative Foundation identity')\n"
    if 'stale SET_006 operative Foundation identity' not in t and stale in t:
        t = t.replace(stale, stale + "    req('OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006' not in v,f'{p}:{\".\".join(loc)} stale SET_006 operative Foundation identity')\n", 1)
    p.write_text(t, encoding='utf-8')


def patch_r3_validator(root: Path) -> None:
    p = root / 'tools/validate_air_r3_remediation.py'; t = p.read_text(encoding='utf-8')
    t = replace_once(t, "req(len(starter['validation_contract']['deterministic_contract_registry']['checks'])==80,'R1 registry lost')", "req(len(starter['validation_contract']['deterministic_contract_registry']['checks'])==82,'R1 registry lost')", 'R3 registry count')
    old = "rc=sm['revision_migration_contracts']['REV15_TO_REV16']; req(rc['apply_before_current_required_carrier_check'] is True,'072 order flag false'); rc17=sm['revision_migration_contracts']['REV16_TO_REV17']; req(rc17['apply_before_current_required_carrier_check'] is True,'v072 rev16->17 order flag false'); req(rc17['history_synthesis']=='PROHIBITED','v072 rev16->17 history synthesis not prohibited'); seq=sm['validation_sequence']; req(seq.index('source card revision detection and applicable revision migration check') < seq.index('required-carrier check after applicable migration'),'072 sequence migration after required carriers'); req(rc['history_synthesis']=='PROHIBITED','072 history synthesis not prohibited')"
    new = "rc=sm['revision_migration_contracts']['REV15_TO_REV16']; req(rc['apply_before_current_required_carrier_check'] is True,'072 order flag false'); rc17=sm['revision_migration_contracts']['REV16_TO_REV17']; req(rc17['apply_before_current_required_carrier_check'] is True,'v072 rev16->17 order flag false'); req(rc17['history_synthesis']=='PROHIBITED','v072 rev16->17 history synthesis not prohibited'); rc18=sm['revision_migration_contracts']['REV17_TO_REV18']; req(rc18['apply_before_current_required_carrier_check'] is True,'v072 rev17->18 order flag false'); req(rc18['history_synthesis']=='PROHIBITED','v072 rev17->18 history synthesis not prohibited'); seq=sm['validation_sequence']; req(seq.index('source card revision detection and applicable revision migration check') < seq.index('required-carrier check after applicable migration'),'072 sequence migration after required carriers'); req(rc['history_synthesis']=='PROHIBITED','072 history synthesis not prohibited')"
    t = replace_once(t, old, new, 'R3 rev18 contract')
    t = replace_once(t, "req(migrated['card_revision']==17,'072 target rev')", "req(migrated['card_revision']==18,'072 target rev')", 'R3 target rev18')
    t = replace_once(t, "req(migrated['migration_state']['migration_decision'].startswith('MIGRATED_REV16_TO_REV17'),'072 migration decision')", "req(migrated['migration_state']['migration_decision'].startswith('MIGRATED_REV17_TO_REV18'),'072 migration decision'); req(migrated['execution_state']['cognitive_scope_state']['positive_execution_authority']=='NONE','v072 migrated cognitive scope gained authority'); req(migrated['execution_state']['cognitive_scope_state']['validation_ingress_state']=='NOT_EVALUATED','v072 migrated cognitive scope fabricated validation')", 'R3 cognitive migration check')
    p.write_text(t, encoding='utf-8')


def patch_r3_mutations(root: Path) -> None:
    p = root / 'tools/test_air_r3_mutations.py'; t = p.read_text(encoding='utf-8')
    if 'R3-N17-REV17-TO-REV18-MIGRATION-ORDER' not in t:
        anchor = "    cases.append(('R3-N16-APPROVAL-FINGERPRINT-VALIDATION', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['validation_registry']['allowed_operators'].remove('APPROVAL_SCOPE_IDENTITY_FINGERPRINT_VALID'))))\n"
        extra = anchor + "    cases.append(('R3-N17-REV17-TO-REV18-MIGRATION-ORDER', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['revision_migration_contracts']['REV17_TO_REV18'].__setitem__('apply_before_current_required_carrier_check',False))))\n    cases.append(('R3-N18-COGNITIVE-SCOPE-AUTHORITY', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['execution_state']['cognitive_scope_state'].__setitem__('positive_execution_authority','ALLOW'))))\n"
        t = replace_once(t, anchor, extra, 'R3 mutation rev18')
    p.write_text(t, encoding='utf-8')


def patch_behavioral_validator(root: Path) -> None:
    p = root / 'tools/validate_air_behavioral_contracts.py'; t = p.read_text(encoding='utf-8')
    t = replace_once(t, "        'AIR_NEW_TASK_BINDING_TRANSACTION_V2',\n", "        'AIR_NEW_TASK_BINDING_TRANSACTION_V2',\n        'AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1',\n", 'behavioral Core marker')
    t = replace_once(t, "        'AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1',\n", "        'AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1',\n        'AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_SURFACE_V1',\n", 'behavioral Control marker')
    anchor = "    require(nt.get('direct_action_or_material_delivery_before_completion') == 'PROHIBITED', 'new-task direct execution bypass allowed')\n"
    extra = anchor + "    cs=cc.get('cognitive_scope_authority_isolation', {})\n    require(cs.get('required') is True and cs.get('cognition_to_control') == 'PROHIBITED', 'cognitive scope authority isolation missing')\n    require(cs.get('validated_contribution_ingress') == 'EXPLICIT_DECLARED_INGESTION_ONLY', 'cognitive scope ingestion boundary missing')\n    require(cs.get('authority_escape_failure_class') == 'COGNITIVE_AUTHORITY_ESCAPE', 'cognitive authority escape failure class missing')\n"
    if 'cognitive scope authority isolation missing' not in t:
        t = replace_once(t, anchor, extra, 'behavioral cognitive contract')
    fixture_anchor = "    prs={x.get('id') for x in fixtures.get('primary_response_surface_cases', [])}; require('PRS-01-COLLAPSED-HOST-SURFACE-NOT-EMISSION' in prs, 'primary surface fixture missing')\n"
    fixture_extra = fixture_anchor + "    csa={x.get('id') for x in fixtures.get('cognitive_scope_authority_cases', [])}; require({'CSA-01-DIRECT-TASK-IDENTITY-MUTATION','CSA-03-DIRECT-APPROVAL-MUTATION','CSA-06-DETERMINISTIC-ROUTE-REORDER','CSA-P01-VALIDATED-EXPLICIT-INGESTION','CSA-P02-HANDOFF-NONAUTHORITY'} <= csa, 'cognitive scope fixtures missing')\n"
    if 'cognitive scope fixtures missing' not in t:
        t = replace_once(t, fixture_anchor, fixture_extra, 'behavioral cognitive fixtures')
    p.write_text(t, encoding='utf-8')


def patch_behavioral_mutations(root: Path) -> None:
    p = root / 'tools/test_air_behavioral_contract_mutations.py'; t = p.read_text(encoding='utf-8')
    if 'mutate_cognitive_scope_control' not in t:
        anchor = '\n\nMUTATIONS = [\n'
        funcs = '''\n\ndef mutate_cognitive_scope_control(root: Path):\n    p=root/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; x=load(p)\n    x['compiler_contract']['cognitive_scope_authority_isolation']['cognition_to_control']='ALLOWED'; dump(p,x)\n\ndef mutate_cognitive_scope_ingress(root: Path):\n    p=root/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; x=load(p)\n    x['compiler_contract']['cognitive_scope_authority_isolation']['validated_contribution_ingress']='IMPLICIT'; dump(p,x)\n'''
        t = t.replace(anchor, funcs + anchor, 1)
        t = replace_once(t, "    ('new_task_route_determinism', mutate_new_task_route_determinism),\n", "    ('new_task_route_determinism', mutate_new_task_route_determinism),\n    ('cognitive_scope_control', mutate_cognitive_scope_control),\n    ('cognitive_scope_ingress', mutate_cognitive_scope_ingress),\n", 'behavioral mutation list')
    p.write_text(t, encoding='utf-8')


def patch_control_validator(root: Path) -> None:
    p = root / 'tools/validate_air_control_plane.py'; t = p.read_text(encoding='utf-8')
    anchor = "    req('approval_scope_fingerprint' in gov, 'v0.7.2 approval fingerprint governance missing')\n"
    extra = anchor + "    req('AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1' in core, 'cognitive scope Core law missing')\n    req('AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_SURFACE_V1' in control, 'cognitive scope Control law missing')\n    req('AIR_GOVERNANCE_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1' in gov, 'cognitive scope Governance law missing')\n"
    if 'cognitive scope Core law missing' not in t:
        t = replace_once(t, anchor, extra, 'control validator cognitive markers')
    anchor2 = "    nt=cc.get('new_task_binding_transaction',{}); req(nt.get('required') is True and nt.get('inference_policy')=='PROHIBITED_AFTER_NEW_TASK_BOUNDARY_LATCH','new-task typed transaction missing')\n"
    extra2 = anchor2 + "    cs=cc.get('cognitive_scope_authority_isolation',{}); req(cs.get('required') is True and cs.get('cognition_to_control')=='PROHIBITED','cognitive scope control boundary missing'); req(cs.get('validated_contribution_ingress')=='EXPLICIT_DECLARED_INGESTION_ONLY','cognitive scope ingestion boundary missing'); req(cs.get('candidate_output_authority')=='NONE','cognitive candidates gained authority')\n"
    if 'cognitive scope control boundary missing' not in t:
        t = replace_once(t, anchor2, extra2, 'control validator cognitive contract')
    anchor3 = "    sm=handoff['schema_manifest']; req(sm['strict_output_mode']=='DOWNLOADABLE_JSON_FILE_ONLY','handoff is not file-only');"
    extra3 = "    cs_h=handoff['execution_state']['cognitive_scope_state']; req(cs_h['positive_execution_authority']=='NONE' and cs_h['validation_ingress_state']=='NOT_EVALUATED','handoff cognitive scope gained authority or fabricated validation')\n" + anchor3
    if 'handoff cognitive scope gained authority' not in t:
        t = replace_once(t, anchor3, extra3, 'control validator handoff cognitive')
    p.write_text(t, encoding='utf-8')


def patch_control_mutations(root: Path) -> None:
    p = root / 'tools/test_air_control_plane_mutations.py'; t = p.read_text(encoding='utf-8')
    if 'cognitive contribution gains control authority' not in t:
        anchor = "    cases.append(('execution defect failure capture removed',m24))\n"
        extra = anchor + "    def m25(d):\n        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['cognitive_scope_authority_isolation']['cognition_to_control']='ALLOWED'; save(p,o)\n    cases.append(('cognitive contribution gains control authority',m25))\n    def m26(d):\n        p=d/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; o=load(p); o['AIR_HANDOFF_CARD']['execution_state']['cognitive_scope_state']['positive_execution_authority']='ALLOW'; save(p,o)\n    cases.append(('handoff cognitive scope gains authority',m26))\n"
        t = replace_once(t, anchor, extra, 'control cognitive mutations')
    p.write_text(t, encoding='utf-8')


def patch_v072_validator(root: Path) -> None:
    p = root / 'tools/validate_air_v072_release_seal.py'; t = p.read_text(encoding='utf-8')
    reps = [
        ("FOUNDATION='AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006'", "FOUNDATION='AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'"),
        ("STATUS='AIR_2_6_1_OBJECT_CONTRACT_SET_006_FIVE_PACKAGE_INDEX_V072_CANDIDATE_STATIC_VALIDATED'", "STATUS='AIR_2_6_2_OBJECT_CONTRACT_SET_007_FIVE_PACKAGE_INDEX_V072_CANDIDATE_STATIC_VALIDATED'"),
        ("COMPLETE='COMPLETE_FOR_AIR_2_6_1_OBJECT_CONTRACT_SET_006_V072_CANDIDATE_SPECIALIST_CATALOG'", "COMPLETE='COMPLETE_FOR_AIR_2_6_2_OBJECT_CONTRACT_SET_007_V072_CANDIDATE_SPECIALIST_CATALOG'"),
        ("req('PROMPT_VERSION: 2.6.1' in core,'Core not 2.6.1')", "req('PROMPT_VERSION: 2.6.2' in core,'Core not 2.6.2')"),
        ("req('PROMPT_VERSION: 2.6.1' in control,'Control not 2.6.1')", "req('PROMPT_VERSION: 2.6.2' in control,'Control not 2.6.2')"),
        ("req('PROMPT_VERSION: 2.3.1' in gov,'Governance not 2.3.1')", "req('PROMPT_VERSION: 2.3.2' in gov,'Governance not 2.3.2')"),
        ("req(starter['PROMPT_VERSION']=='2.6.1','Starter not 2.6.1')", "req(starter['PROMPT_VERSION']=='2.6.2','Starter not 2.6.2')"),
        ("req(card['schema_version']=='2.3.0' and card['card_revision']==17,'Handoff not schema 2.3.0 rev17')", "req(card['schema_version']=='2.3.0' and card['card_revision']==18,'Handoff not schema 2.3.0 rev18')"),
        ("req(rmap['MAP_VERSION']=='1.2.0','Route Map not 1.2.0')", "req(rmap['MAP_VERSION']=='1.2.1','Route Map not 1.2.1')"),
        ("req(idx['INDEX_VERSION']=='1.3.1','Index not 1.3.1')", "req(idx['INDEX_VERSION']=='1.3.2','Index not 1.3.2')"),
        ("req(fx['foundation_identity']==FOUNDATION,'fixtures Foundation stale')", "req(fx['foundation_identity']==FOUNDATION,'fixtures Foundation stale')"),
        ("print('handoff_revision',17)", "print('handoff_revision',18)"),
    ]
    for old, new in reps:
        if old != new:
            t = replace_once(t, old, new, 'v072 validator '+old[:30])
    marker = "    req('AIR_NEW_TASK_BINDING_TRANSACTION_V2' in core,'new-task binding transaction absent'); req('AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1' in control,'primary response surface law absent'); req('approval_scope_fingerprint' in gov,'approval fingerprint governance absent')\n"
    extra = marker + "    req('AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1' in core,'cognitive scope Core law absent'); req('AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_SURFACE_V1' in control,'cognitive scope Control law absent'); req('AIR_GOVERNANCE_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1' in gov,'cognitive scope Governance law absent'); req(starter['compiler_contract']['cognitive_scope_authority_isolation']['cognition_to_control']=='PROHIBITED','cognitive scope control boundary invalid'); req(card['execution_state']['cognitive_scope_state']['positive_execution_authority']=='NONE','Handoff cognitive scope authority invalid')\n"
    if 'cognitive scope Core law absent' not in t:
        t = replace_once(t, marker, extra, 'v072 cognitive checks')
    fixture = "req(len(fx.get('repository_patch_reconciliation_cases',[]))>=2,'repo reconciliation fixtures incomplete')"
    if 'cognitive scope fixtures incomplete' not in t:
        t = replace_once(t, fixture, fixture + "; req(len(fx.get('cognitive_scope_authority_cases',[]))>=10,'cognitive scope fixtures incomplete')", 'v072 fixture check')
    p.write_text(t, encoding='utf-8')


def patch_v072_mutations(root: Path) -> None:
    p = root / 'tools/test_air_v072_release_seal_mutations.py'; t = p.read_text(encoding='utf-8')
    if 'V072-N06-COGNITIVE-SCOPE-CONTROL' not in t:
        anchor = "    add('V072-N05-PRIMARY-SURFACE-REMOVED',m5)\n"
        extra = anchor + "    def m6(d): p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['cognitive_scope_authority_isolation']['cognition_to_control']='ALLOWED'; dump(p,o)\n    add('V072-N06-COGNITIVE-SCOPE-CONTROL',m6)\n    def m7(d): p=d/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; o=load(p); o['AIR_HANDOFF_CARD']['execution_state']['cognitive_scope_state']['positive_execution_authority']='ALLOW'; dump(p,o)\n    add('V072-N07-HANDOFF-COGNITIVE-AUTHORITY',m7)\n"
        t = replace_once(t, anchor, extra, 'v072 mutation cognitive cases')
    p.write_text(t, encoding='utf-8')


def patch_route_map(root: Path) -> None:
    p = root / 'catalog/AIR_RUNTIME_ROUTE_MAP.json'; o = load(p)
    o['MAP_VERSION'] = '1.2.1'
    o['source_of_truth']['prompt_version'] = '2.6.2'
    rule = 'cognitive_scope_authority_isolation mirrors Core AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1; cognition is scope-bounded candidate production only, has no direct control authority, and validated contributions enter task/Artifact state only through an explicit declared ingestion boundary.'
    if rule not in o['rules']:
        o['rules'].append(rule)
    r = next(x for x in o['routes'] if x['route_id'] == 'RT.COGNITIVE_RESOLVE')
    if 'DEP.COGNITIVE_SCOPE_DECLARED' not in r['requires']:
        r['requires'].append('DEP.COGNITIVE_SCOPE_DECLARED')
    if 'COGNITIVE_SCOPE_CANDIDATE_CONTRIBUTIONS' not in r['produces']:
        r['produces'].append('COGNITIVE_SCOPE_CANDIDATE_CONTRIBUTIONS')
    if FLOOR_028 not in r['does_not_bypass']:
        r['does_not_bypass'].append(FLOOR_028)
    r['invalidates'] = ['PRIOR_COGNITIVE_COVERAGE_WHEN_INPUT_OR_TASK_OR_SCOPE_CHANGED']
    r['cognitive_scope_contract'] = {
        'contract': 'AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1',
        'scope_owner': 'AIR_ARTIFACT.execution_benchmark_profile.cognitive_scope',
        'control_to_cognition': 'DECLARED_SCOPE_ONLY',
        'cognition_to_control': 'PROHIBITED',
        'cognition_to_validation': 'CANDIDATE_CONTRIBUTION_ONLY',
        'validated_ingestion': 'EXPLICIT_DECLARED_INGESTION_ONLY',
        'authority_escape_failure_class': 'COGNITIVE_AUTHORITY_ESCAPE'
    }
    core = root / 'prompts/AIR_CORE_RUNTIME.md'
    core_text = core.read_text(encoding='utf-8')
    o['source_of_truth']['sha256'] = hashlib.sha256(core.read_bytes()).hexdigest()
    line_by = {ln.split('=', 1)[1]: i for i, ln in enumerate(core_text.splitlines(), 1) if ln.startswith('id=RT.')}
    for rr in o['routes']:
        rr['source_anchor']['line'] = line_by[rr['route_id']]
    dump(p, o)


def patch_profiles(root: Path) -> None:
    for p in sorted((root / 'profiles').glob('**/*.json')):
        o = current_transform(load(p)); update_dependency_versions(o); dump(p, o)


def patch_index(root: Path) -> None:
    p = root / 'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'; o = current_transform(load(p)); update_dependency_versions(o)
    o['INDEX_VERSION'] = '1.3.2'
    o['status'] = 'AIR_2_6_2_OBJECT_CONTRACT_SET_007_FIVE_PACKAGE_INDEX_V072_CANDIDATE_STATIC_VALIDATED'
    o['catalog_scope']['catalog_completeness_claim'] = 'COMPLETE_FOR_AIR_2_6_2_OBJECT_CONTRACT_SET_007_V072_CANDIDATE_SPECIALIST_CATALOG'
    o['foundation_compatibility_catalog']['identity'] = NEW_FOUNDATION
    o['foundation_adjacent_compatibility_catalog']['runtime_route_map']['version'] = '1.2.1'
    vs = o['validation_state']
    vs['foundation_identity_closure'] = 'PASS_' + NEW_FOUNDATION
    vs['component_internal_foundation_compatibility'] = 'PASS_SET_007_EXACT_RECEIPTS'
    for e in o['entries']:
        e['foundation_compatibility_identity'] = NEW_FOUNDATION
    dump(p, o)


def main(root: Path) -> None:
    patch_core(root)
    patch_control(root)
    patch_governance(root)
    patch_starter(root)
    patch_handoff(root)
    patch_readme(root)
    patch_fixtures(root)
    patch_migration_tool(root)
    patch_r1_validator(root)
    patch_boot_validator(root)
    patch_release_validator(root)
    patch_r7_validator(root)
    patch_r3_validator(root)
    patch_r3_mutations(root)
    patch_behavioral_validator(root)
    patch_behavioral_mutations(root)
    patch_control_validator(root)
    patch_control_mutations(root)
    patch_v072_validator(root)
    patch_v072_mutations(root)
    patch_route_map(root)
    patch_profiles(root)
    patch_index(root)
    print('AIR v0.7.2 cognitive-scope authority-isolation patch applied')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('root', nargs='?', default='.')
    args = ap.parse_args()
    main(Path(args.root).resolve())
