from __future__ import annotations
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); VAL=ROOT/'tools/validate_air_handoff_runtime_contract.py'

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def run(root): return subprocess.run([sys.executable,str(root/'tools/validate_air_handoff_runtime_contract.py'),str(root)],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode

def mutate_text(rel,old,new):
 def f(d):
  p=d/rel; t=p.read_text(encoding='utf-8');
  if old not in t: raise RuntimeError('anchor missing '+old)
  p.write_text(t.replace(old,new,1),encoding='utf-8')
 return f

def mutate_json(rel,fn):
 def f(d):
  p=d/rel;o=load(p);fn(o);save(p,o)
 return f

CASES=[
 ('HC-MUT-01-CORE-CONTRACT-MARKER',mutate_text('prompts/AIR_CORE_RUNTIME.md','Patch marker: AIR_HANDOFF_RUNTIME_DURABILITY_AND_GENERATION_CONTRACT_V1','Patch marker: REMOVED_HANDOFF_RUNTIME_CONTRACT')),
 ('HC-MUT-02-SESSION-LIVE-OWNER',mutate_json('prompts/AIR_DEFAULT_STARTER_PROFILE.json',lambda o:o['compiler_contract']['handoff_runtime_durability_and_generation'].__setitem__('session_live_owner_path','AIR_HANDOFF_CARD.handoff_mode_state'))),
 ('HC-MUT-03-PROVIDER-ADAPTER',mutate_json('prompts/AIR_DEFAULT_STARTER_PROFILE.json',lambda o:o['compiler_contract']['handoff_runtime_durability_and_generation'].__setitem__('provider_adapter_contract','INFER_PROVIDER'))),
 ('HC-MUT-04-DUPLICATE-GENERATION-ROOT',mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json',lambda o:o['AIR_HANDOFF_CARD'].__setitem__('handoff_generation_evaluation',{}))),
 ('HC-MUT-05-GENERATION-OPERATOR',mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json',lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['validation_registry']['allowed_operators'].remove('HANDOFF_GENERATION_EVALUATION_VALID'))),
 ('HC-MUT-06-PORTABLE-OPERATOR',mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json',lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['validation_registry']['allowed_operators'].remove('PORTABLE_HANDOFF_STATE_VALID'))),
 ('HC-MUT-07-COMPOSITE-VALIDATOR',mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json',lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['validation_registry']['rules'].__setitem__('HC-VALIDATE-HANDOFF-MODE-PROVENANCE',{'operator':'HANDOFF_MODE_PROVENANCE_VALID','path':'$'}))),
 ('HC-MUT-08-ROUTE-LIVE-OWNER',mutate_json('catalog/AIR_RUNTIME_ROUTE_MAP.json',lambda o:next(r for r in o['routes'] if r['route_id']=='RT.HANDOFF_CREATE')['handoff_runtime_contract'].__setitem__('live_session_owner_path','AIR_HANDOFF_CARD.handoff_mode_state'))),
 ('HC-MUT-09-ROUTE-GENERATION-CARRIER',mutate_json('catalog/AIR_RUNTIME_ROUTE_MAP.json',lambda o:next(r for r in o['routes'] if r['route_id']=='RT.HANDOFF_CREATE')['handoff_runtime_contract'].__setitem__('generation_evaluation_serialized_carrier','AIR_HANDOFF_CARD.handoff_generation_evaluation'))),
 ('HC-MUT-10-STARTER-RECEIPT-FORMAL',mutate_json('prompts/AIR_DEFAULT_STARTER_PROFILE.json',lambda o:o['compiler_contract']['handoff_file_delivery']['receipt_contract'].__setitem__('formal_air_object',True))),
 ('HC-MUT-11-ROUTE-RECEIPT-FORMAL',mutate_json('catalog/AIR_RUNTIME_ROUTE_MAP.json',lambda o:next(r for r in o['routes'] if r['route_id']=='RT.HANDOFF_CREATE')['handoff_file_delivery']['receipt_contract'].__setitem__('formal_air_object',True))),
 ('HC-MUT-12-RESTORE-RENEGOTIATION',mutate_json('catalog/AIR_RUNTIME_ROUTE_MAP.json',lambda o:next(r for r in o['routes'] if r['route_id']=='RT.HANDOFF_RESTORE')['handoff_durability_restore_contract'].__setitem__('target_provider_discovery_required',False))),
 ('HC-MUT-13-CONTROL-DURABILITY-RENDERER',mutate_text('prompts/AIR_CONTROL_SURFACE.md','Patch marker: AIR_CONTROL_HANDOFF_RUNTIME_DURABILITY_RENDERER_V1','Patch marker: REMOVED_CONTROL_DURABILITY_RENDERER')),
 ('HC-MUT-14-REGISTRY-COVERAGE',mutate_json('prompts/AIR_DEFAULT_STARTER_PROFILE.json',lambda o:o['validation_contract']['deterministic_contract_registry']['coverage_contract'].__setitem__('declared_check_count',999))),
 ('HC-MUT-15-ROUTE-ROOT-LIVE-OWNER',mutate_json('catalog/AIR_RUNTIME_ROUTE_MAP.json',lambda o:o['handoff_runtime_contract_registry'].__setitem__('live_session_owner_path','AIR_HANDOFF_CARD.handoff_mode_state'))),
 ('HC-MUT-16-ROUTE-ROOT-RECEIPT-FORMAL',mutate_json('catalog/AIR_RUNTIME_ROUTE_MAP.json',lambda o:o['handoff_runtime_contract_registry']['receipt_contract'].__setitem__('formal_air_object',True)))
]

def main():
 if run(ROOT)!=0: raise SystemExit('mutation baseline failed')
 killed=0
 for name,fn in CASES:
  with tempfile.TemporaryDirectory(prefix='air-handoff-mut-') as td:
   d=Path(td)/'repo';shutil.copytree(ROOT,d);fn(d)
   if run(d)==0: raise SystemExit('MUTATION SURVIVED: '+name)
   killed+=1;print(name+': KILLED')
 print(f'AIR Handoff runtime mutation suite: PASS ({killed}/{len(CASES)} targeted mutants killed)')
if __name__=='__main__': main()
