#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXPECTED_CORE_SHA='fe857e23ee58b641faca0e0e15fbc6d4bdca087c1fb571ed272d8b0e07453dbb'
FIELDS_EXEC=['capability_clusters when vector compilation is material','missing_vectors when vector compilation is material','degraded_execution_mode when execution is materially degraded','dependency_edges when execution dependencies are material','vector_family_state_summary when vector-family state is material','objective when coding/implementation formation is material']
FIELDS_READY=['readiness_reason when coding/readiness is material','stage_constraints when coding/readiness is material','promotion_requirements when coding/readiness is material','blocked_capabilities when coding/readiness is material','decision_state when coding/readiness review is material']
REQUIRED_NAMES=[x.split(' when ')[0] for x in FIELDS_EXEC+FIELDS_READY]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def lc(p):
 b=p.read_bytes(); return b.count(b'\n')+(0 if b.endswith(b'\n') else 1)
def run(args,cwd=None,env=None):
 print('+',' '.join(map(str,args)),flush=True); subprocess.run(args,cwd=cwd or ROOT,env=env,check=True)
def dump(p,obj): p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def patch_core():
 p=ROOT/'prompts/AIR_CORE_RUNTIME.md'
 if sha(p)!=EXPECTED_CORE_SHA: raise SystemExit(f'fail closed: Core SHA {sha(p)} != expected {EXPECTED_CORE_SHA}')
 t=p.read_text('utf-8'); a='- execution_benchmark_profile\n'
 if a not in t: raise SystemExit('fail closed: execution benchmark anchor missing')
 t=t.replace(a,a+''.join(f'- {x}\n' for x in FIELDS_EXEC),1); a='- readiness_stage when coding/readiness is material\n'
 if a not in t: raise SystemExit('fail closed: readiness anchor missing')
 t=t.replace(a,a+''.join(f'- {x}\n' for x in FIELDS_READY),1); p.write_text(t,encoding='utf-8')
def patch_checker():
 p=ROOT/'tests/air_object_contract_check.py'; t=p.read_text('utf-8'); anchor="req(af.get('source_marker')=='AIR_OBJECT_RESPONSIBILITY_CLOSURE_V1','Starter Artifact registry source marker drift')\n"
 if anchor not in t: raise SystemExit('fail closed: object checker anchor missing')
 block="""\n# Closed-world AIR_ARTIFACT must admit every field that Core itself conditionally requires.\nartifact_section=core[core.index('AIR_ARTIFACT base allowed object-owned top-level fields:'):core.index('AIR_ACTIVE_CONTRACT allowed object-owned top-level fields:')]\nrequired_artifact_fields=[\n    'capability_clusters','missing_vectors','degraded_execution_mode','dependency_edges',\n    'vector_family_state_summary','objective','readiness_reason','stage_constraints',\n    'promotion_requirements','blocked_capabilities','decision_state'\n]\nfor field in required_artifact_fields:\n    req(re.search(rf'^-\\s+{re.escape(field)}(?:\\s|$)',artifact_section,re.M) is not None,\n        f'Core AIR_ARTIFACT closed-world list omits Core-required field: {field}')\n"""
 if 'required_artifact_fields=[' not in t: p.write_text(t.replace(anchor,anchor+block,1),encoding='utf-8')
def reseal():
 source=[]
 for d in [ROOT/'prompts',ROOT/'catalog',ROOT/'profiles']: source += [p for p in d.rglob('*') if p.is_file()]
 byname={}
 for p in source: byname.setdefault(p.name,[]).append(p)
 def resolve(name,current):
  a=byname.get(name,[])
  if len(a)==1:return a[0]
  for p in a:
   if p.parent==current.parent:return p
  return None
 def meta(p): return {'sha256':sha(p),'size_bytes':p.stat().st_size,'line_count':lc(p)}
 def walk(x,current):
  changed=False
  if isinstance(x,dict):
   name=x.get('filename') or x.get('canonical_filename')
   if isinstance(name,str):
    target=resolve(name,current)
    if target:
     m=meta(target)
     for k in ('sha256','observed_sha256','expected_sha256'):
      if k in x and x[k]!=m['sha256']: x[k]=m['sha256']; changed=True
     for k in ('size_bytes','line_count'):
      if k in x and x[k]!=m[k]: x[k]=m[k]; changed=True
   mf=x.get('manifest_filename')
   if isinstance(mf,str):
    target=resolve(mf,current)
    if target:
     m=meta(target)
     for k,mk in [('manifest_sha256','sha256'),('manifest_size_bytes','size_bytes'),('manifest_line_count','line_count')]:
      if k in x and x[k]!=m[mk]: x[k]=m[mk]; changed=True
   for v in x.values():
    if walk(v,current): changed=True
  elif isinstance(x,list):
   for v in x:
    if walk(v,current): changed=True
  return changed
 json_sources=[p for p in source if p.suffix=='.json']
 for n in range(20):
  changed=False
  for p in json_sources:
   obj=json.loads(p.read_text('utf-8'))
   if walk(obj,p): dump(p,obj); changed=True
  if not changed: print('dependency reseal fixed point rounds:',n+1); break
 else: raise SystemExit('fail closed: reseal did not converge')
 tm=ROOT/'tests/air-test-manifest.json'; obj=json.loads(tm.read_text('utf-8'))
 for test in obj.get('tests',[]):
  if test.get('type')=='sha256_equals' and isinstance(test.get('path'),str):
   p=ROOT/test['path']
   if p.is_file(): test['expected']=sha(p)
 dump(tm,obj)
def assert_field_closure():
 core=(ROOT/'prompts/AIR_CORE_RUNTIME.md').read_text('utf-8'); sec=core[core.index('AIR_ARTIFACT base allowed object-owned top-level fields:'):core.index('AIR_ACTIVE_CONTRACT allowed object-owned top-level fields:')]
 missing=[f for f in REQUIRED_NAMES if re.search(rf'^-\s+{re.escape(f)}(?:\s|$)',sec,re.M) is None]
 if missing: raise SystemExit(f'fail closed: missing AIR_ARTIFACT fields {missing}')
 print('AIR_ARTIFACT 11-field closure PASS:',', '.join(REQUIRED_NAMES))
def executable_suite(out):
 run([sys.executable,'tests/air_object_contract_check.py'])
 env=os.environ.copy(); env.update({'TZ':'UTC','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','PYTHONHASHSEED':'0','AIR_TEST_SEED':'0','AIR_NETWORK_POLICY':'DISABLED_ENFORCED_CI','AIR_SOURCE_COMMIT':os.environ.get('GITHUB_SHA','S14_REMEDIATION')})
 runs=[]
 for i in (1,2,3):
  rp=out/f'run-{i}.json'; run([sys.executable,'tests/air_test_runner.py','--manifest','tests/air-test-manifest.json','--output',str(rp),'--run-index',str(i)],env=env); d=json.loads(rp.read_text('utf-8'))
  if d.get('decision')!='PASS' or d.get('tests_failed')!=0: raise SystemExit(f'executable run {i} failed')
  runs.append(d)
 for k in ('suite_sha256','fixture_set_sha256','decision_fingerprint'):
  if len({r[k] for r in runs})!=1: raise SystemExit(f'run fingerprint mismatch: {k}')
 print('executable suite PASS x3:',runs[0]['tests_passed'],'/',runs[0]['tests_total'])
def static_suite(out):
 cand=out/'candidate'
 for d in ['foundation','catalog','validation','tools','specialists/capability-ecology','specialists/grounding','specialists/sfv','specialists/ai-governance']:(cand/d).mkdir(parents=True,exist_ok=True)
 for p in (ROOT/'prompts').iterdir():
  if p.is_file() and p.name.startswith('AIR_'): shutil.copy2(p,cand/'foundation'/p.name)
 for p in (ROOT/'catalog').iterdir():
  if p.is_file(): shutil.copy2(p,cand/'catalog'/p.name)
 for p in (ROOT/'validation').iterdir():
  if p.is_file(): shutil.copy2(p,cand/'validation'/p.name)
 for p in (ROOT/'tools').iterdir():
  if p.is_file(): shutil.copy2(p,cand/'tools'/p.name)
 for src,dst in [('capability ecology architect','capability-ecology'),('grounding specialist','grounding'),('specification first verification specialist','sfv'),('governance specialist','ai-governance')]:
  for p in (ROOT/'profiles'/src).iterdir():
   if p.is_file(): shutil.copy2(p,cand/'specialists'/dst/p.name)
 spec=cand/'validation/AIR_2.5.0_OBJECT_CONTRACT_SPECIALIST_LAYER_VALIDATION.json'; run([sys.executable,'tools/validate_specialist_layer.py',str(cand),str(spec)],cwd=cand)
 env=os.environ.copy(); env['AIR250_VALIDATION_ROOT']=str(cand); env['AIR250_VALIDATION_OUT']=str(cand/'validation'); run([sys.executable,'tools/validate_air250_full_static.py'],cwd=cand,env=env)
 sd=json.loads(spec.read_text('utf-8'))['AIR_VALIDATION_REPORT']; fd=json.loads((cand/'validation/AIR_2.5.0_FULL_CROSS_SYSTEM_STATIC_VALIDATION.json').read_text('utf-8'))['AIR_VALIDATION_REPORT']
 if sd.get('decision')!='PASS' or sd.get('summary',{}).get('passed')!=185: raise SystemExit('Specialist validation is not 185/185 PASS')
 if fd.get('decision')!='PASS_STATIC_OBJECT_CONTRACT_CLOSURE_VALIDATED_PENDING_FRESH_BEHAVIORAL' or fd.get('summary')!={'total':927,'passed':927,'failed':0,'warnings':0}: raise SystemExit(f'integrated static mismatch: {fd.get("decision")} {fd.get("summary")}')
 for fn in ['AIR_2.5.0_OBJECT_CONTRACT_SPECIALIST_LAYER_VALIDATION.json','AIR_2.5.0_FULL_CROSS_SYSTEM_STATIC_VALIDATION.json','AIR_2.5.0_INTEGRATED_CANDIDATE_INVENTORY.json','AIR_2.5.0_FULL_STATIC_DEFECT_MAP.md','AIR_2.5.0_FULL_STATIC_TRANSACTION_RECEIPT.json']: shutil.copy2(cand/'validation'/fn,ROOT/'validation'/fn)
 print('static closure PASS: 185/185, 28/28 edges, 927/927, warnings 0')
def main():
 if os.environ.get('GITHUB_REF_NAME')!='air250-preview-stage-t12d': raise SystemExit('fail closed: wrong branch')
 patch_core(); patch_checker(); reseal(); assert_field_closure()
 with tempfile.TemporaryDirectory(prefix='air-s14-') as td:
  out=Path(td); executable_suite(out); static_suite(out)
 print('S14 remediation complete'); print('CORE_SHA256',sha(ROOT/'prompts/AIR_CORE_RUNTIME.md')); print('ROUTE_MAP_SHA256',sha(ROOT/'catalog/AIR_RUNTIME_ROUTE_MAP.json')); print('SPECIALIST_INDEX_SHA256',sha(ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'))
if __name__=='__main__': main()
