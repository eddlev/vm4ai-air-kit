from __future__ import annotations
import json, sys
from pathlib import Path

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()

def load(rel):
    return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def save(rel,obj):
    (ROOT/rel).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')
def replace_once(text,old,new,label):
    if new in text:
        return text
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected one anchor, found {n}')
    return text.replace(old,new,1)

REG='profiles/capability ecology architect/AIR_DOMAIN_CAPABILITY_REGISTRY.json'
TR='profiles/capability ecology architect/AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json'
ARCH='profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT.json'
MP='profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json'
CORE='prompts/AIR_CORE_RUNTIME.md'
STARTER='prompts/AIR_DEFAULT_STARTER_PROFILE.json'
HANDOFF='prompts/AIR_HANDOFF_CARD_TEMPLATE.json'

reg=load(REG)
canonical=list(reg['detailed_domain_package_template']['required_fields'])
if len(canonical)!=44:
    raise SystemExit(f'canonical Domain Package field count expected 44, got {len(canonical)}')
reg['registry_schema']['required_domain_package_fields']=canonical
reg['registry_schema']['fixture_wrapper_required_fields']=['fixture_id','fixture_role','runtime_authority','runtime_match_allowed']
reg['registry_schema']['fixture_wrapper_result_field_contract']={
    'discriminator_field':'fixture_role',
    'cases':{
        'GOLDEN_DOMAIN_CONSTRUCTION_FIXTURE':{'required_result_field':'expected_validation','forbidden_result_fields':['expected_decision']},
        'NEGATIVE_DOMAIN_CONSTRUCTION_FIXTURE':{'required_result_field':'expected_decision','forbidden_result_fields':['expected_validation']}
    },
    'unknown_fixture_role_behavior':'REJECT',
    'literal_pseudo_field_tokens_forbidden':True
}
reg['registry_schema']['fixture_mutation_path_contract']={
    'path_root':'candidate_domain_package',
    'json_member_case':'EXACT_CASE_SENSITIVE',
    'remove_or_replace_precondition':'TARGET_PATH_MUST_RESOLVE_EXACTLY',
    'add_precondition':'PARENT_PATH_MUST_RESOLVE_EXACTLY_AND_TARGET_KEY_MUST_BE_ABSENT',
    'bracket_list_removal_semantics':'key[A,B] means the exact list-valued key must exist and contain each named list item',
    'unresolved_path_behavior':'FIXTURE_INVALID_BEFORE_DEFECT_EVALUATION'
}
extra_defaults={
    'test_evidence_and_reproducibility_requirements':{'required_evidence_classes':['REPLAYABLE_EVALUATION'],'presentation_mode':'STANDARD_EVIDENCE_PRESENTATION','expanded_presentation_command':'air -t on','regulatory_evidence_required':False},
    'mii_cognitive_route_requirements':{'required_routes':['COG.KNOWLEDGE_TO_EXECUTION'],'recommended_routes':[],'selection_owner':'RT.COGNITIVE_RESOLVE'},
    'mii_contribution_contract':{'target':'AIR_ARTIFACT.execution_benchmark_profile','authority':'CANDIDATE_ONLY','validation_required':True},
    'semantic_fidelity_requirements':{'preserve_source_semantics':True,'unsupported_semantic_inference':'REVIEW'},
    'epistemic_sufficiency_requirements':{'source_and_claim_sufficiency_required':True,'insufficient_state':'EVIDENCE_REQUIRED'},
    'morphology_recommendations':{'state':'NOT_MATERIAL_UNLESS_TASK_REQUIRES','authority':'RECOMMENDATION_ONLY'},
    'risk_propagation_requirements':{'state':'TASK_DEPENDENT','required_when':'MATERIAL_DOWNSTREAM_RISK'},
    'test_evidence_presentation_requirements':{'default_mode':'STANDARD_EVIDENCE_PRESENTATION','expanded_mode_command':'air -t on','presentation_only':True}
}
reg['detailed_domain_package_template']['golden_fixture_required_field_defaults']=extra_defaults
for fx in reg['detailed_domain_fixture_suite']['golden_fixtures']:
    cand=fx['candidate_domain_package']
    for k,v in extra_defaults.items(): cand.setdefault(k,v)
for fx in reg['detailed_domain_fixture_suite']['negative_fixtures']:
    for mut in fx.get('negative_mutations',[]):
        if mut.get('path')=='knowledge_dimensions.procedural': mut['path']='knowledge_dimensions.PROCEDURAL'
save(REG,reg)

tr=load(TR)
required=list(tr['machine_native_translation_contract']['required_translation_outputs'])
fields=tr['output_artifact']['required_fields']
for k in required:
    if k not in fields: fields.append(k)
tr['output_artifact']['required_translation_output_projection']={k:{'path':f'$.{k}','required':True,'projection':'DIRECT_TOP_LEVEL_FIELD'} for k in required}
save(TR,tr)

arch=load(ARCH)
cc=arch['detailed_domain_package_construction_contract']
cc['required_template_fields']=canonical
cc['required_template_fields_source']='AIR_DOMAIN_CAPABILITY_REGISTRY_V2.detailed_domain_package_template.required_fields'
translator_outputs=tr['detailed_domain_package_contribution_contract']['required_outputs']
map_spec={
 'knowledge_required':('$.knowledge_dimensions.FACTUAL.translator_contribution','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'conceptual_relations_required':('$.knowledge_dimensions.CONCEPTUAL.translator_contribution','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'procedures_required':('$.knowledge_dimensions.PROCEDURAL.translator_contribution','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'recognition_and_pattern_capabilities':('$.cognitive_depth_profile.machine_native_capabilities.recognition_and_pattern','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'analysis_capabilities':('$.cognitive_depth_profile.machine_native_capabilities.analysis','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'evaluation_capabilities':('$.cognitive_depth_profile.machine_native_capabilities.evaluation','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'adaptation_capabilities':('$.cognitive_depth_profile.machine_native_capabilities.adaptation','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'creation_or_synthesis_capabilities':('$.cognitive_depth_profile.machine_native_capabilities.creation_or_synthesis','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'experience_derived_candidates':('$.experience_derived_knowledge_requirements.translator_candidates','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'human_bound_elements':('$.human_boundaries_and_non_transferable_authority.human_bound_elements','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'authority_non_transferable':('$.human_boundaries_and_non_transferable_authority.authority_non_transferable','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'evidence_required':('$.epistemic_requirements.translator_evidence_required','MERGE_OR_CREATE_DECLARED_SUBFIELD'),
 'representative_tests':('$.representative_task_tests','MERGE_UNIQUE'),
 'test_evidence_and_reproducibility_requirements':('$.test_evidence_and_reproducibility_requirements','MERGE_OBJECT'),
 'required_test_evidence_classes':('$.test_evidence_and_reproducibility_requirements.required_test_evidence_classes','MERGE_UNIQUE'),
 'regulatory_evidence_obligation_candidates':('$.test_evidence_and_reproducibility_requirements.regulatory_evidence_obligation_candidates','MERGE_UNIQUE'),
 'mii_cognitive_route_requirements':('$.mii_cognitive_route_requirements','MERGE_OBJECT'),
 'mii_contribution_contract':('$.mii_contribution_contract','MERGE_OBJECT'),
 'semantic_fidelity_requirements':('$.semantic_fidelity_requirements','MERGE_OBJECT'),
 'epistemic_sufficiency_requirements':('$.epistemic_sufficiency_requirements','MERGE_OBJECT'),
 'morphology_recommendations':('$.morphology_recommendations','MERGE_OBJECT'),
 'risk_propagation_requirements':('$.risk_propagation_requirements','MERGE_OBJECT'),
 'test_evidence_presentation_requirements':('$.test_evidence_presentation_requirements','MERGE_OBJECT'),
 'uncertainty_resolution_requirements':('$.epistemic_sufficiency_requirements.uncertainty_resolution_requirements','MERGE_OR_CREATE_DECLARED_SUBFIELD')
}
if set(map_spec)!=set(translator_outputs): raise SystemExit('translator mapping coverage mismatch')
cc['translator_to_canonical_package_mapping']={'mapping_version':'1.0.0','source_contract':'AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR_V2.detailed_domain_package_contribution_contract.required_outputs','target_contract':'AIR_DOMAIN_CAPABILITY_REGISTRY_V2.detailed_domain_package_template.required_fields','unknown_source_field_behavior':'REVIEW','unmapped_required_output_behavior':'REJECT_CONSTRUCTION_AS_INCOMPLETE','mappings':{k:{'target_path':v[0],'operation':v[1]} for k,v in map_spec.items()}}
save(ARCH,arch)

mp=load(MP)
for b in mp['branch_contracts'].values():
    for key in ('required_steps','optional_steps'):
        if key in b: b[key]=['M4' if x=='M4_WHEN_TRIGGERED' else x for x in b[key]]
mp['method_execution_contract']['completion_rule']='A method step cannot become COMPLETE without its declared evidence_to_advance unless an exact matching AIR_METHOD_EVIDENCE_WAIVER is recorded, permitted, current for this method/step/requirement, and referenced by step_evidence_waiver_refs. Free text, generic approval, or reconstructed state never satisfies the exception. The whole method cannot become COMPLETE while a required branch step is BLOCKED, REVIEW, FAILED, INVALIDATED or stale.'
mp['evidence_waiver_contract']={'formal_object':'AIR_METHOD_EVIDENCE_WAIVER','waiver_scope':'METHOD_STEP_EVIDENCE_TO_ADVANCE_ONLY','allowed_permission_basis_types':['EXPLICIT_USER_APPROVAL'],'method_policy_waiver_enabled':False,'required_match_fields':['method_identity','method_version','step_id','waived_requirement','artifact_scope_ref'],'accepted_validity_states':['ACTIVE_CURRENT','APPLIED_RECORDED'],'completion_rule':'A COMPLETE step with missing evidence_to_advance must have exactly one matching current or applied AIR_METHOD_EVIDENCE_WAIVER reference for the missing requirement. Revoked, expired, mismatched, free-text, or unresolved refs fail the completion predicate.','handoff_persistence_path':'$.execution_state.method_handoff_state.method_specific_state.step_evidence_waiver_refs','positive_execution_authority':'NONE'}
ms=mp['handoff_requirements']['method_specific_state_schema']
if 'step_evidence_waiver_refs' not in ms['required_fields']:
    ms['required_fields'].insert(ms['required_fields'].index('step_evidence_refs')+1,'step_evidence_waiver_refs')
for step in mp.get('ordered_steps',[]):
    if step.get('step_id')=='M12' and isinstance(step.get('evidence_to_advance'),list):
        step['evidence_to_advance']=[('no step is closed without evidence or exact matching AIR_METHOD_EVIDENCE_WAIVER' if x=='no step is closed without evidence or permitted waiver' else x) for x in step['evidence_to_advance']]
save(MP,mp)

cp=ROOT/CORE
core=cp.read_text(encoding='utf-8')
core=replace_once(core,'- AIR_FAILURE_MODE_RECORD: FAILURE_MODE_RECORD\n- AIR_PRIOR_EFFECT_RECORD: RECOVERY_RECORD','- AIR_FAILURE_MODE_RECORD: FAILURE_MODE_RECORD\n- AIR_METHOD_EVIDENCE_WAIVER: METHOD_EVIDENCE_WAIVER_RECORD\n- AIR_PRIOR_EFFECT_RECORD: RECOVERY_RECORD','core class list')
core=replace_once(core,'- AIR_FAILURE_MODE_RECORD owns one evidenced reusable failure mode, exact applicability signature/hash, corrective constraint, retest lifecycle, and recurrence state; it never supplies positive execution authority.\n- AIR_PRIOR_EFFECT_RECORD owns recovery facts','- AIR_FAILURE_MODE_RECORD owns one evidenced reusable failure mode, exact applicability signature/hash, corrective constraint, retest lifecycle, and recurrence state; it never supplies positive execution authority.\n- AIR_METHOD_EVIDENCE_WAIVER owns one narrow exception to one Method step evidence_to_advance requirement. It never supplies action execution, Gate, approval, binding, or Orbit 0 authority. A waiver is permitted only when its typed scope/method/version/step/requirement/artifact match is exact, its permission basis resolves under the active Method Pack waiver contract, and validity_state is ACTIVE_CURRENT or APPLIED_RECORDED.\n- AIR_PRIOR_EFFECT_RECORD owns recovery facts','core responsibility')
anchor='''AIR_FAILURE_MODE_RECORD allowed object-owned top-level fields:\n- failure_mode_id\n- originating_task_ref\n- originating_attempt_id\n- failure_class\n- failed_step_or_route\n- expected_behavior\n- observed_behavior\n- trigger_conditions\n- root_cause_state\n- root_cause_basis\n- invalidated_assumption_or_strategy\n- prohibited_retry_pattern\n- corrective_constraint\n- applicability_signature\n- applicability_signature_hash\n- applicability_state\n- affected_task_classes\n- specialist_or_method_refs\n- retest_requirement\n- retest_state\n- lifecycle_state\n- recurrence_count\n- superseded_by\n- evidence_refs\n- source_ledger_entry_ref\n\nAIR_PRIOR_EFFECT_RECORD allowed object-owned top-level fields:'''
insert='''AIR_FAILURE_MODE_RECORD allowed object-owned top-level fields:\n- failure_mode_id\n- originating_task_ref\n- originating_attempt_id\n- failure_class\n- failed_step_or_route\n- expected_behavior\n- observed_behavior\n- trigger_conditions\n- root_cause_state\n- root_cause_basis\n- invalidated_assumption_or_strategy\n- prohibited_retry_pattern\n- corrective_constraint\n- applicability_signature\n- applicability_signature_hash\n- applicability_state\n- affected_task_classes\n- specialist_or_method_refs\n- retest_requirement\n- retest_state\n- lifecycle_state\n- recurrence_count\n- superseded_by\n- evidence_refs\n- source_ledger_entry_ref\n\nAIR_METHOD_EVIDENCE_WAIVER allowed object-owned top-level fields:\n- waiver_id\n- method_identity\n- method_version\n- step_id\n- waived_requirement\n- waiver_scope\n- artifact_scope_ref\n- permission_basis_type\n- permission_basis_ref\n- reason\n- issued_state_epoch\n- validity_state\n- applied_state\n- evidence_refs\n- claim_boundary\n\nAIR_METHOD_EVIDENCE_WAIVER validation law:\n- waiver_scope must equal METHOD_STEP_EVIDENCE_TO_ADVANCE_ONLY.\n- method_identity, method_version, step_id, waived_requirement, and artifact_scope_ref must exactly match the active Method execution and the one missing evidence_to_advance requirement.\n- permission_basis_type must be explicitly allowed by the active Method Pack evidence_waiver_contract. EXPLICIT_USER_APPROVAL requires a resolvable user-visible permission_basis_ref; free text, generic approval state, model judgment, or inferred intent is insufficient.\n- validity_state is ACTIVE_CURRENT, APPLIED_RECORDED, REVOKED, or EXPIRED. Only ACTIVE_CURRENT or APPLIED_RECORDED may support the exact completion whose basis they record.\n- applied_state records whether the exact waiver has been consumed as completion basis; it does not grant execution authority and remains historical evidence after application.\n- AIR_METHOD_EVIDENCE_WAIVER must be canonically emitted/ledgered before it may be referenced for completion or Handoff. Restored references remain non-authorizing bootstrap input until current validation.\n\nAIR_PRIOR_EFFECT_RECORD allowed object-owned top-level fields:'''
core=replace_once(core,anchor,insert,'core waiver fields')
core=replace_once(core,'A step cannot become COMPLETE without its evidence_to_advance unless an explicit, permitted waiver is recorded. Written instructions alone do not prove execution.','A step cannot become COMPLETE without its evidence_to_advance unless an exact AIR_METHOD_EVIDENCE_WAIVER is canonically recorded and validates for that method/version/step/requirement/artifact scope under the active Method Pack waiver contract. Free text, generic approval, inferred permission, or reconstructed Handoff state cannot satisfy the exception. Written instructions alone do not prove execution.','core method completion')
cp.write_text(core,encoding='utf-8')

st=load(STARTER)
ids=st['typed_registries']['formal_objects']['object_ids']
if 'AIR_METHOD_EVIDENCE_WAIVER' not in ids: ids.insert(ids.index('AIR_FAILURE_MODE_RECORD')+1,'AIR_METHOD_EVIDENCE_WAIVER')
if 'method-evidence-waiver' not in st['compiler_contract']['required_formal_object_rendering_rule']:
    st['compiler_contract']['required_formal_object_rendering_rule']=st['compiler_contract']['required_formal_object_rendering_rule'].replace('surfaced-object ledger, or failure-mode records','surfaced-object ledger, failure-mode, or method-evidence-waiver records')
save(STARTER,st)

h=load(HANDOFF); card=h['AIR_HANDOFF_CARD']; vr=card['schema_manifest']['validation_registry']; ops=vr['allowed_operators']
if 'METHOD_EVIDENCE_WAIVER_REFS_VALID' not in ops: ops.append('METHOD_EVIDENCE_WAIVER_REFS_VALID')
vr['operator_semantics']['METHOD_EVIDENCE_WAIVER_REFS_VALID']='If active Method Pack method_specific_state declares step_evidence_waiver_refs, each non-null ref must resolve to a surfaced canonical AIR_METHOD_EVIDENCE_WAIVER snapshot whose method/version/step/waived_requirement/artifact scope match the serialized method state and whose validity_state is ACTIVE_CURRENT or APPLIED_RECORDED. Empty refs are allowed when no waiver was used. Unresolved, free-text, mismatched, revoked, expired, or synthesized refs route REVIEW.'
vr['rules']['HC-VALIDATE-METHOD']={'operator':'ALL','predicates':[{'operator':'ACTIVE_METHOD_PACK_HANDOFF_SCHEMA_VALID','path':'$.execution_state.method_handoff_state'},{'operator':'METHOD_EVIDENCE_WAIVER_REFS_VALID','path':'$.execution_state.method_handoff_state'}]}
card['continuation_bootstrap']['method_handoff_recheck']='When method continuation is material, validate method identity/version/origin, active method state/step/gate, staleness, evidence references, blockers, next action, method_specific_state against the current method requirements, and every preserved AIR_METHOD_EVIDENCE_WAIVER ref against its exact current method/version/step/requirement/artifact scope. Missing material state or invalid waiver refs route to REVIEW; do not invent them.'
save(HANDOFF,h)
print('R5 source patch applied or already present')
