from __future__ import annotations
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
VALIDATOR=Path(sys.argv[2] if len(sys.argv)>2 else 'tools/validate_air_r8_remediation.py').resolve()

def run(root:Path):
    return subprocess.run([sys.executable,str(VALIDATOR),str(root)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

def writej(p:Path,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def mutate_text(t:Path, rel:str, old:str,new:str,count:int=1):
    p=t/rel; s=p.read_text(encoding='utf-8')
    if old not in s: raise SystemExit(f'mutation source missing {old!r} in {rel}')
    p.write_text(s.replace(old,new,count),encoding='utf-8')

def case(name, mut, expect):
    with tempfile.TemporaryDirectory() as td:
        t=Path(td)
        shutil.copytree(ROOT/'prompts',t/'prompts')
        mut(t)
        p=run(t)
        if p.returncode==0: raise SystemExit(f'{name}: SURVIVED')
        if expect not in p.stdout: raise SystemExit(f'{name}: wrong failure; expected {expect!r}; got {p.stdout!r}')
        print(name+': KILLED')

base=run(ROOT)
if base.returncode: raise SystemExit('R8-MUTATION-BASELINE FAIL: '+base.stdout)
print('R8-MUTATION-BASELINE: PASS')

CORE='prompts/AIR_CORE_RUNTIME.md'; CONTROL='prompts/AIR_CONTROL_SURFACE.md'; STARTER='prompts/AIR_DEFAULT_STARTER_PROFILE.json'; HANDOFF='prompts/AIR_HANDOFF_CARD_TEMPLATE.json'
REFCORE='AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-CORE].expected'
REFCONTROL='AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-CONTROL].expected'
PROFILE='AIR_TARGET_PLATFORM_NORMALIZATION_PORTABLE_V1'

case('R8-N01-CORE-SENTINEL-TYPED-REF-REMOVED',lambda t:mutate_text(t,CORE,REFCORE,'MISSING_TYPED_SENTINEL_REF'), 'sentinel declaration does not resolve all typed expectations')
case('R8-N02-CONTROL-SENTINEL-TYPED-REF-REMOVED',lambda t:mutate_text(t,CONTROL,REFCONTROL,'MISSING_TYPED_SENTINEL_REF'), 'Control sentinel declaration does not resolve typed expectation')
case('R8-N03-CONTROL-CORE-BOOT-MARK-OWNERSHIP-REMOVED',lambda t:mutate_text(t,CONTROL,'patch marker AIR_BOOT_BRAND_MARK_M2','patch marker BROKEN_BOOT_MARK_OWNER'), 'Control boot mark is not Core-owned')
case('R8-N04-CONTROL-THREE-LINE-BOOT-VARIANT-RESTORED',lambda t:mutate_text(t,CONTROL,'Core-owned canonical boot mark','full three-line boot mark',1), 'old boot mark variant remains')
case('R8-N05-Q1D-EVIDENCE-MODIFIER-OMITTED',lambda t:mutate_text(t,CORE,'   - air -t off: use standard evidence presentation; default','   - air -t OMITTED: use standard evidence presentation; default',1), 'Q1D modifier set incomplete')
case('R8-N06-Q1D-FOUR-MODIFIER-WORDING-REGRESSED',lambda t:mutate_text(t,CORE,'explain all four canonical system modifiers','explain only the two system modifiers',1), 'Q1D four-modifier wording missing')
case('R8-N07-CORE-UNICODE-FORM-NFC',lambda t:mutate_text(t,CORE,'Unicode normalization form: NFKC.','Unicode normalization form: NFC.',1), 'Core NFKC normalization form missing')
case('R8-N08-CORE-TARGET-PROFILE-MUTATED',lambda t:mutate_text(t,CORE,f'target-platform normalization profile: {PROFILE}.','target-platform normalization profile: BROKEN_PROFILE.',1), 'Core target-platform profile missing')

def starter_profile(t):
    p=t/STARTER; o=json.loads(p.read_text(encoding='utf-8')); o['local_profile_policies']['file_identity_and_delivery']['target_platform_normalization_profile']='BROKEN_PROFILE'; writej(p,o)
case('R8-N09-STARTER-TARGET-PROFILE-MUTATED',starter_profile,'Starter target-platform profile mismatch')

def handoff_unknown(t):
    p=t/HANDOFF; o=json.loads(p.read_text(encoding='utf-8')); o['AIR_HANDOFF_CARD']['platform_state']['unknown_target_platform_behavior']='INFER_PLATFORM'; writej(p,o)
case('R8-N10-HANDOFF-UNKNOWN-TARGET-NOT-FAIL-CLOSED',handoff_unknown,'Handoff unknown-target behavior mismatch')

def reserved_missing(t):
    p=t/STARTER; o=json.loads(p.read_text(encoding='utf-8')); a=o['validation_contract']['deterministic_contract_registry']['checks']; c=next(x for x in a if x['check_id']=='DC-FOUNDATION-NORMALIZED-COLLISION'); c['portable_reserved_basename_stems'].remove('CON'); writej(p,o)
case('R8-N11-PORTABLE-RESERVED-NAME-SET-INCOMPLETE',reserved_missing,'portable reserved basename set mismatch')

def handoff_resolution(t):
    p=t/HANDOFF; o=json.loads(p.read_text(encoding='utf-8')); o['AIR_HANDOFF_CARD']['file_identity_and_delivery_state']['target_platform_profile_resolution_state']='UNKNOWN_PERMISSIVE'; writej(p,o)
case('R8-N12-HANDOFF-TARGET-PROFILE-RESOLUTION-WEAKENED',handoff_resolution,'Handoff target profile resolution state mismatch')

print('AIR R8 remediation mutation suite: PASS (12/12 targeted mutants killed)')
