from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
class E(Exception): pass
def req(c,m):
    if not c: raise E(m)
def load(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def gov_eval(proto, missing):
    d=proto['request_decision_contract']
    if missing:
        b=d['material_required_input_gap_remaining']
        return {'emit_user_information_request':b['emit_user_information_request'],'action':b['action'],'requested_inputs':missing[:1]}
    b=d['all_material_inputs_available']
    return {'emit_user_information_request':b['emit_user_information_request'],'action':b['action']}
def cw_eval(contract, state):
    c=contract['CW06_COMPARE_AND_SELECT']
    if state['further_search_justified'] is True:
        b=c['further_search_branch']; return {'advance_to_cw07':b['advance_to_cw07'],'next_step':b['next_step']}
    a=c['advance_to_cw07_requires']
    if all(state.get(k)==v for k,v in a.items()): return {'advance_to_cw07':True,'next_step':'CW07_REVIEW_COPY_IN_SCOPE'}
    return {'advance_to_cw07':False,'next_step':'REVIEW_REQUIRED'}
def main():
    gov=load('profiles/governance specialist/AIR_AI_GOVERNANCE_SPECIALIST.json')
    cw=load('profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json')
    fx=load('tests/air_contract_fixtures.json')
    p=gov['source_layer']['source_access_boot_protocol']
    req(p.get('visible_request_required')=='CONDITIONAL_ON_MATERIAL_REQUIRED_INPUT_GAP','053 conditional mode absent')
    req(p.get('pre_request_context_check_required') is True,'053 pre-request check absent')
    exp=['current session','source inventory','validated package state','authorized tools and connectors','source rights','freshness','jurisdiction','lifecycle','organizational role','intended purpose','evidence obligations']
    req(p.get('pre_request_context_sources')==exp,'053 pre-request source set/order mismatch')
    req('request_once_at_boot' not in p,'053 unconditional request list remains')
    allok=p['request_decision_contract']['all_material_inputs_available']; gap=p['request_decision_contract']['material_required_input_gap_remaining']
    req(allok=={'emit_user_information_request':False,'action':'ACKNOWLEDGE_CURRENT_SOURCE_ACCESS_STATE','preserve_existing_authorized_context':True},'053 already-satisfied decision wrong')
    req(gap.get('emit_user_information_request') is True and gap.get('action')=='REQUEST_SMALLEST_EXACT_MISSING_INPUT' and gap.get('request_scope')=='STILL_MISSING_MATERIALLY_REQUIRED_CATEGORIES_ONLY' and gap.get('preserve_unresolved_state_until_satisfied') is True,'053 gap decision wrong')
    req(p.get('default_if_paid_material_absent')=='PUBLIC_SOURCE_ONLY','053 public fallback changed')
    req(p.get('public_source_only_tags',{}).get('clause_level_standard_mapping')=='BLOCKED','053 clause-level fallback boundary changed')
    ga=gov.get('authority_boundary',{})
    req(ga.get('independent_execution_authority') is False and ga.get('active_execution_binding_authority') is False and ga.get('self_approval') is False and ga.get('self_binding') is False and ga.get('positive_material_execution_authority_source')=='SOLE_BOUND_ORBIT_0_AIR_ARTIFACT','053 Governance authority boundary changed')
    req(not any(x=='Ask for source inventory and access mode at boot before material governance mapping.' for x in gov['execution_constraints']),'053 old unconditional execution constraint remains')
    req(any('otherwise acknowledge the current source-access state without re-requesting information' in x for x in gov['execution_constraints']),'053 acknowledgment behavior absent')
    cases={x['id']:x for x in fx.get('r6_package_local_behavior_cases',[])}
    ids={'GOV-BEH-01-ALREADY-SATISFIED','GOV-BEH-02-ONE-MISSING','CW-BEH-04-FURTHER-SEARCH-NO-PASS','CW-BEH-05-PASS-AND-STOPPED','CW-BEH-06-PASS-BUT-FURTHER-SEARCH'}
    req(ids<=set(cases),'R6 fixtures incomplete')
    for i in ['GOV-BEH-01-ALREADY-SATISFIED','GOV-BEH-02-ONE-MISSING']:
        c=cases[i]; req(gov_eval(p,c['input']['missing_material_required_inputs'])==c['expected'],f'{i} behavior mismatch')
    opt=cw.get('step_optimality_contribution_contract',{})
    req(opt.get('authority')=='CONTRIBUTION_ONLY_CORE_OWNS_FINAL_STEP_OPTIMALITY_AND_AMRS','056 authority changed')
    c=opt.get('CW06_COMPARE_AND_SELECT',{}); a=c.get('advance_to_cw07_requires',{}); s=c.get('further_search_branch',{})
    req(a=={'candidate_contribution_state':'PASS_CANDIDATE','further_search_justified':False,'proportional_stopping_basis_recorded':True,'material_unresolved_domination':False},'056 advance predicate mismatch')
    req(s=={'when':{'further_search_justified':True},'next_step':'CW04_FORM_CANDIDATE_STRUCTURE','advance_to_cw07':False,'preserve_unresolved_method_state':True},'056 search continuation branch mismatch')
    for coll in ('method_steps','ordered_steps'):
        st=next(x for x in cw[coll] if x['step_id']=='CW06_COMPARE_AND_SELECT')
        req(st.get('branch_contract_ref')=='step_optimality_contribution_contract.CW06_COMPARE_AND_SELECT',f'056 branch ref missing {coll}')
        req(st.get('further_search_route')=='CW04_FORM_CANDIDATE_STRUCTURE',f'056 search route missing {coll}')
        txt=' '.join(st.get('evidence_to_advance',[]))
        req(' or further search is justified' not in txt,f'056 OR bug remains {coll}')
        req('PASS_CANDIDATE' in txt and 'further_search_justified is false' in txt and 'proportional_stopping_basis_recorded is true' in txt and 'material_unresolved_domination is false' in txt,f'056 advance evidence incomplete {coll}')
    o=next(x for x in cw['ordered_steps'] if x['step_id']=='CW06_COMPARE_AND_SELECT')
    req('route to CW04_FORM_CANDIDATE_STRUCTURE and do not advance to CW07' in o['next_step_rule'],'056 ordered next-step branch absent')
    req(cw.get('authority_boundary',{}).get('positive_material_execution_authority_source')=='SOLE_BOUND_ORBIT_0_AIR_ARTIFACT','056 positive authority boundary changed')
    for i in ['CW-BEH-04-FURTHER-SEARCH-NO-PASS','CW-BEH-05-PASS-AND-STOPPED','CW-BEH-06-PASS-BUT-FURTHER-SEARCH']:
        cc=cases[i]; req(cw_eval(opt,cc['input'])==cc['expected'],f'{i} behavior mismatch')
    print('R6 remediation validation: PASS')
    print('r6_findings 2')
    print('governance_boot_cases 2')
    print('cw06_cases 3')
    print('audited_source_changes 2')
if __name__=='__main__':
    try: main()
    except (E,KeyError,StopIteration) as e:
        print('R6 remediation validation: FAIL:',e,file=sys.stderr); raise SystemExit(1)
