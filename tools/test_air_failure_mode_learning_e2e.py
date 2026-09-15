from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path('.').resolve()


class ReplayError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReplayError(message)


def load(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode('utf-8')).hexdigest()


def canonicalize_signature(signature: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    required_keys = list(schema.get('required_keys', []))
    require(set(signature) == set(required_keys), 'applicability signature key set mismatch')
    out: dict[str, Any] = {}
    for key in required_keys:
        value = signature[key]
        if key in {'component_ids', 'source_evidence_condition_ids'}:
            require(isinstance(value, list) and all(isinstance(x, str) for x in value), f'{key} must be a string array')
            out[key] = sorted(set(value))
        else:
            require(isinstance(value, str) and value != '', f'{key} must be a non-empty string')
            out[key] = value
    return out


def signature_hash(signature: dict[str, Any], schema: dict[str, Any]) -> str:
    return canonical_hash(canonicalize_signature(signature, schema))


def query_exact_matches(registry: dict[str, Any], current_signature: dict[str, Any], schema: dict[str, Any]) -> list[dict[str, Any]]:
    registry['query_count'] = registry.get('query_count', 0) + 1
    current_hash = signature_hash(current_signature, schema)
    return [record for record in registry.get('records', []) if record.get('applicability_signature_hash') == current_hash]


def compile_constraint_into_artifact(artifact: dict[str, Any], record: dict[str, Any]) -> None:
    artifact.setdefault('failure_mode_constraint_refs', []).append(record['failure_mode_id'])
    artifact.setdefault('compiled_corrective_constraints', []).append(record['corrective_constraint'])


def specialist_attempt_registry_mutation(
    specialist_contract: dict[str, Any],
    registry: dict[str, Any],
    mutation: dict[str, Any],
) -> bool:
    if specialist_contract.get('package_or_component_registry_mutation_authority') == 'NONE':
        return False
    registry.update(mutation)
    return True


def main() -> None:
    starter = load('prompts/AIR_DEFAULT_STARTER_PROFILE.json')
    handoff = load('prompts/AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']
    fixtures = load('tests/air_contract_fixtures.json')
    specialist_manifest = load('profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json')

    fm = starter['compiler_contract']['failure_mode_registry']
    signature_schema = fm['applicability_signature_schema']
    handoff_fm = handoff['failure_mode_state']
    specialist_fm = specialist_manifest['failure_mode_integration_contract']

    expected_signature_keys = [
        'signature_version',
        'task_family_id',
        'route_id',
        'control_event_id',
        'action_class',
        'artifact_class',
        'failure_class',
        'component_ids',
        'environment_class',
        'source_evidence_condition_ids',
    ]

    fixture_ids = {case.get('id') for case in fixtures.get('failure_mode_learning_cases', [])}
    require(
        {
            'FM-01-RETRY-EXACT-MATCH',
            'FM-02-MITIGATION-RETENTION',
            'FM-03-RECURRENCE',
            'FM-04-COMPATIBLE-NOT-EXACT',
            'FM-05-SPECIALIST-PACKAGE',
            'FM-06-HANDOFF-PERSISTENCE',
        } <= fixture_ids,
        'FM-01 through FM-06 failure-mode fixtures are not all present',
    )
    print('FM-E2E-01 fixture coverage: PASS')

    require(fm.get('required') is True, 'Starter failure-mode registry is not required')
    require(fm.get('owner') == 'AIR_CORE_RUNTIME_V2', 'failure-mode registry owner is not Core')
    require(fm.get('automatic_applicability') == 'EXACT_MATCH_ONLY', 'automatic applicability is not exact-match only')
    require(fm.get('pre_retry_query_required') is True, 'pre-retry registry query is not required')
    require(fm.get('successful_retest_state') == 'MITIGATED_RETAIN_FOR_REGRESSION', 'successful retest state drifted')
    require(fm.get('specialist_registry_mutation_authority') == 'NONE', 'Starter grants Specialist registry mutation authority')
    require(fm.get('handoff_path') == 'AIR_HANDOFF_CARD.failure_mode_state', 'Starter failure-mode Handoff path drifted')
    require(fm.get('failure_record_source_ledger_entry_required') is True, 'Starter no longer requires ledger-backed failure records')
    require(signature_schema.get('required_keys') == expected_signature_keys, 'applicability signature schema drifted')
    require(signature_schema.get('array_canonicalization') == 'SORTED_UNIQUE_STRINGS', 'signature array canonicalization drifted')
    require(handoff_fm.get('registry_version') == fm.get('registry_version'), 'Handoff failure registry version mismatch')
    require(handoff_fm.get('positive_execution_authority') == 'NONE', 'restored Handoff failure state gained execution authority')
    require(handoff_fm.get('automatic_match_rule') == 'EXACT_CANONICAL_SIGNATURE_HASH_EQUALITY_ONLY_AFTER_RESTORE_VALIDATION', 'Handoff automatic match rule drifted')
    require(handoff_fm.get('source_history_carrier') == 'AIR_HANDOFF_CARD.surfaced_object_ledger_state', 'Handoff failure source-history carrier drifted')
    require(specialist_fm.get('pre_execution_query_required') is True, 'Specialist pre-execution failure registry query missing')
    require(specialist_fm.get('automatic_applicability') == 'EXACT_MATCH_ONLY', 'Specialist failure applicability is not exact-match only')
    require(specialist_fm.get('package_or_component_registry_mutation_authority') == 'NONE', 'Specialist package gained Core registry mutation authority')
    require(specialist_fm.get('failure_record_source') == 'CORE_LEDGER_BACKED_AIR_FAILURE_MODE_RECORD_ONLY', 'Specialist failure record source drifted')
    print('FM-E2E-02 live contract carriers: PASS')

    initial_signature = {
        'signature_version': '1.0.0',
        'task_family_id': 'AIR_FAILURE_MODE_E2E_REPLAY',
        'route_id': 'RT.ACTION',
        'control_event_id': 'CE.E2E.FAILURE.RETRY',
        'action_class': 'REPOSITORY_PATCH',
        'artifact_class': 'AIR_ARTIFACT',
        'failure_class': 'EXECUTION_DEFECT',
        'component_ids': ['AIR_CAPABILITY_ECOLOGY_ARCHITECT_V2'],
        'environment_class': 'LOCAL_DETERMINISTIC_TEST',
        'source_evidence_condition_ids': ['OPERATOR_CONFIRMED_EXECUTION_DEFECT'],
    }
    canonical_signature = canonicalize_signature(initial_signature, signature_schema)
    applicability_hash = signature_hash(canonical_signature, signature_schema)
    record = {
        'failure_mode_id': 'FM-E2E-001',
        'failure_class': 'EXECUTION_DEFECT',
        'lifecycle_state': 'ACTIVE_CORRECTIVE_CONSTRAINT',
        'root_cause_state': 'ESTABLISHED',
        'corrective_constraint': 'USE_VALIDATED_PATCH_TRANSPORT_AND_PRECHECK_BEFORE_RETRY',
        'prohibited_retry_pattern': 'REPEAT_UNVALIDATED_PATCH_TRANSPORT',
        'applicability_signature': canonical_signature,
        'applicability_signature_hash': applicability_hash,
        'applicability_state': 'EXACT_MATCH',
        'retest_requirement': 'REPLAY_SAME_EXACT_SIGNATURE_WITH_CORRECTIVE_CONSTRAINT',
        'retest_state': 'PENDING',
        'recurrence_count': 0,
        'source_ledger_entry_ref': 'AIR_SURFACED_OBJECT_LEDGER_ENTRY::LEDGER-E2E::1',
        'specialist_or_method_refs': ['AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2'],
        'evidence_refs': ['EVIDENCE-E2E-FIRST-FAILURE'],
    }
    core_registry = {
        'registry_version': fm['registry_version'],
        'owner': fm['owner'],
        'records': [copy.deepcopy(record)],
        'query_count': 0,
    }
    print('FM-E2E-03 first evidenced Core-owned failure: PASS')

    query_before = core_registry['query_count']
    matches = query_exact_matches(core_registry, initial_signature, signature_schema)
    require(core_registry['query_count'] == query_before + 1, 'retry did not query registry first')
    require(len(matches) == 1 and matches[0]['failure_mode_id'] == record['failure_mode_id'], 'exact retry did not match stable failure record')
    retry_artifact = {
        'artifact_id': 'AIR-ART-E2E-RETRY-001',
        'failure_mode_constraint_refs': [],
        'compiled_corrective_constraints': [],
    }
    compile_constraint_into_artifact(retry_artifact, matches[0])
    require(record['failure_mode_id'] in retry_artifact['failure_mode_constraint_refs'], 'corrective constraint ref was not compiled into retry Artifact')
    require(record['corrective_constraint'] in retry_artifact['compiled_corrective_constraints'], 'corrective constraint was not compiled into retry Artifact')
    retry_pattern = 'VALIDATED_PATCH_TRANSPORT_AFTER_PRECHECK'
    require(retry_pattern != record['prohibited_retry_pattern'], 'retry repeated prohibited failure pattern')
    print('FM-E2E-04 exact retry and Artifact constraint compilation: PASS')

    retained = core_registry['records'][0]
    retained['lifecycle_state'] = fm['successful_retest_state']
    retained['retest_state'] = 'PASS'
    core_registry['mitigated_retain_for_regression_refs'] = [retained['failure_mode_id']]
    require(retained['lifecycle_state'] == 'MITIGATED_RETAIN_FOR_REGRESSION', 'successful retest did not retain mitigation')
    require(len(core_registry['records']) == 1, 'successful retest deleted the failure record')
    print('FM-E2E-05 successful retest retains mitigation: PASS')

    handoff_carrier = copy.deepcopy(handoff_fm)
    handoff_carrier['records'] = [copy.deepcopy(retained)]
    handoff_carrier['active_corrective_constraint_refs'] = []
    handoff_carrier['mitigated_retain_for_regression_refs'] = [retained['failure_mode_id']]
    serialized = canonical_json(handoff_carrier).encode('utf-8')
    restored_carrier = json.loads(serialized.decode('utf-8'))
    require(restored_carrier['records'][0] == retained, 'Handoff mutated failure record values')
    require(restored_carrier.get('positive_execution_authority') == 'NONE', 'Handoff failure record restored with positive authority')
    restored_registry = {
        'registry_version': restored_carrier['registry_version'],
        'validation_state': 'UNVALIDATED_BOOTSTRAP_INPUT',
        'positive_execution_authority': restored_carrier['positive_execution_authority'],
        'records': restored_carrier['records'],
        'query_count': 0,
    }
    restored_matches = query_exact_matches(restored_registry, initial_signature, signature_schema)
    require(len(restored_matches) == 1, 'restored exact signature was not discoverable for validation')
    require(restored_registry['validation_state'] != 'VALIDATED_CURRENT', 'restored failure state was silently validated')
    later_artifact = {
        'artifact_id': 'AIR-ART-E2E-RESTORE-001',
        'failure_mode_constraint_refs': [],
        'compiled_corrective_constraints': [],
    }
    automatic_before_validation = (
        restored_registry['validation_state'] == 'VALIDATED_CURRENT'
        and retained['failure_mode_id'] in later_artifact['failure_mode_constraint_refs']
    )
    require(automatic_before_validation is False, 'restored mitigation became operative before restore validation/Artifact compilation')
    restored_registry['validation_state'] = 'VALIDATED_CURRENT'
    compile_constraint_into_artifact(later_artifact, restored_matches[0])
    automatic_after_validation = (
        restored_registry['validation_state'] == 'VALIDATED_CURRENT'
        and retained['failure_mode_id'] in later_artifact['failure_mode_constraint_refs']
    )
    require(automatic_after_validation is True, 'validated restored exact match did not become reusable through rebound Artifact')
    print('FM-E2E-06 Handoff persistence, restore validation, and later exact reuse: PASS')

    non_exact_signature = copy.deepcopy(initial_signature)
    non_exact_signature['environment_class'] = 'DIFFERENT_ENVIRONMENT_CLASS'
    require(signature_hash(non_exact_signature, signature_schema) != applicability_hash, 'non-exact signature unexpectedly hashed equal')
    non_exact_matches = query_exact_matches(restored_registry, non_exact_signature, signature_schema)
    require(non_exact_matches == [], 'non-exact signature activated a failure record automatically')
    print('FM-E2E-07 non-exact automatic applicability rejection: PASS')

    recurrence_matches = query_exact_matches(core_registry, initial_signature, signature_schema)
    require(len(recurrence_matches) == 1, 'recurrence exact signature did not locate retained record')
    recurrence_record = recurrence_matches[0]
    require(recurrence_record['lifecycle_state'] == 'MITIGATED_RETAIN_FOR_REGRESSION', 'recurrence did not start from mitigated state')
    recurrence_record['recurrence_count'] += 1
    recurrence_record['lifecycle_state'] = 'RECURRENT'
    recurrence_record['root_cause_or_constraint_review_required'] = True
    require(recurrence_record['recurrence_count'] == 1, 'recurrence_count did not increment')
    require(recurrence_record['lifecycle_state'] == 'RECURRENT', 'recurrence lifecycle did not become RECURRENT')
    require(recurrence_record['root_cause_or_constraint_review_required'] is True, 'recurrence did not require root-cause/corrective review')
    print('FM-E2E-08 recurrence lifecycle: PASS')

    specialist_query_before = core_registry['query_count']
    specialist_matches = query_exact_matches(core_registry, initial_signature, signature_schema)
    require(core_registry['query_count'] == specialist_query_before + 1, 'Specialist execution did not query Core registry first')
    require(len(specialist_matches) == 1, 'Specialist did not receive applicable Core failure record')
    core_before_specialist = canonical_hash(core_registry)
    mutation_applied = specialist_attempt_registry_mutation(
        specialist_fm,
        core_registry,
        {'records': []},
    )
    require(mutation_applied is False, 'Specialist-side Core registry mutation was allowed')
    require(canonical_hash(core_registry) == core_before_specialist, 'Specialist attempt mutated Core registry')
    print('FM-E2E-09 Specialist consumes Core record without mutation authority: PASS')

    print('AIR failure-mode learning E2E replay: PASS (9/9 stages)')


if __name__ == '__main__':
    try:
        main()
    except ReplayError as exc:
        raise SystemExit(f'AIR failure-mode learning E2E replay FAILED: {exc}')
