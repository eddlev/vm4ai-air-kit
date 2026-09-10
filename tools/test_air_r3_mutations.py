from __future__ import annotations
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path('.').resolve(); PY=sys.executable

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def run_validator(root):
    return subprocess.run([PY,'tools/validate_air_r3_remediation.py','.'],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode

def mutate_json(rel, fn):
    def m(d):
        p=d/rel; o=load(p); fn(o); save(p,o)
    return m

def mutate_text(rel, old, new):
    def m(d):
        p=d/rel; t=p.read_text(encoding='utf-8')
        if old not in t: raise RuntimeError('mutation anchor absent: '+old)
        p.write_text(t.replace(old,new,1),encoding='utf-8')
    return m

def main():
    cases=[]
    cases.append(('R3-N01-VISIBILITY-AUTHORITY-CARRIER', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD'].pop('object_visibility_authority_state'))))
    cases.append(('R3-N02-METHOD-BASELINE-TRIGGER', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['condition_registry']['predicates'].__setitem__('HC-COND-METHOD',{'operator':'ANY_PATH_NOT_NULL','paths':['$.execution_state.method','$.execution_state.method_handoff_state']}))))
    cases.append(('R3-N03-ACTION-OPEN-AUTH-TRIGGER', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['condition_registry']['predicates']['HC-COND-ACTION-GOVERNANCE']['predicates'].__setitem__(2,{'operator':'PATH_NONEMPTY','path':'$.action_governance_state.action_receipts'}))))
    cases.append(('R3-N04-AMRS-NONPASS-TRIGGER', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['condition_registry']['predicates'].__setitem__('HC-COND-AMRS-STEP-OPTIMALITY-REV15',{'operator':'ALL','predicates':[{'operator':'PATH_GTE','path':'$.card_revision','expected':15},{'operator':'PATH_NOT_IN','path':'$.execution_state.review_state.step_optimality_state','values':[None,'NOT_APPLICABLE']}]}))))
    cases.append(('R3-N05-PROFILE-POSTURE-CARRIER', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD'].pop('profile_posture_acceptance_state'))))
    cases.append(('R3-N06-FLOOR-UNRESOLVED-ENUM', mutate_text('prompts/AIR_GOV.md','- UNRESOLVED\n','')))
    cases.append(('R3-N07-APPROVAL-CANONICAL-VALIDATION', mutate_json('prompts/AIR_DEFAULT_STARTER_PROFILE.json', lambda o:o['compiler_contract']['runtime_control_event_registry']['events'][next(i for i,e in enumerate(o['compiler_contract']['runtime_control_event_registry']['events']) if e['route_id']=='RT.APPROVAL_RESOLVE')]['guards'].__setitem__(1,{'operator':'EXACT_TOKEN_IN_DECLARED_SET','left_path':'CURRENT_USER_INPUT','right_path':'OPEN_APPROVAL_SCOPE.operational_response_tokens'}))))
    cases.append(('R3-N08-GOV-12-FIELD-COVERAGE', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['conditional_rules'][next(i for i,r in enumerate(o['AIR_HANDOFF_CARD']['schema_manifest']['conditional_rules']) if r['id']=='HC-COND-GOV')].__setitem__('requirements',o['AIR_HANDOFF_CARD']['schema_manifest']['conditional_rules'][next(i for i,r in enumerate(o['AIR_HANDOFF_CARD']['schema_manifest']['conditional_rules']) if r['id']=='HC-COND-GOV')]['requirements'][:6]))))
    cases.append(('R3-N09-EDITION-REVIEW-TOKEN', mutate_text('prompts/AIR_GOV.md','If semantic equivalence cannot be shown, route through Core AIR_GATE with decision = REVIEW.','If semantic equivalence cannot be shown, route to REVIEW_REQUIRED.')))
    cases.append(('R3-N10-METHOD-TYPED-HANDOFF-SCHEMA', mutate_json('profiles/grounding specialist/AIR_GROUNDING_METHOD_PACK.json', lambda o:o.__setitem__('handoff_requirements',['preserve method state as prose']))))
    cases.append(('R3-N11-OVERLAY-NOT-EVALUATED', mutate_json('profiles/governance specialist/AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json', lambda o:o['binding_rules']['activation_state_values'].remove('NOT_EVALUATED'))))
    cases.append(('R3-N12-GOV-METHOD-STEP-STATE', mutate_json('profiles/governance specialist/AIR_AI_GOVERNANCE_METHOD_PACK.json', lambda o:o['method_execution_state_schema'].__setitem__('step_states',['PENDING','ACTIVE','COMPLETED','BLOCKED','SKIPPED_APPROVED','FAILED','INVALIDATED','STALE_NEEDS_REGROUND']))))
    cases.append(('R3-N13-SOURCE-RIGHTS-PRECEDENCE', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['source_state']['source_rights_projection_contract'].__setitem__('last_writer_wins',True))))
    cases.append(('R3-N14-REV15-MIGRATION-ORDER', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['revision_migration_contracts']['REV15_TO_REV16'].__setitem__('apply_before_current_required_carrier_check',False))))
    if run_validator(ROOT)!=0: raise SystemExit('R3-MUTATION-BASELINE failed')
    print('R3-MUTATION-BASELINE: PASS')
    killed=0
    for name,fn in cases:
        with tempfile.TemporaryDirectory(prefix='air-r3-mut-') as td:
            d=Path(td)/'repo'; shutil.copytree(ROOT,d,ignore=shutil.ignore_patterns('.git','__pycache__'))
            fn(d)
            rc=run_validator(d)
            if rc==0: raise SystemExit('MUTATION SURVIVED: '+name)
            killed+=1; print(name+': KILLED')
    print(f'AIR R3 remediation mutation suite: PASS ({killed}/{len(cases)} targeted mutants killed)')
if __name__=='__main__': main()
