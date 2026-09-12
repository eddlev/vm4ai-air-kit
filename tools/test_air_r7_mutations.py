from __future__ import annotations
import json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
VAL=Path(sys.argv[2] if len(sys.argv)>2 else 'tools/validate_air_r7_remediation.py').resolve()
def load(p):return json.loads(p.read_text())
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def run(r):return subprocess.run([sys.executable,str(VAL),str(r)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode
def jfn(mut):
 def f(p):
  o=load(p);mut(o);dump(p,o)
 return f
CASES=[]
def add(n,rel,fn):CASES.append((n,rel,fn))
add('R7-N01-CORE-CANDIDATE-LIFECYCLE-REMOVED','prompts/AIR_CORE_RUNTIME.md',lambda p:p.write_text(p.read_text().replace('Patch marker: AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1','Patch marker: REMOVED_R7_LIFECYCLE',1)))
add('R7-N02-INDEX-CANDIDATE-PREMATURE-RELEASE','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:o['entries'][0].__setitem__('availability_state','RELEASE_CATALOG_ENTRY')))
add('R7-N03-CEA-FOUNDATION-IDENTITY-STALE','profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT.json',jfn(lambda o:o['integration_refresh'].__setitem__('foundation_identity_state','OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_AIR_2_5_0_MII_CANDIDATE_SET_005')))
add('R7-N04-CEA-MANIFEST-STATUS-MIRROR-STALE','profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json',jfn(lambda o:o['components'][0].__setitem__('status','STALE_STATUS')))
add('R7-N05-GROUNDING-FOUNDATION-IDENTITY-STALE','profiles/grounding specialist/AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json',jfn(lambda o:o['integration_refresh'].__setitem__('foundation_identity_state','OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_AIR_2_5_0_MII_CANDIDATE_SET_005')))
add('R7-N06-GROUNDING-BEHAVIORAL-PASS-RESTORED','profiles/grounding specialist/AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json',jfn(lambda o:o['components'][0].__setitem__('availability_state','COORDINATED_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_FRESH_PROMPT_RUNTIME_BEHAVIORAL_REVALIDATION_PASS')))
add('R7-N07-GOVERNANCE-FOUNDATION-IDENTITY-STALE','profiles/governance specialist/AIR_AI_GOVERNANCE_SPECIALIST.json',jfn(lambda o:o['integration_refresh'].__setitem__('foundation_identity_state','OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_AIR_2_5_0_MII_CANDIDATE_SET_005')))
add('R7-N08-GOVERNANCE-BEHAVIORAL-PASS-RESTORED','profiles/governance specialist/AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json',jfn(lambda o:o['validation_state'].__setitem__('behavioral_revalidation','PASS_CURRENT_SESSION_PROMPT_RUNTIME_REPRESENTATIVE_SCENARIO_REVALIDATION')))
add('R7-N09-GOVERNANCE-ROLES-NULL','profiles/governance specialist/AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json',jfn(lambda o:o['failure_mode_integration_contract'].__setitem__('component_roles_observed',[None]*5)))
add('R7-N10-COPYWRITING-AVAILABILITY-STALE','profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json',jfn(lambda o:o['components'][0].__setitem__('availability_state','AVAILABLE_UNVALIDATED')))
add('R7-N11-SFV-FOUNDATION-IDENTITY-STALE','profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json',jfn(lambda o:o['integration_refresh'].__setitem__('foundation_identity_state','OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_AIR_2_5_0_MII_CANDIDATE_SET_005')))
add('R7-N12-SFV-BEHAVIORAL-PASS-RESTORED','profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json',jfn(lambda o:o['package_completion_contract'].__setitem__('package_state','PACKAGE_STRUCTURALLY_COMPLETE_STATIC_VALIDATED_AVAILABLE_UNBOUND_FRESH_PROMPT_RUNTIME_BEHAVIORAL_REVALIDATION_PASS')))
add('R7-N13-SFV-REQUIRED-PACKAGE-LITERAL-RESTORED','profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json',jfn(lambda o:o['validation_contract'].__setitem__('required_package_version','2.4.0')))
add('R7-N14-INDEX-HYBRID-COMPLETENESS-RESTORED','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:o['catalog_scope'].__setitem__('catalog_completeness_claim','COMPLETE_FOR_AIR_2_5_0_SET_005_V070_RELEASE_SPECIALIST_CATALOG')))
add('R7-N15-T7-HISTORY-REWRITTEN','profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json',jfn(lambda o:o['t7_change_record'].__setitem__('package_version','2.5.0')))
add('R7-N16-MANIFEST-RECEIPT-STALE','profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json',jfn(lambda o:o['components'][0].__setitem__('sha256','0'*64)))
add('R7-N17-RESEAL-HISTORY-GUARD-REMOVED','tools/reseal_air_candidate.py',lambda p:p.write_text(p.read_text().replace('if historical_path(path): return','if False: return',1)))
add('R7-N18-FLOOR028-MISSING','profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT.json',jfn(lambda o:o['foundation_compatibility']['required_floor_invariants'].remove('AIR-FLOOR-028-COGNITIVE-SCOPE-AUTHORITY-ISOLATION')))
add('R7-N19-COPYWRITING-COMPAT-STALE','profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST.json',jfn(lambda o:o['foundation_compatibility'].__setitem__('compatibility_state','COORDINATED_SET_005_RESEAL_STATIC_AND_FRESH_PROMPT_RUNTIME_BEHAVIORAL_REVALIDATION_PENDING')))
add('R7-N20-INDEX-HANDOFF-REV18-STALE','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:o['validation_state'].__setitem__('handoff_rev18_catalog_compatibility','STALE_REV17')))
if run(ROOT)!=0:raise SystemExit('R7-MUTATION-BASELINE failed')
print('R7-MUTATION-BASELINE: PASS')
with tempfile.TemporaryDirectory(prefix='air-r7-mutations-') as td:
 dst=Path(td)/'repo';shutil.copytree(ROOT,dst,ignore=shutil.ignore_patterns('.git','__pycache__'))
 originals={rel:(dst/rel).read_bytes() for _,rel,_ in CASES}
 for name,rel,fn in CASES:
  p=dst/rel;p.write_bytes(originals[rel]);fn(p)
  if run(dst)==0:
   print('MUTATION SURVIVED:',name,file=sys.stderr);raise SystemExit(1)
  print(name+': KILLED');p.write_bytes(originals[rel])
print(f'AIR R7 remediation mutation suite: PASS ({len(CASES)}/{len(CASES)} targeted mutants killed)')
