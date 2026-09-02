import json, pathlib, hashlib, sys
ROOT=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parents[1]
OUT=pathlib.Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'validation/AIR_2.5.0_OBJECT_CONTRACT_SPECIALIST_LAYER_VALIDATION.json'
FOUNDATION_ID='AIR_FOUNDATION_2_5_0_OBJECT_CONTRACT_SET_003'
STALE=('CANDIDATE_SET_001','PENDING_T8','PENDING_T9','PENDING_T10','PENDING_SPECIALIST_INDEX_RESEAL')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def lc(p):
 b=p.read_bytes();return b.count(b'\n')+(1 if b and not b.endswith(b'\n') else 0)
def load(p):
 dup=[]
 def hook(pairs):
  d={}; seen=set()
  for k,v in pairs:
   if k in seen: dup.append(k)
   seen.add(k); d[k]=v
  return d
 with open(p,encoding='utf-8') as f:d=json.load(f,object_pairs_hook=hook)
 if dup: raise ValueError('duplicate keys '+repr(sorted(set(dup))))
 return d

def refs(o):
 out=[]
 def walk(x,path=()):
  if isinstance(x,dict):
   fn=x.get('filename') or x.get('canonical_filename')
   if fn:
    for hk in ('sha256','observed_sha256'):
     if hk in x and x.get(hk) is not None: out.append((fn,x[hk],'.'.join(map(str,path+(hk,)))))
   for k,v in x.items():walk(v,path+(k,))
  elif isinstance(x,list):
   for i,v in enumerate(x):walk(v,path+(i,))
 walk(o); return out

PKGS={
 'cea':('specialists/capability-ecology',['AIR_DOMAIN_CAPABILITY_REGISTRY.json','AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json','AIR_CAPABILITY_ECOLOGY_ARCHITECT.json','AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json'],'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json',[
 ('AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json','AIR_DOMAIN_CAPABILITY_REGISTRY.json'),('AIR_CAPABILITY_ECOLOGY_ARCHITECT.json','AIR_DOMAIN_CAPABILITY_REGISTRY.json'),('AIR_CAPABILITY_ECOLOGY_ARCHITECT.json','AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json'),('AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json','AIR_DOMAIN_CAPABILITY_REGISTRY.json'),('AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json','AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json'),('AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json','AIR_CAPABILITY_ECOLOGY_ARCHITECT.json')]),
 'grounding':('specialists/grounding',['AIR_GROUNDING_DOMAIN_PACKAGE.json','AIR_GROUNDING_METHOD_PACK.json','AIR_GROUNDING_SPECIALIST.json','AIR_GROUNDING_EXECUTOR.json'],'AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json',[
 ('AIR_GROUNDING_METHOD_PACK.json','AIR_GROUNDING_DOMAIN_PACKAGE.json'),('AIR_GROUNDING_SPECIALIST.json','AIR_GROUNDING_DOMAIN_PACKAGE.json'),('AIR_GROUNDING_SPECIALIST.json','AIR_GROUNDING_METHOD_PACK.json'),('AIR_GROUNDING_EXECUTOR.json','AIR_GROUNDING_DOMAIN_PACKAGE.json'),('AIR_GROUNDING_EXECUTOR.json','AIR_GROUNDING_METHOD_PACK.json'),('AIR_GROUNDING_EXECUTOR.json','AIR_GROUNDING_SPECIALIST.json')]),
 'sfv':('specialists/sfv',['AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json','AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json','AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json','AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json'],'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json',[
 ('AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json','AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json'),('AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json','AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json'),('AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json','AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json'),('AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json','AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json'),('AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json','AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json'),('AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json','AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json')]),
 'aigov':('specialists/ai-governance',['AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json','AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json','AIR_AI_GOVERNANCE_SPECIALIST.json','AIR_AI_GOVERNANCE_METHOD_PACK.json','AIR_AI_GOVERNANCE_EXECUTOR.json'],'AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json',[
 ('AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json','AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json'),('AIR_AI_GOVERNANCE_SPECIALIST.json','AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json'),('AIR_AI_GOVERNANCE_SPECIALIST.json','AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json'),('AIR_AI_GOVERNANCE_METHOD_PACK.json','AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json'),('AIR_AI_GOVERNANCE_METHOD_PACK.json','AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json'),('AIR_AI_GOVERNANCE_METHOD_PACK.json','AIR_AI_GOVERNANCE_SPECIALIST.json'),('AIR_AI_GOVERNANCE_EXECUTOR.json','AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json'),('AIR_AI_GOVERNANCE_EXECUTOR.json','AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json'),('AIR_AI_GOVERNANCE_EXECUTOR.json','AIR_AI_GOVERNANCE_SPECIALIST.json'),('AIR_AI_GOVERNANCE_EXECUTOR.json','AIR_AI_GOVERNANCE_METHOD_PACK.json')])}
checks=[]
def add(cid,ok,detail):checks.append({'check_id':cid,'status':'PASS' if ok else 'FAIL','detail':detail})
manifest_hash={};edge_count=0
for pkg,(rel,components,mfn,edges) in PKGS.items():
 d=ROOT/rel; objs={}; actual={}
 for fn in components:
  p=d/fn
  try:objs[fn]=load(p);add(f'JSON.{pkg}.{fn}',True,'strict JSON and no duplicate keys')
  except Exception as e:add(f'JSON.{pkg}.{fn}',False,str(e));continue
  actual[fn]=sha(p)
  fc=objs[fn].get('foundation_compatibility',{})
  add(f'FOUNDATION.{pkg}.{fn}',fc.get('compatibility_state')=='ALIGNED_TO_AIR_2_5_0_OBJECT_CONTRACT_SET_003' and fc.get('foundation_candidate_set_identity')==FOUNDATION_ID,f'{fc.get("compatibility_state")!r} / {fc.get("foundation_candidate_set_identity")!r}')
  st=str(objs[fn].get('STATUS',objs[fn].get('status','')))
  add(f'LIFECYCLE.{pkg}.{fn}',not any(t in st for t in STALE) and 'OBJECT_CONTRACT_SET_003_RESEAL_STATIC_VALIDATED' in st,st)
 for src,tgt in edges:
  edge_count+=1
  rs=[(h,path) for f,h,path in refs(objs[src]) if f==tgt]
  add(f'EDGE.{pkg}.{src}->{tgt}',any(h==actual[tgt] for h,path in rs),f'actual={actual[tgt]}; refs={rs}')
 for src,o in objs.items():
  for tgt,h,path in refs(o):
   if tgt in actual:add(f'REF.{pkg}.{src}.{path}',h==actual[tgt],f'{tgt}: declared={h}, actual={actual[tgt]}')
 mp=d/mfn;m=load(mp);manifest_hash[pkg]=sha(mp)
 fc=m.get('foundation_compatibility',{})
 add(f'MANIFEST.FOUNDATION.{pkg}',fc.get('compatibility_state')=='ALIGNED_TO_AIR_2_5_0_OBJECT_CONTRACT_SET_003' and fc.get('foundation_candidate_set_identity')==FOUNDATION_ID,f'{fc.get("compatibility_state")!r} / {fc.get("foundation_candidate_set_identity")!r}')
 st=str(m.get('status',m.get('STATUS','')));add(f'MANIFEST.LIFECYCLE.{pkg}',not any(t in st for t in STALE) and 'OBJECT_CONTRACT_SET_003_RESEAL_STATICALLY_VALIDATED' in st,st)
 mc={e.get('filename'):e for e in m.get('components',[])}
 add(f'MANIFEST.COMPONENT_SET.{pkg}',set(mc)==set(components),f'{sorted(mc)}')
 for fn in components:
  p=d/fn;e=mc.get(fn,{})
  add(f'MANIFEST.HASH.{pkg}.{fn}',e.get('sha256')==sha(p),f'{e.get("sha256")} / {sha(p)}')
  add(f'MANIFEST.SIZE.{pkg}.{fn}',e.get('size_bytes')==p.stat().st_size,f'{e.get("size_bytes")} / {p.stat().st_size}')
  add(f'MANIFEST.LINES.{pkg}.{fn}',e.get('line_count')==lc(p),f'{e.get("line_count")} / {lc(p)}')
idx=load(ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json')
add('EDGE.CANONICAL_COUNT',edge_count==28,f'{edge_count}')
add('INDEX.VERSION',idx.get('INDEX_VERSION')=='1.1.1',str(idx.get('INDEX_VERSION')))
ids={'cea':'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2','grounding':'AIR_GROUNDING_SPECIALIST_PACKAGE_V2','sfv':'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2','aigov':'AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_V2'}
ents={e.get('package_identity'):e for e in idx.get('entries',[])}
for pkg,pid in ids.items():
 e=ents.get(pid,{})
 add(f'INDEX.MANIFEST.{pkg}',e.get('manifest_sha256')==manifest_hash[pkg],f'{e.get("manifest_sha256")} / {manifest_hash[pkg]}')
 add(f'INDEX.FOUNDATION.{pkg}',e.get('foundation_compatibility_identity')==FOUNDATION_ID,str(e.get('foundation_compatibility_identity')))
vs=idx.get('validation_state',{})
add('INDEX.INTERNAL_CLOSURE_STATE',vs.get('specialist_internal_dependency_closure')=='PASS_28_OF_28',str(vs.get('specialist_internal_dependency_closure')))
add('INDEX.LIFECYCLE_STATE',vs.get('operative_lifecycle_coherence')=='PASS',str(vs.get('operative_lifecycle_coherence')))
failed=[c for c in checks if c['status']=='FAIL']
report={'AIR_VALIDATION_REPORT':{'report_id':'AIR-VAL-AIR250-OBJECT-CONTRACT-SPECIALIST-RESEAL-001','object_version':'2.0.0','record_class':'VALIDATION_RECORD','validated_target':'AIR 2.5.0 four-Specialist layer plus Specialist Package Index 1.1.1','validation_kind':'REPRODUCIBLE_EXECUTABLE_STATIC_ANALYSIS','decision':'PASS' if not failed else 'FAIL','summary':{'total':len(checks),'passed':len(checks)-len(failed),'failed':len(failed),'canonical_internal_edges':edge_count},'failed_check_ids':[c['check_id'] for c in failed],'checks':checks,'runtime_origin':'TOOL_OBSERVED','backend_validation_claimed':False,'hidden_reasoning_claimed':False}}
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'decision':report['AIR_VALIDATION_REPORT']['decision'],'summary':report['AIR_VALIDATION_REPORT']['summary'],'report':str(OUT)},indent=2))
sys.exit(1 if failed else 0)
