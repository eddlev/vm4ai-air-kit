from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path('.').resolve()
VAL = ROOT / 'tools' / 'validate_air_v074_release_seal.py'
PYTHON = sys.executable


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj) -> None:
    path.write_bytes((json.dumps(obj, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))


def run(root: Path) -> int:
    return subprocess.run([PYTHON, str(VAL), str(root)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode


def main() -> None:
    if run(ROOT) != 0:
        raise SystemExit('v0.7.4 release-seal mutation baseline failed')

    cases = []
    def add(name, fn): cases.append((name, fn))

    def version_rollback(d: Path):
        (d / 'VERSION').write_bytes(b'0.7.3\n')
    add('V074-N01-VERSION-ROLLBACK', version_rollback)

    def core_drift(d: Path):
        p=d/'prompts/AIR_CORE_RUNTIME.md'; p.write_bytes(p.read_bytes()+b'\nV074_MUTANT\n')
    add('V074-N02-CORE-HASH-DRIFT', core_drift)

    def route_drift(d: Path):
        p=d/'catalog/AIR_RUNTIME_ROUTE_MAP.json'; o=load(p); o['MAP_VERSION']='1.2.1'; dump(p,o)
    add('V074-N03-ROUTE-HASH-DRIFT', route_drift)

    def index_candidate_status(d: Path):
        p=d/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'; o=load(p); o['status']='AIR_2_6_3_OBJECT_CONTRACT_SET_008_FIVE_PACKAGE_INDEX_V074_RELEASE_CANDIDATE_REPLAYABLE_BEHAVIORAL_VALIDATED'; dump(p,o)
    add('V074-N04-INDEX-CANDIDATE-STATUS', index_candidate_status)

    def index_candidate_completeness(d: Path):
        p=d/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'; o=load(p); o['catalog_scope']['catalog_completeness_claim']='COMPLETE_FOR_AIR_2_6_3_OBJECT_CONTRACT_SET_008_V074_RELEASE_CANDIDATE_SPECIALIST_CATALOG'; dump(p,o)
    add('V074-N05-INDEX-CANDIDATE-COMPLETENESS', index_candidate_completeness)

    def readme_candidate(d: Path):
        p=d/'README.md'; s=p.read_text(encoding='utf-8').replace('## Current release — AIR Kit v0.7.4','## Current release candidate — AIR Kit v0.7.4',1); p.write_bytes(s.encode('utf-8'))
    add('V074-N06-README-CANDIDATE-HEADING', readme_candidate)

    def handoff_rev19(d: Path):
        p=d/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'; o=load(p); o['AIR_HANDOFF_CARD']['template_revision']=19; dump(p,o)
    add('V074-N07-HANDOFF-REV19', handoff_rev19)

    def cw_candidate_registration(d: Path):
        p=d/'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json'; o=load(p); o['package_validation_state']['release_catalog_registration']='INCLUDED_IN_SET_008_V074_RELEASE_CANDIDATE_CATALOG'; dump(p,o)
    add('V074-N08-COPYWRITING-CANDIDATE-REGISTRATION', cw_candidate_registration)

    def sfv_candidate_registration(d: Path):
        p=d/'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json'; o=load(p); o['package_validation_state']['release_catalog_registration']='INCLUDED_IN_SET_008_V074_RELEASE_CANDIDATE_CATALOG_WITH_EXECUTOR_DRAFT_UNAVAILABLE'; dump(p,o)
    add('V074-N09-SFV-CANDIDATE-REGISTRATION', sfv_candidate_registration)

    def grounding_candidate_registration(d: Path):
        p=d/'profiles/grounding specialist/AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json'; o=load(p); o['package_validation_state']['release_catalog_registration']='INCLUDED_IN_SET_008_V074_RELEASE_CANDIDATE_CATALOG_WITH_EXECUTOR_DRAFT_UNAVAILABLE'; dump(p,o)
    add('V074-N10-GROUNDING-CANDIDATE-REGISTRATION', grounding_candidate_registration)

    def v073_validator_drift(d: Path):
        p=d/'tools/validate_air_v073_release_seal.py'; p.write_bytes(p.read_bytes()+b'\n# historical mutant\n')
    add('V074-N11-HISTORICAL-V073-VALIDATOR-DRIFT', v073_validator_drift)

    def inline_handoff_enabled(d: Path):
        p=d/'catalog/AIR_RUNTIME_ROUTE_MAP.json'; o=load(p); r=next(x for x in o['routes'] if x['route_id']=='RT.HANDOFF_CREATE'); r['handoff_file_delivery']['inline_payload']='ALLOWED'; dump(p,o)
    add('V074-N12-HANDOFF-INLINE-PAYLOAD', inline_handoff_enabled)

    killed = 0
    with tempfile.TemporaryDirectory(prefix='air-v074-release-mutations-') as td:
        base = Path(td)
        for name, fn in cases:
            dst = base / name
            shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
            fn(dst)
            if run(dst) == 0:
                raise SystemExit(f'mutation {name} SURVIVED v0.7.4 release seal')
            print(f'{name}: KILLED')
            killed += 1
    print(f'AIR v0.7.4 release-seal mutation suite: PASS ({killed}/{len(cases)} mutants killed)')


if __name__ == '__main__':
    main()
