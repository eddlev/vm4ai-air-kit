from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
FOUNDATION='AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006'
STATUS='AIR_2_6_1_OBJECT_CONTRACT_SET_006_FIVE_PACKAGE_INDEX_V072_CANDIDATE_STATIC_VALIDATED'
COMPLETE='COMPLETE_FOR_AIR_2_6_1_OBJECT_CONTRACT_SET_006_V072_CANDIDATE_SPECIALIST_CATALOG'
CANDIDATE='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'
class E(Exception): pass
def req(c,m):
    if not c: raise E(m)
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    req((ROOT/'VERSION').read_text().strip()=='0.7.2','AIR Kit VERSION is not 0.7.2')
    core=(ROOT/'prompts/AIR_CORE_RUNTIME.md').read_text(); control=(ROOT/'prompts/AIR_CONTROL_SURFACE.md').read_text(); gov=(ROOT/'prompts/AIR_GOV.md').read_text(); starter=load(ROOT/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'); card=load(ROOT/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']; idx=load(ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'); rmap=load(ROOT/'catalog/AIR_RUNTIME_ROUTE_MAP.json')
    req('PROMPT_VERSION: 2.6.1' in core,'Core not 2.6.1'); req('PROMPT_VERSION: 2.6.1' in control,'Control not 2.6.1'); req('PROMPT_VERSION: 2.3.1' in gov,'Governance not 2.3.1'); req(starter['PROMPT_VERSION']=='2.6.1','Starter not 2.6.1'); req(card['schema_version']=='2.3.0' and card['card_revision']==17,'Handoff not schema 2.3.0 rev17')
    req('AIR_NEW_TASK_BINDING_TRANSACTION_V2' in core,'new-task binding transaction absent'); req('AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1' in control,'primary response surface law absent'); req('approval_scope_fingerprint' in gov,'approval fingerprint governance absent')
    nt=starter['compiler_contract']['new_task_binding_transaction']; req(nt['required'] is True and nt['ordered_states'][-1]=='NEW_TASK_EXECUTION_ELIGIBLE','Starter new-task transaction invalid')
    req(nt['ordered_states'][-3:]==['PRIMARY_USER_VISIBLE_ARTIFACT_EMITTED','ARTIFACT_SURFACED_LEDGER_ACCOUNTED','NEW_TASK_EXECUTION_ELIGIBLE'],'Starter new-task visible/accounting terminal order invalid')
    events={e['route_id']:e for e in starter['compiler_contract']['runtime_control_event_registry']['events']}; req(len(events['RT.TASK_SWITCH']['guards'])>=7,'Task-switch typed guards incomplete'); req(len(events['RT.ACTION']['guards'])>=12,'Action exact Artifact guards incomplete')
    req(rmap['MAP_VERSION']=='1.2.0','Route Map not 1.2.0'); routes={r['route_id']:r for r in rmap['routes']}; req(routes['RT.TASK_SWITCH'].get('execution_semantics')=='DETERMINISTIC_PIPELINE','Task Switch not deterministic in Route Map'); req('RT.TASK_SWITCH' in rmap['deterministic_pipeline_contract']['declared_route_ids'],'Task Switch absent from deterministic route catalog')
    req(idx['INDEX_VERSION']=='1.3.1','Index not 1.3.1'); req(idx['status']==STATUS,'Index candidate status mismatch'); req(idx['catalog_scope']['catalog_completeness_claim']==COMPLETE,'Index completeness mismatch'); req(idx['foundation_compatibility_catalog']['identity']==FOUNDATION,'Index Foundation mismatch'); req(idx['candidate_lifecycle_contract']['current_candidate_state']==CANDIDATE,'Index candidate lifecycle mismatch'); req(idx['validation_state']['behavioral_revalidation']=='PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE','unsupported behavioral PASS'); req(idx['validation_state']['release_publication_state']=='EXTERNAL_RELEASE_STATE_NOT_RUNTIME_AUTHORITY','publication boundary changed')
    req(len(idx['entries'])==5,'Index package count');
    for e in idx['entries']:
        req(e['package_version']=='2.5.0','Specialist package version changed'); req(e['foundation_compatibility_identity']==FOUNDATION,'Specialist Foundation compatibility stale'); req(e['availability_state']==CANDIDATE,'Specialist index availability not candidate'); m=list((ROOT/'profiles').glob('**/'+e['manifest_filename'])); req(len(m)==1,'manifest target missing'); req(e['manifest_sha256']==sha(m[0]),'manifest hash stale')
    fx=load(ROOT/'tests/air_contract_fixtures.json'); req(fx['foundation_identity']==FOUNDATION,'fixtures Foundation stale'); req(len(fx.get('new_task_binding_barrier_negative_cases',[]))==8,'new-task fixtures incomplete'); req(len(fx.get('approval_scope_identity_cases',[]))>=3,'approval identity fixtures incomplete'); req(len(fx.get('repository_patch_reconciliation_cases',[]))>=2,'repo reconciliation fixtures incomplete')
    print('AIR v0.7.2 candidate-seal validation: PASS'); print('foundation',FOUNDATION); print('handoff_revision',17); print('specialist_packages',5); print('behavioral_evidence','PENDING'); print('publication_state','EXTERNAL_ONLY')
if __name__=='__main__':
    try: main()
    except (E,KeyError,ValueError) as e:
        print('AIR v0.7.2 candidate-seal validation: FAIL:',e,file=sys.stderr); raise SystemExit(1)
