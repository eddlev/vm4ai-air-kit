import json, hashlib, pathlib, re, os, zipfile, shutil
from collections import defaultdict, Counter
from datetime import datetime, timezone

ROOT=pathlib.Path(os.environ.get('AIR250_VALIDATION_ROOT', pathlib.Path(__file__).resolve().parents[1]))
OUT=pathlib.Path(os.environ.get('AIR250_VALIDATION_OUT', ROOT/'validation')); OUT.mkdir(parents=True,exist_ok=True)

# Canonical semantic candidate files.
FILES={
 'foundation.core': ROOT/'foundation/AIR_CORE_RUNTIME.md',
 'foundation.control': ROOT/'foundation/AIR_CONTROL_SURFACE.md',
 'foundation.gov': ROOT/'foundation/AIR_GOV.md',
 'foundation.starter': ROOT/'foundation/AIR_DEFAULT_STARTER_PROFILE.json',
 'foundation.handoff': ROOT/'foundation/AIR_HANDOFF_CARD_TEMPLATE.json',
 'foundation.route_map': ROOT/'catalog/AIR_RUNTIME_ROUTE_MAP.json',
 'catalog.specialist_index': ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',
 'cea.registry': ROOT/'specialists/capability-ecology/AIR_DOMAIN_CAPABILITY_REGISTRY.json',
 'cea.translator': ROOT/'specialists/capability-ecology/AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json',
 'cea.architect': ROOT/'specialists/capability-ecology/AIR_CAPABILITY_ECOLOGY_ARCHITECT.json',
 'cea.method': ROOT/'specialists/capability-ecology/AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json',
 'cea.manifest': ROOT/'specialists/capability-ecology/AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json',
 'grounding.domain': ROOT/'specialists/grounding/AIR_GROUNDING_DOMAIN_PACKAGE.json',
 'grounding.method': ROOT/'specialists/grounding/AIR_GROUNDING_METHOD_PACK.json',
 'grounding.specialist': ROOT/'specialists/grounding/AIR_GROUNDING_SPECIALIST.json',
 'grounding.executor': ROOT/'specialists/grounding/AIR_GROUNDING_EXECUTOR.json',
 'grounding.manifest': ROOT/'specialists/grounding/AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json',
 'sfv.domain': ROOT/'specialists/sfv/AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json',
 'sfv.method': ROOT/'specialists/sfv/AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json',
 'sfv.specialist': ROOT/'specialists/sfv/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json',
 'sfv.executor': ROOT/'specialists/sfv/AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json',
 'sfv.manifest': ROOT/'specialists/sfv/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json',
 'aigov.domain': ROOT/'specialists/ai-governance/AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json',
 'aigov.overlay': ROOT/'specialists/ai-governance/AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json',
 'aigov.specialist': ROOT/'specialists/ai-governance/AIR_AI_GOVERNANCE_SPECIALIST.json',
 'aigov.method': ROOT/'specialists/ai-governance/AIR_AI_GOVERNANCE_METHOD_PACK.json',
 'aigov.executor': ROOT/'specialists/ai-governance/AIR_AI_GOVERNANCE_EXECUTOR.json',
 'aigov.manifest': ROOT/'specialists/ai-governance/AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json',
}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def line_count(p):
    b=p.read_bytes()
    return b.count(b'\n') + (1 if b and not b.endswith(b'\n') else 0)

def strict_load(p):
    duplicates=[]
    def hook(pairs):
        d={}; seen=set()
        for k,v in pairs:
            if k in seen: duplicates.append(k)
            seen.add(k); d[k]=v
        return d
    with open(p,encoding='utf-8') as f:
        obj=json.load(f, object_pairs_hook=hook)
    if duplicates: raise ValueError('duplicate keys: '+', '.join(sorted(set(duplicates))))
    return obj

checks=[]
def add(cid, ok, category, detail, severity='ERROR', evidence=None):
    ev=[]
    for x in (evidence or []):
        sx=str(x)
        root_prefix=str(ROOT)
        if sx.startswith(root_prefix):
            sx='.'+sx[len(root_prefix):]
        ev.append(sx.replace(os.sep,'/').replace('\\','/'))
    checks.append({
      'check_id':cid,
      'status':'PASS' if ok else ('WARN' if severity=='WARNING' else 'FAIL'),
      'category':category,
      'severity':severity,
      'detail':detail,
      'evidence':ev
    })

# Inventory and JSON integrity.
for key,p in FILES.items():
    add(f'INV.EXISTS.{key}',p.exists(),'INVENTORY',f'{key} exists at {p.name}', evidence=[str(p)])
    if p.exists():
        add(f'INV.NONEMPTY.{key}',p.stat().st_size>0,'INVENTORY',f'{key} non-empty ({p.stat().st_size} bytes)', evidence=[str(p)])
        if p.suffix=='.json':
            try:
                strict_load(p); ok=True; detail='strict JSON parse passed; duplicate keys rejected'
            except Exception as e:
                ok=False; detail=f'strict JSON parse failed: {e}'
            add(f'JSON.STRICT.{key}',ok,'JSON_INTEGRITY',detail,evidence=[str(p)])

add('INV.SEMANTIC_FILE_COUNT',len(FILES)==28,'INVENTORY',f'Integrated semantic candidate set contains {len(FILES)} expected files; expected 28.')

# Load data.
core=FILES['foundation.core'].read_text(encoding='utf-8')
control=FILES['foundation.control'].read_text(encoding='utf-8')
gov=FILES['foundation.gov'].read_text(encoding='utf-8')
starter=strict_load(FILES['foundation.starter'])
handoff=strict_load(FILES['foundation.handoff'])
route_map=strict_load(FILES['foundation.route_map'])
index=strict_load(FILES['catalog.specialist_index'])

# T12D Foundation regression checks: close the three known Foundation defects.
handoff_card=handoff.get('AIR_HANDOFF_CARD',{})
gov_match=re.search(r'(?m)^PROMPT_VERSION:\s*([^\n]+)$',gov)
active_gov_version=gov_match.group(1).strip() if gov_match else None
add('FOUNDATION.HANDOFF_GOVERNANCE_VERSION_DRIFT_CLOSED',handoff_card.get('governance_state',{}).get('governance_supplement_version')==active_gov_version=='2.3.0','FOUNDATION_CONSISTENCY',f'Handoff governance version={handoff_card.get("governance_state",{}).get("governance_supplement_version")!r}; active Governance={active_gov_version!r}.')
restore_match=re.search(r'Required restoration carriers include:(.*?)(?=\nGovernance state must preserve:)',core,re.S)
restore_seg=restore_match.group(1) if restore_match else ''
te=handoff_card.get('test_evidence_state',{})
restore_ok=all(x in restore_seg for x in ['presentation_mode and presentation_mode_source','evidence_capture_gaps']) and all(x not in restore_seg for x in ['mode and mode_source','rerun_required_for_full_evidence']) and all(k in te for k in ['presentation_mode','presentation_mode_source','evidence_capture_gaps'])
add('FOUNDATION.HANDOFF_RESTORATION_SCHEMA_DRIFT_CLOSED',restore_ok,'FOUNDATION_CONSISTENCY',f'Core restoration carriers and Handoff schema 2.3 presentation fields agree={restore_ok}.')
old_presentation_contradiction='STANDARD_EVIDENCE_PRESENTATION cannot satisfy it without an authorized equivalent evidence source'
presentation_ok=old_presentation_contradiction not in core and 'regardless of presentation mode' in core and 'Both modes preserve the same underlying evidence state.' in core
add('FOUNDATION.EVIDENCE_PRESENTATION_SEMANTIC_CONTRADICTION_CLOSED',presentation_ok,'FOUNDATION_CONSISTENCY',f'Presentation-only evidence semantics coherent={presentation_ok}.')

# Formal-object responsibility closure checks.
canonical_object_ids=[
 'AIR_RUNTIME_BRIDGE','AIR_SESSION','AIR_PROJECT_INITIALIZATION_BRIEF','AIR_PROJECT_EXECUTION_MAP',
 'AIR_ARTIFACT','AIR_ACTIVE_CONTRACT','AIR_GATE','AIR_VALIDATION_REPORT','AIR_ALIGNMENT_CHECK',
 'AIR_ERROR','AIR_ACTION_AUTHORIZATION','AIR_ACTION_RECEIPT','AIR_PRIOR_EFFECT_RECORD',
 'AIR_REQUIRED_INPUT_REQUEST','AIR_HANDOFF_CARD']
add('OBJECTS.REGISTRY_MARKER','AIR_CANONICAL_OBJECT_CONTRACTS_V4' in core and 'AIR_OBJECT_RESPONSIBILITY_CLOSURE_V1' in core,'OBJECT_RESPONSIBILITY','Core V4 canonical registry and responsibility-closure marker are present.')
class_seg=core[core.index('Canonical formal object classes:'):core.index('Object identity and record category:')] if 'Canonical formal object classes:' in core and 'Object identity and record category:' in core else ''
core_object_ids=re.findall(r'^-\s+(AIR_[A-Z0-9_]+):\s+[A-Z_]+\s*$',class_seg,re.M)
add('OBJECTS.CANONICAL_SET',core_object_ids==canonical_object_ids,'OBJECT_RESPONSIBILITY',f'Core canonical object set/order={core_object_ids!r}.')
add('OBJECTS.ROOT_IDENTITY_RULE','The top-level AIR object root name identifies semantic object identity.' in core and 'record_class identifies the semantic record category' in core,'OBJECT_RESPONSIBILITY','Root name owns object identity; record_class is a category.')
add('OBJECTS.CLOSED_WORLD_RULE','OBJECT_SCHEMA_FIELD_OWNERSHIP_VIOLATION' in core and 'CLOSED-WORLD TOP-LEVEL FIELD LAW' in core,'OBJECT_RESPONSIBILITY','Unknown/foreign top-level formal-object fields fail closed.')
for oid in canonical_object_ids:
    if oid=='AIR_HANDOFF_CARD':
        ok='AIR_HANDOFF_CARD allowed top-level fields are exactly those declared by its current template schema' in core
    elif oid=='AIR_ARTIFACT':
        ok='AIR_ARTIFACT base allowed object-owned top-level fields' in core
    else:
        ok=f'{oid} allowed object-owned top-level fields' in core
    add(f'OBJECTS.OWNERSHIP.{oid}',ok,'OBJECT_RESPONSIBILITY',f'{oid} has a Core-owned closed responsibility declaration.')
# Reservation surfaces must match the canonical set and contain no retired pseudo-object.
def _reserved(text,start_phrase,end_phrase):
    try: seg=text[text.index(start_phrase)+len(start_phrase):text.index(end_phrase,text.index(start_phrase)+len(start_phrase))]
    except ValueError: return []
    return re.findall(r'^-\s+(AIR_[A-Z0-9_]+)\s*$',seg,re.M)
core_reserved=_reserved(core,'Reserved formal object labels include:','AIR must not use reserved formal object labels')
control_reserved=_reserved(control,'Reserved labels:','In compact interaction')
add('OBJECTS.RESERVED.CORE',core_reserved==canonical_object_ids and 'AIR_PRIMED_ONBOARDING' not in core,'OBJECT_RESPONSIBILITY',f'Core reserved labels={core_reserved!r}.')
add('OBJECTS.RESERVED.CONTROL',control_reserved==canonical_object_ids and 'AIR_PRIMED_ONBOARDING' not in control,'OBJECT_RESPONSIBILITY',f'Control reserved labels={control_reserved!r}.')
formal_reg=starter.get('typed_registries',{}).get('formal_objects',{})
add('OBJECTS.STARTER.REGISTRY',formal_reg.get('registry_designation')=='AIR_CANONICAL_OBJECT_CONTRACTS_V4' and formal_reg.get('object_ids')==canonical_object_ids,'OBJECT_RESPONSIBILITY',f'Starter registry designation={formal_reg.get("registry_designation")!r}; object count={len(formal_reg.get("object_ids",[]))}.')
add('OBJECTS.STARTER.CLOSED_WORLD',formal_reg.get('top_level_schema_rule')=='CLOSED_WORLD_CORE_OWNED_FIELDS_ONLY','OBJECT_RESPONSIBILITY',f'Starter top-level schema rule={formal_reg.get("top_level_schema_rule")!r}.')
af=starter.get('typed_registries',{}).get('artifact_fields',{})
add('OBJECTS.STARTER.NO_BASE_REDECLARATION',isinstance(af,dict) and af.get('semantic_fields_redeclared') is False and af.get('source_marker')=='AIR_OBJECT_RESPONSIBILITY_CLOSURE_V1','OBJECT_RESPONSIBILITY',f'Starter Artifact registry consumer state={af!r}.')
formal_labels=set(canonical_object_ids)
foreign=[]
for r in starter.get('typed_registries',{}).get('conditional_requirements',[]):
    for f in r.get('fields',[]):
        if f in formal_labels: foreign.append((r.get('id'),f))
add('OBJECTS.STARTER.NO_OBJECT_AS_FIELD',not foreign,'OBJECT_RESPONSIBILITY',f'Formal object labels embedded as fields={foreign!r}.')
add('OBJECTS.EXACT_GATE_SCHEMA','AIR_GATE_V3' in core and '"evaluation_checks"' in core and 'The prior Gate fields mode, artifact_binding_state, authority_level' in core,'OBJECT_RESPONSIBILITY','Gate is a compact decision projection rather than a copy of Artifact/Contract state.')
add('OBJECTS.EXACT_ACTION_AUTH','AIR_ACTION_AUTHORIZATION exact schema:' in core and '"gate_ref"' in core and '"controlling_artifact_ref"' in core,'OBJECT_RESPONSIBILITY','Authorization exact single-use ticket schema is defined by Core.')
add('OBJECTS.EXACT_ACTION_RECEIPT','AIR_ACTION_RECEIPT exact schema:' in core and '"state_comparison"' in core and '"unexpected_side_effects"' in core,'OBJECT_RESPONSIBILITY','Receipt exact intended-versus-actual schema is defined by Core.')
add('OBJECTS.EXACT_PRIOR_EFFECT','AIR_PRIOR_EFFECT_RECORD exact schema:' in core and '"retroactive_authorization_forbidden"' in core,'OBJECT_RESPONSIBILITY','Prior-effect exact recovery schema is defined by Core.')
add('OBJECTS.ACTIVE_CONTRACT.VOCABULARY','deprecated aliases scope_in, scope_out, prohibited_actions, required_evidence, rescope_rule, and binding_state' in core,'OBJECT_RESPONSIBILITY','Active Contract aliases are retired in favor of Artifact execution-contract vocabulary.')
add('OBJECTS.HANDOFF.REV14',handoff_card.get('card_revision')==14,'OBJECT_RESPONSIBILITY',f'Handoff card revision={handoff_card.get("card_revision")!r}; expected 14.')
toc=handoff_card.get('transfer_ownership_contract',{})
add('OBJECTS.HANDOFF.TRANSFER_OWNERSHIP',isinstance(toc,dict) and toc.get('contract_version')=='1.0.0' and 'current_task_binding' in toc.get('canonical_transfer_carriers',{}),'OBJECT_RESPONSIBILITY','Handoff transfer ownership/precedence contract is present for rev14.')

# Prior stage validations are evidence inputs, not substitutes.
# The distributable T12C integrated report preserves the six earlier stage decisions.
prior_integrated=ROOT/'validation/AIR_2.5.0_T12C_FULL_CROSS_SYSTEM_STATIC_VALIDATION.json'
try:
    pr=strict_load(prior_integrated)['AIR_VALIDATION_REPORT']
    prior_checks={c.get('check_id'):c for c in pr.get('checks',[])}
    for name in ['F1','T7','T8','T9','T10','INDEX']:
        cid=f'PRIOR.{name}.PASS'; c=prior_checks.get(cid,{})
        ok=c.get('status')=='PASS'
        add(cid,ok,'PRIOR_STAGE_EVIDENCE',f'{name} prior validation preserved by T12C integrated report; status={c.get("status")!r}.',evidence=[str(prior_integrated)])
except Exception as e:
    for name in ['F1','T7','T8','T9','T10','INDEX']:
        add(f'PRIOR.{name}.PASS',False,'PRIOR_STAGE_EVIDENCE',f'{name} prior validation unavailable from preserved T12C integrated report: {e}',evidence=[str(prior_integrated)])

# Foundation canonical actual identities.
foundation_actual={
 'AIR_CORE_RUNTIME.md': {'path':FILES['foundation.core'],'designation':'AIR_CORE_RUNTIME_V2','version':'2.5.0','class':'FOUNDATION_PROMPT'},
 'AIR_CONTROL_SURFACE.md': {'path':FILES['foundation.control'],'designation':'AIR_CONTROL_SURFACE_V2','version':'2.5.0','class':'FOUNDATION_PROMPT'},
 'AIR_GOV.md': {'path':FILES['foundation.gov'],'designation':'AIR_HR_GOVERNANCE_SUPPLEMENT_V2','version':'2.3.0','class':'FOUNDATION_PROMPT'},
 'AIR_DEFAULT_STARTER_PROFILE.json': {'path':FILES['foundation.starter'],'designation':'AIR_DEFAULT_STARTER_V2','version':'2.5.0','class':'TASK_COMPOSITE'},
 'AIR_HANDOFF_CARD_TEMPLATE.json': {'path':FILES['foundation.handoff'],'designation':'AIR_HANDOFF_CARD_TEMPLATE_V2','version':'2.3.0','class':'TEMPLATE'},
}
for fn,meta in foundation_actual.items():
    meta['sha256']=sha(meta['path']); meta['size_bytes']=meta['path'].stat().st_size; meta['line_count']=line_count(meta['path'])

# Index foundation closure.
idx_ff={x['filename']:x for x in index['foundation_compatibility_catalog']['required_files']}
add('INDEX.FOUNDATION_COUNT',len(idx_ff)==5,'INDEX_CLOSURE',f'Index Foundation file count={len(idx_ff)}; expected 5.')
for fn,a in foundation_actual.items():
    e=idx_ff.get(fn)
    add(f'INDEX.FOUNDATION_PRESENT.{fn}',e is not None,'INDEX_CLOSURE',f'Index contains {fn}.')
    if e:
        for fld in ['sha256','size_bytes','line_count','designation','version','class']:
            add(f'INDEX.FOUNDATION_{fld.upper()}.{fn}',e.get(fld)==a.get(fld),'INDEX_CLOSURE',f'{fn} {fld}: index={e.get(fld)!r}, actual={a.get(fld)!r}')

# Route map source identity and authority.
rm_st=route_map.get('source_of_truth',{})
add('ROUTE_MAP.SOURCE_SHA',rm_st.get('sha256')==foundation_actual['AIR_CORE_RUNTIME.md']['sha256'],'ROUTE_GRAPH',f'Route Map Core SHA={rm_st.get("sha256")}; actual={foundation_actual["AIR_CORE_RUNTIME.md"]["sha256"]}')
for fld in ['execution','binding','selection','approval','semantic_definition']:
    add(f'ROUTE_MAP.AUTHORITY.{fld}',route_map.get('authority',{}).get(fld)=='NONE','ROUTE_GRAPH',f'Route Map {fld} authority={route_map.get("authority",{}).get(fld)!r}; expected NONE.')

# Parse Core [AIR_ROUTE] blocks and compare exact derivation.
route_block_re=re.compile(r'\[AIR_ROUTE\]\n(.*?)(?=\n\[AIR_ROUTE\]|\n={10,}|\Z)',re.S)
core_routes=[]
for block in route_block_re.findall(core):
    d={}
    for line in block.strip().splitlines():
        if '=' in line:
            k,v=line.split('=',1); d[k.strip()]=v.strip()
    if 'id' in d:
        core_routes.append(d)
rm_routes=route_map.get('routes',[])
rm_ids=[r.get('route_id') for r in rm_routes]
core_ids=[r.get('id') for r in core_routes]
add('ROUTE.UNIQUE_IDS',len(rm_ids)==len(set(rm_ids)),'ROUTE_GRAPH',f'Route Map IDs unique: {len(set(rm_ids))}/{len(rm_ids)}.')
add('ROUTE.COUNT_MATCH_CORE',len(core_ids)==len(rm_ids)==route_map.get('route_count'),'ROUTE_GRAPH',f'Core routes={len(core_ids)}, map routes={len(rm_ids)}, declared={route_map.get("route_count")}.')
add('ROUTE.ID_SET_MATCH_CORE',set(core_ids)==set(rm_ids),'ROUTE_GRAPH',f'Core/Route Map route ID sets match.')
canonical_routes=set(rm_ids)
rm_by={r['route_id']:r for r in rm_routes}
for r in rm_routes:
    rid=r['route_id']
    add(f'ROUTE.OWNER.{rid}',r.get('semantic_owner')=='AIR_CORE_RUNTIME','ROUTE_GRAPH',f'{rid} semantic_owner={r.get("semantic_owner")!r}.')
    for nxt in r.get('allowed_next_routes',[]):
        add(f'ROUTE.NEXT_VALID.{rid}.{nxt}',nxt in canonical_routes or nxt=='END_RESPONSE','ROUTE_GRAPH',f'{rid} allowed_next {nxt} is canonical or END_RESPONSE.')
    fr=r.get('failure_route')
    add(f'ROUTE.FAIL_VALID.{rid}',fr in canonical_routes or fr=='END_RESPONSE','ROUTE_GRAPH',f'{rid} failure_route={fr}.')

# Compare route-map values to Core blocks.
def split_field(s):
    if s is None or s=='none': return []
    return s.split('|') if '|' in s else s.split(';')
for c in core_routes:
    rid=c['id']; r=rm_by.get(rid)
    if not r: continue
    add(f'ROUTE.DERIVE.OWNER.{rid}',r.get('semantic_owner')==c.get('semantic_owner'),'ROUTE_DERIVATION',f'{rid} owner derives from Core.')
    add(f'ROUTE.DERIVE.TRIGGER.{rid}',r.get('trigger')==c.get('trigger'),'ROUTE_DERIVATION',f'{rid} trigger derives from Core.')
    for corek,mapk in [('requires','requires'),('produces','produces'),('allowed_next','allowed_next_routes'),('invalidates','invalidates'),('does_not_bypass','does_not_bypass')]:
        exp=[] if c.get(corek) in (None,'none') else split_field(c.get(corek))
        got=r.get(mapk,[])
        add(f'ROUTE.DERIVE.{corek.upper()}.{rid}',got==exp,'ROUTE_DERIVATION',f'{rid} {corek}: map={got}, Core={exp}')
    add(f'ROUTE.DERIVE.FAILURE.{rid}',r.get('failure_route')==c.get('failure_route'),'ROUTE_DERIVATION',f'{rid} failure route derives from Core.')

# Graph cycle and reachability.
graph={r['route_id']:[x for x in r.get('allowed_next_routes',[]) if x in canonical_routes] for r in rm_routes}
state={}; stack=[]; cycles=[]
def dfs(u):
    state[u]=1; stack.append(u)
    for v in graph.get(u,[]):
        if state.get(v,0)==0: dfs(v)
        elif state.get(v)==1:
            try:i=stack.index(v); cycles.append(stack[i:]+[v])
            except:pass
    stack.pop(); state[u]=2
for u in canonical_routes:
    if state.get(u,0)==0: dfs(u)
add('ROUTE.NO_CYCLES',not cycles,'ROUTE_GRAPH',f'Illegal cycles={cycles}.')
seen=set(); todo=['RT.BOOT']
while todo:
    u=todo.pop()
    if u in seen: continue
    seen.add(u); todo.extend(graph.get(u,[]))
unreach=sorted(canonical_routes-seen)
add('ROUTE.REACHABLE_FROM_BOOT',not unreach,'ROUTE_GRAPH',f'Unreachable canonical routes from RT.BOOT={unreach}.')

# Namespace integrity across operative semantic files.
semantic_paths=list(FILES.values())
rt_refs=defaultdict(list); cog_refs=defaultdict(list)
for p in semantic_paths:
    txt=p.read_text(encoding='utf-8',errors='replace')
    for m in re.finditer(r'\bRT\.[A-Z0-9_]+\b',txt): rt_refs[m.group()].append((p,m.start()))
    for m in re.finditer(r'\bCOG\.[A-Z0-9_]+\b',txt): cog_refs[m.group()].append((p,m.start()))
extra_rt=sorted(set(rt_refs)-canonical_routes)
add('ROUTE.NAMESPACE_NO_UNDECLARED_RT',not extra_rt,'ROUTE_GRAPH',f'Undeclared RT.* references={extra_rt}.',evidence=[x[0].relative_to(ROOT).as_posix() for r in extra_rt for x in rt_refs[r][:1]])

# Canonical COG routes.
mii_sec=core.split('Patch marker: AIR_MII_COGNITIVE_ARCHITECTURE_V1',1)[1].split('MII SEMANTIC TRANSLATION AND FIDELITY LAW',1)[0]
canonical_cog=set(re.findall(r'\bCOG\.[A-Z0-9_]+\b',mii_sec))
expected_cog={'COG.KNOWLEDGE_TO_EXECUTION','COG.MULTI_LENS','COG.CAUSAL_COUNTERFACTUAL','COG.RISK_PROPAGATION','COG.ADVERSARIAL_DISCONFIRMATION','COG.DECISION_TRADEOFF','COG.UNCERTAINTY_FUSION','COG.TEMPORAL_SYSTEM_DYNAMICS','COG.INFORMATION_GAIN','COG.EVIDENCE_TRIANGULATION'}
add('MII.COG_ROUTE_SET',canonical_cog==expected_cog,'MII',f'Canonical COG route set size={len(canonical_cog)} and matches expected 10.')
extra_cog=sorted(set(cog_refs)-canonical_cog)
add('MII.COG_NAMESPACE_NO_UNDECLARED',not extra_cog,'MII',f'Undeclared COG.* references={extra_cog}.')

# Formal object registry.
reg_sec=core.split('Canonical formal object classes:',1)[1].split('record_class identifies semantic object identity',1)[0]
registry={m.group(1):m.group(2) for m in re.finditer(r'^- (AIR_[A-Z0-9_]+): ([A-Z0-9_]+)$',reg_sec,re.M)}
expected_registry={
'AIR_RUNTIME_BRIDGE':'STATE_TRANSITION_RECORD','AIR_SESSION':'SESSION_STATE_RECORD','AIR_PROJECT_INITIALIZATION_BRIEF':'PROJECT_STATE_RECORD','AIR_PROJECT_EXECUTION_MAP':'PROJECT_STATE_RECORD','AIR_ARTIFACT':'ACTIVE_EXECUTION_RECORD','AIR_ACTIVE_CONTRACT':'EXECUTION_CONTRACT','AIR_GATE':'DECISION_RECORD','AIR_VALIDATION_REPORT':'VALIDATION_RECORD','AIR_ALIGNMENT_CHECK':'ALIGNMENT_EVALUATION_RECORD','AIR_ERROR':'ERROR_RECORD','AIR_ACTION_AUTHORIZATION':'ACTION_AUTHORIZATION_RECORD','AIR_ACTION_RECEIPT':'ACTION_RECEIPT_RECORD','AIR_PRIOR_EFFECT_RECORD':'RECOVERY_RECORD','AIR_REQUIRED_INPUT_REQUEST':'REQUIRED_INPUT_REQUEST_RECORD','AIR_HANDOFF_CARD':'TRANSFER_RECORD'}
add('OBJECT.REGISTRY_EXACT',registry==expected_registry,'FORMAL_OBJECTS',f'Core registry entries={len(registry)}; exact expected mapping={registry==expected_registry}.')
add('OBJECT.NO_OLD_ALIGNMENT_CLASS',all('ALIGNMENT_WATCHDOG_RECORD' not in p.read_text(encoding='utf-8',errors='replace') for p in semantic_paths),'FORMAL_OBJECTS','No operative semantic candidate file uses retired ALIGNMENT_WATCHDOG_RECORD.')
add('OBJECT.REQUIRED_INPUT_CLASS_STARTER','REQUIRED_INPUT_REQUEST_RECORD' in FILES['foundation.starter'].read_text(encoding='utf-8'),'FORMAL_OBJECTS','Starter references Core REQUIRED_INPUT_REQUEST_RECORD.')

# Alignment constructor dependency graph checks.
exempt={'AIR_ALIGNMENT_CHECK','AIR_VALIDATION_REPORT'}
formal=set(registry)
formal_producers=[]
for r in rm_routes:
    prods=set(r.get('produces',[])) & formal
    if prods: formal_producers.append((r['route_id'],prods,r))
for rid,prods,r in formal_producers:
    nonex=prods-exempt
    if not nonex: continue
    # Handoff's explicit generation evaluation is accepted as a route-specific evaluation dependency.
    eval_dep=('DEP.CURRENT_EVALUATION_BASIS' in r.get('requires',[]) or 'DEP.HANDOFF_GENERATION_EVALUATION' in r.get('requires',[]))
    add(f'ALIGN.CONSTRUCTOR_BASIS.{rid}',eval_dep,'ALIGNMENT_DEPENDENCY',f'{rid} produces non-exempt formal objects {sorted(nonex)}; requires={r.get("requires",[])}.')
# Explicit boot/activation construction reachability.
activate=rm_by['RT.ACTIVATE']
add('ALIGN.ACTIVATE_REQUIRES_EVALUATION_BASIS','DEP.CURRENT_EVALUATION_BASIS' in activate.get('requires',[]),'ALIGNMENT_DEPENDENCY',f'RT.ACTIVATE produces AIR_RUNTIME_BRIDGE/AIR_SESSION/AIR_ARTIFACT but requires={activate.get("requires")}.')
# Uncertainty request can be entered from onboarding before any RT.ALIGN; route must carry a basis or explicit alignment-failure exception.
unc=rm_by['RT.UNCERTAINTY_RESOLVE']
add('ALIGN.UNCERTAINTY_REQUIRED_INPUT_HAS_BASIS','DEP.CURRENT_EVALUATION_BASIS' in unc.get('requires',[]),'ALIGNMENT_DEPENDENCY',f'RT.UNCERTAINTY_RESOLVE produces AIR_REQUIRED_INPUT_REQUEST but requires={unc.get("requires")}.')
# Post-effect receipt must occur only after a new post-effect alignment because RT.ACTION invalidates pre-effect basis.
action=rm_by['RT.ACTION']; receipt=rm_by['RT.RECEIPT']
post_align_edge=(action.get('alignment_interlock')=='RT.ALIGN' and action.get('alignment_profile')=='POST_MATERIAL_EFFECT' and action.get('alignment_interlock_point')=='POST_EFFECT_PRE_NEXT')
add('ACTION.POST_EFFECT_ALIGNMENT_REACHABLE_BEFORE_RECEIPT',post_align_edge,'ACTION_ORDER',f'RT.ACTION post-effect alignment interlock={action.get("alignment_interlock")}, profile={action.get("alignment_profile")}, point={action.get("alignment_interlock_point")}; allowed_next={action.get("allowed_next_routes")}.')
add('ACTION.RECEIPT_REQUIRES_CURRENT_EVALUATION_BASIS','DEP.CURRENT_EVALUATION_BASIS' in receipt.get('requires',[]),'ACTION_ORDER',f'RT.RECEIPT produces AIR_ACTION_RECEIPT after pre-effect basis invalidation but requires={receipt.get("requires")}.')
# State transition reevaluation after artifact amendment.
amend=rm_by['RT.AMEND']
add('ALIGN.AMEND_REEVALUATION_EDGE',amend.get('alignment_interlock')=='RT.ALIGN' and amend.get('alignment_profile')=='STATE_TRANSITION' and amend.get('alignment_interlock_point')=='POST_TRANSITION_PRE_NEXT','ALIGNMENT_DEPENDENCY',f'RT.AMEND invalidates prior evaluation basis; alignment_interlock={amend.get("alignment_interlock")}, profile={amend.get("alignment_profile")}, point={amend.get("alignment_interlock_point")}.')
# Handoff restore should explicitly support HANDOFF_RESTORE evaluation before activate; accept only if RT.ALIGN edge exists or ACTIVATE requires current basis.
hr=rm_by['RT.HANDOFF_RESTORE']
restore_alignment=(hr.get('alignment_interlock')=='RT.ALIGN' and hr.get('alignment_profile')=='HANDOFF_RESTORE' and hr.get('alignment_interlock_point')=='POST_RESTORE_PRE_NEXT' and 'DEP.CURRENT_EVALUATION_BASIS' in activate.get('requires',[]))
add('ALIGN.HANDOFF_RESTORE_EVALUATION_REACHABLE',restore_alignment,'ALIGNMENT_DEPENDENCY',f'RT.HANDOFF_RESTORE alignment_interlock={hr.get("alignment_interlock")}, profile={hr.get("alignment_profile")}, point={hr.get("alignment_interlock_point")}; RT.ACTIVATE requires={activate.get("requires")}.')

# Action/delivery positive ordering checks.
for dep in ['DEP.CURRENT_EVALUATION_BASIS','DEP.ARTIFACT_BOUND','DEP.LEASE_ACTIVE','DEP.SCOPE_MATCH','DEP.APPROVAL_CURRENT','DEP.GATE_ALLOW']:
    add(f'ACTION.REQUIRES.{dep}',dep in action.get('requires',[]),'ACTION_ORDER',f'RT.ACTION requires {dep}.')
add('ACTION.NEXT_RECEIPT_ONLY',action.get('allowed_next_routes')==['RT.RECEIPT'],'ACTION_ORDER',f'RT.ACTION allowed_next={action.get("allowed_next_routes")}.')
for dep in ['DEP.MATCHING_AUTHORIZATION','DEP.OBSERVED_EFFECT_EVIDENCE']:
    add(f'RECEIPT.REQUIRES.{dep}',dep in receipt.get('requires',[]),'ACTION_ORDER',f'RT.RECEIPT requires {dep}.')
deliver=rm_by['RT.DELIVER']
for dep in ['DEP.OUTPUT_REVIEW','DEP.SEMANTIC_FIDELITY_RECONCILED','DEP.EPISTEMIC_SUFFICIENCY','DEP.CLOSURE_DELIVERY_GATE']:
    add(f'DELIVER.REQUIRES.{dep}',dep in deliver.get('requires',[]),'DELIVERY_ORDER',f'RT.DELIVER requires {dep}.')
for db in ['AIR_GATE','BENCHMARK_JUDGE','AIR-FLOOR-022']:
    add(f'DELIVER.NO_BYPASS.{db}',db in deliver.get('does_not_bypass',[]),'DELIVERY_ORDER',f'RT.DELIVER does_not_bypass contains {db}.')

# Q1 entry/answer separation.
add('Q1.ENTRY_SEPARATION_MARKER','AIR_ENTRY_PATH_Q1_SEPARATION_V1' in core,'ONBOARDING','Core contains entry/Q1 separation marker.')
add('Q1.START_PHRASE_LEAVES_UNANSWERED','This sets only entry_path. It leaves Q1 = UNANSWERED' in core,'ONBOARDING','Fresh-start entry phrase sets entry path only and leaves Q1 unanswered.')
add('Q1.STARTER_UNCERTAINTY_ROUTE','RT.UNCERTAINTY_RESOLVE' in FILES['foundation.starter'].read_text(encoding='utf-8'),'ONBOARDING','Starter routes unresolved material intent through Core uncertainty resolution.')

# Floor registry.
floor_names={int(m.group(1)):m.group(0).split(':',1)[0][2:] for m in re.finditer(r'^- AIR-FLOOR-(\d{3})-[A-Z0-9-]+:',core,re.M)}
add('FLOOR.REGISTRY_CONTIGUOUS_001_024',set(floor_names)==set(range(1,25)),'FLOOR_REGISTRY',f'Core named floor slots={sorted(floor_names)}.')
for num,name in {
21:'AIR-FLOOR-021-CURRENT-ALIGNMENT-EVALUATION-DEPENDENCY',22:'AIR-FLOOR-022-SEMANTIC-INTENT-AND-CONTEXT-FIDELITY',23:'AIR-FLOOR-023-EPISTEMIC-SUFFICIENCY-AND-CLARIFICATION',24:'AIR-FLOOR-024-COGNITIVE-CONTRIBUTION-NONAUTHORITY-AND-BENCHMARK-COMPILATION'}.items():
    add(f'FLOOR.{num}.EXACT',name in core,'FLOOR_REGISTRY',f'Core contains exact {name}.')
    add(f'FLOOR.{num}.GOV',name in gov,'FLOOR_REGISTRY',f'Governance contains exact {name}.')

# Handoff schema, migration and startup discovery.
handoff_root=handoff.get('AIR_HANDOFF_CARD',handoff)
add('HANDOFF.SCHEMA_2_3_0',handoff_root.get('SCHEMA_VERSION')=='2.3.0' and handoff_root.get('schema_version')=='2.3.0','HANDOFF',f'Handoff schema versions: SCHEMA_VERSION={handoff_root.get("SCHEMA_VERSION")}, schema_version={handoff_root.get("schema_version")}.')
htxt=FILES['foundation.handoff'].read_text(encoding='utf-8')
add('HANDOFF.NO_OPERATIVE_CADENCE','alignment_check_interval_user_messages' not in htxt,'HANDOFF','No cadence interval carrier remains in Handoff 2.3.0.')
add('HANDOFF.RUNTIME_ALIGNMENT_STATE','runtime_alignment_state' in htxt,'HANDOFF','Handoff serializes runtime_alignment_state.')
add('HANDOFF.ROUTE_MAP_STARTUP','AIR_RUNTIME_ROUTE_MAP.json' in htxt,'HANDOFF','Handoff recommends Runtime Route Map as startup discovery input.')
add('HANDOFF.SPECIALIST_INDEX_STARTUP','AIR_SPECIALIST_PACKAGE_INDEX.json' in htxt,'HANDOFF','Handoff preserves Specialist Index startup discovery input.')
add('HANDOFF.STRICT_SERIALIZATION_NOT_BYPASS','serialization exception only' in core.lower() or 'serialization-only exception' in core.lower(),'HANDOFF','Core states strict handoff is serialization-only exception.')

# Evidence/presentation separation and legacy terms only in explicitly historical/migration contexts.
for key in ['foundation.core','foundation.control','foundation.gov']:
    txt=FILES[key].read_text(encoding='utf-8')
    add(f'EVIDENCE.NO_SUMMARY_ONLY.{key}','SUMMARY_ONLY' not in txt,'EVIDENCE_PRESENTATION',f'{key} has no SUMMARY_ONLY token.')
    add(f'EVIDENCE.NO_FULL_TEST_EVIDENCE.{key}','FULL_TEST_EVIDENCE' not in txt,'EVIDENCE_PRESENTATION',f'{key} has no FULL_TEST_EVIDENCE token.')
add('EVIDENCE.CORE_STANDARD_MODE','STANDARD_EVIDENCE_PRESENTATION' in core and 'EXPANDED_EVIDENCE_PRESENTATION' in core,'EVIDENCE_PRESENTATION','Core defines standard/expanded presentation modes.')
add('EVIDENCE.CONTROL_PRESENTATION_ONLY','presentation' in control.lower() and 'evidence' in control.lower(),'EVIDENCE_PRESENTATION','Control evidence toggle is framed as presentation behavior.')

def legacy_tokens_outside_history(obj,path=''):
    bad=[]
    if isinstance(obj,dict):
        for k,v in obj.items():
            p=f'{path}.{k}' if path else k
            bad.extend(legacy_tokens_outside_history(v,p))
    elif isinstance(obj,list):
        for i,v in enumerate(obj): bad.extend(legacy_tokens_outside_history(v,f'{path}[{i}]'))
    elif isinstance(obj,str) and ('SUMMARY_ONLY' in obj or 'FULL_TEST_EVIDENCE' in obj):
        low=path.lower()
        allowed=any(t in low for t in ['amendment_history','migration','historical','source_baseline','legacy'])
        if not allowed: bad.append((path,obj[:180]))
    return bad
for key,p in FILES.items():
    if p.suffix!='.json': continue
    d=strict_load(p); bad=legacy_tokens_outside_history(d)
    add(f'EVIDENCE.LEGACY_TOKENS_CONTEXT.{key}',not bad,'EVIDENCE_PRESENTATION',f'{key}: legacy SUMMARY/FULL token uses outside explicit history/migration={bad[:3]}')

# Specialist manifests and component integrity.
package_specs={
 'cea':(FILES['cea.manifest'], ROOT/'specialists/capability-ecology'),
 'grounding':(FILES['grounding.manifest'], ROOT/'specialists/grounding'),
 'sfv':(FILES['sfv.manifest'], ROOT/'specialists/sfv'),
 'aigov':(FILES['aigov.manifest'], ROOT/'specialists/ai-governance'),
}
manifests={}
manifest_hashes={}
for pkg,(mp,dirp) in package_specs.items():
    m=strict_load(mp); manifests[pkg]=m; manifest_hashes[pkg]=sha(mp)
    add(f'PKG.VERSION.{pkg}',m.get('PACKAGE_VERSION')=='2.4.0','PACKAGE_INTEGRITY',f'{pkg} package version={m.get("PACKAGE_VERSION")}; expected 2.4.0.')
    comps=m.get('components',[])
    declared_count=m.get('component_count',m.get('package_validation_state',{}).get('component_count',len(comps)))
    add(f'PKG.COMPONENT_COUNT.{pkg}',len(comps)==declared_count,'PACKAGE_INTEGRITY',f'{pkg} manifest components={len(comps)}, declared={declared_count}.')
    for comp in comps:
        fn=comp.get('filename'); cp=dirp/fn
        add(f'PKG.COMP_EXISTS.{pkg}.{fn}',cp.exists(),'PACKAGE_INTEGRITY',f'{pkg} component {fn} exists.')
        if cp.exists():
            for fld,actual in [('sha256',sha(cp)),('size_bytes',cp.stat().st_size),('line_count',line_count(cp))]:
                add(f'PKG.COMP_{fld.upper()}.{pkg}.{fn}',comp.get(fld)==actual,'PACKAGE_INTEGRITY',f'{pkg}/{fn} {fld}: manifest={comp.get(fld)!r}, actual={actual!r}.')
    # Foundation exact closure.
    ff={x['filename']:x for x in m.get('foundation_compatibility',{}).get('required_files',[])}
    add(f'PKG.FOUNDATION_COUNT.{pkg}',len(ff)==5,'CROSS_FOUNDATION',f'{pkg} foundation refs={len(ff)}; expected 5.')
    for fn,a in foundation_actual.items():
        e=ff.get(fn)
        add(f'PKG.FOUNDATION_PRESENT.{pkg}.{fn}',e is not None,'CROSS_FOUNDATION',f'{pkg} references {fn}.')
        if e:
            for fld in ['sha256','size_bytes','line_count','designation','version','class']:
                add(f'PKG.FOUNDATION_{fld.upper()}.{pkg}.{fn}',e.get(fld)==a.get(fld),'CROSS_FOUNDATION',f'{pkg}/{fn} {fld}: manifest={e.get(fld)!r}, actual={a.get(fld)!r}.')
    reqfloors=set(m.get('foundation_compatibility',{}).get('required_floor_invariants',[]))
    for n in [21,22,23,24]:
        expected=[x for x in ['AIR-FLOOR-021-CURRENT-ALIGNMENT-EVALUATION-DEPENDENCY','AIR-FLOOR-022-SEMANTIC-INTENT-AND-CONTEXT-FIDELITY','AIR-FLOOR-023-EPISTEMIC-SUFFICIENCY-AND-CLARIFICATION','AIR-FLOOR-024-COGNITIVE-CONTRIBUTION-NONAUTHORITY-AND-BENCHMARK-COMPILATION'] if x.startswith(f'AIR-FLOOR-{n:03d}-')][0]
        add(f'PKG.FLOOR_{n}.{pkg}',expected in reqfloors,'CROSS_FOUNDATION',f'{pkg} requires {expected}.')
    # Authority boundary.
    ab=m.get('authority_boundary',{})
    for k in ['independent_execution_authority','active_execution_binding_authority']:
        if k in ab: add(f'PKG.NO_AUTHORITY.{pkg}.{k}',ab.get(k) is False,'AUTHORITY_BOUNDARY',f'{pkg} {k}={ab.get(k)!r}.')

# T12C mandatory Specialist internal dependency closure and operative lifecycle coherence.
# These checks close the validator gap exposed by the fresh-session Grounding bind refusal.
def _internal_refs(obj):
    refs=[]
    def walk(o,path=()):
        if isinstance(o,dict):
            fn=o.get('filename') or o.get('canonical_filename')
            if fn:
                for hk in ('sha256','observed_sha256'):
                    if hk in o and o.get(hk) is not None:
                        refs.append((fn,o.get(hk),'.'.join(map(str,path+(hk,)))))
            for k,v in o.items(): walk(v,path+(k,))
        elif isinstance(o,list):
            for i,v in enumerate(o): walk(v,path+(i,))
    walk(obj)
    return refs

expected_internal_edges={
 'cea':[
  ('AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json','AIR_DOMAIN_CAPABILITY_REGISTRY.json'),
  ('AIR_CAPABILITY_ECOLOGY_ARCHITECT.json','AIR_DOMAIN_CAPABILITY_REGISTRY.json'),
  ('AIR_CAPABILITY_ECOLOGY_ARCHITECT.json','AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json'),
  ('AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json','AIR_DOMAIN_CAPABILITY_REGISTRY.json'),
  ('AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json','AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json'),
  ('AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json','AIR_CAPABILITY_ECOLOGY_ARCHITECT.json')],
 'grounding':[
  ('AIR_GROUNDING_METHOD_PACK.json','AIR_GROUNDING_DOMAIN_PACKAGE.json'),
  ('AIR_GROUNDING_SPECIALIST.json','AIR_GROUNDING_DOMAIN_PACKAGE.json'),
  ('AIR_GROUNDING_SPECIALIST.json','AIR_GROUNDING_METHOD_PACK.json'),
  ('AIR_GROUNDING_EXECUTOR.json','AIR_GROUNDING_DOMAIN_PACKAGE.json'),
  ('AIR_GROUNDING_EXECUTOR.json','AIR_GROUNDING_METHOD_PACK.json'),
  ('AIR_GROUNDING_EXECUTOR.json','AIR_GROUNDING_SPECIALIST.json')],
 'sfv':[
  ('AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json','AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json'),
  ('AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json','AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json'),
  ('AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json','AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json'),
  ('AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json','AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json'),
  ('AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json','AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json'),
  ('AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json','AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json')],
 'aigov':[
  ('AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json','AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json'),
  ('AIR_AI_GOVERNANCE_SPECIALIST.json','AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json'),
  ('AIR_AI_GOVERNANCE_SPECIALIST.json','AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json'),
  ('AIR_AI_GOVERNANCE_METHOD_PACK.json','AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json'),
  ('AIR_AI_GOVERNANCE_METHOD_PACK.json','AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json'),
  ('AIR_AI_GOVERNANCE_METHOD_PACK.json','AIR_AI_GOVERNANCE_SPECIALIST.json'),
  ('AIR_AI_GOVERNANCE_EXECUTOR.json','AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json'),
  ('AIR_AI_GOVERNANCE_EXECUTOR.json','AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json'),
  ('AIR_AI_GOVERNANCE_EXECUTOR.json','AIR_AI_GOVERNANCE_SPECIALIST.json'),
  ('AIR_AI_GOVERNANCE_EXECUTOR.json','AIR_AI_GOVERNANCE_METHOD_PACK.json')]
}
expected_edge_count=sum(len(v) for v in expected_internal_edges.values())
add('PKG.INTERNAL_EDGE_EXPECTED_COUNT',expected_edge_count==28,'PACKAGE_DEPENDENCY_CLOSURE',f'Canonical package-internal dependency edge count={expected_edge_count}; expected 28.')
stale_lifecycle_tokens=('CANDIDATE_SET_001','PENDING_T8','PENDING_T9','PENDING_T10','PENDING_SPECIALIST_INDEX_RESEAL')
for pkg,(mp,dirp) in package_specs.items():
    m=manifests[pkg]
    component_files=[x.get('filename') for x in m.get('components',[])]
    actual_hash={fn:sha(dirp/fn) for fn in component_files if fn and (dirp/fn).exists()}
    component_data={fn:strict_load(dirp/fn) for fn in component_files if fn and (dirp/fn).exists()}
    # Every canonical edge must be represented by a current exact hash-bearing reference.
    for src,tgt in expected_internal_edges[pkg]:
        refs=[(h,path) for fn,h,path in _internal_refs(component_data[src]) if fn==tgt]
        ok=any(h==actual_hash.get(tgt) for h,path in refs)
        add(f'PKG.INTERNAL_EDGE.{pkg}.{src}->{tgt}',ok,'PACKAGE_DEPENDENCY_CLOSURE',f'{pkg} {src}->{tgt}: actual target SHA={actual_hash.get(tgt)}; declared refs={refs}.')
    # Any package-internal hash-bearing reference must resolve to current bytes, not just the canonical edge list.
    for src,o in component_data.items():
        for tgt,h,path in _internal_refs(o):
            if tgt in actual_hash:
                add(f'PKG.INTERNAL_REF.{pkg}.{src}.{path}',h==actual_hash[tgt],'PACKAGE_DEPENDENCY_CLOSURE',f'{pkg} {src}:{path} -> {tgt}: declared={h}; actual={actual_hash[tgt]}.')
    # Current Foundation identity and lifecycle carriers must not retain overtaken set/stage state.
    for fn,o in list(component_data.items())+[(mp.name,m)]:
        fc=o.get('foundation_compatibility',{}) if isinstance(o,dict) else {}
        add(f'PKG.OPERATIVE_FOUNDATION_STATE.{pkg}.{fn}',fc.get('compatibility_state')=='ALIGNED_TO_AIR_2_5_0_OBJECT_CONTRACT_SET_003' and fc.get('foundation_candidate_set_identity')=='AIR_FOUNDATION_2_5_0_OBJECT_CONTRACT_SET_003','PACKAGE_LIFECYCLE_COHERENCE',f'{pkg}/{fn}: compatibility_state={fc.get("compatibility_state")!r}, identity={fc.get("foundation_candidate_set_identity")!r}.')
        status=str(o.get('STATUS',o.get('status','')))
        add(f'PKG.OPERATIVE_STATUS_CURRENT.{pkg}.{fn}',not any(tok in status for tok in stale_lifecycle_tokens),'PACKAGE_LIFECYCLE_COHERENCE',f'{pkg}/{fn}: current status={status!r}.')
    pvs=m.get('package_validation_state',{})
    if isinstance(pvs,dict) and pvs:
        cur=' | '.join(str(pvs.get(k,'')) for k in ('package_state','cross_file','regression'))
        add(f'PKG.OPERATIVE_VALIDATION_STATE_CURRENT.{pkg}',not any(tok in cur for tok in stale_lifecycle_tokens),'PACKAGE_LIFECYCLE_COHERENCE',f'{pkg} current package validation carriers={cur!r}.')

# Index package closure.
idx_entries={e['package_identity']:e for e in index.get('entries',[])}
expected_pkg_ids={
 'cea':'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2','grounding':'AIR_GROUNDING_SPECIALIST_PACKAGE_V2','sfv':'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2','aigov':'AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_V2'}
add('INDEX.ENTRY_COUNT',len(index.get('entries',[]))==4,'INDEX_CLOSURE',f'Index entry count={len(index.get("entries",[]))}; expected 4.')
for pkg,pid in expected_pkg_ids.items():
    e=idx_entries.get(pid); m=manifests[pkg]
    add(f'INDEX.ENTRY_PRESENT.{pkg}',e is not None,'INDEX_CLOSURE',f'Index contains {pid}.')
    if e:
        add(f'INDEX.MANIFEST_HASH.{pkg}',e.get('manifest_sha256')==manifest_hashes[pkg],'INDEX_CLOSURE',f'{pkg} Index manifest SHA={e.get("manifest_sha256")}; actual={manifest_hashes[pkg]}.')
        add(f'INDEX.PACKAGE_VERSION.{pkg}',e.get('package_version')==m.get('PACKAGE_VERSION'),'INDEX_CLOSURE',f'{pkg} Index version={e.get("package_version")}; manifest={m.get("PACKAGE_VERSION")}.')
        manifest_fns=[x.get('filename') for x in m.get('components',[])]
        add(f'INDEX.COMPONENT_FILENAMES.{pkg}',e.get('canonical_component_filenames')==manifest_fns,'INDEX_CLOSURE',f'{pkg} Index component filenames match manifest load list.')
        add(f'INDEX.FOUNDATION_ID.{pkg}',e.get('foundation_compatibility_identity')=='AIR_FOUNDATION_2_5_0_OBJECT_CONTRACT_SET_003','INDEX_CLOSURE',f'{pkg} Index Foundation identity={e.get("foundation_compatibility_identity")}.')

# Index authority boundary.
iab=index.get('authority_boundary',{})
for k in ['execution_authority','binding_authority','selection_authority','approval_authority','cognitive_route_selection_authority','mii_fusion_authority']:
    add(f'INDEX.NO_AUTHORITY.{k}',iab.get(k)=='NONE','AUTHORITY_BOUNDARY',f'Index {k}={iab.get(k)!r}; expected NONE.')

# Route Map identity across package manifests.
actual_rm_hash=sha(FILES['foundation.route_map'])
for pkg,m in manifests.items():
    txt=json.dumps(m,sort_keys=True)
    add(f'PKG.ROUTE_MAP_HASH.{pkg}',actual_rm_hash in txt,'CROSS_FOUNDATION',f'{pkg} records current Route Map SHA {actual_rm_hash}.')

# MII contribution / semantic / epistemic / morphology contracts.
for pkg,m in manifests.items():
    txt=json.dumps(m,sort_keys=True)
    add(f'MII.CORE_COG_OWNER.{pkg}','RT.COGNITIVE_RESOLVE' in txt,'MII',f'{pkg} references Core RT.COGNITIVE_RESOLVE.')
    add(f'MII.CONTRIBUTION_NONAUTHORITY.{pkg}','AIR-FLOOR-024-COGNITIVE-CONTRIBUTION-NONAUTHORITY-AND-BENCHMARK-COMPILATION' in txt,'MII',f'{pkg} binds MII contribution nonauthority to Floor 024.')
    add(f'SEMANTIC.FIDELITY.{pkg}','AIR-FLOOR-022-SEMANTIC-INTENT-AND-CONTEXT-FIDELITY' in txt,'SEMANTIC_FIDELITY',f'{pkg} binds semantic fidelity to Floor 022.')
    add(f'EPISTEMIC.FLOOR.{pkg}','AIR-FLOOR-023-EPISTEMIC-SUFFICIENCY-AND-CLARIFICATION' in txt,'EPISTEMIC_SUFFICIENCY',f'{pkg} binds epistemic sufficiency to Floor 023.')
    add(f'EPISTEMIC.ROUTE.{pkg}','RT.UNCERTAINTY_RESOLVE' in txt,'EPISTEMIC_SUFFICIENCY',f'{pkg} routes material uncertainty through RT.UNCERTAINTY_RESOLVE.')
    add(f'MORPHOLOGY.CORE_OWNER.{pkg}','RT.MORPHOLOGY_BIND' in txt,'MORPHOLOGY',f'{pkg} recognizes Core morphology binding route.')

# Peer observed-hash validation evidence (non-runtime pins).
for pkg,m in manifests.items():
    txt=json.dumps(m)
    for peer,ph in manifest_hashes.items():
        if peer==pkg: continue
        # Only assert if the exact peer package identity or hash is present as observed context.
        if ph in txt:
            add(f'PEER.OBSERVED_HASH_VALID.{pkg}.{peer}',True,'CROSS_SPECIALIST',f'{pkg} observed peer hash for {peer} matches current final manifest {ph}.')

# Stale route-owner/version references in operative current fields.
# Exact AIR_CORE_RUNTIME_2_4_6 is not valid as a current router owner in 2.5.0; source/history metadata strings are handled separately.
stale=[]
for key,p in FILES.items():
    if p.suffix!='.json': continue
    try:d=strict_load(p)
    except:continue
    def walk(o,path=''):
        if isinstance(o,dict):
            for k,v in o.items():
                np=f'{path}.{k}' if path else k
                if isinstance(v,str) and ('owner' in k.lower() or 'router' in k.lower()) and ('2_4_6' in v or '2.4.6' in v):
                    stale.append((key,np,v))
                walk(v,np)
        elif isinstance(o,list):
            for i,v in enumerate(o): walk(v,f'{path}[{i}]')
    walk(d)
add('STALE.NO_2_4_6_ROUTE_OWNER',not stale,'STALE_REFERENCE',f'Stale 2.4.6 owner/router references={stale}.')

# Semantic route references must all resolve to canonical route IDs; this is intentionally separate from route-map-only check.
# Already checked extra_rt; preserve as cross-system gate.
add('CROSS_SYSTEM.ROUTE_REFERENCE_CLOSURE',not extra_rt,'CROSS_SYSTEM',f'All RT.* references across 28 semantic files resolve to the 21-route registry. Extras={extra_rt}.')

# Evidence modes in current contract exact values.
for pkg,m in manifests.items():
    te=m.get('test_evidence_contract',{})
    if te:
        add(f'EVIDENCE.DEFAULT_PRESENTATION.{pkg}',te.get('default_presentation_mode')=='STANDARD_EVIDENCE_PRESENTATION','EVIDENCE_PRESENTATION',f'{pkg} default_presentation_mode={te.get("default_presentation_mode")!r}.')
        add(f'EVIDENCE.PRESENTATION_ONLY_RULE.{pkg}',bool(te.get('presentation_only_rule')),'EVIDENCE_PRESENTATION',f'{pkg} carries presentation_only_rule.')

# Stage-local status metadata: warn when it names already-completed predecessor checkpoints. This is not treated as semantic authority failure by itself.
stage_warnings=[]
for key,p in FILES.items():
    if p.suffix!='.json' or not any(key.startswith(x) for x in ['cea.','grounding.','sfv.','aigov.']): continue
    txt=p.read_text(encoding='utf-8')
    if 'PENDING_SPECIALIST_INDEX_RESEAL' in txt:
        stage_warnings.append((key,'PENDING_SPECIALIST_INDEX_RESEAL'))
    if 'PENDING_T9_T10' in txt or 'PENDING_T10_AND' in txt or 'PENDING_CROSS_SPECIALIST' in txt:
        stage_warnings.append((key,'EARLIER_STAGE_PENDING_MARKER'))
add('STATUS.STAGE_LOCAL_PENDING_MARKERS',not stage_warnings,'STATUS_METADATA',f'Stage-local checkpoint status markers now overtaken by later completed stages={stage_warnings[:20]}.',severity='WARNING')

# Full-system hash inventory.
inventory=[]
for key,p in sorted(FILES.items()):
    inventory.append({'logical_id':key,'filename':p.name,'sha256':sha(p),'size_bytes':p.stat().st_size,'line_count':line_count(p),'source_path':p.relative_to(ROOT).as_posix()})

# Count and decision.
failed=[c for c in checks if c['status']=='FAIL']
warned=[c for c in checks if c['status']=='WARN']
passed=[c for c in checks if c['status']=='PASS']
decision='PASS_STATIC_OBJECT_CONTRACT_CLOSURE_VALIDATED_PENDING_FRESH_BEHAVIORAL' if not failed else 'FAIL_STATIC_BLOCKED_PENDING_PATCH_AND_REVALIDATION'
report={
 'AIR_VALIDATION_REPORT':{
   'report_id':'AIR-VAL-AIR250-OBJECT-CONTRACT-FULL-STATIC-001',
   'object_version':'2.0.0',
   'record_class':'VALIDATION_RECORD',
   'validated_target':'AIR 2.5.0 integrated Foundation + Route Map + four Specialist packages + Specialist Package Index candidate graph',
   'candidate_set_identity':'AIR_2_5_0_OBJECT_CONTRACT_INTEGRATED_STATIC_SET_005',
   'validation_kind':'REPRODUCIBLE_EXECUTABLE_STATIC_ANALYSIS',
   'evidence_class':'TOOL_OBSERVED_GOVERNANCE_RECORD',
   'decision':decision,
   'summary':{'total':len(checks),'passed':len(passed),'failed':len(failed),'warnings':len(warned)},
   'failed_check_ids':[c['check_id'] for c in failed],
   'warning_check_ids':[c['check_id'] for c in warned],
   'checks':checks,
   'material_findings':[c for c in failed],
   'warnings':[c for c in warned],
   'limitations':[
      'Static validation evaluates the supplied prompt/package bytes and declared graph/contracts; it is not fresh-host behavioral evidence.',
      'Prior stage PASS evidence is preserved from earlier integrated validation records and is not treated as a substitute for this Object Contract Closure rerun.',
      'Object Contract Closure preserves the repaired Foundation consistency baseline, closes formal-object ownership/schema defects, and revalidates downstream exact-hash closure. Fresh behavioral evidence remains a separate release consideration.'
   ],
   'known_out_of_scope_findings':[
      'FRESH_BEHAVIORAL_RELEASE_VALIDATION_NOT_EXECUTED: static repair validation does not establish fresh-host behavioral release readiness.'
   ],
   'next_required_state':'PATCH_BLOCKING_STATIC_DEFECTS_THEN_RERUN_FULL_STATIC' if failed else 'FRESH_BEHAVIORAL_RELEASE_VALIDATION',
   'runtime_origin':'TOOL_OBSERVED',
   'backend_validation_claimed':False,
   'hidden_reasoning_claimed':False
 }
}
report_path=OUT/'AIR_2.5.0_FULL_CROSS_SYSTEM_STATIC_VALIDATION.json'
report_path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
inv_path=OUT/'AIR_2.5.0_INTEGRATED_CANDIDATE_INVENTORY.json'
inv_obj={'candidate_set_identity':'AIR_2_5_0_OBJECT_CONTRACT_INTEGRATED_STATIC_SET_005','semantic_file_count':len(inventory),'files':inventory,'validation_report_filename':report_path.name,'validation_report_sha256':sha(report_path)}
inv_path.write_text(json.dumps(inv_obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')

# Receipt for validation action (validation execution can succeed even if candidate fails).
receipt={
 'AIR_ACTION_RECEIPT':{
  'receipt_id':'RECEIPT-AIR250-OBJECT-CONTRACT-FULL-STATIC-001',
  'object_version':'2.0.0','record_class':'ACTION_RECEIPT_RECORD','authorization_ref':'AUTH-AIR250-OBJECT-CONTRACT-CLOSURE-001',
  'action_attempted':'AIR_2_5_0_FULL_CROSS_SYSTEM_STATIC_VALIDATION',
  'result':'SUCCESS_VALIDATION_COMPLETED',
  'validation_report_ref':'AIR-VAL-AIR250-OBJECT-CONTRACT-FULL-STATIC-001',
  'validation_decision':decision,
  'validation_counts':report['AIR_VALIDATION_REPORT']['summary'],
  'candidate_bytes_mutated':False,
  'behavioral_regression_executed':False,
  'public_repository_mutated':False,
  'next_required_state':report['AIR_VALIDATION_REPORT']['next_required_state'],
  'runtime_origin':'TOOL_OBSERVED','backend_validation_claimed':False,'hidden_reasoning_claimed':False
 }
}
receipt_path=OUT/'AIR_2.5.0_FULL_STATIC_TRANSACTION_RECEIPT.json'
receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')

# Human-readable concise defect map.
defect_path=OUT/'AIR_2.5.0_FULL_STATIC_DEFECT_MAP.md'
lines=['# AIR 2.5.0 Object Contract Closure — Full Cross-System Static Validation Defect Map','',f'Decision: **{decision}**',f'Checks: {len(passed)} PASS / {len(failed)} FAIL / {len(warned)} WARN ({len(checks)} total)','']
if failed:
    lines += ['## Blocking findings','']
    for c in failed:
        lines += [f'- `{c["check_id"]}` — {c["detail"]}']
else:
    lines += ['No blocking findings in the implemented Object Contract Closure static checkset.', '', 'The prior Foundation consistency defects remain closed and the Object Contract Closure checks pass. Fresh behavioral evidence remains a separate release consideration.']
if warned:
    lines += ['', '## Warnings','']
    for c in warned: lines += [f'- `{c["check_id"]}` — {c["detail"]}']
lines += ['', 'No candidate source/component/manifest/index bytes were modified by this validation.']
defect_path.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')

# Create integrated checkpoint bundle with semantic candidates copied under canonical-ish layout plus reports.
bundle_root=ROOT/'bundle'
if bundle_root.exists(): shutil.rmtree(bundle_root)
(bundle_root/'foundation').mkdir(parents=True)
(bundle_root/'catalog').mkdir(parents=True)
(bundle_root/'specialists/capability-ecology').mkdir(parents=True)
(bundle_root/'specialists/grounding').mkdir(parents=True)
(bundle_root/'specialists/sfv').mkdir(parents=True)
(bundle_root/'specialists/ai-governance').mkdir(parents=True)
(bundle_root/'validation').mkdir(parents=True)
(bundle_root/'receipts').mkdir(parents=True)
# Preserve exact bytes, normalize distribution filenames only by copying.
copy_map={
 FILES['foundation.core']:bundle_root/'foundation/AIR_CORE_RUNTIME.md',
 FILES['foundation.control']:bundle_root/'foundation/AIR_CONTROL_SURFACE.md',
 FILES['foundation.gov']:bundle_root/'foundation/AIR_GOV.md',
 FILES['foundation.starter']:bundle_root/'foundation/AIR_DEFAULT_STARTER_PROFILE.json',
 FILES['foundation.handoff']:bundle_root/'foundation/AIR_HANDOFF_CARD_TEMPLATE.json',
 FILES['foundation.route_map']:bundle_root/'catalog/AIR_RUNTIME_ROUTE_MAP.json',
 FILES['catalog.specialist_index']:bundle_root/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',
}
for key,p in FILES.items():
    if key.startswith('cea.'): copy_map[p]=bundle_root/f'specialists/capability-ecology/{p.name}'
    elif key.startswith('grounding.'): copy_map[p]=bundle_root/f'specialists/grounding/{p.name}'
    elif key.startswith('sfv.'): copy_map[p]=bundle_root/f'specialists/sfv/{p.name}'
    elif key.startswith('aigov.'): copy_map[p]=bundle_root/f'specialists/ai-governance/{p.name}'
for src,dst in copy_map.items(): shutil.copy2(src,dst)
shutil.copy2(report_path,bundle_root/'validation'/report_path.name)
shutil.copy2(inv_path,bundle_root/'validation'/inv_path.name)
shutil.copy2(defect_path,bundle_root/'validation'/defect_path.name)
shutil.copy2(receipt_path,bundle_root/'receipts'/receipt_path.name)
zip_path=ROOT/'validation/AIR_2.5.0_OBJECT_CONTRACT_FULL_STATIC_VALIDATION_CHECKPOINT.zip'
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(bundle_root.rglob('*')):
        if p.is_file(): z.write(p,p.relative_to(bundle_root))

print(json.dumps({
 'decision':decision,'total':len(checks),'passed':len(passed),'failed':len(failed),'warnings':len(warned),
 'failed_ids':[c['check_id'] for c in failed],
 'warning_ids':[c['check_id'] for c in warned],
 'report':str(report_path),'inventory':str(inv_path),'defect_map':str(defect_path),'receipt':str(receipt_path),'bundle':str(zip_path),'bundle_sha256':sha(zip_path)
},indent=2))
