from __future__ import annotations
import json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); VAL=Path(sys.argv[2] if len(sys.argv)>2 else 'tools/validate_air_r5_remediation.py').resolve()
CA='profiles/capability ecology architect/'
def run(root): return subprocess.run([sys.executable,str(VAL),str(root)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode
def mutate_json(root,rel,fn):
 p=root/rel; o=json.load(open(p)); fn(o); p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def case(name,fn):
 with tempfile.TemporaryDirectory() as td:
  dst=Path(td)/'src'; shutil.copytree(ROOT,dst); fn(dst)
  if run(dst)==0: raise SystemExit(f'{name}: SURVIVED')
  print(name+': KILLED')
def main():
 if run(ROOT)!=0: raise SystemExit('R5-MUTATION-BASELINE: FAIL')
 print('R5-MUTATION-BASELINE: PASS')
 case('R5-N01-REGISTRY-REQUIRED-FIELDS-STALE',lambda r: mutate_json(r,CA+'AIR_DOMAIN_CAPABILITY_REGISTRY.json',lambda o:o['registry_schema'].__setitem__('required_domain_package_fields',o['registry_schema']['required_domain_package_fields'][:-1])))
 case('R5-N02-FIXTURE-PSEUDO-RESULT-FIELD',lambda r: mutate_json(r,CA+'AIR_DOMAIN_CAPABILITY_REGISTRY.json',lambda o:o['registry_schema'].__setitem__('fixture_wrapper_required_fields',o['registry_schema']['fixture_wrapper_required_fields']+['expected_validation_or_expected_decision'])))
 def n3(o):
  for f in o['detailed_domain_fixture_suite']['negative_fixtures']:
   for m in f['negative_mutations']:
    if m['path']=='knowledge_dimensions.PROCEDURAL': m['path']='knowledge_dimensions.procedural'; return
 case('R5-N03-CASE-MISMATCHED-MUTATION-PATH',lambda r: mutate_json(r,CA+'AIR_DOMAIN_CAPABILITY_REGISTRY.json',n3))
 def n4(o):
  k='uncertainty_resolution_requirements'; o['output_artifact']['required_fields'].remove(k); o['output_artifact']['required_translation_output_projection'].pop(k,None)
 case('R5-N04-TRANSLATOR-FINAL-OUTPUT-OMISSION',lambda r: mutate_json(r,CA+'AIR_HUMAN_TO_MACHINE_CAPABILITY_TRANSLATOR.json',n4))
 def n5(o): o['detailed_domain_package_construction_contract']['translator_to_canonical_package_mapping']['mappings'].pop('uncertainty_resolution_requirements')
 case('R5-N05-ARCHITECT-UNMAPPED-TRANSLATOR-OUTPUT',lambda r: mutate_json(r,CA+'AIR_CAPABILITY_ECOLOGY_ARCHITECT.json',n5))
 def n6(o): o['branch_contracts']['ACTIVE_TASK_CAPABILITY_ENVELOPE']['required_steps'][4]='M4_WHEN_TRIGGERED'
 case('R5-N06-NONEXISTENT-METHOD-STEP',lambda r: mutate_json(r,CA+'AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json',n6))
 def n7(o): o['handoff_requirements']['method_specific_state_schema']['required_fields'].remove('step_evidence_waiver_refs')
 case('R5-N07-UNTYPED-WAIVER-HANDOFF',lambda r: mutate_json(r,CA+'AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json',n7))
 print('AIR R5 remediation mutation suite: PASS (7/7 targeted mutants killed)')
if __name__=='__main__': main()
