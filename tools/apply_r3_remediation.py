from __future__ import annotations
import argparse, json, hashlib, re, shutil, os
from pathlib import Path

ROOT=Path('.')

def load(rel):
    return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def save(rel,obj):
    (ROOT/rel).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def replace_once(text, old, new, label):
    if new in text: return text
    if old not in text: raise RuntimeError(f'{label}: old anchor not found')
    if text.count(old)!=1: raise RuntimeError(f'{label}: old anchor count {text.count(old)}')
    return text.replace(old,new,1)
def insert_before_sentinel(rel, block, sentinel):
    p=ROOT/rel; t=p.read_text(encoding='utf-8')
    marker=block.strip().splitlines()[0]
    if marker in t: return
    idx=t.rfind(sentinel)
    if idx<0: raise RuntimeError(f'{rel}: sentinel missing')
    t=t[:idx].rstrip()+"\n\n"+block.strip()+"\n\n"+t[idx:]
    p.write_text(t,encoding='utf-8')

def patch_core():
    rel='prompts/AIR_CORE_RUNTIME.md'; p=ROOT/rel; t=p.read_text(encoding='utf-8')
    old='''A v2 handoff card is valid for restoration only when:\n1. it parses as strict JSON with exactly one top-level root key, AIR_HANDOFF_CARD\n2. AIR_HANDOFF_CARD.template_designation = AIR_HANDOFF_CARD_TEMPLATE_V2\n3. AIR_HANDOFF_CARD.schema_version = Core CANONICAL_HANDOFF_SCHEMA_VERSION\n4. required restoration fields are present\n5. runtime_origin and backend_validation_claimed do not conflict with floor invariants\n6. legacy migration state is resolved or visibly blocked'''
    new='''A v2 handoff card is valid for restoration only when:\n1. it parses as strict JSON with exactly one top-level root key, AIR_HANDOFF_CARD\n2. AIR_HANDOFF_CARD.template_designation = AIR_HANDOFF_CARD_TEMPLATE_V2\n3. AIR_HANDOFF_CARD.schema_version = Core CANONICAL_HANDOFF_SCHEMA_VERSION\n4. source card revision is identified and any declared revision migration completes before current-revision required-carrier validation\n5. required restoration fields are present after any applicable migration\n6. runtime_origin and backend_validation_claimed do not conflict with floor invariants\n7. legacy migration state is resolved or visibly blocked'''
    t=replace_once(t,old,new,'core inbound order')
    old='''Schema 2.1 migration boundary:\n- A schema 2.1.0 card may be accepted only as `MIGRATION_INPUT_PENDING_REVIEW`, not as directly restorable current state.'''
    new='''Rev15 to rev16 migration boundary:\n- A schema-2.3.0 card with card_revision = 15 is valid migration input to rev16 and must enter the declared rev15-to-rev16 migration before rev16-only required-carrier validation.\n- Rev15 did not serialize failure_mode_state or surfaced_object_ledger_state. Migration must create typed `LEGACY_UNRECORDED_PRE_REV16` carriers; an empty migrated list never means the pre-rev16 history was observed or complete.\n- Migrated rev15 surfaced-object history begins a new current-session ledger boundary at HANDOFF_RESTORE. No pre-rev16 ledger identity, failure record, authorization, receipt, approval, or visibility provenance may be fabricated.\n- Rev15 object_visibility_mode = ALL_OBJECTS may map to the immutable default authority. A rev15 MINIMUM_REQUIRED_OBJECTS value without explicit authority provenance remains historical requested state only and restores clamped to ALL_OBJECTS pending explicit re-selection.\n- Rev15 has no canonical weaker-profile acceptance carrier. Migration therefore records posture history as LEGACY_UNRECORDED_PRE_REV16 and clamps current posture to the Default Starter baseline until explicit current evidence establishes an accepted weaker delta.\n- Active rev15 Method Pack state without a current typed method-specific schema reference routes to REVIEW; do not infer a method-specific mapping from prose.\n\nSchema 2.1 migration boundary:\n- A schema 2.1.0 card may be accepted only as `MIGRATION_INPUT_PENDING_REVIEW`, not as directly restorable current state.'''
    t=replace_once(t,old,new,'core rev15 migration')
    old='''- object_visibility_mode\n- test_evidence_state'''
    new='''- object_visibility_mode\n- object_visibility_authority_state\n- profile_posture_acceptance_state\n- test_evidence_state'''
    t=replace_once(t,old,new,'core required carriers')
    old='''AIR_SESSION allowed object-owned top-level fields:\n- session_runtime_frame\n- contract_activation\n- orbit_state\n- task_binding\n- compiler_contract\n- artifact_presence\n- object_visibility_mode\n- load_integrity'''
    new='''AIR_SESSION allowed object-owned top-level fields:\n- session_runtime_frame\n- contract_activation\n- orbit_state\n- task_binding\n- compiler_contract\n- artifact_presence\n- object_visibility_mode\n- object_visibility_authority_state\n- profile_posture_acceptance_state\n- load_integrity'''
    t=replace_once(t,old,new,'core session allowed fields')
    old='''explicitly accepts the weaker posture, which is then recorded in\nAIR_SESSION and every subsequent handoff card.'''
    new='''explicitly accepts the weaker posture, which is then recorded in\nAIR_SESSION and every subsequent handoff card.\n\nCanonical profile_posture_acceptance_state is the single continuity carrier for that acceptance. It contains baseline_profile_ref, accepted_weaker_postures, history_state, restoration_state, and positive_execution_authority = NONE. Each accepted_weaker_postures record contains acceptance_id, profile_ref, profile_version when known, weaker_delta_ids, acceptance_source = USER_EXPLICIT, user_acceptance_evidence_ref, scope, and lifecycle_state. A restored record remains non-authorizing continuation input until the profile identity, exact delta, acceptance evidence, scope, and current task fit are revalidated. Missing or legacy-unrecorded acceptance clamps to the Default Starter baseline; AIR must not infer acceptance.'''
    t=replace_once(t,old,new,'core weaker posture carrier')
    old='''ALL_OBJECTS is the immutable default selection rule. MINIMUM_REQUIRED_OBJECTS may become active only from an explicit user command/selection or restoration of that explicit selection from a valid Handoff Card. AIR must not infer, optimize, compress, or silently switch into minimum mode. There is no full object-off mode. Display settings do not create objects solely for display and do not change scope, evidence, approval, or execution state.'''
    new='''ALL_OBJECTS is the immutable default selection rule. MINIMUM_REQUIRED_OBJECTS may become active only from an explicit user command/selection or restoration of that explicit selection from a valid Handoff Card. AIR must not infer, optimize, compress, or silently switch into minimum mode. There is no full object-off mode. Display settings do not create objects solely for display and do not change scope, evidence, approval, or execution state.\n\nCanonical object_visibility_authority_state records the authority for the current object_visibility_mode. Required fields are visibility_mode_ref, authority_source, selection_evidence_ref, source_handoff_ref, restoration_state, and positive_execution_authority = NONE. Allowed authority_source values are IMMUTABLE_DEFAULT_BASELINE, USER_EXPLICIT, RESTORED_EXPLICIT_SELECTION, and LEGACY_UNVERIFIED_SELECTION. MINIMUM_REQUIRED_OBJECTS is restorable only with USER_EXPLICIT or RESTORED_EXPLICIT_SELECTION plus a non-null selection_evidence_ref; LEGACY_UNVERIFIED_SELECTION is historical input only and clamps current visibility to ALL_OBJECTS pending explicit re-selection.'''
    t=replace_once(t,old,new,'core visibility authority')
    old='''- evidence_refs\n- method_specific_state\n\n`method_specific_state` contains only method-defined continuation state'''
    new='''- evidence_refs\n- method_specific_state_schema_ref when method_origin = METHOD_PACK\n- method_specific_state_schema_version when method_origin = METHOD_PACK\n- method_specific_state\n\nFor METHOD_PACK origin, method_specific_state_schema_ref must exactly equal the active Method Pack's declared handoff_requirements.method_specific_state_schema.schema_id and the serialized state must validate against that typed schema. A prose-only requirement list is not sufficient for restoration. INLINE methods may leave the schema reference null when no separate typed method-specific contract exists.\n\n`method_specific_state` contains only method-defined continuation state'''
    t=replace_once(t,old,new,'core method schema ref')
    old='''A second full mutable copy is prohibited even when the values currently match. A non-owner copy cannot authorize execution, override its owner, repair staleness, or become current merely because it is newer in the conversation.'''
    new='''A second full mutable copy is prohibited even when the values currently match. A non-owner copy cannot authorize execution, override its owner, repair staleness, or become current merely because it is newer in the conversation.\n\nGovernance-controlled source-rights records have one canonical owner: the Governance `governance_source_rights_state` record set keyed by source_rights_id. AIR_ARTIFACT.source_rights_state and AIR_HANDOFF_CARD.source_state.source_rights_state may carry only DERIVED_NONAUTHORITATIVE projections or references for those Governance-owned records. Every such projection must carry source_rights_id, governance_record_ref, authoritative = false, and projected_rights_state; it may not copy a second mutable permission record. Conflict, missing canonical reference, or disagreement between a projection and its Governance owner routes to REVIEW and cannot be resolved by last-writer-wins or consumer preference.'''
    t=replace_once(t,old,new,'core source rights owner')
    p.write_text(t,encoding='utf-8')

def patch_control():
    rel='prompts/AIR_CONTROL_SURFACE.md'
    block='''Patch marker: AIR_CONTROL_HANDOFF_R3_RESTORATION_RENDERER_V1\n\nHandoff restoration rendering rules for rev16:\n- validate any declared revision migration before reporting current-revision carrier completeness;\n- treat migrated rev15 failure/ledger history as LEGACY_UNRECORDED_PRE_REV16, never as empty-complete history;\n- restore MINIMUM_REQUIRED_OBJECTS only when object_visibility_authority_state proves explicit authority; otherwise render ALL_OBJECTS and the review reason;\n- never present restored weaker-profile posture as accepted without a valid profile_posture_acceptance_state record;\n- do not render an approval scope as actionable until its exact AIR_APPROVE::<approval_scope_id> / AIR_REJECT::<approval_scope_id> pair and canonical response mode have been revalidated;\n- when a Method Pack is active, show REVIEW if its method_specific_state schema reference or required typed state is missing;\n- Governance-owned source-rights state controls any generic source-rights projection; conflicting projections render REVIEW rather than choosing a carrier.'''
    sentinel='AIR_LOAD_SENTINEL :: AIR_CONTROL_SURFACE :: END_OF_FILE :: LOAD_INTEGRITY_V2'
    insert_before_sentinel(rel,block,sentinel)

def patch_gov():
    rel='prompts/AIR_GOV.md'; p=ROOT/rel; t=p.read_text(encoding='utf-8')
    old='''- approval_response_mode\n\nAllowed approval_state values:'''
    new='''- approval_response_mode\n\nAllowed approval_response_mode values:\n- EXACT_CANONICAL_SCOPE_TOKEN_PAIR\n\nFor a material scope, operational_response_tokens is valid only when it is the exact two-element set derived from approval_scope_id: AIR_APPROVE::<approval_scope_id> and AIR_REJECT::<approval_scope_id>, with no substitution, alias, duplicate, or extra token. Restored scopes must re-run this derivation check before Core approval resolution can consume the set.\n\nAllowed approval_state values:'''
    t=replace_once(t,old,new,'gov approval mode')
    old='''Allowed resolution_state values:\n- RESOLVED\n- REVIEW_REQUIRED\n- REJECTED'''
    new='''Allowed resolution_state values:\n- UNRESOLVED\n- RESOLVED\n- REVIEW_REQUIRED\n- REJECTED\n\nUNRESOLVED is a bootstrap/serialization value only. It has no positive authority and must transition to RESOLVED, REVIEW_REQUIRED, or REJECTED before Governance-dependent operative use.'''
    t=replace_once(t,old,new,'gov floor unresolved')
    old='''Governance source-rights state must feed AIR_GATE.evaluation_checks.evidence, AIR_GATE.evaluation_checks.allowed_action, AIR_GATE.evaluation_checks.stop_condition, and AIR_GATE.reason when source use is material.'''
    new='''Governance source-rights state must feed AIR_GATE.evaluation_checks.evidence, AIR_GATE.evaluation_checks.allowed_action, AIR_GATE.evaluation_checks.stop_condition, and AIR_GATE.reason when source use is material.\n\nCanonical ownership and projection:\n- the Governance governance_source_rights_state record set is the canonical mutable owner for Governance-controlled source permissions and restrictions, keyed by source_rights_id;\n- AIR_ARTIFACT.source_rights_state and AIR_HANDOFF_CARD.source_state.source_rights_state are DERIVED_NONAUTHORITATIVE views for Governance-owned records and must reference the canonical governance record by source_rights_id/governance_record_ref;\n- a projection may carry projected_rights_state but cannot independently alter permissions, restrictions, expiry/revocation, evidence, or decision reason;\n- missing canonical reference or any owner/projection disagreement routes to REVIEW and blocks affected use; last-writer-wins and consumer-selected precedence are prohibited.'''
    t=replace_once(t,old,new,'gov source rights projection')
    t=replace_once(t,'4. If semantic equivalence cannot be shown, route to REVIEW_REQUIRED.','4. If semantic equivalence cannot be shown, route through Core AIR_GATE with decision = REVIEW.','gov edition review')
    p.write_text(t,encoding='utf-8')

def patch_starter():
    rel='prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(rel); cc=o['compiler_contract']
    ar=cc['approval_response_resolution']
    ar['approval_response_mode']='EXACT_CANONICAL_SCOPE_TOKEN_PAIR'
    ar['restored_scope_token_derivation_required']=True
    ar['validated_token_state']='VALIDATED_CANONICAL_SCOPE_TOKEN_PAIR'
    ar['token_set_rule']='EXACT_TWO_ELEMENT_SET_DERIVED_FROM_APPROVAL_SCOPE_ID_NO_EXTRAS_OR_ALIASES'
    for e in cc['runtime_control_event_registry']['events']:
        if e['route_id']=='RT.APPROVAL_RESOLVE':
            guards=e['guards']
            if not any(g.get('path')=='OPEN_APPROVAL_SCOPE_TOKEN_VALIDATION_STATE' for g in guards):
                guards.insert(1,{'operator':'STATE_EQUALS','path':'OPEN_APPROVAL_SCOPE_TOKEN_VALIDATION_STATE','expected':'VALIDATED_CANONICAL_SCOPE_TOKEN_PAIR'})
    save(rel,o)

def typed_method_req(method_id, required, optional=None, generic_extra=None):
    generic=[
        '$.execution_state.method_handoff_state.method_identity',
        '$.execution_state.method_handoff_state.method_origin',
        '$.execution_state.method_handoff_state.active_method_state',
        '$.execution_state.method_handoff_state.active_method_step',
        '$.execution_state.method_handoff_state.method_step_gate',
        '$.execution_state.method_handoff_state.method_evidence_state',
        '$.execution_state.method_handoff_state.staleness_state',
        '$.execution_state.method_handoff_state.unresolved_blockers',
        '$.execution_state.method_handoff_state.next_allowed_action',
        '$.execution_state.method_handoff_state.evidence_refs',
        '$.execution_state.method_handoff_state.method_specific_state_schema_ref',
        '$.execution_state.method_handoff_state.method_specific_state_schema_version',
        '$.execution_state.method_handoff_state.method_specific_state',
    ]
    if generic_extra: generic.extend(generic_extra)
    schema_id=re.sub(r'[^A-Z0-9]+','_',method_id.upper()).strip('_')+'_METHOD_SPECIFIC_STATE_V1'
    return {
        'schema_version':'1.0.0',
        'schema_id':re.sub(r'[^A-Z0-9]+','_',method_id.upper()).strip('_')+'_HANDOFF_REQUIREMENTS_V1',
        'generic_required_paths':generic,
        'method_specific_state_schema':{
            'schema_id':schema_id,
            'schema_version':'1.0.0',
            'required_fields':required,
            'optional_fields':optional or [],
            'additional_fields_policy':'REVIEW_UNLESS_DECLARED',
            'positive_execution_authority':'NONE'
        },
        'validation_rule':'GENERIC_PATHS_PRESENT_AND_METHOD_SPECIFIC_STATE_VALIDATES_EXACT_DECLARED_SCHEMA_BEFORE_RESTORE_REUSE',
    }

def patch_method_packs():
    configs={
      'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json':[
        'active_branch','step_state_by_id','step_evidence_refs','component_receipts','selected_capability_refs','deferred_capability_refs','rejected_capability_refs','domain_match_refs','domain_package_refs','knowledge_dimension_state','cognitive_depth_state','knowledge_to_execution_path_ref','representative_task_result_refs','required_input_request_refs','test_evidence_state_ref'],
      'profiles/grounding specialist/AIR_GROUNDING_METHOD_PACK.json':[
        'grounding_need_state','grounding_scope','source_access_mode','source_freshness_state','grounding_decision_state','grounding_component_refs','required_input_request_refs','revalidation_triggers'],
      'profiles/governance specialist/AIR_AI_GOVERNANCE_METHOD_PACK.json':[
        'source_access_mode','jurisdiction_and_role_state','agentic_overlay_state','framework_adapter_state','regulatory_evidence_requirement_state','human_authority_gates','unresolved_required_inputs','staleness_triggers'],
      'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json':[
        'method_selection_state','candidate_comparison_state','review_contribution_state','revalidation_triggers'],
      'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json':[
        'specification_target_refs','task_classification','open_ambiguity_requests','open_assumption_requests','open_evidence_requests','selected_verification_layers','verification_specification_ref_or_snapshot','specification_adequacy_decision','baseline_evidence_state','observed_verification_evidence_refs','integrity_review_state','intent_reconciliation_state'],
    }
    for rel,required in configs.items():
        o=load(rel); old=o.get('handoff_requirements'); req=typed_method_req(o['method_id'],required,optional=['test_evidence_mode'])
        if isinstance(old,dict):
            if old.get('continuation_rule'): req['continuation_rule']=old['continuation_rule']
            if old.get('missing_file_rule'): req['missing_file_rule']=old['missing_file_rule']
        else:
            req['continuation_rule']='Restore only as continuation input; current identity, applicability, evidence, staleness, and Orbit 0 artifact compilation must be revalidated.'
        o['handoff_requirements']=req
        save(rel,o)

def patch_overlay():
    rel='profiles/governance specialist/AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json'; o=load(rel)
    br=o['binding_rules']; vals=br['activation_state_values']
    if 'NOT_EVALUATED' not in vals: vals.insert(0,'NOT_EVALUATED')
    br['pre_evaluation_transition_rule']='NOT_EVALUATED -> NOT_TRIGGERED when trigger evaluation is complete and no trigger applies; NOT_EVALUATED -> TRIGGERED_PENDING_VALIDATION when a declared trigger applies. No other implicit transition is permitted.'
    save(rel,o)

def patch_gov_method_states():
    rel='profiles/governance specialist/AIR_AI_GOVERNANCE_METHOD_PACK.json'; o=load(rel)
    o['method_execution_state_schema']['step_states']=['PENDING','ACTIVE','COMPLETE','BLOCKED','REVIEW','SKIPPED_APPROVED','FAILED','INVALIDATED']
    o['method_execution_state_schema']['staleness_state_location']='METHOD_EXECUTION_LEVEL_NOT_STEP_STATE_ENUM'
    save(rel,o)

def patch_handoff():
    rel='prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; o=load(rel); H=o['AIR_HANDOFF_CARD']; sm=H['schema_manifest']
    H['object_visibility_authority_state']={
      'visibility_mode_ref':'AIR_HANDOFF_CARD.object_visibility_mode',
      'authority_source':'IMMUTABLE_DEFAULT_BASELINE',
      'selection_evidence_ref':None,
      'source_handoff_ref':None,
      'restoration_state':'UNVALIDATED_BOOTSTRAP_INPUT',
      'positive_execution_authority':'NONE'
    }
    H['profile_posture_acceptance_state']={
      'baseline_profile_ref':'AIR_DEFAULT_STARTER_V2',
      'accepted_weaker_postures':[],
      'history_state':'CURRENT_REV16_NO_ACCEPTED_WEAKER_POSTURE_RECORDED',
      'restoration_state':'UNVALIDATED_BOOTSTRAP_INPUT',
      'positive_execution_authority':'NONE'
    }
    def reposition(d,key,after):
        val=d[key]; nd={}
        for k,v in d.items():
            if k==key: continue
            nd[k]=v
            if k==after: nd[key]=val
        return nd
    H=reposition(H,'object_visibility_authority_state','object_visibility_mode')
    H=reposition(H,'profile_posture_acceptance_state','object_visibility_authority_state')
    o['AIR_HANDOFF_CARD']=H; sm=H['schema_manifest']
    req=sm['required_fields']
    for k in ['object_visibility_authority_state','profile_posture_acceptance_state']:
        if k not in req:
            req.insert(req.index('onboarding_state'),k)
    mh=H['execution_state']['method_handoff_state']
    mh.setdefault('method_specific_state_schema_ref',None)
    mh.setdefault('method_specific_state_schema_version',None)
    mh2={}
    for k,v in mh.items():
        if k=='method_specific_state':
            mh2['method_specific_state_schema_ref']=mh['method_specific_state_schema_ref']
            mh2['method_specific_state_schema_version']=mh['method_specific_state_schema_version']
        if k not in ('method_specific_state_schema_ref','method_specific_state_schema_version'):
            mh2[k]=v
    H['execution_state']['method_handoff_state']=mh2
    H['execution_state']['patch_state'].setdefault('patch_activity_state','NOT_ACTIVE')
    H['source_state']['source_rights_projection_contract']={
      'governance_owner_path':'AIR_HANDOFF_CARD.governance_state.governance_source_rights_state',
      'projection_path':'AIR_HANDOFF_CARD.source_state.source_rights_state',
      'projection_authority':'DERIVED_NONAUTHORITATIVE',
      'projection_key':'source_rights_id',
      'required_projection_fields':['source_rights_id','governance_record_ref','authoritative','projected_rights_state'],
      'authoritative_required':False,
      'conflict_behavior':'REVIEW_BLOCK_AFFECTED_USE',
      'last_writer_wins':False,
      'reconciliation_state':'NOT_EVALUATED'
    }
    H['governance_state']['floor_invariant_reference']['resolution_state']='UNRESOLVED'
    ms=H['migration_state']
    ms.setdefault('source_card_revision',None)
    ms.setdefault('revision_migration_path',None)
    ms.setdefault('legacy_history_state',None)
    ms['rules']['v2_3_rev15_to_rev16_root_carriers']='MIGRATE_BEFORE_REV16_REQUIRED_CARRIER_VALIDATION; ADD_FAILURE_AND_SURFACED_LEDGER_CARRIERS_AS_LEGACY_UNRECORDED_PRE_REV16; ADD_VISIBILITY_AUTHORITY_AND_PROFILE_POSTURE_CARRIERS_WITH_NONAUTHORITATIVE_SAFE_DEFAULTS; NEVER_FABRICATE_HISTORY; REQUIRE_CURRENT_HANDOFF_RESTORE_ALIGNMENT_AND_ARTIFACT_REBINDING'
    rules={x['id']:x for x in sm['conditional_rules']}
    preds=sm['condition_registry']['predicates']
    allowed=sm['condition_registry']['allowed_operators']
    for op in ['ANY','PATH_EXISTS','PATH_IN']:
        if op not in allowed: allowed.append(op)
    rules['HC-COND-APPROVAL']['requirements']=[
      'open_approval_scope.approval_scope_id','open_approval_scope.gate_id','open_approval_scope.exact_gate_question','open_approval_scope.requested_action',
      'open_approval_scope.authorized_action_ids','open_approval_scope.excluded_action_ids','open_approval_scope.required_evidence','open_approval_scope.stop_conditions',
      'open_approval_scope.expiry_or_completion_condition','open_approval_scope.approval_state','open_approval_scope.approval_source',
      'open_approval_scope.operational_response_tokens when material','open_approval_scope.approval_response_mode when material']
    rules['HC-COND-APPROVAL']['validation_ref']='AIR_HANDOFF_CARD.schema_manifest.validation_registry.HC-VALIDATE-APPROVAL'
    rules['HC-COND-GOV']['requirements']=['governance_state.'+x for x in ['governance_supplement_designation','governance_supplement_version','prompt_edition','governance_floor_version','floor_invariant_reference','open_approval_scope_ref','active_framework_projections','governance_source_rights_state','token_debug_preference','governance_blockers','governance_evidence_references','restricted_content_excluded']]
    rules['HC-COND-GOV']['validation_ref']='AIR_HANDOFF_CARD.schema_manifest.validation_registry.HC-VALIDATE-GOV'
    rules['HC-COND-SPECIALIST']['validation_ref']='AIR_HANDOFF_CARD.schema_manifest.validation_registry.HC-VALIDATE-SPECIALIST'
    rules['HC-COND-METHOD']['requirements']=[
      'execution_state.method_handoff_state.method_identity or execution_state.method inline identity','execution_state.method_handoff_state.method_origin','execution_state.method_handoff_state.active_method_state','execution_state.method_handoff_state.active_method_step','execution_state.method_handoff_state.method_step_gate','execution_state.method_handoff_state.method_evidence_state','execution_state.method_handoff_state.staleness_state','execution_state.method_handoff_state.unresolved_blockers','execution_state.method_handoff_state.next_allowed_action','execution_state.method_handoff_state.evidence_refs','execution_state.method_handoff_state.method_specific_state_schema_ref and version when METHOD_PACK','execution_state.method_handoff_state.method_specific_state validates active Method Pack typed handoff schema']
    rules['HC-COND-METHOD']['validation_ref']='AIR_HANDOFF_CARD.schema_manifest.validation_registry.HC-VALIDATE-METHOD'
    rules['HC-COND-PATCH']['validation_ref']='AIR_HANDOFF_CARD.schema_manifest.validation_registry.HC-VALIDATE-PATCH'
    rules['HC-COND-ACTION-GOVERNANCE']['validation_ref']='AIR_HANDOFF_CARD.schema_manifest.validation_registry.HC-VALIDATE-ACTION-GOVERNANCE'
    rules['HC-COND-AMRS-STEP-OPTIMALITY-REV15']['validation_ref']='AIR_HANDOFF_CARD.schema_manifest.validation_registry.HC-VALIDATE-AMRS-STEP-OPTIMALITY'
    if 'HC-COND-VISIBILITY-AUTHORITY' not in rules:
      newrule={'id':'HC-COND-VISIBILITY-AUTHORITY','condition':'object visibility mode always has typed authority provenance','requirements':['object_visibility_authority_state'],'failure_behavior':'REVIEW_AND_CLAMP_TO_ALL_OBJECTS','condition_authority':'NON_OPERATIVE_DESCRIPTION','predicate_ref':'AIR_HANDOFF_CARD.schema_manifest.condition_registry.HC-COND-VISIBILITY-AUTHORITY','validation_ref':'AIR_HANDOFF_CARD.schema_manifest.validation_registry.HC-VALIDATE-VISIBILITY-AUTHORITY'}
      sm['conditional_rules'].append(newrule); rules[newrule['id']]=newrule
    if 'HC-COND-PROFILE-POSTURE' not in rules:
      newrule={'id':'HC-COND-PROFILE-POSTURE','condition':'a weaker profile posture acceptance is serialized','requirements':['profile_posture_acceptance_state.accepted_weaker_postures'],'failure_behavior':'REVIEW_AND_CLAMP_TO_DEFAULT_STARTER_BASELINE','condition_authority':'NON_OPERATIVE_DESCRIPTION','predicate_ref':'AIR_HANDOFF_CARD.schema_manifest.condition_registry.HC-COND-PROFILE-POSTURE','validation_ref':'AIR_HANDOFF_CARD.schema_manifest.validation_registry.HC-VALIDATE-PROFILE-POSTURE'}
      sm['conditional_rules'].append(newrule); rules[newrule['id']]=newrule
    if 'HC-COND-SOURCE-RIGHTS-PROJECTION' not in rules:
      newrule={'id':'HC-COND-SOURCE-RIGHTS-PROJECTION','condition':'governance or generic source-rights state is serialized','requirements':['governance_state.governance_source_rights_state','source_state.source_rights_state','source_state.source_rights_projection_contract'],'failure_behavior':'REVIEW_BLOCK_AFFECTED_USE','condition_authority':'NON_OPERATIVE_DESCRIPTION','predicate_ref':'AIR_HANDOFF_CARD.schema_manifest.condition_registry.HC-COND-SOURCE-RIGHTS-PROJECTION','validation_ref':'AIR_HANDOFF_CARD.schema_manifest.validation_registry.HC-VALIDATE-SOURCE-RIGHTS-PROJECTION'}
      sm['conditional_rules'].append(newrule); rules[newrule['id']]=newrule
    preds['HC-COND-SPECIALIST']={'operator':'ANY','predicates':[
      {'operator':'PATH_NOT_NULL','path':'$.specialist_binding_state.active_specialist'},
      *[{'operator':'PATH_NONEMPTY','path':p} for p in ['$.specialist_binding_state.supporting_specialists','$.specialist_binding_state.available_specialists','$.specialist_binding_state.recommended_specialists','$.specialist_binding_state.generated_pending_validation','$.profile_stack.supporting_profile_refs','$.profile_stack.domain_overlay_refs','$.profile_stack.source_pack_refs','$.profile_stack.method_pack_refs','$.profile_stack.executor_refs']],
      {'operator':'PATH_NOT_NULL','path':'$.profile_stack.active_specialist_profile_ref'}]}
    preds['HC-COND-METHOD']={'operator':'ANY','predicates':[
      {'operator':'PATH_NOT_NULL','path':'$.execution_state.method'},
      {'operator':'PATH_NOT_NULL','path':'$.execution_state.method_handoff_state.method_identity'},
      {'operator':'PATH_NOT_NULL','path':'$.execution_state.method_handoff_state.active_method_state'},
      {'operator':'PATH_NOT_NULL','path':'$.execution_state.method_handoff_state.active_method_step'}]}
    preds['HC-COND-PATCH']={'operator':'ANY','predicates':[
      {'operator':'PATH_EQUALS','path':'$.execution_state.patch_state.patch_activity_state','expected':'ACTIVE_FILE_MUTATION_OR_PATCH'},
      {'operator':'PATH_NONEMPTY','path':'$.execution_state.patch_state.source_inventory'},
      {'operator':'PATH_NONEMPTY','path':'$.execution_state.patch_state.mutation_scope'}]}
    preds['HC-COND-ACTION-GOVERNANCE']={'operator':'ANY','predicates':[
      *[{'operator':'PATH_NONEMPTY','path':p} for p in ['$.action_governance_state.resource_scope_pins','$.action_governance_state.historical_action_authorizations','$.action_governance_state.open_authorizations','$.action_governance_state.action_receipts','$.action_governance_state.unbound_prior_effects']],
      {'operator':'PATH_NOT_NULL','path':'$.active_artifact.resource_scope_pin'},
      {'operator':'PATH_NOT_NULL','path':'$.active_artifact.action_governance_state'},
      {'operator':'PATH_NOT_NULL','path':'$.active_artifact.artifact_lease.lease_state_before_handoff'}]}
    preds['HC-COND-AMRS-STEP-OPTIMALITY-REV15']={'operator':'ALL','predicates':[
      {'operator':'PATH_GTE','path':'$.card_revision','expected':15},
      {'operator':'ANY','predicates':[
        {'operator':'PATH_EQUALS','path':'$.execution_state.knowledge_to_execution_path_state.path_validation_state','expected':'COMPLETE_FOR_ACTIVE_STEP'},
        {'operator':'PATH_EQUALS','path':'$.execution_state.readiness_state.completion_readiness_state','expected':'TARGET_SATISFIED'}]}]}
    preds['HC-COND-VISIBILITY-AUTHORITY']={'operator':'CONST_TRUE'}
    preds['HC-COND-PROFILE-POSTURE']={'operator':'PATH_NONEMPTY','path':'$.profile_posture_acceptance_state.accepted_weaker_postures'}
    preds['HC-COND-SOURCE-RIGHTS-PROJECTION']={'operator':'ANY','predicates':[
      {'operator':'PATH_NONEMPTY','path':'$.governance_state.governance_source_rights_state'},
      {'operator':'PATH_NONEMPTY','path':'$.source_state.source_rights_state'}]}
    gov_fields=['governance_supplement_designation','governance_supplement_version','prompt_edition','governance_floor_version','floor_invariant_reference','open_approval_scope_ref','active_framework_projections','governance_source_rights_state','token_debug_preference','governance_blockers','governance_evidence_references','restricted_content_excluded']
    sm['validation_registry']={
      'registry_version':'1.0.0','authority_class':'RUNTIME_OPERATIVE_TYPED_CONTRACT','unknown_operator_behavior':'FAIL_CLOSED',
      'allowed_operators':['ALL','PATH_EXISTS','PATH_EQUALS','PATH_IN','APPROVAL_SCOPE_CANONICAL_TOKEN_PAIR','OBJECT_VISIBILITY_AUTHORITY_VALID','PROFILE_POSTURE_ACCEPTANCE_VALID','ACTIVE_METHOD_PACK_HANDOFF_SCHEMA_VALID','SOURCE_RIGHTS_PROJECTION_CONSISTENT','PATCH_ACTIVITY_REQUIREMENTS_VALID','AMRS_STEP_OPTIMALITY_COMPLETION_VALID'],
      'operator_semantics':{
        'APPROVAL_SCOPE_CANONICAL_TOKEN_PAIR':'For non-null material open scope, require approval_response_mode=EXACT_CANONICAL_SCOPE_TOKEN_PAIR and operational_response_tokens set equality with exactly AIR_APPROVE::<approval_scope_id> and AIR_REJECT::<approval_scope_id>. Produce OPEN_APPROVAL_SCOPE_TOKEN_VALIDATION_STATE=VALIDATED_CANONICAL_SCOPE_TOKEN_PAIR only on success.',
        'OBJECT_VISIBILITY_AUTHORITY_VALID':'visibility_mode_ref must name AIR_HANDOFF_CARD.object_visibility_mode. MINIMUM_REQUIRED_OBJECTS requires USER_EXPLICIT or RESTORED_EXPLICIT_SELECTION and non-null selection_evidence_ref; LEGACY_UNVERIFIED_SELECTION cannot restore minimum and clamps to ALL_OBJECTS.',
        'PROFILE_POSTURE_ACCEPTANCE_VALID':'Each accepted weaker posture requires exact profile/delta identity, USER_EXPLICIT acceptance evidence, scope and lifecycle. Missing, legacy-unrecorded, or conflicting acceptance clamps to Default Starter baseline.',
        'ACTIVE_METHOD_PACK_HANDOFF_SCHEMA_VALID':'If method_origin=METHOD_PACK, schema ref/version must exactly match the active Method Pack handoff_requirements.method_specific_state_schema and method_specific_state must satisfy required fields. Missing schema or field routes REVIEW without reconstruction.',
        'SOURCE_RIGHTS_PROJECTION_CONSISTENT':'Governance-owned source_rights_id is canonical. Generic projections must reference that owner, set authoritative=false, and match projected_rights_state; conflicts route REVIEW.',
        'PATCH_ACTIVITY_REQUIREMENTS_VALID':'ACTIVE_FILE_MUTATION_OR_PATCH requires nonempty source_inventory, replacement_policy, mutation_scope, validation_plan and last_validation_state carrier.',
        'AMRS_STEP_OPTIMALITY_COMPLETION_VALID':'When the completion trigger is true, path_validation_state must be COMPLETE_FOR_ACTIVE_STEP and step_optimality_state must be PASS with preserved basis/stopping evidence as applicable.'},
      'rules':{
        'HC-VALIDATE-APPROVAL':{'operator':'ALL','predicates':[{'operator':'PATH_EXISTS','path':'$.open_approval_scope.'+f} for f in ['approval_scope_id','gate_id','exact_gate_question','requested_action','authorized_action_ids','excluded_action_ids','required_evidence','stop_conditions','expiry_or_completion_condition','approval_state','approval_source','operational_response_tokens','approval_response_mode']]+[{'operator':'APPROVAL_SCOPE_CANONICAL_TOKEN_PAIR','path':'$.open_approval_scope'}]},
        'HC-VALIDATE-GOV':{'operator':'ALL','predicates':[{'operator':'PATH_EXISTS','path':'$.governance_state.'+f} for f in gov_fields]+[{'operator':'PATH_IN','path':'$.governance_state.floor_invariant_reference.resolution_state','values':['UNRESOLVED','RESOLVED','REVIEW_REQUIRED','REJECTED']}]},
        'HC-VALIDATE-SPECIALIST':{'operator':'ALL','predicates':[{'operator':'PATH_EXISTS','path':'$.specialist_binding_state.active_specialist'},{'operator':'PATH_EXISTS','path':'$.specialist_binding_state.restoration_state'}]},
        'HC-VALIDATE-METHOD':{'operator':'ACTIVE_METHOD_PACK_HANDOFF_SCHEMA_VALID','path':'$.execution_state.method_handoff_state'},
        'HC-VALIDATE-PATCH':{'operator':'PATCH_ACTIVITY_REQUIREMENTS_VALID','path':'$.execution_state.patch_state'},
        'HC-VALIDATE-ACTION-GOVERNANCE':{'operator':'ALL','predicates':[{'operator':'PATH_EXISTS','path':'$.action_governance_state.open_authorizations'},{'operator':'PATH_EXISTS','path':'$.action_governance_state.authorization_restoration_rule'}]},
        'HC-VALIDATE-AMRS-STEP-OPTIMALITY':{'operator':'AMRS_STEP_OPTIMALITY_COMPLETION_VALID','path':'$.execution_state'},
        'HC-VALIDATE-VISIBILITY-AUTHORITY':{'operator':'OBJECT_VISIBILITY_AUTHORITY_VALID','path':'$.object_visibility_authority_state'},
        'HC-VALIDATE-PROFILE-POSTURE':{'operator':'PROFILE_POSTURE_ACCEPTANCE_VALID','path':'$.profile_posture_acceptance_state'},
        'HC-VALIDATE-SOURCE-RIGHTS-PROJECTION':{'operator':'SOURCE_RIGHTS_PROJECTION_CONSISTENT','path':'$.source_state.source_rights_state'}
      }
    }
    legacy_failure={**H['failure_mode_state']}
    legacy_failure['state']='LEGACY_UNRECORDED_PRE_REV16'; legacy_failure['records']=[]; legacy_failure['history_completeness_state']='LEGACY_UNRECORDED_PRE_REV16'; legacy_failure['legacy_source_card_revision']=15
    legacy_ledger={**H['surfaced_object_ledger_state']}
    legacy_ledger['state']='LEGACY_UNRECORDED_PRE_REV16'; legacy_ledger['entries']=[]; legacy_ledger['completeness_state']='LEGACY_UNRECORDED_PRE_REV16'; legacy_ledger['history_origin']='LEGACY_UNRECORDED_PRE_REV16'; legacy_ledger['capture_cutoff']={**legacy_ledger['capture_cutoff'],'last_included_message_count':None,'last_included_state_epoch':None,'last_included_ledger_id':None,'last_included_ledger_hash':None,'freeze_point':'HANDOFF_RESTORE_BOUNDARY_FROM_REV15_NO_PRE_REV16_LEDGER'}
    sm['revision_migration_contracts']={
      'REV15_TO_REV16':{
        'source_schema_version':'2.3.0','source_card_revision':15,'target_schema_version':'2.3.0','target_card_revision':16,
        'apply_before_current_required_carrier_check':True,
        'missing_pre_rev16_history_semantics':'LEGACY_UNRECORDED_PRE_REV16_NOT_EMPTY_COMPLETE',
        'allowed_added_root_carriers':['failure_mode_state','surfaced_object_ledger_state','object_visibility_authority_state','profile_posture_acceptance_state'],
        'failure_mode_state_template':legacy_failure,
        'surfaced_object_ledger_state_template':legacy_ledger,
        'all_objects_visibility_authority_template':H['object_visibility_authority_state'],
        'minimum_visibility_legacy_behavior':'PRESERVE_REQUESTED_VALUE_AS_HISTORY_BUT_CLAMP_CURRENT_SESSION_TO_ALL_OBJECTS_PENDING_EXPLICIT_RESELECTION',
        'profile_posture_legacy_behavior':'HISTORY_LEGACY_UNRECORDED_PRE_REV16_CLAMP_TO_DEFAULT_STARTER_BASELINE',
        'method_pack_legacy_behavior':'ACTIVE_METHOD_PACK_WITHOUT_TYPED_SCHEMA_REF_ROUTES_REVIEW_NO_PROSE_INFERENCE',
        'history_synthesis':'PROHIBITED','positive_execution_authority':'NONE','post_migration_requirements':['CURRENT_HANDOFF_RESTORE_ALIGNMENT','ARTIFACT_PRECHECK','ARTIFACT_REBINDING']
      }
    }
    seq=sm['validation_sequence']
    seq=[x for x in seq if x not in ('required-carrier check','legacy migration check','source card revision detection and applicable revision migration check','required-carrier check after applicable migration')]
    insert_at=4
    seq[insert_at:insert_at]=['source card revision detection and applicable revision migration check','legacy migration check','required-carrier check after applicable migration']
    sm['validation_sequence']=seq
    sc=sm['schema_compatibility_contract']; sc['revision_migration_before_required_carrier_validation']=True; sc['rev15_to_rev16_migration_contract_ref']='AIR_HANDOFF_CARD.schema_manifest.revision_migration_contracts.REV15_TO_REV16'
    H['failure_mode_state'].setdefault('history_completeness_state','CURRENT_REV16_GENERATED_HISTORY_REQUIRED')
    H['surfaced_object_ledger_state'].setdefault('history_origin','REV16_NATIVE')
    save(rel,o)

def patch_route_map():
    rel='catalog/AIR_RUNTIME_ROUTE_MAP.json'; o=load(rel); core=(ROOT/'prompts/AIR_CORE_RUNTIME.md').read_text(encoding='utf-8')
    o['source_of_truth']['sha256']=hashlib.sha256(core.encode('utf-8')).hexdigest()
    lines=core.splitlines(); line_by={ln.split('=',1)[1]:i for i,ln in enumerate(lines,1) if ln.startswith('id=RT.')}
    for r in o['routes']:
        if r['route_id'] in line_by: r['source_anchor']['line']=line_by[r['route_id']]
    save(rel,o)

def main():
    patch_core(); patch_control(); patch_gov(); patch_starter(); patch_overlay(); patch_method_packs(); patch_gov_method_states(); patch_handoff(); patch_route_map()

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('root',nargs='?',default='.'); a=ap.parse_args(); ROOT=Path(a.root).resolve(); main()
    print('R3 source patch applied or already present')
