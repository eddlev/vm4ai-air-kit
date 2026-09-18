from __future__ import annotations
import sys
from pathlib import Path
from validate_air_r1_remediation import E, load, eval_registry


def main(root: Path) -> None:
    starter_path=root/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'
    starter=load(starter_path)
    registry=starter.get('validation_contract',{}).get('deterministic_contract_registry',{})
    if registry.get('execution_semantics')!='DETERMINISTIC_PIPELINE':
        raise E('registry execution_semantics mismatch')
    if registry.get('inference_policy')!='PROHIBITED':
        raise E('registry inference_policy mismatch')
    if registry.get('prose_authority')!='NON_OPERATIVE_DESCRIPTION':
        raise E('registry prose authority mismatch')
    n=eval_registry(root,starter)
    full_surface=starter.get('compiler_contract',{}).get('full_surface_integrity_audit',{})
    if full_surface.get('required_for_candidate_and_public_release') is not True:
        raise E('full-surface integrity audit not required for candidate/public release')
    if full_surface.get('contract')!='AIR_FULL_SURFACE_INTEGRITY_AUDIT_V1':
        raise E('full-surface integrity contract identity mismatch')
    hard=set(full_surface.get('hard_floor_invariants',[]))
    if 'AIR-FLOOR-029-MANDATORY-VISIBLE-ALIGNMENT-AND-VALIDATION' not in hard:
        raise E('Floor 029 missing from Starter full-surface registry')
    if 'AIR-FLOOR-030-NEW-TASK-ARTIFACT-VISIBLE-BEFORE-CONTINUATION' not in hard:
        raise E('Floor 030 missing from Starter full-surface registry')
    manifest=load(root/'tests/air_full_surface_coverage_manifest.json')
    scenarios=load(root/'tests/air_full_surface_scenario_matrix.json')
    if manifest.get('discovered_file_count')!=len(manifest.get('files',[])):
        raise E('full-surface manifest discovered count mismatch')
    if len(scenarios.get('scenarios',[]))<20:
        raise E('full-surface scenario matrix below 20 scenarios')
    print('AIR deterministic contract registry validation: PASS')
    print(f'Registered deterministic checks: {n}')
    print(f'Implemented deterministic checks: {n}/{n}')
    print(f'Executed deterministic checks: {n}/{n}')
    print('Unimplemented: 0')
    print('Unexecuted: 0')

if __name__=='__main__':
    try:
        main(Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve())
    except (E,KeyError) as exc:
        raise SystemExit(f'AIR deterministic contract registry validation FAILED: {exc}')
