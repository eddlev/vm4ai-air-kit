from __future__ import annotations
import hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
EXPECTED_BASE = '89b12f0043844e7d7f42c2cc9b990ddb37c5d211'
FOUNDATION_ID = 'AIR_FOUNDATION_2_6_3_OBJECT_CONTRACT_SET_008'
SET007_ID = 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'
SET008_COMPAT = 'ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008'
PENDING_STATIC = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION'
PENDING_BEHAVIOR = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'
CW_PACKAGE = 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'
SFV_PACKAGE = 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2'
SFV_DIR = ROOT / 'profiles' / 'specification first verification specialist'
PERMANENT = [
    'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json',
    'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json',
    'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json',
    'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json',
    'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json',
    'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',
    'tools/validate_air_r7_remediation.py',
    'tools/test_air_r7_mutations.py',
    'tools/validate_air_v073_release_seal.py',
    'tools/test_air_v073_release_seal_mutations.py',
]
BOOTSTRAP = 'tools/apply_r1_remediation.py'
HISTORY = {
    'source_baseline','mainline_release_binding','t7_change_record','historical_release_catalogs',
    'source_candidate_manifest','change_history','release_history','historical_records'
}

class E(Exception):
    pass

def req(c, m):
    if not c:
        raise E(m)

def run(cmd, check=True):
    print('+', ' '.join(cmd), flush=True)
    p = subprocess.run(cmd, cwd=ROOT, text=True)
    if check and p.returncode != 0:
        raise E(f'command failed ({p.returncode}): {" ".join(cmd)}')
    return p

def out(cmd):
    return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def dump(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def meta(path):
    raw = Path(path).read_bytes()
    return {
        'sha256': hashlib.sha256(raw).hexdigest(),
        'size_bytes': len(raw),
        'line_count': len(raw.decode('utf-8').splitlines()),
    }

def historical(path):
    return any(x in HISTORY or str(x).startswith('historical_') for x in path)

def rewrite_current(node, path=()):
    if historical(path):
        return node
    if isinstance(node, dict):
        return {k: rewrite_current(v, path + (k,)) for k, v in node.items()}
    if isinstance(node, list):
        return [rewrite_current(v, path + (str(i),)) for i, v in enumerate(node)]
    if isinstance(node, str):
        s = node
        s = s.replace(SET007_ID, FOUNDATION_ID)
        s = s.replace('OBJECT_CONTRACT_SET_007_RESEAL', 'OBJECT_CONTRACT_SET_008_RESEAL')
        s = s.replace('COORDINATED_SET_007_RESEAL', 'COORDINATED_SET_008_RESEAL')
        s = s.replace('PASS_SET_007_EXACT_RECEIPTS', 'PASS_SET_008_EXACT_RECEIPTS')
        return s
    return node

def replace_once(text, old, new, label):
    n = text.count(old)
    req(n == 1, f'{label}: expected one anchor, found {n}')
    return text.replace(old, new, 1)

def insert_before_once(text, anchor, insertion, label):
    n = text.count(anchor)
    req(n == 1, f'{label}: expected one anchor, found {n}')
    return text.replace(anchor, insertion + anchor, 1)

def refresh_refs(node, metas):
    if isinstance(node, dict):
        fn = node.get('filename')
        if fn in metas:
            m = metas[fn]
            for k in ('sha256', 'size_bytes', 'line_count'):
                if k in node:
                    node[k] = m[k]
        for v in node.values():
            refresh_refs(v, metas)
    elif isinstance(node, list):
        for v in node:
            refresh_refs(v, metas)

run(['git', 'fetch', '--no-tags', '--deepen=1', 'origin', 'audit-remediation-r1-939801a9'])
base = out(['git', 'rev-parse', 'HEAD^'])
req(base == EXPECTED_BASE, f'carrier base drift: {base}')
req(out(['git', 'status', '--porcelain']) == '', 'carrier worktree not clean at entry')

foundation_files = {
    'AIR_CORE_RUNTIME.md': ROOT/'prompts/AIR_CORE_RUNTIME.md',
    'AIR_CONTROL_SURFACE.md': ROOT/'prompts/AIR_CONTROL_SURFACE.md',
    'AIR_GOV.md': ROOT/'prompts/AIR_GOV.md',
    'AIR_DEFAULT_STARTER_PROFILE.json': ROOT/'prompts/AIR_DEFAULT_STARTER_PROFILE.json',
    'AIR_HANDOFF_CARD_TEMPLATE.json': ROOT/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json',
}
foundation_versions = {
    'AIR_CORE_RUNTIME.md': '2.6.3',
    'AIR_CONTROL_SURFACE.md': '2.6.3',
    'AIR_GOV.md': '2.3.2',
    'AIR_DEFAULT_STARTER_PROFILE.json': '2.6.3',
    'AIR_HANDOFF_CARD_TEMPLATE.json': '2.3.0',
}
foundation_meta = {k: meta(v) for k, v in foundation_files.items()}
route_path = ROOT/'catalog/AIR_RUNTIME_ROUTE_MAP.json'
route = load(route_path)
route_meta = meta(route_path)
req(route.get('MAP_VERSION') == '1.2.2', 'Route Map is not 1.2.2')
handoff = load(foundation_files['AIR_HANDOFF_CARD_TEMPLATE.json'])['AIR_HANDOFF_CARD']
req(handoff.get('template_revision') == 19, 'Handoff template revision is not 19')

def update_foundation_compat(obj):
    fc = obj.get('foundation_compatibility')
    req(isinstance(fc, dict), 'foundation_compatibility missing')
    fc['target_identity'] = FOUNDATION_ID
    fc['compatibility_state'] = SET008_COMPAT
    for rec in fc.get('required_files', []):
        fn = rec.get('filename')
        if fn in foundation_files:
            rec['version'] = foundation_versions[fn]
            rec.update(foundation_meta[fn])
            if fn == 'AIR_HANDOFF_CARD_TEMPLATE.json':
                rec.pop('card_revision', None)
                rec['template_revision'] = 19
                rec['revision_fields'] = ['template_revision', 'user_revision']
    tfv = fc.get('target_foundation_versions')
    if isinstance(tfv, dict):
        tfv['core'] = '2.6.3'
        tfv['control'] = '2.6.3'
        tfv['governance'] = '2.3.2'
        tfv['starter'] = '2.6.3'
        tfv['handoff_schema'] = '2.3.0'
    if 'foundation_candidate_set_identity' in fc:
        fc['foundation_candidate_set_identity'] = FOUNDATION_ID
    rr = fc.get('route_map_discovery_input') or fc.get('foundation_adjacent_route_map')
    if isinstance(rr, dict):
        rr['version'] = '1.2.2'
        rr.update(route_meta)
    return obj

component_names = [
    'AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json',
    'AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json',
    'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json',
    'AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json',
]
objs = {}
for name in component_names:
    p = SFV_DIR/name
    o = rewrite_current(load(p))
    update_foundation_compat(o)
    objs[name] = o

req(objs['AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json'].get('STATUS') == 'DRAFT', 'Executor ceased to be DRAFT before write')

component_meta = {}
for name in component_names:
    o = objs[name]
    refresh_refs(o, component_meta)
    p = SFV_DIR/name
    dump(p, o)
    component_meta[name] = meta(p)

for name in component_names:
    o = load(SFV_DIR/name)
    def verify_refs(node):
        if isinstance(node, dict):
            fn = node.get('filename')
            if fn in component_meta and 'sha256' in node:
                req(node['sha256'] == component_meta[fn]['sha256'], f'{name}: stale dependency hash {fn}')
            for v in node.values():
                verify_refs(v)
        elif isinstance(node, list):
            for v in node:
                verify_refs(v)
    verify_refs(o)

manifest_path = SFV_DIR/'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json'
manifest = rewrite_current(load(manifest_path))
update_foundation_compat(manifest)
manifest['generated_at'] = '2026-09-15T05:28:00Z'
pvs = manifest.get('package_validation_state', {})
if 'behavioral_revalidation' in pvs:
    pvs['behavioral_revalidation'] = 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'
pvs['component_internal_foundation_compatibility'] = 'PASS_SET_008_EXACT_RECEIPTS'
refresh_refs(manifest, component_meta)
for c in manifest.get('components', []):
    fn = c.get('filename')
    if fn in component_meta:
        co = load(SFV_DIR/fn)
        st = str(co.get('STATUS') or co.get('status') or '')
        c['status'] = st
        c['availability_state'] = 'AVAILABLE_UNVALIDATED' if st == 'DRAFT' else 'VALIDATED_AVAILABLE_UNBOUND'
dump(manifest_path, manifest)
manifest_meta = meta(manifest_path)

idx_path = ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'
idx = load(idx_path)
req(idx.get('INDEX_VERSION') == '1.3.5', 'unexpected pre-SFV Index version')
idx['INDEX_VERSION'] = '1.3.6'
idx['generated_at'] = '2026-09-15T05:28:00Z'
ivs = idx['validation_state']
ivs['manifest_hash_closure'] = 'MIXED_SET_007_AND_SET_008_RECEIPTS_COPYWRITING_AND_SFV_SET_008_STATIC_PASS_OTHER_PACKAGES_PENDING'
ivs['component_internal_foundation_compatibility'] = 'COPYWRITING_AND_SFV_PASS_SET_008_REMAINING_PACKAGES_REVALIDATION_REQUIRED'
prog = ivs['set008_static_revalidation_progress']
prog['passed_package_identities'] = [CW_PACKAGE, SFV_PACKAGE]
prog['pending_package_identities'] = [
    'AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_V2',
    'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2',
    'AIR_GROUNDING_SPECIALIST_PACKAGE_V2',
]
prog['passed_count'] = 2
prog['pending_count'] = 3
prog['behavioral_revalidation_ready_package_identities'] = [SFV_PACKAGE]
prog['behavioral_revalidation_passed_package_identities'] = [CW_PACKAGE]
prog['behavioral_revalidation_passed_count'] = 1
sfve = next(e for e in idx['entries'] if e['package_identity'] == SFV_PACKAGE)
sfve['manifest_sha256'] = manifest_meta['sha256']
sfve['foundation_compatibility_identity'] = FOUNDATION_ID
sfve['availability_state'] = PENDING_BEHAVIOR
sfve['current_foundation_compatibility_target'] = FOUNDATION_ID
sfve['current_foundation_compatibility_state'] = 'STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING'
dump(idx_path, idx)
index_hash = meta(idx_path)['sha256']

p = ROOT/'tools/validate_air_r7_remediation.py'
s = p.read_text(encoding='utf-8')
s = replace_once(s,
"CW_PACKAGE='AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'\nCW_DIR='public surface copywriting specialist'\n",
"CW_PACKAGE='AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'\nSFV_PACKAGE='AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2'\nCW_DIR='public surface copywriting specialist'\nSFV_DIR='specification first verification specialist'\n",
'r7 constants')
s = replace_once(s,
"req(idx.get('INDEX_VERSION')=='1.3.5','Copywriting SET_008 behavioral promotion index version mismatch')",
"req(idx.get('INDEX_VERSION')=='1.3.6','SFV SET_008 static revalidation index version mismatch')",
'r7 index version')
s = replace_once(s,
"req(prog.get('passed_package_identities')==[CW_PACKAGE] and prog.get('passed_count')==1 and prog.get('pending_count')==4 and prog.get('behavioral_revalidation_ready_package_identities')==[] and prog.get('behavioral_revalidation_passed_package_identities')==[CW_PACKAGE] and prog.get('behavioral_revalidation_passed_count')==1,'R7 SET_008 progress carrier mismatch')\n req(len(prog.get('pending_package_identities',[]))==4 and CW_PACKAGE not in prog.get('pending_package_identities',[]),'R7 SET_008 pending package set mismatch')",
"req(prog.get('passed_package_identities')==[CW_PACKAGE,SFV_PACKAGE] and prog.get('passed_count')==2 and prog.get('pending_count')==3 and prog.get('behavioral_revalidation_ready_package_identities')==[SFV_PACKAGE] and prog.get('behavioral_revalidation_passed_package_identities')==[CW_PACKAGE] and prog.get('behavioral_revalidation_passed_count')==1,'R7 SET_008 progress carrier mismatch')\n req(len(prog.get('pending_package_identities',[]))==3 and CW_PACKAGE not in prog.get('pending_package_identities',[]) and SFV_PACKAGE not in prog.get('pending_package_identities',[]),'R7 SET_008 pending package set mismatch')",
'r7 progress')
s = replace_once(s,
"""  if e['package_identity']==CW_PACKAGE:
   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'Copywriting index Foundation identity not SET_008')
   req(e['availability_state']==RELEASED,'Copywriting index lifecycle not released after behavioral revalidation')
   req(e.get('current_foundation_compatibility_state')=='STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED' and e.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'Copywriting SET_008 behavioral state mismatch')
  else:
   req(e['foundation_compatibility_identity']==LEGACY_FOUNDATION_ID,'non-Copywriting index Foundation identity changed before revalidation')
   req(e['availability_state']==PENDING_STATIC,'non-Copywriting index lifecycle changed before static revalidation')
""",
"""  if e['package_identity']==CW_PACKAGE:
   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'Copywriting index Foundation identity not SET_008')
   req(e['availability_state']==RELEASED,'Copywriting index lifecycle not released after behavioral revalidation')
   req(e.get('current_foundation_compatibility_state')=='STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED' and e.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'Copywriting SET_008 behavioral state mismatch')
  elif e['package_identity']==SFV_PACKAGE:
   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'SFV index Foundation identity not SET_008')
   req(e['availability_state']==PENDING_BEHAVIOR,'SFV index lifecycle not pending behavioral revalidation')
   req(e.get('current_foundation_compatibility_state')=='STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING','SFV SET_008 static state mismatch')
  else:
   req(e['foundation_compatibility_identity']==LEGACY_FOUNDATION_ID,'remaining pending index Foundation identity changed before revalidation')
   req(e['availability_state']==PENDING_STATIC,'remaining pending index lifecycle changed before static revalidation')
""",
'r7 entry lifecycle')
s = replace_once(s,
"""  is_cw=CW_DIR in str(p)
  expected_compat=SET008_SPECIALIST_COMPAT if is_cw else SPECIALIST_COMPAT
  req(fc.get('compatibility_state')==expected_compat,f'{p}: stale Foundation compatibility state')
  if is_cw:
   req(fc.get('target_identity')==FOUNDATION_ID,f'{p}: Copywriting target identity not SET_008')
   h=next((x for x in fc.get('required_files',[]) if x.get('filename')=='AIR_HANDOFF_CARD_TEMPLATE.json'),{})
   req(h.get('template_revision')==19 and h.get('revision_fields')==['template_revision','user_revision'] and 'card_revision' not in h,f'{p}: Copywriting Handoff revision split stale')
   rr=fc.get('route_map_discovery_input') or fc.get('foundation_adjacent_route_map') or {}
   req(rr.get('version')=='1.2.2' and rr.get('sha256')=='a8817d0abe078a2b94f87562386ac5e63a575b0926c0b2d050a6e470f578e89c',f'{p}: Copywriting Route Map receipt stale')
""",
"""  is_cw=CW_DIR in str(p)
  is_sfv=SFV_DIR in str(p)
  is_set008=is_cw or is_sfv
  expected_compat=SET008_SPECIALIST_COMPAT if is_set008 else SPECIALIST_COMPAT
  req(fc.get('compatibility_state')==expected_compat,f'{p}: stale Foundation compatibility state')
  if is_set008:
   req(fc.get('target_identity')==FOUNDATION_ID,f'{p}: SET_008 target identity missing')
   h=next((x for x in fc.get('required_files',[]) if x.get('filename')=='AIR_HANDOFF_CARD_TEMPLATE.json'),{})
   req(h.get('template_revision')==19 and h.get('revision_fields')==['template_revision','user_revision'] and 'card_revision' not in h,f'{p}: Handoff revision split stale')
   rr=fc.get('route_map_discovery_input') or fc.get('foundation_adjacent_route_map') or {}
   req(rr.get('version')=='1.2.2' and rr.get('sha256')=='a8817d0abe078a2b94f87562386ac5e63a575b0926c0b2d050a6e470f578e89c',f'{p}: Route Map receipt stale')
""",
'r7 profile compatibility')
s = replace_once(s,
"expected_state=SET008_FOUNDATION_STATE if CW_DIR in str(p) else FOUNDATION_STATE",
"expected_state=SET008_FOUNDATION_STATE if (CW_DIR in str(p) or SFV_DIR in str(p)) else FOUNDATION_STATE",
'r7 integration identity')
insert = """ sfvman=parsed[ROOT/'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json']
 req(sfvman['foundation_compatibility'].get('target_identity')==FOUNDATION_ID and sfvman['foundation_compatibility'].get('compatibility_state')==SET008_SPECIALIST_COMPAT,'SFV manifest SET_008 compatibility missing')
 spvs=sfvman.get('package_validation_state',{})
 req(spvs.get('behavioral_revalidation')==BEHAVIOR_PENDING and spvs.get('component_internal_foundation_compatibility')=='PASS_SET_008_EXACT_RECEIPTS','SFV manifest validation state mismatch')
 sfvexec=parsed[ROOT/'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json']
 req(sfvexec.get('STATUS')=='DRAFT','SFV Executor was promoted out of DRAFT')
 sfventry=next(e for e in idx['entries'] if e['package_identity']==SFV_PACKAGE)
 req(sfventry.get('availability_state')==PENDING_BEHAVIOR and sfventry.get('foundation_compatibility_identity')==FOUNDATION_ID,'SFV index static promotion mismatch')
"""
s = insert_before_once(s, " for e in idx['entries']:\n  targets=list(ROOT.glob('profiles/**/'+e['manifest_filename']))\n", insert, 'r7 sfv assertions')
p.write_text(s, encoding='utf-8')

p = ROOT/'tools/test_air_r7_mutations.py'
s = p.read_text(encoding='utf-8')
mut_insert = """add('R7-N27-SFV-INDEX-STATIC-ROLLBACK','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:next(e for e in o['entries'] if e['package_identity']=='AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2').__setitem__('availability_state','RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION')))
add('R7-N28-SFV-INDEX-SET007-ROLLBACK','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:next(e for e in o['entries'] if e['package_identity']=='AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2').__setitem__('foundation_compatibility_identity','AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007')))
add('R7-N29-SFV-EXECUTOR-PREMATURE-PROMOTION','profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json',jfn(lambda o:o.__setitem__('STATUS','V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING')))
add('R7-N30-SFV-CARD-REVISION-RESTORED','profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json',jfn(lambda o:next(x for x in o['foundation_compatibility']['required_files'] if x['filename']=='AIR_HANDOFF_CARD_TEMPLATE.json').__setitem__('card_revision',18)))
"""
s = insert_before_once(s, "if run(ROOT)!=0:raise SystemExit('R7-MUTATION-BASELINE failed')\n", mut_insert, 'r7 mutations')
p.write_text(s, encoding='utf-8')

p = ROOT/'tools/validate_air_v073_release_seal.py'
s = p.read_text(encoding='utf-8')
s = replace_once(s,
"CW_PACKAGE = 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'\n",
"CW_PACKAGE = 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'\nSFV_PACKAGE = 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2'\n",
'seal constants')
s = replace_once(s,
"    'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json': '1305db0990880850290d7733831458e392dc163766751fab7eac279c04484955',",
f"    'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json': '{index_hash}',",
'seal index hash')
s = replace_once(s,
"    req(index['INDEX_VERSION'] == '1.3.5', 'Index behavioral-promotion version mismatch')",
"    req(index['INDEX_VERSION'] == '1.3.6', 'Index SFV-static-revalidation version mismatch')",
'seal index version')
s = replace_once(s,
"""    others = [e for e in index['entries'] if e['package_identity'] != CW_PACKAGE]
    req(len(others) == 4 and all(e['availability_state'] == PENDING_STATIC for e in others), 'remaining Specialist lifecycle not pending-static')
    req(all(e['foundation_compatibility_identity'] == SET007 for e in others), 'non-Copywriting historical compatibility identity changed')
    req(all(e['current_foundation_compatibility_state'] == 'REVALIDATION_REQUIRED_NOT_INFERRED_FROM_INDEX_RESEAL' for e in others), 'non-Copywriting SET_008 compatibility inferred')
    prog = index['validation_state'].get('set008_static_revalidation_progress', {})
    req(prog.get('passed_package_identities') == [CW_PACKAGE] and prog.get('passed_count') == 1 and prog.get('pending_count') == 4, 'Index SET_008 progress mismatch')
""",
"""    sfv = [e for e in index['entries'] if e['package_identity'] == SFV_PACKAGE]
    req(len(sfv) == 1, 'SFV index entry missing')
    se = sfv[0]
    req(se['availability_state'] == PENDING_BEHAVIOR, 'SFV lifecycle not pending behavioral revalidation')
    req(se['foundation_compatibility_identity'] == FOUNDATION_ID, 'SFV SET_008 identity missing')
    req(se['current_foundation_compatibility_state'] == 'STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING', 'SFV SET_008 static state mismatch')
    others = [e for e in index['entries'] if e['package_identity'] not in {CW_PACKAGE, SFV_PACKAGE}]
    req(len(others) == 3 and all(e['availability_state'] == PENDING_STATIC for e in others), 'remaining Specialist lifecycle not pending-static')
    req(all(e['foundation_compatibility_identity'] == SET007 for e in others), 'remaining historical compatibility identity changed')
    req(all(e['current_foundation_compatibility_state'] == 'REVALIDATION_REQUIRED_NOT_INFERRED_FROM_INDEX_RESEAL' for e in others), 'remaining SET_008 compatibility inferred')
    prog = index['validation_state'].get('set008_static_revalidation_progress', {})
    req(prog.get('passed_package_identities') == [CW_PACKAGE, SFV_PACKAGE] and prog.get('passed_count') == 2 and prog.get('pending_count') == 3 and prog.get('behavioral_revalidation_ready_package_identities') == [SFV_PACKAGE], 'Index SET_008 progress mismatch')
""",
'seal lifecycle split')
seal_insert = """    sfv_dir = ROOT / 'profiles' / 'specification first verification specialist'
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
    req(load(sfv_dir / 'AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json').get('STATUS') == 'DRAFT', 'SFV Executor was promoted out of DRAFT')
    sfvm = load(sfv_dir / 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json')
    req(sfvm['foundation_compatibility'].get('target_identity') == FOUNDATION_ID, 'SFV manifest target identity stale')
    req(sfvm['package_validation_state'].get('behavioral_revalidation') == 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE', 'SFV behavioral state overclaimed')
    req(sfvm['package_validation_state'].get('component_internal_foundation_compatibility') == 'PASS_SET_008_EXACT_RECEIPTS', 'SFV component receipt state stale')

"""
s = insert_before_once(s, "    migrator = load_migrator()\n", seal_insert, 'seal sfv assertions')
p.write_text(s, encoding='utf-8')

p = ROOT/'tools/test_air_v073_release_seal_mutations.py'
s = p.read_text(encoding='utf-8')
s = replace_once(s,
"    add('V073-N10-INDEX-VERSION-ROLLBACK', idxmut(lambda o: o.__setitem__('INDEX_VERSION', '1.3.4')))",
"    add('V073-N10-INDEX-VERSION-ROLLBACK', idxmut(lambda o: o.__setitem__('INDEX_VERSION', '1.3.5')))",
'seal mutation index rollback')
seal_mut = """    add('V073-N14-SFV-SET007-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2').__setitem__('foundation_compatibility_identity', 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007')))
    add('V073-N15-SFV-PENDING-STATIC-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2').__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION')))

    def sfv_executor_promoted(d: Path):
        p = d / 'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json'; o = load(p)
        o['STATUS'] = 'V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING'
        dump(p, o)
    add('V073-N16-SFV-EXECUTOR-PREMATURE-PROMOTION', sfv_executor_promoted)

    def sfv_card_revision(d: Path):
        p = d / 'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json'; o = load(p)
        hr = next(x for x in o['foundation_compatibility']['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')
        hr['card_revision'] = 18
        dump(p, o)
    add('V073-N17-SFV-CARD-REVISION-RESTORED', sfv_card_revision)

"""
s = insert_before_once(s, "    killed = 0\n", seal_mut, 'seal mutations')
p.write_text(s, encoding='utf-8')

bootstrap_path = ROOT/BOOTSTRAP
with bootstrap_path.open('w', encoding='utf-8') as f:
    subprocess.run(['git', 'show', f'{EXPECTED_BASE}:{BOOTSTRAP}'], cwd=ROOT, check=True, stdout=f, text=True)

for d in ROOT.rglob('__pycache__'):
    if d.is_dir():
        shutil.rmtree(d, ignore_errors=True)
for pyc in ROOT.rglob('*.pyc'):
    try:
        pyc.unlink()
    except FileNotFoundError:
        pass

net = sorted(x for x in out(['git', 'diff', '--name-only', EXPECTED_BASE]).splitlines() if x)
req(net == sorted(PERMANENT), f'pre-validation net path drift: {net}')

run([sys.executable, 'tools/validate_air_suite.py'])

for d in ROOT.rglob('__pycache__'):
    if d.is_dir():
        shutil.rmtree(d, ignore_errors=True)
for pyc in ROOT.rglob('*.pyc'):
    try:
        pyc.unlink()
    except FileNotFoundError:
        pass

net = sorted(x for x in out(['git', 'diff', '--name-only', EXPECTED_BASE]).splitlines() if x)
req(net == sorted(PERMANENT), f'post-validation net path drift: {net}')
req(load(SFV_DIR/'AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json').get('STATUS') == 'DRAFT', 'final Executor state not DRAFT')

run(['git', 'config', 'user.name', 'github-actions[bot]'])
run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'])
run(['git', 'add', '--', *PERMANENT, BOOTSTRAP])
run(['git', 'commit', '-m', 'specialists: revalidate Specification-First Verification for SET_008 [r1-applied]'])
final = out(['git', 'rev-parse', 'HEAD'])
final_net = sorted(x for x in out(['git', 'diff', '--name-only', EXPECTED_BASE, final]).splitlines() if x)
req(final_net == sorted(PERMANENT), f'committed net path drift: {final_net}')
run(['git', 'push'])
print('SFV SET_008 trusted carrier PASS', final, flush=True)
