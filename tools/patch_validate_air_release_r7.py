from __future__ import annotations
from pathlib import Path

p=Path('tools/validate_air_release.py')
s=p.read_text(encoding='utf-8')

history_block="""
HISTORICAL_CONTAINER_KEYS = {
    'source_baseline', 'mainline_release_binding', 't7_change_record',
    'historical_release_catalogs', 'source_candidate_manifest', 'change_history',
    'release_history', 'historical_records',
}
R7_STATIC_PASS = 'PASS_R7_DETERMINISTIC_STATIC_SUITE'
R7_BEHAVIOR_PENDING = 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'
R7_INDEX_COMPLETENESS = 'COMPLETE_FOR_AIR_2_6_0_OBJECT_CONTRACT_SET_005_V071_RELEASE_CANDIDATE_SPECIALIST_CATALOG'
R7_CANDIDATE_STATE = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'

"""
if 'HISTORICAL_CONTAINER_KEYS = {' not in s:
    anchor='class ValidationError(Exception):\n'
    if anchor not in s: raise SystemExit('R7 release patch: ValidationError anchor missing')
    s=s.replace(anchor,history_block+anchor,1)

helper="""
def historical_path(path: tuple[str, ...]) -> bool:
    return any(part in HISTORICAL_CONTAINER_KEYS or part.startswith('historical_') for part in path)


def walk_current(obj: Any, fn, path: tuple[str, ...] = ()) -> None:
    if historical_path(path):
        return
    fn(obj, path)
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk_current(v, fn, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_current(v, fn, path + (str(i),))


"""
if 'def walk_current(' not in s:
    anchor='def parse_core_routes(core: str) -> dict[str, dict[str, str]]:\n'
    if anchor not in s: raise SystemExit('R7 release patch: parse_core_routes anchor missing')
    s=s.replace(anchor,helper+anchor,1)

s=s.replace('walk(parsed[p], lambda node, loc, owner=p: check_ref(node, loc, owner))','walk_current(parsed[p], lambda node, loc, owner=p: check_ref(node, loc, owner))')
s=s.replace('walk(parsed[p], reject_stale_peer_hash)','walk_current(parsed[p], reject_stale_peer_hash)')
s=s.replace('walk(parsed[p], lambda node, loc, owner=p: collect_behavioral_pass(node, loc, owner))','walk_current(parsed[p], lambda node, loc, owner=p: collect_behavioral_pass(node, loc, owner))')

r7_checks="""
    # R7 lifecycle/version/history truth and package reseal.
    require('Patch marker: AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1' in core, 'R7 candidate lifecycle marker missing')
    lifecycle = index.get('candidate_lifecycle_contract', {})
    require(lifecycle.get('current_candidate_state') == R7_CANDIDATE_STATE, 'R7 current candidate lifecycle mismatch')
    require(lifecycle.get('candidate_states_are_release_sealed') is False, 'R7 candidate state incorrectly release-sealed')
    require(index.get('catalog_scope', {}).get('catalog_completeness_claim') == R7_INDEX_COMPLETENESS, 'R7 Index completeness identity mismatch')
    require(index.get('validation_state', {}).get('static_validation') == R7_STATIC_PASS, 'R7 Index static validation state mismatch')
    require(index.get('validation_state', {}).get('behavioral_revalidation') == R7_BEHAVIOR_PENDING, 'R7 Index behavioral validation must remain pending without replay evidence')
    for entry in index['entries']:
        require(entry.get('availability_state') == R7_CANDIDATE_STATE, f'R7 candidate availability mismatch: {entry.get("package_identity")}')
    hist_release = index.get('catalog_scope', {}).get('historical_release_catalogs', [])
    require(hist_release == [{
        'kit_release': '0.7.0',
        'foundation_identity': 'AIR_FOUNDATION_2_5_0_OBJECT_CONTRACT_SET_004',
        'index_generation': 'V070',
        'catalog_completeness_claim': 'COMPLETE_FOR_AIR_2_5_0_SET_004_V070_RELEASE_SPECIALIST_CATALOG',
        'state': 'RELEASED_HISTORICAL_NON_OPERATIVE',
    }], 'R7 historical v0.7.0 catalog identity mismatch')

    expected_current_foundation_state = 'OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_' + EXPECTED_FOUNDATION_ID
    current_identity_count = 0
    for pp in sorted(ROOT.glob('profiles/**/*.json')):
        oo = parsed[pp]
        ir = oo.get('integration_refresh') if isinstance(oo, dict) else None
        if isinstance(ir, dict) and 'foundation_identity_state' in ir:
            current_identity_count += 1
            require(ir['foundation_identity_state'] == expected_current_foundation_state, f'{pp}: R7 current Foundation identity stale')
    require(current_identity_count == 21, f'R7 current Foundation identity carrier count changed: {current_identity_count}')

    for mp in sorted(ROOT.glob('profiles/**/*PACKAGE_MANIFEST.json')):
        mo = parsed[mp]
        for comp in mo.get('components', []):
            cp = mp.parent / comp['filename']
            co = parsed[cp]
            canonical_status = str(co.get('STATUS') or co.get('status') or '')
            require(comp.get('status') == canonical_status, f'{mp}: R7 component status mirror mismatch {comp["filename"]}')
            expected_availability = 'VALIDATED_AVAILABLE_UNBOUND' if 'STATIC_VALIDATED' in canonical_status else 'AVAILABLE_UNVALIDATED'
            require(comp.get('availability_state') == expected_availability, f'{mp}: R7 component availability mirror mismatch {comp["filename"]}')

    gov_manifest = parsed[ROOT / 'profiles' / 'governance specialist' / 'AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json']
    expected_roles = [c.get('role') for c in gov_manifest.get('components', [])]
    require(gov_manifest.get('failure_mode_integration_contract', {}).get('component_roles_observed') == expected_roles and all(expected_roles), 'R7 Governance component role mirror mismatch')

    sfv_method = parsed[ROOT / 'profiles' / 'specification first verification specialist' / 'AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json']
    sfv_vc = sfv_method.get('validation_contract', {})
    require('required_package_version' not in sfv_vc, 'R7 SFV stale required_package_version literal remains')
    require(sfv_vc.get('required_package_version_source') == '$.package_version' and sfv_vc.get('required_package_version_check') == 'EQUAL_TO_CANONICAL_TOP_LEVEL_PACKAGE_VERSION', 'R7 SFV package version source/check missing')

    cea_manifest = parsed[ROOT / 'profiles' / 'capability ecology architect' / 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json']
    require(cea_manifest.get('t7_change_record', {}).get('package_version') == '2.4.0', 'R7 T7 historical package_version rewritten')
    require(cea_manifest.get('t7_change_record', {}).get('source_package_version') == '2.3.9', 'R7 T7 historical source version rewritten')
"""
if '# R7 lifecycle/version/history truth and package reseal.' not in s:
    anchor="    inventory = parsed[ROOT / 'tests' / 'deterministic_contract_inventory.json']\n"
    if anchor not in s: raise SystemExit('R7 release patch: inventory anchor missing')
    s=s.replace(anchor,r7_checks+'\n'+anchor,1)

fixture_check="""
    r7_ids = {x.get('id') for x in fixtures.get('r7_lifecycle_reseal_cases', [])}
    require({
        'R7-LC-01-CANDIDATE-NOT-RELEASED',
        'R7-LC-02-BEHAVIORAL-EVIDENCE-BOUNDARY',
        'R7-LC-03-HISTORY-IMMUTABLE',
        'R7-LC-04-SFV-PACKAGE-VERSION-SOURCE',
        'R7-LC-05-GOVERNANCE-COMPONENT-ROLES',
    } <= r7_ids, 'R7 lifecycle/reseal regression fixtures missing')
"""
if "R7-LC-01-CANDIDATE-NOT-RELEASED" not in s:
    anchor="    require(len(fixtures.get('material_action_transaction_negative_cases', [])) >= 9, 'insufficient material action transaction fixtures')\n"
    if anchor not in s: raise SystemExit('R7 release patch: fixture anchor missing')
    s=s.replace(anchor,anchor+fixture_check,1)

p.write_text(s,encoding='utf-8')
print('R7 release validator patch applied')
