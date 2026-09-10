from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
class V(Exception): pass
def req(c,m):
    if not c: raise V(m)
def load(rel):
    def hook(pairs):
        d={}
        for k,v in pairs:
            if k in d: raise V(f'duplicate key {k} in {rel}')
            d[k]=v
        return d
    return json.loads((ROOT/rel).read_text(encoding='utf-8'),object_pairs_hook=hook)
REG='profiles/capability ecology architect/AIR_DOMAIN_CAPABILITY_REGISTRY.json'
TR='profiles/capability ecology architect/AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json'
ARCH='profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT.json'
MP='profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json'
CORE='prompts/AIR_CORE_RUNTIME.md'; STARTER='prompts/AIR_DEFAULT_STARTER_PROFILE.json'; HANDOFF='prompts/AIR_HANDOFF_CARD_TEMPLATE.json'
def path_preflight(cand,path,op):
    parts=path.split('.'); cur=cand
    for i,part in enumerate(parts):
        m=re.fullmatch(r'([^\[]+)\[([^\]]+)\]',part)
        if m:
            key=m.group(1); vals=m.group(2).split(',')
            req(isinstance(cur,dict) and key in cur,f'unresolved path {path}: {key}')
            arr=cur[key]; req(isinstance(arr,list),f'non-list bracket path {path}')
            for v in vals: req(v in arr,f'missing list item {v} in {path}')
            cur=arr; continue
        last=i==len(parts)-1
        if last and op=='ADD':
            req(isinstance(cur,dict),f'ADD parent non-object {path}'); req(part not in cur,f'ADD target already exists {path}'); return
        req(isinstance(cur,dict) and part in cur,f'unresolved path {path}: {part}'); cur=cur[part]
def _dupe(p,pairs):
    d={}
    for k,v in pairs:
        if k in d: raise V(f'duplicate key {k} in {p}')
        d[k]=v
    return d
def main():
    reg=load(REG); tr=load(TR); arch=load(ARCH); mp=load(MP); st=load(STARTER); h=load(HANDOFF); core=(ROOT/CORE).read_text(encoding='utf-8')
    canon=reg['detailed_domain_package_template']['required_fields']
    req(len(canon)==44 and len(set(canon))==44,'canonical Domain Package field set not 44 unique')
    req(reg['registry_schema']['required_domain_package_fields']==canon,'registry required fields diverge from canonical template')
    gold=reg['detailed_domain_fixture_suite']['golden_fixtures']; neg=reg['detailed_domain_fixture_suite']['negative_fixtures']
    req(len(gold)==9 and len(neg)==9,'fixture counts changed')
    for fx in gold:
        req(set(canon)<=set(fx['candidate_domain_package']),f'{fx["fixture_id"]}: missing canonical fields')
        req(fx['expected_validation'].get('required_template_fields_present') is True,f'{fx["fixture_id"]}: expected validation mismatch')
    rs=reg['registry_schema']; req('expected_validation_or_expected_decision' not in rs['fixture_wrapper_required_fields'],'pseudo-field remains')
    rc=rs['fixture_wrapper_result_field_contract']['cases']
    for fx in gold:
        req(fx['fixture_role']=='GOLDEN_DOMAIN_CONSTRUCTION_FIXTURE','gold role drift'); req(rc[fx['fixture_role']]['required_result_field']=='expected_validation','gold result contract'); req('expected_validation' in fx and 'expected_decision' not in fx,'gold expected result shape invalid')
    for fx in neg:
        req(fx['fixture_role']=='NEGATIVE_DOMAIN_CONSTRUCTION_FIXTURE','negative role drift'); req(rc[fx['fixture_role']]['required_result_field']=='expected_decision','negative result contract'); req('expected_decision' in fx and 'expected_validation' not in fx,'negative expected result shape invalid')
    byid={x['fixture_id']:x['candidate_domain_package'] for x in gold}
    for fx in neg:
        source=byid[fx['derived_from_golden_fixture_id']]
        for mut in fx['negative_mutations']: path_preflight(source,mut['path'],mut['operation'])
    req(sum(m['path']=='knowledge_dimensions.PROCEDURAL' for f in neg for m in f['negative_mutations'])==2,'expected two corrected PROCEDURAL paths')
    tro=tr['machine_native_translation_contract']['required_translation_outputs']; out=tr['output_artifact']['required_fields']
    req(len(tro)==29,'Translator required output count changed unexpectedly'); req(set(tro)<=set(out),f'Translator final output missing {set(tro)-set(out)}')
    proj=tr['output_artifact']['required_translation_output_projection']; req(set(proj)==set(tro),'Translator output projection coverage mismatch')
    for k in tro: req(proj[k]=={'path':f'$.{k}','required':True,'projection':'DIRECT_TOP_LEVEL_FIELD'},f'bad Translator projection {k}')
    cc=arch['detailed_domain_package_construction_contract']; req(cc['required_template_fields']==canon,'Architect required template fields diverge')
    dpout=tr['detailed_domain_package_contribution_contract']['required_outputs']; maps=cc['translator_to_canonical_package_mapping']['mappings']; req(set(maps)==set(dpout),'Architect Translator mapping coverage mismatch')
    roots=set(canon)
    for k,m in maps.items():
        req(m['target_path'].startswith('$.'),f'{k}: noncanonical target path'); root=m['target_path'][2:].split('.',1)[0]; req(root in roots,f'{k}: target root {root} outside canonical package schema'); req(m['operation'] in {'MERGE_OR_CREATE_DECLARED_SUBFIELD','MERGE_UNIQUE','MERGE_OBJECT'},f'{k}: unknown mapping operation')
    ids={x['step_id'] for x in mp['ordered_steps']}; req(ids=={f'M{i}' for i in range(13)},'ordered Method step IDs changed')
    for name,b in mp['branch_contracts'].items():
        for key in ('required_steps','optional_steps'): req(set(b.get(key,[]))<=ids,f'{name}.{key}: unresolved step refs {set(b.get(key,[]))-ids}')
    req('M4_WHEN_TRIGGERED' not in json.dumps(mp),'pseudo-step M4_WHEN_TRIGGERED remains')
    req('- AIR_METHOD_EVIDENCE_WAIVER: METHOD_EVIDENCE_WAIVER_RECORD' in core,'Core waiver formal object class missing'); req('AIR_METHOD_EVIDENCE_WAIVER allowed object-owned top-level fields:' in core,'Core waiver field law missing')
    for field in ['waiver_id','method_identity','method_version','step_id','waived_requirement','waiver_scope','artifact_scope_ref','permission_basis_type','permission_basis_ref','validity_state','claim_boundary']: req(f'- {field}' in core,f'Core waiver field missing {field}')
    req('METHOD_STEP_EVIDENCE_TO_ADVANCE_ONLY' in core,'Core waiver scope rule missing'); req('AIR_METHOD_EVIDENCE_WAIVER' in st['typed_registries']['formal_objects']['object_ids'],'Starter waiver object mirror missing')
    wc=mp['evidence_waiver_contract']; req(wc['formal_object']=='AIR_METHOD_EVIDENCE_WAIVER' and wc['positive_execution_authority']=='NONE','Method waiver authority mismatch'); req(wc['allowed_permission_basis_types']==['EXPLICIT_USER_APPROVAL'] and wc['method_policy_waiver_enabled'] is False,'Method waiver permission too broad')
    ms=mp['handoff_requirements']['method_specific_state_schema']['required_fields']; req('step_evidence_waiver_refs' in ms,'Method Handoff waiver refs not required')
    vr=h['AIR_HANDOFF_CARD']['schema_manifest']['validation_registry']; req('METHOD_EVIDENCE_WAIVER_REFS_VALID' in vr['allowed_operators'],'Handoff waiver validator operator missing')
    meth=vr['rules']['HC-VALIDATE-METHOD']; req(meth['operator']=='ALL','HC-VALIDATE-METHOD not compound validation'); predops={p['operator'] for p in meth['predicates']}; req({'ACTIVE_METHOD_PACK_HANDOFF_SCHEMA_VALID','METHOD_EVIDENCE_WAIVER_REFS_VALID'}<=predops,'Handoff Method waiver validation missing')
    req('Free text, generic approval' in mp['method_execution_contract']['completion_rule'],'Method completion rule does not reject untyped waiver')
    js=list(ROOT.glob('**/*.json')); req(len(js)==28,f'expected 28 JSON source files, got {len(js)}')
    for p in js: json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=lambda pairs,p=p:_dupe(p,pairs))
    print('R5 remediation validation: PASS'); print('r5_findings 7'); print('canonical_domain_package_fields',len(canon)); print('golden_fixtures',len(gold)); print('negative_mutation_paths',sum(len(f['negative_mutations']) for f in neg)); print('translator_required_outputs',len(tro)); print('translator_domain_mapping',len(maps)); print('method_branches',len(mp['branch_contracts'])); print('json_sources',len(js))
if __name__=='__main__':
    try: main()
    except (V,KeyError,TypeError,AssertionError) as e:
        print('R5 remediation validation: FAIL:',e,file=sys.stderr); raise SystemExit(1)
