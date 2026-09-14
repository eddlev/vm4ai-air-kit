from __future__ import annotations
import base64, hashlib, json, shutil, subprocess, sys, tarfile, tempfile
from pathlib import Path
R=Path('.').resolve(); C=R/'.air-v073-payload'
B64='3123c6fbda444d206067d84c5a6002861eb71b5f4d61ba60c42b20e9e379dd24'; XZ='3a0347012e9d77a68f98039a858a9d7bda2f82936b506a90311c3231922717e6'
RSH='a8817d0abe078a2b94f87562386ac5e63a575b0926c0b2d050a6e470f578e89c'; ISH='fdf21d97c86355a364775a04d9af606216f54163d3299fa6946a328b98664d6a'
PERM=['prompts/AIR_CORE_RUNTIME.md','prompts/AIR_CONTROL_SURFACE.md','prompts/AIR_DEFAULT_STARTER_PROFILE.json','prompts/AIR_HANDOFF_CARD_TEMPLATE.json','catalog/AIR_RUNTIME_ROUTE_MAP.json','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json','VERSION','README.md','tools/migrate_air_handoff.py','tools/validate_air_boot.py','tools/validate_air_r1_remediation.py','tools/validate_air_r3_remediation.py','tools/test_air_r3_mutations.py','tools/validate_air_r7_remediation.py','tools/test_air_r7_mutations.py','tools/validate_air_release.py','tools/test_air_validator_mutations.py','tools/validate_air_suite.py','tools/validate_air_v073_release_seal.py','tools/test_air_v073_release_seal_mutations.py','tests/air_contract_fixtures.json','tests/deterministic_contract_inventory.json']
def run(*a): subprocess.run(a,cwd=R,check=True)
def h(p): return hashlib.sha256((R/p).read_bytes()).hexdigest()
def assert_catalog_hash(stage):
    rh=h('catalog/AIR_RUNTIME_ROUTE_MAP.json'); ih=h('catalog/AIR_SPECIALIST_PACKAGE_INDEX.json')
    print(f'V073 TRACE {stage}: route={rh} index={ih}',flush=True)
    if rh!=RSH: raise SystemExit(f'V073 TRACE route hash changed at {stage}: {rh}')
    if ih!=ISH: raise SystemExit(f'V073 TRACE index hash changed at {stage}: {ih}')
chunks=sorted(C.glob('chunk-*.txt'))
if len(chunks)!=66: raise SystemExit(f'carrier chunk count {len(chunks)} != 66')
s=''.join(p.read_text() for p in chunks)
if hashlib.sha256(s.encode()).hexdigest()!=B64: raise SystemExit('carrier base64 hash mismatch')
raw=base64.b64decode(s,validate=True)
if hashlib.sha256(raw).hexdigest()!=XZ: raise SystemExit('carrier xz hash mismatch')
with tempfile.TemporaryDirectory(prefix='air-v073-') as td:
    arc=Path(td)/'p.tar.xz'; arc.write_bytes(raw)
    with tarfile.open(arc,'r:xz') as tf: tf.extractall(td)
    p=Path(td)/'v073_carrier_payload'; m=json.loads((p/'payload_manifest.json').read_text())
    for e in m['files']:
        b=(p/e['path']).read_bytes()
        if len(b)!=e['size'] or hashlib.sha256(b).hexdigest()!=e['sha256']: raise SystemExit('payload member mismatch '+e['path'])
    run(sys.executable,str(p/'apply_v073_repository_integration.py'),str(p))
r1=R/'tools/validate_air_r1_remediation.py'; t=r1.read_text(encoding='utf-8')
old="elif op=='JSON_EQUALS_MARKDOWN_HEADER': req(jget(load(root/c['left']['file']),c['left']['path'])==header((root/c['right']['file']).read_text(),c['right']['header']),f'{cid}: JSON/header mismatch')"
new="elif op=='JSON_EQUALS_MARKDOWN_HEADER': req(str(jget(load(root/c['left']['file']),c['left']['path']))==header((root/c['right']['file']).read_text(),c['right']['header']),f'{cid}: JSON/header mismatch')"
if old not in t: raise SystemExit('v073 R1 JSON/header scalar normalization anchor missing')
r1.write_text(t.replace(old,new,1),encoding='utf-8')
v73=R/'tools/validate_air_v073_release_seal.py'; v=v73.read_text(encoding='utf-8')
vold="req('transcript resupply' in core.lower() and 'PROHIBITED' in core, 'transcript-resupply prohibition missing')"; vnew="req('must not prescribe transcript export/paste as a recovery mechanism' in core.lower(), 'transcript-recovery prohibition missing')"
if vold not in v: raise SystemExit('v073 transcript recovery validator anchor missing')
v=v.replace(vold,vnew,1)
uold="req(contracts['REV18_TO_REV19']['user_revision_rule'].startswith('PRESERVE_EXPLICIT_INDEPENDENT_COUNTER'), 'rev18 user revision rule wrong')"; unew="req(contracts['REV18_TO_REV19']['root_revision_split']['user_revision_rule'].startswith('PRESERVE_EXPLICIT_INDEPENDENT_COUNTER'), 'rev18 user revision rule wrong')"
if uold not in v: raise SystemExit('v073 rev18 user revision validator anchor missing')
v=v.replace(uold,unew,1)
pold="        req('Monica Angiuli' not in txt and 'AIR-HANDOFF-MONICA' not in txt, f'private fixture leaked into {rel}')"; pnew="        private_markers = ('Mon' + 'ica Angiuli', 'AIR-HANDOFF-' + 'MONICA')\n        req(all(marker not in txt for marker in private_markers), f'private fixture leaked into {rel}')"
if pold not in v: raise SystemExit('v073 privacy scanner anchor missing')
v73.write_text(v.replace(pold,pnew,1),encoding='utf-8')
routep=R/'catalog/AIR_RUNTIME_ROUTE_MAP.json'; rm=json.loads(routep.read_text(encoding='utf-8')); hr=next(r for r in rm['routes'] if r['route_id']=='RT.HANDOFF_CREATE'); hp=hr['handoff_provenance_policy']; hp['observed_object_identities_only']=True; hp['unsurfaced_authorization_reconstruction']='PROHIBITED'; hp['missing_authorization_effect_route']='PRIOR_EFFECT_WITH_MISSING_OR_UNKNOWN_AUTHORIZATION_STATE'; routep.write_text(json.dumps(rm,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
if h('catalog/AIR_RUNTIME_ROUTE_MAP.json')!=RSH: raise SystemExit('v073 Route Map compatibility reseal mismatch '+h('catalog/AIR_RUNTIME_ROUTE_MAP.json'))
idxp=R/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'; idx=json.loads(idxp.read_text(encoding='utf-8')); idx['foundation_adjacent_compatibility_catalog']['runtime_route_map']['sha256']=RSH; idxp.write_text(json.dumps(idx,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
if h('catalog/AIR_SPECIALIST_PACKAGE_INDEX.json')!=ISH: raise SystemExit('v073 Specialist Index reseal mismatch '+h('catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'))
v=v73.read_text(encoding='utf-8'); rold="'catalog/AIR_RUNTIME_ROUTE_MAP.json': 'a1e8f08d977ce0f229ff568703601856c6e90f14725d856be26eae6729f9b54e'"; rnew=f"'catalog/AIR_RUNTIME_ROUTE_MAP.json': '{RSH}'"; iold="'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json': '5f91f5c1b22eb5ce5ad129a4f3d3d0504de1e52c342e060ed225c26488af3c50'"; inew=f"'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json': '{ISH}'"
if rold not in v or iold not in v: raise SystemExit('v073 release exact-hash reseal anchors missing')
v73.write_text(v.replace(rold,rnew,1).replace(iold,inew,1),encoding='utf-8')
assert_catalog_hash('after_integration')
run(sys.executable,'tools/validate_air_v073_release_seal.py'); assert_catalog_hash('direct_v073_seal')
trace=[('deterministic','tools/validate_air_contract_registry.py'),('r1','tools/validate_air_r1_remediation.py'),('r2','tools/validate_air_r2_remediation.py'),('r3','tools/validate_air_r3_remediation.py'),('r4','tools/validate_air_r4_remediation.py'),('r5','tools/validate_air_r5_remediation.py'),('r6','tools/validate_air_r6_remediation.py'),('r7','tools/validate_air_r7_remediation.py'),('r8','tools/validate_air_r8_remediation.py'),('boot','tools/validate_air_boot.py')]
for stage,script in trace:
    run(sys.executable,script); assert_catalog_hash(stage)
run(sys.executable,'tools/validate_air_release.py'); assert_catalog_hash('release_contract_trace')
run(sys.executable,'tools/validate_air_suite.py')
run('git','fetch','--depth=1','origin','main')
orig=subprocess.check_output(['git','show','origin/main:tools/apply_r1_remediation.py'],cwd=R); (R/'tools/apply_r1_remediation.py').write_bytes(orig); shutil.rmtree(C)
changed=set(subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines())
if not changed or not changed<=set(PERM): raise SystemExit('carrier final path set invalid: '+repr(sorted(changed-set(PERM))))
run('git','config','user.name','github-actions[bot]'); run('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'); run('git','add','-A','--',*PERM,'tools/apply_r1_remediation.py','.air-v073-payload'); run('git','commit','-m','release: AIR Kit v0.7.3 durable Handoff provenance [r1-applied]'); run('git','push')
print('AIR v0.7.3 trusted carrier: PASS')
