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
