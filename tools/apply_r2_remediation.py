from __future__ import annotations
import json, hashlib, re, sys
from pathlib import Path

class PatchError(RuntimeError): pass

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o): p.write_text(json.dumps(o, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
def replace_once(t, old, new, label):
    if new in t: return t, False
    n=t.count(old)
    if n==0:
        raise PatchError(f'{label}: anchor not found')
    if n!=1: raise PatchError(f'{label}: expected one anchor, found {n}')
    return t.replace(old,new,1), True

def patch(root: Path):
    changed=[]
    core_p=root/'prompts/AIR_CORE_RUNTIME.md'; core=core_p.read_text(encoding='utf-8'); orig=core
    core,_=replace_once(core,
        '- AIR_ACTION_RECEIPT: ACTION_RECEIPT_RECORD\n- AIR_PRIOR_EFFECT_RECORD: RECOVERY_RECORD',
        '- AIR_ACTION_RECEIPT: ACTION_RECEIPT_RECORD\n- AIR_SURFACED_OBJECT_LEDGER: SURFACED_OBJECT_LEDGER_RECORD\n- AIR_FAILURE_MODE_RECORD: FAILURE_MODE_RECORD\n- AIR_PRIOR_EFFECT_RECORD: RECOVERY_RECORD',
        'formal object class closure')
    core,_=replace_once(core,
        '- test_evidence_requirements when testing/evidence affects execution\n\nAIR_ACTIVE_CONTRACT allowed object-owned top-level fields:',
        '- test_evidence_requirements when testing/evidence affects execution\n- prompt_layer_qualitative_trace when prompt-layer qualitative native checks materially affect the active step; mandatory when prompt AIR references backend-inspired native behavior\n\nAIR_ACTIVE_CONTRACT allowed object-owned top-level fields:',
        'artifact qualitative trace registration')
    old=('AIR maintains a prompt-layer append-only surfaced-object ledger for every canonical formal AIR object actually emitted in the governed session. '
         'A ledger entry is valid only for a canonical object actually emitted earlier in the same visible response or a prior response already carrying a valid ledger entry. '
         'Constructed-but-not-emitted objects do not enter the ledger. AIR_SURFACED_OBJECT_LEDGER cannot include itself in its own same-response entries; the next ledger emission records the prior ledger object. '
         'Every substantive post-activation governed response that emits any formal AIR object must end its formal-object section with a ledger delta before narrative/delivery, except that a material-effect response may emit the pre-effect authority ledger barrier and a later post-effect ledger delta.')
    new=('AIR maintains a prompt-layer append-only surfaced-object ledger for every canonical formal AIR object actually emitted in the governed session. '
         'A committed ledger entry is valid only for a canonical object actually emitted earlier in the same visible response or a prior response already carrying a valid ledger entry. '
         'Constructed-but-not-emitted objects do not enter the ledger. The sole pre-emission exception is reservation of a ledger-entry identity when a canonical object schema requires a reference to its own eventual surfaced ledger entry; a reservation is not a committed entry, does not assert USER_VISIBLE_EMITTED, and grants no authority. '
         'AIR_SURFACED_OBJECT_LEDGER cannot include itself in its own same-response entries; the next ledger emission records the prior ledger object. '
         'Every substantive post-activation governed response that emits any formal AIR object must end its formal-object section with a ledger delta before narrative/delivery, except that a material-effect response may emit the pre-effect authority ledger barrier and a later post-effect ledger delta.')
    core,_=replace_once(core,old,new,'ledger reservation rule')
    core,_=replace_once(core,
        'Each entry contains:\n- emission_sequence\n- object_name',
        'Each entry contains:\n- ledger_entry_ref\n- emission_sequence\n- object_name',
        'ledger entry ref field')
    anchor='- source_state_epoch\n\nAll canonical formal objects are ledgered.'
    insertion='''- source_state_epoch\n\nCanonical ledger-entry identity and reservation protocol:\n- ledger_id is stable for the governed session ledger across emitted ledger deltas; previous_ledger_hash and ledger_hash chain those emitted deltas.\n- ledger_entry_ref = AIR_SURFACED_OBJECT_LEDGER_ENTRY::<ledger_id>::<emission_sequence>. The pair ledger_id + emission_sequence is unique within the governed session.\n- Reservation is permitted only when a Core-owned canonical schema requires an object to carry a reference to its own first surfaced ledger entry before that object can be canonically hashed.\n- Reservation sequence is deterministic: reserve the next uncommitted emission_sequence without advancing committed ledger state; construct ledger_entry_ref; place that exact ref into the object; canonicalize/hash and visibly emit the object; then commit the ledger entry with the same ref and exact canonical_object_sha256.\n- If construction or visible emission fails, discard the reservation and do not advance the committed emission sequence. A discarded reservation has no historical, visibility, approval, or execution meaning.\n- A reserved ref is not resolvable for dependency, Handoff, retry, or provenance purposes until the matching USER_VISIBLE_EMITTED ledger entry is committed. Semantic inference may not synthesize, repair, or redirect a reserved or committed ledger_entry_ref.\n\nAll canonical formal objects are ledgered.'''
    core,_=replace_once(core,anchor,insertion,'ledger reservation protocol insertion')
    old='Every surfaced AIR_FAILURE_MODE_RECORD must carry source_ledger_entry_ref after it is visibly emitted; Handoff may preserve the record only through that ledger-backed identity.'
    new=('For AIR_FAILURE_MODE_RECORD, source_ledger_entry_ref means the record\'s own first committed AIR_SURFACED_OBJECT_LEDGER entry, not an evidence-source reference; evidence sources remain in evidence_refs. '
         'Before first visible emission, AIR must reserve the next ledger_entry_ref under the canonical reservation protocol and place that exact ref in source_ledger_entry_ref before canonicalization and hashing. '
         'The ref becomes resolvable only after the matching USER_VISIBLE_EMITTED ledger entry is committed with the exact emitted record hash. Handoff may preserve the record only through that committed ledger-backed identity.')
    core,_=replace_once(core,old,new,'failure record self-ledger semantics')
    old='5. A same-turn reference to a Gate, Authorization, Receipt, Artifact, Session, Map, or other formal object may point only to an object actually constructed and schema-valid in the current transaction, or to a specifically permitted previously observed object whose identity and state remain current.'
    new=('5. A same-turn reference to a Gate, Authorization, Receipt, Artifact, Session, Map, or other formal object may point only to an object actually constructed and schema-valid in the current transaction, or to a specifically permitted previously observed object whose identity and state remain current. '
         'The only forward-reserved provenance exception is AIR_FAILURE_MODE_RECORD.source_ledger_entry_ref under AIR_SURFACED_OBJECT_LEDGER_V1: it must match a valid reserved ledger_entry_ref and must be committed to the exact emitted record before any dependency, persistence, retry, or Handoff use.')
    core,_=replace_once(core,old,new,'constructor reservation exception')
    for old,new,label in [
        ('invalidates=PRIOR_HOLD_GATE_WHEN_RESOLVED','invalidates=PRIOR_REVIEW_GATE_WHEN_RESOLVED','approval route invalidation'),
        ('A prior HOLD Gate does not become ALLOW by implication when approval later arrives','A prior REVIEW Gate does not become ALLOW by implication when approval later arrives','material action review gate'),
        ('missing, stale, HOLD, null, mismatched, un-emitted, or schema-invalid','missing, stale, REVIEW, null, mismatched, un-emitted, or schema-invalid','material predecessor review state'),
        ('User approval, a HOLD Gate, a planned validation_after_receipt step','User approval, a REVIEW Gate, a planned validation_after_receipt step','handoff review gate')]:
        core,_=replace_once(core,old,new,label)
    core,_=replace_once(core,'    "decision": "ALLOW | REJECT",','    "decision": "ALLOW",','authorization decision enum')
    if core!=orig:
        core_p.write_text(core,encoding='utf-8'); changed.append(str(core_p.relative_to(root)))

    p=root/'prompts/AIR_CONTROL_SURFACE.md'; t=p.read_text(encoding='utf-8'); orig=t
    t,_=replace_once(t,'A prior HOLD Gate, planned authorization, receipt-authored reference, or prose assertion cannot substitute','A prior REVIEW Gate, planned authorization, receipt-authored reference, or prose assertion cannot substitute','control review gate')
    if t!=orig: p.write_text(t,encoding='utf-8'); changed.append(str(p.relative_to(root)))

    p=root/'prompts/AIR_GOV.md'; t=p.read_text(encoding='utf-8'); orig=t
    old='Governance source-rights state must feed AIR_GATE evidence_check, allowed_action_check, stop_condition_check, and reason when source use is material.'
    new='Governance source-rights state must feed AIR_GATE.evaluation_checks.evidence, AIR_GATE.evaluation_checks.allowed_action, AIR_GATE.evaluation_checks.stop_condition, and AIR_GATE.reason when source use is material.'
    t,_=replace_once(t,old,new,'governance gate paths')
    if t!=orig: p.write_text(t,encoding='utf-8'); changed.append(str(p.relative_to(root)))

    p=root/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); before=json.dumps(o,ensure_ascii=False,sort_keys=True)
    ids=o['typed_registries']['formal_objects']['object_ids']
    for name, after in [('AIR_SURFACED_OBJECT_LEDGER','AIR_ACTION_RECEIPT'),('AIR_FAILURE_MODE_RECORD','AIR_SURFACED_OBJECT_LEDGER')]:
        if name not in ids:
            ids.insert(ids.index(after)+1,name)
    mat=o['compiler_contract']['material_action_transaction']
    if 'prior_hold_gate_may_be_reused_as_allow' in mat:
        val=mat.pop('prior_hold_gate_may_be_reused_as_allow')
        mat['prior_review_gate_may_be_reused_as_allow']=val
    elif 'prior_review_gate_may_be_reused_as_allow' not in mat: raise PatchError('Starter review gate key missing')
    led=o['compiler_contract']['surfaced_object_ledger']
    led.update({
        'ledger_id_scope':'STABLE_FOR_GOVERNED_SESSION',
        'entry_reference_field':'ledger_entry_ref',
        'entry_reference_format':'AIR_SURFACED_OBJECT_LEDGER_ENTRY::<ledger_id>::<emission_sequence>',
        'failure_record_entry_reservation':{
            'permitted_for':['AIR_FAILURE_MODE_RECORD.source_ledger_entry_ref'],
            'reservation_state':'RESERVED_NOT_EMITTED_NOT_AUTHORITY',
            'sequence_allocation_rule':'RESERVE_NEXT_UNCOMMITTED_EMISSION_SEQUENCE_WITHOUT_ADVANCING_COMMITTED_SEQUENCE',
            'commit_rule':'COMMIT_ONLY_AFTER_EXACT_CANONICAL_OBJECT_VISIBLE_EMISSION_WITH_MATCHING_REF_AND_HASH',
            'abort_rule':'DISCARD_RESERVATION_AND_DO_NOT_ADVANCE_COMMITTED_SEQUENCE',
            'resolution_rule':'REFERENCE_RESOLVES_ONLY_AFTER_MATCHING_USER_VISIBLE_EMITTED_LEDGER_ENTRY_COMMIT',
            'inference_policy':'PROHIBITED'
        }
    })
    fm=o['compiler_contract']['failure_mode_registry']
    fm.update({
        'source_ledger_entry_ref_semantics':'SELF_FIRST_COMMITTED_SURFACED_LEDGER_ENTRY',
        'source_ledger_entry_ref_evidence_source_role':'NONE_USE_EVIDENCE_REFS_FOR_EVIDENCE_SOURCES',
        'first_emission_transaction':[
            'RESERVE_NEXT_LEDGER_ENTRY_REF',
            'CONSTRUCT_FAILURE_RECORD_WITH_RESERVED_SOURCE_LEDGER_ENTRY_REF',
            'CANONICALIZE_AND_HASH_FAILURE_RECORD',
            'VISIBLY_EMIT_FAILURE_RECORD',
            'COMMIT_MATCHING_USER_VISIBLE_EMITTED_LEDGER_ENTRY_WITH_EXACT_HASH',
            'ONLY_THEN_SOURCE_LEDGER_ENTRY_REF_RESOLVES'
        ],
        'reservation_authority':'NONE_UNTIL_MATCHING_LEDGER_ENTRY_COMMIT'
    })
    ctor=o['compiler_contract']['formal_object_constructor_validation']['checks']
    if 'FAILURE_MODE_RESERVED_LEDGER_ENTRY_REF_VALID' not in ctor:
        ctor.append('FAILURE_MODE_RESERVED_LEDGER_ENTRY_REF_VALID')
    after=json.dumps(o,ensure_ascii=False,sort_keys=True)
    if after!=before: dump(p,o); changed.append(str(p.relative_to(root)))

    p=root/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; o=load(p); before=json.dumps(o,ensure_ascii=False,sort_keys=True)
    card=o['AIR_HANDOFF_CARD']; sls=card['surfaced_object_ledger_state']; req=sls['entry_requirements']['required_fields']
    if 'ledger_entry_ref' not in req: req.insert(0,'ledger_entry_ref')
    sls['entry_requirements']['ledger_entry_ref_rule']='AIR_SURFACED_OBJECT_LEDGER_ENTRY::<ledger_id>::<emission_sequence>; UNIQUE_AND_MATCHES_ENTRY_LEDGER_ID_AND_EMISSION_SEQUENCE'
    sls['entry_requirements']['reserved_reference_rule']='RESERVATION_ALONE_IS_NOT_HISTORY; ONLY_COMMITTED_USER_VISIBLE_EMITTED_ENTRY_MAY_BE_SERIALIZED'
    fms=card['failure_mode_state']
    fms['source_ledger_entry_ref_semantics']='SELF_FIRST_COMMITTED_SURFACED_LEDGER_ENTRY'
    fms['source_ledger_entry_ref_validation_rule']='MUST_RESOLVE_TO_COMMITTED_LEDGER_ENTRY_WITH_OBJECT_NAME_AIR_FAILURE_MODE_RECORD_AND_CANONICAL_SNAPSHOT_HASH_EQUAL_TO_RECORD_HASH'
    fms['unresolved_reserved_reference_behavior']='FAIL_CLOSED_DO_NOT_PERSIST_OR_AUTO_APPLY'
    cr=card['schema_manifest']['conditional_rules']
    for rule in cr:
        if rule.get('id')=='HC-COND-FAILURE-MODE':
            rule['requirements']=[('every failure_mode_state.records entry preserves source_ledger_entry_ref as its own first committed surfaced-object ledger entry' if x=='every failure_mode_state.records entry preserves source_ledger_entry_ref' else x) for x in rule.get('requirements',[])]
    after=json.dumps(o,ensure_ascii=False,sort_keys=True)
    if after!=before: dump(p,o); changed.append(str(p.relative_to(root)))

    p=root/'catalog/AIR_RUNTIME_ROUTE_MAP.json'; o=load(p); before=json.dumps(o,ensure_ascii=False,sort_keys=True)
    for r in o['routes']:
        if r['route_id']=='RT.APPROVAL_RESOLVE':
            r['invalidates']=['PRIOR_REVIEW_GATE_WHEN_RESOLVED' if x=='PRIOR_HOLD_GATE_WHEN_RESOLVED' else x for x in r.get('invalidates',[])]
    core_text=core_p.read_text(encoding='utf-8'); o['source_of_truth']['sha256']=hashlib.sha256(core_p.read_bytes()).hexdigest()
    line_by={ln.split('=',1)[1]:i for i,ln in enumerate(core_text.splitlines(),1) if ln.startswith('id=RT.')}
    for r in o['routes']:
        r['source_anchor']['line']=line_by[r['route_id']]
    after=json.dumps(o,ensure_ascii=False,sort_keys=True)
    if after!=before: dump(p,o); changed.append(str(p.relative_to(root)))

    fxp=root/'tests/air_contract_fixtures.json'
    if fxp.is_file():
        fx=load(fxp); before=json.dumps(fx,ensure_ascii=False,sort_keys=True)
        mats=fx.get('material_action_transaction_negative_cases',[])
        for c in mats:
            if c.get('id')=='MAT-02-HOLD-GATE-IMPLICITLY-UPGRADED':
                c['id']='MAT-02-REVIEW-GATE-IMPLICITLY-UPGRADED'
                c['invalid_if']='prior REVIEW Gate is treated as current ALLOW after approval without constructing and emitting a current ALLOW Gate'
        fms=fx.get('failure_mode_learning_cases',[])
        if not any(c.get('id')=='FM-07-FIRST-EMISSION-LEDGER-RESERVATION' for c in fms):
            fms.append({'id':'FM-07-FIRST-EMISSION-LEDGER-RESERVATION','setup':'new evidenced reusable failure mode has no prior surfaced ledger entry','expected':['reserve next ledger_entry_ref without committing visibility','construct failure record with reserved source_ledger_entry_ref','hash and visibly emit exact failure record','commit matching USER_VISIBLE_EMITTED ledger entry with same ref and exact hash','only then allow persistence/retry/Handoff resolution'],'fail_if':['record emitted with null or invented source_ledger_entry_ref','reservation treated as emitted history or authority','ledger entry hash differs from exact emitted failure record','dependency or Handoff resolves the ref before entry commit']})
        if not any(c.get('id')=='FM-08-FAILURE-LEDGER-REF-MISMATCH' for c in fms):
            fms.append({'id':'FM-08-FAILURE-LEDGER-REF-MISMATCH','setup':'failure record carries a source_ledger_entry_ref that resolves to a different object/ref/hash','expected':['fail closed for persistence and automatic applicability','do not repair reference by semantic inference'],'fail_if':['mismatched entry accepted','record auto-applied despite unresolved or mismatched self-ledger identity']})
        fx['r2_formal_object_contract_cases']=[
            {'id':'R2-FO-01-FORMAL-CLASS-CLOSURE','invalid_if':'reserved Core formal object with closed-world field schema is absent from canonical formal-object class registry'},
            {'id':'R2-FO-02-ARTIFACT-TRACE-REGISTRATION','invalid_if':'prompt_layer_qualitative_trace is required/used but absent from AIR_ARTIFACT allowed field registry'},
            {'id':'R2-GATE-01-NONCANONICAL-HOLD','invalid_if':'HOLD is referenced as an AIR_GATE decision/state without being in canonical Gate enum'},
            {'id':'R2-AUTH-01-REJECT-AUTHORIZATION','invalid_if':'AIR_ACTION_AUTHORIZATION accepts REJECT without an explicit canonical reject-authorization lifecycle'},
            {'id':'R2-GOV-01-RETIRED-GATE-PATHS','invalid_if':'Governance source-rights mapping targets evidence_check/allowed_action_check/stop_condition_check instead of AIR_GATE.evaluation_checks nested paths'}
        ]
        after=json.dumps(fx,ensure_ascii=False,sort_keys=True)
        if after!=before: dump(fxp,fx); changed.append(str(fxp.relative_to(root)))

    print('R2 source patch applied' if changed else 'R2 source patch already applied; no mutation performed')
    for x in changed: print('changed',x)
    print('Core sha256',hashlib.sha256(core_p.read_bytes()).hexdigest())
    print('Route anchors',len(load(root/'catalog/AIR_RUNTIME_ROUTE_MAP.json')['routes']))
    return changed

if __name__=='__main__':
    try: patch(Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve())
    except (PatchError,KeyError,ValueError) as e:
        print('R2 remediation patch FAILED:',e,file=sys.stderr); raise SystemExit(1)
