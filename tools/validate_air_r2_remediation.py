from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
class E(Exception): pass
def req(c,m):
    if not c: raise E(m)
def reject(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise E(f'duplicate JSON key: {k}')
        d[k]=v
    return d
def load(p): return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=reject)
def main(root:Path):
    core_p=root/'prompts/AIR_CORE_RUNTIME.md'; core=core_p.read_text(encoding='utf-8')
    control=(root/'prompts/AIR_CONTROL_SURFACE.md').read_text(encoding='utf-8')
    gov=(root/'prompts/AIR_GOV.md').read_text(encoding='utf-8')
    starter=load(root/'prompts/AIR_DEFAULT_STARTER_PROFILE.json')
    handoff=load(root/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']
    rmap=load(root/'catalog/AIR_RUNTIME_ROUTE_MAP.json')
    m=re.search(r'Canonical formal object classes:\n(?P<b>(?:- AIR_[A-Z_]+: [A-Z_]+\n)+)\nObject identity',core)
    req(bool(m),'canonical formal-object class registry not parseable')
    classes={ln[2:].split(':',1)[0]:ln.split(':',1)[1].strip() for ln in m.group('b').strip().splitlines()}
    req(len(classes)==18,f'formal object class count {len(classes)} != 18')
    req(classes.get('AIR_SURFACED_OBJECT_LEDGER')=='SURFACED_OBJECT_LEDGER_RECORD','ledger formal class missing/wrong')
    req(classes.get('AIR_FAILURE_MODE_RECORD')=='FAILURE_MODE_RECORD','failure formal class missing/wrong')
    req(classes.get('AIR_METHOD_EVIDENCE_WAIVER')=='METHOD_EVIDENCE_WAIVER_RECORD','method evidence waiver formal class missing/wrong')
    m=re.search(r'Reserved formal object labels include:\n(?P<b>(?:- AIR_[A-Z_]+\n)+)\nAIR must not use',core)
    req(bool(m),'reserved formal label set not parseable')
    reserved={ln[2:] for ln in m.group('b').strip().splitlines()}
    req(set(classes)==reserved,f'formal class/reserved label mismatch: {set(classes)^reserved}')
    owner_names=set(re.findall(r'(?m)^(AIR_[A-Z_]+)(?: base)? allowed object-owned top-level fields(?: are exactly[^\n]*)?:',core))
    if 'AIR_REQUIRED_INPUT_REQUEST allowed object-owned top-level fields are exactly' in core: owner_names.add('AIR_REQUIRED_INPUT_REQUEST')
    if 'AIR_HANDOFF_CARD allowed top-level fields are exactly' in core: owner_names.add('AIR_HANDOFF_CARD')
    req(owner_names==set(classes),f'formal class/field owner mismatch: {owner_names^set(classes)}')
    starter_ids=set(starter['typed_registries']['formal_objects']['object_ids'])
    req(starter_ids==set(classes),f'Starter formal object mirror mismatch: {starter_ids^set(classes)}')
    art=core[core.index('AIR_ARTIFACT base allowed object-owned top-level fields:'):core.index('AIR_ACTIVE_CONTRACT allowed object-owned top-level fields:')]
    req('prompt_layer_qualitative_trace when prompt-layer qualitative native checks materially affect the active step' in art,'Artifact qualitative trace not registered')
    req('This trace is mandatory when prompt AIR references backend-inspired native behavior.' in core,'qualitative trace mandatory trigger missing')
    gm=re.search(r'AIR_GATE decision values:\n(?P<b>(?:- [A-Z_]+\n)+)',core); req(bool(gm),'Gate enum not parseable')
    gates={x[2:] for x in gm.group('b').strip().splitlines()}
    req(gates=={'ALLOW','REVIEW','REJECT','RESCOPE_REQUIRED','EVIDENCE_REQUIRED'},f'Gate enum mismatch {gates}')
    joined='\n'.join([core,control,json.dumps(starter,ensure_ascii=False),json.dumps(rmap,ensure_ascii=False)])
    for bad in ['HOLD Gate','PRIOR_HOLD_GATE','prior_hold_gate']:
        req(bad not in joined,f'undefined Gate HOLD token remains: {bad}')
    req('PRIOR_REVIEW_GATE_WHEN_RESOLVED' in core and 'PRIOR_REVIEW_GATE_WHEN_RESOLVED' in json.dumps(rmap),'approval resolution REVIEW invalidation missing')
    req(starter['compiler_contract']['material_action_transaction'].get('prior_review_gate_may_be_reused_as_allow') is False,'Starter REVIEW Gate reuse barrier missing')
    sec=core[core.index('AIR_ACTION_AUTHORIZATION exact schema:'):core.index('The authorization references gate_ref',core.index('AIR_ACTION_AUTHORIZATION exact schema:'))]
    req('"decision": "ALLOW"' in sec,'Authorization ALLOW decision missing')
    req('REJECT' not in sec,'Authorization still exposes lifecycle-unreachable REJECT')
    expected='Governance source-rights state must feed AIR_GATE.evaluation_checks.evidence, AIR_GATE.evaluation_checks.allowed_action, AIR_GATE.evaluation_checks.stop_condition, and AIR_GATE.reason when source use is material.'
    req(expected in gov,'Governance source-rights Gate mapping not canonical')
    for bad in ['AIR_GATE evidence_check','AIR_GATE allowed_action_check','AIR_GATE stop_condition_check']:
        req(bad not in gov,f'Governance retired Gate alias remains: {bad}')
    led=starter['compiler_contract']['surfaced_object_ledger']; fm=starter['compiler_contract']['failure_mode_registry']
    fmt='AIR_SURFACED_OBJECT_LEDGER_ENTRY::<ledger_id>::<emission_sequence>'
    req(led.get('entry_reference_field')=='ledger_entry_ref','Starter ledger entry ref field missing')
    req(led.get('entry_reference_format')==fmt,'Starter ledger ref format mismatch')
    req(led.get('ledger_id_scope')=='STABLE_FOR_GOVERNED_SESSION','ledger_id scope not pinned')
    res=led.get('failure_record_entry_reservation',{})
    req(res.get('reservation_state')=='RESERVED_NOT_EMITTED_NOT_AUTHORITY','reservation authority boundary missing')
    req(res.get('inference_policy')=='PROHIBITED','reservation inference not prohibited')
    req(res.get('commit_rule')=='COMMIT_ONLY_AFTER_EXACT_CANONICAL_OBJECT_VISIBLE_EMISSION_WITH_MATCHING_REF_AND_HASH','reservation commit rule mismatch')
    req(res.get('abort_rule')=='DISCARD_RESERVATION_AND_DO_NOT_ADVANCE_COMMITTED_SEQUENCE','reservation abort rule mismatch')
    seq=fm.get('first_emission_transaction',[])
    req(seq==['RESERVE_NEXT_LEDGER_ENTRY_REF','CONSTRUCT_FAILURE_RECORD_WITH_RESERVED_SOURCE_LEDGER_ENTRY_REF','CANONICALIZE_AND_HASH_FAILURE_RECORD','VISIBLY_EMIT_FAILURE_RECORD','COMMIT_MATCHING_USER_VISIBLE_EMITTED_LEDGER_ENTRY_WITH_EXACT_HASH','ONLY_THEN_SOURCE_LEDGER_ENTRY_REF_RESOLVES'],f'failure first-emission sequence mismatch: {seq}')
    req(fm.get('source_ledger_entry_ref_semantics')=='SELF_FIRST_COMMITTED_SURFACED_LEDGER_ENTRY','failure source ref semantics ambiguous')
    req('ledger_entry_ref\n- emission_sequence' in core or 'ledger_entry_ref\r\n- emission_sequence' in core,'Core ledger entry schema lacks ledger_entry_ref')
    req('source_ledger_entry_ref means the record\'s own first committed AIR_SURFACED_OBJECT_LEDGER entry' in core,'Core failure self-ledger meaning missing')
    req('reserve the next ledger_entry_ref' in core,'Core failure ref reservation step missing')
    hreq=handoff['surfaced_object_ledger_state']['entry_requirements']['required_fields']
    req('ledger_entry_ref' in hreq,'Handoff ledger entries omit ledger_entry_ref')
    req(handoff['failure_mode_state'].get('source_ledger_entry_ref_semantics')=='SELF_FIRST_COMMITTED_SURFACED_LEDGER_ENTRY','Handoff failure ref semantics mismatch')
    req('OBJECT_NAME_AIR_FAILURE_MODE_RECORD' in handoff['failure_mode_state'].get('source_ledger_entry_ref_validation_rule',''),'Handoff failure ref resolution rule incomplete')
    ledger_id='LEDGER-R2-TEST'; emission_sequence=17
    ref=f'AIR_SURFACED_OBJECT_LEDGER_ENTRY::{ledger_id}::{emission_sequence}'
    rec={'object_version':'2.0.0','record_class':'FAILURE_MODE_RECORD','failure_mode_id':'FM-R2-TEST','source_ledger_entry_ref':ref,'runtime_origin':'PROMPT_COMPILED','backend_validation_claimed':False,'hidden_reasoning_claimed':False}
    raw=json.dumps(rec,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode(); sha=hashlib.sha256(raw).hexdigest()
    entry={'ledger_entry_ref':ref,'emission_sequence':emission_sequence,'object_name':'AIR_FAILURE_MODE_RECORD','object_identity':'FM-R2-TEST','record_class':'FAILURE_MODE_RECORD','canonical_object_sha256':sha,'visibility_state':'USER_VISIBLE_EMITTED'}
    req(entry['ledger_entry_ref']==rec['source_ledger_entry_ref'],'synthetic positive ref mismatch')
    req(entry['canonical_object_sha256']==hashlib.sha256(raw).hexdigest(),'synthetic positive hash mismatch')
    bad=dict(entry); bad['ledger_entry_ref']=f'AIR_SURFACED_OBJECT_LEDGER_ENTRY::{ledger_id}::18'
    req(bad['ledger_entry_ref']!=rec['source_ledger_entry_ref'],'synthetic negative ref mutant not constructed')
    req(rmap['source_of_truth']['sha256']==hashlib.sha256(core_p.read_bytes()).hexdigest(),'Route Map Core hash stale after R2')
    line_by={ln.split('=',1)[1]:i for i,ln in enumerate(core.splitlines(),1) if ln.startswith('id=RT.')}
    for rr in rmap['routes']:
        req(rr['source_anchor']['line']==line_by[rr['route_id']],f'{rr["route_id"]}: Route Map anchor stale after R2')
    fxp=root/'tests/air_contract_fixtures.json'
    if fxp.is_file():
        fx=load(fxp)
        mids={x['id'] for x in fx.get('material_action_transaction_negative_cases',[])}
        req('MAT-02-REVIEW-GATE-IMPLICITLY-UPGRADED' in mids,'REVIEW Gate material-action fixture missing')
        req('MAT-02-HOLD-GATE-IMPLICITLY-UPGRADED' not in mids,'HOLD Gate fixture remains')
        fids={x['id'] for x in fx.get('failure_mode_learning_cases',[])}
        req({'FM-07-FIRST-EMISSION-LEDGER-RESERVATION','FM-08-FAILURE-LEDGER-REF-MISMATCH'}<=fids,'failure ledger fixtures incomplete')
        req(len(fx.get('r2_formal_object_contract_cases',[]))>=5,'R2 formal object fixture section incomplete')
    print('R2 remediation validation: PASS')
    print('formal_object_classes',len(classes))
    print('gate_decisions',len(gates))
    print('authorization_decisions',1)
    print('failure_first_emission_steps',len(seq))
    print('route_anchors',len(rmap['routes']))
if __name__=='__main__':
    try: main(Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve())
    except (E,KeyError,ValueError) as e:
        print('R2 remediation validation: FAIL:',e,file=sys.stderr); raise SystemExit(1)
