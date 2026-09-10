from __future__ import annotations
import sys,json,re,hashlib,unicodedata
from urllib.parse import unquote
from pathlib import Path

class E(Exception): pass
def req(c,m):
    if not c: raise E(m)
def reject_dupes(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise E(f'duplicate JSON key: {k}')
        d[k]=v
    return d
def load(p):
    try: return json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=reject_dupes)
    except Exception as e:
        if isinstance(e,E): raise
        raise E(f'{p}: strict JSON parse failed: {e}')
def jget(o,path):
    req(path.startswith('$.'),f'bad path {path}')
    cur=o
    for part in path[2:].split('.'):
        if not isinstance(cur,dict) or part not in cur: raise KeyError(path)
        cur=cur[part]
    return cur
def header(text,key):
    m=re.search(rf'(?m)^{re.escape(key)}:\s*(\S+)\s*$',text)
    if not m: raise E(f'missing header {key}')
    return m.group(1)
def parse_routes(core):
    # Exact canonical markers only, never prose mentions.
    blocks=re.split(r'(?m)^\[AIR_ROUTE\]\s*$',core)
    req(len(blocks)-1==22,f'exact route marker count {len(blocks)-1} != 22')
    out={}
    for block in blocks[1:]:
        rec={}
        for line in block.splitlines():
            s=line.strip()
            if not s: continue
            if s.startswith('='): break
            if '=' in s:
                k,v=s.split('=',1); rec[k.strip()]=v.strip()
        req('id' in rec,'route block missing id')
        req(rec['id'] not in out,f'duplicate route {rec["id"]}')
        out[rec['id']]=rec
    req(len(out)==22,'route parse did not yield 22 unique routes')
    return out
def closed_det_set(core):
    m=re.search(r'Canonical deterministic runtime route set for this Foundation candidate:\n(?P<body>(?:- RT\.[A-Z_]+\n)+)\nThe route set is explicit and closed',core)
    req(bool(m),'closed deterministic set missing')
    return {ln[2:] for ln in m.group('body').strip().splitlines()}
def eval_registry(root,starter):
    core=(root/'prompts/AIR_CORE_RUNTIME.md').read_text(encoding='utf-8')
    dcr=starter['validation_contract']['deterministic_contract_registry']
    checks=dcr['checks']; cov=dcr['coverage_contract']
    req(cov['declared_check_count']==len(checks),'declared registry count mismatch')
    req(cov['implemented_check_count_required']==len(checks),'implemented-required count mismatch')
    req(cov['executed_check_count_required']==len(checks),'executed-required count mismatch')
    supported={'FILE_EXISTS','MARKDOWN_HEADER_EQUALS_LITERAL','MARKDOWN_FINAL_LINE_EQUALS_LITERAL','JSON_EQUALS_LITERAL','JSON_EQUALS_REFERENCE','JSON_EQUALS_MARKDOWN_HEADER','JSON_ROOT_KEYS_DECLARED_BY_MANIFEST','JSON_ARRAY_CONTAINS_LITERAL','JSON_PATH_ABSENT','JSON_SUBTREE_TEXT_NOT_CONTAINS_LITERAL','TEXT_CONTAINS_LITERAL','TEXT_NOT_CONTAINS_LITERAL','MARKDOWN_HEADER_EQUALS_REGISTRY_VALUE','STRICT_JSON_PARSE_NO_DUPLICATES','FOUNDATION_MANIFEST_EXACT','FOUNDATION_FILENAME_COLLISION_FREE'}
    ids=[]
    for c in checks:
        cid=c['check_id']; ids.append(cid); op=c['operator']
        req(op in supported,f'{cid}: unsupported operator {op}')
        req(c.get('on_failure')=='FAIL_CLOSED',f'{cid}: not fail closed')
        try:
            if op=='FILE_EXISTS': req((root/c['file']).is_file(),f'{cid}: missing file')
            elif op=='MARKDOWN_HEADER_EQUALS_LITERAL': req(header((root/c['file']).read_text(),c['header'])==c['expected'],f'{cid}: header mismatch')
            elif op=='MARKDOWN_HEADER_EQUALS_REGISTRY_VALUE':
                exp=jget(starter,c['registry_value_path']); got=header((root/c['file']).read_text(),c['header']); req(got==exp,f'{cid}: {got} != {exp}')
            elif op=='MARKDOWN_FINAL_LINE_EQUALS_LITERAL':
                lines=(root/c['file']).read_text().rstrip().splitlines(); req(lines and lines[-1]==c['expected'],f'{cid}: sentinel mismatch')
            elif op=='JSON_EQUALS_LITERAL': req(jget(load(root/c['left']['file']),c['left']['path'])==c['expected'],f'{cid}: JSON literal mismatch')
            elif op=='JSON_EQUALS_REFERENCE': req(jget(load(root/c['left']['file']),c['left']['path'])==jget(load(root/c['right']['file']),c['right']['path']),f'{cid}: JSON ref mismatch')
            elif op=='JSON_EQUALS_MARKDOWN_HEADER': req(jget(load(root/c['left']['file']),c['left']['path'])==header((root/c['right']['file']).read_text(),c['right']['header']),f'{cid}: JSON/header mismatch')
            elif op=='JSON_ROOT_KEYS_DECLARED_BY_MANIFEST':
                o=load(root/c['file']); ro=jget(o,c['root_path']); declared=set(jget(o,c['required_path']))|set(jget(o,c['optional_path'])); req(not(set(ro)-declared),f'{cid}: undeclared root')
            elif op=='JSON_ARRAY_CONTAINS_LITERAL': req(c['expected'] in jget(load(root/c['left']['file']),c['left']['path']),f'{cid}: missing array literal')
            elif op=='JSON_PATH_ABSENT':
                o=load(root/c['left']['file'])
                try:jget(o,c['left']['path']); exists=True
                except KeyError: exists=False
                req(not exists,f'{cid}: forbidden path present')
            elif op=='JSON_SUBTREE_TEXT_NOT_CONTAINS_LITERAL': req(c['expected'] not in json.dumps(jget(load(root/c['left']['file']),c['left']['path']),ensure_ascii=False),f'{cid}: forbidden text present')
            elif op=='TEXT_CONTAINS_LITERAL': req(c['expected'] in (root/c['file']).read_text(),f'{cid}: text missing')
            elif op=='TEXT_NOT_CONTAINS_LITERAL': req(c['expected'] not in (root/c['file']).read_text(),f'{cid}: forbidden text present')
            elif op=='STRICT_JSON_PARSE_NO_DUPLICATES': load(root/c['file'])
            elif op=='FOUNDATION_MANIFEST_EXACT':
                o=load(root/c['manifest_file']); arr=jget(o,c['manifest_path']); req(isinstance(arr,list) and len(arr)==5,f'{cid}: expected 5 roles')
                roles=[x['canonical_role'] for x in arr]; names=[x['canonical_filename'] for x in arr]
                req(len(set(roles))==5 and len(set(names))==5,f'{cid}: duplicate role/name')
                actual={p.name for p in (root/c['foundation_directory']).iterdir() if p.is_file() and p.suffix in {'.md','.json'}}
                req(actual==set(names),f'{cid}: active Foundation set mismatch {actual^set(names)}')
                for x in arr:
                    p=root/c['foundation_directory']/x['canonical_filename']; req(p.is_file(),f'{cid}: missing {p.name}')
                    if p.suffix=='.md': got=header(p.read_text(), 'SYSTEM_DESIGNATION'); exp=x['SYSTEM_DESIGNATION']
                    else:
                        obj=load(p)
                        if p.name=='AIR_HANDOFF_CARD_TEMPLATE.json': got=obj['AIR_HANDOFF_CARD']['TEMPLATE_DESIGNATION']; exp=x['TEMPLATE_DESIGNATION']
                        else: got=obj['SYSTEM_DESIGNATION']; exp=x['SYSTEM_DESIGNATION']
                    req(got==exp,f'{cid}: designation mismatch {p.name}')
            elif op=='FOUNDATION_FILENAME_COLLISION_FREE':
                arr=jget(load(root/c['manifest_file']),c['manifest_path']); names=[x['canonical_filename'] for x in arr]
                def norm(s): return unicodedata.normalize('NFKC',unquote(s)).casefold().rstrip(' .')
                vals=[norm(x) for x in names]; req(len(vals)==len(set(vals)),f'{cid}: normalized manifest collision')
                actual=[p.name for p in (root/'prompts').iterdir() if p.is_file() and p.suffix in {'.md','.json'}]
                vals=[norm(x) for x in actual]; req(len(vals)==len(set(vals)),f'{cid}: normalized active-folder collision')
        except (E, KeyError) as exc:
            msg=str(exc)
            if cid not in msg:
                raise E(f'{cid}: {msg}') from exc
            raise
    req(len(ids)==len(set(ids)),'duplicate deterministic check ids')
    return len(checks)
def main(root):
    core_p=root/'prompts/AIR_CORE_RUNTIME.md'; starter_p=root/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; control_p=root/'prompts/AIR_CONTROL_SURFACE.md'; rmap_p=root/'catalog/AIR_RUNTIME_ROUTE_MAP.json'
    core=core_p.read_text(encoding='utf-8'); control=control_p.read_text(encoding='utf-8'); starter=load(starter_p); rmap=load(rmap_p)
    routes=parse_routes(core)
    det_closed=closed_det_set(core)
    det_tagged={rid for rid,r in routes.items() if r.get('execution_semantics')=='DETERMINISTIC_PIPELINE'}
    det_starter=set(starter['compiler_contract']['deterministic_pipeline_non_inference']['declared_runtime_routes'])
    det_map=set(rmap['deterministic_pipeline_contract']['declared_route_ids'])
    req(det_closed==det_tagged==det_starter==det_map, f'deterministic sets diverge: closed={det_closed} tagged={det_tagged} starter={det_starter} map={det_map}')
    req('RT.APPROVAL_RESOLVE' in det_closed,'approval resolve missing deterministic set')
    events={e['route_id']:e for e in starter['compiler_contract']['runtime_control_event_registry']['events']}
    req(set(events)==set(routes),'event/route coverage mismatch')
    for rid in det_closed:
        r=routes[rid]; req(r.get('trigger_authority')=='NON_OPERATIVE_DESCRIPTION',f'{rid}: trigger authority')
        req(r.get('control_event_ref')==events[rid]['event_id'],f'{rid}: event ref mismatch')
    req(routes['RT.APPROVAL_RESOLVE']['control_event_ref']=='CE-RT-APPROVAL_RESOLVE','approval event id mismatch')
    # All route-bound evaluation profiles are typed.
    profiles=set(starter['typed_registries']['runtime_states']['alignment_evaluation_profile'])
    used=set()
    for r in routes.values():
        for k in ['alignment_profile','post_effect_alignment_profile','required_alignment_profile']:
            if r.get(k): used.add(r[k])
    req(used<=profiles,f'untyped alignment profiles {used-profiles}')
    req({'ACTIVATION','UNCERTAINTY_RESOLUTION'}<=profiles,'new canonical profile semantics missing')
    # Reachable pre-entry/bootstrap event guards.
    no_basis={'RT.BOOT','RT.ONBOARD','RT.HANDOFF_RESTORE','RT.ACTIVATE','RT.ALIGN','RT.UNCERTAINTY_RESOLVE','RT.RECOVERY'}
    for rid in no_basis:
        paths={g.get('path') for g in events[rid]['guards']}; req('CURRENT_EVALUATION_BASIS' not in paths,f'{rid}: current basis remains self/prior prerequisite')
    apaths={g.get('path') for g in events['RT.ALIGN']['guards']}; req({'CANONICAL_CURRENT_STATE','REQUESTED_ALIGNMENT_PROFILE'}<=apaths,'ALIGN input guards incomplete')
    # Conditional approval contract.
    ar=routes['RT.ACTION']; areq=set(ar['requires'].split(';'))
    req('DEP.APPROVAL_PRECONDITION_SATISFIED' in areq,'ACTION missing conditional approval precondition')
    req('DEP.APPROVAL_CURRENT' not in areq and 'DEP.APPROVAL_RESOLUTION_ALLOW_EMITTED' not in areq,'ACTION retains unconditional approval predecessor')
    ag=[g for g in events['RT.ACTION']['guards'] if g.get('operator')=='APPROVAL_PRECONDITION_SATISFIED']; req(len(ag)==1,'ACTION typed approval guard missing')
    sat=set(ag[0]['satisfying_states']); req(sat=={'APPROVAL_NOT_REQUIRED','APPROVAL_REQUIRED_AND_CURRENT_APPROVAL_WITH_ALLOW_RESOLUTION_EMITTED'},'ACTION approval satisfiers mismatch')
    req('CURRENT_APPROVAL_WHEN_REQUIRED' in ar.get('pre_effect_sequence',''),'ACTION sequence not conditional')
    # Obsolete Starter required_version requirement removed from actual obligations.
    req('Starter top-level PROMPT_VERSION equals validation_contract.required_version' not in core,'Core stale required_version boot check remains')
    req(not any('top-level PROMPT_VERSION equals validation_contract.required_version' in x for x in starter['validation_contract']['required_retests']),'Starter stale required_retest remains')
    # Five-file authority manifest.
    req(len(starter['authority_contract']['required_files'])==5,'authority required_files not five')
    req({x['canonical_filename'] for x in starter['authority_contract']['required_files']}=={'AIR_CORE_RUNTIME.md','AIR_CONTROL_SURFACE.md','AIR_GOV.md','AIR_DEFAULT_STARTER_PROFILE.json','AIR_HANDOFF_CARD_TEMPLATE.json'},'authority file set mismatch')
    # Expanded registry and mandatory coverage.
    n=eval_registry(root,starter); req(n==80,f'expected 80 deterministic checks, got {n}')
    ids={c['check_id'] for c in starter['validation_contract']['deterministic_contract_registry']['checks']}
    for x in ['DC-VERSION-CORE','DC-VERSION-CONTROL','DC-VERSION-GOV','DC-KIND-STARTER','DC-FUNCTION-CLASS-STARTER','DC-FILENAME-STARTER','DC-STRICT-JSON-STARTER','DC-STRICT-JSON-HANDOFF','DC-FOUNDATION-MANIFEST-EXACT','DC-FOUNDATION-NORMALIZED-COLLISION']:
        req(x in ids,f'missing deterministic check {x}')
    for i in range(1,28): req((f'DC-CORE-FLOOR-{i:03d}' in ids) if i<25 else True,f'missing floor check {i}')
    # Route Map anchors, Core hash, and RT.ACTION requirement mirror.
    req(rmap['source_of_truth']['sha256']==hashlib.sha256(core_p.read_bytes()).hexdigest(),'route-map Core hash stale')
    line_by={ln.split('=',1)[1]:i for i,ln in enumerate(core.splitlines(),1) if ln.startswith('id=RT.')}
    for rr in rmap['routes']:
        req(rr['source_anchor']['line']==line_by[rr['route_id']],f'{rr["route_id"]}: stale source anchor')
    mroute={r['route_id']:r for r in rmap['routes']}['RT.ACTION']
    req(set(mroute['requires'])==areq,'Route Map ACTION requirements diverge')
    # Canonical SFV capability vocabulary.
    core_need=set(re.findall(r'^- ([A-Z][A-Z0-9_]+)$', core[core.index('Need states:'):core.index('Capability layer check output should include:')], re.M))
    sfv=starter['routing_contracts']['sfv_method_routing']; req(set(sfv['need_states'])<=core_need,'SFV need states outside Core')
    req(sfv.get('layer_type')=='METHOD_PACK' and sfv.get('specialization')=='SPECIFICATION_FIRST_VERIFICATION','SFV discriminator missing')
    req('When Core returns FULL_SFV_' not in control,'Control still consumes undeclared FULL_SFV state')
    req(set(sfv['legacy_state_projection'].values())<=core_need,'legacy SFV projection not canonical')
    fixture_path=root/'tests/r1_remediation_fixtures.json'
    if fixture_path.is_file():
        fx=load(fixture_path)
        req(len(fx.get('finding_scope',[]))==14,'R1 fixture finding scope must contain 14 findings')
        req(len(fx.get('negative_cases',[]))>=14,'R1 negative fixture coverage incomplete')
        req(len(fx.get('positive_cases',[]))>=8,'R1 positive fixture coverage incomplete')
    print('R1 remediation validation: PASS')
    print('deterministic_routes',len(det_closed))
    print('route_event_bindings',len(det_closed))
    print('typed_registry_checks',n)
    print('route_anchors',len(rmap['routes']))
    print('alignment_profiles',len(profiles))
if __name__=='__main__':
    try: main(Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve())
    except (E,KeyError,AssertionError) as e:
        print('R1 remediation validation: FAIL:',e,file=sys.stderr); raise SystemExit(1)
