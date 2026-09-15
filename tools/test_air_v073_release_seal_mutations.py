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

    add('V073-N07-COPYWRITING-SET007-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2').__setitem__('foundation_compatibility_identity', 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007')))
    add('V073-N08-COPYWRITING-PENDING-STATIC-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2').__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION')))

    def copywriting_card_revision(d: Path):
        p = d / 'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST.json'; o = load(p)
        hr = next(x for x in o['foundation_compatibility']['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')
        hr['card_revision'] = 18
        dump(p, o)
    add('V073-N09-COPYWRITING-CARD-REVISION-RESTORED', copywriting_card_revision)

    add('V073-N10-INDEX-VERSION-ROLLBACK', idxmut(lambda o: o.__setitem__('INDEX_VERSION', '1.3.8')))

    add('V073-N11-COPYWRITING-BEHAVIORAL-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2').__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION')))

    def evidence_receipt_stale(d: Path):
        p = d / 'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json'; o = load(p); o['behavioral_evidence_receipt']['sha256'] = '0' * 64; dump(p, o)
    add('V073-N12-COPYWRITING-EVIDENCE-RECEIPT-STALE', evidence_receipt_stale)

    def evidence_passcount_stale(d: Path):
        p = d / 'tests/AIR_PUBLIC_SURFACE_COPYWRITING_SET008_BEHAVIORAL_EVIDENCE_V1.json'; o = load(p); o['summary']['pass_count'] = 5; dump(p, o)
    add('V073-N13-COPYWRITING-EVIDENCE-PASSCOUNT-STALE', evidence_passcount_stale)

    add('V073-N14-SFV-SET007-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2').__setitem__('foundation_compatibility_identity', 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007')))
    add('V073-N15-SFV-PENDING-STATIC-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2').__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION')))

    def sfv_executor_promoted(d: Path):
        p = d / 'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_EXECUTOR.json'; o = load(p)
        o['STATUS'] = 'V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING'
        dump(p, o)
    add('V073-N16-SFV-EXECUTOR-PREMATURE-PROMOTION', sfv_executor_promoted)

    def sfv_card_revision(d: Path):
        p = d / 'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json'; o = load(p)
        hr = next(x for x in o['foundation_compatibility']['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')
        hr['card_revision'] = 18
        dump(p, o)
    add('V073-N17-SFV-CARD-REVISION-RESTORED', sfv_card_revision)


    add('V073-N18-SFV-BEHAVIORAL-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_V2').__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION')))

    def sfv_evidence_receipt_stale(d: Path):
        p = d / 'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST_PACKAGE_MANIFEST.json'; o = load(p); o['behavioral_evidence_receipt']['sha256'] = '0' * 64; dump(p, o)
    add('V073-N19-SFV-EVIDENCE-RECEIPT-STALE', sfv_evidence_receipt_stale)

    def sfv_evidence_passcount_stale(d: Path):
        p = d / 'tests/AIR_SPECIFICATION_FIRST_VERIFICATION_SET008_BEHAVIORAL_EVIDENCE_V1.json'; o = load(p); o['summary']['pass_count'] = 5; dump(p, o)
    add('V073-N20-SFV-EVIDENCE-PASSCOUNT-STALE', sfv_evidence_passcount_stale)

    def sfv_component_behavioral_rollback(d: Path):
        p = d / 'profiles/specification first verification specialist/AIR_SPECIFICATION_FIRST_VERIFICATION_SPECIALIST.json'; o = load(p); o['STATUS'] = 'V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING'; dump(p, o)
    add('V073-N21-SFV-COMPONENT-BEHAVIORAL-ROLLBACK', sfv_component_behavioral_rollback)

    add('V073-N22-CEA-SET007-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2').__setitem__('foundation_compatibility_identity', 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007')))
    add('V073-N23-CEA-PENDING-STATIC-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2').__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_STATIC_VALIDATION')))

    def cea_card_revision(d: Path):
        p = d / 'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT.json'; o = load(p)
        hr = next(x for x in o['foundation_compatibility']['required_files'] if x['filename'] == 'AIR_HANDOFF_CARD_TEMPLATE.json')
        hr['card_revision'] = 18
        dump(p, o)
    add('V073-N24-CEA-CARD-REVISION-RESTORED', cea_card_revision)

    def cea_route_map_rollback(d: Path):
        p = d / 'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_METHOD_PACK.json'; o = load(p)
        o['foundation_compatibility']['route_map_discovery_input']['version'] = '1.2.1'
        dump(p, o)
    add('V073-N25-CEA-ROUTE-MAP-ROLLBACK', cea_route_map_rollback)

    add('V073-N26-CEA-BEHAVIORAL-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_V2').__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION')))

    def cea_evidence_receipt_stale(d: Path):
        p=d/'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json';o=load(p);o['behavioral_evidence_receipt']['sha256']='0'*64;dump(p,o)
    add('V073-N27-CEA-EVIDENCE-RECEIPT-STALE', cea_evidence_receipt_stale)

    def cea_evidence_passcount_stale(d: Path):
        p=d/'tests/AIR_CAPABILITY_ECOLOGY_ARCHITECT_SET008_BEHAVIORAL_EVIDENCE_V1.json';o=load(p);o['summary']['pass_count']=5;dump(p,o)
    add('V073-N28-CEA-EVIDENCE-PASSCOUNT-STALE', cea_evidence_passcount_stale)

    def cea_component_behavioral_rollback(d: Path):
        p=d/'profiles/capability ecology architect/AIR_CAPABILITY_ECOLOGY_ARCHITECT.json';o=load(p);o['STATUS']='V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING';dump(p,o)
    add('V073-N29-CEA-COMPONENT-BEHAVIORAL-ROLLBACK', cea_component_behavioral_rollback)
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
