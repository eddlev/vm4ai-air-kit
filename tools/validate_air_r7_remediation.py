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
CEA_PACKAGE='AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2'
GOV_PACKAGE='AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_V2'
GROUND_PACKAGE='AIR_GROUNDING_SPECIALIST_PACKAGE_V2'
CW_DIR='public surface copywriting specialist'
SFV_DIR='specification first verification specialist'
CEA_DIR='capability ecology architect'
GOV_DIR='governance specialist'
GROUND_DIR='grounding specialist'
CEA_COMPONENT_PASS_STATUS='V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND'
GOV_COMPONENT_PASS_STATUS='V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND'
SFV_COMPONENT_PASS_STATUS='V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND'
SFV_PACKAGE_PASS_STATE='PACKAGE_STRUCTURALLY_COMPLETE_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND_EXECUTOR_DRAFT_UNVALIDATED'
GROUND_COMPONENT_PASS_STATUS='V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND'
GROUND_PACKAGE_PASS_STATE='PACKAGE_STRUCTURALLY_COMPLETE_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND_EXECUTOR_DRAFT_UNVALIDATED'
SFV_BEHAVIORAL_COMPONENTS={'AIR_SPECIFICATION_FIRST_VERIFICATION_DOMAIN_PACKAGE.json','AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json','AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json'}
GOV_BEHAVIORAL_COMPONENTS={'AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json','AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json','AIR_AI_GOVERNANCE_SPECIALIST.json','AIR_AI_GOVERNANCE_METHOD_PACK.json'}
GROUND_BEHAVIORAL_COMPONENTS={'AIR_GROUNDING_DOMAIN_PACKAGE.json','AIR_GROUNDING_METHOD_PACK.json','AIR_GROUNDING_SPECIALIST.json'}
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
def validate_route_receipt(node,expected,label,require_full=False):
 fields=('version','sha256','size_bytes','line_count')
 if require_full:req(all(k in node for k in fields),f'{label}: Route Map receipt incomplete')
 for k in fields:
  if k in node:req(node.get(k)==expected[k],f'{label}: Route Map {k} receipt stale')
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
 route_path=ROOT/'catalog/AIR_RUNTIME_ROUTE_MAP.json';route_obj=parsed[route_path]
 route_version=route_obj.get('ROUTE_MAP_VERSION')
 req(isinstance(route_version,str) and route_version and route_obj.get('MAP_VERSION')==route_version,'Route Map version split mismatch')
 route_expected={'version':route_version,**meta(route_path)}
 core=(ROOT/'prompts/AIR_CORE_RUNTIME.md').read_text()
 req('Patch marker: AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1' in core,'006 Core candidate lifecycle marker missing')
 for tok in ['RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION','RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION','RELEASE_CATALOG_ENTRY']:
  req(tok in core,'006 Core lifecycle token missing '+tok)
 idx=parsed[ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json']
 req(idx.get('INDEX_VERSION')=='1.3.13','Grounding SET_008 behavioral promotion index version mismatch')
 req(idx['foundation_compatibility_catalog'].get('identity')==FOUNDATION_ID,'SET_008 catalog identity mismatch')
 req(idx['status']=='AIR_2_6_3_OBJECT_CONTRACT_SET_008_FIVE_PACKAGE_INDEX_V073_RELEASE_SEALED_REPLAYABLE_BEHAVIORAL_VALIDATED','v073 release-sealed index status incoherent')
 req(idx['catalog_scope']['catalog_completeness_claim']=='COMPLETE_FOR_AIR_2_6_3_OBJECT_CONTRACT_SET_008_V073_RELEASE_SPECIALIST_CATALOG','v073 release completeness identity incoherent')
 histrel=idx['catalog_scope'].get('historical_release_catalogs',[])
 req(histrel==[{'kit_release':'0.7.0','foundation_identity':'AIR_FOUNDATION_2_5_0_OBJECT_CONTRACT_SET_004','index_generation':'V070','catalog_completeness_claim':'COMPLETE_FOR_AIR_2_5_0_SET_004_V070_RELEASE_SPECIALIST_CATALOG','state':'RELEASED_HISTORICAL_NON_OPERATIVE'}],'073 v0.7.0 history not explicit/immutable')
 lc=idx.get('candidate_lifecycle_contract',{})
 req(lc.get('core_patch_marker')=='AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1','006 index lifecycle not bound to Core')
 req(lc.get('states')==['RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION','RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION','RELEASE_CATALOG_ENTRY'],'006 lifecycle state set mismatch')
 req(lc.get('current_candidate_state')==RELEASED and lc.get('candidate_states_are_release_sealed') is False,'006 release state semantics wrong')
 req(idx['validation_state'].get('static_validation')==STATIC_PASS,'R7 index static validation stage mismatch')
 req(idx['validation_state'].get('behavioral_revalidation')==BEHAVIOR_PASS,'R7 index behavioral state must reflect all-five replayable evidence pass')
 prog=idx['validation_state'].get('set008_static_revalidation_progress',{})
 req(prog.get('passed_package_identities')==[GOV_PACKAGE,CEA_PACKAGE,CW_PACKAGE,SFV_PACKAGE,GROUND_PACKAGE] and prog.get('passed_count')==5 and prog.get('pending_count')==0 and prog.get('behavioral_revalidation_ready_package_identities')==[] and prog.get('behavioral_revalidation_passed_package_identities')==[GOV_PACKAGE,CEA_PACKAGE,CW_PACKAGE,SFV_PACKAGE,GROUND_PACKAGE] and prog.get('behavioral_revalidation_passed_count')==5,'R7 SET_008 progress carrier mismatch')
 req(prog.get('pending_package_identities')==[],'R7 SET_008 pending package set mismatch')
 req(idx['validation_state'].get('release_publication_state')=='EXTERNAL_RELEASE_STATE_NOT_RUNTIME_AUTHORITY','R7 publication authority changed')
 for e in idx['entries']:
  if e['package_identity']==GOV_PACKAGE:
   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'Governance index Foundation identity not SET_008')
   req(e['availability_state']==RELEASED,'Governance index lifecycle not released after behavioral revalidation')
   req(e.get('current_foundation_compatibility_state')=='STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED_EXECUTOR_DRAFT_UNVALIDATED' and e.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'Governance SET_008 behavioral state mismatch')
   req(e.get('executor_component_state')=='DRAFT_AVAILABLE_UNVALIDATED','Governance Executor component boundary missing from index')
  elif e['package_identity']==CW_PACKAGE:
   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'Copywriting index Foundation identity not SET_008')
   req(e['availability_state']==RELEASED,'Copywriting index lifecycle not released after behavioral revalidation')
   req(e.get('current_foundation_compatibility_state')=='STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED' and e.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'Copywriting SET_008 behavioral state mismatch')
  elif e['package_identity']==SFV_PACKAGE:
   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'SFV index Foundation identity not SET_008')
   req(e['availability_state']==RELEASED,'SFV index lifecycle not released after behavioral revalidation')
   req(e.get('current_foundation_compatibility_state')=='STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED_EXECUTOR_DRAFT_UNVALIDATED' and e.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'SFV SET_008 behavioral state mismatch')
   req(e.get('executor_component_state')=='DRAFT_AVAILABLE_UNVALIDATED','SFV Executor component boundary missing from index')
  elif e['package_identity']==CEA_PACKAGE:
   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'CEA index Foundation identity not SET_008')
   req(e['availability_state']==RELEASED,'CEA index lifecycle not released after behavioral revalidation')
   req(e.get('current_foundation_compatibility_state')=='STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED' and e.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'CEA SET_008 behavioral state mismatch')
  elif e['package_identity']==GROUND_PACKAGE:
   req(e['foundation_compatibility_identity']==FOUNDATION_ID,'Grounding index Foundation identity not SET_008')
   req(e['availability_state']==RELEASED,'Grounding index lifecycle not released after behavioral revalidation')
   req(e.get('current_foundation_compatibility_state')=='STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED_EXECUTOR_DRAFT_UNVALIDATED' and e.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'Grounding SET_008 behavioral state mismatch')
   req(e.get('executor_component_state')=='DRAFT_AVAILABLE_UNVALIDATED','Grounding Executor component boundary missing from index')
  else:
   req(False,'unexpected Specialist package identity '+str(e.get('package_identity')))
 profile_count=0
 for p,o in parsed.items():
  if not str(p).startswith(str(ROOT/'profiles')):continue
  profile_count+=1
  fc=o.get('foundation_compatibility') if isinstance(o,dict) else None
  req(isinstance(fc,dict),f'{p}: foundation compatibility missing')
  is_cw=CW_DIR in str(p)
  is_sfv=SFV_DIR in str(p)
  is_cea=CEA_DIR in str(p)
  is_gov=GOV_DIR in str(p)
  is_ground=GROUND_DIR in str(p)
  is_set008=is_cw or is_sfv or is_cea or is_gov or is_ground
  expected_compat=SET008_SPECIALIST_COMPAT if is_set008 else SPECIALIST_COMPAT
  req(fc.get('compatibility_state')==expected_compat,f'{p}: stale Foundation compatibility state')
  if is_set008:
   req(fc.get('target_identity')==FOUNDATION_ID,f'{p}: SET_008 target identity missing')
   h=next((x for x in fc.get('required_files',[]) if x.get('filename')=='AIR_HANDOFF_CARD_TEMPLATE.json'),{})
   req(h.get('template_revision')==19 and h.get('revision_fields')==['template_revision','user_revision'] and 'card_revision' not in h,f'{p}: Handoff revision split stale')
   rr=fc.get('route_map_discovery_input') or fc.get('foundation_adjacent_route_map') or {}
   validate_route_receipt(rr,route_expected,str(p),True)
  req(SPECIALIST_REQUIRED_FLOORS.issubset(set(fc.get('required_floor_invariants',[]))),f'{p}: floors 027/028 missing')
  req(fc.get('cognitive_scope_authority_ref')=='AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION',f'{p}: Floor 028 reference missing')
  if p.name in SFV_BEHAVIORAL_COMPONENTS:
   req(status_of(p)==SFV_COMPONENT_PASS_STATUS,f'{p}: SFV behavioral component status mismatch')
   req(o.get('package_completion_contract',{}).get('package_state')==SFV_PACKAGE_PASS_STATE,f'{p}: SFV package completion state mismatch')
  if p.name in GOV_BEHAVIORAL_COMPONENTS:
   req(status_of(p)==GOV_COMPONENT_PASS_STATUS,f'{p}: Governance behavioral component status mismatch')
  if p.name in GROUND_BEHAVIORAL_COMPONENTS:
   req(status_of(p)==GROUND_COMPONENT_PASS_STATUS,f'{p}: Grounding behavioral component status mismatch')
   req(o.get('package_completion_contract',{}).get('package_state')==GROUND_PACKAGE_PASS_STATE,f'{p}: Grounding package completion state mismatch')
  if p.name=='AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json':
   req(o.get('STATUS')=='DRAFT',f'{p}: SFV Executor was promoted out of DRAFT')
  if p.name=='AIR_AI_GOVERNANCE_EXECUTOR.json':
   req(o.get('STATUS')=='DRAFT',f'{p}: Governance Executor was promoted out of DRAFT')
  if p.name=='AIR_GROUNDING_EXECUTOR.json':
   req(o.get('STATUS')=='DRAFT',f'{p}: Grounding Executor was promoted out of DRAFT')
 for p,o in parsed.items():
  for path,node in walk(o):
   if not isinstance(node,dict):continue
   ref=node.get('filename') or node.get('canonical_filename')
   designation=node.get('designation')
   if ref!='AIR_RUNTIME_ROUTE_MAP.json' and designation!='AIR_RUNTIME_ROUTE_MAP_V1':continue
   if not any(k in node for k in ('version','sha256','size_bytes','line_count')):continue
   label=f"{p}:{'.'.join(path) or '<root>'}"
   validate_route_receipt(node,route_expected,label,False)
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
   expected_state=SET008_FOUNDATION_STATE if (CW_DIR in str(p) or SFV_DIR in str(p) or CEA_DIR in str(p) or GOV_DIR in str(p) or GROUND_DIR in str(p)) else FOUNDATION_STATE
   req(ir['foundation_identity_state']==expected_state,f'{p}: stale current Foundation identity')
 req(count==21,f'current integration_refresh identity carrier count changed: {count}')
 mans=sorted(ROOT.glob('profiles/**/*PACKAGE_MANIFEST.json'))
 req(len(mans)==5,'manifest count !=5')
 for p in mans:
  o=parsed[p]
  st=str(o.get('status') or '')
  is_cw=CW_DIR in str(p)
  is_sfv=SFV_DIR in str(p)
  is_cea=CEA_DIR in str(p)
  is_ground=GROUND_DIR in str(p)
  if is_ground or is_cw or is_sfv or is_cea or (GOV_DIR in str(p)):req('STATIC_VALIDATED' in st and 'REPLAYABLE_BEHAVIORAL_VALIDATED' in st and 'BEHAVIORAL_REVALIDATION_PENDING' not in st,f'{p}: SET_008 behavioral-pass lifecycle missing')
  else:req(False,f'{p}: unexpected manifest package')
  pvs=o.get('package_validation_state',{})
  static_keys=[k for k in ('t7_static_validation','coordinated_reseal_static_validation','static_design_validation') if k in pvs]
  req(static_keys,f'{p}: no static validation carrier')
  for k in static_keys:req(pvs[k]==STATIC_PASS,f'{p}: {k} not static PASS')
  if 'behavioral_revalidation' in pvs:req(pvs['behavioral_revalidation']==(BEHAVIOR_PASS if (is_ground or is_cw or is_sfv or is_cea or (GOV_DIR in str(p))) else BEHAVIOR_PENDING),f'{p}: behavioral validation state mismatch')
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
 groundman=parsed[ROOT/'profiles/grounding specialist/AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json']
 req(groundman['foundation_compatibility'].get('target_identity')==FOUNDATION_ID and groundman['foundation_compatibility'].get('compatibility_state')==SET008_SPECIALIST_COMPAT,'Grounding manifest SET_008 compatibility missing')
 gmpvs=groundman.get('package_validation_state',{})
 req(gmpvs.get('behavioral_revalidation')==BEHAVIOR_PASS and gmpvs.get('component_internal_foundation_compatibility')=='PASS_SET_008_EXACT_RECEIPTS' and gmpvs.get('executor_validation_state')=='DRAFT_AVAILABLE_UNVALIDATED_EXCLUDED_FROM_BEHAVIORAL_PASS','Grounding manifest validation state mismatch')
 groundexec=parsed[ROOT/'profiles/grounding specialist/AIR_GROUNDING_EXECUTOR.json']
 req(groundexec.get('STATUS')=='DRAFT','Grounding Executor was promoted out of DRAFT')
 groundentry=next(e for e in idx['entries'] if e['package_identity']==GROUND_PACKAGE)
 req(groundentry.get('availability_state')==RELEASED and groundentry.get('foundation_compatibility_identity')==FOUNDATION_ID and groundentry.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'Grounding index behavioral promotion mismatch')
 groundevp=ROOT/'tests/AIR_GROUNDING_SET008_BEHAVIORAL_EVIDENCE_V1.json'; req(groundevp.is_file(),'Grounding behavioral evidence file missing'); groundev=load(groundevp); grounder=groundman.get('behavioral_evidence_receipt',{})
 req(meta(groundevp)['sha256']=='77fd1409d8fde79c3e8169f9823cd5b3fdd0a97fc8eea5e9f7ca303f3add2c92' and grounder.get('sha256')=='77fd1409d8fde79c3e8169f9823cd5b3fdd0a97fc8eea5e9f7ca303f3add2c92','Grounding behavioral evidence hash mismatch')
 req(groundev.get('evidence_id')=='AIR_BEHAVIORAL_EVIDENCE_GROUNDING_SET008_20260915_V1' and groundev.get('summary',{}).get('pass_count')==6 and groundev.get('summary',{}).get('scenario_count')==6 and groundev.get('summary',{}).get('behavioral_revalidation_result')=='PASS_ON_CURRENT_MODEL_HOST','Grounding behavioral evidence result mismatch')
 req(grounder.get('result')==BEHAVIOR_PASS and grounder.get('model_host')=='ChatGPT / GPT-5.6 Sol' and grounder.get('cross_host_equivalence_claimed') is False and grounder.get('executor_included_in_behavioral_pass') is False,'Grounding behavioral evidence receipt mismatch')
 groundentry=next(e for e in idx['entries'] if e['package_identity']==GROUND_PACKAGE)
 req(groundentry.get('availability_state')==RELEASED and groundentry.get('foundation_compatibility_identity')==FOUNDATION_ID and groundentry.get('behavioral_revalidation_state')==BEHAVIOR_PASS and groundentry.get('executor_component_state')=='DRAFT_AVAILABLE_UNVALIDATED','Grounding index behavioral promotion mismatch')
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
 gpvs=gov.get('package_validation_state',{})
 req(gpvs.get('behavioral_revalidation')==BEHAVIOR_PASS and gpvs.get('component_internal_foundation_compatibility')=='PASS_SET_008_EXACT_RECEIPTS' and gpvs.get('executor_validation_state')=='DRAFT_AVAILABLE_UNVALIDATED_EXCLUDED_FROM_BEHAVIORAL_PASS','Governance manifest behavioral validation state mismatch')
 for fn in ['AIR_AI_GOVERNANCE_DOMAIN_PACKAGE.json','AIR_AI_GOVERNANCE_AGENTIC_OVERLAY.json','AIR_AI_GOVERNANCE_SPECIALIST.json','AIR_AI_GOVERNANCE_METHOD_PACK.json']: req(status_of(ROOT/'profiles/governance specialist'/fn)==GOV_COMPONENT_PASS_STATUS,f'Governance behavioral component status mismatch {fn}')
 govexec=parsed[ROOT/'profiles/governance specialist/AIR_AI_GOVERNANCE_EXECUTOR.json']; req(govexec.get('STATUS')=='DRAFT','Governance Executor was promoted out of DRAFT')
 goventry=next(e for e in idx['entries'] if e['package_identity']==GOV_PACKAGE); req(goventry.get('availability_state')==RELEASED and goventry.get('behavioral_revalidation_state')==BEHAVIOR_PASS and goventry.get('executor_component_state')=='DRAFT_AVAILABLE_UNVALIDATED','Governance index behavioral promotion mismatch')
 govevp=ROOT/'tests/AIR_AI_GOVERNANCE_SET008_BEHAVIORAL_EVIDENCE_V1.json'; req(govevp.is_file(),'Governance behavioral evidence file missing'); govev=load(govevp); gover=gov.get('behavioral_evidence_receipt',{})
 req(meta(govevp)['sha256']=='7b568dfd9ea04e247b4b4b425af34e616765af0ad86c70a716e96c9629ebd3e9' and gover.get('sha256')=='7b568dfd9ea04e247b4b4b425af34e616765af0ad86c70a716e96c9629ebd3e9','Governance behavioral evidence hash mismatch')
 req(govev.get('evidence_id')=='AIR_BEHAVIORAL_EVIDENCE_AI_GOVERNANCE_SET008_20260915_V1' and govev.get('summary',{}).get('pass_count')==6 and govev.get('summary',{}).get('scenario_count')==6 and govev.get('summary',{}).get('behavioral_revalidation_result')=='PASS_ON_CURRENT_MODEL_HOST','Governance behavioral evidence result mismatch')
 req(gover.get('result')==BEHAVIOR_PASS and gover.get('model_host')=='ChatGPT / GPT-5.6 Sol' and gover.get('cross_host_equivalence_claimed') is False and gover.get('executor_included_in_behavioral_pass') is False,'Governance behavioral evidence receipt mismatch')
 sfv=parsed[ROOT/'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json']
 vc=sfv['validation_contract']
 req('required_package_version' not in vc,'061 stale duplicate required_package_version remains')
 req(vc.get('required_package_version_source')=='$.package_version' and vc.get('required_package_version_check')=='EQUAL_TO_CANONICAL_TOP_LEVEL_PACKAGE_VERSION','061 canonical package version reference missing')
 req(sfv.get('package_version')=='2.5.0','061 current package_version changed')
 cea=parsed[ROOT/'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json']
 req(cea['foundation_compatibility'].get('target_identity')==FOUNDATION_ID and cea['foundation_compatibility'].get('compatibility_state')==SET008_SPECIALIST_COMPAT,'CEA manifest SET_008 compatibility missing')
 ceapvs=cea.get('package_validation_state',{})
 req(ceapvs.get('behavioral_revalidation')==BEHAVIOR_PASS and ceapvs.get('component_internal_foundation_compatibility')=='PASS_SET_008_EXACT_RECEIPTS','CEA manifest behavioral validation state mismatch')
 for fn in ['AIR_DOMAIN_CAPABILITY_REGISTRY.json', 'AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json', 'AIR_CAPABILITY_ECOLOGY_ARCHITECT.json', 'AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json']: req(status_of(ROOT/'profiles/capability ecology architect'/fn)==CEA_COMPONENT_PASS_STATUS,f'CEA behavioral component status mismatch {fn}')
 ceaevp=ROOT/'tests/AIR_CAPABILITY_ECOLOGY_ARCHITECT_SET008_BEHAVIORAL_EVIDENCE_V1.json'; req(ceaevp.is_file(),'CEA behavioral evidence file missing'); ceaev=load(ceaevp); ceaer=cea.get('behavioral_evidence_receipt',{})
 req(meta(ceaevp)['sha256']=='4779e1e48a4b9b614c66e892c7bf964fcabcd4b04bfae41af2bddbb01564307d' and ceaer.get('sha256')=='4779e1e48a4b9b614c66e892c7bf964fcabcd4b04bfae41af2bddbb01564307d','CEA behavioral evidence hash mismatch')
 req(ceaev.get('evidence_id')=='AIR_BEHAVIORAL_EVIDENCE_CAPABILITY_ECOLOGY_ARCHITECT_SET008_20260915_V1' and ceaev.get('summary',{}).get('pass_count')==6 and ceaev.get('summary',{}).get('scenario_count')==6 and ceaev.get('summary',{}).get('behavioral_revalidation_result')=='PASS_ON_CURRENT_MODEL_HOST','CEA behavioral evidence result mismatch')
 req(ceaer.get('result')==BEHAVIOR_PASS and ceaer.get('model_host')=='ChatGPT / GPT-5.6 Sol' and ceaer.get('cross_host_equivalence_claimed') is False,'CEA behavioral evidence receipt mismatch')
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
