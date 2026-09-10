from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
CANDIDATE = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'
RELEASED = 'RELEASE_CATALOG_ENTRY'
STATUS_CANDIDATE = 'AIR_2_6_0_OBJECT_CONTRACT_SET_005_FIVE_PACKAGE_INDEX_V071_RELEASE_CANDIDATE'
STATUS_RELEASED = 'AIR_2_6_0_OBJECT_CONTRACT_SET_005_FIVE_PACKAGE_INDEX_V071_RELEASE_SEALED'
COMPLETE_CANDIDATE = 'COMPLETE_FOR_AIR_2_6_0_OBJECT_CONTRACT_SET_005_V071_RELEASE_CANDIDATE_SPECIALIST_CATALOG'
COMPLETE_RELEASED = 'COMPLETE_FOR_AIR_2_6_0_OBJECT_CONTRACT_SET_005_V071_RELEASE_SPECIALIST_CATALOG'
DECISION_RELEASED = 'RELEASE_SEALED_MAINTAINER_ACCEPTED_ACTIVE_USE_WITH_REPLAYABLE_MODEL_HOST_EVIDENCE_PENDING'
LIFECYCLE_RELEASED = 'PASS_V071_RELEASE_SEALED_LIFECYCLE'


def dump_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding='utf-8')
    if new in text:
        return
    if old not in text:
        raise SystemExit(f'{path}: expected release-seal anchor not found: {old!r}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


def main() -> None:
    index_path = ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json'
    index = json.loads(index_path.read_text(encoding='utf-8'))

    if index.get('status') not in {STATUS_CANDIDATE, STATUS_RELEASED}:
        raise SystemExit(f'unexpected Specialist Index status: {index.get("status")!r}')
    index['status'] = STATUS_RELEASED

    scope = index['catalog_scope']
    if scope.get('catalog_completeness_claim') not in {COMPLETE_CANDIDATE, COMPLETE_RELEASED}:
        raise SystemExit('unexpected Specialist Index completeness claim')
    scope['catalog_completeness_claim'] = COMPLETE_RELEASED

    index['index_rules'] = [
        rule.replace('candidate release-catalog identity', 'release-catalog identity')
            .replace('Handoff schema 2.3.0 rev15', 'Handoff schema 2.3.0 rev16')
        for rule in index['index_rules']
    ]
    index['authority_boundary']['operative_rule'] = index['authority_boundary']['operative_rule'].replace(
        'candidate release-catalog identity', 'release-catalog identity'
    )

    validation = index['validation_state']
    validation['decision'] = DECISION_RELEASED
    validation['operative_lifecycle_coherence'] = LIFECYCLE_RELEASED
    validation['release_publication_rule'] = (
        'Verify tag/release/publication through the current external repository/release surface at release time. '
        'Release-sealed catalog bytes do not assert completed publication as runtime truth.'
    )
    if validation.get('behavioral_revalidation') != 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE':
        raise SystemExit('release seal must not synthesize replayable/model-host behavioral PASS evidence')

    for entry in index['entries']:
        entry['availability_state'] = RELEASED

    lifecycle = index['candidate_lifecycle_contract']
    lifecycle['current_candidate_state'] = RELEASED
    lifecycle['candidate_states_are_release_sealed'] = False

    dump_json(index_path, index)

    r7 = ROOT / 'tools' / 'validate_air_r7_remediation.py'
    replace_once(r7, "req(idx['status']=='AIR_2_6_0_OBJECT_CONTRACT_SET_005_FIVE_PACKAGE_INDEX_V071_RELEASE_CANDIDATE','073 current index status incoherent')", "req(idx['status']=='AIR_2_6_0_OBJECT_CONTRACT_SET_005_FIVE_PACKAGE_INDEX_V071_RELEASE_SEALED','073 current index status incoherent')")
    replace_once(r7, "req(idx['catalog_scope']['catalog_completeness_claim']=='COMPLETE_FOR_AIR_2_6_0_OBJECT_CONTRACT_SET_005_V071_RELEASE_CANDIDATE_SPECIALIST_CATALOG','073 completeness identity incoherent')", "req(idx['catalog_scope']['catalog_completeness_claim']=='COMPLETE_FOR_AIR_2_6_0_OBJECT_CONTRACT_SET_005_V071_RELEASE_SPECIALIST_CATALOG','073 completeness identity incoherent')")
    replace_once(r7, "req(lc.get('current_candidate_state')=='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION' and lc.get('candidate_states_are_release_sealed') is False,'006 candidate state semantics wrong')", "req(lc.get('current_candidate_state')=='RELEASE_CATALOG_ENTRY' and lc.get('candidate_states_are_release_sealed') is False,'006 release state semantics wrong')")
    replace_once(r7, "req(e['availability_state']=='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION','006 index entry lifecycle mismatch')", "req(e['availability_state']=='RELEASE_CATALOG_ENTRY','006 index entry lifecycle mismatch')")

    release = ROOT / 'tools' / 'validate_air_release.py'
    replace_once(release, "R7_INDEX_COMPLETENESS = 'COMPLETE_FOR_AIR_2_6_0_OBJECT_CONTRACT_SET_005_V071_RELEASE_CANDIDATE_SPECIALIST_CATALOG'", "R7_INDEX_COMPLETENESS = 'COMPLETE_FOR_AIR_2_6_0_OBJECT_CONTRACT_SET_005_V071_RELEASE_SPECIALIST_CATALOG'")
    replace_once(release, "R7_CANDIDATE_STATE = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'", "R7_CANDIDATE_STATE = 'RELEASE_CATALOG_ENTRY'")

    mut = ROOT / 'tools' / 'test_air_r7_mutations.py'
    replace_once(mut, "add('R7-N02-INDEX-CANDIDATE-PREMATURE-RELEASE','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:o['entries'][0].__setitem__('availability_state','RELEASE_CATALOG_ENTRY')))" , "add('R7-N02-INDEX-RELEASE-DEMOTED-TO-CANDIDATE','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:o['entries'][0].__setitem__('availability_state','RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION')))" )

    suite = ROOT / 'tools' / 'validate_air_suite.py'
    replace_once(suite, "    run_stage('release_contract', [py, 'tools/validate_air_release.py'])\n", "    run_stage('release_contract', [py, 'tools/validate_air_release.py'])\n    run_stage('v071_release_seal', [py, 'tools/validate_air_v071_release_seal.py'])\n")
    replace_once(suite, "        run_stage('r8_low_risk_presentation_portability_mutations', [py, 'tools/test_air_r8_mutations.py', '.', 'tools/validate_air_r8_remediation.py'])\n", "        run_stage('r8_low_risk_presentation_portability_mutations', [py, 'tools/test_air_r8_mutations.py', '.', 'tools/validate_air_r8_remediation.py'])\n        run_stage('v071_release_seal_mutations', [py, 'tools/test_air_v071_release_seal_mutations.py'])\n")

    print('AIR v0.7.1 release-seal transition applied')
    print('replayable_model_host_evidence PENDING')
    print('release_acceptance MAINTAINER_APPROVED_ACTIVE_USE')


if __name__ == '__main__':
    main()
