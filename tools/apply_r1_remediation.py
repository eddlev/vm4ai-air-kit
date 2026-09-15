from pathlib import Path
import json, hashlib, re, sys
ROOT=(Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path('.').resolve())
core_p=ROOT/'prompts/AIR_CORE_RUNTIME.md'
starter_p=ROOT/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'
control_p=ROOT/'prompts/AIR_CONTROL_SURFACE.md'
rmap_p=ROOT/'catalog/AIR_RUNTIME_ROUTE_MAP.json'
core=core_p.read_text(encoding='utf-8')
if 'Starter top-level PROMPT_VERSION is the sole current Starter version' in core and 'Starter top-level PROMPT_VERSION equals validation_contract.required_version' not in core:
    print('R1 source patch already applied; no mutation performed')
    raise SystemExit(0)
old=core

def one(a,b):
    global core
    n=core.count(a)
    assert n==1, (a[:100], n)
    core=core.replace(a,b,1)

one('7. Starter top-level PROMPT_VERSION equals validation_contract.required_version','7. Starter top-level PROMPT_VERSION is the sole current Starter version; every boot consumer that carries Starter version state compares directly to that canonical path')
one('- RT.ALIGN\n- RT.ACTION\n- RT.RECEIPT','- RT.ALIGN\n- RT.APPROVAL_RESOLVE\n- RT.ACTION\n- RT.RECEIPT')
core=core.replace('failure_route=RT.RECOVERY[AIR_ROUTE]', 'failure_route=RT.RECOVERY\n[AIR_ROUTE]')
core=core.replace('failure_route=END_RESPONSE[AIR_ROUTE]', 'failure_route=END_RESPONSE\n[AIR_ROUTE]')
assert not any('failure_route=' in ln and '[AIR_ROUTE]' in ln for ln in core.splitlines())
one('Evaluation profiles:\n- BOOTSTRAP\n- TURN_ENTRY\n- STATE_TRANSITION\n- HANDOFF_RESTORE\n- PRE_MATERIAL_EFFECT\n- POST_MATERIAL_EFFECT\n- RECOVERY','Evaluation profiles:\n- BOOTSTRAP\n- ACTIVATION\n- TURN_ENTRY\n- STATE_TRANSITION\n- HANDOFF_RESTORE\n- PRE_MATERIAL_EFFECT\n- POST_MATERIAL_EFFECT\n- UNCERTAINTY_RESOLUTION\n- RECOVERY\n\nProfile-specific semantics:\n- ACTIVATION evaluates the canonical pre-bind activation state used by RT.ACTIVATE after onboarding or restored candidate-state preparation; it is not an alias for BOOTSTRAP or STATE_TRANSITION.\n- UNCERTAINTY_RESOLUTION evaluates the canonical state and identified material basis gap immediately before RT.UNCERTAINTY_RESOLVE constructs a required-input, safe-degraded-boundary, review, or evidence-required result; it is not an alias for another profile.\n- All profiles share the same current-state/evaluation-basis constructor and differ only in the declared evaluation purpose and material state slice.')
one('requires=DEP.CURRENT_EVALUATION_BASIS;DEP.ARTIFACT_BOUND;DEP.LEASE_ACTIVE;DEP.SCOPE_MATCH;DEP.APPROVAL_CURRENT;DEP.GATE_ALLOW;DEP.APPROVAL_RESOLUTION_ALLOW_EMITTED;DEP.AUTHORITY_LEDGER_COMMITTED','requires=DEP.CURRENT_EVALUATION_BASIS;DEP.ARTIFACT_BOUND;DEP.LEASE_ACTIVE;DEP.SCOPE_MATCH;DEP.APPROVAL_PRECONDITION_SATISFIED;DEP.GATE_ALLOW;DEP.AUTHORITY_LEDGER_COMMITTED')
one('pre_effect_sequence=TURN_ENTRY_ALIGNMENT;CURRENT_ARTIFACT;ACTIVE_LEASE;NON_NULL_RESOURCE_SCOPE_PIN;CURRENT_APPROVAL;AIR_GATE_ALLOW;AIR_ACTION_AUTHORIZATION_EMITTED','pre_effect_sequence=TURN_ENTRY_ALIGNMENT;CURRENT_ARTIFACT;ACTIVE_LEASE;NON_NULL_RESOURCE_SCOPE_PIN;CURRENT_APPROVAL_WHEN_REQUIRED;AIR_GATE_ALLOW;AIR_ACTION_AUTHORIZATION_EMITTED')
one('approval_resolution_route=RT.APPROVAL_RESOLVE\npost_effect_alignment_profile=POST_MATERIAL_EFFECT','approval_resolution_route=RT.APPROVAL_RESOLVE\napproval_precondition_dependency=DEP.APPROVAL_PRECONDITION_SATISFIED\napproval_precondition_satisfiers=APPROVAL_NOT_REQUIRED|APPROVAL_REQUIRED_AND_CURRENT_APPROVAL_WITH_ALLOW_RESOLUTION_EMITTED\napproval_precondition_unknown_behavior=FAIL_CLOSED\npost_effect_alignment_profile=POST_MATERIAL_EFFECT')
one('AIR-FLOOR-018-MATERIAL-ACTION-AUTHORIZATION-AND-RECEIPT: every material action follows AIR_MATERIAL_ACTION_TRANSACTION_V1 in strict order: current TURN_ENTRY alignment; bound Artifact; ACTIVE lease; non-null exact resource scope pin; current approval; current ALLOW Gate;','AIR-FLOOR-018-MATERIAL-ACTION-AUTHORIZATION-AND-RECEIPT: every material action follows AIR_MATERIAL_ACTION_TRANSACTION_V1 in strict order: current TURN_ENTRY alignment; bound Artifact; ACTIVE lease; non-null exact resource scope pin; current approval when approval is required, otherwise an explicit typed APPROVAL_NOT_REQUIRED precondition; current ALLOW Gate;')
route_blocks=re.split(r'(?m)^\[AIR_ROUTE\]\s*$', core)
assert len(route_blocks)-1==22, len(route_blocks)-1
fixed=[route_blocks[0].rstrip('\n')]
for block in route_blocks[1:]:
    lines=block.splitlines(); rid=None
    for line in lines:
        if line.startswith('id='):
            rid=line.split('=',1)[1].strip(); break
    assert rid
    event_id='CE-RT-'+rid.split('.',1)[1].replace('.', '_').replace('-', '_')
    lines=[ln for ln in lines if not ln.startswith('control_event_ref=') and not ln.startswith('trigger_authority=')]
    out=[]; inserted=False
    for ln in lines:
        out.append(ln)
        if ln.startswith('trigger='):
            out.append('trigger_authority=NON_OPERATIVE_DESCRIPTION')
            out.append(f'control_event_ref={event_id}')
            inserted=True
    assert inserted, rid
    fixed.append('\n'.join(out).strip('\n'))
core='\n[AIR_ROUTE]\n'.join(fixed)
if old.endswith('\n') and not core.endswith('\n'): core+='\n'
core_p.write_text(core,encoding='utf-8')

starter=json.loads(starter_p.read_text(encoding='utf-8'))
starter['authority_contract']['required_files']=[
 {'canonical_role':'CORE_RUNTIME','canonical_filename':'AIR_CORE_RUNTIME.md','SYSTEM_DESIGNATION':'AIR_CORE_RUNTIME_V2'},
 {'canonical_role':'CONTROL_SURFACE','canonical_filename':'AIR_CONTROL_SURFACE.md','SYSTEM_DESIGNATION':'AIR_CONTROL_SURFACE_V2'},
 {'canonical_role':'GOVERNANCE_SUPPLEMENT','canonical_filename':'AIR_GOV.md','SYSTEM_DESIGNATION':'AIR_HR_GOVERNANCE_SUPPLEMENT_V2'},
 {'canonical_role':'DEFAULT_STARTER_PROFILE','canonical_filename':'AIR_DEFAULT_STARTER_PROFILE.json','SYSTEM_DESIGNATION':'AIR_DEFAULT_STARTER_V2'},
 {'canonical_role':'HANDOFF_CARD_TEMPLATE','canonical_filename':'AIR_HANDOFF_CARD_TEMPLATE.json','TEMPLATE_DESIGNATION':'AIR_HANDOFF_CARD_TEMPLATE_V2'}]
det=starter['compiler_contract']['deterministic_pipeline_non_inference']['declared_runtime_routes']
if 'RT.APPROVAL_RESOLVE' not in det: det.append('RT.APPROVAL_RESOLVE')
det.sort()
starter['typed_registries']['runtime_states']['alignment_evaluation_profile']=['BOOTSTRAP','ACTIVATION','TURN_ENTRY','STATE_TRANSITION','HANDOFF_RESTORE','PRE_MATERIAL_EFFECT','POST_MATERIAL_EFFECT','UNCERTAINTY_RESOLUTION','RECOVERY']
mat=starter['compiler_contract']['material_action_transaction']
mat['approval_precondition_contract']={'state_path':'ACTION_APPROVAL_PRECONDITION','approval_required_path':'CURRENT_ACTION_GOVERNANCE.approval_required','allowed_states':['APPROVAL_NOT_REQUIRED','APPROVAL_REQUIRED_AND_CURRENT_APPROVAL_WITH_ALLOW_RESOLUTION_EMITTED','UNRESOLVED'],'satisfying_states':['APPROVAL_NOT_REQUIRED','APPROVAL_REQUIRED_AND_CURRENT_APPROVAL_WITH_ALLOW_RESOLUTION_EMITTED'],'required_when_approval_required_true':['CURRENT_APPROVAL','APPROVAL_RESOLUTION_STATE=APPROVED','ALLOW_RESOLUTION_EMITTED'],'false_branch_rule':'approval_required=false produces APPROVAL_NOT_REQUIRED without synthesizing approval history','unknown_rule':'UNRESOLVED_FAIL_CLOSED'}
reg=starter['compiler_contract']['runtime_control_event_registry']
if 'APPROVAL_PRECONDITION_SATISFIED' not in reg['allowed_guard_operators']: reg['allowed_guard_operators'].append('APPROVAL_PRECONDITION_SATISFIED')
events={e['route_id']:e for e in reg['events']}
def guards(rid, gs): events[rid]['guards']=gs; events[rid]['guard_join']='ALL'
guards('RT.BOOT',[{'operator':'STATE_PRESENT','path':'LOAD_INTEGRITY_STATE'}])
guards('RT.ONBOARD',[{'operator':'STATE_PRESENT','path':'ENTRY_PATH_STATE'}])
guards('RT.HANDOFF_RESTORE',[{'operator':'STATE_EQUALS','path':'HANDOFF_SCHEMA_VALIDATION_STATE','expected':'VALID'},{'operator':'STATE_PRESENT','path':'HANDOFF_EXPLICIT_STATE_INPUT'}])
guards('RT.ACTIVATE',[{'operator':'STATE_PRESENT','path':'CANONICAL_CURRENT_STATE'},{'operator':'STATE_EQUALS','path':'BINDABLE_ARTIFACT_CANDIDATE_COUNT','expected':1}])
guards('RT.ALIGN',[{'operator':'STATE_PRESENT','path':'CANONICAL_CURRENT_STATE'},{'operator':'REFERENCE_RESOLVES','path':'REQUESTED_ALIGNMENT_PROFILE','registry_path':'typed_registries.runtime_states.alignment_evaluation_profile'}])
guards('RT.UNCERTAINTY_RESOLVE',[{'operator':'STATE_PRESENT','path':'BASIS_GAP_IDENTIFIED'},{'operator':'STATE_PRESENT','path':'CANONICAL_CURRENT_STATE'}])
guards('RT.RECOVERY',[{'operator':'STATE_PRESENT','path':'RECOVERY_TRIGGER_STATE'},{'operator':'STATE_PRESENT','path':'CANONICAL_CURRENT_STATE'}])
guards('RT.ACTION',[{'operator':'STATE_PRESENT','path':'CURRENT_EVALUATION_BASIS'},{'operator':'STATE_PRESENT','path':'CURRENT_BOUND_ARTIFACT'},{'operator':'APPROVAL_PRECONDITION_SATISFIED','path':'ACTION_APPROVAL_PRECONDITION','satisfying_states':['APPROVAL_NOT_REQUIRED','APPROVAL_REQUIRED_AND_CURRENT_APPROVAL_WITH_ALLOW_RESOLUTION_EMITTED']},{'operator':'STATE_EQUALS','path':'CURRENT_AIR_GATE.decision','expected':'ALLOW'},{'operator':'LEDGER_CONTAINS','path':'AIR_SURFACED_OBJECT_LEDGER','object_name':'AIR_GATE'},{'operator':'STATE_NOT_NULL','path':'CURRENT_RESOURCE_SCOPE_PIN'},{'operator':'STATE_EQUALS','path':'CURRENT_ARTIFACT_LEASE.state','expected':'ACTIVE'},{'operator':'STATE_EQUALS','path':'AUTHORITY_LEDGER_COMMIT_STATE','expected':'COMMITTED'}])
sfv=starter['routing_contracts']['sfv_method_routing']
sfv['need_states']=['NOT_NEEDED','INLINE_METHOD_SUFFICIENT','RECOMMENDED','REQUIRED_FOR_APPROVAL','REQUIRED_FOR_SAFE_EXECUTION']
sfv['layer_type']='METHOD_PACK'; sfv['specialization']='SPECIFICATION_FIRST_VERIFICATION'
sfv['legacy_state_projection']={'FULL_SFV_RECOMMENDED':'RECOMMENDED','FULL_SFV_REQUIRED_FOR_APPROVAL':'REQUIRED_FOR_APPROVAL','FULL_SFV_REQUIRED_FOR_SAFE_EXECUTION':'REQUIRED_FOR_SAFE_EXECUTION'}
sfv['legacy_state_projection_authority']='MIGRATION_OR_DISPLAY_COMPATIBILITY_ONLY_NOT_CORE_CONTROL_OUTPUT'
starter['local_profile_policies']['method_and_executor']['specification_first_verification_method']['routing_rule']='Core chooses canonical capability need_state NOT_NEEDED, INLINE_METHOD_SUFFICIENT, RECOMMENDED, REQUIRED_FOR_APPROVAL, or REQUIRED_FOR_SAFE_EXECUTION with layer_type=METHOD_PACK and specialization=SPECIFICATION_FIRST_VERIFICATION using specification dependence, consequence, evidence pressure, recurrence, downstream dependency, verification difficulty, and portability/handoff need.'
rt=starter['validation_contract']['required_retests']
for i,s in enumerate(rt):
    if 'top-level PROMPT_VERSION equals validation_contract.required_version' in s: rt[i]='new-project boot accepts the current Starter only when top-level PROMPT_VERSION is present and all typed cross-file consumers that carry Starter version state agree with that canonical path'
dcr=starter['validation_contract']['deterministic_contract_registry']; dcr['registry_version']='1.1.0'; dcr['foundation_prompt_version_contract']={'authority_class':'RUNTIME_OPERATIVE_TYPED_CONTRACT','CORE':'2.6.0','CONTROL':'2.6.0','GOVERNANCE':'2.3.0'}
checks=dcr['checks']; ids={c['check_id'] for c in checks}
def add(c): assert c['check_id'] not in ids,c['check_id']; checks.append(c); ids.add(c['check_id'])
for cid,name,key in [('DC-VERSION-CORE','prompts/AIR_CORE_RUNTIME.md','CORE'),('DC-VERSION-CONTROL','prompts/AIR_CONTROL_SURFACE.md','CONTROL'),('DC-VERSION-GOV','prompts/AIR_GOV.md','GOVERNANCE')]: add({'check_id':cid,'operator':'MARKDOWN_HEADER_EQUALS_REGISTRY_VALUE','on_failure':'FAIL_CLOSED','file':name,'header':'PROMPT_VERSION','registry_value_path':f'$.validation_contract.deterministic_contract_registry.foundation_prompt_version_contract.{key}'})
for cid,path,expected in [('DC-KIND-STARTER','$.PROFILE_KIND','TASK_COMPOSITE'),('DC-FUNCTION-CLASS-STARTER','$.profile_function_class','DEFAULT_STARTER_PROFILE'),('DC-FILENAME-STARTER','$.canonical_filename','AIR_DEFAULT_STARTER_PROFILE.json')]: add({'check_id':cid,'operator':'JSON_EQUALS_LITERAL','on_failure':'FAIL_CLOSED','left':{'file':'prompts/AIR_DEFAULT_STARTER_PROFILE.json','path':path},'expected':expected})
for cid,name in [('DC-STRICT-JSON-STARTER','prompts/AIR_DEFAULT_STARTER_PROFILE.json'),('DC-STRICT-JSON-HANDOFF','prompts/AIR_HANDOFF_CARD_TEMPLATE.json')]: add({'check_id':cid,'operator':'STRICT_JSON_PARSE_NO_DUPLICATES','on_failure':'FAIL_CLOSED','file':name})
add({'check_id':'DC-FOUNDATION-NORMALIZED-COLLISION','operator':'FOUNDATION_FILENAME_COLLISION_FREE','on_failure':'FAIL_CLOSED','manifest_file':'prompts/AIR_DEFAULT_STARTER_PROFILE.json','manifest_path':'$.authority_contract.required_files','normalization_steps':['PERCENT_DECODE','UNICODE_NFKC','CASEFOLD','TRIM_TRAILING_SPACE_OR_PERIOD']})
add({'check_id':'DC-FOUNDATION-MANIFEST-EXACT','operator':'FOUNDATION_MANIFEST_EXACT','on_failure':'FAIL_CLOSED','manifest_file':'prompts/AIR_DEFAULT_STARTER_PROFILE.json','manifest_path':'$.authority_contract.required_files','foundation_directory':'prompts'})
core_text=core_p.read_text(encoding='utf-8')
for n in range(1,25):
    m=re.search(rf'^- (AIR-FLOOR-{n:03d}-[^:]+):',core_text,re.M); assert m,n
    add({'check_id':f'DC-CORE-FLOOR-{n:03d}','operator':'TEXT_CONTAINS_LITERAL','on_failure':'FAIL_CLOSED','file':'prompts/AIR_CORE_RUNTIME.md','expected':m.group(1)})
for k in ['declared_check_count','implemented_check_count_required','executed_check_count_required']: dcr['coverage_contract'][k]=len(checks)
starter_p.write_text(json.dumps(starter,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

control=control_p.read_text(encoding='utf-8')
needle='- When Core returns FULL_SFV_RECOMMENDED or a required Full-SFV state, show why the reusable method adds value, what it changes in procedure/evidence/handoff, whether work is blocked, and the inline fallback when safe.'
assert control.count(needle)==1
control=control.replace(needle,'- When Core returns RECOMMENDED, REQUIRED_FOR_APPROVAL, or REQUIRED_FOR_SAFE_EXECUTION for layer_type=METHOD_PACK with specialization=SPECIFICATION_FIRST_VERIFICATION, show why the reusable SFV method adds value, what it changes in procedure/evidence/handoff, whether work is blocked, and the inline fallback when safe.')
control_p.write_text(control,encoding='utf-8')

rmap=json.loads(rmap_p.read_text(encoding='utf-8')); rmap['source_of_truth']['sha256']=hashlib.sha256(core_p.read_bytes()).hexdigest(); ct=core_p.read_text(encoding='utf-8')
route_info={}
for block in re.split(r'(?m)^\[AIR_ROUTE\]\s*$', ct)[1:]:
    rec={}
    for ln in block.splitlines():
        ln=ln.strip()
        if not ln: continue
        if ln.startswith('='): break
        if '=' in ln:
            k,v=ln.split('=',1); rec[k.strip()]=v.strip()
    if 'id' in rec: route_info[rec['id']]=rec
assert len(route_info)==22,len(route_info)
line_by_id={}
for i,ln in enumerate(ct.splitlines(),1):
    if ln.startswith('id=RT.'): line_by_id[ln.split('=',1)[1]]=i
for r in rmap['routes']:
    rid=r['route_id']; c=route_info[rid]; r['source_anchor']={'filename':'AIR_CORE_RUNTIME.md','patch_marker':'AIR_ROUTE_DEPENDENCY_KERNEL_V1','line':line_by_id[rid]}
    if rid=='RT.ACTION':
        r['requires']=c['requires'].split(';') if c['requires'] else []
        r.setdefault('material_action_transaction',{})['approval_precondition_dependency']='DEP.APPROVAL_PRECONDITION_SATISFIED'
        r['material_action_transaction']['approval_required_branch']='CURRENT_EXACT_APPROVAL_AND_ALLOW_RESOLUTION_EMITTED'
        r['material_action_transaction']['approval_not_required_branch']='EXPLICIT_TYPED_APPROVAL_NOT_REQUIRED'
rmap['deterministic_pipeline_contract']['declared_route_ids']=sorted(starter['compiler_contract']['deterministic_pipeline_non_inference']['declared_runtime_routes'])
rmap_p.write_text(json.dumps(rmap,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('R1 source patch applied')
print('Core sha256',hashlib.sha256(core_p.read_bytes()).hexdigest())
print('Starter checks',len(checks))
print('Route anchors',len(line_by_id))
