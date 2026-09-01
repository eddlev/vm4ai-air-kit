#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CORE=ROOT/'prompts/AIR_CORE_RUNTIME.md'
CONTROL=ROOT/'prompts/AIR_CONTROL_SURFACE.md'
STARTER=ROOT/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'
HANDOFF=ROOT/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'

CANONICAL=[
'AIR_RUNTIME_BRIDGE','AIR_SESSION','AIR_PROJECT_INITIALIZATION_BRIEF','AIR_PROJECT_EXECUTION_MAP',
'AIR_ARTIFACT','AIR_ACTIVE_CONTRACT','AIR_GATE','AIR_VALIDATION_REPORT','AIR_ALIGNMENT_CHECK',
'AIR_ERROR','AIR_ACTION_AUTHORIZATION','AIR_ACTION_RECEIPT','AIR_PRIOR_EFFECT_RECORD',
'AIR_REQUIRED_INPUT_REQUEST','AIR_HANDOFF_CARD']

fail=[]
def req(ok,msg):
    if not ok: fail.append(msg)

def strict(path):
    dup=[]
    def hook(pairs):
        d={}
        for k,v in pairs:
            if k in d: dup.append(k)
            d[k]=v
        return d
    obj=json.loads(path.read_text('utf-8'), object_pairs_hook=hook)
    req(not dup,f'{path.name}: duplicate JSON keys {sorted(set(dup))}')
    return obj

def bullet_set(text,start_phrase,end_phrase):
    s=text.index(start_phrase)+len(start_phrase)
    e=text.index(end_phrase,s)
    return [m.group(1).strip() for m in re.finditer(r'^-\s+(AIR_[A-Z0-9_]+)\s*$',text[s:e],re.M)]

core=CORE.read_text('utf-8')
control=CONTROL.read_text('utf-8')
starter=strict(STARTER)
handoff=strict(HANDOFF)['AIR_HANDOFF_CARD']

req('AIR_CANONICAL_OBJECT_CONTRACTS_V4' in core,'Core canonical object registry is not V4')
req('AIR_OBJECT_RESPONSIBILITY_CLOSURE_V1' in core,'Core responsibility closure marker missing')
req('OBJECT_SCHEMA_FIELD_OWNERSHIP_VIOLATION' in core,'Core foreign-field failure class missing')
req('The top-level AIR object root name identifies semantic object identity.' in core,'Core object identity rule missing')
req('record_class identifies the semantic record category' in core,'Core record_class category rule missing')
req('AIR_PRIMED_ONBOARDING' not in core,'Core still reserves non-canonical AIR_PRIMED_ONBOARDING')
req('AIR_PRIMED_ONBOARDING' not in control,'Control still reserves non-canonical AIR_PRIMED_ONBOARDING')

# Canonical registry set from Core class list.
sec=core[core.index('Canonical formal object classes:'):core.index('Object identity and record category:')]
core_objs=re.findall(r'^-\s+(AIR_[A-Z0-9_]+):\s+[A-Z_]+\s*$',sec,re.M)
req(core_objs==CANONICAL,f'Core canonical object order/set mismatch: {core_objs}')

core_reserved=bullet_set(core,'Reserved formal object labels include:','AIR must not use reserved formal object labels')
control_reserved=bullet_set(control,'Reserved labels:','In compact interaction')
req(core_reserved==CANONICAL,f'Core reserved labels mismatch: {core_reserved}')
req(control_reserved==CANONICAL,f'Control reserved labels mismatch: {control_reserved}')

for marker in ['AIR_GATE_V3','AIR_ACTION_AUTHORIZATION exact schema:','AIR_ACTION_RECEIPT exact schema:','AIR_PRIOR_EFFECT_RECORD exact schema:']:
    req(marker in core,f'Core exact object contract marker missing: {marker}')
for retired in ['scope_in, scope_out, prohibited_actions, required_evidence, rescope_rule, and binding_state']:
    req(retired in core,'Active Contract alias retirement rule missing')

fo=starter['typed_registries']['formal_objects']
req(fo.get('registry_owner')=='AIR_CORE_RUNTIME_V2','Starter formal-object registry owner drift')
req(fo.get('registry_designation')=='AIR_CANONICAL_OBJECT_CONTRACTS_V4','Starter registry designation drift')
req(fo.get('object_ids')==CANONICAL,'Starter canonical object IDs differ from Core')
req(fo.get('top_level_schema_rule')=='CLOSED_WORLD_CORE_OWNED_FIELDS_ONLY','Starter closed-world consumer rule missing')
req(fo.get('foreign_field_rule')=='UNKNOWN_ALIAS_OR_WRONG_OBJECT_TOP_LEVEL_FIELD_IS_OBJECT_SCHEMA_FIELD_OWNERSHIP_VIOLATION','Starter foreign-field rule missing')

af=starter['typed_registries']['artifact_fields']
req(isinstance(af,dict) and af.get('semantic_fields_redeclared') is False,'Starter still redeclares Core Artifact base fields')
req(af.get('source_marker')=='AIR_OBJECT_RESPONSIBILITY_CLOSURE_V1','Starter Artifact registry source marker drift')

formal=set(CANONICAL)
for r in starter['typed_registries']['conditional_requirements']:
    for f in r.get('fields',[]):
        req(f not in formal,f"Starter requirement {r.get('id')} embeds formal object label as field: {f}")

byid={r['id']:r for r in starter['typed_registries']['conditional_requirements']}
for rid in ['REQ-PATCH-ARTIFACT','REQ-PATCH-VALIDATION','REQ-TEST-EVIDENCE-BRIEF','REQ-TEST-EVIDENCE-MAP','REQ-TEST-EVIDENCE-ARTIFACT','REQ-TEST-EVIDENCE-VALIDATION','REQ-MATERIAL-ACTION-AUTHORIZATION','REQ-MATERIAL-ACTION-RECEIPT','REQ-UNBOUND-PRIOR-EFFECT-RECORD']:
    req(rid in byid,f'Starter split ownership requirement missing: {rid}')
req('mutation_scope' not in byid['REQ-PATCH-VALIDATION']['fields'],'Validation Report still owns mutation_scope')
req('delivery_receipts' not in byid['REQ-PATCH-VALIDATION']['fields'],'Validation Report still owns delivery receipts')
req(byid['REQ-VTT']['plane']=='AIR_ARTIFACT','VTT state still leaks into Gate plane')
req('approval_scope' not in byid['REQ-GOV']['fields'],'Governance extension duplicates Artifact execution_contract approval_scope')

req(handoff.get('card_revision')==14,'Handoff current template revision is not 14')
toc=handoff.get('transfer_ownership_contract')
req(isinstance(toc,dict),'Handoff transfer_ownership_contract missing')
if isinstance(toc,dict):
    req(toc.get('contract_version')=='1.0.0','Handoff transfer ownership version drift')
    carriers=toc.get('canonical_transfer_carriers',{})
    for k in ['current_task_binding','current_orbit_state','current_receiver_delivery_state','current_action_history_and_unresolved_effects','current_runtime_alignment_transfer_state']:
        req(k in carriers,f'Handoff canonical transfer carrier missing: {k}')
req('transfer_ownership_contract' in handoff['schema_manifest'].get('optional_fields',[]),'Handoff schema manifest does not declare transfer_ownership_contract')
req(any(x.get('id')=='HC-COND-OBJECT-RESPONSIBILITY-REV14' for x in handoff['schema_manifest'].get('conditional_rules',[])),'Handoff rev14 ownership conditional rule missing')

if fail:
    print(f'{len(fail)} object-contract checks FAILED')
    for x in fail: print('FAIL:',x)
    sys.exit(1)
print('AIR formal-object responsibility closure PASS: 15/15 canonical object identities covered; closed-world ownership guards active')
