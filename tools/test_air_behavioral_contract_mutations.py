from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path('.').resolve()


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def run_validator(root: Path) -> int:
    return subprocess.run([sys.executable, 'tools/validate_air_behavioral_contracts.py'], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode


def mutate_remove_core_marker(root: Path):
    p = root / 'prompts/AIR_CORE_RUNTIME.md'
    t = p.read_text(encoding='utf-8').replace('Patch marker: AIR_MATERIAL_ACTION_TRANSACTION_V1', 'Patch marker: REMOVED_MATERIAL_ACTION_TRANSACTION', 1)
    p.write_text(t, encoding='utf-8')


def mutate_orbit_bundle(root: Path):
    p = root / 'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; x = load(p)
    x['compiler_contract']['transition_emission_transaction']['orbit_transition_atomic_bundle'] = ['AIR_PROJECT_EXECUTION_MAP', 'AIR_ARTIFACT']; dump(p, x)


def mutate_action_sequence(root: Path):
    p = root / 'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; x = load(p)
    s = x['compiler_contract']['material_action_transaction']['ordered_pre_and_post_effect_states']; s.remove('AIR_ACTION_AUTHORIZATION_EMITTED'); dump(p, x)


def mutate_post_effect_profile(root: Path):
    p = root / 'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; x = load(p)
    x['compiler_contract']['material_action_transaction']['post_effect_alignment_profile'] = 'STATE_TRANSITION'; dump(p, x)


def mutate_receipt_match(root: Path):
    p = root / 'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; x = load(p)
    x['compiler_contract']['material_action_transaction']['authorization_receipt_exact_match_required'] = False; dump(p, x)


def mutate_handoff_provenance(root: Path):
    p = root / 'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; x = load(p)
    x['AIR_HANDOFF_CARD']['action_governance_state']['provenance_policy']['unsurfaced_authorization_reconstruction'] = 'ALLOWED'; dump(p, x)


def mutate_cw2(root: Path):
    p = root / 'tests/air_contract_fixtures.json'; x = load(p)
    for c in x['copywriting_behavior_cases']:
        if c['id'] == 'CW-BEH-02-MISSING-DOMAIN-TRUTH': c['acceptable_runtime_outcomes'] = ['EVIDENCE_REQUIRED only']
    dump(p, x)


def mutate_projection_order(root: Path):
    p = root / 'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; x = load(p)
    x['compiler_contract']['deterministic_projection_order_integrity']['commuting_operations_may_reorder'] = True; dump(p, x)


def mutate_route_bundle(root: Path):
    p = root / 'catalog/AIR_RUNTIME_ROUTE_MAP.json'; x = load(p)
    for r in x['routes']:
        if r['route_id'] == 'RT.TASK_SWITCH': r['transition_emission_bundle']['members'] = ['AIR_PROJECT_EXECUTION_MAP', 'AIR_ARTIFACT']
    dump(p, x)


MUTATIONS = [
    ('core_marker', mutate_remove_core_marker),
    ('orbit_bundle', mutate_orbit_bundle),
    ('action_sequence', mutate_action_sequence),
    ('post_effect_profile', mutate_post_effect_profile),
    ('receipt_match', mutate_receipt_match),
    ('handoff_provenance', mutate_handoff_provenance),
    ('cw2_safe_remainder', mutate_cw2),
    ('projection_order', mutate_projection_order),
    ('route_bundle', mutate_route_bundle),
]


def main() -> None:
    killed = 0
    for name, fn in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix='air-behavioral-mutation-') as td:
            dst = Path(td) / 'repo'
            shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns('.git', '__pycache__'))
            fn(dst)
            if run_validator(dst) == 0:
                print(f'MUTATION SURVIVED: {name}', file=sys.stderr)
                raise SystemExit(1)
            killed += 1
            print(f'MUTATION KILLED: {name}')
    print(f'AIR behavioral transaction mutation suite: PASS ({killed}/{len(MUTATIONS)})')

if __name__ == '__main__':
    main()
