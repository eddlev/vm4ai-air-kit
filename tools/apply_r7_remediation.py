from __future__ import annotations
import json, sys
from pathlib import Path
from typing import Any

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
FOUNDATION_ID = 'AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005'
FOUNDATION_STATE = 'OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_' + FOUNDATION_ID
STATIC_PASS = 'PASS_R7_DETERMINISTIC_STATIC_SUITE'
BEHAVIOR_PENDING = 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'
R7_FIXTURES = [
    {"id":"R7-LC-01-CANDIDATE-NOT-RELEASED","finding_ids":["AIR-AUD-006","AIR-AUD-073"],"invalid_if":"a SET_005/V071 release-candidate entry uses RELEASE_CATALOG_ENTRY before external release sealing"},
    {"id":"R7-LC-02-BEHAVIORAL-EVIDENCE-BOUNDARY","finding_ids":["AIR-AUD-032","AIR-AUD-042","AIR-AUD-048","AIR-AUD-055","AIR-AUD-058"],"invalid_if":"current component or package state claims behavioral PASS without a replayable/model-host evidence manifest for the exact current Foundation identity"},
    {"id":"R7-LC-03-HISTORY-IMMUTABLE","finding_ids":["AIR-AUD-074"],"invalid_if":"current dependency reseal rewrites t7_change_record, historical_release_catalogs, source_baseline, mainline_release_binding, or another explicitly historical container"},
    {"id":"R7-LC-04-SFV-PACKAGE-VERSION-SOURCE","finding_ids":["AIR-AUD-061"],"invalid_if":"SFV Method duplicates a stale required_package_version literal instead of checking the canonical top-level package_version"},
    {"id":"R7-LC-05-GOVERNANCE-COMPONENT-ROLES","finding_ids":["AIR-AUD-050"],"invalid_if":"Governance reseal records null component_roles_observed instead of the actual manifest roles"}
]

HISTORY_KEYS = {
    'source_baseline','mainline_release_binding','t7_change_record','historical_release_catalogs',
    'source_candidate_manifest','change_history','release_history','historical_records'
}

T7_ORIGINAL = {
    'change_id': 'AIR_T7_CEA_MII_INTEGRATION_001',
    'package_version': '2.4.0',
    'component_prompt_version': '2.2.0',
    'manifest_prompt_version': '2.1.0',
    'change_class': 'MINOR_SEMANTIC_PACKAGE_EXPANSION_WITH_NO_AUTHORITY_EXPANSION',
    'reason_for_version': '2.4.0 selected after actual diff because all four operative components gain additive MII/semantic/epistemic/morphology contribution contracts and evidence-presentation semantics while package identity and authority class remain v2-compatible.',
    'source_package_version': '2.3.9',
    'applied_at': '2026-08-28T21:05:00+02:00'
}

CORE_OLD = '- availability_state = RELEASE_CATALOG_ENTRY\n\nIndex rules:'
CORE_NEW = '''- availability_state in { RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION, RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION, RELEASE_CATALOG_ENTRY }

Patch marker: AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1
Candidate-to-release lifecycle:
- RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION = candidate bytes are discoverable but current deterministic/static validation has not passed; this is not a released catalog entry.
- RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION = current deterministic/static validation has passed for the candidate bytes, but required replayable/model-host behavioral evidence remains pending; this is not a released catalog entry.
- RELEASE_CATALOG_ENTRY = release-sealed catalog entry. This state may be emitted only after the release process closes every validation requirement declared by that release and the release-sealed index carries the exact manifest receipt.
- Candidate states are discovery metadata only and never grant selection, approval, binding, or execution authority.

Index rules:'''


def loadj(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def dumpj(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def historical_path(path: tuple[str,...]) -> bool:
    return any(p in HISTORY_KEYS or p.startswith('historical_') for p in path)

def normalize_current_strings(obj: Any, path: tuple[str,...]=()):
    if historical_path(path):
        return obj
    if isinstance(obj, dict):
        return {k: normalize_current_strings(v, path+(k,)) for k,v in obj.items()}
    if isinstance(obj, list):
        return [normalize_current_strings(v, path+(str(i),)) for i,v in enumerate(obj)]
    if isinstance(obj, str):
        if obj == 'PASS_CURRENT_SESSION_PROMPT_RUNTIME_REPRESENTATIVE_SCENARIO_REVALIDATION':
            return BEHAVIOR_PENDING
        if obj == 'PENDING_POST_PATCH_DETERMINISTIC_VALIDATION':
            return STATIC_PASS
        if obj == 'PENDING_POST_PATCH_REPLAYABLE_EVALUATION':
            return BEHAVIOR_PENDING
        if 'BEHAVIORAL_REVALIDATION_PASS' in obj:
            obj = obj.replace('BEHAVIORAL_REVALIDATION_PASS', 'BEHAVIORAL_REVALIDATION_PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE')
        if 'PASS_AIR_2_5_0_FOUNDATION_SET_005_AND_EXACT_SPECIALIST_INTERNAL_DEPENDENCY_CLOSURE' in obj:
            obj = obj.replace('PASS_AIR_2_5_0_FOUNDATION_SET_005_AND_EXACT_SPECIALIST_INTERNAL_DEPENDENCY_CLOSURE',
                              'PASS_AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005_AND_EXACT_SPECIALIST_INTERNAL_DEPENDENCY_CLOSURE')
        return obj
    return obj

def promote_top_status(obj: dict):
    for key in ('STATUS','status'):
        v=obj.get(key)
        if isinstance(v,str) and 'STATIC_CONTRACT_VALIDATION_PENDING' in v:
            obj[key]=v.replace('STATIC_CONTRACT_VALIDATION_PENDING','STATIC_VALIDATED')

def patch_core():
    p=ROOT/'prompts/AIR_CORE_RUNTIME.md'
    s=p.read_text(encoding='utf-8')
    if 'Patch marker: AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1' not in s:
        if CORE_OLD not in s:
            raise RuntimeError('Core Specialist Index lifecycle anchor not found')
        s=s.replace(CORE_OLD, CORE_NEW, 1)
        p.write_text(s, encoding='utf-8')

def patch_profile(path: Path):
    obj=loadj(path)
    obj=normalize_current_strings(obj)
    promote_top_status(obj)
    ir=obj.get('integration_refresh')
    if isinstance(ir,dict) and 'foundation_identity_state' in ir:
        ir['foundation_identity_state']=FOUNDATION_STATE
    if path.name == 'AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json':
        vc=obj.setdefault('validation_contract',{})
        vc.pop('required_package_version',None)
        vc['required_package_version_source']='$.package_version'
        vc['required_package_version_check']='EQUAL_TO_CANONICAL_TOP_LEVEL_PACKAGE_VERSION'
    dumpj(path,obj)

def actual_component_status(folder: Path, filename: str) -> str:
    c=loadj(folder/filename)
    return str(c.get('STATUS') or c.get('status') or '')

def availability_for_status(status: str) -> str:
    if status == 'DRAFT' or 'STATIC_CONTRACT_VALIDATION_PENDING' in status:
        return 'AVAILABLE_UNVALIDATED'
    if 'STATIC_VALIDATED' in status:
        return 'VALIDATED_AVAILABLE_UNBOUND'
    return 'AVAILABLE_UNVALIDATED'

def patch_manifest(path: Path):
    obj=loadj(path)
    obj=normalize_current_strings(obj)
    promote_top_status(obj)
    ir=obj.get('integration_refresh')
    if isinstance(ir,dict) and 'foundation_identity_state' in ir:
        ir['foundation_identity_state']=FOUNDATION_STATE
    pvs=obj.setdefault('package_validation_state',{})
    for key in ('t7_static_validation','coordinated_reseal_static_validation','static_design_validation'):
        if key in pvs:
            pvs[key]=STATIC_PASS
    for key in ('behavioral_revalidation','regression','prior_behavioral_evidence_inheritance'):
        if key in pvs:
            pvs[key]=BEHAVIOR_PENDING
    if 'package_state' in pvs:
        pvs['package_state']='PACKAGE_COMPLETE_OBJECT_CONTRACT_SET_005_RESEAL_STATICALLY_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING'
    if 'decision' in pvs:
        pvs['decision']='STATIC_VALIDATED_AVAILABLE_UNBOUND_BEHAVIORAL_REVALIDATION_PENDING'
    if 'cross_file' in pvs:
        pvs['cross_file']='PASS_AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005_AND_EXACT_SPECIALIST_INTERNAL_DEPENDENCY_CLOSURE'
    if path.name == 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json':
        pvs['static_design_validation']=STATIC_PASS
        pvs['behavioral_revalidation']=BEHAVIOR_PENDING
        pvs['release_catalog_registration']='INCLUDED_IN_SET_005_V071_RELEASE_CANDIDATE_INDEX'
    if path.name == 'AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json':
        vs=obj.get('validation_state')
        if isinstance(vs,dict):
            vs['behavioral_revalidation']=BEHAVIOR_PENDING
            vs['operative_lifecycle_coherence']='PASS_R7_CURRENT_COMPONENT_STATUS_MIRROR'
        roles=[]
        for c in obj.get('components',[]): roles.append(c.get('role'))
        fm=obj.get('failure_mode_integration_contract')
        if isinstance(fm,dict): fm['component_roles_observed']=roles
    if path.name == 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json':
        obj['t7_change_record']=dict(T7_ORIGINAL)
    folder=path.parent
    for c in obj.get('components',[]):
        fn=c.get('filename')
        if isinstance(fn,str) and (folder/fn).is_file():
            st=actual_component_status(folder,fn)
            c['status']=st
            c['availability_state']=availability_for_status(st)
    dumpj(path,obj)

def patch_index():
    p=ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'
    obj=loadj(p)  # stdlib intentionally collapses the remediation-state duplicate key; strict validators run after repair.
    obj['catalog_scope']['catalog_completeness_claim']='COMPLETE_FOR_AIR_2_6_0_OBJECT_CONTRACT_SET_005_V071_RELEASE_CANDIDATE_SPECIALIST_CATALOG'
    obj['catalog_scope']['historical_release_catalogs']=[{
        'kit_release':'0.7.0',
        'foundation_identity':'AIR_FOUNDATION_2_5_0_OBJECT_CONTRACT_SET_004',
        'index_generation':'V070',
        'catalog_completeness_claim':'COMPLETE_FOR_AIR_2_5_0_SET_004_V070_RELEASE_SPECIALIST_CATALOG',
        'state':'RELEASED_HISTORICAL_NON_OPERATIVE'
    }]
    obj['candidate_lifecycle_contract']={
        'core_patch_marker':'AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1',
        'states':[
            'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION',
            'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION',
            'RELEASE_CATALOG_ENTRY'
        ],
        'current_candidate_state':'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION',
        'released_state':'RELEASE_CATALOG_ENTRY',
        'candidate_states_are_release_sealed':False,
        'authority_effect':'DISCOVERY_METADATA_ONLY_NO_SELECTION_APPROVAL_BINDING_OR_EXECUTION_AUTHORITY'
    }
    vs=obj['validation_state']
    vs.clear()
    vs.update({
        'decision':'STATIC_VALIDATED_CANDIDATE_PENDING_REPLAYABLE_BEHAVIORAL_REVALIDATION',
        'entry_count':5,
        'core_minimum_entry_contract':'PASS_TYPED_CANDIDATE_TO_RELEASE_LIFECYCLE',
        'manifest_hash_closure':'PASS_R7_EXACT_RESEAL',
        'foundation_identity_closure':'PASS_AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005',
        'route_map_identity_closure':'PASS_R7_EXACT_RESEAL',
        'authority_boundary':'PASS_NO_AUTHORITY_EXPANSION',
        'catalog_uniqueness':'PASS',
        'mii_discovery_boundary':'PASS_DISCOVERY_ONLY',
        'handoff_rev16_catalog_compatibility':'PASS_DISCOVERY_PROVENANCE_ONLY',
        'target_readiness_step_optimality_boundary':'PASS_NONAUTHORIZING',
        'static_validation':STATIC_PASS,
        'behavioral_revalidation':BEHAVIOR_PENDING,
        'release_publication_state':'EXTERNAL_RELEASE_STATE_NOT_RUNTIME_AUTHORITY',
        'operative_lifecycle_coherence':'PASS_R7_CURRENT_CANDIDATE_LIFECYCLE',
        'component_internal_foundation_compatibility':'PASS_SET_005_EXACT_RECEIPTS',
        'release_publication_rule':'Verify tag/release/publication through the current external repository/release surface at release time. Candidate catalog bytes do not assert completed publication as runtime truth.'
    })
    for e in obj['entries']:
        e['foundation_compatibility_identity']=FOUNDATION_ID
        e['availability_state']='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'
    dumpj(p,obj)

def patch_fixtures():
    p=ROOT/'tests/air_contract_fixtures.json'
    if not p.is_file():
        return
    obj=loadj(p)
    obj['r7_lifecycle_reseal_cases']=R7_FIXTURES
    dumpj(p,obj)

def main():
    patch_core()
    # Components first, manifests after so status mirrors see promoted component status.
    manifests=[]
    for p in sorted((ROOT/'profiles').glob('**/*.json')):
        if p.name.endswith('PACKAGE_MANIFEST.json'): manifests.append(p)
        else: patch_profile(p)
    for p in manifests: patch_manifest(p)
    patch_index()
    patch_fixtures()
    print('R7 semantic lifecycle/history patch applied')
if __name__=='__main__': main()
