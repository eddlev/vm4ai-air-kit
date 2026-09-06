from __future__ import annotations
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path('.').resolve(); PY=sys.executable

def run_mut(name, mutate):
    with tempfile.TemporaryDirectory() as td:
        dst=Path(td)/'repo'; shutil.copytree(ROOT,dst,ignore=shutil.ignore_patterns('.git','__pycache__'))
        mutate(dst)
        p=subprocess.run([PY,'tools/validate_air_control_plane.py'],cwd=dst,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if p.returncode==0: raise SystemExit('mutation survived: '+name)
        print('KILLED',name)

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def main():
    cases=[]
    def m1(d):
        p=d/'catalog/AIR_RUNTIME_ROUTE_MAP.json'; o=load(p); next(r for r in o['routes'] if r['route_id']=='RT.ACTION').pop('control_event_ref',None); save(p,o)
    cases.append(('missing route control_event_ref',m1))
    def m2(d):
        p=d/'catalog/AIR_RUNTIME_ROUTE_MAP.json'; o=load(p); next(r for r in o['routes'] if r['route_id']=='RT.ACTION')['trigger_authority']='OPERATIVE_NATURAL_LANGUAGE'; save(p,o)
    cases.append(('operative natural-language trigger',m2))
    def m3(d):
        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['approval_response_resolution']['natural_language_paraphrase_authority']='ALLOW'; save(p,o)
    cases.append(('natural-language approval authority',m3))
    def m4(d):
        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); s=o['compiler_contract']['material_action_transaction']['ordered_pre_and_post_effect_states']; s.remove('AUTHORITY_OBJECTS_LEDGER_COMMITTED'); save(p,o)
    cases.append(('missing authority ledger barrier',m4))
    def m5(d):
        p=d/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; o=load(p); o['AIR_HANDOFF_CARD']['schema_manifest']['strict_output_mode']='RAW_ONE_ROOT_JSON_NO_FENCE_NO_PROSE'; save(p,o)
    cases.append(('inline handoff mode',m5))
    def m6(d):
        p=d/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; o=load(p); o['AIR_HANDOFF_CARD']['schema_manifest']['required_fields'].remove('failure_mode_state'); save(p,o)
    cases.append(('handoff omits failure_mode_state',m6))
    def m7(d):
        p=d/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; o=load(p); o['AIR_HANDOFF_CARD']['schema_manifest']['conditional_rules'][0]['condition_authority']='OPERATIVE_NATURAL_LANGUAGE'; save(p,o)
    cases.append(('operative handoff semantic condition',m7))
    def m8(d):
        p=next(d.glob('profiles/**/*PACKAGE_MANIFEST.json')); o=load(p); o.pop('failure_mode_integration_contract',None); save(p,o)
    cases.append(('Specialist package missing failure integration',m8))
    def m9(d):
        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['failure_mode_registry']['automatic_applicability']='SEMANTIC_SIMILARITY'; save(p,o)
    cases.append(('semantic failure applicability',m9))
    def m10(d):
        p=d/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; o=load(p); o['AIR_HANDOFF_CARD']['action_governance_state']['provenance_policy']['surfaced_object_ledger_required']=False; save(p,o)
    cases.append(('handoff history without ledger',m10))

    def m11(d):
        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['failure_mode_registry']['applicability_signature_schema']['exact_match_rule']='SEMANTIC_SIMILARITY'; save(p,o)
    cases.append(('failure signature hash matching removed',m11))
    def m12(d):
        p=next(d.glob('profiles/**/*PACKAGE_MANIFEST.json')); o=load(p); o['failure_mode_integration_contract']['exact_match_rule']='PARTIAL_SEMANTIC_MATCH'; save(p,o)
    cases.append(('Specialist exact failure signature matching removed',m12))

    def m13(d):
        p=d/'prompts/AIR_CORE_RUNTIME.md'; x=p.read_text(encoding='utf-8'); x=x.replace('AIR_SURFACED_OBJECT_LEDGER allowed object-owned top-level fields:','AIR_SURFACED_OBJECT_LEDGER schema removed:'); p.write_text(x,encoding='utf-8')
    cases.append(('surfaced ledger closed-world schema removed',m13))
    def m14(d):
        p=d/'prompts/AIR_CONTROL_SURFACE.md'; x=p.read_text(encoding='utf-8'); x=x.replace('AIR_HANDOFF_CARD output remains downloadable JSON-file-only. Do not inline the card payload.','Strict AIR_HANDOFF_CARD output remains raw JSON only.'); p.write_text(x,encoding='utf-8')
    cases.append(('stale inline Handoff exception reintroduced',m14))
    for n,f in cases: run_mut(n,f)
    print('AIR semantic-loophole mutation suite: PASS',len(cases),'/',len(cases))
if __name__=='__main__': main()
