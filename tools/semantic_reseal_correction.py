from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path('.')
PROFILES = ROOT / 'profiles'
HANDOFF = 'AIR_HANDOFF_CARD_TEMPLATE.json'
EXPECTED_CARD_REVISION = 16
PASS_TOKEN = 'BEHAVIORAL_REVALIDATION_PASS'
PENDING_TOKEN = 'BEHAVIORAL_REVALIDATION_PENDING'


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


changed_state_paths: list[str] = []
changed_card_revision_paths: list[str] = []


def fix_semantic_state(node: Any, loc: tuple[str, ...], owner: Path) -> bool:
    changed = False
    if isinstance(node, dict):
        ref = node.get('filename') or node.get('canonical_filename')
        if ref == HANDOFF and 'card_revision' in node and node['card_revision'] != EXPECTED_CARD_REVISION:
            node['card_revision'] = EXPECTED_CARD_REVISION
            changed_card_revision_paths.append(f'{owner}:{".".join(loc + ("card_revision",))}')
            changed = True
        for key, value in list(node.items()):
            if isinstance(value, str) and 'SET_005' in value and PASS_TOKEN in value:
                node[key] = value.replace(PASS_TOKEN, PENDING_TOKEN)
                changed_state_paths.append(f'{owner}:{".".join(loc + (key,))}')
                changed = True
            elif isinstance(value, (dict, list)):
                changed |= fix_semantic_state(value, loc + (key,), owner)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            if isinstance(value, str) and 'SET_005' in value and PASS_TOKEN in value:
                node[i] = value.replace(PASS_TOKEN, PENDING_TOKEN)
                changed_state_paths.append(f'{owner}:{".".join(loc + (str(i),))}')
                changed = True
            elif isinstance(value, (dict, list)):
                changed |= fix_semantic_state(value, loc + (str(i),), owner)
    return changed


profile_files = sorted(PROFILES.rglob('*.json'))
for path in profile_files:
    obj = load(path)
    if fix_semantic_state(obj, (), path):
        dump(path, obj)

validator = ROOT / 'tools' / 'validate_air_release.py'
text = validator.read_text(encoding='utf-8')
anchor = "EXPECTED_PACKAGE_VERSION = '2.5.0'\n"
insert = anchor + "EXPECTED_HANDOFF_CARD_REVISION = 16\n"
if 'EXPECTED_HANDOFF_CARD_REVISION' not in text:
    if anchor not in text:
        raise SystemExit('validator anchor missing: EXPECTED_PACKAGE_VERSION')
    text = text.replace(anchor, insert, 1)

text = text.replace(
    "require(handoff['card_revision'] == 16, 'Handoff card revision mismatch')",
    "require(handoff['card_revision'] == EXPECTED_HANDOFF_CARD_REVISION, 'Handoff card revision mismatch')",
)

ref_anchor = "        if ref in FOUNDATION_VERSION and 'version' in node:\n            require(node['version'] == FOUNDATION_VERSION[ref], f'{owner}: stale version for {ref}')\n"
ref_insert = ref_anchor + "        if ref == 'AIR_HANDOFF_CARD_TEMPLATE.json' and 'card_revision' in node:\n            require(node['card_revision'] == EXPECTED_HANDOFF_CARD_REVISION, f'{owner}: stale card_revision for {ref} at {\".\".join(path_tuple)}')\n"
if 'stale card_revision for' not in text:
    if ref_anchor not in text:
        raise SystemExit('validator anchor missing: reference metadata check')
    text = text.replace(ref_anchor, ref_insert, 1)

behavioral_anchor = "    index = parsed[ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json']\n"
behavioral_block = """    behavioral_manifest_path = ROOT / 'tests' / 'behavioral_revalidation_manifest.json'
    behavioral_evidence_pass = False
    if behavioral_manifest_path.is_file():
        behavioral_manifest = load_json(behavioral_manifest_path)
        behavioral_evidence_pass = (
            behavioral_manifest.get('foundation_identity') == EXPECTED_FOUNDATION_ID
            and behavioral_manifest.get('result') == 'PASS'
        )

    behavioral_pass_claims: list[str] = []
    def collect_behavioral_pass(node: Any, loc: tuple[str, ...], owner: Path) -> None:
        if isinstance(node, str) and 'SET_005' in node and 'BEHAVIORAL_REVALIDATION_PASS' in node:
            behavioral_pass_claims.append(f'{owner}:{".".join(loc)}')
    for p in sorted(ROOT.glob('profiles/**/*.json')):
        walk(parsed[p], lambda node, loc, owner=p: collect_behavioral_pass(node, loc, owner))
    if behavioral_pass_claims:
        require(
            behavioral_evidence_pass,
            'unsupported SET_005 behavioral PASS claims without passing replay manifest: '
            + ', '.join(behavioral_pass_claims[:12]),
        )

    for p in sorted(ROOT.glob('profiles/**/*PACKAGE_MANIFEST.json')):
        obj = parsed[p]
        top_status = str(obj.get('status') or obj.get('STATUS') or '')
        if 'BEHAVIORAL_REVALIDATION_PENDING' in top_status:
            contradictory: list[str] = []
            def collect_contradiction(node: Any, loc: tuple[str, ...]) -> None:
                if isinstance(node, str) and 'SET_005' in node and 'BEHAVIORAL_REVALIDATION_PASS' in node:
                    contradictory.append('.'.join(loc))
            walk(obj.get('components', []), collect_contradiction)
            require(not contradictory, f'{p}: package behavioral state pending but component PASS remains at {contradictory}')

"""
if 'unsupported SET_005 behavioral PASS claims' not in text:
    if behavioral_anchor not in text:
        raise SystemExit('validator anchor missing: Specialist Index')
    text = text.replace(behavioral_anchor, behavioral_block + behavioral_anchor, 1)

fixture_anchor = "    require(len(fixtures.get('copywriting_behavior_cases', [])) >= 3, 'insufficient Copywriting behavior fixtures')\n"
fixture_insert = fixture_anchor + "    require(len(fixtures.get('semantic_reseal_negative_cases', [])) >= 3, 'insufficient semantic reseal negative fixtures')\n"
if 'insufficient semantic reseal negative fixtures' not in text:
    if fixture_anchor not in text:
        raise SystemExit('validator anchor missing: fixture checks')
    text = text.replace(fixture_anchor, fixture_insert, 1)

print_anchor = "    print('Behavioral replay fixtures: PRESENT (not evidence that model evaluation has run)')\n"
print_insert = "    print('Semantic evidence-state closure: PASS')\n    print('Handoff semantic card_revision receipts: PASS')\n" + print_anchor
if 'Semantic evidence-state closure: PASS' not in text:
    if print_anchor not in text:
        raise SystemExit('validator anchor missing: output summary')
    text = text.replace(print_anchor, print_insert, 1)

validator.write_text(text, encoding='utf-8')

fixtures_path = ROOT / 'tests' / 'air_contract_fixtures.json'
fixtures = load(fixtures_path)
fixtures['semantic_reseal_negative_cases'] = [
    {
        'id': 'SR-01-UNSUPPORTED-BEHAVIORAL-PASS',
        'invalid_if': 'current SET_005 profile/package state claims BEHAVIORAL_REVALIDATION_PASS without a replay manifest for the same Foundation identity with result PASS',
    },
    {
        'id': 'SR-02-STALE-HANDOFF-REVISION-RECEIPT',
        'invalid_if': 'a live compatibility receipt for AIR_HANDOFF_CARD_TEMPLATE.json carries card_revision different from the actual template card_revision',
    },
    {
        'id': 'SR-03-PACKAGE-COMPONENT-BEHAVIORAL-CONTRADICTION',
        'invalid_if': 'package-level current state says behavioral revalidation pending while a current SET_005 component state says behavioral revalidation PASS',
    },
]
dump(fixtures_path, fixtures)


def file_meta(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        'sha256': hashlib.sha256(raw).hexdigest(),
        'size_bytes': len(raw),
        'line_count': len(raw.decode('utf-8').splitlines()),
    }


operational = [
    *sorted((ROOT / 'prompts').glob('*')),
    *sorted((ROOT / 'catalog').glob('*')),
    *sorted(PROFILES.rglob('*')),
]
operational = [p for p in operational if p.is_file()]


def metadata_map() -> dict[str, dict[str, Any]]:
    return {p.name: file_meta(p) for p in operational}


def refresh_refs(node: Any, metas: dict[str, dict[str, Any]]) -> bool:
    changed = False
    if isinstance(node, dict):
        ref = node.get('filename') or node.get('canonical_filename')
        if isinstance(ref, str) and ref in metas:
            meta = metas[ref]
            for key in ('sha256', 'observed_sha256'):
                if key in node and node[key] != meta['sha256']:
                    node[key] = meta['sha256']
                    changed = True
            for key in ('size_bytes', 'line_count'):
                if key in node and node[key] != meta[key]:
                    node[key] = meta[key]
                    changed = True
            if ref == HANDOFF and 'card_revision' in node and node['card_revision'] != EXPECTED_CARD_REVISION:
                node['card_revision'] = EXPECTED_CARD_REVISION
                changed = True
        for value in node.values():
            if isinstance(value, (dict, list)):
                changed |= refresh_refs(value, metas)
    elif isinstance(node, list):
        for value in node:
            if isinstance(value, (dict, list)):
                changed |= refresh_refs(value, metas)
    return changed


for _ in range(12):
    metas = metadata_map()
    changed = False
    for path in profile_files:
        obj = load(path)
        if refresh_refs(obj, metas):
            dump(path, obj)
            changed = True
    if not changed:
        break
else:
    raise SystemExit('profile metadata reseal did not converge')

index_path = ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json'
index = load(index_path)
metas = metadata_map()
index_changed = False
for entry in index.get('entries', []):
    name = entry.get('manifest_filename')
    if name in metas:
        m = metas[name]
        for key, source_key in (
            ('manifest_sha256', 'sha256'),
            ('manifest_size_bytes', 'size_bytes'),
            ('manifest_line_count', 'line_count'),
        ):
            if key in entry and entry[key] != m[source_key]:
                entry[key] = m[source_key]
                index_changed = True
if index_changed:
    dump(index_path, index)

metas = metadata_map()
for path in profile_files:
    obj = load(path)
    if refresh_refs(obj, metas):
        dump(path, obj)

changed_files = subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines()
unexpected = [
    p for p in changed_files
    if not (
        p.startswith('profiles/')
        or p == 'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'
        or p == 'tools/validate_air_release.py'
        or p == 'tests/air_contract_fixtures.json'
    )
]
if unexpected:
    raise SystemExit(f'unexpected changed paths: {unexpected}')

report = {
    'behavioral_state_paths_changed': len(changed_state_paths),
    'handoff_card_revision_paths_changed': len(changed_card_revision_paths),
    'changed_files': changed_files,
    'expected_handoff_card_revision': EXPECTED_CARD_REVISION,
}
Path('/tmp/semantic-reseal-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, indent=2))
