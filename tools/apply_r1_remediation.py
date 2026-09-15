from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
BASE = '0c66231da8cd91b8c2ee142d023034e01773dc29'
FOUNDATION_ID = 'AIR_FOUNDATION_2_6_3_OBJECT_CONTRACT_SET_008'
LEGACY_FOUNDATION_ID = 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'
SET008_COMPAT = 'ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008'
SET008_STATE = 'OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_' + FOUNDATION_ID
STATIC_STATUS = 'V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING'
MANIFEST_STATUS = 'PACKAGE_COMPLETE_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING'
BEHAVIOR_PENDING = 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'
CEA_PACKAGE = 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2'
CW_PACKAGE = 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'
SFV_PACKAGE = 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2'
GOV_PACKAGE = 'AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_V2'
GROUNDING_PACKAGE = 'AIR_GROUNDING_SPECIALIST_PACKAGE_V2'
CEA_DIR = ROOT / 'profiles' / 'capability ecology architect'
GENERATED_AT = '2026-09-15T06:35:00Z'

COMPONENTS = [
    'AIR_DOMAIN_CAPABILITY_REGISTRY.json',
    'AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json',
    'AIR_CAPABILITY_ECOLOGY_ARCHITECT.json',
    'AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json',
]
MANIFEST = 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json'
PERMANENT_PATHS = {
    'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',
    'profiles/capability ecology architect/AIR_DOMAIN_CAPABILITY_REGISTRY.json',
    'profiles/capability ecology architect/AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json',
    'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT.json',
    'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json',
    'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json',
    'tools/validate_air_r7_remediation.py',
    'tools/test_air_r7_mutations.py',
    'tools/validate_air_v073_release_seal.py',
    'tools/test_air_v073_release_seal_mutations.py',
}


def req(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(msg)


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def meta(path: Path) -> dict:
    raw = path.read_bytes()
    return {
        'sha256': hashlib.sha256(raw).hexdigest(),
        'size_bytes': len(raw),
        'line_count': len(raw.decode('utf-8').splitlines()),
    }


def run(*cmd: str) -> None:
    print('+', ' '.join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def one_text(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding='utf-8')
    count = text.count(old)
    req(count == 1, f'{path}: expected exactly one anchor, got {count}: {old[:120]}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


def one_regex(path: Path, pattern: str, repl: str) -> None:
    text = path.read_text(encoding='utf-8')
    new, count = re.subn(pattern, repl, text, count=1)
    req(count == 1, f'{path}: regex anchor count {count}: {pattern}')
    path.write_text(new, encoding='utf-8')


def foundation_receipts() -> list[dict]:
    specs = [
        ('AIR_CORE_RUNTIME.md', 'AIR_CORE_RUNTIME_V2', '2.6.3', 'FOUNDATION_PROMPT'),
        ('AIR_CONTROL_SURFACE.md', 'AIR_CONTROL_SURFACE_V2', '2.6.3', 'FOUNDATION_PROMPT'),
        ('AIR_GOV.md', 'AIR_HR_GOVERNANCE_SUPPLEMENT_V2', '2.3.2', 'FOUNDATION_PROMPT'),
        ('AIR_DEFAULT_STARTER_PROFILE.json', 'AIR_DEFAULT_STARTER_V2', '2.6.3', 'TASK_COMPOSITE'),
        ('AIR_HANDOFF_CARD_TEMPLATE.json', 'AIR_HANDOFF_CARD_TEMPLATE_V2', '2.3.0', 'TEMPLATE'),
    ]
    out = []
    for filename, designation, version, cls in specs:
        m = meta(ROOT / 'prompts' / filename)
        rec = {
            'filename': filename,
            'designation': designation,
            'version': version,
            'class': cls,
            **m,
        }
        if filename == 'AIR_HANDOFF_CARD_TEMPLATE.json':
            rec['template_revision'] = 19
            rec['revision_fields'] = ['template_revision', 'user_revision']
        out.append(rec)
    return out


def route_receipt() -> dict:
    m = meta(ROOT / 'catalog' / 'AIR_RUNTIME_ROUTE_MAP.json')
    return {
        'filename': 'AIR_RUNTIME_ROUTE_MAP.json',
        'designation': 'AIR_RUNTIME_ROUTE_MAP_V1',
        'version': '1.2.2',
        'class': 'FOUNDATION_ADJACENT_BOOTSTRAP_ROUTE_CATALOG',
        **m,
    }


def update_foundation(obj: dict) -> None:
    fc = obj['foundation_compatibility']
    fc['required_files'] = foundation_receipts()
    fc['compatibility_state'] = SET008_COMPAT
    fc['target_foundation_versions'] = {
        'core': '2.6.3',
        'control': '2.6.3',
        'governance': '2.3.2',
        'starter': '2.6.3',
        'handoff_schema': '2.3.0',
    }
    fc['foundation_candidate_set_identity'] = FOUNDATION_ID
    fc['target_identity'] = FOUNDATION_ID
    fc['route_map_discovery_input'] = route_receipt()
    fc['cognitive_scope_authority_ref'] = 'AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION'


def update_common(obj: dict) -> None:
    obj['STATUS'] = STATIC_STATUS
    update_foundation(obj)
    ir = obj.get('integration_refresh')
    if isinstance(ir, dict) and 'foundation_identity_state' in ir:
        ir['foundation_identity_state'] = SET008_STATE


def set_dependency_hash(obj: dict, key: str, value: str) -> None:
    dep = obj.get('external_dependency_state', {}).get(key)
    if not isinstance(dep, dict):
        return
    if 'sha256' in dep:
        dep['sha256'] = value
    if 'observed_sha256' in dep:
        dep['observed_sha256'] = value


def main() -> None:
    run('git', 'fetch', '--no-tags', 'origin', BASE)
    req((ROOT / 'VERSION').read_text(encoding='utf-8').strip() == '0.7.3', 'VERSION drifted')
    req(meta(ROOT / 'catalog' / 'AIR_RUNTIME_ROUTE_MAP.json')['sha256'] == 'a8817d0abe078a2b94f87562386ac5e63a575b0926c0b2d050a6e470f578e89c', 'Route Map hash drifted')

    man_before = load(CEA_DIR / MANIFEST)
    old_hash = {c['filename']: c['sha256'] for c in man_before['components']}
    req(set(old_hash) == set(COMPONENTS), 'CEA manifest component set drifted')
    req(man_before.get('t7_change_record', {}).get('change_id') == 'AIR_T7_CEA_MII_INTEGRATION_001', 'CEA T7 record missing before reseal')

    registry_path = CEA_DIR / COMPONENTS[0]
    registry = load(registry_path)
    update_common(registry)
    dump(registry_path, registry)
    registry_hash = meta(registry_path)['sha256']

    translator_path = CEA_DIR / COMPONENTS[1]
    translator = load(translator_path)
    update_common(translator)
    set_dependency_hash(translator, 'domain_capability_registry', registry_hash)
    dump(translator_path, translator)
    translator_hash = meta(translator_path)['sha256']

    architect_path = CEA_DIR / COMPONENTS[2]
    architect = load(architect_path)
    update_common(architect)
    set_dependency_hash(architect, 'domain_capability_registry', registry_hash)
    set_dependency_hash(architect, 'human_to_machine_capability_translator', translator_hash)
    dump(architect_path, architect)
    architect_hash = meta(architect_path)['sha256']

    method_path = CEA_DIR / COMPONENTS[3]
    method = load(method_path)
    update_common(method)
    set_dependency_hash(method, 'domain_capability_registry', registry_hash)
    set_dependency_hash(method, 'human_to_machine_capability_translator', translator_hash)
    set_dependency_hash(method, 'capability_ecology_architect', architect_hash)
    dump(method_path, method)

    manifest_path = CEA_DIR / MANIFEST
    manifest = load(manifest_path)
    manifest['status'] = MANIFEST_STATUS
    manifest['generated_at'] = GENERATED_AT
    update_foundation(manifest)
    ir = manifest.get('integration_refresh')
    if isinstance(ir, dict) and 'foundation_identity_state' in ir:
        ir['foundation_identity_state'] = SET008_STATE
    pvs = manifest['package_validation_state']
    pvs['package_state'] = 'PACKAGE_COMPLETE_OBJECT_CONTRACT_SET_008_RESEAL_STATICALLY_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING'
    pvs['cross_file'] = 'PASS_AIR_FOUNDATION_2_6_3_OBJECT_CONTRACT_SET_008_AND_EXACT_SPECIALIST_INTERNAL_DEPENDENCY_CLOSURE'
    pvs['regression'] = BEHAVIOR_PENDING
    pvs['prior_behavioral_evidence_inheritance'] = BEHAVIOR_PENDING
    pvs['decision'] = 'STATIC_VALIDATED_AVAILABLE_UNBOUND_BEHAVIORAL_REVALIDATION_PENDING'
    pvs['coordinated_reseal_static_validation'] = 'PASS_R7_DETERMINISTIC_STATIC_SUITE'
    pvs['behavioral_revalidation'] = BEHAVIOR_PENDING
    pvs['component_internal_foundation_compatibility'] = 'PASS_SET_008_EXACT_RECEIPTS'
    by_name = {c['filename']: c for c in manifest['components']}
    for filename in COMPONENTS:
        cp = CEA_DIR / filename
        cm = meta(cp)
        by_name[filename].update(cm)
        by_name[filename]['status'] = load(cp).get('STATUS')
        by_name[filename]['availability_state'] = 'VALIDATED_AVAILABLE_UNBOUND'
    req(manifest.get('t7_change_record') == man_before.get('t7_change_record'), 'historical T7 record changed during reseal')
    dump(manifest_path, manifest)
    cea_manifest_hash = meta(manifest_path)['sha256']

    idx_path = ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json'
    idx = load(idx_path)
    req(idx.get('INDEX_VERSION') == '1.3.7', 'unexpected source Index version')
    idx['INDEX_VERSION'] = '1.3.8'
    idx['generated_at'] = GENERATED_AT
    vs = idx['validation_state']
    vs['manifest_hash_closure'] = 'MIXED_SET_007_AND_SET_008_RECEIPTS_CEA_COPYWRITING_SFV_SET_008_OTHER_PACKAGES_PENDING'
    vs['component_internal_foundation_compatibility'] = 'CEA_COPYWRITING_SFV_PASS_SET_008_GOVERNANCE_AND_GROUNDING_REVALIDATION_REQUIRED'
    prog = vs['set008_static_revalidation_progress']
    prog['passed_package_identities'] = [CEA_PACKAGE, CW_PACKAGE, SFV_PACKAGE]
    prog['pending_package_identities'] = [GOV_PACKAGE, GROUNDING_PACKAGE]
    prog['passed_count'] = 3
    prog['pending_count'] = 2
    prog['behavioral_revalidation_ready_package_identities'] = [CEA_PACKAGE]
    prog['behavioral_revalidation_passed_package_identities'] = [CW_PACKAGE, SFV_PACKAGE]
    prog['behavioral_revalidation_passed_count'] = 2
    cea_entry = next(e for e in idx['entries'] if e['package_identity'] == CEA_PACKAGE)
    cea_entry['manifest_sha256'] = cea_manifest_hash
    cea_entry['foundation_compatibility_identity'] = FOUNDATION_ID
    cea_entry['availability_state'] = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'
    cea_entry['current_foundation_compatibility_state'] = 'STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING'
    dump(idx_path, idx)
    index_hash = meta(idx_path)['sha256']

    r7 = ROOT / 'tools' / 'validate_air_r7_remediation.py'
    one_text(r7,
        "CW_PACKAGE='AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'\nSFV_PACKAGE='AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2'\nCW_DIR='public surface copywriting specialist'\nSFV_DIR='specification first verification specialist'",
        "CW_PACKAGE='AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'\nSFV_PACKAGE='AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2'\nCEA_PACKAGE='AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2'\nCW_DIR='public surface copywriting specialist'\nSFV_DIR='specification first verification specialist'\nCEA_DIR='capability ecology architect'")
    one_text(r7, "req(idx.get('INDEX_VERSION')=='1.3.7','SFV SET_008 behavioral promotion index version mismatch')", "req(idx.get('INDEX_VERSION')=='1.3.8','CEA SET_008 static revalidation index version mismatch')")
    one_text(r7,
        "req(prog.get('passed_package_identities')==[CW_PACKAGE,SFV_PACKAGE] and prog.get('passed_count')==2 and prog.get('pending_count')==3 and prog.get('behavioral_revalidation_ready_package_identities')==[] and prog.get('behavioral_revalidation_passed_package_identities')==[CW_PACKAGE,SFV_PACKAGE] and prog.get('behavioral_revalidation_passed_count')==2,'R7 SET_008 progress carrier mismatch')",
        "req(prog.get('passed_package_identities')==[CEA_PACKAGE,CW_PACKAGE,SFV_PACKAGE] and prog.get('passed_count')==3 and prog.get('pending_count')==2 and prog.get('behavioral_revalidation_ready_package_identities')==[CEA_PACKAGE] and prog.get('behavioral_revalidation_passed_package_identities')==[CW_PACKAGE,SFV_PACKAGE] and prog.get('behavioral_revalidation_passed_count')==2,'R7 SET_008 progress carrier mismatch')")
    one_text(r7,
        "req(len(prog.get('pending_package_identities',[]))==3 and CW_PACKAGE not in prog.get('pending_package_identities',[]) and SFV_PACKAGE not in prog.get('pending_package_identities',[]),'R7 SET_008 pending package set mismatch')",
        "req(prog.get('pending_package_identities')==['AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_V2','AIR_GROUNDING_SPECIALIST_PACKAGE_V2'],'R7 SET_008 pending package set mismatch')")
    one_text(r7,
        "   req(e.get('executor_component_state')=='DRAFT_AVAILABLE_UNVALIDATED','SFV Executor component boundary missing from index')\n  else:\n   req(e['foundation_compatibility_identity']==LEGACY_FOUNDATION_ID,'remaining pending index Foundation identity changed before revalidation')",
        "   req(e.get('executor_component_state')=='DRAFT_AVAILABLE_UNVALIDATED','SFV Executor component boundary missing from index')\n  elif e['package_identity']==CEA_PACKAGE:\n   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'CEA index Foundation identity not SET_008')\n   req(e['availability_state']==PENDING_BEHAVIOR,'CEA index lifecycle not pending behavioral revalidation')\n   req(e.get('current_foundation_compatibility_state')=='STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING','CEA SET_008 static state mismatch')\n  else:\n   req(e['foundation_compatibility_identity']==LEGACY_FOUNDATION_ID,'remaining pending index Foundation identity changed before revalidation')")
    one_text(r7,
        "  is_cw=CW_DIR in str(p)\n  is_sfv=SFV_DIR in str(p)\n  is_set008=is_cw or is_sfv",
        "  is_cw=CW_DIR in str(p)\n  is_sfv=SFV_DIR in str(p)\n  is_cea=CEA_DIR in str(p)\n  is_set008=is_cw or is_sfv or is_cea")
    one_text(r7,
        "   expected_state=SET008_FOUNDATION_STATE if (CW_DIR in str(p) or SFV_DIR in str(p)) else FOUNDATION_STATE",
        "   expected_state=SET008_FOUNDATION_STATE if (CW_DIR in str(p) or SFV_DIR in str(p) or CEA_DIR in str(p)) else FOUNDATION_STATE")
    one_text(r7,
        " cea=parsed[ROOT/'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json']\n req(cea.get('t7_change_record')==T7,'074 T7 historical record mutated')",
        " cea=parsed[ROOT/'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json']\n req(cea['foundation_compatibility'].get('target_identity')==FOUNDATION_ID and cea['foundation_compatibility'].get('compatibility_state')==SET008_SPECIALIST_COMPAT,'CEA manifest SET_008 compatibility missing')\n ceapvs=cea.get('package_validation_state',{})\n req(ceapvs.get('behavioral_revalidation')==BEHAVIOR_PENDING and ceapvs.get('component_internal_foundation_compatibility')=='PASS_SET_008_EXACT_RECEIPTS','CEA manifest validation state mismatch')\n req(cea.get('t7_change_record')==T7,'074 T7 historical record mutated')")

    r7mut = ROOT / 'tools' / 'test_air_r7_mutations.py'
    one_text(r7mut,
        "add('R7-N34-SFV-COMPONENT-BEHAVIORAL-ROLLBACK','profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json',jfn(lambda o:o.__setitem__('STATUS','V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING')))\nif run(ROOT)!=0:raise SystemExit('R7-MUTATION-BASELINE failed')",
        "add('R7-N34-SFV-COMPONENT-BEHAVIORAL-ROLLBACK','profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json',jfn(lambda o:o.__setitem__('STATUS','V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING')))\nadd('R7-N35-CEA-INDEX-STATIC-ROLLBACK','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:next(e for e in o['entries'] if e['package_identity']=='AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2').__setitem__('availability_state','RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION')))\nadd('R7-N36-CEA-INDEX-SET007-ROLLBACK','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:next(e for e in o['entries'] if e['package_identity']=='AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2').__setitem__('foundation_compatibility_identity','AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007')))\nadd('R7-N37-CEA-CARD-REVISION-RESTORED','profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT.json',jfn(lambda o:next(x for x in o['foundation_compatibility']['required_files'] if x['filename']=='AIR_HANDOFF_CARD_TEMPLATE.json').__setitem__('card_revision',18)))\nadd('R7-N38-CEA-ROUTE-MAP-ROLLBACK','profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json',jfn(lambda o:o['foundation_compatibility']['route_map_discovery_input'].__setitem__('version','1.2.1')))\nif run(ROOT)!=0:raise SystemExit('R7-MUTATION-BASELINE failed')")

    v073 = ROOT / 'tools' / 'validate_air_v073_release_seal.py'
    one_text(v073,
        "CW_PACKAGE = 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'\nSFV_PACKAGE = 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2'",
        "CW_PACKAGE = 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'\nSFV_PACKAGE = 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2'\nCEA_PACKAGE = 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2'")
    one_regex(v073, r"('catalog/AIR_SPECIALIST_PACKAGE_INDEX\.json': ')[0-9a-f]{64}(')", r"\g<1>" + index_hash + r"\g<2>")
    one_text(v073, "req(index['INDEX_VERSION'] == '1.3.7', 'Index SFV-behavioral-promotion version mismatch')", "req(index['INDEX_VERSION'] == '1.3.8', 'Index CEA-static-revalidation version mismatch')")
    one_text(v073,
        "    others = [e for e in index['entries'] if e['package_identity'] not in {CW_PACKAGE, SFV_PACKAGE}]\n    req(len(others) == 3 and all(e['availability_state'] == PENDING_STATIC for e in others), 'remaining Specialist lifecycle not pending-static')\n    req(all(e['foundation_compatibility_identity'] == SET007 for e in others), 'remaining historical compatibility identity changed')\n    req(all(e['current_foundation_compatibility_state'] == 'REVALIDATION_REQUIRED_NOT_INFERRED_FROM_INDEX_RESEAL' for e in others), 'remaining SET_008 compatibility inferred')\n    prog = index['validation_state'].get('set008_static_revalidation_progress', {})\n    req(prog.get('passed_package_identities') == [CW_PACKAGE, SFV_PACKAGE] and prog.get('passed_count') == 2 and prog.get('pending_count') == 3 and prog.get('behavioral_revalidation_ready_package_identities') == [] and prog.get('behavioral_revalidation_passed_package_identities') == [CW_PACKAGE, SFV_PACKAGE] and prog.get('behavioral_revalidation_passed_count') == 2, 'Index SET_008 progress mismatch')",
        "    cea = [e for e in index['entries'] if e['package_identity'] == CEA_PACKAGE]\n    req(len(cea) == 1, 'CEA index entry missing')\n    cae = cea[0]\n    req(cae['availability_state'] == PENDING_BEHAVIOR, 'CEA lifecycle not pending behavioral revalidation')\n    req(cae['foundation_compatibility_identity'] == FOUNDATION_ID, 'CEA SET_008 identity missing')\n    req(cae['current_foundation_compatibility_state'] == 'STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING', 'CEA SET_008 static state mismatch')\n    others = [e for e in index['entries'] if e['package_identity'] not in {CW_PACKAGE, SFV_PACKAGE, CEA_PACKAGE}]\n    req(len(others) == 2 and all(e['availability_state'] == PENDING_STATIC for e in others), 'remaining Specialist lifecycle not pending-static')\n    req(all(e['foundation_compatibility_identity'] == SET007 for e in others), 'remaining historical compatibility identity changed')\n    req(all(e['current_foundation_compatibility_state'] == 'REVALIDATION_REQUIRED_NOT_INFERRED_FROM_INDEX_RESEAL' for e in others), 'remaining SET_008 compatibility inferred')\n    prog = index['validation_state'].get('set008_static_revalidation_progress', {})\n    req(prog.get('passed_package_identities') == [CEA_PACKAGE, CW_PACKAGE, SFV_PACKAGE] and prog.get('passed_count') == 3 and prog.get('pending_count') == 2 and prog.get('behavioral_revalidation_ready_package_identities') == [CEA_PACKAGE] and prog.get('behavioral_revalidation_passed_package_identities') == [CW_PACKAGE, SFV_PACKAGE] and prog.get('behavioral_revalidation_passed_count') == 2, 'Index SET_008 progress mismatch')")
    one_text(v073,
        "    migrator = load_migrator()",
        "    cea_dir = ROOT / 'profiles' / 'capability ecology architect'\n    for name in [\n        'AIR_DOMAIN_CAPABILITY_REGISTRY.json',\n        'AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json',\n        'AIR_CAPABILITY_ECOLOGY_ARCHITECT.json',\n        'AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json',\n    ]:\n        obj = load(cea_dir / name)\n        fc = obj['foundation_compatibility']\n        req(fc.get('target_identity') == FOUNDATION_ID and fc.get('compatibility_state') == 'ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008', f'{name}: CEA SET_008 compatibility missing')\n        hr = next(x for x in fc['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')\n        req(hr.get('template_revision') == 19 and hr.get('revision_fields') == ['template_revision', 'user_revision'] and 'card_revision' not in hr, f'{name}: CEA stale Handoff revision contract')\n        rr = fc.get('route_map_discovery_input', {})\n        req(rr.get('version') == '1.2.2' and rr.get('sha256') == sha(ROOT / 'catalog/AIR_RUNTIME_ROUTE_MAP.json'), f'{name}: CEA stale Route Map receipt')\n        req(obj.get('STATUS') == 'V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING', f'{name}: CEA static lifecycle mismatch')\n    ceam = load(cea_dir / 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json')\n    req(ceam['foundation_compatibility'].get('target_identity') == FOUNDATION_ID, 'CEA manifest target identity stale')\n    req(ceam['package_validation_state'].get('behavioral_revalidation') == 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE', 'CEA behavioral state overclaimed')\n    req(ceam['package_validation_state'].get('component_internal_foundation_compatibility') == 'PASS_SET_008_EXACT_RECEIPTS', 'CEA component receipt state stale')\n\n    migrator = load_migrator()")
    one_text(v073, "print('specialist_index', '1.3.3 pending SET_008 static revalidation')", "print('specialist_index', '1.3.8 pending SET_008 static revalidation')")

    v073mut = ROOT / 'tools' / 'test_air_v073_release_seal_mutations.py'
    one_text(v073mut, "add('V073-N10-INDEX-VERSION-ROLLBACK', idxmut(lambda o: o.__setitem__('INDEX_VERSION', '1.3.6')))", "add('V073-N10-INDEX-VERSION-ROLLBACK', idxmut(lambda o: o.__setitem__('INDEX_VERSION', '1.3.7')))")
    one_text(v073mut,
        "    add('V073-N21-SFV-COMPONENT-BEHAVIORAL-ROLLBACK', sfv_component_behavioral_rollback)\n    killed = 0",
        "    add('V073-N21-SFV-COMPONENT-BEHAVIORAL-ROLLBACK', sfv_component_behavioral_rollback)\n\n    add('V073-N22-CEA-SET007-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2').__setitem__('foundation_compatibility_identity', 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007')))\n    add('V073-N23-CEA-PENDING-STATIC-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2').__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION')))\n\n    def cea_card_revision(d: Path):\n        p = d / 'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT.json'; o = load(p)\n        hr = next(x for x in o['foundation_compatibility']['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')\n        hr['card_revision'] = 18\n        dump(p, o)\n    add('V073-N24-CEA-CARD-REVISION-RESTORED', cea_card_revision)\n\n    def cea_route_map_rollback(d: Path):\n        p = d / 'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json'; o = load(p)\n        o['foundation_compatibility']['route_map_discovery_input']['version'] = '1.2.1'\n        dump(p, o)\n    add('V073-N25-CEA-ROUTE-MAP-ROLLBACK', cea_route_map_rollback)\n    killed = 0")

    # Verify the candidate before producing any permanent commit.
    run(sys.executable, 'tools/validate_air_suite.py')

    # Restore the transport/bootstrap file so it cannot enter the permanent diff.
    run('git', 'checkout', BASE, '--', 'tools/apply_r1_remediation.py')

    changed = set(subprocess.check_output(['git', 'diff', '--name-only', BASE], cwd=ROOT, text=True).splitlines())
    req(changed == PERMANENT_PATHS, f'permanent path scope mismatch: {sorted(changed)}')

    run('git', 'config', 'user.name', 'github-actions[bot]')
    run('git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
    run('git', 'add', '--', *sorted(PERMANENT_PATHS))
    run('git', 'commit', '-m', 'specialists: revalidate Capability Ecology Architect for SET_008 [r1-applied]')
    run('git', 'push')
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    print('CEA SET_008 static carrier PASS', sha, flush=True)


if __name__ == '__main__':
    main()
