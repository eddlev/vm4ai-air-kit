from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path('.')
EXPECTED_KIT_VERSION = '0.7.1'
EXPECTED_FOUNDATION_ID = 'AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005'
EXPECTED_ROUTE_MAP_VERSION = '1.1.0'
EXPECTED_INDEX_VERSION = '1.3.0'
EXPECTED_PACKAGE_VERSION = '2.5.0'
EXPECTED_HANDOFF_CARD_REVISION = 16
EXPECTED_SPECIALIST_DIRS = {
    'capability ecology architect',
    'governance specialist',
    'grounding specialist',
    'public surface copywriting specialist',
    'specification first verification specialist',
}
METHOD_REQUIRED_FIELDS = {
    'SYSTEM_DESIGNATION', 'PROMPT_VERSION', 'PROFILE_KIND', 'method_id', 'purpose',
    'scope', 'inputs', 'outputs', 'dependencies', 'ordered_steps',
    'staleness_policy', 'handoff_requirements', 'binding_requirements',
}
METHOD_STEP_REQUIRED_FIELDS = {
    'step_id', 'name', 'action', 'preconditions', 'required_inputs',
    'expected_outputs', 'evidence_to_advance', 'failure_behavior', 'next_step_rule',
}
SPECIALIST_REQUIRED_FIELDS = {
    'title', 'SYSTEM_DESIGNATION', 'PROFILE_KIND', 'STATUS', 'STANDARD_CODE',
    'description', 'capability_scope', 'non_goals', 'source_layer', 'preferred_geometry',
    'lambda_pressure_defaults', 'vector_family_preferences', 'required_vectors',
    'preferred_vectors', 'blocking_conditions', 'execution_constraints', 'deliverables',
    'output_contract', 'specialist_integrity_check', 'recommended_domain_packages',
    'compatible_domain_packages', 'runtime_law_extensions',
}
FOUNDATION_VERSION = {
    'AIR_CORE_RUNTIME.md': '2.6.0',
    'AIR_CONTROL_SURFACE.md': '2.6.0',
    'AIR_GOV.md': '2.3.0',
    'AIR_DEFAULT_STARTER_PROFILE.json': '2.6.0',
    'AIR_HANDOFF_CARD_TEMPLATE.json': '2.3.0',
    'AIR_RUNTIME_ROUTE_MAP.json': '1.1.0',
}

class ValidationError(Exception):
    pass


def reject_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in out:
            raise ValidationError(f'duplicate JSON key: {k}')
        out[k] = v
    return out


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=reject_dupes)
    except Exception as exc:
        raise ValidationError(f'{path}: strict JSON parse failed: {exc}') from exc


def meta(path: Path, parsed: Any | None = None) -> dict[str, Any]:
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    if parsed is None and path.suffix == '.json':
        parsed = load_json(path)
    designation = None
    prompt_version = None
    component_version = None
    if isinstance(parsed, dict):
        designation = parsed.get('SYSTEM_DESIGNATION') or parsed.get('PACKAGE_DESIGNATION')
        prompt_version = parsed.get('PROMPT_VERSION')
        component_version = parsed.get('package_version') or parsed.get('PACKAGE_VERSION') or prompt_version
    return {
        'path': path, 'sha256': hashlib.sha256(raw).hexdigest(), 'size_bytes': len(raw),
        'line_count': len(text.splitlines()), 'designation': designation,
        'prompt_version': prompt_version, 'component_version': component_version,
    }


def all_json() -> list[Path]:
    return sorted([
        *ROOT.glob('prompts/*.json'), *ROOT.glob('catalog/*.json'), *ROOT.glob('profiles/**/*.json'),
        *ROOT.glob('tests/*.json'),
    ])


def basename_index(paths: list[Path]) -> dict[str, Path]:
    idx: dict[str, Path] = {}
    for p in paths:
        if p.name in idx:
            raise ValidationError(f'duplicate operational basename: {p.name}: {idx[p.name]} vs {p}')
        idx[p.name] = p
    return idx


def walk(obj: Any, fn, path: tuple[str, ...] = ()) -> None:
    fn(obj, path)
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk(v, fn, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, fn, path + (str(i),))


def parse_core_routes(core: str) -> dict[str, dict[str, str]]:
    routes: dict[str, dict[str, str]] = {}
    for block in core.split('[AIR_ROUTE]')[1:]:
        rec: dict[str, str] = {}
        for line in block.splitlines():
            line = line.strip()
            if not line:
                if rec:
                    break
                continue
            if line.startswith('=') or line.startswith('['):
                break
            if '=' in line:
                k, v = line.split('=', 1)
                rec[k.strip()] = v.strip()
        if 'id' in rec:
            routes[rec['id']] = rec
    return routes


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValidationError(msg)


def main() -> None:
    require((ROOT / 'VERSION').read_text(encoding='utf-8').strip() == EXPECTED_KIT_VERSION, 'VERSION mismatch')
    required_foundation = [
        'AIR_CORE_RUNTIME.md', 'AIR_CONTROL_SURFACE.md', 'AIR_GOV.md',
        'AIR_DEFAULT_STARTER_PROFILE.json', 'AIR_HANDOFF_CARD_TEMPLATE.json',
    ]
    for name in required_foundation:
        require((ROOT / 'prompts' / name).is_file(), f'missing Foundation file {name}')
    require((ROOT / 'catalog' / 'AIR_RUNTIME_ROUTE_MAP.json').is_file(), 'missing Route Map')
    require((ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json').is_file(), 'missing Specialist Index')
    require((ROOT / 'tools' / 'validate_air_release.py').is_file(), 'missing permanent validator')
    require((ROOT / 'tests' / 'air_contract_fixtures.json').is_file(), 'missing regression fixtures')

    parsed: dict[Path, Any] = {p: load_json(p) for p in all_json()}
    operational_paths = [p for p in parsed if not str(p).startswith('tests/')]
    idx = basename_index(operational_paths + [ROOT / 'prompts' / 'AIR_CORE_RUNTIME.md', ROOT / 'prompts' / 'AIR_CONTROL_SURFACE.md', ROOT / 'prompts' / 'AIR_GOV.md'])
    metas = {name: meta(path, parsed.get(path)) for name, path in idx.items()}

    core = (ROOT / 'prompts' / 'AIR_CORE_RUNTIME.md').read_text(encoding='utf-8')
    control = (ROOT / 'prompts' / 'AIR_CONTROL_SURFACE.md').read_text(encoding='utf-8')
    require('PROMPT_VERSION: 2.6.0' in core, 'Core version mismatch')
    require('PROMPT_VERSION: 2.6.0' in control, 'Control version mismatch')
    require('Patch marker: AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1' in core, 'missing Core closed-world emission closure')
    require('Patch marker: AIR_CONTROL_CLOSED_WORLD_EMISSION_RENDERER_V1' in control, 'missing Control emission renderer closure')

    starter_path = ROOT / 'prompts' / 'AIR_DEFAULT_STARTER_PROFILE.json'
    starter = parsed[starter_path]
    require(starter['PROMPT_VERSION'] == '2.6.0', 'Starter version mismatch')
    require(starter.get('compiler_contract', {}).get('closed_world_emission_closure', {}).get('required') is True, 'Starter missing closed-world emission closure mirror')

    handoff = parsed[ROOT / 'prompts' / 'AIR_HANDOFF_CARD_TEMPLATE.json']['AIR_HANDOFF_CARD']
    require(handoff['schema_version'] == '2.3.0', 'Handoff schema mismatch')
    require(handoff['card_revision'] == EXPECTED_HANDOFF_CARD_REVISION, 'Handoff card revision mismatch')
    manifest = handoff['schema_manifest']
    declared = set(manifest['required_fields']) | set(manifest.get('optional_fields', []))
    undeclared = sorted(set(handoff) - declared)
    require(not undeclared, f'Handoff root fields missing from schema manifest: {undeclared}')
    require('runtime_drift_hardening_schema_extension' in declared, 'Handoff drift extension not declared')

    routes = parse_core_routes(core)
    for rid in ['RT.ACTIVATE', 'RT.ALIGN', 'RT.AMEND', 'RT.TASK_SWITCH', 'RT.ACTION', 'RT.RECEIPT', 'RT.HANDOFF_CREATE']:
        require(rid in routes, f'missing Core route {rid}')
    require('AIR_ALIGNMENT_CHECK' in routes['RT.ALIGN']['produces'] and 'AIR_VALIDATION_REPORT' in routes['RT.ALIGN']['produces'], 'RT.ALIGN pair missing')
    require('AIR_PROJECT_INITIALIZATION_BRIEF_WHEN_FIRST_ACTIVATION' in routes['RT.ACTIVATE']['produces'], 'RT.ACTIVATE missing init brief emission token')
    require('AIR_PROJECT_EXECUTION_MAP_WHEN_FIRST_ACTIVATION' in routes['RT.ACTIVATE']['produces'], 'RT.ACTIVATE missing execution map emission token')
    require('AIR_ARTIFACT' in routes['RT.AMEND']['produces'], 'RT.AMEND missing revised artifact emission')
    require('AIR_PROJECT_EXECUTION_MAP' in routes['RT.TASK_SWITCH']['produces'] and 'AIR_ARTIFACT' in routes['RT.TASK_SWITCH']['produces'], 'RT.TASK_SWITCH emission closure incomplete')

    route_map = parsed[ROOT / 'catalog' / 'AIR_RUNTIME_ROUTE_MAP.json']
    require(route_map['MAP_VERSION'] == EXPECTED_ROUTE_MAP_VERSION, 'Route Map version mismatch')
    require(route_map.get('emission_closure', {}).get('core_patch_marker') == 'AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1', 'Route Map missing emission closure metadata')
    require(route_map['source_of_truth']['sha256'] == metas['AIR_CORE_RUNTIME.md']['sha256'], 'Route Map Core hash mismatch')
    route_map_by_id = {r['route_id']: r for r in route_map['routes']}
    require('AIR_PROJECT_INITIALIZATION_BRIEF_WHEN_FIRST_ACTIVATION' in route_map_by_id['RT.ACTIVATE']['produces'], 'Route Map RT.ACTIVATE stale')
    require('AIR_ARTIFACT' in route_map_by_id['RT.AMEND']['produces'], 'Route Map RT.AMEND stale')

    specialist_dirs = {p.name for p in (ROOT / 'profiles').iterdir() if p.is_dir()}
    require(specialist_dirs == EXPECTED_SPECIALIST_DIRS, f'Specialist directories mismatch: {sorted(specialist_dirs)}')

    specialist_count = 0
    method_count = 0
    manifest_count = 0
    for p in sorted(ROOT.glob('profiles/**/*.json')):
        obj = parsed[p]
        pfc = obj.get('profile_function_class') if isinstance(obj, dict) else None
        if pfc == 'SPECIALIST_CAPABILITY_PROFILE':
            specialist_count += 1
            missing = sorted(SPECIALIST_REQUIRED_FIELDS - set(obj))
            require(not missing, f'{p}: Specialist contract missing {missing}')
        if pfc == 'METHOD_PACK':
            method_count += 1
            missing = sorted(METHOD_REQUIRED_FIELDS - set(obj))
            require(not missing, f'{p}: Method contract missing {missing}')
            require(isinstance(obj['ordered_steps'], list) and obj['ordered_steps'], f'{p}: ordered_steps empty')
            for s in obj['ordered_steps']:
                sm = sorted(METHOD_STEP_REQUIRED_FIELDS - set(s))
                require(not sm, f'{p}: method step {s.get("step_id")} missing {sm}')
        if obj.get('artifact_class') == 'SPECIALIST_PACKAGE_MANIFEST':
            manifest_count += 1
            components = obj.get('components', [])
            require(isinstance(components, list) and components, f'{p}: manifest components missing')
            if 'component_count' in obj:
                require(obj['component_count'] == len(components), f'{p}: component_count mismatch')
            for c in components:
                name = c.get('filename')
                require(name in metas, f'{p}: manifest references missing component {name}')
                m = metas[name]
                require(c.get('sha256') == m['sha256'], f'{p}: hash mismatch for {name}')
                require(c.get('size_bytes') == m['size_bytes'], f'{p}: size mismatch for {name}')
                require(c.get('line_count') == m['line_count'], f'{p}: line count mismatch for {name}')
        # Package release version, when carried, must be current.
        if isinstance(obj, dict) and 'package_version' in obj:
            require(obj['package_version'] == EXPECTED_PACKAGE_VERSION, f'{p}: package_version mismatch')
        if isinstance(obj, dict) and 'PACKAGE_VERSION' in obj:
            require(obj['PACKAGE_VERSION'] == EXPECTED_PACKAGE_VERSION, f'{p}: PACKAGE_VERSION mismatch')

    require(specialist_count == 5, f'expected 5 Specialist profiles, found {specialist_count}')
    require(method_count >= 5, f'expected at least 5 Method Packs, found {method_count}')
    require(manifest_count == 5, f'expected 5 package manifests, found {manifest_count}')

    copy = parsed[ROOT / 'profiles' / 'public surface copywriting specialist' / 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST.json']
    for key in ['required_input_acquisition_contract', 'knowledge_to_execution_path_contract', 'synthetic_benchmark_contract', 'mii_contribution_contract', 'specialist_delta_contract']:
        require(key in copy, f'Copywriting Specialist missing {key}')
    require(copy['specialist_delta_contract'].get('generic_copy_is_not_sufficient', True) is True, 'Copywriting delta contract invalid')

    # Check every live filename/hash metadata record against actual bytes.
    def check_ref(node: Any, path_tuple: tuple[str, ...], owner: Path) -> None:
        if not isinstance(node, dict):
            return
        ref = node.get('filename') or node.get('canonical_filename')
        if not isinstance(ref, str) or ref not in metas or ref == owner.name:
            return
        m = metas[ref]
        if 'sha256' in node:
            require(node['sha256'] == m['sha256'], f'{owner}: stale sha256 for {ref} at {".".join(path_tuple)}')
        if 'observed_sha256' in node:
            require(node['observed_sha256'] == m['sha256'], f'{owner}: stale observed_sha256 for {ref} at {".".join(path_tuple)}')
        if 'size_bytes' in node:
            require(node['size_bytes'] == m['size_bytes'], f'{owner}: stale size for {ref} at {".".join(path_tuple)}')
        if 'line_count' in node:
            require(node['line_count'] == m['line_count'], f'{owner}: stale line_count for {ref} at {".".join(path_tuple)}')
        if ref in FOUNDATION_VERSION and 'version' in node:
            require(node['version'] == FOUNDATION_VERSION[ref], f'{owner}: stale version for {ref}')
        if ref == 'AIR_HANDOFF_CARD_TEMPLATE.json' and 'card_revision' in node:
            require(node['card_revision'] == EXPECTED_HANDOFF_CARD_REVISION, f'{owner}: stale card_revision for {ref} at {".".join(path_tuple)}')

    for p in sorted(ROOT.glob('profiles/**/*.json')):
        walk(parsed[p], lambda node, loc, owner=p: check_ref(node, loc, owner))

    def reject_stale_peer_hash(node: Any, loc: tuple[str, ...]) -> None:
        if isinstance(node, dict):
            bad = [k for k in node if re.match(r'^t\d+_observed_manifest_sha256$', k)]
            require(not bad, f'stale construction-time peer manifest hash keys remain at {".".join(loc)}: {bad}')
    for p in sorted(ROOT.glob('profiles/**/*.json')):
        walk(parsed[p], reject_stale_peer_hash)

    behavioral_manifest_path = ROOT / 'tests' / 'behavioral_revalidation_manifest.json'
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

    index = parsed[ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json']
    require(index['INDEX_VERSION'] == EXPECTED_INDEX_VERSION, 'Specialist Index version mismatch')
    require(index['catalog_scope']['specialist_package_count'] == 5, 'Index package count mismatch')
    require(index['validation_state'].get('release_publication_state') == 'EXTERNAL_RELEASE_STATE_NOT_RUNTIME_AUTHORITY', 'Index carries stale publication state')
    require(index['foundation_compatibility_catalog']['identity'] == EXPECTED_FOUNDATION_ID, 'Index Foundation identity mismatch')
    for entry in index['entries']:
        require(entry['package_version'] == EXPECTED_PACKAGE_VERSION, f'Index package version stale: {entry["package_identity"]}')
        manifest_name = entry['manifest_filename']
        require(manifest_name in metas, f'Index missing manifest target {manifest_name}')
        require(entry['manifest_sha256'] == metas[manifest_name]['sha256'], f'Index manifest hash mismatch {manifest_name}')

    fixtures = parsed[ROOT / 'tests' / 'air_contract_fixtures.json']
    require(fixtures.get('fixture_set') == 'AIR_SET005_REGRESSION_FIXTURES_V1', 'fixture identity mismatch')
    require(len(fixtures.get('emission_closure_cases', [])) >= 5, 'insufficient emission fixtures')
    require(len(fixtures.get('copywriting_behavior_cases', [])) >= 3, 'insufficient Copywriting behavior fixtures')
    require(len(fixtures.get('semantic_reseal_negative_cases', [])) >= 3, 'insufficient semantic reseal negative fixtures')

    print('AIR v0.7.1 set-005 deterministic validation: PASS')
    print(f'Strict JSON files: {len(parsed)}')
    print(f'Specialist profiles: {specialist_count}/5')
    print(f'Method packs: {method_count}')
    print(f'Package manifests: {manifest_count}/5')
    print('Handoff schema-manifest root closure: PASS')
    print('Closed-world emission route closure: PASS')
    print('Manifest/dependency hash-size-line closure: PASS')
    print('Copywriting operational delta contract: PRESENT')
    print('Semantic evidence-state closure: PASS')
    print('Handoff semantic card_revision receipts: PASS')
    print('Behavioral replay fixtures: PRESENT (not evidence that model evaluation has run)')

if __name__ == '__main__':
    try:
        main()
    except ValidationError as exc:
        raise SystemExit(f'AIR release validation FAILED: {exc}')
