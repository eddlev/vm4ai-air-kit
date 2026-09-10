from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path('.').resolve()
VALIDATOR = ROOT / 'tools' / 'validate_air_v071_release_seal.py'


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def run(root: Path) -> int:
    return subprocess.run([sys.executable, str(VALIDATOR), str(root)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode


def mutate(root: Path, fn) -> None:
    path = root / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json'
    obj = load(path)
    fn(obj)
    dump(path, obj)


CASES = [
    ('V071-SEAL-N01-STATUS-DEMOTED', lambda o: o.__setitem__('status', 'AIR_2_6_0_OBJECT_CONTRACT_SET_005_FIVE_PACKAGE_INDEX_V071_RELEASE_CANDIDATE')),
    ('V071-SEAL-N02-ENTRY-DEMOTED', lambda o: o['entries'][0].__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION')),
    ('V071-SEAL-N03-MAINTAINER-ACCEPTANCE-REMOVED', lambda o: o['validation_state'].__setitem__('decision', 'STATIC_VALIDATED_CANDIDATE_PENDING_REPLAYABLE_BEHAVIORAL_REVALIDATION')),
    ('V071-SEAL-N04-UNSUPPORTED-BEHAVIORAL-PASS', lambda o: o['validation_state'].__setitem__('behavioral_revalidation', 'BEHAVIORAL_REVALIDATION_PASS')),
    ('V071-SEAL-N05-CANDIDATE-STATES-FALSELY-SEALED', lambda o: o['candidate_lifecycle_contract'].__setitem__('candidate_states_are_release_sealed', True)),
]


if run(ROOT) != 0:
    raise SystemExit('v0.7.1 release-seal mutation baseline failed')
print('V071-RELEASE-SEAL-MUTATION-BASELINE: PASS')

with tempfile.TemporaryDirectory(prefix='air-v071-release-seal-') as td:
    dst = Path(td) / 'repo'
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
    base = (dst / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json').read_bytes()
    for name, fn in CASES:
        p = dst / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json'
        p.write_bytes(base)
        mutate(dst, fn)
        if run(dst) == 0:
            raise SystemExit(f'MUTATION SURVIVED: {name}')
        print(f'{name}: KILLED')

print(f'AIR v0.7.1 release-seal mutation suite: PASS ({len(CASES)}/{len(CASES)} mutants killed)')
