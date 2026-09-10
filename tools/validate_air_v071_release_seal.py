from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
RELEASED = 'RELEASE_CATALOG_ENTRY'
STATUS_RELEASED = 'AIR_2_6_0_OBJECT_CONTRACT_SET_005_FIVE_PACKAGE_INDEX_V071_RELEASE_SEALED'
COMPLETE_RELEASED = 'COMPLETE_FOR_AIR_2_6_0_OBJECT_CONTRACT_SET_005_V071_RELEASE_SPECIALIST_CATALOG'
DECISION_RELEASED = 'RELEASE_SEALED_MAINTAINER_ACCEPTED_ACTIVE_USE_WITH_REPLAYABLE_MODEL_HOST_EVIDENCE_PENDING'


class E(Exception):
    pass


def req(condition: bool, message: str) -> None:
    if not condition:
        raise E(message)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    req((ROOT / 'VERSION').read_text(encoding='utf-8').strip() == '0.7.1', 'AIR Kit VERSION is not 0.7.1')
    idx = load(ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json')

    req(idx.get('status') == STATUS_RELEASED, 'Specialist Index is not v0.7.1 release-sealed')
    req(idx.get('catalog_scope', {}).get('catalog_completeness_claim') == COMPLETE_RELEASED, 'release catalog completeness identity mismatch')

    validation = idx.get('validation_state', {})
    req(validation.get('decision') == DECISION_RELEASED, 'maintainer release acceptance decision missing')
    req(validation.get('behavioral_revalidation') == 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE', 'release seal must preserve replayable/model-host evidence truth')
    req(validation.get('release_publication_state') == 'EXTERNAL_RELEASE_STATE_NOT_RUNTIME_AUTHORITY', 'runtime catalog must not self-assert publication')
    req(validation.get('operative_lifecycle_coherence') == 'PASS_V071_RELEASE_SEALED_LIFECYCLE', 'release lifecycle coherence marker mismatch')

    lifecycle = idx.get('candidate_lifecycle_contract', {})
    req(lifecycle.get('current_candidate_state') == RELEASED, 'current lifecycle state is not RELEASE_CATALOG_ENTRY')
    req(lifecycle.get('released_state') == RELEASED, 'released lifecycle token mismatch')
    req(lifecycle.get('candidate_states_are_release_sealed') is False, 'candidate states must remain non-release-sealed')

    req(len(idx.get('entries', [])) == 5, 'Specialist release catalog entry count mismatch')
    for entry in idx['entries']:
        req(entry.get('availability_state') == RELEASED, f"{entry.get('package_identity')}: entry not release-sealed")
        manifest_name = entry.get('manifest_filename')
        matches = list((ROOT / 'profiles').glob(f'**/{manifest_name}'))
        req(len(matches) == 1, f'{manifest_name}: manifest target missing or ambiguous')
        req(entry.get('manifest_sha256') == sha256(matches[0]), f'{manifest_name}: release-sealed manifest hash mismatch')

    hist = idx.get('catalog_scope', {}).get('historical_release_catalogs', [])
    req(hist == [{
        'kit_release': '0.7.0',
        'foundation_identity': 'AIR_FOUNDATION_2_5_0_OBJECT_CONTRACT_SET_004',
        'index_generation': 'V070',
        'catalog_completeness_claim': 'COMPLETE_FOR_AIR_2_5_0_SET_004_V070_RELEASE_SPECIALIST_CATALOG',
        'state': 'RELEASED_HISTORICAL_NON_OPERATIVE',
    }], 'v0.7.0 historical release record changed')

    raw = (ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json').read_text(encoding='utf-8')
    req('BEHAVIORAL_REVALIDATION_PASS' not in raw, 'release seal synthesized unsupported behavioral PASS')
    req('PASS_CURRENT_SESSION_PROMPT_RUNTIME_REPRESENTATIVE_SCENARIO_REVALIDATION' not in raw, 'release seal restored stale behavioral PASS claim')
    req('Handoff schema 2.3.0 rev15 may record this index identity' not in raw, 'stale rev15 release-catalog provenance rule remains')

    print('AIR v0.7.1 release-seal validation: PASS')
    print('release_catalog_entries 5')
    print('release_lifecycle RELEASE_CATALOG_ENTRY')
    print('replayable_model_host_evidence PENDING')
    print('publication_state EXTERNAL_ONLY')


if __name__ == '__main__':
    try:
        main()
    except (E, KeyError, ValueError) as exc:
        print(f'AIR v0.7.1 release-seal validation: FAIL: {exc}', file=sys.stderr)
        raise SystemExit(1)
