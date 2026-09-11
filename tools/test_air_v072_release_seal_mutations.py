from __future__ import annotations
import json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path('.').resolve(); VAL=ROOT/'tools/validate_air_v072_release_seal.py'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def run(d): return subprocess.run([sys.executable,str(VAL),str(d)],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode
def main():
    if run(ROOT)!=0: raise SystemExit('v0.7.2 candidate-seal mutation baseline failed')
    cases=[]
    def add(n,f): cases.append((n,f))
    def idxmut(fn):
        def m(d): p=d/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'; o=load(p); fn(o); dump(p,o)
        return m
    add('V072-N01-STATUS-STALE',idxmut(lambda o:o.__setitem__('status','STALE')))
    add('V072-N02-ENTRY-RELEASED-PREMATURELY',idxmut(lambda o:o['entries'][0].__setitem__('availability_state','RELEASE_CATALOG_ENTRY')))
    add('V072-N03-UNSUPPORTED-BEHAVIORAL-PASS',idxmut(lambda o:o['validation_state'].__setitem__('behavioral_revalidation','BEHAVIORAL_REVALIDATION_PASS')))
    def m4(d): p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['new_task_binding_transaction']['ordered_states'].remove('ARTIFACT_SURFACED_LEDGER_ACCOUNTED'); dump(p,o)
    add('V072-N04-NEW-TASK-ACCOUNTING-REMOVED',m4)
    def m5(d): p=d/'prompts/AIR_CONTROL_SURFACE.md'; p.write_text(p.read_text().replace('AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1','REMOVED_PRIMARY_SURFACE',1))
    add('V072-N05-PRIMARY-SURFACE-REMOVED',m5)
    for name,fn in cases:
        with tempfile.TemporaryDirectory(prefix='v072-seal-mut-') as td:
            d=Path(td)/'repo'; shutil.copytree(ROOT,d,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc')); fn(d)
            if run(d)==0: raise SystemExit('MUTATION SURVIVED: '+name)
            print(name+': KILLED')
    print(f'AIR v0.7.2 candidate-seal mutation suite: PASS ({len(cases)}/{len(cases)})')
if __name__=='__main__': main()
