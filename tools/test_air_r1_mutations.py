from __future__ import annotations
import json, shutil, tempfile, re, contextlib, io, hashlib
from pathlib import Path
from validate_air_r1_remediation import E, main as validate_r1
ROOT=Path('.').resolve()
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def copytree():
    td=tempfile.TemporaryDirectory(); t=Path(td.name)
    for d in ['prompts','catalog','tests']: shutil.copytree(ROOT/d,t/d)
    return td,t
def run_in_process(t):
    buf=io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf): validate_r1(t)
        return 0,buf.getvalue()
    except (E,KeyError,AssertionError) as exc:
        return 1,'R1 remediation validation: FAIL: '+str(exc)+'\n'+buf.getvalue()
def mutate(t,i):
    cp=t/'prompts/AIR_CORE_RUNTIME.md'; sp=t/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; rp=t/'catalog/AIR_RUNTIME_ROUTE_MAP.json'
    if i==1:
        s=cp.read_text(); s=s.replace('failure_route=RT.RECOVERY\n[AIR_ROUTE]','failure_route=RT.RECOVERY[AIR_ROUTE]',1); cp.write_text(s)
    elif i==2:
        s=load(sp); s['compiler_contract']['deterministic_pipeline_non_inference']['declared_runtime_routes'].remove('RT.APPROVAL_RESOLVE'); save(sp,s)
    elif i==3:
        s=cp.read_text(); m=re.search(r'(id=RT\.ALIGN\n.*?)(?=\n\[AIR_ROUTE\])',s,re.S); b=m.group(1).replace('control_event_ref=CE-RT-ALIGN\n',''); cp.write_text(s[:m.start(1)]+b+s[m.end(1):])
    elif i==4:
        s=load(sp); s['typed_registries']['runtime_states']['alignment_evaluation_profile'].remove('ACTIVATION'); save(sp,s)
    elif i==5:
        s=load(sp); e=next(x for x in s['compiler_contract']['runtime_control_event_registry']['events'] if x['route_id']=='RT.ALIGN'); e['guards']=[{'operator':'STATE_PRESENT','path':'CURRENT_EVALUATION_BASIS'}]; save(sp,s)
    elif i==6:
        s=cp.read_text(); s=s.replace('DEP.APPROVAL_PRECONDITION_SATISFIED','DEP.APPROVAL_CURRENT',1); cp.write_text(s)
    elif i==7:
        s=cp.read_text(encoding='utf-8')
        matches=list(re.finditer(r'(?m)^PROMPT_VERSION:\s*\S+\s*$',s))
        if len(matches)!=1: raise AssertionError(f'R1-N07 expected one current Core PROMPT_VERSION declaration, got {len(matches)}')
        m=matches[0]; cp.write_text(s[:m.start()]+'PROMPT_VERSION: 9.9.9'+s[m.end():],encoding='utf-8')
    elif i==8:
        s=load(sp); del s['profile_function_class']; save(sp,s)
    elif i==9:
        s=load(sp); s['authority_contract']['required_files']=[x for x in s['authority_contract']['required_files'] if x['canonical_role']!='HANDOFF_CARD_TEMPLATE']; save(sp,s)
    elif i==10:
        raw=sp.read_text(); sp.write_text(raw.replace('  "PROFILE_KIND": "TASK_COMPOSITE",','  "PROFILE_KIND": "TASK_COMPOSITE",\n  "PROFILE_KIND": "TASK_COMPOSITE",',1))
    elif i==11:
        cp.write_text(cp.read_text().replace('AIR-FLOOR-012-LEGACY-V1-NON-BINDING','AIR-FLOOR-012-MUTATED'))
        r=load(rp); r['source_of_truth']['sha256']=hashlib.sha256(cp.read_bytes()).hexdigest(); save(rp,r)
    elif i==12:
        s=load(rp); next(x for x in s['routes'] if x['route_id']=='RT.ACTION')['source_anchor']['line']-=1; save(rp,s)
    elif i==13:
        s=load(rp); next(x for x in s['routes'] if x['route_id']=='RT.ACTION')['requires'].remove('DEP.APPROVAL_PRECONDITION_SATISFIED'); save(rp,s)
    elif i==14:
        s=load(sp); s['routing_contracts']['sfv_method_routing']['need_states'].append('FULL_SFV_RECOMMENDED'); save(sp,s)
def main():
    fx=load(ROOT/'tests/r1_remediation_fixtures.json'); neg=fx['negative_cases']; rc,out=run_in_process(ROOT)
    if rc: raise SystemExit('R1 mutation baseline does not pass: '+out)
    print('R1-MUTATION-BASELINE: PASS')
    for idx,case in enumerate(neg,1):
        td,t=copytree()
        try:
            mutate(t,idx); rc,out=run_in_process(t)
            if rc==0: raise SystemExit(f"{case['id']}: mutation SURVIVED")
            if case['must_fail'] not in out: raise SystemExit(f"{case['id']}: wrong failure; expected {case['must_fail']!r}; got {out!r}")
            print(case['id']+': KILLED')
        finally: td.cleanup()
    print(f'AIR R1 remediation mutation suite: PASS ({len(neg)}/{len(neg)} targeted mutants killed)')
if __name__=='__main__': main()
