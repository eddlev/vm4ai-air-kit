from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path('.')
class E(Exception): pass
def req(c,m):
    if not c: raise E(m)
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def main():
    core=(ROOT/'prompts/AIR_CORE_RUNTIME.md').read_text(encoding='utf-8')
    control=(ROOT/'prompts/AIR_CONTROL_SURFACE.md').read_text(encoding='utf-8')
    gov=(ROOT/'prompts/AIR_GOV.md').read_text(encoding='utf-8')
    starter=load('prompts/AIR_DEFAULT_STARTER_PROFILE.json')
    handoff=load('prompts/AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']
    rmap=load('catalog/AIR_RUNTIME_ROUTE_MAP.json')
    index=load('catalog/AIR_SPECIALIST_PACKAGE_INDEX.json')
    fixtures=load('tests/air_contract_fixtures.json')
    for m in ['AIR_RUNTIME_CONTROL_EVENT_REGISTRY_V1','AIR_APPROVAL_RESPONSE_RESOLUTION_V1','AIR_SURFACED_OBJECT_LEDGER_V1','AIR_FAILURE_MODE_REGISTRY_V1','AIR_HANDOFF_FILE_DELIVERY_V1']:
        req(('Patch marker: '+m) in core, 'missing Core marker '+m)
    for m in ['AIR_CONTROL_APPROVAL_RESPONSE_RENDERER_V1','AIR_CONTROL_SURFACED_OBJECT_LEDGER_RENDERER_V1','AIR_CONTROL_FAILURE_MODE_LEARNING_RENDERER_V1','AIR_CONTROL_HANDOFF_FILE_DELIVERY_RENDERER_V1']:
        req(('Patch marker: '+m) in control, 'missing Control marker '+m)
    req('AIR_GOVERNANCE_DETERMINISTIC_APPROVAL_RESPONSE_V1' in gov, 'missing Governance approval deterministic rule')
    req('AIR_GOVERNANCE_FAILURE_MODE_LEARNING_V1' in gov, 'missing Governance failure learning rule')
    cc=starter['compiler_contract']
    reg=cc['runtime_control_event_registry']
    req(reg['authority_class']=='RUNTIME_OPERATIVE_TYPED_CONTRACT','runtime control registry authority mismatch')
    events={e['route_id']:e for e in reg['events']}
    routes={r['route_id']:r for r in rmap['routes']}
    req(set(events)==set(routes),'control-event registry route coverage mismatch')
    req(reg['route_count']==len(routes)==rmap['route_count'],'route count mismatch')
    allowed=set(reg['allowed_guard_operators'])
    for rid,r in routes.items():
        req(r.get('control_event_ref')==events[rid]['event_id'], rid+' control_event_ref mismatch')
        req(r.get('trigger_authority')=='NON_OPERATIVE_DESCRIPTION', rid+' natural-language trigger became operative')
        req(events[rid].get('semantic_proposal_authority')=='NONE', rid+' semantic proposal has control authority')
        for g in events[rid].get('guards',[]): req(g.get('operator') in allowed, rid+' unknown guard operator')
    req('RT.APPROVAL_RESOLVE' in routes,'approval resolution route missing')
    ar=cc['approval_response_resolution']
    req(ar['exact_match_required'] is True,'approval exact token not required')
    req(ar['natural_language_paraphrase_authority']=='NONE','natural-language approval has authority')
    mat=cc['material_action_transaction']
    seq=mat['ordered_pre_and_post_effect_states']
    req(seq.index('AUTHORITY_OBJECTS_LEDGER_COMMITTED')>seq.index('AIR_ACTION_AUTHORIZATION_EMITTED'),'authority ledger not after Authorization')
    req(seq.index('AUTHORITY_OBJECTS_LEDGER_COMMITTED')<seq.index('EFFECT_ATTEMPT'),'effect can precede authority ledger')
    req(mat['authority_ledger_required_before_effect'] is True,'authority ledger barrier missing')
    led=cc['surfaced_object_ledger']; req(led['authorization_consumption_requires_ledger_entry'] is True,'Authorization ledger consumption barrier missing')
    fm=cc['failure_mode_registry']; req(fm['pre_retry_query_required'] is True,'failure-mode pre-retry query missing'); req(fm['automatic_applicability']=='EXACT_MATCH_ONLY','failure-mode exact match boundary missing'); req(fm['specialist_registry_mutation_authority']=='NONE','Specialist can mutate failure registry')
    req(fm['applicability_signature_schema']['exact_match_rule']=='CURRENT_SIGNATURE_HASH_EQUALS_RECORDED_APPLICABILITY_SIGNATURE_HASH','failure applicability signature hash rule missing')
    req(fm['failure_record_source_ledger_entry_required'] is True,'failure record ledger-source requirement missing')
    req('AIR-FLOOR-027-FAILURE-MODE-LEARNING-AND-RETRY' in starter['authority_contract']['floor_invariants_required'],'Starter floor027 missing')
    sm=handoff['schema_manifest']; req(sm['strict_output_mode']=='DOWNLOADABLE_JSON_FILE_ONLY','handoff is not file-only'); req(sm['handoff_delivery_contract']['inline_chat_payload']=='PROHIBITED','inline handoff payload allowed'); req('failure_mode_state' in sm['required_fields'],'handoff failure_mode_state not required')
    creg=sm['condition_registry']; preds=creg['predicates']; allowedc=set(creg['allowed_operators'])
    for rule in sm['conditional_rules']:
        req(rule.get('condition_authority')=='NON_OPERATIVE_DESCRIPTION','handoff semantic condition became operative: '+rule.get('id','?'))
        rid=rule['id']; req(rid in preds,'handoff predicate missing '+rid)
        op=preds[rid].get('operator'); req(op in allowedc,'handoff unknown predicate operator '+rid)
    pol=handoff['action_governance_state']['provenance_policy']; req(pol['surfaced_object_ledger_required'] is True,'handoff ledger provenance missing')
    fms=handoff['failure_mode_state']; req(fms['positive_execution_authority']=='NONE','handoff failure modes have execution authority')
    req(fms['automatic_match_rule']=='EXACT_CANONICAL_SIGNATURE_HASH_EQUALITY_ONLY_AFTER_RESTORE_VALIDATION','handoff failure-mode exact hash rule missing')
    manifests=sorted(ROOT.glob('profiles/**/*PACKAGE_MANIFEST.json')); req(len(manifests)==5,'expected five Specialist manifests')
    for p in manifests:
        m=json.loads(p.read_text(encoding='utf-8')); c=m.get('failure_mode_integration_contract',{}); req(c.get('required') is True,str(p)+' failure integration missing'); req(c.get('package_scope')=='ALL_PACKAGE_COMPONENTS',str(p)+' failure integration not all components'); req(c.get('package_or_component_registry_mutation_authority')=='NONE',str(p)+' can mutate registry'); req(c.get('exact_match_rule')=='CURRENT_CANONICAL_APPLICABILITY_SIGNATURE_HASH_EQUALS_RECORDED_HASH',str(p)+' exact failure signature hash rule missing')
    req(index['failure_mode_integration_policy']['required_for_all_catalogued_packages'] is True,'Specialist index failure integration policy missing')
    for e in index['entries']: req(e.get('failure_mode_integration_required') is True,'Specialist index entry missing failure integration '+e.get('package_identity','?'))
    ids={x['id'] for x in fixtures['failure_mode_learning_cases']}; req({'FM-01-RETRY-EXACT-MATCH','FM-05-SPECIALIST-PACKAGE','FM-06-HANDOFF-PERSISTENCE'}<=ids,'failure learning fixtures incomplete')
    print('AIR semantic-loophole/control-plane validation: PASS')
    print('Typed runtime control events:',len(routes))
    print('Specialist failure-mode integration packages:',len(manifests))
if __name__=='__main__':
    try: main()
    except E as e:
        print('AIR semantic-loophole/control-plane validation: FAIL:',e,file=sys.stderr); raise SystemExit(1)
