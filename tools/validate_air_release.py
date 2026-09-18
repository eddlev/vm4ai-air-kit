from __future__ import annotations

import json
from pathlib import Path

from validate_air_durable_provenance_provider import run_validation as validate_provider
from validate_air_full_surface_integrity import validate as validate_full_surface
from validate_air_v074_release_seal import main as validate_v074

ROOT = Path('.').resolve()


def main() -> None:
    manifest = json.loads((ROOT / 'tests/air_full_surface_coverage_manifest.json').read_text(encoding='utf-8'))
    if manifest.get('release_gate_state') == 'CANDIDATE_ONLY_NOT_RELEASE':
        raise SystemExit('AIR release validation FAILED: full-surface manifest still candidate-only')
    report = validate_full_surface(
        ROOT,
        ROOT / 'tests/air_full_surface_coverage_manifest.json',
        ROOT / 'tests/air_full_surface_scenario_matrix.json',
    )
    if report.get('decision') != 'PASS':
        raise SystemExit('AIR release validation FAILED: full-surface integrity')
    provider = validate_provider()
    if provider.get('decision') != 'PASS':
        raise SystemExit('AIR release validation FAILED: durable provenance provider validation')
    validate_v074()
    print('AIR release validation: PASS (full-surface + provider + v0.7.4 seal)')


if __name__ == '__main__':
    main()
