from __future__ import annotations
import hashlib,json,sys,re
from pathlib import Path
from typing import Any
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
FOUNDATION_ID='AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006'
FOUNDATION_STATE='OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_'+FOUNDATION_ID
STATIC_PASS='PASS_R7_DETERMINISTIC_STATIC_SUITE'
BEHAVIOR_PENDING='PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'
T7={
 'change_id':'AIR_T7_CEA_MII_INTEGRATION_001','package_version':'2.4.0','component_prompt_version':'2.2.0','manifest_prompt_version':'2.1.0',
 'change_class':'MINOR_SEMANTIC_PACKAGE_EXPANSION_WITH_NO_AUTHORITY_EXPANSION',
 'reason_for_version':'2.4.0 selected after actual diff because all four operative components gain additive MII/semantic/epistemic/morphology contribution contracts and evidence-presentation semantics while package identity and authority class remain v2-compatible.',
 'source_package_version':'2.3.9','applied_at':'2026-08-28T21:05:00+02:00'}
HISTORY={'source_baseline','mainline_release_binding','t7_change_record','historical_release_catalogs','source_candidate_manifest','change_history','release_history','historical_records'}
class E(Exception):pass
def req(c,m):
 if not c:raise E(m)
def reject(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise E('duplicate JSON key '+k)
  d[k]=v
 return d
def load(p):return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=reject)
def meta(p):
 raw=p.read_bytes();return {'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'line_count':len(raw.decode().splitlines())}
def hist(path):return any(x in HISTORY or x.startswith('historical_') for x in path)
def walk(o,path=()):
 if hist(path):return
 if isinstance(o,dict):
  yield path,o
  for k,v in o.items():yield from walk(v,path+(k,))
 elif isinstance(o,list):
  for i,v in enumerate(o):yield from walk(v,path+(str(i),))
 else:yield path,o
def status_of(p):
 o=load(p);return str(o.get('STATUS') or o.get('status') or '')
def avail(st):
 if st=='DRAFT' or 'STATIC_CONTRACT_VALIDATION_PENDING' in st:return 'AVAILABLE_UNVALIDATED'
 if 'STATIC_VALIDATED' in st:return 'VALIDATED_AVAILABLE_UNBOUND'
 return 'AVAILABLE_UNVALIDATED'
def main():
 files=sorted([*ROOT.glob('prompts/*.json'),*ROOT.glob('catalog/*.json'),*ROOT.glob('profiles/**/*.json')])
 req(len(files)==28,'operational JSON count != 28')
 parsed={p:load(p) for p in files}
 core=(ROOT/'prompts/AIR_CORE_RUNTIME.md').read_text()
 req('Patch marker: AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1' in core,'006 Core candidate lifecycle marker missing')
 for tok in ['RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION','RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION','RELEASE_CATALOG_ENTRY']:
  req(tok in core,'006 Core lifecycle token missing '+tok)
 idx=parsed[ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json']
 req(idx['status']=='AIR_2_6_1_OBJECT_CONTRACT_SET_006_FIVE_PACKAGE_INDEX_V072_CANDIDATE_STATIC_VALIDATED','073 current index status incoherent')
 req(idx['catalog_scope']['catalog_completeness_claim']=='COMPLETE_FOR_AIR_2_6_1_OBJECT_CONTRACT_SET_006_V072_CANDIDATE_SPECIALIST_CATALOG','073 completeness identity incoherent')
 histrel=idx['catalog_scope'].get('historical_release_catalogs',[])
 req(histrel==[{'kit_release':'0.7.0','foundation_identity':'AIR_FOUNDATION_2_5_0_OBJECT_CONTRACT_SET_004','index_generation':'V070','catalog_completeness_claim':'COMPLETE_FOR_AIR_2_5_0_SET_004_V070_RELEASE_SPECIALIST_CATALOG','state':'RELEASED_HISTORICAL_NON_OPERATIVE'}],'073 v0.7.0 history not explicit/immutable')
 lc=idx.get('candidate_lifecycle_contract',{})
 req(lc.get('core_patch_marker')=='AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1','006 index lifecycle not bound to Core')
 req(lc.get('states')==['RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION','RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION','RELEASE_CATALOG_ENTRY'],'006 lifecycle state set mismatch')
 req(lc.get('current_candidate_state')=='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION' and lc.get('candidate_states_are_release_sealed') is False,'006 release state semantics wrong')
 req(idx['validation_state'].get('static_validation')==STATIC_PASS,'R7 index static validation not PASS')
 req(idx['validation_state'].get('behavioral_revalidation')==BEHAVIOR_PENDING,'R7 index behavioral state not pending')
 req(idx['validation_state'].get('release_publication_state')=='EXTERNAL_RELEASE_STATE_NOT_RUNTIME_AUTHORITY','R7 publication authority changed')
 for e in idx['entries']:
  req(e['foundation_compatibility_identity']==FOUNDATION_ID,'index entry Foundation identity stale')
  req(e['availability_state']=='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION','006 index entry lifecycle mismatch')
 count=0
 for p,o in parsed.items():
  if not str(p).startswith(str(ROOT/'profiles')):continue
  ir=o.get('integration_refresh') if isinstance(o,dict) else None
  if isinstance(ir,dict) and 'foundation_identity_state' in ir:
   count+=1;req(ir['foundation_identity_state']==FOUNDATION_STATE,f'{p}: stale current Foundation identity')
 req(count==21,f'current integration_refresh identity carrier count changed: {count}')
 mans=sorted(ROOT.glob('profiles/**/*PACKAGE_MANIFEST.json'))
 req(len(mans)==5,'manifest count !=5')
 for p in mans:
  o=parsed[p]
  st=str(o.get('status') or '')
  req('STATIC_VALIDATED' in st and 'BEHAVIORAL_REVALIDATION_PENDING' in st and 'STATIC_CONTRACT_VALIDATION_PENDING' not in st,f'{p}: top lifecycle not R7 static-pass/behavior-pending')
  pvs=o.get('package_validation_state',{})
  static_keys=[k for k in ('t7_static_validation','coordinated_reseal_static_validation','static_design_validation') if k in pvs]
  req(static_keys,f'{p}: no static validation carrier')
  for k in static_keys:req(pvs[k]==STATIC_PASS,f'{p}: {k} not static PASS')
  if 'behavioral_revalidation' in pvs:req(pvs['behavioral_revalidation']==BEHAVIOR_PENDING,f'{p}: behavioral validation not pending')
  for c in o.get('components',[]):
   fn=c['filename']; cp=p.parent/fn; req(cp.is_file(),f'{p}: missing component {fn}')
   m=meta(cp)
   for k in ('sha256','size_bytes','line_count'):
    req(c.get(k)==m[k],f'{p}: stale {k} for {fn}')
   cst=status_of(cp)
   req(c.get('status')==cst,f'{p}: component status mirror mismatch {fn}')
   req(c.get('availability_state')==avail(cst),f'{p}: component availability mirror mismatch {fn}')
 for e in idx['entries']:
  targets=list(ROOT.glob('profiles/**/'+e['manifest_filename']))
  req(len(targets)==1,'index manifest target ambiguity '+e['manifest_filename'])
  req(e['manifest_sha256']==meta(targets[0])['sha256'],'index manifest hash stale '+e['manifest_filename'])
 rm=parsed[ROOT/'catalog/AIR_RUNTIME_ROUTE_MAP.json']
 req(rm['source_of_truth']['sha256']==meta(ROOT/'prompts/AIR_CORE_RUNTIME.md')['sha256'],'route map Core receipt stale')
 for p,o in parsed.items():
  if not str(p).startswith(str(ROOT/'profiles')):continue
  for loc,v in walk(o):
   if isinstance(v,str):
    req('BEHAVIORAL_REVALIDATION_PASS' not in v,f'{p}:{".".join(loc)} unsupported current behavioral PASS')
    req(v!='PASS_CURRENT_SESSION_PROMPT_RUNTIME_REPRESENTATIVE_SCENARIO_REVALIDATION',f'{p}:{".".join(loc)} stale current-session behavioral PASS')
    req('OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_AIR_2_5_0_MII_CANDIDATE_SET_005' not in v,f'{p}:{".".join(loc)} old operative Foundation identity')
 gov=parsed[ROOT/'profiles/governance specialist/AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json']
 expected=[c.get('role') for c in gov['components']]
 roles=gov['failure_mode_integration_contract'].get('component_roles_observed')
 req(roles==expected and all(roles),'050 Governance component roles not populated from actual roles')
 sfv=parsed[ROOT/'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json']
 vc=sfv['validation_contract']
 req('required_package_version' not in vc,'061 stale duplicate required_package_version remains')
 req(vc.get('required_package_version_source')=='$.package_version' and vc.get('required_package_version_check')=='EQUAL_TO_CANONICAL_TOP_LEVEL_PACKAGE_VERSION','061 canonical package version reference missing')
 req(sfv.get('package_version')=='2.5.0','061 current package_version changed')
 cea=parsed[ROOT/'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json']
 req(cea.get('t7_change_record')==T7,'074 T7 historical record mutated')
 rp=ROOT/'tools/reseal_air_candidate.py'
 if rp.is_file():
  txt=rp.read_text()
  req('HISTORICAL_CONTAINER_KEYS' in txt and 'historical_path' in txt and 'if historical_path(path): return' in txt,'R7 resealer historical exclusion missing')
 print('R7 remediation validation: PASS')
 print('r7_findings 14')
 print('current_foundation_identity_carriers',count)
 print('package_manifests 5')
 print('operational_json 28')
 print('behavioral_evidence CURRENTLY_PENDING')
if __name__=='__main__':
 try:main()
 except (E,KeyError,StopIteration,IndexError) as e:
  print('R7 remediation validation: FAIL:',e,file=sys.stderr);raise SystemExit(1)
