from __future__ import annotations
import copy, json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
VAL=Path(sys.argv[2] if len(sys.argv)>2 else 'tools/validate_air_r6_remediation.py').resolve()
G='profiles/governance specialist/AIR_AI_GOVERNANCE_SPECIALIST.json'
C='profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json'
F='tests/air_contract_fixtures.json'
def run(root): return subprocess.run([sys.executable,str(VAL),str(root)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True).returncode
def load(p): return json.loads(p.read_text())
def dump(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def mutate(name, fn):
    with tempfile.TemporaryDirectory() as td:
        t=Path(td)
        for rel in (G,C,F):
            p=t/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/rel).read_bytes())
        fn(t)
        killed=run(t)!=0
        print(f'{name}: '+('KILLED' if killed else 'SURVIVED'))
        if not killed: raise SystemExit(1)
if run(ROOT)!=0: raise SystemExit('R6-MUTATION-BASELINE failed')
print('R6-MUTATION-BASELINE: PASS')

def mg(field,val):
    def f(t):
        p=t/G;o=load(p);o['source_layer']['source_access_boot_protocol'][field]=val;dump(p,o)
    return f
mutate('R6-N01-GOV-UNCONDITIONAL-VISIBLE-REQUEST',mg('visible_request_required',True))
def n2(t):
    p=t/G;o=load(p);o['source_layer']['source_access_boot_protocol']['request_decision_contract']['all_material_inputs_available']['emit_user_information_request']=True;dump(p,o)
mutate('R6-N02-GOV-ALREADY-SATISFIED-REQUESTS',n2)
def n3(t):
    p=t/G;o=load(p);o['source_layer']['source_access_boot_protocol']['request_decision_contract']['material_required_input_gap_remaining']['action']='ACKNOWLEDGE_CURRENT_SOURCE_ACCESS_STATE';dump(p,o)
mutate('R6-N03-GOV-MISSING-INPUT-NOT-REQUESTED',n3)
def n4(t):
    p=t/G;o=load(p);o['execution_constraints'][0]='Ask for source inventory and access mode at boot before material governance mapping.';dump(p,o)
mutate('R6-N04-GOV-OLD-BOOT-CONSTRAINT',n4)
def n5(t):
    p=t/C;o=load(p);next(x for x in o['method_steps'] if x['step_id']=='CW06_COMPARE_AND_SELECT')['evidence_to_advance']=['step-optimality contribution is PASS_CANDIDATE or further search is justified'];dump(p,o)
mutate('R6-N05-CW06-PREMATURE-OR-RESTORED',n5)
def n6(t):
    p=t/C;o=load(p);o['step_optimality_contribution_contract']['CW06_COMPARE_AND_SELECT']['further_search_branch']['advance_to_cw07']=True;dump(p,o)
mutate('R6-N06-CW06-FURTHER-SEARCH-ADVANCES',n6)
def n7(t):
    p=t/C;o=load(p);o['step_optimality_contribution_contract']['CW06_COMPARE_AND_SELECT']['further_search_branch']['next_step']='CW07_REVIEW_COPY_IN_SCOPE';dump(p,o)
mutate('R6-N07-CW06-FURTHER-SEARCH-ROUTES-CW07',n7)
def n8(t):
    p=t/C;o=load(p);o['step_optimality_contribution_contract']['CW06_COMPARE_AND_SELECT']['advance_to_cw07_requires']['further_search_justified']=True;dump(p,o)
mutate('R6-N08-CW06-ADVANCE-REQUIRES-FURTHER-SEARCH',n8)
def n9(t):
    p=t/C;o=load(p);del o['step_optimality_contribution_contract']['CW06_COMPARE_AND_SELECT']['advance_to_cw07_requires']['proportional_stopping_basis_recorded'];dump(p,o)
mutate('R6-N09-CW06-STOPPING-BASIS-REMOVED',n9)
def n10(t):
    p=t/C;o=load(p);next(x for x in o['ordered_steps'] if x['step_id']=='CW06_COMPARE_AND_SELECT').pop('branch_contract_ref',None);dump(p,o)
mutate('R6-N10-CW06-ORDERED-BRANCH-REF-REMOVED',n10)
def n11(t):
    p=t/G;o=load(p);o['authority_boundary']['independent_execution_authority']=True;dump(p,o)
mutate('R6-N11-GOV-AUTHORITY-EXPANSION',n11)
def n12(t):
    p=t/C;o=load(p);o['authority_boundary']['positive_material_execution_authority_source']='SPECIALIST';dump(p,o)
mutate('R6-N12-CW-AUTHORITY-EXPANSION',n12)
print('AIR R6 remediation mutation suite: PASS (12/12 targeted mutants killed)')
