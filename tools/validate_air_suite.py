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

def skip_stage(name: str, reason: str) -> None:
    print(f'=== AIR validation stage skipped: {name} ({reason}) ===', flush=True)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--without-mutations', action='store_true')
    parser.add_argument('--candidate', action='store_true')
    args = parser.parse_args()
    py = sys.executable
    run_stage('deterministic_contract_registry', [py, 'tools/validate_air_contract_registry.py'])
    run_stage('r1_foundation_deterministic_spine', [py, 'tools/validate_air_r1_remediation.py'])
    run_stage('r2_formal_object_gate_authorization_failure_ledger', [py, 'tools/validate_air_r2_remediation.py'])
    run_stage('r3_handoff_approval_restoration_closure', [py, 'tools/validate_air_r3_remediation.py'])
    run_stage('handoff_runtime_durability_generation_e2e', [py, 'tools/validate_air_handoff_runtime_contract.py'])
    run_stage('r4_shared_package_schema_normalization', [py, 'tools/validate_air_r4_remediation.py'])
    run_stage('r5_capability_ecology_constructor_chain', [py, 'tools/validate_air_r5_remediation.py'])
    run_stage('r6_package_local_behavioral_contradictions', [py, 'tools/validate_air_r6_remediation.py'])
    run_stage('r7_lifecycle_version_history_reseal', [py, 'tools/validate_air_r7_remediation.py'])
    run_stage('r8_low_risk_presentation_portability', [py, 'tools/validate_air_r8_remediation.py'])
    run_stage('routine_boot', [py, 'tools/validate_air_boot.py'])
    if args.candidate:
        skip_stage('release_contract', 'candidate tree; v0.7.4 exact release validation not applicable')
        skip_stage('v074_release_seal', 'candidate tree; v0.7.4 exact release seal not applicable')
    else:
        run_stage('release_contract', [py, 'tools/validate_air_release.py'])
        run_stage('v074_release_seal', [py, 'tools/validate_air_v074_release_seal.py'])
    run_stage('control_plane_semantic_loopholes', [py, 'tools/validate_air_control_plane.py'])
    run_stage('behavioral_transaction_contracts', [py, 'tools/validate_air_behavioral_contracts.py'])
    run_stage('failure_mode_learning_e2e', [py, 'tools/test_air_failure_mode_learning_e2e.py'])
    if not args.without_mutations:
        run_stage('validator_mutations', [py, 'tools/test_air_validator_mutations.py'] + (['--candidate'] if args.candidate else []))
        run_stage('deterministic_contract_mutations', [py, 'tools/test_air_contract_registry_mutations.py'])
        run_stage('r1_foundation_deterministic_spine_mutations', [py, 'tools/test_air_r1_mutations.py'])
        run_stage('r2_formal_object_gate_authorization_failure_ledger_mutations', [py, 'tools/test_air_r2_mutations.py'])
        run_stage('r3_handoff_approval_restoration_closure_mutations', [py, 'tools/test_air_r3_mutations.py'])
        run_stage('handoff_runtime_durability_generation_e2e_mutations', [py, 'tools/test_air_handoff_runtime_contract_mutations.py'])
        run_stage('r4_shared_package_schema_normalization_mutations', [py, 'tools/test_air_r4_mutations.py', '.', 'tools/validate_air_r4_remediation.py'])
        run_stage('r5_capability_ecology_constructor_chain_mutations', [py, 'tools/test_air_r5_mutations.py', '.', 'tools/validate_air_r5_remediation.py'])
        run_stage('r6_package_local_behavioral_contradictions_mutations', [py, 'tools/test_air_r6_mutations.py', '.', 'tools/validate_air_r6_remediation.py'])
        run_stage('r7_lifecycle_version_history_reseal_mutations', [py, 'tools/test_air_r7_mutations.py', '.', 'tools/validate_air_r7_remediation.py'])
        run_stage('r8_low_risk_presentation_portability_mutations', [py, 'tools/test_air_r8_mutations.py', '.', 'tools/validate_air_r8_remediation.py'])
        if args.candidate:
            skip_stage('v074_release_seal_mutations', 'candidate tree; v0.7.4 exact release-seal mutation baseline not applicable')
        else:
            run_stage('v074_release_seal_mutations', [py, 'tools/test_air_v074_release_seal_mutations.py'])
        run_stage('behavioral_transaction_mutations', [py, 'tools/test_air_behavioral_contract_mutations.py'])
        run_stage('control_plane_semantic_loophole_mutations', [py, 'tools/test_air_control_plane_mutations.py'])
    print('AIR canonical validation suite: PASS')

if __name__ == '__main__':
    main()
