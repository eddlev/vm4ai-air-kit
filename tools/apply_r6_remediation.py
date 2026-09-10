from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()

GOV_REL = 'profiles/governance specialist/AIR_AI_GOVERNANCE_SPECIALIST.json'
CW_REL = 'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json'
FIX_REL = 'tests/air_contract_fixtures.json'
BEH_REL = 'tools/validate_air_behavioral_contracts.py'

REQUESTABLE = [
    'Target jurisdictions and sectors',
    'AI system or use-case description, lifecycle stage, and intended purpose',
    'Organization role and likely AI Act role, if known',
    'Internal policies, risk appetite, control library, contracts, DPIAs, model cards, system cards, vendor documents, and incident records',
    'Any lawfully accessible licensed standards, extracts, or clause references the user wants mapped',
    'Requested output: orientation, governance design, gap review, clause-level mapping, audit support, or external claim review',
]
PRECHECK = [
    'current session',
    'source inventory',
    'validated package state',
    'authorized tools and connectors',
    'source rights',
    'freshness',
    'jurisdiction',
    'lifecycle',
    'organizational role',
    'intended purpose',
    'evidence obligations',
]
GOV_MODE = 'CONDITIONAL_ON_MATERIAL_REQUIRED_INPUT_GAP'
GOV_CONSTRAINT = 'At boot, inspect authorized current context before material governance mapping. If a material required governance input remains missing, request only the smallest exact missing input; otherwise acknowledge the current source-access state without re-requesting information.'
CW_EVIDENCE = 'candidate_contribution_state is PASS_CANDIDATE, further_search_justified is false, proportional_stopping_basis_recorded is true, and material_unresolved_domination is false'
CW_NEXT = 'Apply step_optimality_contribution_contract. If further_search_justified=true, route to CW04_FORM_CANDIDATE_STRUCTURE and do not advance to CW07. Advance to CW07_REVIEW_COPY_IN_SCOPE only when every advance_to_cw07_requires condition is satisfied; otherwise apply failure_behavior and preserve unresolved method state.'
CW_REF = 'step_optimality_contribution_contract.CW06_COMPARE_AND_SELECT'
CW_ROUTE = 'CW04_FORM_CANDIDATE_STRUCTURE'

R6_CASES = [
    {
      'id': 'GOV-BEH-01-ALREADY-SATISFIED',
      'finding': 'AIR-AUD-053',
      'input': {'missing_material_required_inputs': []},
      'expected': {'emit_user_information_request': False, 'action': 'ACKNOWLEDGE_CURRENT_SOURCE_ACCESS_STATE'}
    },
    {
      'id': 'GOV-BEH-02-ONE-MISSING',
      'finding': 'AIR-AUD-053',
      'input': {'missing_material_required_inputs': ['Target jurisdictions and sectors']},
      'expected': {'emit_user_information_request': True, 'action': 'REQUEST_SMALLEST_EXACT_MISSING_INPUT', 'requested_inputs': ['Target jurisdictions and sectors']}
    },
    {
      'id': 'CW-BEH-04-FURTHER-SEARCH-NO-PASS',
      'finding': 'AIR-AUD-056',
      'input': {'candidate_contribution_state': 'NO_PASS_CANDIDATE', 'further_search_justified': True, 'proportional_stopping_basis_recorded': False, 'material_unresolved_domination': True},
      'expected': {'advance_to_cw07': False, 'next_step': 'CW04_FORM_CANDIDATE_STRUCTURE'}
    },
    {
      'id': 'CW-BEH-05-PASS-AND-STOPPED',
      'finding': 'AIR-AUD-056',
      'input': {'candidate_contribution_state': 'PASS_CANDIDATE', 'further_search_justified': False, 'proportional_stopping_basis_recorded': True, 'material_unresolved_domination': False},
      'expected': {'advance_to_cw07': True, 'next_step': 'CW07_REVIEW_COPY_IN_SCOPE'}
    },
    {
      'id': 'CW-BEH-06-PASS-BUT-FURTHER-SEARCH',
      'finding': 'AIR-AUD-056',
      'input': {'candidate_contribution_state': 'PASS_CANDIDATE', 'further_search_justified': True, 'proportional_stopping_basis_recorded': False, 'material_unresolved_domination': False},
      'expected': {'advance_to_cw07': False, 'next_step': 'CW04_FORM_CANDIDATE_STRUCTURE'}
    }
]

BEHAVIOR_INSERT = r'''
    # R6 package-local behavioral contradiction regressions.
    r6_cases = fixtures.get('r6_package_local_behavior_cases', [])
    r6_ids = {x.get('id') for x in r6_cases}
    require({
        'GOV-BEH-01-ALREADY-SATISFIED',
        'GOV-BEH-02-ONE-MISSING',
        'CW-BEH-04-FURTHER-SEARCH-NO-PASS',
        'CW-BEH-05-PASS-AND-STOPPED',
        'CW-BEH-06-PASS-BUT-FURTHER-SEARCH',
    } <= r6_ids, 'R6 package-local behavior fixtures missing')

    gov = load('profiles/governance specialist/AIR_AI_GOVERNANCE_SPECIALIST.json')
    boot = gov['source_layer']['source_access_boot_protocol']
    require(boot.get('visible_request_required') == 'CONDITIONAL_ON_MATERIAL_REQUIRED_INPUT_GAP', 'Governance boot request is not conditional')
    require(boot.get('pre_request_context_check_required') is True, 'Governance pre-request context check missing')
    decision = boot.get('request_decision_contract', {})
    all_ok = decision.get('all_material_inputs_available', {})
    one_gap = decision.get('material_required_input_gap_remaining', {})
    require(all_ok.get('emit_user_information_request') is False and all_ok.get('action') == 'ACKNOWLEDGE_CURRENT_SOURCE_ACCESS_STATE', 'Governance already-satisfied state still requests input')
    require(one_gap.get('emit_user_information_request') is True and one_gap.get('action') == 'REQUEST_SMALLEST_EXACT_MISSING_INPUT', 'Governance missing-input state does not request smallest exact input')
    require('request_once_at_boot' not in boot, 'Governance unconditional boot request list remains')
    require(not any(x == 'Ask for source inventory and access mode at boot before material governance mapping.' for x in gov.get('execution_constraints', [])), 'Governance unconditional boot execution constraint remains')
    require(gov['source_layer']['source_access_boot_protocol'].get('default_if_paid_material_absent') == 'PUBLIC_SOURCE_ONLY', 'Governance PUBLIC_SOURCE_ONLY fallback changed')

    cw = load('profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json')
    opt = cw.get('step_optimality_contribution_contract', {}).get('CW06_COMPARE_AND_SELECT', {})
    adv = opt.get('advance_to_cw07_requires', {})
    search = opt.get('further_search_branch', {})
    require(adv.get('candidate_contribution_state') == 'PASS_CANDIDATE', 'CW06 pass candidate requirement missing')
    require(adv.get('further_search_justified') is False, 'CW06 advance permits further search')
    require(adv.get('proportional_stopping_basis_recorded') is True, 'CW06 proportional stopping basis not required')
    require(adv.get('material_unresolved_domination') is False, 'CW06 advance permits unresolved domination')
    require(search.get('when', {}).get('further_search_justified') is True and search.get('advance_to_cw07') is False and search.get('next_step') == 'CW04_FORM_CANDIDATE_STRUCTURE', 'CW06 further-search branch does not remain in search/comparison')
    for coll in ('method_steps', 'ordered_steps'):
        step = next(x for x in cw[coll] if x.get('step_id') == 'CW06_COMPARE_AND_SELECT')
        require(step.get('branch_contract_ref') == 'step_optimality_contribution_contract.CW06_COMPARE_AND_SELECT', f'CW06 branch ref missing in {coll}')
        require(step.get('further_search_route') == 'CW04_FORM_CANDIDATE_STRUCTURE', f'CW06 further-search route missing in {coll}')
        joined = ' '.join(step.get('evidence_to_advance', []))
        require(' or further search is justified' not in joined, f'CW06 premature OR condition remains in {coll}')
        require('further_search_justified is false' in joined and 'proportional_stopping_basis_recorded is true' in joined, f'CW06 stopping evidence incomplete in {coll}')
    require(cw.get('authority_boundary', {}).get('positive_material_execution_authority_source') == 'SOLE_BOUND_ORBIT_0_AIR_ARTIFACT', 'Copywriting authority boundary changed')
'''


def loadj(rel):
    return json.loads((ROOT/rel).read_text(encoding='utf-8'))

def writej(rel, obj):
    (ROOT/rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def patch_gov():
    g=loadj(GOV_REL)
    p=g['source_layer']['source_access_boot_protocol']
    p['visible_request_required']=GOV_MODE
    p.pop('request_once_at_boot', None)
    # Insert before source_access_modes for readability while preserving existing remainder.
    new={}
    for k,v in p.items():
        if k=='source_access_modes':
            new['pre_request_context_check_required']=True
            new['pre_request_context_sources']=PRECHECK
            new['requestable_input_categories']=REQUESTABLE
            new['request_selection_rule']='Request only still-missing categories that are materially required, choosing the smallest exact sufficient request after the pre-request context check.'
            new['request_decision_contract']={
                'all_material_inputs_available': {
                    'emit_user_information_request': False,
                    'action': 'ACKNOWLEDGE_CURRENT_SOURCE_ACCESS_STATE',
                    'preserve_existing_authorized_context': True,
                },
                'material_required_input_gap_remaining': {
                    'emit_user_information_request': True,
                    'action': 'REQUEST_SMALLEST_EXACT_MISSING_INPUT',
                    'request_scope': 'STILL_MISSING_MATERIALLY_REQUIRED_CATEGORIES_ONLY',
                    'preserve_unresolved_state_until_satisfied': True,
                },
            }
        new[k]=v
    # Handle idempotent rerun where source_access_modes insertion point already passed.
    if 'pre_request_context_check_required' not in new:
        new['pre_request_context_check_required']=True
        new['pre_request_context_sources']=PRECHECK
        new['requestable_input_categories']=REQUESTABLE
        new['request_selection_rule']='Request only still-missing categories that are materially required, choosing the smallest exact sufficient request after the pre-request context check.'
        new['request_decision_contract']={
            'all_material_inputs_available': {'emit_user_information_request': False,'action':'ACKNOWLEDGE_CURRENT_SOURCE_ACCESS_STATE','preserve_existing_authorized_context':True},
            'material_required_input_gap_remaining': {'emit_user_information_request': True,'action':'REQUEST_SMALLEST_EXACT_MISSING_INPUT','request_scope':'STILL_MISSING_MATERIALLY_REQUIRED_CATEGORIES_ONLY','preserve_unresolved_state_until_satisfied':True},
        }
    # Remove duplicates created by rerun ordering.
    keys=['pre_request_context_check_required','pre_request_context_sources','requestable_input_categories','request_selection_rule','request_decision_contract']
    ordered={}
    inserted=False
    for k,v in new.items():
        if k in keys: continue
        if k=='source_access_modes' and not inserted:
            for kk in keys: ordered[kk]=new[kk]
            inserted=True
        ordered[k]=v
    if not inserted:
        for kk in keys: ordered[kk]=new[kk]
    g['source_layer']['source_access_boot_protocol']=ordered
    old='Ask for source inventory and access mode at boot before material governance mapping.'
    ecs=g.get('execution_constraints',[])
    if old in ecs:
        ecs[ecs.index(old)]=GOV_CONSTRAINT
    elif GOV_CONSTRAINT not in ecs:
        raise RuntimeError('Governance execution constraint anchor not found')
    writej(GOV_REL,g)

def patch_cw():
    c=loadj(CW_REL)
    c['step_optimality_contribution_contract']={
        'contract_id':'AIR_PUBLIC_SURFACE_COPYWRITING_CW06_STEP_OPTIMALITY_V1',
        'authority':'CONTRIBUTION_ONLY_CORE_OWNS_FINAL_STEP_OPTIMALITY_AND_AMRS',
        'candidate_contribution_state_values':['PASS_CANDIDATE','NO_PASS_CANDIDATE','REVIEW_REQUIRED'],
        'CW06_COMPARE_AND_SELECT':{
            'advance_to_cw07_requires':{
                'candidate_contribution_state':'PASS_CANDIDATE',
                'further_search_justified':False,
                'proportional_stopping_basis_recorded':True,
                'material_unresolved_domination':False,
            },
            'further_search_branch':{
                'when':{'further_search_justified':True},
                'next_step':'CW04_FORM_CANDIDATE_STRUCTURE',
                'advance_to_cw07':False,
                'preserve_unresolved_method_state':True,
            },
            'nonpassing_stopped_branch':{
                'when':{'candidate_contribution_state':'NO_PASS_CANDIDATE','further_search_justified':False},
                'next_route':'REVIEW_REQUIRED',
                'advance_to_cw07':False,
            },
        },
    }
    for coll in ('method_steps','ordered_steps'):
        step=next(x for x in c[coll] if x.get('step_id')=='CW06_COMPARE_AND_SELECT')
        step['evidence_to_advance']=[CW_EVIDENCE]
        step['branch_contract_ref']=CW_REF
        step['further_search_route']=CW_ROUTE
        if coll=='ordered_steps': step['next_step_rule']=CW_NEXT
    writej(CW_REL,c)

def patch_fixtures():
    f=loadj(FIX_REL)
    f['r6_package_local_behavior_cases']=R6_CASES
    writej(FIX_REL,f)

def patch_behavior_validator():
    p=ROOT/BEH_REL
    if not p.exists(): return
    s=p.read_text(encoding='utf-8')
    marker='    # R6 package-local behavioral contradiction regressions.'
    if marker in s: return
    anchor="    print('AIR behavioral transaction contract validation: PASS')"
    if anchor not in s: raise RuntimeError('behavior validator insertion anchor not found')
    s=s.replace(anchor, BEHAVIOR_INSERT+'\n'+anchor, 1)
    p.write_text(s, encoding='utf-8')

def main():
    patch_gov(); patch_cw(); patch_fixtures(); patch_behavior_validator()
    print('R6 source/test patch applied or already present')
if __name__=='__main__': main()
