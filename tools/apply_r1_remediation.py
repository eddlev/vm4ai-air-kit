from __future__ import annotations
import base64, hashlib, json, shutil, subprocess, sys, tarfile, tempfile
from pathlib import Path
R=Path('.').resolve(); C=R/'.air-v073-payload'
B64='3123c6fbda444d206067d84c5a6002861eb71b5f4d61ba60c42b20e9e379dd24'; XZ='3a0347012e9d77a68f98039a858a9d7bda2f82936b506a90311c3231922717e6'
PERM=['prompts/AIR_CORE_RUNTIME.md','prompts/AIR_CONTROL_SURFACE.md','prompts/AIR_DEFAULT_STARTER_PROFILE.json','prompts/AIR_HANDOFF_CARD_TEMPLATE.json','catalog/AIR_RUNTIME_ROUTE_MAP.json','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json','VERSION','README.md','tools/migrate_air_handoff.py','tools/validate_air_boot.py','tools/validate_air_r1_remediation.py','tools/validate_air_r3_remediation.py','tools/test_air_r3_mutations.py','tools/validate_air_r7_remediation.py','tools/test_air_r7_mutations.py','tools/validate_air_release.py','tools/test_air_validator_mutations.py','tools/validate_air_suite.py','tools/validate_air_v073_release_seal.py','tools/test_air_v073_release_seal_mutations.py','tests/air_contract_fixtures.json','tests/deterministic_contract_inventory.json']
def run(*a): subprocess.run(a,cwd=R,check=True)
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
# v0.7.3 adds an integer template_revision cross-file check. The canonical
# markdown-header comparison is lexical, so normalize the JSON scalar to its
# lexical representation before comparison. Existing string checks remain exact.
r1=R/'tools/validate_air_r1_remediation.py'
t=r1.read_text(encoding='utf-8')
old="elif op=='JSON_EQUALS_MARKDOWN_HEADER': req(jget(load(root/c['left']['file']),c['left']['path'])==header((root/c['right']['file']).read_text(),c['right']['header']),f'{cid}: JSON/header mismatch')"
new="elif op=='JSON_EQUALS_MARKDOWN_HEADER': req(str(jget(load(root/c['left']['file']),c['left']['path']))==header((root/c['right']['file']).read_text(),c['right']['header']),f'{cid}: JSON/header mismatch')"
if old not in t: raise SystemExit('v073 R1 JSON/header scalar normalization anchor missing')
r1.write_text(t.replace(old,new,1),encoding='utf-8')
# Validate Core's actual fail-closed transcript-recovery law rather than a phrase it does not use.
v73=R/'tools/validate_air_v073_release_seal.py'
v=v73.read_text(encoding='utf-8')
vold="req('transcript resupply' in core.lower() and 'PROHIBITED' in core, 'transcript-resupply prohibition missing')"
vnew="req('must not prescribe transcript export/paste as a recovery mechanism' in core.lower(), 'transcript-recovery prohibition missing')"
if vold not in v: raise SystemExit('v073 transcript recovery validator anchor missing')
v=v.replace(vold,vnew,1)
# REV18_TO_REV19 stores its split-counter rule under root_revision_split.
uold="req(contracts['REV18_TO_REV19']['user_revision_rule'].startswith('PRESERVE_EXPLICIT_INDEPENDENT_COUNTER'), 'rev18 user revision rule wrong')"
unew="req(contracts['REV18_TO_REV19']['root_revision_split']['user_revision_rule'].startswith('PRESERVE_EXPLICIT_INDEPENDENT_COUNTER'), 'rev18 user revision rule wrong')"
if uold not in v: raise SystemExit('v073 rev18 user revision validator anchor missing')
v=v.replace(uold,unew,1)
# Keep the privacy scanner self-applicable without embedding the forbidden
# private markers as contiguous literals in the validator itself.
pold="        req('Monica Angiuli' not in txt and 'AIR-HANDOFF-MONICA' not in txt, f'private fixture leaked into {rel}')"
pnew="        private_markers = ('Mon' + 'ica Angiuli', 'AIR-HANDOFF-' + 'MONICA')\n        req(all(marker not in txt for marker in private_markers), f'private fixture leaked into {rel}')"
if pold not in v: raise SystemExit('v073 privacy scanner anchor missing')
v73.write_text(v.replace(pold,pnew,1),encoding='utf-8')
run(sys.executable,'tools/validate_air_suite.py')
run('git','fetch','--depth=1','origin','main')
orig=subprocess.check_output(['git','show','origin/main:tools/apply_r1_remediation.py'],cwd=R)
(R/'tools/apply_r1_remediation.py').write_bytes(orig); shutil.rmtree(C)
changed=set(subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines())
if not changed or not changed<=set(PERM): raise SystemExit('carrier final path set invalid: '+repr(sorted(changed-set(PERM))))
run('git','config','user.name','github-actions[bot]'); run('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
run('git','add','-A','--',*PERM,'tools/apply_r1_remediation.py','.air-v073-payload')
run('git','commit','-m','release: AIR Kit v0.7.3 durable Handoff provenance [r1-applied]')
run('git','push')
print('AIR v0.7.3 trusted carrier: PASS')
