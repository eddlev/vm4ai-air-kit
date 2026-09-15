from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()

KIT_VERSION = '0.7.3'
FOUNDATION_ID = 'AIR_FOUNDATION_2_6_3_OBJECT_CONTRACT_SET_008'
SET007 = 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'
PENDING_STATIC = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION'
PENDING_BEHAVIOR = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'
RELEASED = 'RELEASE_CATALOG_ENTRY'
BEHAVIOR_PASS = 'PASS_REPLAYABLE_MODEL_HOST_EVIDENCE'
CW_PACKAGE = 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'
SFV_PACKAGE = 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2'
CEA_PACKAGE = 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2'
GOV_PACKAGE = 'AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_V2'
GROUND_PACKAGE = 'AIR_GROUNDING_SPECIALIST_PACKAGE_V2'
EXPECTED_HASHES = {
    'prompts/AIR_CORE_RUNTIME.md': 'e6915ad2f8af6a75f68d52eac3a7cf45d2dd9a3d300310c0d79c11a4033c8371',
    'prompts/AIR_CONTROL_SURFACE.md': '0ef70702500350aedf30ff3dc29fc5bc4533df2c00c505470aca01a70763e3ff',
    'prompts/AIR_DEFAULT_STARTER_PROFILE.json': '465cac6cb3303d98fed14a9110061f2b487cdec364e787f4310ffcbf35aa649c',
    'prompts/AIR_HANDOFF_CARD_TEMPLATE.json': '05ccdbc18ad82e81ab56ed69e524d5fa7b9dcbd19a65ed7662f422179af922e2',
    'prompts/AIR_GOV.md': '80f037b38b69d75436ddf2ec7b1dc757e84ab65d17aaeaf450cb963af44b4842',
    'catalog/AIR_RUNTIME_ROUTE_MAP.json': 'a8817d0abe078a2b94f87562386ac5e63a575b0926c0b2d050a6e470f578e89c',
    'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json': '0b32ae3d5289c24959f444079195a3786d0bbdd5e32313eb0c9c26208c6a0693',
}


class E(Exception):
    pass


def req(cond: bool, msg: str) -> None:
    if not cond:
        raise E(msg)


def reject_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise E(f'duplicate JSON key {key}')
        out[key] = value
    return out


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=reject_dupes)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_migrator():
    path = ROOT / 'tools' / 'migrate_air_handoff.py'
    spec = importlib.util.spec_from_file_location('air_handoff_migrator_v073', str(path))
    req(spec is not None and spec.loader is not None, 'migration utility import failed')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def synthetic_floor_card() -> dict[str, Any]:
    return {
        'AIR_HANDOFF_CARD': {
            'TEMPLATE_DESIGNATION': 'AIR_HANDOFF_CARD_TEMPLATE_V2',
            'SCHEMA_VERSION': '2.2.0',
            'template_designation': 'AIR_HANDOFF_CARD_TEMPLATE_V2',
            'schema_version': '2.2.0',
            'card_id': 'AIR-HANDOFF-SYNTHETIC-FLOOR',
            'card_revision': 44,
            'record_class': 'TRANSFER_RECORD',
            'runtime_origin': 'PROMPT_COMPILED',
            'backend_validation_claimed': False,
            'hidden_reasoning_claimed': False,
            'project_state': {'project_id': 'SYNTHETIC-FLOOR', 'project_status': 'ACTIVE'},
            'object_visibility_mode': 'ALL_OBJECTS',
            'profile_stack': {
                'starter_profile': {
                    'SYSTEM_DESIGNATION': 'AIR_DEFAULT_STARTER_V2',
                    'PROMPT_VERSION': '2.4.3',
                }
            },
            'schema_manifest': {'schema_compatibility_contract': {'canonical_schema_version': '2.2.0'}},
            'extensions': {'synthetic_fixture': True},
        }
    }


def main() -> None:
    req((ROOT / 'VERSION').read_text(encoding='utf-8').strip() == KIT_VERSION, 'VERSION is not 0.7.3')
    for rel, expected in EXPECTED_HASHES.items():
        p = ROOT / rel
        req(p.is_file(), f'missing sealed file {rel}')
        req(sha(p) == expected, f'exact sealed hash mismatch {rel}')

    core = (ROOT / 'prompts/AIR_CORE_RUNTIME.md').read_text(encoding='utf-8')
    control = (ROOT / 'prompts/AIR_CONTROL_SURFACE.md').read_text(encoding='utf-8')
    starter = load(ROOT / 'prompts/AIR_DEFAULT_STARTER_PROFILE.json')
    handoff = load(ROOT / 'prompts/AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']
    route = load(ROOT / 'catalog/AIR_RUNTIME_ROUTE_MAP.json')
    index = load(ROOT / 'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json')

    req('PROMPT_VERSION: 2.6.3' in core, 'Core not 2.6.3')
    req('PROMPT_VERSION: 2.6.3' in control, 'Control not 2.6.3')
    req(starter.get('PROMPT_VERSION') == '2.6.3', 'Starter not 2.6.3')
    req('CANONICAL_HANDOFF_TEMPLATE_REVISION: 19' in core, 'Core Handoff template revision not 19')
    req('AIR_DURABLE_SURFACED_OBJECT_PROVENANCE_V1' in core, 'durable provenance law missing')
    req('Strict-Handoff durability surface:' in control, 'Control durability surface missing')
    req('must not prescribe transcript export/paste as a recovery mechanism' in core.lower(), 'transcript-recovery prohibition missing')

    registry = starter['validation_contract']['deterministic_contract_registry']
    checks = registry['checks']
    ids = {c['check_id'] for c in checks}
    req(len(checks) == 90, f'deterministic registry count {len(checks)} != 90')
    req(registry['coverage_contract']['declared_check_count'] == 90, 'declared registry count not 90')
    for cid in {
        'DC-HANDOFF-TEMPLATE-REVISION',
        'DC-HANDOFF-NO-CURRENT-CARD-REVISION',
        'DC-HANDOFF-REQUIRED-TEMPLATE-REVISION',
        'DC-HANDOFF-REQUIRED-USER-REVISION',
        'DC-HANDOFF-CURRENT-PREDICATES-NO-CARD-REVISION',
        'DC-CORE-DURABLE-PROVENANCE-LAW',
        'DC-CONTROL-STRICT-HANDOFF-DURABILITY-SURFACE',
        'DC-STARTER-DURABLE-PROVENANCE-CONTRACT',
    }:
        req(cid in ids, f'missing deterministic check {cid}')

    req(handoff['schema_version'] == handoff['SCHEMA_VERSION'] == '2.3.0', 'Handoff schema mismatch')
    req(handoff['template_revision'] == 19, 'Handoff template_revision mismatch')
    req(handoff['user_revision'] is None, 'template user_revision baseline must be null')
    req('card_revision' not in handoff, 'current rev19 template still emits card_revision')
    declared = set(handoff['schema_manifest']['required_fields']) | set(handoff['schema_manifest'].get('optional_fields', []))
    req(set(handoff) == declared, 'Handoff root manifest closure mismatch')
    contracts = handoff['schema_manifest']['revision_migration_contracts']
    for key in ['REV18_TO_REV19', 'LEGACY_2_2_FLOOR_TO_REV19', 'SCHEMA_2_3_PRE_REV19_TO_REV19']:
        req(key in contracts, f'missing Handoff migration contract {key}')
    floor = contracts['LEGACY_2_2_FLOOR_TO_REV19']
    req(floor['minimum_recognized_starter_profile']['PROMPT_VERSION'] == '2.4.3', 'legacy floor Starter mismatch')
    req(floor['legacy_revision_interpretation'] == 'USER_REVISION', 'legacy 2.2 revision semantics wrong')
    req(contracts['REV18_TO_REV19']['root_revision_split']['user_revision_rule'].startswith('PRESERVE_EXPLICIT_INDEPENDENT_COUNTER'), 'rev18 user revision rule wrong')

    req(route['MAP_VERSION'] == route['ROUTE_MAP_VERSION'] == '1.2.2', 'Route Map version split mismatch')
    req(route['source_of_truth']['prompt_version'] == '2.6.3', 'Route Map Core version stale')
    req(route['source_of_truth']['sha256'] == sha(ROOT / 'prompts/AIR_CORE_RUNTIME.md'), 'Route Map Core hash stale')
    handoff_route = next(x for x in route['routes'] if x['route_id'] == 'RT.HANDOFF_CREATE')
    req('DEP.DURABLE_SURFACED_PROVENANCE_COMPLETE' in handoff_route['requires'], 'Route Map Handoff durability dependency missing')
    req(handoff_route['handoff_provenance_policy']['transcript_resupply_fallback'] == 'PROHIBITED', 'Route Map transcript fallback not prohibited')

    req(index['INDEX_VERSION'] == '1.3.13', 'Index Grounding-SET008-behavioral-promotion version mismatch')
    req(index['foundation_compatibility_catalog']['identity'] == FOUNDATION_ID, 'Index SET_008 identity mismatch')
    rr = index['foundation_adjacent_compatibility_catalog']['runtime_route_map']
    req(rr['version'] == '1.2.2' and rr['sha256'] == sha(ROOT / 'catalog/AIR_RUNTIME_ROUTE_MAP.json'), 'Index Route Map receipt stale')
    req(index['candidate_lifecycle_contract']['current_candidate_state'] == RELEASED, 'Index aggregate lifecycle not fully released after all-five behavioral revalidation')
    req(index['validation_state']['decision'] == 'PASS_ALL_FIVE_SET008_REPLAYABLE_BEHAVIORAL_REVALIDATION', 'Index validation decision not all-five behavioral-pass')
    req(index['validation_state']['static_validation'] == 'PASS_R7_DETERMINISTIC_STATIC_SUITE', 'Index static state mismatch')
    req(index['validation_state']['behavioral_revalidation'] == BEHAVIOR_PASS, 'Index behavioral state not all-five replayable pass')
    cw = [e for e in index['entries'] if e['package_identity'] == CW_PACKAGE]
    req(len(cw) == 1, 'Copywriting index entry missing')
    ce = cw[0]
    req(ce['availability_state'] == RELEASED, 'Copywriting lifecycle not released after behavioral revalidation')
    req(ce['foundation_compatibility_identity'] == FOUNDATION_ID, 'Copywriting SET_008 identity missing')
    req(ce['current_foundation_compatibility_state'] == 'STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED' and ce.get('behavioral_revalidation_state') == BEHAVIOR_PASS, 'Copywriting SET_008 behavioral state mismatch')
    sfv = [e for e in index['entries'] if e['package_identity'] == SFV_PACKAGE]
    req(len(sfv) == 1, 'SFV index entry missing')
    se = sfv[0]
    req(se['availability_state'] == RELEASED, 'SFV lifecycle not released after behavioral revalidation')
    req(se['foundation_compatibility_identity'] == FOUNDATION_ID, 'SFV SET_008 identity missing')
    req(se['current_foundation_compatibility_state'] == 'STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED_EXECUTOR_DRAFT_UNVALIDATED' and se.get('behavioral_revalidation_state') == BEHAVIOR_PASS, 'SFV SET_008 behavioral state mismatch')
    req(se.get('executor_component_state') == 'DRAFT_AVAILABLE_UNVALIDATED', 'SFV Executor component boundary missing from index')
    cea = [e for e in index['entries'] if e['package_identity'] == CEA_PACKAGE]
    req(len(cea) == 1, 'CEA index entry missing')
    cae = cea[0]
    req(cae['availability_state'] == RELEASED, 'CEA lifecycle not released after behavioral revalidation')
    req(cae['foundation_compatibility_identity'] == FOUNDATION_ID, 'CEA SET_008 identity missing')
    req(cae['current_foundation_compatibility_state'] == 'STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED' and cae.get('behavioral_revalidation_state') == BEHAVIOR_PASS, 'CEA SET_008 behavioral state mismatch')
    gov = [e for e in index['entries'] if e['package_identity'] == GOV_PACKAGE]
    req(len(gov) == 1, 'Governance index entry missing')
    goe = gov[0]
    req(goe['availability_state'] == RELEASED, 'Governance lifecycle not released after behavioral revalidation')
    req(goe['foundation_compatibility_identity'] == FOUNDATION_ID, 'Governance SET_008 identity missing')
    req(goe['current_foundation_compatibility_state'] == 'STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED_EXECUTOR_DRAFT_UNVALIDATED' and goe.get('behavioral_revalidation_state') == BEHAVIOR_PASS, 'Governance SET_008 behavioral state mismatch')
    req(goe.get('executor_component_state') == 'DRAFT_AVAILABLE_UNVALIDATED', 'Governance Executor component boundary missing from index')
    grounding = [e for e in index['entries'] if e['package_identity'] == GROUND_PACKAGE]
    req(len(grounding) == 1, 'Grounding index entry missing')
    gre = grounding[0]
    req(gre['availability_state'] == RELEASED, 'Grounding lifecycle not released after behavioral revalidation')
    req(gre['foundation_compatibility_identity'] == FOUNDATION_ID, 'Grounding SET_008 identity missing')
    req(gre['current_foundation_compatibility_state'] == 'STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED_EXECUTOR_DRAFT_UNVALIDATED' and gre.get('behavioral_revalidation_state') == BEHAVIOR_PASS, 'Grounding SET_008 behavioral state mismatch')
    req(gre.get('executor_component_state') == 'DRAFT_AVAILABLE_UNVALIDATED', 'Grounding Executor component boundary missing from index')
    prog = index['validation_state'].get('set008_static_revalidation_progress', {})
    req(prog.get('passed_package_identities') == [GOV_PACKAGE, CEA_PACKAGE, CW_PACKAGE, SFV_PACKAGE, GROUND_PACKAGE] and prog.get('passed_count') == 5 and prog.get('pending_count') == 0 and prog.get('pending_package_identities') == [] and prog.get('behavioral_revalidation_ready_package_identities') == [] and prog.get('behavioral_revalidation_passed_package_identities') == [GOV_PACKAGE, CEA_PACKAGE, CW_PACKAGE, SFV_PACKAGE, GROUND_PACKAGE] and prog.get('behavioral_revalidation_passed_count') == 5, 'Index SET_008 progress mismatch')

    gov_dir = ROOT / 'profiles' / 'governance specialist'
    gov_names = ['AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json','AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json','AIR_AI_GOVERNANCE_SPECIALIST.json','AIR_AI_GOVERNANCE_METHOD_PACK.json','AIR_AI_GOVERNANCE_EXECUTOR.json']
    for name in gov_names:
        obj = load(gov_dir / name); fc = obj['foundation_compatibility']
        req(fc.get('target_identity') == FOUNDATION_ID and fc.get('compatibility_state') == 'ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008', f'{name}: Governance SET_008 compatibility missing')
        hr = next(x for x in fc['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')
        req(hr.get('template_revision') == 19 and hr.get('revision_fields') == ['template_revision','user_revision'] and 'card_revision' not in hr, f'{name}: Governance Handoff revision split stale')
        rr = fc['route_map_discovery_input']; req(rr.get('version') == '1.2.2' and rr.get('sha256') == sha(ROOT / 'catalog/AIR_RUNTIME_ROUTE_MAP.json'), f'{name}: Governance Route Map receipt stale')
        if isinstance(obj.get('foundation_routing_compatibility'), dict) and isinstance(obj['foundation_routing_compatibility'].get('runtime_route_map'), dict):
            rr2=obj['foundation_routing_compatibility']['runtime_route_map']; req(rr2.get('version') == '1.2.2' and rr2.get('sha256') == sha(ROOT / 'catalog/AIR_RUNTIME_ROUTE_MAP.json'), f'{name}: Governance secondary Route Map receipt stale')
    for name in ['AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json','AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json','AIR_AI_GOVERNANCE_SPECIALIST.json','AIR_AI_GOVERNANCE_METHOD_PACK.json']:
        req(load(gov_dir / name).get('STATUS') == 'V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND', f'{name}: Governance behavioral lifecycle mismatch')
    req(load(gov_dir / 'AIR_AI_GOVERNANCE_EXECUTOR.json').get('STATUS') == 'DRAFT', 'Governance Executor prematurely promoted')
    govm=load(gov_dir / 'AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json')
    req(govm['package_validation_state'].get('component_internal_foundation_compatibility') == 'PASS_SET_008_EXACT_RECEIPTS' and govm['package_validation_state'].get('behavioral_revalidation') == BEHAVIOR_PASS and govm['package_validation_state'].get('executor_validation_state') == 'DRAFT_AVAILABLE_UNVALIDATED_EXCLUDED_FROM_BEHAVIORAL_PASS', 'Governance manifest behavioral state mismatch')
    govevp=ROOT/'tests/AIR_AI_GOVERNANCE_SET008_BEHAVIORAL_EVIDENCE_V1.json'
    req(govevp.is_file() and sha(govevp) == '7b568dfd9ea04e247b4b4b425af34e616765af0ad86c70a716e96c9629ebd3e9', 'Governance behavioral evidence file/hash mismatch')
    govev=load(govevp); gover=govm.get('behavioral_evidence_receipt', {})
    req(govev.get('evidence_id') == 'AIR_BEHAVIORAL_EVIDENCE_AI_GOVERNANCE_SET008_20260915_V1' and govev.get('summary', {}).get('pass_count') == 6 and govev.get('summary', {}).get('scenario_count') == 6 and govev.get('summary', {}).get('behavioral_revalidation_result') == 'PASS_ON_CURRENT_MODEL_HOST', 'Governance behavioral evidence result mismatch')
    req(gover.get('sha256') == '7b568dfd9ea04e247b4b4b425af34e616765af0ad86c70a716e96c9629ebd3e9' and gover.get('result') == BEHAVIOR_PASS and gover.get('cross_host_equivalence_claimed') is False and gover.get('executor_included_in_behavioral_pass') is False, 'Governance behavioral evidence receipt mismatch')

    # Manifest receipts remain exact for the current package bytes.
    for entry in index['entries']:
        targets = list(ROOT.glob('profiles/**/' + entry['manifest_filename']))
        req(len(targets) == 1, f"manifest target ambiguous {entry['manifest_filename']}")
        req(sha(targets[0]) == entry['manifest_sha256'], f"manifest hash changed {entry['manifest_filename']}")

    cw_dir = ROOT / 'profiles' / 'public surface copywriting specialist'
    for name in ['AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST.json', 'AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json']:
        obj = load(cw_dir / name)
        fc = obj['foundation_compatibility']
        req(fc.get('target_identity') == FOUNDATION_ID and fc.get('compatibility_state') == 'ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008', f'{name}: SET_008 compatibility missing')
        hr = next(x for x in fc['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')
        req(hr.get('template_revision') == 19 and hr.get('revision_fields') == ['template_revision', 'user_revision'] and 'card_revision' not in hr, f'{name}: stale Handoff revision contract')
    cwm = load(cw_dir / 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json')
    req(cwm['foundation_compatibility'].get('target_identity') == FOUNDATION_ID, 'Copywriting manifest target identity stale')
    req(cwm['package_validation_state'].get('foundation_reseal') == 'PASS_COORDINATED_SET_008_RESEAL', 'Copywriting manifest reseal state stale')
    req(cwm['package_validation_state'].get('behavioral_revalidation') == BEHAVIOR_PASS, 'Copywriting behavioral evidence not promoted')
    evp = ROOT / 'tests/AIR_PUBLIC_SURFACE_COPYWRITING_SET008_BEHAVIORAL_EVIDENCE_V1.json'
    req(evp.is_file() and sha(evp) == '948dfcf7f9dfe1839e06475bb7566521b56430d2fb141cb96065e1e8fd45769d', 'Copywriting behavioral evidence file/hash mismatch')
    ev = load(evp); er = cwm.get('behavioral_evidence_receipt', {})
    req(ev.get('evidence_id') == 'AIR_BEHAVIORAL_EVIDENCE_PUBLIC_SURFACE_COPYWRITING_SET008_20260914_V1' and ev.get('summary', {}).get('pass_count') == 6 and ev.get('summary', {}).get('scenario_count') == 6, 'Copywriting behavioral evidence result mismatch')
    req(er.get('sha256') == '948dfcf7f9dfe1839e06475bb7566521b56430d2fb141cb96065e1e8fd45769d' and er.get('result') == BEHAVIOR_PASS and er.get('cross_host_equivalence_claimed') is False, 'Copywriting behavioral evidence receipt mismatch')

    sfv_dir = ROOT / 'profiles' / 'specification first verification specialist'
    for name in [
        'AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json',
        'AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json',
        'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json',
        'AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json',
    ]:
        obj = load(sfv_dir / name)
        fc = obj['foundation_compatibility']
        req(fc.get('target_identity') == FOUNDATION_ID and fc.get('compatibility_state') == 'ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008', f'{name}: SET_008 compatibility missing')
        hr = next(x for x in fc['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')
        req(hr.get('template_revision') == 19 and hr.get('revision_fields') == ['template_revision', 'user_revision'] and 'card_revision' not in hr, f'{name}: stale Handoff revision contract')
        if name != 'AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json':
            req(obj.get('STATUS') == 'V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND', f'{name}: SFV behavioral status missing')
            req(obj.get('package_completion_contract', {}).get('package_state') == 'PACKAGE_STRUCTURALLY_COMPLETE_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND_EXECUTOR_DRAFT_UNVALIDATED', f'{name}: SFV package completion behavioral state missing')
    req(load(sfv_dir / 'AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json').get('STATUS') == 'DRAFT', 'SFV Executor was promoted out of DRAFT')
    sfvm = load(sfv_dir / 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json')
    req(sfvm['foundation_compatibility'].get('target_identity') == FOUNDATION_ID, 'SFV manifest target identity stale')
    req(sfvm['package_validation_state'].get('behavioral_revalidation') == BEHAVIOR_PASS, 'SFV behavioral evidence not promoted')
    req(sfvm['package_validation_state'].get('component_internal_foundation_compatibility') == 'PASS_SET_008_EXACT_RECEIPTS', 'SFV component receipt state stale')
    req(sfvm['package_validation_state'].get('executor_validation_state') == 'DRAFT_AVAILABLE_UNVALIDATED_EXCLUDED_FROM_BEHAVIORAL_PASS', 'SFV Executor validation boundary missing')
    sfvevp = ROOT / 'tests/AIR_SPECIFICATION_FIRST_VERIFICATION_SET008_BEHAVIORAL_EVIDENCE_V1.json'
    req(sfvevp.is_file() and sha(sfvevp) == '831a048946574a10f7dd5a1adb8cd6b4125e4a39030f9414f9de2d464f1b5649', 'SFV behavioral evidence file/hash mismatch')
    sfvev = load(sfvevp); sfver = sfvm.get('behavioral_evidence_receipt', {})
    req(sfvev.get('evidence_id') == 'AIR_BEHAVIORAL_EVIDENCE_SPECIFICATION_FIRST_VERIFICATION_SET008_20260915_V1' and sfvev.get('summary', {}).get('pass_count') == 6 and sfvev.get('summary', {}).get('scenario_count') == 6 and sfvev.get('summary', {}).get('behavioral_revalidation_result') == 'PASS_ON_CURRENT_MODEL_HOST', 'SFV behavioral evidence result mismatch')
    req(sfver.get('sha256') == '831a048946574a10f7dd5a1adb8cd6b4125e4a39030f9414f9de2d464f1b5649' and sfver.get('result') == BEHAVIOR_PASS and sfver.get('cross_host_equivalence_claimed') is False and sfver.get('executor_included_in_behavioral_pass') is False, 'SFV behavioral evidence receipt mismatch')

    cea_dir = ROOT / 'profiles' / 'capability ecology architect'
    for name in [
        'AIR_DOMAIN_CAPABILITY_REGISTRY.json',
        'AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json',
        'AIR_CAPABILITY_ECOLOGY_ARCHITECT.json',
        'AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json',
    ]:
        obj = load(cea_dir / name)
        fc = obj['foundation_compatibility']
        req(fc.get('target_identity') == FOUNDATION_ID and fc.get('compatibility_state') == 'ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008', f'{name}: CEA SET_008 compatibility missing')
        hr = next(x for x in fc['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')
        req(hr.get('template_revision') == 19 and hr.get('revision_fields') == ['template_revision', 'user_revision'] and 'card_revision' not in hr, f'{name}: CEA stale Handoff revision contract')
        rr = fc.get('route_map_discovery_input', {})
        req(rr.get('version') == '1.2.2' and rr.get('sha256') == sha(ROOT / 'catalog/AIR_RUNTIME_ROUTE_MAP.json'), f'{name}: CEA stale Route Map receipt')
        req(obj.get('STATUS') == 'V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND', f'{name}: CEA behavioral lifecycle mismatch')
    ceam = load(cea_dir / 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json')
    req(ceam['foundation_compatibility'].get('target_identity') == FOUNDATION_ID, 'CEA manifest target identity stale')
    req(ceam['package_validation_state'].get('behavioral_revalidation') == BEHAVIOR_PASS, 'CEA behavioral evidence not promoted')
    req(ceam['package_validation_state'].get('component_internal_foundation_compatibility') == 'PASS_SET_008_EXACT_RECEIPTS', 'CEA component receipt state stale')
    ceaevp=ROOT/'tests/AIR_CAPABILITY_ECOLOGY_ARCHITECT_SET008_BEHAVIORAL_EVIDENCE_V1.json'; req(ceaevp.is_file() and sha(ceaevp)=='4779e1e48a4b9b614c66e892c7bf964fcabcd4b04bfae41af2bddbb01564307d','CEA behavioral evidence file/hash mismatch')
    ceaev=load(ceaevp); ceaer=ceam.get('behavioral_evidence_receipt',{})
    req(ceaev.get('evidence_id')=='AIR_BEHAVIORAL_EVIDENCE_CAPABILITY_ECOLOGY_ARCHITECT_SET008_20260915_V1' and ceaev.get('summary',{}).get('pass_count')==6 and ceaev.get('summary',{}).get('scenario_count')==6 and ceaev.get('summary',{}).get('behavioral_revalidation_result')=='PASS_ON_CURRENT_MODEL_HOST','CEA behavioral evidence result mismatch')
    req(ceaer.get('sha256')=='4779e1e48a4b9b614c66e892c7bf964fcabcd4b04bfae41af2bddbb01564307d' and ceaer.get('result')==BEHAVIOR_PASS and ceaer.get('cross_host_equivalence_claimed') is False,'CEA behavioral evidence receipt mismatch')

    grounding_dir = ROOT / 'profiles' / 'grounding specialist'
    for name in ['AIR_GROUNDING_DOMAIN_PACKAGE.json','AIR_GROUNDING_METHOD_PACK.json','AIR_GROUNDING_SPECIALIST.json','AIR_GROUNDING_EXECUTOR.json']:
        obj = load(grounding_dir / name); fc = obj['foundation_compatibility']
        req(fc.get('target_identity') == FOUNDATION_ID and fc.get('compatibility_state') == 'ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008', f'{name}: Grounding SET_008 compatibility missing')
        hr = next(x for x in fc['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')
        req(hr.get('template_revision') == 19 and hr.get('revision_fields') == ['template_revision','user_revision'] and 'card_revision' not in hr, f'{name}: Grounding Handoff revision split stale')
        rr = fc.get('route_map_discovery_input') or fc.get('foundation_adjacent_route_map') or {}
        req(rr.get('version') == '1.2.2' and rr.get('sha256') == sha(ROOT / 'catalog/AIR_RUNTIME_ROUTE_MAP.json'), f'{name}: Grounding Route Map receipt stale')
        if name != 'AIR_GROUNDING_EXECUTOR.json':
            req(obj.get('STATUS') == 'V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND', f'{name}: Grounding behavioral status missing')
            req(obj.get('package_completion_contract', {}).get('package_state') == 'PACKAGE_STRUCTURALLY_COMPLETE_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND_EXECUTOR_DRAFT_UNVALIDATED', f'{name}: Grounding package completion behavioral state missing')
    req(load(grounding_dir / 'AIR_GROUNDING_EXECUTOR.json').get('STATUS') == 'DRAFT', 'Grounding Executor was promoted out of DRAFT')
    groundm = load(grounding_dir / 'AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json')
    req(groundm['foundation_compatibility'].get('target_identity') == FOUNDATION_ID, 'Grounding manifest target identity stale')
    req(groundm['package_validation_state'].get('behavioral_revalidation') == BEHAVIOR_PASS, 'Grounding behavioral evidence not promoted')
    req(groundm['package_validation_state'].get('component_internal_foundation_compatibility') == 'PASS_SET_008_EXACT_RECEIPTS', 'Grounding component receipt state stale')
    req(groundm['package_validation_state'].get('executor_validation_state') == 'DRAFT_AVAILABLE_UNVALIDATED_EXCLUDED_FROM_BEHAVIORAL_PASS', 'Grounding Executor validation boundary missing')
    groundevp = ROOT / 'tests/AIR_GROUNDING_SET008_BEHAVIORAL_EVIDENCE_V1.json'
    req(groundevp.is_file() and sha(groundevp) == '77fd1409d8fde79c3e8169f9823cd5b3fdd0a97fc8eea5e9f7ca303f3add2c92', 'Grounding behavioral evidence file/hash mismatch')
    groundev = load(groundevp); grounder = groundm.get('behavioral_evidence_receipt', {})
    req(groundev.get('evidence_id') == 'AIR_BEHAVIORAL_EVIDENCE_GROUNDING_SET008_20260915_V1' and groundev.get('summary', {}).get('pass_count') == 6 and groundev.get('summary', {}).get('scenario_count') == 6 and groundev.get('summary', {}).get('behavioral_revalidation_result') == 'PASS_ON_CURRENT_MODEL_HOST', 'Grounding behavioral evidence result mismatch')
    req(grounder.get('sha256') == '77fd1409d8fde79c3e8169f9823cd5b3fdd0a97fc8eea5e9f7ca303f3add2c92' and grounder.get('result') == BEHAVIOR_PASS and grounder.get('cross_host_equivalence_claimed') is False and grounder.get('executor_included_in_behavioral_pass') is False, 'Grounding behavioral evidence receipt mismatch')

    migrator = load_migrator()
    current_doc = {'AIR_HANDOFF_CARD': handoff}
    legacy = synthetic_floor_card()
    migrated = migrator.migrate_to_current(copy.deepcopy(legacy), current_doc)['AIR_HANDOFF_CARD']
    req(migrated['template_revision'] == 19, 'legacy floor did not reach template rev19')
    req(migrated['user_revision'] == 44, 'legacy card_revision 44 was not preserved as user_revision')
    req('card_revision' not in migrated, 'legacy card_revision leaked into rev19 output')
    req(migrated['migration_state']['source_template_revision'] is None, 'legacy 2.2 invented a template revision')
    req(migrated['migration_state']['source_user_revision'] == 44, 'legacy 2.2 source user revision not recorded')
    req(migrated['migration_state']['revision_migration_path'] == 'LEGACY_2_2_FLOOR_TO_REV19', 'legacy floor migration path wrong')
    req(migrated['surfaced_object_ledger_state']['positive_execution_authority'] == 'NONE_HISTORY_ONLY', 'legacy history gained authority')
    req(migrated['project_state']['project_id'] == 'SYNTHETIC-FLOOR', 'legacy explicit project state not preserved')

    prefloor = copy.deepcopy(legacy)
    prefloor['AIR_HANDOFF_CARD']['SCHEMA_VERSION'] = prefloor['AIR_HANDOFF_CARD']['schema_version'] = '2.1.0'
    try:
        migrator.migrate_to_current(prefloor, current_doc)
    except migrator.MigrationError:
        pass
    else:
        raise E('pre-floor schema 2.1.0 was accepted')

    rev18 = copy.deepcopy(current_doc)
    c18 = rev18['AIR_HANDOFF_CARD']
    c18.pop('template_revision', None)
    c18.pop('user_revision', None)
    c18['card_revision'] = 18
    r18 = migrator.migrate_to_current(rev18, current_doc)['AIR_HANDOFF_CARD']
    req(r18['template_revision'] == 19 and r18['user_revision'] is None and 'card_revision' not in r18, 'schema 2.3 rev18 migration semantics wrong')
    req(r18['migration_state']['source_template_revision'] == 18, 'rev18 source template revision missing')

    # Public source must not contain the private fixture identity/content.
    for rel in [
        'prompts/AIR_CORE_RUNTIME.md', 'prompts/AIR_CONTROL_SURFACE.md',
        'prompts/AIR_DEFAULT_STARTER_PROFILE.json', 'prompts/AIR_HANDOFF_CARD_TEMPLATE.json',
        'catalog/AIR_RUNTIME_ROUTE_MAP.json', 'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',
        'tools/migrate_air_handoff.py', 'tools/validate_air_v073_release_seal.py',
        'tests/air_contract_fixtures.json', 'tests/deterministic_contract_inventory.json',
    ]:
        txt = (ROOT / rel).read_text(encoding='utf-8')
        private_markers = ('Mon' + 'ica Angiuli', 'AIR-HANDOFF-' + 'MONICA')
        req(all(marker not in txt for marker in private_markers), f'private fixture leaked into {rel}')

    print('AIR v0.7.3 release-seal validation: PASS')
    print('foundation', FOUNDATION_ID)
    print('handoff_schema', '2.3.0')
    print('handoff_template_revision', 19)
    print('legacy_floor', '2.2.0 / Starter 2.4.3')
    print('route_map', '1.2.2')
    print('specialist_index', '1.3.13; all five Specialist packages SET_008 static-valid and replayable behavioral-pass; Grounding Executor remains DRAFT/unvalidated')
    print('deterministic_registry', '90/90')


if __name__ == '__main__':
    try:
        main()
    except (E, KeyError, ValueError) as exc:
        print('AIR v0.7.3 release-seal validation: FAIL:', exc, file=sys.stderr)
        raise SystemExit(1)
