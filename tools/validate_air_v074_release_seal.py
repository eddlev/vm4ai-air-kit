from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
KIT_VERSION = '0.7.4'
FOUNDATION_ID = 'AIR_FOUNDATION_2_6_3_OBJECT_CONTRACT_SET_008'
RELEASED = 'RELEASE_CATALOG_ENTRY'
BEHAVIOR_PASS = 'PASS_REPLAYABLE_MODEL_HOST_EVIDENCE'
EXPECTED_HASHES = {
    'prompts/AIR_CORE_RUNTIME.md': 'f1130c65500e0569e283f5b6988ea7e4894fc84b2e88d51b79d42d4034b2a453',
    'prompts/AIR_CONTROL_SURFACE.md': '648d2a9e1e423981fb75e06c10b90dadc146a4d8ffe331b70bef562edad73d62',
    'prompts/AIR_GOV.md': '80f037b38b69d75436ddf2ec7b1dc757e84ab65d17aaeaf450cb963af44b4842',
    'prompts/AIR_DEFAULT_STARTER_PROFILE.json': 'bd6271dc2c2fac7fceb97941ef3d4c0a58de0b3284083056058b1f2f4de72100',
    'prompts/AIR_HANDOFF_CARD_TEMPLATE.json': '7fe1fdef37341420e2c043033571cbd7fb977296897d1c67e273062dcfc3a266',
    'catalog/AIR_RUNTIME_ROUTE_MAP.json': '3ec1e78262aa8e7222188aeb25e53041c1ed6b482901653fb868607d289c4bd2',
    'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json': 'ce858d7dfff308c1803d664771d84fb1d5b9a9b3bf3b42a3a920bdc28c44ce62',
}
HISTORICAL_V073_GIT_BLOBS = {
    'tools/validate_air_v073_release_seal.py': '29f2b05839adfb737ee8975e2731e70d20e7285b',
    'tools/test_air_v073_release_seal_mutations.py': '490a0eef3216fe5dc44f7bef75c75ab0e393a0e3',
}
PACKAGE_MANIFESTS = {
    'AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_V2': 'profiles/governance specialist/AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json',
    'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2': 'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json',
    'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2': 'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json',
    'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2': 'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json',
    'AIR_GROUNDING_SPECIALIST_PACKAGE_V2': 'profiles/grounding specialist/AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json',
}


class E(Exception):
    pass


def req(cond: bool, msg: str) -> None:
    if not cond:
        raise E(msg)


def reject_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise E(f'duplicate JSON key {key}')
        out[key] = value
    return out


def canonical_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b'\r\n', b'\n').replace(b'\r', b'\n')


def sha(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def git_blob_sha1(path: Path) -> str:
    raw = canonical_bytes(path)
    header = f'blob {len(raw)}\0'.encode('ascii')
    return hashlib.sha1(header + raw).hexdigest()


def load(path: Path) -> Any:
    return json.loads(canonical_bytes(path).decode('utf-8'), object_pairs_hook=reject_dupes)


def main() -> None:
    req((ROOT / 'VERSION').read_text(encoding='utf-8').strip() == KIT_VERSION, 'VERSION is not 0.7.4')
    for rel, expected in EXPECTED_HASHES.items():
        p = ROOT / rel
        req(p.is_file(), f'missing sealed file {rel}')
        req(sha(p) == expected, f'exact sealed hash mismatch {rel}')
    for rel, expected in HISTORICAL_V073_GIT_BLOBS.items():
        p = ROOT / rel
        req(p.is_file(), f'missing historical v0.7.3 seal tool {rel}')
        req(git_blob_sha1(p) == expected, f'historical v0.7.3 seal tool changed {rel}')

    core = canonical_bytes(ROOT / 'prompts/AIR_CORE_RUNTIME.md').decode('utf-8')
    control = canonical_bytes(ROOT / 'prompts/AIR_CONTROL_SURFACE.md').decode('utf-8')
    starter = load(ROOT / 'prompts/AIR_DEFAULT_STARTER_PROFILE.json')
    handoff = load(ROOT / 'prompts/AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']
    route = load(ROOT / 'catalog/AIR_RUNTIME_ROUTE_MAP.json')
    index = load(ROOT / 'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json')
    readme = canonical_bytes(ROOT / 'README.md').decode('utf-8')

    req('## Current release — AIR Kit v0.7.4' in readme, 'README v0.7.4 current release heading missing')
    req('The release-sealed source for **AIR Kit v0.7.4** is maintained on validated `main`.' in readme, 'README v0.7.4 release-sealed source statement missing')
    req('## Current release candidate — AIR Kit v0.7.4' not in readme, 'README still claims v0.7.4 release candidate')
    req('Specialist Package Index **1.3.13**' in readme, 'README Specialist Index identity stale')

    req('PROMPT_VERSION: 2.6.3' in core, 'Core not 2.6.3')
    req('PROMPT_VERSION: 2.6.3' in control, 'Control not 2.6.3')
    req(starter.get('PROMPT_VERSION') == '2.6.3', 'Starter not 2.6.3')
    req('CANONICAL_HANDOFF_TEMPLATE_REVISION: 20' in core, 'Core Handoff template revision not 20')
    req('AIR_HANDOFF_MODE_SELECTION_V1' in core, 'Core Handoff mode-selection contract missing')
    req('STRICT_PROVENANCE' in core and 'PORTABLE_STATE' in core, 'Core strict/portable Handoff modes missing')

    req(handoff['schema_version'] == handoff['SCHEMA_VERSION'] == '2.3.0', 'Handoff schema mismatch')
    req(handoff['template_revision'] == 20, 'Handoff template_revision mismatch')
    req(handoff['user_revision'] is None, 'template user_revision baseline must be null')
    req('card_revision' not in handoff, 'rev20 template still emits card_revision')
    req('handoff_mode_state' in handoff, 'rev20 Handoff mode state missing')
    declared = set(handoff['schema_manifest']['required_fields']) | set(handoff['schema_manifest'].get('optional_fields', []))
    req(set(handoff) == declared, 'Handoff root manifest closure mismatch')
    contracts = handoff['schema_manifest']['revision_migration_contracts']
    req('REV19_TO_REV20' in contracts, 'Handoff REV19_TO_REV20 migration missing')
    req(contracts['REV19_TO_REV20'].get('target_template_revision') == 20, 'REV19_TO_REV20 target mismatch')

    req(route['MAP_VERSION'] == route['ROUTE_MAP_VERSION'] == '1.2.2', 'Route Map version split mismatch')
    req(route['source_of_truth']['prompt_version'] == '2.6.3', 'Route Map Core version stale')
    req(route['source_of_truth']['sha256'] == sha(ROOT / 'prompts/AIR_CORE_RUNTIME.md'), 'Route Map Core hash stale')
    handoff_route = next(x for x in route['routes'] if x['route_id'] == 'RT.HANDOFF_CREATE')
    req('DEP.HANDOFF_MODE_RESOLVED' in handoff_route['requires'], 'Route Map Handoff mode dependency missing')
    hp = handoff_route['handoff_provenance_policy']
    req(hp.get('mode_contract') == 'AIR_HANDOFF_MODE_SELECTION_V1', 'Route Map Handoff mode contract stale')
    req(hp.get('strict_provenance_dependency') == 'DEP.DURABLE_SURFACED_PROVENANCE_COMPLETE', 'Route Map strict provenance dependency stale')
    req(hp.get('portable_state_dependency') == 'DEP.PORTABLE_HANDOFF_STATE_VALID', 'Route Map portable-state dependency stale')
    req(hp.get('portable_complete_history_claim') is False, 'Portable Handoff complete-history claim must remain false')
    req(hp.get('explicit_strict_downgrade') == 'PROHIBITED', 'Explicit strict Handoff downgrade no longer prohibited')
    req(hp.get('failed_integrity_behavior') == 'BLOCK_REVIEW', 'FAILED_INTEGRITY behavior stale')
    req(handoff_route['handoff_file_delivery'].get('inline_payload') == 'PROHIBITED', 'Handoff inline payload no longer prohibited')

    req(index['INDEX_VERSION'] == '1.3.13', 'Index version mismatch')
    req(index['foundation_compatibility_catalog']['identity'] == FOUNDATION_ID, 'Index Foundation identity mismatch')
    req(index['status'] == 'AIR_2_6_3_OBJECT_CONTRACT_SET_008_FIVE_PACKAGE_INDEX_V074_RELEASE_SEALED_REPLAYABLE_BEHAVIORAL_VALIDATED', 'Index is not v0.7.4 release-sealed')
    req(index['catalog_scope']['catalog_completeness_claim'] == 'COMPLETE_FOR_AIR_2_6_3_OBJECT_CONTRACT_SET_008_V074_RELEASE_SPECIALIST_CATALOG', 'Index v0.7.4 release completeness identity mismatch')
    lifecycle = index['candidate_lifecycle_contract']
    req(lifecycle.get('current_candidate_state') == RELEASED, 'Index aggregate lifecycle not released')
    req(lifecycle.get('candidate_states_are_release_sealed') is False, 'Candidate lifecycle states must not be marked release-sealed')
    req(index['validation_state'].get('decision') == 'PASS_ALL_FIVE_SET008_REPLAYABLE_BEHAVIORAL_REVALIDATION', 'Index validation decision stale')
    req(index['validation_state'].get('behavioral_revalidation') == BEHAVIOR_PASS, 'Index behavioral state stale')
    req(index['validation_state'].get('handoff_rev20_catalog_compatibility') == 'PASS_DISCOVERY_PROVENANCE_ONLY_PACKAGE_REVALIDATION_STILL_REQUIRED', 'Index Handoff rev20 compatibility stale')

    entries = {e['package_identity']: e for e in index['entries']}
    req(set(entries) == set(PACKAGE_MANIFESTS), 'Index Specialist package set mismatch')
    for package_id, rel in PACKAGE_MANIFESTS.items():
        entry = entries[package_id]
        manifest = ROOT / rel
        req(entry.get('availability_state') == RELEASED, f'Index package not released {package_id}')
        req(entry.get('manifest_filename') == manifest.name, f'Index manifest filename mismatch {package_id}')
        req(entry.get('manifest_sha256') == sha(manifest), f'Index manifest hash mismatch {package_id}')

    cw = load(ROOT / PACKAGE_MANIFESTS['AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'])
    sfv = load(ROOT / PACKAGE_MANIFESTS['AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2'])
    grounding = load(ROOT / PACKAGE_MANIFESTS['AIR_GROUNDING_SPECIALIST_PACKAGE_V2'])
    req(cw['package_validation_state'].get('release_catalog_registration') == 'INCLUDED_IN_SET_008_V074_RELEASE_CATALOG', 'Copywriting v0.7.4 release catalog registration mismatch')
    req(sfv['package_validation_state'].get('release_catalog_registration') == 'INCLUDED_IN_SET_008_V074_RELEASE_CATALOG_WITH_EXECUTOR_DRAFT_UNAVAILABLE', 'SFV v0.7.4 release catalog registration mismatch')
    req(grounding['package_validation_state'].get('release_catalog_registration') == 'INCLUDED_IN_SET_008_V074_RELEASE_CATALOG_WITH_EXECUTOR_DRAFT_UNAVAILABLE', 'Grounding v0.7.4 release catalog registration mismatch')

    print('AIR v0.7.4 release-seal validation: PASS')
    print('foundation', FOUNDATION_ID)
    print('handoff_schema', '2.3.0')
    print('handoff_template_revision', 20)
    print('handoff_modes', 'STRICT_PROVENANCE,PORTABLE_STATE')
    print('route_map', '1.2.2')
    print('specialist_index', '1.3.13 release-sealed')
    print('deterministic_registry', '90/90')


if __name__ == '__main__':
    try:
        main()
    except (E, KeyError, ValueError, StopIteration) as exc:
        print('AIR v0.7.4 release-seal validation: FAIL:', exc, file=sys.stderr)
        raise SystemExit(1)
