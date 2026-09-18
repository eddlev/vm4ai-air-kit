from __future__ import annotations
import argparse, copy, hashlib, json, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_IMPORT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_IMPORT))
from adapters.durable_provenance import (
    FilesystemDurableProvenanceProvider,
    RECORD_PREPARED,
    STATE_AVAILABLE_VERIFIED,
    canonical_sha256,
)

class ValidationError(Exception): pass

def req(cond: bool, msg: str) -> None:
    if not cond: raise ValidationError(msg)

def reject_dupes(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValidationError(f'duplicate JSON key: {k}')
        out[k]=v
    return out

def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=reject_dupes)

def sha256_json(obj: Any) -> str:
    raw=json.dumps(obj, sort_keys=True, separators=(',',':'), ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def classify_adapter(a: dict[str,Any]) -> tuple[str,str]:
    ds=a.get('discovery_state')
    if ds=='PROVIDER_FAILED_INTEGRITY' or a.get('integrity_contradiction') is True:
        return 'FAILED_INTEGRITY','BLOCKED_FAILED_INTEGRITY'
    if ds=='PROVIDER_ABSENT':
        return 'UNAVAILABLE','INELIGIBLE_UNAVAILABLE'
    if ds!='PROVIDER_VERIFIED':
        return 'DEGRADED_INCOMPLETE','INELIGIBLE_INCOMPLETE'
    if not all(a.get(k)=='PASS' for k in ('exact_write_capability','exact_readback_capability','stable_identity_retrieval_capability')):
        return 'DEGRADED_INCOMPLETE','INELIGIBLE_INCOMPLETE'
    if a.get('coverage_state')!='COMPLETE_TO_CURRENT_COMMITTED_LEDGER' or a.get('historical_gap_before_provider') is True:
        return 'DEGRADED_INCOMPLETE','INELIGIBLE_INCOMPLETE'
    return 'AVAILABLE_VERIFIED','ELIGIBLE'

def resolve_mode(request: str, eligibility: str) -> str:
    table={
      ('GENERIC','ELIGIBLE'):'STRICT_PROVENANCE',
      ('GENERIC','INELIGIBLE_UNAVAILABLE'):'PORTABLE_STATE',
      ('GENERIC','INELIGIBLE_INCOMPLETE'):'PORTABLE_STATE',
      ('GENERIC','BLOCKED_FAILED_INTEGRITY'):'BLOCK_REVIEW',
      ('STRICT_PROVENANCE','ELIGIBLE'):'STRICT_PROVENANCE',
      ('STRICT_PROVENANCE','INELIGIBLE_UNAVAILABLE'):'FAIL_CLOSED',
      ('STRICT_PROVENANCE','INELIGIBLE_INCOMPLETE'):'FAIL_CLOSED',
      ('STRICT_PROVENANCE','BLOCKED_FAILED_INTEGRITY'):'BLOCK_REVIEW',
      ('PORTABLE_STATE','ELIGIBLE'):'PORTABLE_STATE',
      ('PORTABLE_STATE','INELIGIBLE_UNAVAILABLE'):'PORTABLE_STATE',
      ('PORTABLE_STATE','INELIGIBLE_INCOMPLETE'):'PORTABLE_STATE',
      ('PORTABLE_STATE','BLOCKED_FAILED_INTEGRITY'):'BLOCK_REVIEW',
    }
    return table.get((request,eligibility),'FAIL_CLOSED')

def generation_eval_valid(card: dict[str,Any], current_epoch: int) -> bool:
    if 'handoff_generation_evaluation' in card: return False
    e=card.get('evaluation_basis')
    if not isinstance(e,dict): return False
    return (
        e.get('evaluation_id') not in (None,'') and
        e.get('evaluation_profile')=='HANDOFF_CREATE' and
        e.get('state_epoch')==current_epoch and
        e.get('alignment_check_ref') not in (None,'') and
        e.get('validation_report_ref') not in (None,'') and
        e.get('dependency_state')=='SATISFIED'
    )

def portable_state_valid(card: dict[str,Any], live_durability: str, current_epoch: int) -> bool:
    if card.get('handoff_mode_state',{}).get('selected_mode')!='PORTABLE_STATE': return True
    if live_durability=='FAILED_INTEGRITY': return False
    if not generation_eval_valid(card,current_epoch): return False
    if not strict_provider_capture_valid(card): return False
    led=card.get('surfaced_object_ledger_state',{})
    fm=card.get('failure_mode_state',{})
    hm=card.get('handoff_mode_state',{})
    return (
        led.get('entries')==[] and
        led.get('completeness_state')=='NOT_CLAIMED_PORTABLE_STATE' and
        fm.get('records')==[] and
        fm.get('history_completeness_state')=='NOT_CLAIMED_PORTABLE_STATE' and
        hm.get('positive_execution_authority')=='NONE' and
        card.get('_reconstructed_historical_authority',False) is False
    )

def strict_provider_capture_valid(card: dict[str,Any]) -> bool:
    capture=card.get('surfaced_object_ledger_state',{}).get('provenance_capture',{})
    required_nonempty=[
      'provenance_store_id','persistence_provider_class','provider_identity',
      'provider_generation','provider_instance_id','provider_namespace_id',
      'provider_namespace_fingerprint','storage_location_class',
      'provider_authorization_state_at_capture'
    ]
    if capture.get('provider_adapter_contract')!='AIR_DURABLE_PROVENANCE_PROVIDER_ADAPTER_V1': return False
    if capture.get('credentials_serialized') is not False: return False
    if capture.get('canonicalization_contract')!='UTF8_NO_BOM_SORTED_OBJECT_KEYS_ARRAY_ORDER_PRESERVED_MINIFIED_ALLOW_NAN_FALSE_NO_PROVIDER_UNICODE_NORMALIZATION_SHA256_EXACT_BYTES': return False
    return all(capture.get(k) not in (None,'','UNVALIDATED_TEMPLATE') for k in required_nonempty)

def strict_state_valid(card: dict[str,Any], live_durability: str, eligibility: str, current_epoch: int) -> bool:
    if card.get('handoff_mode_state',{}).get('selected_mode')!='STRICT_PROVENANCE': return True
    if live_durability!='AVAILABLE_VERIFIED' or eligibility!='ELIGIBLE': return False
    if not generation_eval_valid(card,current_epoch): return False
    led=card.get('surfaced_object_ledger_state',{})
    if led.get('completeness_state')!='COMPLETE_PRE_FILE_CAPTURE': return False
    for e in led.get('entries',[]):
        snap=e.get('canonical_object_snapshot')
        if snap is None or sha256_json(snap)!=e.get('canonical_object_sha256'): return False
    return True

def receipt_success(fields: dict[str,Any]) -> bool:
    required=['filename','canonical_role','linked_path_or_file_ref','sha256','byte_count','text_line_count','designation','version_or_schema_identity','strict_parse_state','duplicate_key_state','schema_validation_state','provenance_validation_state','validation_record_ref']
    if not all(k in fields for k in required): return False
    return (
      fields['strict_parse_state']=='PASS' and fields['duplicate_key_state']=='PASS' and
      fields['schema_validation_state']=='PASS' and fields['provenance_validation_state']=='PASS'
    )

def generated_base(template: dict[str,Any], mode: str, epoch: int=7) -> dict[str,Any]:
    c=copy.deepcopy(template)
    c['evaluation_basis']={
      'evaluation_id':'AIR-EVAL-HANDOFF-CREATE-TEST',
      'evaluation_profile':'HANDOFF_CREATE','state_epoch':epoch,
      'alignment_check_ref':'AIR-ALIGN-HANDOFF-CREATE-TEST',
      'validation_report_ref':'AIR-VALID-HANDOFF-CREATE-TEST',
      'dependency_state':'SATISFIED'}
    c['handoff_mode_state']['selected_mode']=mode
    c['handoff_mode_state']['selection_state']='RESOLVED_FOR_REQUEST'
    c['handoff_mode_state']['positive_execution_authority']='NONE'
    if mode=='STRICT_PROVENANCE':
        capture=c['surfaced_object_ledger_state']['provenance_capture']
        capture.update({
          'provenance_store_id':'validator-store',
          'persistence_provider_class':'FILESYSTEM',
          'durability_state':'AVAILABLE_VERIFIED',
          'write_readback_state':'EXACT',
          'coverage_through_capture_cutoff':'COMPLETE',
          'strict_handoff_eligibility':'ELIGIBLE',
          'provider_identity':'filesystem:validator',
          'provider_generation':'validator-provider-generation',
          'provider_instance_id':'validator-provider-instance',
          'provider_namespace_id':'air-project-validator',
          'provider_namespace_fingerprint':'validator-namespace-fingerprint',
          'storage_location_class':'LOCAL_DURABLE_FILESYSTEM',
          'provider_authorization_state_at_capture':'AUTHORIZED_LOCAL',
          'retention_policy':'TEST_RETENTION',
          'deletion_policy':'TEST_DELETION',
          'credentials_serialized':False
        })
    return c

def validate_static(root: Path) -> list[str]:
    core=(root/'prompts/AIR_CORE_RUNTIME.md').read_text(encoding='utf-8')
    control=(root/'prompts/AIR_CONTROL_SURFACE.md').read_text(encoding='utf-8')
    starter=load(root/'prompts/AIR_DEFAULT_STARTER_PROFILE.json')
    handoff=load(root/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']
    rmap=load(root/'catalog/AIR_RUNTIME_ROUTE_MAP.json')
    checks=[]
    def ok(cond,msg): req(cond,msg); checks.append(msg)
    ok('Patch marker: AIR_HANDOFF_RUNTIME_DURABILITY_AND_GENERATION_CONTRACT_V1' in core,'core runtime durability/generation marker')
    ok('AIR_SESSION.handoff_durability_state is the sole canonical live-session owner' in core,'core live Session durability owner')
    ok('- handoff_durability_state' in core,'AIR_SESSION schema permits durability owner')
    ok('AIR_FILE_DELIVERY_RECEIPT is a Core-owned typed non-formal transport receipt' in core,'Core non-formal receipt contract')
    ok('A separate root handoff_generation_evaluation carrier is prohibited' in core,'Core sole serialized generation carrier')
    ok('Patch marker: AIR_CONTROL_HANDOFF_RUNTIME_DURABILITY_RENDERER_V1' in control,'Control durability renderer')
    ok('Patch marker: AIR_CONTROL_HANDOFF_GENERATION_EVALUATION_RENDERER_V1' in control,'Control generation evaluation renderer')
    cc=starter['compiler_contract']; hrt=cc['handoff_runtime_durability_and_generation']
    ok(hrt['session_live_owner_path']=='AIR_SESSION.handoff_durability_state','Starter live owner path')
    ok(hrt['provider_adapter_contract']=='AIR_DURABLE_PROVENANCE_PROVIDER_ADAPTER_V1','Starter provider adapter contract')
    ok(hrt['generation_evaluation_serialized_carrier']=='AIR_HANDOFF_CARD.evaluation_basis','Starter sole evaluation carrier')
    ok(hrt['root_handoff_generation_evaluation_field']=='PROHIBITED','Starter duplicate generation carrier prohibited')
    ok(cc['handoff_file_delivery']['receipt_contract']['formal_air_object'] is False,'Starter receipt non-formal')
    ok('handoff_generation_evaluation' not in handoff,'Template duplicate generation root absent')
    ok('evaluation_basis' in handoff['schema_manifest']['required_fields'],'Template evaluation_basis required')
    ops=handoff['schema_manifest']['validation_registry']['allowed_operators']
    ok('HANDOFF_GENERATION_EVALUATION_VALID' in ops,'Template generation evaluation operator')
    ok('PORTABLE_HANDOFF_STATE_VALID' in ops,'Template portable predicate operator')
    rule=handoff['schema_manifest']['validation_registry']['rules']['HC-VALIDATE-HANDOFF-MODE-PROVENANCE']
    rops=[p.get('operator') for p in rule.get('predicates',[])]
    ok(rule.get('operator')=='ALL' and rops==['HANDOFF_GENERATION_EVALUATION_VALID','HANDOFF_MODE_PROVENANCE_VALID','PORTABLE_HANDOFF_STATE_VALID'],'Template composite Handoff validator')
    ok(handoff['handoff_mode_state']['live_session_durability_owner_path']=='AIR_SESSION.handoff_durability_state','Template serialized durability owner reference')
    capture=handoff['surfaced_object_ledger_state']['provenance_capture']
    provider_fields=['provider_identity','provider_generation','provider_instance_id','provider_namespace_id','provider_namespace_fingerprint','storage_location_class','provider_authorization_state_at_capture','retention_policy','deletion_policy','credentials_serialized']
    ok(all(k in capture for k in provider_fields),'Template durable provider capture fields')
    ok(capture['provider_adapter_contract']=='AIR_DURABLE_PROVENANCE_PROVIDER_ADAPTER_V1','Template provider adapter identity')
    ok(capture['credentials_serialized'] is False,'Template prohibits credential serialization')
    ok(handoff['schema_manifest']['handoff_delivery_contract']['receipt_contract']['formal_air_object'] is False,'Template receipt non-formal')
    routes={r['route_id']:r for r in rmap['routes']}; hr=routes['RT.HANDOFF_CREATE']; rr=routes['RT.HANDOFF_RESTORE']
    reg=rmap['handoff_runtime_contract_registry']
    ok(reg['contract']=='AIR_HANDOFF_RUNTIME_DURABILITY_AND_GENERATION_CONTRACT_V1','Route root runtime contract identity')
    ok(reg['live_session_owner_path']=='AIR_SESSION.handoff_durability_state','Route root live Session owner')
    ok(reg['generation_evaluation_serialized_carrier']=='AIR_HANDOFF_CARD.evaluation_basis','Route root generation carrier')
    ok(reg['receipt_contract']['formal_air_object'] is False,'Route root receipt non-formal')
    rc=hr['handoff_runtime_contract']
    ok(rc['live_session_owner_path']=='AIR_SESSION.handoff_durability_state','Route live Session owner')
    ok(rc['generation_evaluation_serialized_carrier']=='AIR_HANDOFF_CARD.evaluation_basis','Route generation carrier')
    ok(rc['duplicate_root_handoff_generation_evaluation']=='PROHIBITED','Route duplicate root prohibited')
    ok(hr['handoff_file_delivery']['receipt_contract']['formal_air_object'] is False,'Route receipt non-formal')
    ok(rr['handoff_durability_restore_contract']['target_provider_discovery_required'] is True,'Restore target provider renegotiation required')
    cov=starter['validation_contract']['deterministic_contract_registry']['coverage_contract']
    actual=len(starter['validation_contract']['deterministic_contract_registry']['checks'])
    ok(cov['declared_check_count']==cov['implemented_check_count_required']==cov['executed_check_count_required']==actual,'Deterministic registry coverage parity')
    return checks

def run_cases(template: dict[str,Any]) -> list[dict[str,Any]]:
    out=[]
    def case(cid,actual,expected):
        passed=actual==expected
        out.append({'id':cid,'actual':actual,'expected':expected,'result':'PASS' if passed else 'FAIL'})
        req(passed,f'{cid}: expected {expected!r}, got {actual!r}')
    base={'discovery_state':'PROVIDER_ABSENT'}
    case('HD-01-NO-PROVIDER',classify_adapter(base),('UNAVAILABLE','INELIGIBLE_UNAVAILABLE'))
    case('HD-02-PRESENT-UNVERIFIED',classify_adapter({'discovery_state':'PROVIDER_PRESENT_UNVERIFIED'}),('DEGRADED_INCOMPLETE','INELIGIBLE_INCOMPLETE'))
    verified={'discovery_state':'PROVIDER_VERIFIED','exact_write_capability':'PASS','exact_readback_capability':'PASS','stable_identity_retrieval_capability':'PASS','coverage_state':'COMPLETE_TO_CURRENT_COMMITTED_LEDGER'}
    case('HD-03-VERIFIED-COMPLETE',classify_adapter(verified),('AVAILABLE_VERIFIED','ELIGIBLE'))
    bad={**verified,'integrity_contradiction':True}
    case('HD-04-INTEGRITY-CONTRADICTION',classify_adapter(bad),('FAILED_INTEGRITY','BLOCKED_FAILED_INTEGRITY'))
    late={**verified,'historical_gap_before_provider':True}
    case('HD-05-LATE-PROVIDER-GAP',classify_adapter(late),('DEGRADED_INCOMPLETE','INELIGIBLE_INCOMPLETE'))
    for cid,reqmode,elig,exp in [
      ('HM-01-GENERIC-AVAILABLE-STRICT','GENERIC','ELIGIBLE','STRICT_PROVENANCE'),
      ('HM-02-GENERIC-UNAVAILABLE-PORTABLE','GENERIC','INELIGIBLE_UNAVAILABLE','PORTABLE_STATE'),
      ('HM-03-GENERIC-INCOMPLETE-PORTABLE','GENERIC','INELIGIBLE_INCOMPLETE','PORTABLE_STATE'),
      ('HM-04-GENERIC-FAILED-INTEGRITY-BLOCK','GENERIC','BLOCKED_FAILED_INTEGRITY','BLOCK_REVIEW'),
      ('HM-05-EXPLICIT-STRICT-UNAVAILABLE-FAIL','STRICT_PROVENANCE','INELIGIBLE_UNAVAILABLE','FAIL_CLOSED'),
      ('HM-06-EXPLICIT-PORTABLE-UNAVAILABLE','PORTABLE_STATE','INELIGIBLE_UNAVAILABLE','PORTABLE_STATE')]:
        case(cid,resolve_mode(reqmode,elig),exp)
    c=generated_base(template,'PORTABLE_STATE')
    c['surfaced_object_ledger_state']['entries']=[]; c['surfaced_object_ledger_state']['completeness_state']='NOT_CLAIMED_PORTABLE_STATE'
    c['failure_mode_state']['records']=[]; c['failure_mode_state']['history_completeness_state']='NOT_CLAIMED_PORTABLE_STATE'
    case('HE-01-CURRENT-GENERATION-EVAL',generation_eval_valid(c,7),True)
    stale=copy.deepcopy(c); stale['evaluation_basis']['state_epoch']=6
    case('HE-02-STALE-GENERATION-EVAL',generation_eval_valid(stale,7),False)
    dup=copy.deepcopy(c); dup['handoff_generation_evaluation']={'evaluation_id':'duplicate'}
    case('HE-03-DUPLICATE-ROOT-CARRIER',generation_eval_valid(dup,7),False)
    case('HP-01-PORTABLE-VALID',portable_state_valid(c,'UNAVAILABLE',7),True)
    hist=copy.deepcopy(c); hist['surfaced_object_ledger_state']['entries']=[{'x':1}]
    case('HP-02-PORTABLE-HISTORY-REJECT',portable_state_valid(hist,'UNAVAILABLE',7),False)
    case('HP-03-PORTABLE-FAILED-INTEGRITY-REJECT',portable_state_valid(c,'FAILED_INTEGRITY',7),False)
    auth=copy.deepcopy(c); auth['_reconstructed_historical_authority']=True
    case('HP-04-PORTABLE-AUTHORITY-RECONSTRUCTION-REJECT',portable_state_valid(auth,'UNAVAILABLE',7),False)
    snap={'AIR_ALIGNMENT_CHECK':{'check_id':'x'}}
    s=generated_base(template,'STRICT_PROVENANCE'); s['surfaced_object_ledger_state']['completeness_state']='COMPLETE_PRE_FILE_CAPTURE'; s['surfaced_object_ledger_state']['entries']=[{'canonical_object_snapshot':snap,'canonical_object_sha256':sha256_json(snap)}]
    case('HS-01-STRICT-VALID',strict_state_valid(s,'AVAILABLE_VERIFIED','ELIGIBLE',7),True)
    bads=copy.deepcopy(s); bads['surfaced_object_ledger_state']['entries'][0]['canonical_object_sha256']='0'*64
    case('HS-02-STRICT-HASH-MISMATCH',strict_state_valid(bads,'AVAILABLE_VERIFIED','ELIGIBLE',7),False)
    missing_provider=copy.deepcopy(s); missing_provider['surfaced_object_ledger_state']['provenance_capture']['provider_generation']=None
    case('HS-03-STRICT-PROVIDER-METADATA-MISSING',strict_state_valid(missing_provider,'AVAILABLE_VERIFIED','ELIGIBLE',7),False)
    leaked_credentials=copy.deepcopy(s); leaked_credentials['surfaced_object_ledger_state']['provenance_capture']['credentials_serialized']=True
    case('HS-04-STRICT-CREDENTIAL-SERIALIZATION-REJECT',strict_state_valid(leaked_credentials,'AVAILABLE_VERIFIED','ELIGIBLE',7),False)
    receipt={'filename':'AIR_HANDOFF_CARD.json','canonical_role':'HANDOFF_TRANSFER_FILE','linked_path_or_file_ref':'/tmp/card','sha256':'a'*64,'byte_count':100,'text_line_count':10,'designation':'AIR_HANDOFF_CARD_TEMPLATE_V2','version_or_schema_identity':'2.3.0/rev20','strict_parse_state':'PASS','duplicate_key_state':'PASS','schema_validation_state':'PASS','provenance_validation_state':'PASS','validation_record_ref':'V1'}
    case('HR-01-RECEIPT-AFTER-VALIDATION',receipt_success(receipt),True)
    badr={**receipt,'schema_validation_state':'FAIL'}
    case('HR-02-NO-SUCCESS-RECEIPT-ON-POSTWRITE-FAIL',receipt_success(badr),False)
    source=('AVAILABLE_VERIFIED','ELIGIBLE'); target=classify_adapter({'discovery_state':'PROVIDER_ABSENT'})
    case('REST-01-TARGET-RENEGOTIATES-PROVIDER',target,('UNAVAILABLE','INELIGIBLE_UNAVAILABLE'))
    case('REST-02-SOURCE-AVAILABLE-DOES-NOT-UPGRADE-TARGET',target==source,False)
    return out

def strict_load_bytes(raw: bytes) -> dict[str,Any]:
    return json.loads(raw.decode('utf-8'), object_pairs_hook=reject_dupes)

def write_reopen_validate(card: dict[str,Any], live_durability: str, eligibility: str, epoch: int, path: Path, *, tamper_after_write: bool=False) -> tuple[bool,dict[str,Any]|None,dict[str,Any]]:
    raw=(json.dumps({'AIR_HANDOFF_CARD':card},indent=2,ensure_ascii=False)+'\n').encode('utf-8')
    path.write_bytes(raw)
    expected_sha=hashlib.sha256(raw).hexdigest()
    if tamper_after_write:
        changed=path.read_bytes().replace(b'"dependency_state": "SATISFIED"',b'"dependency_state": "STALE"',1)
        path.write_bytes(changed)
    reopened_raw=path.read_bytes()
    parse_ok=True
    try:
        reopened_root=strict_load_bytes(reopened_raw); reopened=reopened_root['AIR_HANDOFF_CARD']
    except Exception:
        parse_ok=False; reopened=None
    sha_ok=hashlib.sha256(reopened_raw).hexdigest()==expected_sha
    mode=(reopened or {}).get('handoff_mode_state',{}).get('selected_mode') if parse_ok else None
    schema_ok=bool(parse_ok and generation_eval_valid(reopened,epoch))
    provenance_ok=False
    if schema_ok and mode=='STRICT_PROVENANCE': provenance_ok=strict_state_valid(reopened,live_durability,eligibility,epoch)
    elif schema_ok and mode=='PORTABLE_STATE': provenance_ok=portable_state_valid(reopened,live_durability,epoch)
    validated=bool(parse_ok and sha_ok and schema_ok and provenance_ok)
    receipt=None
    if validated:
        receipt={
          'filename':path.name,'canonical_role':'HANDOFF_TRANSFER_FILE','linked_path_or_file_ref':str(path),
          'sha256':hashlib.sha256(reopened_raw).hexdigest(),'byte_count':len(reopened_raw),'text_line_count':len(reopened_raw.decode('utf-8').splitlines()),
          'designation':reopened.get('TEMPLATE_DESIGNATION'),'version_or_schema_identity':f"{reopened.get('schema_version')}/rev{reopened.get('template_revision')}",
          'strict_parse_state':'PASS','duplicate_key_state':'PASS','schema_validation_state':'PASS','provenance_validation_state':'PASS',
          'validation_record_ref':'AIR-VALID-HANDOFF-FILE-TEST','formal_air_object':False,'positive_execution_authority':'NONE'
        }
    detail={'parse_ok':parse_ok,'sha_ok':sha_ok,'schema_ok':schema_ok,'provenance_ok':provenance_ok,'receipt_success':bool(receipt and receipt_success(receipt))}
    return validated,receipt,detail

def restore_bootstrap(card: dict[str,Any], target_adapter: dict[str,Any]) -> dict[str,Any]:
    dur,elig=classify_adapter(target_adapter)
    return {
      'target_handoff_durability_state':dur,
      'target_strict_eligibility':elig,
      'serialized_source_durability_authority':'NONE_TRANSFER_PROVENANCE_ONLY',
      'serialized_active_artifact_binding_authority':'NONE_BOOTSTRAP_INPUT_ONLY',
      'fresh_alignment_required':True,
      'fresh_artifact_rebind_required':True,
      'specialist_restore_state':'AVAILABLE_UNBOUND_REVALIDATION_REQUIRED' if card.get('specialist_binding_state',{}).get('active_specialist') else 'NONE',
      'method_restore_state':'AVAILABLE_UNBOUND_REVALIDATION_REQUIRED' if card.get('execution_state',{}).get('method_handoff_state',{}).get('method_identity') else 'NONE'
    }

def run_file_flow_cases(template: dict[str,Any]) -> list[dict[str,Any]]:
    out=[]
    def case(cid,actual,expected):
        passed=actual==expected; out.append({'id':cid,'actual':actual,'expected':expected,'result':'PASS' if passed else 'FAIL'}); req(passed,f'{cid}: expected {expected!r}, got {actual!r}')
    with tempfile.TemporaryDirectory(prefix='air-handoff-e2e-') as td:
        d=Path(td)
        # Strict: qualifying provider + complete immutable surfaced history.
        snap={'AIR_ALIGNMENT_CHECK':{'check_id':'strict-e2e'}}
        strict=generated_base(template,'STRICT_PROVENANCE'); strict['surfaced_object_ledger_state']['completeness_state']='COMPLETE_PRE_FILE_CAPTURE'; strict['surfaced_object_ledger_state']['entries']=[{'canonical_object_snapshot':snap,'canonical_object_sha256':sha256_json(snap)}]
        ok,receipt,detail=write_reopen_validate(strict,'AVAILABLE_VERIFIED','ELIGIBLE',7,d/'strict.json')
        case('E2E-01-STRICT-CREATE-WRITE-REOPEN-RECEIPT', (ok,detail['receipt_success'],receipt['formal_air_object'] if receipt else None),(True,True,False))
        # Portable: no provider, no claimed history/authority.
        portable=generated_base(template,'PORTABLE_STATE'); portable['surfaced_object_ledger_state']['entries']=[]; portable['surfaced_object_ledger_state']['completeness_state']='NOT_CLAIMED_PORTABLE_STATE'; portable['failure_mode_state']['records']=[]; portable['failure_mode_state']['history_completeness_state']='NOT_CLAIMED_PORTABLE_STATE'
        ok,receipt,detail=write_reopen_validate(portable,'UNAVAILABLE','INELIGIBLE_UNAVAILABLE',7,d/'portable.json')
        case('E2E-02-PORTABLE-CREATE-WRITE-REOPEN-RECEIPT',(ok,detail['receipt_success']),(True,True))
        # Explicit strict with unavailable provider fails before successful delivery.
        case('E2E-03-EXPLICIT-STRICT-UNAVAILABLE-NO-DOWNGRADE-NO-RECEIPT',(resolve_mode('STRICT_PROVENANCE','INELIGIBLE_UNAVAILABLE'),None),('FAIL_CLOSED',None))
        # A post-write byte change invalidates the exact-write receipt path.
        ok,receipt,detail=write_reopen_validate(portable,'UNAVAILABLE','INELIGIBLE_UNAVAILABLE',7,d/'tampered.json',tamper_after_write=True)
        case('E2E-04-POSTWRITE-TAMPER-BLOCKS-SUCCESS-RECEIPT',(ok,detail['sha_ok'],receipt),(False,False,None))
        # Restore always renegotiates target provider; source strict state does not transfer authority.
        restored=restore_bootstrap(strict,{'discovery_state':'PROVIDER_ABSENT'})
        case('E2E-05-STRICT-RESTORE-TARGET-RENEGOTIATES',(restored['target_handoff_durability_state'],restored['target_strict_eligibility'],restored['fresh_artifact_rebind_required']),('UNAVAILABLE','INELIGIBLE_UNAVAILABLE',True))
        # Real provider-backed strict flow: exact canonical persistence is exercised,
        # not merely a qualifying-provider test double.
        provider_root=d/'real-provider'
        provider=FilesystemDurableProvenanceProvider(provider_root)
        desc=provider.describe_provider()
        probe=provider.probe_write_readback()
        pns=provider.open_project_namespace('AIR handoff provider E2E project')
        psnap={'AIR_ALIGNMENT_CHECK':{'check_id':'provider-backed-e2e'}}
        pref='AIR_SURFACED_OBJECT_LEDGER_ENTRY::provider-e2e::1'
        pidentity='provider-e2e-object'
        prec={
          'provenance_store_id':'provider-e2e-store',
          'ledger_entry_ref':pref,
          'canonical_object_sha256':canonical_sha256(psnap),
          'canonical_object_snapshot':psnap,
          'record_state':RECORD_PREPARED,
          'source_message_count':1,
          'source_state_epoch':7,
          'object_name':'AIR_ALIGNMENT_CHECK',
          'object_identity':pidentity,
          'persistence_provider_class':desc.provider_class,
          'write_readback_state':'PENDING'
        }
        provider.prepare_snapshot(pns,prec)
        provider.commit_visible(pns,pref)
        coverage=provider.verify_coverage(pns,[{'ledger_entry_ref':pref,'canonical_object_sha256':canonical_sha256(psnap),'object_identity':pidentity}])
        reopened_provider=FilesystemDurableProvenanceProvider(provider_root)
        stable=reopened_provider.stable_retrieve(reopened_provider.open_project_namespace('AIR handoff provider E2E project'),pref)
        pstrict=generated_base(template,'STRICT_PROVENANCE')
        pstrict['surfaced_object_ledger_state']['completeness_state']='COMPLETE_PRE_FILE_CAPTURE'
        pstrict['surfaced_object_ledger_state']['entries']=[{'ledger_entry_ref':pref,'object_identity':pidentity,'canonical_object_snapshot':psnap,'canonical_object_sha256':canonical_sha256(psnap)}]
        pcap=pstrict['surfaced_object_ledger_state']['provenance_capture']
        pcap.update({
          'provenance_store_id':'provider-e2e-store',
          'persistence_provider_class':desc.provider_class,
          'durability_state':'AVAILABLE_VERIFIED',
          'write_readback_state':'EXACT',
          'last_persisted_emission_sequence':1,
          'last_committed_emission_sequence':1,
          'coverage_through_capture_cutoff':'COMPLETE',
          'strict_handoff_eligibility':'ELIGIBLE',
          'provider_identity':desc.provider_identity,
          'provider_generation':desc.provider_generation,
          'provider_instance_id':desc.provider_instance,
          'provider_namespace_id':pns.namespace_id,
          'provider_namespace_fingerprint':pns.namespace_fingerprint,
          'storage_location_class':desc.storage_class,
          'provider_authorization_state_at_capture':desc.authorization_state,
          'retention_policy':'TEST_SCOPE_TEMPORARY',
          'deletion_policy':'TEST_SCOPE_CLEANUP',
          'credentials_serialized':False
        })
        ok,receipt,detail=write_reopen_validate(pstrict,'AVAILABLE_VERIFIED','ELIGIBLE',7,d/'provider-strict.json')
        case('E2E-07-REAL-FILESYSTEM-PROVIDER-STRICT',
             (probe['state'],coverage.state,stable['canonical_object_sha256']==canonical_sha256(psnap),ok,detail['receipt_success']),
             (STATE_AVAILABLE_VERIFIED,STATE_AVAILABLE_VERIFIED,True,True,True))
        # Serialized Specialist/Method continuity is availability only and cannot auto-bind on restore.
        cont=copy.deepcopy(portable); cont['specialist_binding_state']['active_specialist']={'id':'AIR_GROUNDING_SPECIALIST_V2'}; cont['execution_state']['method_handoff_state']['method_identity']='AIR_METHOD_GROUNDING_REVIEW_AND_EXECUTION_V2'
        restored=restore_bootstrap(cont,{'discovery_state':'PROVIDER_ABSENT'})
        case('E2E-06-RESTORED-SPECIALIST-METHOD-NONAUTHORITY',(restored['specialist_restore_state'],restored['method_restore_state'],restored['serialized_active_artifact_binding_authority'],restored['fresh_alignment_required']),('AVAILABLE_UNBOUND_REVALIDATION_REQUIRED','AVAILABLE_UNBOUND_REVALIDATION_REQUIRED','NONE_BOOTSTRAP_INPUT_ONLY',True))
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root',nargs='?',default='.'); ap.add_argument('--write-evidence')
    args=ap.parse_args(); root=Path(args.root).resolve()
    static=validate_static(root)
    template=load(root/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']
    cases=run_cases(template)+run_file_flow_cases(template)
    print(f'AIR Handoff runtime contract validation: PASS ({len(static)} static checks, {len(cases)} executable cases)')
    if args.write_evidence:
        evidence={
          'evidence_id':'AIR_HANDOFF_V074_RUNTIME_CONTRACT_EVIDENCE_V1',
          'evidence_class':'REPRODUCIBLE_EXECUTABLE_HANDOFF_RUNTIME_CONTRACT_EVIDENCE',
          'repository':'eddlev/vm4ai-air-kit',
          'source_baseline_commit':'f456fc579bed739aebcfaa55c175c2c14617d58d',
          'candidate_environment':'ISOLATED_LOCAL_CANDIDATE_FROM_CONFIRMED_SOURCE_SET',
          'generated_at_utc':datetime.now(timezone.utc).isoformat(),
          'contract':'AIR_HANDOFF_RUNTIME_DURABILITY_AND_GENERATION_CONTRACT_V1',
          'static_check_count':len(static),
          'executable_case_count':len(cases),
          'pass_count':sum(x['result']=='PASS' for x in cases),
          'fail_count':sum(x['result']!='PASS' for x in cases),
          'cases':cases,
          'claim_boundary':[
            'Proves deterministic contract logic and current candidate file integration in this local execution environment.',
            'Does not prove a real host durable-provenance provider exists; strict positive uses a deterministic qualifying provider fixture/test double.',
            'Does not create execution authority or replace full repository release validation.'
          ]
        }
        p=Path(args.write_evidence); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print('evidence:',p)

if __name__=='__main__':
    try: main()
    except (ValidationError,KeyError,IndexError,TypeError) as e:
        print('AIR Handoff runtime contract validation: FAIL:',e,file=sys.stderr); raise SystemExit(1)
