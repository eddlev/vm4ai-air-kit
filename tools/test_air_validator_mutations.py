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
RESEAL = ROOT / 'tools' / 'reseal_air_candidate.py'

def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def expect_fail(name: str, proc: subprocess.CompletedProcess[str], expected: str) -> None:
    if proc.returncode == 0:
        raise SystemExit(f'mutation {name} SURVIVED validator')
    if expected not in proc.stdout:
        raise SystemExit(f'mutation {name} failed for wrong reason; expected {expected!r}; output={proc.stdout!r}')
    print(f'{name}: KILLED')

def copy_repo() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    td = tempfile.TemporaryDirectory()
    t = Path(td.name) / 'repo'
    shutil.copytree(ROOT, t, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
    return td, t

def boot_mutation(name: str, mutator, expected: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        shutil.copytree(ROOT / 'prompts', t / 'prompts')
        mutator(t)
        p = run([sys.executable, str(BOOT), str(t)], ROOT)
        expect_fail(name, p, expected)

def full_mutation(name: str, mutator, expected: str, tool: str = 'tools/validate_air_release.py', args: list[str] | None = None) -> None:
    td, t = copy_repo()
    try:
        mutator(t)
        cmd = [sys.executable, tool] + (args or [])
        p = run(cmd, t)
        expect_fail(name, p, expected)
    finally:
        td.cleanup()

def displaced_sentinel(t: Path) -> None:
    p = t / 'prompts' / 'AIR_CONTROL_SURFACE.md'
    p.write_text(p.read_text(encoding='utf-8') + '\nBROKEN_AFTER_SENTINEL\n', encoding='utf-8')

def starter_self_version(t: Path) -> None:
    p = t / 'prompts' / 'AIR_DEFAULT_STARTER_PROFILE.json'
    o = json.loads(p.read_text(encoding='utf-8'))
    o['PROMPT_VERSION'] = '9.9.9'
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

def stale_sibling_sha(t: Path) -> None:
    import hashlib
    profile = t / 'profiles' / 'capability ecology architect' / 'AIR_CAPABILITY_ECOLOGY_ARCHITECT.json'
    o = json.loads(profile.read_text(encoding='utf-8'))
    o['external_dependency_state']['domain_capability_registry']['sha256'] = '0' * 64
    profile.write_text(json.dumps(o, indent=2) + '\n', encoding='utf-8')
    praw = profile.read_bytes()

    manifest = t / 'profiles' / 'capability ecology architect' / 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json'
    mo = json.loads(manifest.read_text(encoding='utf-8'))
    component = next(c for c in mo['components'] if c['filename'] == profile.name)
    component['sha256'] = hashlib.sha256(praw).hexdigest()
    component['size_bytes'] = len(praw)
    component['line_count'] = len(praw.decode('utf-8').splitlines())
    manifest.write_text(json.dumps(mo, indent=2) + '\n', encoding='utf-8')
    mraw = manifest.read_bytes()

    index = t / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json'
    io = json.loads(index.read_text(encoding='utf-8'))
    entry = next(e for e in io['entries'] if e['manifest_filename'] == manifest.name)
    entry['manifest_sha256'] = hashlib.sha256(mraw).hexdigest()
    index.write_text(json.dumps(io, indent=2) + '\n', encoding='utf-8')

def hash_cycle(t: Path) -> None:
    a = t / 'catalog' / 'AIR_RUNTIME_ROUTE_MAP.json'
    b = t / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json'
    ao = json.loads(a.read_text(encoding='utf-8'))
    bo = json.loads(b.read_text(encoding='utf-8'))
    ao['_mutation_cycle_ref'] = {'filename': b.name, 'sha256': '0' * 64}
    bo['_mutation_cycle_ref'] = {'filename': a.name, 'sha256': '0' * 64}
    a.write_text(json.dumps(ao, indent=2) + '\n', encoding='utf-8')
    b.write_text(json.dumps(bo, indent=2) + '\n', encoding='utf-8')

boot_mutation('RB-01-DISPLACED-TERMINAL-SENTINEL', displaced_sentinel, 'terminal sentinel is not the final content line')
boot_mutation('RB-02-STARTER-CANONICAL-VERSION-MISMATCH', starter_self_version, 'Handoff Starter version mismatch')
boot_mutation('RB-03-HANDOFF-STARTER-VERSION-MISMATCH', handoff_starter_version, 'Handoff Starter version mismatch')
full_mutation('DP-ROUTE-INFERENCE-POLICY', route_inference_policy, 'Route Map RT.BOOT: inference_policy mismatch')
full_mutation('RS-01-STALE-SIBLING-SHA', stale_sibling_sha, 'stale sha256 for AIR_DOMAIN_CAPABILITY_REGISTRY.json')
full_mutation('RS-02-IDEMPOTENCE-DETECTS-DRIFT', stale_sibling_sha, 'another reseal pass would change', 'tools/reseal_air_candidate.py', ['--check'])
full_mutation('RS-03-CONTENT-HASH-CYCLE', hash_cycle, 'content-hash dependency cycle', 'tools/reseal_air_candidate.py', ['--check'])
full_mutation('VH-01-SUITE-PROPAGATES-CHILD-FAILURE', displaced_sentinel, 'AIR validation suite FAILED at stage: deterministic_contract_registry', 'tools/validate_air_suite.py', ['--without-mutations'])
print('AIR validator mutation suite: PASS (8/8 mutants killed)')
