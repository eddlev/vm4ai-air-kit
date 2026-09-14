from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
EXPECTED_MAIN = 'b39078347a1066952e58a8648a92ad70e39a220a'
BRANCH = 'audit-remediation-r1-939801a9'
SET007 = 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'
SET008 = 'AIR_FOUNDATION_2_6_3_OBJECT_CONTRACT_SET_008'
SET007_COMPAT = 'ALIGNED_TO_AIR_2_6_2_OBJECT_CONTRACT_SET_007'
SET008_COMPAT = 'ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008'
PENDING_STATIC = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION'
PENDING_BEHAVIOR = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'
CW_PACKAGE = 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'
CW_DIR = ROOT / 'profiles' / 'public surface copywriting specialist'
GENERATED_AT = '2026-09-14T20:58:00Z'

FOUNDATION = {
    'AIR_CORE_RUNTIME.md': {'version': '2.6.3', 'sha256': 'e6915ad2f8af6a75f68d52eac3a7cf45d2dd9a3d300310c0d79c11a4033c8371', 'size_bytes': 413548, 'line_count': 7839},
    'AIR_CONTROL_SURFACE.md': {'version': '2.6.3', 'sha256': '0ef70702500350aedf30ff3dc29fc5bc4533df2c00c505470aca01a70763e3ff', 'size_bytes': 170669, 'line_count': 3317},
    'AIR_GOV.md': {'version': '2.3.2', 'sha256': '80f037b38b69d75436ddf2ec7b1dc757e84ab65d17aaeaf450cb963af44b4842', 'size_bytes': 31075, 'line_count': 564},
    'AIR_DEFAULT_STARTER_PROFILE.json': {'version': '2.6.3', 'sha256': '465cac6cb3303d98fed14a9110061f2b487cdec364e787f4310ffcbf35aa649c', 'size_bytes': 177103, 'line_count': 3748},
    'AIR_HANDOFF_CARD_TEMPLATE.json': {'version': '2.3.0', 'sha256': '05ccdbc18ad82e81ab56ed69e524d5fa7b9dcbd19a65ed7662f422179af922e2', 'size_bytes': 126877, 'line_count': 2327},
}
ROUTE = {'version': '1.2.2', 'sha256': 'a8817d0abe078a2b94f87562386ac5e63a575b0926c0b2d050a6e470f578e89c', 'size_bytes': 39163, 'line_count': 1095}
PERMANENT = {
    'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST.json',
    'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json',
    'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json',
    'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',
    'tools/validate_air_r7_remediation.py',
    'tools/test_air_r7_mutations.py',
    'tools/validate_air_v073_release_seal.py',
    'tools/test_air_v073_release_seal_mutations.py',
}


def sh(*args: str, capture: bool = False) -> str:
    p = subprocess.run(list(args), cwd=ROOT, text=True, capture_output=capture, check=True)
    return p.stdout.strip() if capture else ''


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def meta(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'size_bytes': len(raw), 'line_count': len(raw.decode('utf-8').splitlines())}


def one(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected one replacement anchor, observed {n}')
    return text.replace(old, new, 1)


def update_foundation_compatibility(obj: dict, manifest: bool = False) -> None:
    fc = obj['foundation_compatibility']
    if 'target_identity' in fc:
        fc['target_identity'] = SET008
    if 'foundation_candidate_set_identity' in fc:
        fc['foundation_candidate_set_identity'] = SET008
    if 'compatibility_state' in fc:
        fc['compatibility_state'] = SET008_COMPAT
    if manifest and 'state' in fc:
        fc['state'] = 'COORDINATED_SET_008_RESEAL_STATIC_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING'
    tfv = fc.get('target_foundation_versions')
    if isinstance(tfv, dict):
        tfv.update({'core': '2.6.3', 'control': '2.6.3', 'governance': '2.3.2', 'starter': '2.6.3', 'handoff_schema': '2.3.0'})
    for rec in fc.get('required_files', []):
        name = rec.get('filename')
        if name not in FOUNDATION:
            continue
        rec.update(FOUNDATION[name])
        if name == 'AIR_HANDOFF_CARD_TEMPLATE.json':
            rec.pop('card_revision', None)
            rec['template_revision'] = 19
            rec['revision_fields'] = ['template_revision', 'user_revision']
    for key in ('route_map_discovery_input', 'foundation_adjacent_route_map'):
        rr = fc.get(key)
        if isinstance(rr, dict):
            rr.update(ROUTE)
    ir = obj.get('integration_refresh')
    if isinstance(ir, dict) and 'foundation_identity_state' in ir:
        ir['foundation_identity_state'] = 'OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_' + SET008


def patch_copywriting_package() -> None:
    component_names = [
        'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST.json',
        'AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json',
    ]
    for name in component_names:
        p = CW_DIR / name
        o = load(p)
        old = str(o['STATUS'])
        new = old.replace('OBJECT_CONTRACT_SET_007_RESEAL', 'OBJECT_CONTRACT_SET_008_RESEAL')
        if old == new:
            raise RuntimeError(f'{name}: SET_007 status anchor missing')
        o['STATUS'] = new
        update_foundation_compatibility(o)
        dump(p, o)

    mp = CW_DIR / 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json'
    m = load(mp)
    old = str(m['status'])
    new = old.replace('OBJECT_CONTRACT_SET_007_RESEAL', 'OBJECT_CONTRACT_SET_008_RESEAL')
    if old == new:
        raise RuntimeError('copywriting manifest SET_007 status anchor missing')
    m['status'] = new
    update_foundation_compatibility(m, manifest=True)
    by_name = {c['filename']: c for c in m['components']}
    for name in component_names:
        cp = CW_DIR / name
        co = load(cp)
        cm = meta(cp)
        by_name[name].update(cm)
        by_name[name]['status'] = co['STATUS']
        by_name[name]['availability_state'] = 'VALIDATED_AVAILABLE_UNBOUND'
    pvs = m['package_validation_state']
    pvs['static_design_validation'] = 'PASS_R7_DETERMINISTIC_STATIC_SUITE'
    pvs['behavioral_revalidation'] = 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'
    pvs['foundation_reseal'] = 'PASS_COORDINATED_SET_008_RESEAL'
    pvs['release_catalog_registration'] = 'INCLUDED_IN_SET_008_V073_CANDIDATE_INDEX_PENDING_BEHAVIORAL_REVALIDATION'
    pvs['component_internal_foundation_compatibility'] = 'PASS_SET_008_EXACT_RECEIPTS'
    m['generated_at'] = GENERATED_AT
    dump(mp, m)

    ip = ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json'
    idx = load(ip)
    idx['INDEX_VERSION'] = '1.3.4'
    idx['generated_at'] = GENERATED_AT
    entries = idx['entries']
    cw = [e for e in entries if e['package_identity'] == CW_PACKAGE]
    if len(cw) != 1:
        raise RuntimeError(f'copywriting index entry count {len(cw)} != 1')
    ce = cw[0]
    ce['manifest_sha256'] = meta(mp)['sha256']
    ce['foundation_compatibility_identity'] = SET008
    ce['availability_state'] = PENDING_BEHAVIOR
    ce['current_foundation_compatibility_target'] = SET008
    ce['current_foundation_compatibility_state'] = 'STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING'
    pending = [e['package_identity'] for e in entries if e['package_identity'] != CW_PACKAGE]
    vs = idx['validation_state']
    vs['manifest_hash_closure'] = 'MIXED_SET_007_AND_SET_008_RECEIPTS_COPYWRITING_SET_008_STATIC_PASS_OTHER_PACKAGES_PENDING'
    vs['component_internal_foundation_compatibility'] = 'COPYWRITING_PASS_SET_008_REMAINING_PACKAGES_REVALIDATION_REQUIRED'
    vs['set008_static_revalidation_progress'] = {
        'passed_package_identities': [CW_PACKAGE],
        'pending_package_identities': pending,
        'passed_count': 1,
        'pending_count': 4,
        'behavioral_revalidation_ready_package_identities': [CW_PACKAGE],
    }
    dump(ip, idx)


def patch_r7_validator() -> None:
    p = ROOT / 'tools' / 'validate_air_r7_remediation.py'
    s = p.read_text(encoding='utf-8')
    s = one(s,
"FOUNDATION_ID='AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'\nFOUNDATION_STATE='OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_'+FOUNDATION_ID\nSTATIC_PASS='PASS_R7_DETERMINISTIC_STATIC_SUITE'\nBEHAVIOR_PENDING='PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'\nSPECIALIST_COMPAT='ALIGNED_TO_AIR_2_6_2_OBJECT_CONTRACT_SET_007'",
"FOUNDATION_ID='AIR_FOUNDATION_2_6_3_OBJECT_CONTRACT_SET_008'\nLEGACY_FOUNDATION_ID='AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'\nFOUNDATION_STATE='OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_'+LEGACY_FOUNDATION_ID\nSET008_FOUNDATION_STATE='OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_'+FOUNDATION_ID\nSTATIC_PASS='PASS_R7_DETERMINISTIC_STATIC_SUITE'\nBEHAVIOR_PENDING='PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'\nSPECIALIST_COMPAT='ALIGNED_TO_AIR_2_6_2_OBJECT_CONTRACT_SET_007'\nSET008_SPECIALIST_COMPAT='ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008'\nPENDING_STATIC='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION'\nPENDING_BEHAVIOR='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'\nCW_PACKAGE='AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'\nCW_DIR='public surface copywriting specialist'",
'R7 constants')
    s = one(s,
" idx=parsed[ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json']\n req(idx['status']=='AIR_2_6_3_OBJECT_CONTRACT_SET_008_FIVE_PACKAGE_INDEX_V072_PATCH2_CANDIDATE_PENDING_STATIC_VALIDATION','v073 current index status incoherent')",
" idx=parsed[ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json']\n req(idx.get('INDEX_VERSION')=='1.3.4','Copywriting SET_008 index version mismatch')\n req(idx['foundation_compatibility_catalog'].get('identity')==FOUNDATION_ID,'SET_008 catalog identity mismatch')\n req(idx['status']=='AIR_2_6_3_OBJECT_CONTRACT_SET_008_FIVE_PACKAGE_INDEX_V072_PATCH2_CANDIDATE_PENDING_STATIC_VALIDATION','v073 current index status incoherent')",
'R7 index header')
    s = one(s,
" req(idx['validation_state'].get('behavioral_revalidation')=='BLOCKED_PENDING_SET_008_STATIC_COMPATIBILITY_REVALIDATION','R7 index behavioral state must remain blocked pending static revalidation')\n req(idx['validation_state'].get('release_publication_state')=='EXTERNAL_RELEASE_STATE_NOT_RUNTIME_AUTHORITY','R7 publication authority changed')",
" req(idx['validation_state'].get('behavioral_revalidation')=='BLOCKED_PENDING_SET_008_STATIC_COMPATIBILITY_REVALIDATION','R7 index behavioral state must remain blocked pending static revalidation')\n prog=idx['validation_state'].get('set008_static_revalidation_progress',{})\n req(prog.get('passed_package_identities')==[CW_PACKAGE] and prog.get('passed_count')==1 and prog.get('pending_count')==4 and prog.get('behavioral_revalidation_ready_package_identities')==[CW_PACKAGE],'R7 SET_008 progress carrier mismatch')\n req(len(prog.get('pending_package_identities',[]))==4 and CW_PACKAGE not in prog.get('pending_package_identities',[]),'R7 SET_008 pending package set mismatch')\n req(idx['validation_state'].get('release_publication_state')=='EXTERNAL_RELEASE_STATE_NOT_RUNTIME_AUTHORITY','R7 publication authority changed')",
'R7 progress')
    s = one(s,
" for e in idx['entries']:\n  req(e['foundation_compatibility_identity']==FOUNDATION_ID,'index entry Foundation identity stale')\n  req(e['availability_state']=='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION','006 index entry lifecycle mismatch')",
" for e in idx['entries']:\n  if e['package_identity']==CW_PACKAGE:\n   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'Copywriting index Foundation identity not SET_008')\n   req(e['availability_state']==PENDING_BEHAVIOR,'Copywriting index lifecycle not pending behavioral revalidation')\n   req(e.get('current_foundation_compatibility_state')=='STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING','Copywriting SET_008 state mismatch')\n  else:\n   req(e['foundation_compatibility_identity']==LEGACY_FOUNDATION_ID,'non-Copywriting index Foundation identity changed before revalidation')\n   req(e['availability_state']==PENDING_STATIC,'non-Copywriting index lifecycle changed before static revalidation')",
'R7 index entries')
    s = one(s,
"  req(fc.get('compatibility_state')==SPECIALIST_COMPAT,f'{p}: stale Foundation compatibility state')",
"  is_cw=CW_DIR in str(p)\n  expected_compat=SET008_SPECIALIST_COMPAT if is_cw else SPECIALIST_COMPAT\n  req(fc.get('compatibility_state')==expected_compat,f'{p}: stale Foundation compatibility state')\n  if is_cw:\n   req(fc.get('target_identity')==FOUNDATION_ID,f'{p}: Copywriting target identity not SET_008')\n   h=next((x for x in fc.get('required_files',[]) if x.get('filename')=='AIR_HANDOFF_CARD_TEMPLATE.json'),{})\n   req(h.get('template_revision')==19 and h.get('revision_fields')==['template_revision','user_revision'] and 'card_revision' not in h,f'{p}: Copywriting Handoff revision split stale')\n   rr=fc.get('route_map_discovery_input') or fc.get('foundation_adjacent_route_map') or {}\n   req(rr.get('version')=='1.2.2' and rr.get('sha256')=='a8817d0abe078a2b94f87562386ac5e63a575b0926c0b2d050a6e470f578e89c',f'{p}: Copywriting Route Map receipt stale')",
'R7 profile compatibility')
    s = one(s,
"   count+=1;req(ir['foundation_identity_state']==FOUNDATION_STATE,f'{p}: stale current Foundation identity')",
"   count+=1\n   expected_state=SET008_FOUNDATION_STATE if CW_DIR in str(p) else FOUNDATION_STATE\n   req(ir['foundation_identity_state']==expected_state,f'{p}: stale current Foundation identity')",
'R7 integration refresh')
    anchor = "   req(c.get('availability_state')==avail(cst),f'{p}: component availability mirror mismatch {fn}')\n for e in idx['entries']:"
    insert = "   req(c.get('availability_state')==avail(cst),f'{p}: component availability mirror mismatch {fn}')\n cwman=parsed[ROOT/'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json']\n req(cwman['foundation_compatibility'].get('state')=='COORDINATED_SET_008_RESEAL_STATIC_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING','Copywriting manifest SET_008 state mismatch')\n cpvs=cwman.get('package_validation_state',{})\n req(cpvs.get('foundation_reseal')=='PASS_COORDINATED_SET_008_RESEAL' and cpvs.get('component_internal_foundation_compatibility')=='PASS_SET_008_EXACT_RECEIPTS','Copywriting SET_008 manifest validation state mismatch')\n for e in idx['entries']:"
    s = one(s, anchor, insert, 'R7 Copywriting manifest assertion')
    p.write_text(s, encoding='utf-8')


def patch_r7_mutations() -> None:
    p = ROOT / 'tools' / 'test_air_r7_mutations.py'
    s = p.read_text(encoding='utf-8')
    anchor = "if run(ROOT)!=0:raise SystemExit('R7-MUTATION-BASELINE failed')"
    extra = "add('R7-N21-COPYWRITING-INDEX-STATIC-ROLLBACK','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:next(e for e in o['entries'] if e['package_identity']=='AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2').__setitem__('availability_state','RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION')))\nadd('R7-N22-COPYWRITING-INDEX-SET007-ROLLBACK','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:next(e for e in o['entries'] if e['package_identity']=='AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2').__setitem__('foundation_compatibility_identity','AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007')))\nadd('R7-N23-COPYWRITING-CARD-REVISION-RESTORED','profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST.json',jfn(lambda o:next(x for x in o['foundation_compatibility']['required_files'] if x['filename']=='AIR_HANDOFF_CARD_TEMPLATE.json').__setitem__('card_revision',18)))\n"
    s = one(s, anchor, extra + anchor, 'R7 mutation additions')
    p.write_text(s, encoding='utf-8')


def patch_release_validator() -> None:
    p = ROOT / 'tools' / 'validate_air_v073_release_seal.py'
    s = p.read_text(encoding='utf-8')
    s = one(s,
"SET007 = 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'\nPENDING_STATIC = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION'",
"SET007 = 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'\nPENDING_STATIC = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION'\nPENDING_BEHAVIOR = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'\nCW_PACKAGE = 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'",
'release constants')
    s = one(s, "req(index['INDEX_VERSION'] == '1.3.3', 'Index version mismatch')", "req(index['INDEX_VERSION'] == '1.3.4', 'Index version mismatch')", 'release index version')
    old = "    req(all(e['availability_state'] == PENDING_STATIC for e in index['entries']), 'Index entry lifecycle not uniformly pending-static')\n    req(all(e['foundation_compatibility_identity'] == SET007 for e in index['entries']), 'Specialist historical compatibility identity was rewritten')\n    req(all(e['current_foundation_compatibility_state'] == 'REVALIDATION_REQUIRED_NOT_INFERRED_FROM_INDEX_RESEAL' for e in index['entries']), 'Specialist SET_008 compatibility inferred')"
    new = "    cw = [e for e in index['entries'] if e['package_identity'] == CW_PACKAGE]\n    req(len(cw) == 1, 'Copywriting index entry missing')\n    ce = cw[0]\n    req(ce['availability_state'] == PENDING_BEHAVIOR, 'Copywriting lifecycle not pending behavioral revalidation')\n    req(ce['foundation_compatibility_identity'] == FOUNDATION_ID, 'Copywriting SET_008 identity missing')\n    req(ce['current_foundation_compatibility_state'] == 'STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING', 'Copywriting SET_008 state mismatch')\n    others = [e for e in index['entries'] if e['package_identity'] != CW_PACKAGE]\n    req(len(others) == 4 and all(e['availability_state'] == PENDING_STATIC for e in others), 'remaining Specialist lifecycle not pending-static')\n    req(all(e['foundation_compatibility_identity'] == SET007 for e in others), 'non-Copywriting historical compatibility identity changed')\n    req(all(e['current_foundation_compatibility_state'] == 'REVALIDATION_REQUIRED_NOT_INFERRED_FROM_INDEX_RESEAL' for e in others), 'non-Copywriting SET_008 compatibility inferred')\n    prog = index['validation_state'].get('set008_static_revalidation_progress', {})\n    req(prog.get('passed_package_identities') == [CW_PACKAGE] and prog.get('passed_count') == 1 and prog.get('pending_count') == 4, 'Index SET_008 progress mismatch')"
    s = one(s, old, new, 'release mixed lifecycle')
    manifest_anchor = "        req(sha(targets[0]) == entry['manifest_sha256'], f\"manifest hash changed {entry['manifest_filename']}\")\n\n    migrator = load_migrator()"
    manifest_insert = "        req(sha(targets[0]) == entry['manifest_sha256'], f\"manifest hash changed {entry['manifest_filename']}\")\n\n    cw_dir = ROOT / 'profiles' / 'public surface copywriting specialist'\n    for name in ['AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST.json', 'AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json']:\n        obj = load(cw_dir / name)\n        fc = obj['foundation_compatibility']\n        req(fc.get('target_identity') == FOUNDATION_ID and fc.get('compatibility_state') == 'ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008', f'{name}: SET_008 compatibility missing')\n        hr = next(x for x in fc['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')\n        req(hr.get('template_revision') == 19 and hr.get('revision_fields') == ['template_revision', 'user_revision'] and 'card_revision' not in hr, f'{name}: stale Handoff revision contract')\n    cwm = load(cw_dir / 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json')\n    req(cwm['foundation_compatibility'].get('target_identity') == FOUNDATION_ID, 'Copywriting manifest target identity stale')\n    req(cwm['package_validation_state'].get('foundation_reseal') == 'PASS_COORDINATED_SET_008_RESEAL', 'Copywriting manifest reseal state stale')\n    req(cwm['package_validation_state'].get('behavioral_revalidation') == 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE', 'Copywriting behavioral state overclaimed')\n\n    migrator = load_migrator()"
    s = one(s, manifest_anchor, manifest_insert, 'release copywriting package checks')
    new_index_hash = hashlib.sha256((ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json').read_bytes()).hexdigest()
    s = one(s, "'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json': 'fdf21d97c86355a364775a04d9af606216f54163d3299fa6946a328b98664d6a',", f"'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json': '{new_index_hash}',", 'release index hash')
    p.write_text(s, encoding='utf-8')


def patch_release_mutations() -> None:
    p = ROOT / 'tools' / 'test_air_v073_release_seal_mutations.py'
    s = p.read_text(encoding='utf-8')
    anchor = "    killed = 0\n"
    extra = "    add('V073-N07-COPYWRITING-SET007-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2').__setitem__('foundation_compatibility_identity', 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007')))\n    add('V073-N08-COPYWRITING-PENDING-STATIC-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2').__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION')))\n\n    def copywriting_card_revision(d: Path):\n        p = d / 'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST.json'; o = load(p)\n        hr = next(x for x in o['foundation_compatibility']['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')\n        hr['card_revision'] = 18\n        dump(p, o)\n    add('V073-N09-COPYWRITING-CARD-REVISION-RESTORED', copywriting_card_revision)\n\n    add('V073-N10-INDEX-VERSION-ROLLBACK', idxmut(lambda o: o.__setitem__('INDEX_VERSION', '1.3.3')))\n\n"
    s = one(s, anchor, extra + anchor, 'release mutation additions')
    p.write_text(s, encoding='utf-8')


def verify_and_commit() -> None:
    sh('git', 'fetch', 'origin', 'main', '--depth=1')
    actual_main = sh('git', 'rev-parse', 'origin/main', capture=True)
    if actual_main != EXPECTED_MAIN:
        raise RuntimeError(f'main drifted: {actual_main} != {EXPECTED_MAIN}')

    patch_copywriting_package()
    patch_r7_validator()
    patch_r7_mutations()
    patch_release_validator()
    patch_release_mutations()

    sh(sys.executable, 'tools/reseal_air_candidate.py', '--check')
    sh(sys.executable, 'tools/validate_air_suite.py')

    original_bootstrap = sh('git', 'show', 'origin/main:tools/apply_r1_remediation.py', capture=True) + '\n'
    (ROOT / 'tools' / 'apply_r1_remediation.py').write_text(original_bootstrap, encoding='utf-8')
    for d in ROOT.rglob('__pycache__'):
        if d.is_dir():
            shutil.rmtree(d)
    for pyc in ROOT.rglob('*.pyc'):
        try:
            pyc.unlink()
        except FileNotFoundError:
            pass

    changed = set(filter(None, sh('git', 'diff', '--name-only', 'origin/main', capture=True).splitlines()))
    untracked = set(filter(None, sh('git', 'ls-files', '--others', '--exclude-standard', capture=True).splitlines()))
    net = changed | untracked
    if net != PERMANENT:
        raise RuntimeError(f'final net diff mismatch: expected={sorted(PERMANENT)} observed={sorted(net)}')

    sh('git', 'config', 'user.name', 'github-actions[bot]')
    sh('git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
    sh('git', 'add', *sorted(PERMANENT), 'tools/apply_r1_remediation.py')
    sh('git', 'commit', '-m', 'specialists: revalidate Public-Surface Copywriting for SET_008 [r1-applied]')
    sh('git', 'push', 'origin', f'HEAD:{BRANCH}')
    print('COPYWRITING SET_008 STATIC REMEDIATION: PASS')
    print('final_net_paths', len(PERMANENT))
    print('behavioral_state', 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE')


if __name__ == '__main__':
    verify_and_commit()
