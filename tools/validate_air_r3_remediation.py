from __future__ import annotations
import argparse, json, re, sys, copy, importlib.util, hashlib
from pathlib import Path
ROOT=Path('.')
REV15_PATH=None
class E(Exception): pass
def req(c,m):
    if not c: raise E(m)
def load(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def jpath(o,path):
    req(path.startswith('$.'),'bad path '+path)
    cur=o
    for p in path[2:].split('.'):
        if not isinstance(cur,dict) or p not in cur: raise KeyError(path)
        cur=cur[p]
    return cur
def exists(o,path):
    try: jpath(o,path); return True
    except KeyError: return False
def nonempty(v): return v not in (None,'',[],{})
def eval_pred(card,p):
    op=p['operator']
    if op=='CONST_TRUE': return True
    if op=='PATH_NOT_NULL':
        try:return jpath(card,p['path']) is not None
        except KeyError:return False
    if op=='PATH_NONEMPTY':
        try:return nonempty(jpath(card,p['path']))
        except KeyError:return False
    if op=='PATH_EQUALS':
        try:return jpath(card,p['path'])==p['expected']
        except KeyError:return False
    if op=='PATH_GTE':
        try:return jpath(card,p['path'])>=p['expected']
        except (KeyError,TypeError):return False
    if op=='PATH_NOT_IN':
        try:return jpath(card,p['path']) not in p['values']
        except KeyError:return False
    if op=='PATH_IN':
        try:return jpath(card,p['path']) in p['values']
        except KeyError:return False
    if op=='PATH_EXISTS': return exists(card,p['path'])
    if op=='ANY_PATH_NONEMPTY': return any(exists(card,x) and nonempty(jpath(card,x)) for x in p['paths'])
    if op=='ANY_PATH_NOT_NULL': return any(exists(card,x) and jpath(card,x) is not None for x in p['paths'])
    if op=='ALL': return all(eval_pred(card,x) for x in p['predicates'])
    if op=='ANY': return any(eval_pred(card,x) for x in p['predicates'])
    raise E('unknown condition op '+op)
def token_pair_valid(scope):
    if not isinstance(scope,dict): return False
    sid=scope.get('approval_scope_id')
    return bool(sid) and scope.get('approval_response_mode')=='EXACT_CANONICAL_SCOPE_TOKEN_PAIR' and set(scope.get('operational_response_tokens',[]))=={f'AIR_APPROVE::{sid}',f'AIR_REJECT::{sid}'} and len(scope.get('operational_response_tokens',[]))==2
def visibility_valid(H):
    s=H['object_visibility_authority_state']; mode=H['object_visibility_mode']
    req(s['visibility_mode_ref']=='AIR_HANDOFF_CARD.object_visibility_mode','visibility ref')
    if mode=='MINIMUM_REQUIRED_OBJECTS':
        return s['authority_source'] in {'USER_EXPLICIT','RESTORED_EXPLICIT_SELECTION'} and s['selection_evidence_ref'] is not None
    return mode=='ALL_OBJECTS' and s['authority_source'] in {'IMMUTABLE_DEFAULT_BASELINE','USER_EXPLICIT','RESTORED_EXPLICIT_SELECTION','LEGACY_UNVERIFIED_SELECTION'}
def main():
    core=(ROOT/'prompts/AIR_CORE_RUNTIME.md').read_text(); control=(ROOT/'prompts/AIR_CONTROL_SURFACE.md').read_text(); gov=(ROOT/'prompts/AIR_GOV.md').read_text()
    starter=load('prompts/AIR_DEFAULT_STARTER_PROFILE.json'); H=load('prompts/AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']; sm=H['schema_manifest']; preds=sm['condition_registry']['predicates']
    req(len(starter['validation_contract']['deterministic_contract_registry']['checks'])==82,'R1 registry lost')
    req('AIR_SURFACED_OBJECT_LEDGER: SURFACED_OBJECT_LEDGER_RECORD' in core,'R2 formal class lost')
    req('AIR_FAILURE_MODE_RECORD: FAILURE_MODE_RECORD' in core,'R2 failure class lost')
    req('"decision": "ALLOW"' in core and '"decision": "ALLOW | REJECT"' not in core,'R2 allow-only authorization lost')
    req('object_visibility_authority_state' in H and 'object_visibility_authority_state' in sm['required_fields'],'016 Handoff carrier missing')
    req('object_visibility_authority_state' in core and 'AIR_SESSION allowed object-owned top-level fields:' in core,'016 Core session carrier missing')
    req(visibility_valid(H),'016 baseline visibility authority invalid')
    cs=H['execution_state']['cognitive_scope_state']; req(cs.get('positive_execution_authority')=='NONE','v072 Handoff cognitive scope gained authority'); req(cs.get('validation_ingress_state')=='NOT_EVALUATED','v072 Handoff cognitive scope baseline fabricated validation'); req(H['mii_state'].get('cognitive_scope_ref')=='AIR_HANDOFF_CARD.execution_state.cognitive_scope_state','v072 Handoff cognitive scope ref mismatch')
    hm=copy.deepcopy(H); hm['object_visibility_mode']='MINIMUM_REQUIRED_OBJECTS'; req(not visibility_valid(hm),'016 min without explicit evidence passed')
    hm['object_visibility_authority_state']['authority_source']='USER_EXPLICIT'; hm['object_visibility_authority_state']['selection_evidence_ref']='USER_SELECTION::1'; req(visibility_valid(hm),'016 explicit min failed')
    req(not eval_pred(H,preds['HC-COND-METHOD']),'020 baseline no-method triggers')
    x=copy.deepcopy(H); x['execution_state']['method_handoff_state']['method_identity']='X'; req(eval_pred(x,preds['HC-COND-METHOD']),'020 active method not triggered')
    x=copy.deepcopy(H); x['specialist_binding_state']['active_specialist']={'id':'S'}; req(eval_pred(x,preds['HC-COND-SPECIALIST']),'021 active specialist not triggered')
    x=copy.deepcopy(H); x['action_governance_state']['open_authorizations']=['A']; req(eval_pred(x,preds['HC-COND-ACTION-GOVERNANCE']),'021 open auth not triggered')
    x=copy.deepcopy(H); x['active_artifact']['resource_scope_pin']={'pin_id':'P'}; req(eval_pred(x,preds['HC-COND-ACTION-GOVERNANCE']),'021 artifact scope pin not triggered')
    x=copy.deepcopy(H); x['execution_state']['patch_state']['patch_activity_state']='ACTIVE_FILE_MUTATION_OR_PATCH'; x['execution_state']['patch_state']['source_inventory']=[]; req(eval_pred(x,preds['HC-COND-PATCH']),'021 active patch not triggered')
    for st in ['NOT_EVALUATED','REVIEW_REQUIRED','REJECTED_MATERIALLY_DOMINATED']:
        x=copy.deepcopy(H); x['execution_state']['review_state']['step_optimality_state']=st
        req(not eval_pred(x,preds['HC-COND-AMRS-STEP-OPTIMALITY-REV15']),f'022 {st} falsely triggers')
    x=copy.deepcopy(H); x['execution_state']['knowledge_to_execution_path_state']['path_validation_state']='COMPLETE_FOR_ACTIVE_STEP'; x['execution_state']['review_state']['step_optimality_state']='PASS'; req(eval_pred(x,preds['HC-COND-AMRS-STEP-OPTIMALITY-REV15']),'022 complete stage not triggered')
    req('profile_posture_acceptance_state' in H and 'profile_posture_acceptance_state' in sm['required_fields'],'023 Handoff posture carrier missing')
    req('profile_posture_acceptance_state' in core,'023 Core session carrier missing')
    req(H['profile_posture_acceptance_state']['positive_execution_authority']=='NONE','023 posture carrier gained authority')
    block=gov[gov.index('Allowed resolution_state values:'):gov.index('Rules:',gov.index('Allowed resolution_state values:'))]
    req('- UNRESOLVED' in block,'025 UNRESOLVED not declared')
    req(H['governance_state']['floor_invariant_reference']['resolution_state']=='UNRESOLVED','025 template changed unexpectedly')
    arr=starter['compiler_contract']['approval_response_resolution']; req(arr['approval_response_mode']=='EXACT_CANONICAL_SCOPE_TOKEN_PAIR','026 mode missing')
    ev=next(e for e in starter['compiler_contract']['runtime_control_event_registry']['events'] if e['route_id']=='RT.APPROVAL_RESOLVE')
    req(any(g.get('path')=='OPEN_APPROVAL_SCOPE_TOKEN_VALIDATION_STATE' and g.get('expected')=='VALIDATED_CANONICAL_SCOPE_TOKEN_PAIR' for g in ev['guards']),'026 validated state guard missing')
    good={'approval_scope_id':'SCOPE-TEST','operational_response_tokens':['AIR_APPROVE::SCOPE-TEST','AIR_REJECT::SCOPE-TEST'],'approval_response_mode':'EXACT_CANONICAL_SCOPE_TOKEN_PAIR'}
    bad={'approval_scope_id':'SCOPE-TEST','operational_response_tokens':['YES','NO'],'approval_response_mode':'EXACT_CANONICAL_SCOPE_TOKEN_PAIR'}
    req(token_pair_valid(good) and not token_pair_valid(bad),'026 token derivation behavior wrong')
    vr=sm['validation_registry']['rules']['HC-VALIDATE-APPROVAL']; req(any(p.get('operator')=='APPROVAL_SCOPE_CANONICAL_TOKEN_PAIR' for p in vr['predicates']),'026 Handoff validation op missing')
    req('APPROVAL_SCOPE_IDENTITY_FINGERPRINT_VALID' in sm['validation_registry']['allowed_operators'],'v072 approval fingerprint operator missing')
    req(any(p.get('operator')=='APPROVAL_SCOPE_IDENTITY_FINGERPRINT_VALID' for p in vr['predicates']),'v072 approval fingerprint predicate missing')
    req(any(p.get('path')=='$.open_approval_scope.approval_scope_fingerprint' for p in vr['predicates']),'v072 approval fingerprint path missing')
    req('Allowed approval_response_mode values:' in gov and 'EXACT_CANONICAL_SCOPE_TOKEN_PAIR' in gov,'026 Gov mode enum missing')
    gov_fields=['governance_supplement_designation','governance_supplement_version','prompt_edition','governance_floor_version','floor_invariant_reference','open_approval_scope_ref','active_framework_projections','governance_source_rights_state','token_debug_preference','governance_blockers','governance_evidence_references','restricted_content_excluded']
    rule=next(r for r in sm['conditional_rules'] if r['id']=='HC-COND-GOV')
    req(set(rule['requirements'])=={'governance_state.'+f for f in gov_fields},'027 conditional requirements not 12 exact fields')
    vpaths={p['path'] for p in sm['validation_registry']['rules']['HC-VALIDATE-GOV']['predicates'] if p['operator']=='PATH_EXISTS'}
    req(vpaths=={'$.governance_state.'+f for f in gov_fields},'027 validation paths incomplete')
    req('If semantic equivalence cannot be shown, route to REVIEW_REQUIRED.' not in gov,'028 stale edition token remains')
    req('If semantic equivalence cannot be shown, route through Core AIR_GATE with decision = REVIEW.' in gov,'028 Core REVIEW mapping missing')
    method_paths=list(ROOT.glob('profiles/**/*METHOD_PACK.json')); req(len(method_paths)==5,'expected 5 method packs')
    schema_ids=set()
    for p in method_paths:
        m=json.loads(p.read_text()); hr=m.get('handoff_requirements'); req(isinstance(hr,dict),f'039 prose-only handoff requirements {p.name}')
        ms=hr.get('method_specific_state_schema',{}); req(ms.get('schema_id') and isinstance(ms.get('required_fields'),list),f'039 typed method schema missing {p.name}')
        req(all(str(x).startswith('$.') for x in hr.get('generic_required_paths',[])),f'039 generic paths not typed {p.name}')
        schema_ids.add(ms['schema_id'])
    req(len(schema_ids)==5,'039 schema ids not unique')
    mh=H['execution_state']['method_handoff_state']; req('method_specific_state_schema_ref' in mh and 'method_specific_state_schema_version' in mh,'039 Handoff schema refs absent')
    mvr=sm['validation_registry']['rules']['HC-VALIDATE-METHOD']
    if mvr.get('operator')=='ACTIVE_METHOD_PACK_HANDOFF_SCHEMA_VALID':
        active_method_validator=True
    else:
        active_method_validator=mvr.get('operator')=='ALL' and any(p.get('operator')=='ACTIVE_METHOD_PACK_HANDOFF_SCHEMA_VALID' for p in mvr.get('predicates',[]))
    req(active_method_validator,'039 active method validator absent')
    ov=load('profiles/governance specialist/AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json'); vals=ov['binding_rules']['activation_state_values']; req('NOT_EVALUATED' in vals,'051 NOT_EVALUATED missing'); req('pre_evaluation_transition_rule' in ov['binding_rules'],'051 transition rule missing')
    gm=load('profiles/governance specialist/AIR_AI_GOVERNANCE_METHOD_PACK.json'); exp=['PENDING','ACTIVE','COMPLETE','BLOCKED','REVIEW','SKIPPED_APPROVED','FAILED','INVALIDATED']; req(gm['method_execution_state_schema']['step_states']==exp,'052 step state enum mismatch')
    pc=H['source_state']['source_rights_projection_contract']; req(pc['governance_owner_path']=='AIR_HANDOFF_CARD.governance_state.governance_source_rights_state' and pc['projection_authority']=='DERIVED_NONAUTHORITATIVE' and pc['last_writer_wins'] is False,'069 projection contract missing')
    req('Canonical ownership and projection:' in gov and 'Governance-controlled source-rights records have one canonical owner' in core,'069 owner law missing')
    req(pc['conflict_behavior']=='REVIEW_BLOCK_AFFECTED_USE','069 conflict not review')
    rc=sm['revision_migration_contracts']['REV15_TO_REV16']; req(rc['apply_before_current_required_carrier_check'] is True,'072 order flag false'); rc17=sm['revision_migration_contracts']['REV16_TO_REV17']; req(rc17['apply_before_current_required_carrier_check'] is True,'v072 rev16->17 order flag false'); req(rc17['history_synthesis']=='PROHIBITED','v072 rev16->17 history synthesis not prohibited'); rc18=sm['revision_migration_contracts']['REV17_TO_REV18']; req(rc18['apply_before_current_required_carrier_check'] is True,'v072 rev17->18 order flag false'); req(rc18['history_synthesis']=='PROHIBITED','v072 rev17->18 history synthesis not prohibited'); seq=sm['validation_sequence']; req(seq.index('source card revision detection and applicable revision migration check') < seq.index('required-carrier check after applicable migration'),'072 sequence migration after required carriers'); req(rc['history_synthesis']=='PROHIBITED','072 history synthesis not prohibited')
    spec=importlib.util.spec_from_file_location('mig',str(ROOT/'tools/migrate_air_handoff.py')); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    if REV15_PATH:
        src=json.loads(Path(REV15_PATH).read_text(encoding='utf-8'))
        req(src.get('AIR_HANDOFF_CARD',{}).get('card_revision')==15,'072 supplied historical card is not rev15')
    else:
        base=json.loads((ROOT/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json').read_text(encoding='utf-8')); src=copy.deepcopy(base); c=src['AIR_HANDOFF_CARD']; c['card_revision']=15; c.pop('failure_mode_state',None); c.pop('surfaced_object_ledger_state',None); c.pop('object_visibility_authority_state',None); c.pop('profile_posture_acceptance_state',None)
    migrated=mod.migrate_to_current(src,{'AIR_HANDOFF_CARD':H})['AIR_HANDOFF_CARD']
    req(migrated['card_revision']==18,'072 target rev'); req(migrated['failure_mode_state']['history_completeness_state']=='LEGACY_UNRECORDED_PRE_REV16','072 failure history'); req(migrated['surfaced_object_ledger_state']['completeness_state']=='LEGACY_UNRECORDED_PRE_REV16','072 ledger history'); req(not migrated['failure_mode_state']['records'] and not migrated['surfaced_object_ledger_state']['entries'],'072 fabricated history'); req(migrated['migration_state']['migration_decision'].startswith('MIGRATED_REV17_TO_REV18'),'072 migration decision'); req(migrated['execution_state']['cognitive_scope_state']['positive_execution_authority']=='NONE','v072 migrated cognitive scope gained authority'); req(migrated['execution_state']['cognitive_scope_state']['validation_ingress_state']=='NOT_EVALUATED','v072 migrated cognitive scope fabricated validation')
    declared=set(sm['required_fields'])|set(sm['optional_fields']); req(set(H)==declared,'Handoff root manifest not closed')
    rmap=load('catalog/AIR_RUNTIME_ROUTE_MAP.json'); req(rmap['source_of_truth']['sha256']==hashlib.sha256(core.encode()).hexdigest(),'route map core hash stale')
    line_by={ln.split('=',1)[1]:i for i,ln in enumerate(core.splitlines(),1) if ln.startswith('id=RT.')}
    for r in rmap['routes']: req(r['source_anchor']['line']==line_by[r['route_id']],f"route anchor stale {r['route_id']}")
    print('R3 remediation validation: PASS')
    print('r3_findings',14); print('method_pack_typed_schemas',len(method_paths)); print('condition_rules',len(sm['conditional_rules'])); print('validation_rules',len(sm['validation_registry']['rules'])); print('route_anchors',len(rmap['routes']))
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('root',nargs='?',default='.'); ap.add_argument('--rev15'); a=ap.parse_args(); ROOT=Path(a.root).resolve(); REV15_PATH=a.rev15
    try: main()
    except (E,KeyError) as e:
        print('R3 remediation validation: FAIL:',e,file=sys.stderr); raise SystemExit(1)
