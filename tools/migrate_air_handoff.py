from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path
from typing import Any

class MigrationError(Exception): pass

def load_json(path: Path)->Any:
    return json.loads(path.read_text(encoding='utf-8'))

def canonical_sha(obj: Any)->str:
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def migrate_rev15_to_rev16(doc: dict[str,Any], current_template_doc: dict[str,Any])->dict[str,Any]:
    if set(doc)!= {'AIR_HANDOFF_CARD'}: raise MigrationError('expected exactly one AIR_HANDOFF_CARD root')
    if set(current_template_doc)!= {'AIR_HANDOFF_CARD'}: raise MigrationError('current template root invalid')
    src=doc['AIR_HANDOFF_CARD']; tmpl=current_template_doc['AIR_HANDOFF_CARD']
    if src.get('schema_version')!='2.3.0' or src.get('SCHEMA_VERSION')!='2.3.0': raise MigrationError('source is not schema 2.3.0')
    if src.get('card_revision')!=15: raise MigrationError('source card_revision is not 15')
    contract=tmpl.get('schema_manifest',{}).get('revision_migration_contracts',{}).get('REV15_TO_REV16')
    if not contract or contract.get('apply_before_current_required_carrier_check') is not True: raise MigrationError('current rev16 migration contract missing')
    out=copy.deepcopy(doc); c=out['AIR_HANDOFF_CARD']
    source_manifest_digest=canonical_sha(src.get('schema_manifest',{}))
    c['card_revision']=16
    lf=copy.deepcopy(contract['failure_mode_state_template'])
    ll=copy.deepcopy(contract['surfaced_object_ledger_state_template'])
    c.setdefault('failure_mode_state',lf)
    c.setdefault('surfaced_object_ledger_state',ll)
    if 'object_visibility_authority_state' not in c:
        va=copy.deepcopy(tmpl['object_visibility_authority_state'])
        if c.get('object_visibility_mode')=='MINIMUM_REQUIRED_OBJECTS':
            va['authority_source']='LEGACY_UNVERIFIED_SELECTION'
            va['selection_evidence_ref']=None
            va['restoration_state']='REVIEW_REQUIRED_CLAMP_TO_ALL_OBJECTS'
        else:
            va['authority_source']='IMMUTABLE_DEFAULT_BASELINE'
            va['selection_evidence_ref']=None
            va['restoration_state']='MIGRATED_DEFAULT_PENDING_CURRENT_VALIDATION'
        c['object_visibility_authority_state']=va
    if 'profile_posture_acceptance_state' not in c:
        pa=copy.deepcopy(tmpl['profile_posture_acceptance_state'])
        pa['accepted_weaker_postures']=[]
        pa['history_state']='LEGACY_UNRECORDED_PRE_REV16'
        pa['restoration_state']='CLAMP_TO_DEFAULT_STARTER_BASELINE_PENDING_CURRENT_VALIDATION'
        c['profile_posture_acceptance_state']=pa
    mh=c.get('execution_state',{}).get('method_handoff_state')
    if isinstance(mh,dict):
        mh.setdefault('method_specific_state_schema_ref',None)
        mh.setdefault('method_specific_state_schema_version',None)
    ps=c.get('execution_state',{}).get('patch_state')
    if isinstance(ps,dict): ps.setdefault('patch_activity_state','NOT_ACTIVE')
    ss=c.get('source_state')
    if isinstance(ss,dict):
        ss.setdefault('source_rights_projection_contract',copy.deepcopy(tmpl['source_state']['source_rights_projection_contract']))
        if ss.get('source_rights_state') or c.get('governance_state',{}).get('governance_source_rights_state'):
            ss['source_rights_projection_contract']['reconciliation_state']='LEGACY_REVIEW_REQUIRED'
        else:
            ss['source_rights_projection_contract']['reconciliation_state']='NOT_APPLICABLE_EMPTY_STATE'
    old_ms=c.get('migration_state') if isinstance(c.get('migration_state'),dict) else {}
    ms=copy.deepcopy(tmpl['migration_state'])
    if isinstance(old_ms,dict):
        for k in ['legacy_q4_c_state','legacy_q4_d_state','legacy_prompt_mode_state','legacy_orbit_state','legacy_active_contract_state','legacy_governance_state','unresolved_legacy_states']:
            if k in old_ms: ms[k]=copy.deepcopy(old_ms[k])
    ms['source_schema_version']='2.3.0'
    ms['source_card_revision']=15
    ms['migration_required']=True
    ms['migration_decision']='MIGRATED_REV15_TO_REV16_PENDING_CURRENT_ALIGNMENT_AND_REBINDING'
    ms['revision_migration_path']='REV15_TO_REV16'
    ms['legacy_history_state']={
        'source_card_revision':15,
        'failure_mode_history':'LEGACY_UNRECORDED_PRE_REV16',
        'surfaced_object_history':'LEGACY_UNRECORDED_PRE_REV16',
        'history_synthesis':'PROHIBITED',
        'current_session_ledger_boundary':'START_AT_HANDOFF_RESTORE_AFTER_CURRENT_VALIDATION'
    }
    ms['source_schema_manifest_sha256']=source_manifest_digest
    c['migration_state']=ms
    c['schema_manifest']=copy.deepcopy(tmpl['schema_manifest'])
    required=set(tmpl['schema_manifest']['required_fields'])
    missing=sorted(required-set(c))
    if missing: raise MigrationError('rev15 input still missing current required root carriers after declared migration: '+', '.join(missing))
    allowed_add=set(contract['allowed_added_root_carriers'])
    original=set(src); added=set(c)-original
    unexpected=sorted(added-allowed_add)
    if unexpected: raise MigrationError('undeclared root additions: '+', '.join(unexpected))
    if c['failure_mode_state'].get('history_completeness_state')!='LEGACY_UNRECORDED_PRE_REV16': raise MigrationError('failure history was not marked legacy-unrecorded')
    if c['surfaced_object_ledger_state'].get('completeness_state')!='LEGACY_UNRECORDED_PRE_REV16': raise MigrationError('ledger history was not marked legacy-unrecorded')
    if c['failure_mode_state'].get('records') or c['surfaced_object_ledger_state'].get('entries'): raise MigrationError('migration synthesized pre-rev16 history')
    return out


def migrate_rev16_to_rev17(doc: dict[str,Any], current_template_doc: dict[str,Any])->dict[str,Any]:
    if set(doc)!= {'AIR_HANDOFF_CARD'}: raise MigrationError('expected exactly one AIR_HANDOFF_CARD root')
    if set(current_template_doc)!= {'AIR_HANDOFF_CARD'}: raise MigrationError('current template root invalid')
    src=doc['AIR_HANDOFF_CARD']; tmpl=current_template_doc['AIR_HANDOFF_CARD']
    if src.get('schema_version')!='2.3.0' or src.get('SCHEMA_VERSION')!='2.3.0': raise MigrationError('source is not schema 2.3.0')
    if src.get('card_revision')!=16: raise MigrationError('source card_revision is not 16')
    contract=tmpl.get('schema_manifest',{}).get('revision_migration_contracts',{}).get('REV16_TO_REV17')
    if not contract or contract.get('apply_before_current_required_carrier_check') is not True: raise MigrationError('current rev17 migration contract missing')
    out=copy.deepcopy(doc); c=out['AIR_HANDOFF_CARD']; c['card_revision']=17
    ps=c.setdefault('execution_state',{}).setdefault('patch_state',{})
    defaults=tmpl['execution_state']['patch_state']
    for k in contract['nested_additions']['execution_state.patch_state']:
        ps.setdefault(k,copy.deepcopy(defaults.get(k)))
    scope=c.get('open_approval_scope')
    if isinstance(scope,dict) and scope.get('approval_scope_fingerprint') is None:
        scope['approval_state']='REVIEW_REQUIRED'
    old_ms=c.get('migration_state') if isinstance(c.get('migration_state'),dict) else {}
    ms=copy.deepcopy(tmpl['migration_state'])
    if isinstance(old_ms,dict):
        for k in ['legacy_q4_c_state','legacy_q4_d_state','legacy_prompt_mode_state','legacy_orbit_state','legacy_active_contract_state','legacy_governance_state','unresolved_legacy_states','legacy_history_state']:
            if k in old_ms: ms[k]=copy.deepcopy(old_ms[k])
    ms['source_schema_version']='2.3.0'; ms['source_card_revision']=16; ms['migration_required']=True
    ms['migration_decision']='MIGRATED_REV16_TO_REV17_PENDING_CURRENT_ALIGNMENT_REBINDING_AND_APPROVAL_SCOPE_REVALIDATION'
    ms['revision_migration_path']='REV16_TO_REV17'
    ms['source_schema_manifest_sha256']=canonical_sha(src.get('schema_manifest',{}))
    c['migration_state']=ms; c['schema_manifest']=copy.deepcopy(tmpl['schema_manifest'])
    required=set(tmpl['schema_manifest']['required_fields']); missing=sorted(required-set(c))
    if missing: raise MigrationError('rev16 input missing current required root carriers after declared migration: '+', '.join(missing))
    return out


def migrate_to_current(doc: dict[str,Any], current_template_doc: dict[str,Any])->dict[str,Any]:
    rev=doc.get('AIR_HANDOFF_CARD',{}).get('card_revision')
    if rev==15:
        mid=migrate_rev15_to_rev16(doc,current_template_doc)
        return migrate_rev16_to_rev17(mid,current_template_doc)
    if rev==16:
        return migrate_rev16_to_rev17(doc,current_template_doc)
    if rev==17:
        return copy.deepcopy(doc)
    raise MigrationError(f'unsupported source card_revision {rev!r}')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('--template',default='prompts/AIR_HANDOFF_CARD_TEMPLATE.json'); ap.add_argument('--output')
    a=ap.parse_args(); inp=load_json(Path(a.input)); tmpl=load_json(Path(a.template)); out=migrate_to_current(inp,tmpl)
    txt=json.dumps(out,indent=2,ensure_ascii=False)+'\n'
    if a.output: Path(a.output).write_text(txt,encoding='utf-8')
    else: print(txt,end='')
if __name__=='__main__': main()
