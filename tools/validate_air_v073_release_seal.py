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
EXPECTED_HASHES = {
    'prompts/AIR_CORE_RUNTIME.md': 'e6915ad2f8af6a75f68d52eac3a7cf45d2dd9a3d300310c0d79c11a4033c8371',
    'prompts/AIR_CONTROL_SURFACE.md': '0ef70702500350aedf30ff3dc29fc5bc4533df2c00c505470aca01a70763e3ff',
    'prompts/AIR_DEFAULT_STARTER_PROFILE.json': '465cac6cb3303d98fed14a9110061f2b487cdec364e787f4310ffcbf35aa649c',
    'prompts/AIR_HANDOFF_CARD_TEMPLATE.json': '05ccdbc18ad82e81ab56ed69e524d5fa7b9dcbd19a65ed7662f422179af922e2',
    'prompts/AIR_GOV.md': '80f037b38b69d75436ddf2ec7b1dc757e84ab65d17aaeaf450cb963af44b4842',
    'catalog/AIR_RUNTIME_ROUTE_MAP.json': 'a8817d0abe078a2b94f87562386ac5e63a575b0926c0b2d050a6e470f578e89c',
    'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json': 'cf13dd95416559cdda9e594dd7916c1821e94a1fd9d3b2013f25ea97923ac176',
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

    req(index['INDEX_VERSION'] == '1.3.8', 'Index CEA-static-revalidation version mismatch')
    req(index['foundation_compatibility_catalog']['identity'] == FOUNDATION_ID, 'Index SET_008 identity mismatch')
    rr = index['foundation_adjacent_compatibility_catalog']['runtime_route_map']
    req(rr['version'] == '1.2.2' and rr['sha256'] == sha(ROOT / 'catalog/AIR_RUNTIME_ROUTE_MAP.json'), 'Index Route Map receipt stale')
    req(index['candidate_lifecycle_contract']['current_candidate_state'] == PENDING_STATIC, 'Index aggregate candidate lifecycle overclaims evidence')
    req(index['validation_state']['decision'] == 'CANDIDATE_PENDING_STATIC_VALIDATION', 'Index validation decision not pending-static')
    req(index['validation_state']['static_validation'] == 'PENDING_SPECIALIST_PACKAGE_SET_008_STATIC_COMPATIBILITY_REVALIDATION', 'Index static state mismatch')
    req(index['validation_state']['behavioral_revalidation'] == 'BLOCKED_PENDING_SET_008_STATIC_COMPATIBILITY_REVALIDATION', 'Index behavioral state not blocked by static')
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
    req(cae['availability_state'] == PENDING_BEHAVIOR, 'CEA lifecycle not pending behavioral revalidation')
    req(cae['foundation_compatibility_identity'] == FOUNDATION_ID, 'CEA SET_008 identity missing')
    req(cae['current_foundation_compatibility_state'] == 'STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING', 'CEA SET_008 static state mismatch')
    others = [e for e in index['entries'] if e['package_identity'] not in {CW_PACKAGE, SFV_PACKAGE, CEA_PACKAGE}]
    req(len(others) == 2 and all(e['availability_state'] == PENDING_STATIC for e in others), 'remaining Specialist lifecycle not pending-static')
    req(all(e['foundation_compatibility_identity'] == SET007 for e in others), 'remaining historical compatibility identity changed')
    req(all(e['current_foundation_compatibility_state'] == 'REVALIDATION_REQUIRED_NOT_INFERRED_FROM_INDEX_RESEAL' for e in others), 'remaining SET_008 compatibility inferred')
    prog = index['validation_state'].get('set008_static_revalidation_progress', {})
    req(prog.get('passed_package_identities') == [CEA_PACKAGE, CW_PACKAGE, SFV_PACKAGE] and prog.get('passed_count') == 3 and prog.get('pending_count') == 2 and prog.get('behavioral_revalidation_ready_package_identities') == [CEA_PACKAGE] and prog.get('behavioral_revalidation_passed_package_identities') == [CW_PACKAGE, SFV_PACKAGE] and prog.get('behavioral_revalidation_passed_count') == 2, 'Index SET_008 progress mismatch')

    # Manifest receipts remain exact for the unchanged SET_007 package bytes.
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
        req(obj.get('STATUS') == 'V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING', f'{name}: CEA static lifecycle mismatch')
    ceam = load(cea_dir / 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json')
    req(ceam['foundation_compatibility'].get('target_identity') == FOUNDATION_ID, 'CEA manifest target identity stale')
    req(ceam['package_validation_state'].get('behavioral_revalidation') == 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE', 'CEA behavioral state overclaimed')
    req(ceam['package_validation_state'].get('component_internal_foundation_compatibility') == 'PASS_SET_008_EXACT_RECEIPTS', 'CEA component receipt state stale')

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
    print('specialist_index', '1.3.8 pending SET_008 static revalidation')
    print('deterministic_registry', '90/90')


if __name__ == '__main__':
    try:
        main()
    except (E, KeyError, ValueError) as exc:
        print('AIR v0.7.3 release-seal validation: FAIL:', exc, file=sys.stderr)
        raise SystemExit(1)
