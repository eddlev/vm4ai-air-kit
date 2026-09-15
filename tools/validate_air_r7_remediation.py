from __future__ import annotations
import hashlib,json,sys,re
from pathlib import Path
from typing import Any
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
FOUNDATION_ID='AIR_FOUNDATION_2_6_3_OBJECT_CONTRACT_SET_008'
LEGACY_FOUNDATION_ID='AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'
FOUNDATION_STATE='OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_'+LEGACY_FOUNDATION_ID
SET008_FOUNDATION_STATE='OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_'+FOUNDATION_ID
STATIC_PASS='PASS_R7_DETERMINISTIC_STATIC_SUITE'
BEHAVIOR_PENDING='PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'
BEHAVIOR_PASS='PASS_REPLAYABLE_MODEL_HOST_EVIDENCE'
SPECIALIST_COMPAT='ALIGNED_TO_AIR_2_6_2_OBJECT_CONTRACT_SET_007'
SET008_SPECIALIST_COMPAT='ALIGNED_TO_AIR_2_6_3_OBJECT_CONTRACT_SET_008'
PENDING_STATIC='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION'
PENDING_BEHAVIOR='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'
RELEASED='RELEASE_CATALOG_ENTRY'
CW_PACKAGE='AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'
SFV_PACKAGE='AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2'
CW_DIR='public surface copywriting specialist'
SFV_DIR='specification first verification specialist'
SFV_COMPONENT_PASS_STATUS='V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND'
SFV_PACKAGE_PASS_STATE='PACKAGE_STRUCTURALLY_COMPLETE_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND_EXECUTOR_DRAFT_UNVALIDATED'
SFV_BEHAVIORAL_COMPONENTS={'AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json','AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json','AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json'}
SPECIALIST_REQUIRED_FLOORS={'AIR-FLOOR-027-FAILURE-MODE-LEARNING-AND-RETRY','AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION'}
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
 req(idx.get('INDEX_VERSION')=='1.3.7','SFV SET_008 behavioral promotion index version mismatch')
 req(idx['foundation_compatibility_catalog'].get('identity')==FOUNDATION_ID,'SET_008 catalog identity mismatch')
 req(idx['status']=='AIR_2_6_3_OBJECT_CONTRACT_SET_008_FIVE_PACKAGE_INDEX_V072_PATCH2_CANDIDATE_PENDING_STATIC_VALIDATION','v073 current index status incoherent')
 req(idx['catalog_scope']['catalog_completeness_claim']=='COMPLETE_FOR_AIR_2_6_3_OBJECT_CONTRACT_SET_008_V072_PATCH2_CANDIDATE_SPECIALIST_CATALOG','v073 completeness identity incoherent')
 histrel=idx['catalog_scope'].get('historical_release_catalogs',[])
 req(histrel==[{'kit_release':'0.7.0','foundation_identity':'AIR_FOUNDATION_2_5_0_OBJECT_CONTRACT_SET_004','index_generation':'V070','catalog_completeness_claim':'COMPLETE_FOR_AIR_2_5_0_SET_004_V070_RELEASE_SPECIALIST_CATALOG','state':'RELEASED_HISTORICAL_NON_OPERATIVE'}],'073 v0.7.0 history not explicit/immutable')
 lc=idx.get('candidate_lifecycle_contract',{})
 req(lc.get('core_patch_marker')=='AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1','006 index lifecycle not bound to Core')
 req(lc.get('states')==['RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION','RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION','RELEASE_CATALOG_ENTRY'],'006 lifecycle state set mismatch')
 req(lc.get('current_candidate_state')=='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION' and lc.get('candidate_states_are_release_sealed') is False,'006 release state semantics wrong')
 req(idx['validation_state'].get('static_validation')=='PENDING_SPECIALIST_PACKAGE_SET_008_STATIC_COMPATIBILITY_REVALIDATION','R7 index static validation stage mismatch')
 req(idx['validation_state'].get('behavioral_revalidation')=='BLOCKED_PENDING_SET_008_STATIC_COMPATIBILITY_REVALIDATION','R7 index behavioral state must remain blocked pending static revalidation')
 prog=idx['validation_state'].get('set008_static_revalidation_progress',{})
 req(prog.get('passed_package_identities')==[CW_PACKAGE,SFV_PACKAGE] and prog.get('passed_count')==2 and prog.get('pending_count')==3 and prog.get('behavioral_revalidation_ready_package_identities')==[] and prog.get('behavioral_revalidation_passed_package_identities')==[CW_PACKAGE,SFV_PACKAGE] and prog.get('behavioral_revalidation_passed_count')==2,'R7 SET_008 progress carrier mismatch')
 req(len(prog.get('pending_package_identities',[]))==3 and CW_PACKAGE not in prog.get('pending_package_identities',[]) and SFV_PACKAGE not in prog.get('pending_package_identities',[]),'R7 SET_008 pending package set mismatch')
 req(idx['validation_state'].get('release_publication_state')=='EXTERNAL_RELEASE_STATE_NOT_RUNTIME_AUTHORITY','R7 publication authority changed')
 for e in idx['entries']:
  if e['package_identity']==CW_PACKAGE:
   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'Copywriting index Foundation identity not SET_008')
   req(e['availability_state']==RELEASED,'Copywriting index lifecycle not released after behavioral revalidation')
   req(e.get('current_foundation_compatibility_state')=='STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED' and e.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'Copywriting SET_008 behavioral state mismatch')
  elif e['package_identity']==SFV_PACKAGE:
   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'SFV index Foundation identity not SET_008')
   req(e['availability_state']==RELEASED,'SFV index lifecycle not released after behavioral revalidation')
   req(e.get('current_foundation_compatibility_state')=='STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED_EXECUTOR_DRAFT_UNVALIDATED' and e.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'SFV SET_008 behavioral state mismatch')
   req(e.get('executor_component_state')=='DRAFT_AVAILABLE_UNVALIDATED','SFV Executor component boundary missing from index')
  else:
   req(e['foundation_compatibility_identity']==LEGACY_FOUNDATION_ID,'remaining pending index Foundation identity changed before revalidation')
   req(e['availability_state']==PENDING_STATIC,'remaining pending index lifecycle changed before static revalidation')
 profile_count=0
 for p,o in parsed.items():
  if not str(p).startswith(str(ROOT/'profiles')):continue
  profile_count+=1
  fc=o.get('foundation_compatibility') if isinstance(o,dict) else None
  req(isinstance(fc,dict),f'{p}: foundation compatibility missing')
  is_cw=CW_DIR in str(p)
  is_sfv=SFV_DIR in str(p)
  is_set008=is_cw or is_sfv
  expected_compat=SET008_SPECIALIST_COMPAT if is_set008 else SPECIALIST_COMPAT
  req(fc.get('compatibility_state')==expected_compat,f'{p}: stale Foundation compatibility state')
  if is_set008:
   req(fc.get('target_identity')==FOUNDATION_ID,f'{p}: SET_008 target identity missing')
   h=next((x for x in fc.get('required_files',[]) if x.get('filename')=='AIR_HANDOFF_CARD_TEMPLATE.json'),{})
   req(h.get('template_revision')==19 and h.get('revision_fields')==['template_revision','user_revision'] and 'card_revision' not in h,f'{p}: Handoff revision split stale')
   rr=fc.get('route_map_discovery_input') or fc.get('foundation_adjacent_route_map') or {}
   req(rr.get('version')=='1.2.2' and rr.get('sha256')=='a8817d0abe078a2b94f87562386ac5e63a575b0926c0b2d050a6e470f578e89c',f'{p}: Route Map receipt stale')
  req(SPECIALIST_REQUIRED_FLOORS.issubset(set(fc.get('required_floor_invariants',[]))),f'{p}: floors 027/028 missing')
  req(fc.get('cognitive_scope_authority_ref')=='AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION',f'{p}: Floor 028 reference missing')
  if p.name in SFV_BEHAVIORAL_COMPONENTS:
   req(status_of(p)==SFV_COMPONENT_PASS_STATUS,f'{p}: SFV behavioral component status mismatch')
   req(o.get('package_completion_contract',{}).get('package_state')==SFV_PACKAGE_PASS_STATE,f'{p}: SFV package completion state mismatch')
  if p.name=='AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json':
   req(o.get('STATUS')=='DRAFT',f'{p}: SFV Executor was promoted out of DRAFT')
 req(profile_count==24,f'Specialist profile/package file count changed: {profile_count}')
 ivs=idx['validation_state']
 req(ivs.get('handoff_rev19_catalog_compatibility')=='PASS_DISCOVERY_PROVENANCE_ONLY_PACKAGE_REVALIDATION_STILL_REQUIRED','Index Handoff rev19 provenance missing')
 req('handoff_rev16_catalog_compatibility' not in ivs and 'handoff_rev17_catalog_compatibility' not in ivs and 'handoff_rev18_catalog_compatibility' not in ivs,'stale current Handoff rev16/rev17/rev18 provenance remains')
 count=0
 for p,o in parsed.items():
  if not str(p).startswith(str(ROOT/'profiles')):continue
  ir=o.get('integration_refresh') if isinstance(o,dict) else None
  if isinstance(ir,dict) and 'foundation_identity_state' in ir:
   count+=1
   expected_state=SET008_FOUNDATION_STATE if (CW_DIR in str(p) or SFV_DIR in str(p)) else FOUNDATION_STATE
   req(ir['foundation_identity_state']==expected_state,f'{p}: stale current Foundation identity')
 req(count==21,f'current integration_refresh identity carrier count changed: {count}')
 mans=sorted(ROOT.glob('profiles/**/*PACKAGE_MANIFEST.json'))
 req(len(mans)==5,'manifest count !=5')
 for p in mans:
  o=parsed[p]
  st=str(o.get('status') or '')
  is_cw=CW_DIR in str(p)
  is_sfv=SFV_DIR in str(p)
  if is_cw or is_sfv:req('STATIC_VALIDATED' in st and 'REPLAYABLE_BEHAVIORAL_VALIDATED' in st and 'BEHAVIORAL_REVALIDATION_PENDING' not in st,f'{p}: SET_008 behavioral-pass lifecycle missing')
  else:req('STATIC_VALIDATED' in st and 'BEHAVIORAL_REVALIDATION_PENDING' in st and 'STATIC_CONTRACT_VALIDATION_PENDING' not in st,f'{p}: top lifecycle not R7 static-pass/behavior-pending')
  pvs=o.get('package_validation_state',{})
  static_keys=[k for k in ('t7_static_validation','coordinated_reseal_static_validation','static_design_validation') if k in pvs]
  req(static_keys,f'{p}: no static validation carrier')
  for k in static_keys:req(pvs[k]==STATIC_PASS,f'{p}: {k} not static PASS')
  if 'behavioral_revalidation' in pvs:req(pvs['behavioral_revalidation']==(BEHAVIOR_PASS if (is_cw or is_sfv) else BEHAVIOR_PENDING),f'{p}: behavioral validation state mismatch')
  for c in o.get('components',[]):
   fn=c['filename']; cp=p.parent/fn; req(cp.is_file(),f'{p}: missing component {fn}')
   m=meta(cp)
   for k in ('sha256','size_bytes','line_count'):
    req(c.get(k)==m[k],f'{p}: stale {k} for {fn}')
   cst=status_of(cp)
   req(c.get('status')==cst,f'{p}: component status mirror mismatch {fn}')
   req(c.get('availability_state')==avail(cst),f'{p}: component availability mirror mismatch {fn}')
 cwman=parsed[ROOT/'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json']
 req(cwman['foundation_compatibility'].get('state')=='COORDINATED_SET_008_RESEAL_STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED','Copywriting manifest SET_008 behavioral state mismatch')
 cpvs=cwman.get('package_validation_state',{})
 req(cpvs.get('foundation_reseal')=='PASS_COORDINATED_SET_008_RESEAL' and cpvs.get('component_internal_foundation_compatibility')=='PASS_SET_008_EXACT_RECEIPTS','Copywriting SET_008 manifest validation state mismatch')
 evp=ROOT/'tests/AIR_PUBLIC_SURFACE_COPYWRITING_SET008_BEHAVIORAL_EVIDENCE_V1.json'; req(evp.is_file(),'Copywriting behavioral evidence file missing'); ev=load(evp); er=cwman.get('behavioral_evidence_receipt',{})
 req(meta(evp)['sha256']=='948dfcf7f9dfe1839e06475bb7566521b56430d2fb141cb96065e1e8fd45769d' and er.get('sha256')=='948dfcf7f9dfe1839e06475bb7566521b56430d2fb141cb96065e1e8fd45769d','Copywriting behavioral evidence hash mismatch')
 req(ev.get('evidence_id')=='AIR_BEHAVIORAL_EVIDENCE_PUBLIC_SURFACE_COPYWRITING_SET008_20260914_V1' and ev.get('summary',{}).get('pass_count')==6 and ev.get('summary',{}).get('scenario_count')==6 and ev.get('summary',{}).get('behavioral_revalidation_result')=='PASS_ON_CURRENT_MODEL_HOST','Copywriting behavioral evidence result mismatch')
 req(er.get('result')==BEHAVIOR_PASS and er.get('model_host')=='ChatGPT / GPT-5.6 Sol' and er.get('cross_host_equivalence_claimed') is False,'Copywriting behavioral evidence receipt mismatch')
 sfvman=parsed[ROOT/'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json']
 req(sfvman['foundation_compatibility'].get('target_identity')==FOUNDATION_ID and sfvman['foundation_compatibility'].get('compatibility_state')==SET008_SPECIALIST_COMPAT,'SFV manifest SET_008 compatibility missing')
 spvs=sfvman.get('package_validation_state',{})
 req(spvs.get('behavioral_revalidation')==BEHAVIOR_PASS and spvs.get('component_internal_foundation_compatibility')=='PASS_SET_008_EXACT_RECEIPTS' and spvs.get('executor_validation_state')=='DRAFT_AVAILABLE_UNVALIDATED_EXCLUDED_FROM_BEHAVIORAL_PASS','SFV manifest validation state mismatch')
 sfvexec=parsed[ROOT/'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json']
 req(sfvexec.get('STATUS')=='DRAFT','SFV Executor was promoted out of DRAFT')
 sfventry=next(e for e in idx['entries'] if e['package_identity']==SFV_PACKAGE)
 req(sfventry.get('availability_state')==RELEASED and sfventry.get('foundation_compatibility_identity')==FOUNDATION_ID and sfventry.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'SFV index behavioral promotion mismatch')
 sfvevp=ROOT/'tests/AIR_SPECIFICATION_FIRST_VERIFICATION_SET008_BEHAVIORAL_EVIDENCE_V1.json'; req(sfvevp.is_file(),'SFV behavioral evidence file missing'); sfvev=load(sfvevp); sfver=sfvman.get('behavioral_evidence_receipt',{})
 req(meta(sfvevp)['sha256']=='831a048946574a10f7dd5a1adb8cd6b4125e4a39030f9414f9de2d464f1b5649' and sfver.get('sha256')=='831a048946574a10f7dd5a1adb8cd6b4125e4a39030f9414f9de2d464f1b5649','SFV behavioral evidence hash mismatch')
 req(sfvev.get('evidence_id')=='AIR_BEHAVIORAL_EVIDENCE_SPECIFICATION_FIRST_VERIFICATION_SET008_20260915_V1' and sfvev.get('summary',{}).get('pass_count')==6 and sfvev.get('summary',{}).get('scenario_count')==6 and sfvev.get('summary',{}).get('behavioral_revalidation_result')=='PASS_ON_CURRENT_MODEL_HOST','SFV behavioral evidence result mismatch')
 req(sfver.get('result')==BEHAVIOR_PASS and sfver.get('model_host')=='ChatGPT / GPT-5.6 Sol' and sfver.get('cross_host_equivalence_claimed') is False and sfver.get('executor_included_in_behavioral_pass') is False,'SFV behavioral evidence receipt mismatch')
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
    req('OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006' not in v,f'{p}:{".".join(loc)} stale SET_006 operative Foundation identity')
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
 print('behavioral_evidence PASS_REPLAYABLE_MODEL_HOST_EVIDENCE')
if __name__=='__main__':
 try:main()
 except (E,KeyError,StopIteration,IndexError) as e:
  print('R7 remediation validation: FAIL:',e,file=sys.stderr);raise SystemExit(1)
