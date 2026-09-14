from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path('.').resolve()
VAL = ROOT / 'tools' / 'validate_air_v073_release_seal.py'
PYTHON = sys.executable


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def run(root: Path) -> int:
    return subprocess.run([PYTHON, str(VAL), str(root)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode


def main() -> None:
    if run(ROOT) != 0:
        raise SystemExit('v0.7.3 release-seal mutation baseline failed')
    cases = []

    def add(name, fn):
        cases.append((name, fn))

    def idxmut(fn):
        def m(d: Path):
            p = d / 'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'
            o = load(p); fn(o); dump(p, o)
        return m

    add('V073-N01-AGGREGATE-LIFECYCLE-OVERCLAIM', idxmut(lambda o: o['candidate_lifecycle_contract'].__setitem__('current_candidate_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION')))
    add('V073-N02-ENTRY-PREMATURE-RELEASE', idxmut(lambda o: o['entries'][0].__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY')))

    def route_version(d: Path):
        p = d / 'catalog/AIR_RUNTIME_ROUTE_MAP.json'; o = load(p); o['MAP_VERSION'] = '1.2.1'; dump(p, o)
    add('V073-N03-ROUTE-MAP-VERSION-SPLIT', route_version)

    def handoff_legacy_field(d: Path):
        p = d / 'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; o = load(p); o['AIR_HANDOFF_CARD']['card_revision'] = 19; dump(p, o)
    add('V073-N04-CURRENT-CARD-REVISION-LEAK', handoff_legacy_field)

    def migration_user_counter(d: Path):
        p = d / 'tools/migrate_air_handoff.py'; s = p.read_text(encoding='utf-8')
        anchor = 'source_user_revision=user_revision,'
        if anchor not in s:
            raise RuntimeError('migration mutant anchor missing')
        p.write_text(s.replace(anchor, 'source_user_revision=None,', 1), encoding='utf-8')
    add('V073-N05-LEGACY-USER-REVISION-DROPPED', migration_user_counter)

    def registry_count(d: Path):
        p = d / 'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o = load(p)
        o['validation_contract']['deterministic_contract_registry']['checks'].pop()
        o['validation_contract']['deterministic_contract_registry']['coverage_contract']['declared_check_count'] = 89
        o['validation_contract']['deterministic_contract_registry']['coverage_contract']['implemented_check_count_required'] = 89
        o['validation_contract']['deterministic_contract_registry']['coverage_contract']['executed_check_count_required'] = 89
        dump(p, o)
    add('V073-N06-REGISTRY-COVERAGE-DROPPED', registry_count)

    killed = 0
    for name, fn in cases:
        with tempfile.TemporaryDirectory(prefix='air-v073-seal-mut-') as td:
            d = Path(td) / 'repo'
            shutil.copytree(ROOT, d, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
            fn(d)
            if run(d) == 0:
                raise SystemExit('MUTATION SURVIVED: ' + name)
            killed += 1
            print(name + ': KILLED')
    print(f'AIR v0.7.3 release-seal mutation suite: PASS ({killed}/{len(cases)} targeted mutants killed)')


if __name__ == '__main__':
    main()
