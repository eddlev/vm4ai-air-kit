from __future__ import annotations
import json,hashlib,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path('.').resolve(); VALIDATOR=ROOT/'tools/validate_air_r2_remediation.py'; PY=sys.executable

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sync_rmap(d):
    cp=d/'prompts/AIR_CORE_RUNTIME.md'; core=cp.read_text(encoding='utf-8'); rp=d/'catalog/AIR_RUNTIME_ROUTE_MAP.json'; o=load(rp)
    o['source_of_truth']['sha256']=hashlib.sha256(cp.read_bytes()).hexdigest()
    lines={ln.split('=',1)[1]:i for i,ln in enumerate(core.splitlines(),1) if ln.startswith('id=RT.')}
    for r in o['routes']: r['source_anchor']['line']=lines[r['route_id']]
    dump(rp,o)
def run(d): return subprocess.run([PY,str(VALIDATOR),str(d)],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
def core_mut(d,old,new):
    p=d/'prompts/AIR_CORE_RUNTIME.md'; t=p.read_text(encoding='utf-8')
    if old not in t: raise RuntimeError('mutation anchor missing')
    p.write_text(t.replace(old,new,1),encoding='utf-8'); sync_rmap(d)
def m1(d): core_mut(d,'- AIR_SURFACED_OBJECT_LEDGER: SURFACED_OBJECT_LEDGER_RECORD\n- AIR_FAILURE_MODE_RECORD: FAILURE_MODE_RECORD\n','')
def m2(d): core_mut(d,'A prior REVIEW Gate does not become ALLOW','A prior HOLD Gate does not become ALLOW')
def m3(d): core_mut(d,'    "decision": "ALLOW",','    "decision": "ALLOW | REJECT",')
def m4(d): core_mut(d,'- prompt_layer_qualitative_trace when prompt-layer qualitative native checks materially affect the active step; mandatory when prompt AIR references backend-inspired native behavior\n','')
def m5(d):
    p=d/'prompts/AIR_GOV.md'; t=p.read_text(); old='Governance source-rights state must feed AIR_GATE.evaluation_checks.evidence, AIR_GATE.evaluation_checks.allowed_action, AIR_GATE.evaluation_checks.stop_condition, and AIR_GATE.reason when source use is material.'; new='Governance source-rights state must feed AIR_GATE evidence_check, allowed_action_check, stop_condition_check, and reason when source use is material.'; p.write_text(t.replace(old,new,1))
def m6(d):
    p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['surfaced_object_ledger']['failure_record_entry_reservation']['reservation_state']='USER_VISIBLE_EMITTED'; dump(p,o)
def m7(d):
    p=d/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; o=load(p); o['AIR_HANDOFF_CARD']['surfaced_object_ledger_state']['entry_requirements']['required_fields'].remove('ledger_entry_ref'); dump(p,o)
def m8(d):
    p=d/'catalog/AIR_RUNTIME_ROUTE_MAP.json'; o=load(p); r=next(x for x in o['routes'] if x['route_id']=='RT.APPROVAL_RESOLVE'); r['invalidates']=['PRIOR_HOLD_GATE_WHEN_RESOLVED' if x=='PRIOR_REVIEW_GATE_WHEN_RESOLVED' else x for x in r['invalidates']]; dump(p,o)
CASES=[('R2-N01-FORMAL-CLASS-OMISSION',m1),('R2-N02-NONCANONICAL-HOLD-GATE',m2),('R2-N03-REJECT-AUTHORIZATION-ENUM',m3),('R2-N04-UNREGISTERED-QUALITATIVE-TRACE',m4),('R2-N05-RETIRED-GOV-GATE-PATHS',m5),('R2-N06-RESERVATION-GAINS-VISIBILITY',m6),('R2-N07-HANDOFF-LEDGER-REF-OMITTED',m7),('R2-N08-ROUTE-MAP-HOLD-INVALIDATION',m8)]
def main():
    base=run(ROOT)
    if base.returncode: raise SystemExit('R2 mutation baseline failed: '+base.stdout)
    print('R2-MUTATION-BASELINE: PASS')
    for name,fn in CASES:
        with tempfile.TemporaryDirectory(prefix='r2mut-') as td:
            d=Path(td)/'tree'; shutil.copytree(ROOT,d,ignore=shutil.ignore_patterns('.git','__pycache__'))
            fn(d); p=run(d)
            if p.returncode==0: raise SystemExit(f'{name}: SURVIVED')
            print(name+': KILLED')
    print(f'AIR R2 remediation mutation suite: PASS ({len(CASES)}/{len(CASES)} targeted mutants killed)')
if __name__=='__main__': main()
