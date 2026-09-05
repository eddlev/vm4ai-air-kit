from __future__ import annotations

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
                if field in {'manifest_sha256', 'observed_sha256'}:
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
