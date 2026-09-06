from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path('.').resolve()

def run_stage(name: str, command: list[str]) -> None:
    print(f'=== AIR validation stage: {name} ===', flush=True)
    proc = subprocess.run(command, cwd=ROOT)
    if proc.returncode != 0:
        raise SystemExit(f'AIR validation suite FAILED at stage: {name} (exit {proc.returncode})')

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--without-mutations', action='store_true')
    args = parser.parse_args()
    py = sys.executable
    run_stage('deterministic_contract_registry', [py, 'tools/validate_air_contract_registry.py'])
    run_stage('routine_boot', [py, 'tools/validate_air_boot.py'])
    run_stage('release_contract', [py, 'tools/validate_air_release.py'])
    run_stage('behavioral_transaction_contracts', [py, 'tools/validate_air_behavioral_contracts.py'])
    run_stage('reseal_idempotence', [py, 'tools/reseal_air_candidate.py', '--check'])
    if not args.without_mutations:
        run_stage('validator_mutations', [py, 'tools/test_air_validator_mutations.py'])
        run_stage('deterministic_contract_mutations', [py, 'tools/test_air_contract_registry_mutations.py'])
        run_stage('behavioral_transaction_mutations', [py, 'tools/test_air_behavioral_contract_mutations.py'])
    print('AIR canonical validation suite: PASS')

if __name__ == '__main__':
    main()
