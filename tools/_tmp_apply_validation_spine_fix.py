from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('.')

RESEAL = r'''from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path('.')
HASH_FIELDS = {'sha256', 'observed_sha256'}
META_FIELDS = HASH_FIELDS | {'size_bytes', 'line_count'}

class ResealError(Exception):
    pass

def reject_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in out:
            raise ResealError(f'duplicate JSON key: {k}')
        out[k] = v
    return out

def load_json_bytes(raw: bytes, path: Path) -> Any:
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=reject_dupes)
    except Exception as exc:
        raise ResealError(f'{path}: strict JSON parse failed: {exc}') from exc

def operational_files(root: Path) -> list[Path]:
    return sorted([
        *root.glob('prompts/*.md'),
        *root.glob('prompts/*.json'),
        *root.glob('catalog/*.json'),
        *root.glob('profiles/**/*.json'),
    ])

def walk_dicts(obj: Any):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk_dicts(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk_dicts(value)

def ref_target(node: dict[str, Any], names: set[str]) -> tuple[str | None, set[str]]:
    ref = node.get('filename') or node.get('canonical_filename')
    fields = set(node) & META_FIELDS
    if isinstance(ref, str) and ref in names and fields:
        return ref, fields
    manifest = node.get('manifest_filename')
    if isinstance(manifest, str) and manifest in names and 'manifest_sha256' in node:
        return manifest, {'manifest_sha256'}
    return None, set()

def metadata(raw: bytes) -> dict[str, Any]:
    text = raw.decode('utf-8')
    return {
        'sha256': hashlib.sha256(raw).hexdigest(),
        'size_bytes': len(raw),
        'line_count': len(text.splitlines()),
    }

def build_graph(files: list[Path], raw_by_path: dict[Path, bytes]) -> tuple[dict[Path, set[Path]], dict[str, Path]]:
    by_name: dict[str, Path] = {}
    for p in files:
        if p.name in by_name:
            raise ResealError(f'duplicate operational basename: {p.name}')
        by_name[p.name] = p
    names = set(by_name)
    graph: dict[Path, set[Path]] = {p: set() for p in files if p.suffix == '.json'}
    for owner in graph:
        obj = load_json_bytes(raw_by_path[owner], owner)
        for node in walk_dicts(obj):
            target_name, _ = ref_target(node, names)
            if target_name and target_name != owner.name:
                target = by_name[target_name]
                # Only JSON owners are resealed; markdown targets are terminal leaves.
                if target.suffix == '.json':
                    graph[owner].add(target)
    return graph, by_name

def topo(graph: dict[Path, set[Path]]) -> list[Path]:
    state: dict[Path, int] = {}
    out: list[Path] = []
    stack: list[Path] = []
    def visit(node: Path) -> None:
        mark = state.get(node, 0)
        if mark == 2:
            return
        if mark == 1:
            try:
                i = stack.index(node)
            except ValueError:
                i = 0
            cycle = stack[i:] + [node]
            raise ResealError('content-hash dependency cycle: ' + ' -> '.join(str(p) for p in cycle))
        state[node] = 1
        stack.append(node)
        for dep in sorted(graph[node], key=str):
            visit(dep)
        stack.pop()
        state[node] = 2
        out.append(node)
    for node in sorted(graph, key=str):
        visit(node)
    return out

def virtual_reseal(root: Path) -> tuple[dict[Path, bytes], list[Path], int]:
    files = operational_files(root)
    actual = {p: p.read_bytes() for p in files}
    virtual = dict(actual)
    graph, by_name = build_graph(files, actual)
    names = set(by_name)
    order = topo(graph)
    updates = 0
    for owner in order:
        obj = load_json_bytes(virtual[owner], owner)
        changed = False
        for node in walk_dicts(obj):
            target_name, fields = ref_target(node, names)
            if not target_name or target_name == owner.name:
                continue
            m = metadata(virtual[by_name[target_name]])
            for field in fields:
                if field == 'manifest_sha256':
                    new = m['sha256']
                else:
                    new = m[field]
                if node.get(field) != new:
                    node[field] = new
                    updates += 1
                    changed = True
        if changed:
            virtual[owner] = (json.dumps(obj, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    changed_paths = [p for p in files if virtual[p] != actual[p]]
    return virtual, changed_paths, updates

def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    virtual, changed, updates = virtual_reseal(ROOT)
    if args.check:
        if changed:
            raise SystemExit('AIR candidate reseal check FAILED: another reseal pass would change: ' + ', '.join(str(p) for p in changed[:20]))
        print('AIR candidate reseal idempotence: PASS (0 changes)')
        return
    for path in changed:
        path.write_bytes(virtual[path])
    print(f'AIR dependency-graph reseal applied: {len(changed)} files, {updates} metadata fields updated')
    # A successful apply must converge immediately.
    _, second_changed, _ = virtual_reseal(ROOT)
    if second_changed:
        raise SystemExit('AIR candidate reseal FAILED to converge: ' + ', '.join(str(p) for p in second_changed[:20]))
    print('AIR dependency-graph reseal convergence: PASS')

if __name__ == '__main__':
    try:
        main()
    except ResealError as exc:
        raise SystemExit(f'AIR candidate reseal FAILED: {exc}')
'''

SUITE = r'''from __future__ import annotations

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
    run_stage('routine_boot', [py, 'tools/validate_air_boot.py'])
    run_stage('release_contract', [py, 'tools/validate_air_release.py'])
    run_stage('reseal_idempotence', [py, 'tools/reseal_air_candidate.py', '--check'])
    if not args.without_mutations:
        run_stage('validator_mutations', [py, 'tools/test_air_validator_mutations.py'])
    print('AIR canonical validation suite: PASS')

if __name__ == '__main__':
    main()
'''

MUTATIONS = r'''from __future__ import annotations

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

def stale_sibling_sha(t: Path) -> None:
    p = t / 'profiles' / 'capability ecology architect' / 'AIR_CAPABILITY_ECOLOGY_ARCHITECT.json'
    o = json.loads(p.read_text(encoding='utf-8'))
    o['external_dependency_state']['domain_capability_registry']['sha256'] = '0' * 64
    p.write_text(json.dumps(o, indent=2) + '\n', encoding='utf-8')

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
boot_mutation('RB-02-STARTER-SELF-VERSION-MISMATCH', starter_self_version, 'Starter PROMPT_VERSION != validation_contract.required_version')
boot_mutation('RB-03-HANDOFF-STARTER-VERSION-MISMATCH', handoff_starter_version, 'Handoff Starter version mismatch')
full_mutation('DP-ROUTE-INFERENCE-POLICY', route_inference_policy, 'Route Map RT.BOOT: inference_policy mismatch')
full_mutation('RS-01-STALE-SIBLING-SHA', stale_sibling_sha, 'stale sha256 for AIR_DOMAIN_CAPABILITY_REGISTRY.json')
full_mutation('RS-02-IDEMPOTENCE-DETECTS-DRIFT', stale_sibling_sha, 'another reseal pass would change', 'tools/reseal_air_candidate.py', ['--check'])
full_mutation('RS-03-CONTENT-HASH-CYCLE', hash_cycle, 'content-hash dependency cycle', 'tools/reseal_air_candidate.py', ['--check'])
full_mutation('VH-01-SUITE-PROPAGATES-CHILD-FAILURE', displaced_sentinel, 'AIR validation suite FAILED at stage: routine_boot', 'tools/validate_air_suite.py', ['--without-mutations'])
print('AIR validator mutation suite: PASS (8/8 mutants killed)')
'''

(ROOT / 'tools' / 'reseal_air_candidate.py').write_text(RESEAL, encoding='utf-8')
(ROOT / 'tools' / 'validate_air_suite.py').write_text(SUITE, encoding='utf-8')
(ROOT / 'tools' / 'test_air_validator_mutations.py').write_text(MUTATIONS, encoding='utf-8')

# Extend deterministic release validator so the validation spine itself is required.
vp = ROOT / 'tools' / 'validate_air_release.py'
text = vp.read_text(encoding='utf-8')
old = "    require((ROOT / 'tools' / 'validate_air_release.py').is_file(), 'missing permanent validator')\n    require((ROOT / 'tests' / 'air_contract_fixtures.json').is_file(), 'missing regression fixtures')"
new = "    require((ROOT / 'tools' / 'validate_air_release.py').is_file(), 'missing permanent validator')\n    require((ROOT / 'tools' / 'validate_air_boot.py').is_file(), 'missing independent boot validator')\n    require((ROOT / 'tools' / 'validate_air_suite.py').is_file(), 'missing canonical validation suite runner')\n    require((ROOT / 'tools' / 'reseal_air_candidate.py').is_file(), 'missing dependency-graph resealer')\n    require((ROOT / 'tools' / 'test_air_validator_mutations.py').is_file(), 'missing validator mutation suite')\n    require((ROOT / 'tests' / 'air_contract_fixtures.json').is_file(), 'missing regression fixtures')"
if old not in text:
    raise SystemExit('release validator tool requirement anchor not found')
text = text.replace(old, new, 1)
old2 = "    require(len(fixtures.get('semantic_reseal_negative_cases', [])) >= 3, 'insufficient semantic reseal negative fixtures')"
new2 = old2 + "\n    require(len(fixtures.get('validation_spine_negative_cases', [])) >= 4, 'insufficient validation spine negative fixtures')"
if old2 not in text:
    raise SystemExit('release validator fixture anchor not found')
text = text.replace(old2, new2, 1)
old3 = "    print('Behavioral replay fixtures: PRESENT (not evidence that model evaluation has run)')"
new3 = old3 + "\n    print('Validation spine regression fixtures: PRESENT')"
text = text.replace(old3, new3, 1)
vp.write_text(text, encoding='utf-8')

# Add permanent regression definitions for the newly discovered failure classes.
fp = ROOT / 'tests' / 'air_contract_fixtures.json'
fixtures = json.loads(fp.read_text(encoding='utf-8'))
fixtures['validation_spine_negative_cases'] = [
    {
        'id': 'VS-01-CHILD-VALIDATOR-FAILURE-PROPAGATION',
        'invalid_if': 'a child validator exits non-zero but the canonical suite or CI reports PASS'
    },
    {
        'id': 'VS-02-STALE-LIVE-SIBLING-HASH',
        'invalid_if': 'a live operational component carries a hash/size/line receipt that differs from the referenced current component bytes'
    },
    {
        'id': 'VS-03-RESEAL-NON-IDEMPOTENCE',
        'invalid_if': 'a second dependency-graph reseal pass would change any candidate byte or live receipt'
    },
    {
        'id': 'VS-04-CONTENT-HASH-DEPENDENCY-CYCLE',
        'invalid_if': 'two or more operational files form a cycle of exact content-hash dependencies that cannot be topologically resealed'
    }
]
fp.write_text(json.dumps(fixtures, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

print('validation spine implementation written; dependency reseal must run next')
