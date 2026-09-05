from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path('.').resolve()
BOOT = ROOT / 'tools' / 'validate_air_boot.py'
RELEASE = ROOT / 'tools' / 'validate_air_release.py'

def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def expect_fail(name: str, proc: subprocess.CompletedProcess[str], expected: str) -> None:
    if proc.returncode == 0:
        raise SystemExit(f'mutation {name} SURVIVED validator')
    if expected not in proc.stdout:
        raise SystemExit(f'mutation {name} failed for wrong reason; expected {expected!r}; output={proc.stdout!r}')
    print(f'{name}: KILLED')

def boot_mutation(name: str, mutator, expected: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        shutil.copytree(ROOT / 'prompts', t / 'prompts')
        mutator(t)
        p = run([sys.executable, str(BOOT), str(t)], ROOT)
        expect_fail(name, p, expected)

def full_mutation(name: str, mutator, expected: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        t = Path(td) / 'repo'
        shutil.copytree(ROOT, t, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
        mutator(t)
        p = run([sys.executable, 'tools/validate_air_release.py'], t)
        expect_fail(name, p, expected)

def displaced_sentinel(t: Path) -> None:
    p = t / 'prompts' / 'AIR_CONTROL_SURFACE.md'
    p.write_text(p.read_text(encoding='utf-8') + '\nBROKEN_AFTER_SENTINEL\n', encoding='utf-8')

def starter_self_version(t: Path) -> None:
    p = t / 'prompts' / 'AIR_DEFAULT_STARTER_PROFILE.json'
    o = json.loads(p.read_text(encoding='utf-8'))
    o['validation_contract']['required_version'] = '9.9.9'
    p.write_text(json.dumps(o, indent=2) + '\n', encoding='utf-8')

def handoff_starter_version(t: Path) -> None:
    p = t / 'prompts' / 'AIR_HANDOFF_CARD_TEMPLATE.json'
    o = json.loads(p.read_text(encoding='utf-8'))
    o['AIR_HANDOFF_CARD']['profile_stack']['starter_profile']['PROMPT_VERSION'] = '9.9.9'
    p.write_text(json.dumps(o, indent=2) + '\n', encoding='utf-8')

def route_inference_policy(t: Path) -> None:
    p = t / 'catalog' / 'AIR_RUNTIME_ROUTE_MAP.json'
    o = json.loads(p.read_text(encoding='utf-8'))
    target = next(r for r in o['routes'] if r['route_id'] == 'RT.BOOT')
    target['inference_policy'] = 'ALLOWED'
    p.write_text(json.dumps(o, indent=2) + '\n', encoding='utf-8')

boot_mutation('RB-01-DISPLACED-TERMINAL-SENTINEL', displaced_sentinel, 'terminal sentinel is not the final content line')
boot_mutation('RB-02-STARTER-SELF-VERSION-MISMATCH', starter_self_version, 'Starter PROMPT_VERSION != validation_contract.required_version')
boot_mutation('RB-03-HANDOFF-STARTER-VERSION-MISMATCH', handoff_starter_version, 'Handoff Starter version mismatch')
full_mutation('DP-ROUTE-INFERENCE-POLICY', route_inference_policy, 'Route Map RT.BOOT: inference_policy mismatch')
print('AIR validator mutation suite: PASS (4/4 mutants killed)')
