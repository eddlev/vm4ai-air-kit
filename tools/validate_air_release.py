from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any
from validate_air_r8_remediation import E as R8ValidationError, main as validate_r8

ROOT = Path('.')
EXPECTED_KIT_VERSION = '0.7.2'
EXPECTED_FOUNDATION_ID = 'AIR_FOUNDATION_2_6_2_OBJECT_CONTRACT_SET_007'
EXPECTED_ROUTE_MAP_VERSION = '1.2.1'
EXPECTED_INDEX_VERSION = '1.3.2'
EXPECTED_PACKAGE_VERSION = '2.5.0'
EXPECTED_HANDOFF_CARD_REVISION = 18
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
    'AIR_CORE_RUNTIME.md': '2.6.2',
    'AIR_CONTROL_SURFACE.md': '2.6.2',
    'AIR_GOV.md': '2.3.2',
    'AIR_DEFAULT_STARTER_PROFILE.json': '2.6.2',
    'AIR_HANDOFF_CARD_TEMPLATE.json': '2.3.0',
    'AIR_RUNTIME_ROUTE_MAP.json': '1.2.1',
}


HISTORICAL_CONTAINER_KEYS = {
    'source_baseline', 'mainline_release_binding', 't7_change_record',
    'historical_release_catalogs', 'source_candidate_manifest', 'change_history',
    'release_history', 'historical_records',
}
R7_STATIC_PASS = 'PASS_R7_DETERMINISTIC_STATIC_SUITE'
R7_BEHAVIOR_PENDING = 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'
R7_INDEX_COMPLETENESS = 'COMPLETE_FOR_AIR_2_6_2_OBJECT_CONTRACT_SET_007_V072_CANDIDATE_SPECIALIST_CATALOG'
R7_CANDIDATE_STATE = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'

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



def historical_path(path: tuple[str, ...]) -> bool:
    return any(part in HISTORICAL_CONTAINER_KEYS or part.startswith('historical_') for part in path)


def walk_current(obj: Any, fn, path: tuple[str, ...] = ()) -> None:
    if historical_path(path):
        return
    fn(obj, path)
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk_current(v, fn, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_current(v, fn, path + (str(i),))


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
    try:
        validate_r8(ROOT.resolve())
    except (R8ValidationError, KeyError, ValueError) as exc:
        raise ValidationError(f'R8 presentation/portability release check failed: {exc}') from exc
    required_foundation = [
        'AIR_CORE_RUNTIME.md', 'AIR_CONTROL_SURFACE.md', 'AIR_GOV.md',
        'AIR_DEFAULT_STARTER_PROFILE.json', 'AIR_HANDOFF_CARD_TEMPLATE.json',
    ]
    for name in required_foundation:
        require((ROOT / 'prompts' / name).is_file(), f'missing Foundation file {name}')
    require((ROOT / 'catalog' / 'AIR_RUNTIME_ROUTE_MAP.json').is_file(), 'missing Route Map')
    require((ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json').is_file(), 'missing Specialist Index')
    require((ROOT / 'tools' / 'validate_air_release.py').is_file(), 'missing permanent validator')
    require((ROOT / 'tools' / 'validate_air_boot.py').is_file(), 'missing independent boot validator')
    require((ROOT / 'tools' / 'validate_air_suite.py').is_file(), 'missing canonical validation suite runner')
    require((ROOT / 'tools' / 'reseal_air_candidate.py').is_file(), 'missing dependency-graph resealer')
    require((ROOT / 'tools' / 'test_air_validator_mutations.py').is_file(), 'missing validator mutation suite')
    require((ROOT / 'tools' / 'validate_air_contract_registry.py').is_file(), 'missing deterministic contract registry validator')
    require((ROOT / 'tools' / 'test_air_contract_registry_mutations.py').is_file(), 'missing deterministic contract mutation suite')
    require((ROOT / 'tools' / 'validate_air_behavioral_contracts.py').is_file(), 'missing behavioral transaction validator')
    require((ROOT / 'tools' / 'test_air_behavioral_contract_mutations.py').is_file(), 'missing behavioral transaction mutation suite')
    require((ROOT / 'tools' / 'validate_air_control_plane.py').is_file(), 'missing control-plane semantic-loophole validator')
    require((ROOT / 'tools' / 'test_air_control_plane_mutations.py').is_file(), 'missing control-plane semantic-loophole mutation suite')
    require((ROOT / 'tests' / 'air_contract_fixtures.json').is_file(), 'missing regression fixtures')
    require((ROOT / 'tests' / 'deterministic_contract_inventory.json').is_file(), 'missing deterministic contract inventory')

    parsed: dict[Path, Any] = {p: load_json(p) for p in all_json()}
    operational_paths = [p for p in parsed if not str(p).startswith('tests/')]
    idx = basename_index(operational_paths + [ROOT / 'prompts' / 'AIR_CORE_RUNTIME.md', ROOT / 'prompts' / 'AIR_CONTROL_SURFACE.md', ROOT / 'prompts' / 'AIR_GOV.md'])
    metas = {name: meta(path, parsed.get(path)) for name, path in idx.items()}

    core = (ROOT / 'prompts' / 'AIR_CORE_RUNTIME.md').read_text(encoding='utf-8')
    control = (ROOT / 'prompts' / 'AIR_CONTROL_SURFACE.md').read_text(encoding='utf-8')
    require('PROMPT_VERSION: 2.6.2' in core, 'Core version mismatch')
    require('PROMPT_VERSION: 2.6.2' in control, 'Control version mismatch')
    require('Patch marker: AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1' in core, 'missing Core closed-world emission closure')
    require('Patch marker: AIR_CONTROL_CLOSED_WORLD_EMISSION_RENDERER_V1' in control, 'missing Control emission renderer closure')

    gov = (ROOT / 'prompts' / 'AIR_GOV.md').read_text(encoding='utf-8')
    expected_sentinels = {
        'AIR_CORE_RUNTIME.md': 'AIR_LOAD_SENTINEL :: AIR_CORE_RUNTIME :: END_OF_FILE :: LOAD_INTEGRITY_V2',
        'AIR_CONTROL_SURFACE.md': 'AIR_LOAD_SENTINEL :: AIR_CONTROL_SURFACE :: END_OF_FILE :: LOAD_INTEGRITY_V2',
        'AIR_GOV.md': 'AIR_LOAD_SENTINEL :: AIR_HR_GOVERNANCE_SUPPLEMENT :: END_OF_FILE :: LOAD_INTEGRITY_V2',
    }
    for name, body in [('AIR_CORE_RUNTIME.md', core), ('AIR_CONTROL_SURFACE.md', control), ('AIR_GOV.md', gov)]:
        lines = body.rstrip().splitlines()
        require(bool(lines) and lines[-1] == expected_sentinels[name], f'{name}: terminal sentinel is not final content line')
    require('Patch marker: AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1' in core, 'missing Core deterministic-pipeline non-inference law')
    require('AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE' in core, 'missing Core floor 025')
    require('AIR-FLOOR-026-DETERMINISTIC-CONTRACT-MACHINE-REPRESENTATION' in core, 'missing Core floor 026')
    require('AIR-FLOOR-027-FAILURE-MODE-LEARNING-AND-RETRY' in core, 'missing Core floor 027')
    require('Patch marker: AIR_DETERMINISTIC_CONTRACT_MACHINE_REPRESENTATION_V1' in core, 'missing deterministic contract representation law')
    require('Patch marker: AIR_NEW_TASK_BINDING_TRANSACTION_V2' in core, 'missing v0.7.2 new-task binding transaction')
    require('Patch marker: AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1' in control, 'missing v0.7.2 primary response surface law')
    require('Patch marker: AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1' in core, 'missing cognitive scope authority isolation law')
    require('Patch marker: AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_SURFACE_V1' in control, 'missing cognitive scope surface law')
    require('Patch marker: AIR_GOVERNANCE_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1' in gov, 'missing governance cognitive scope law')
    require('PROMPT_VERSION: 2.3.2' in gov, 'Governance version mismatch')

    starter_path = ROOT / 'prompts' / 'AIR_DEFAULT_STARTER_PROFILE.json'
    starter = parsed[starter_path]
    require(starter['PROMPT_VERSION'] == '2.6.2', 'Starter version mismatch')
    require(starter.get('compiler_contract', {}).get('cognitive_scope_authority_isolation', {}).get('required') is True, 'Starter cognitive scope contract missing')
    require(starter.get('compiler_contract', {}).get('closed_world_emission_closure', {}).get('required') is True, 'Starter missing closed-world emission closure mirror')
    vc = starter.get('validation_contract', {})
    require('required_version' not in vc, 'Starter duplicated required_version literal remains')
    require('required_designation' not in vc, 'Starter duplicated required_designation literal remains')
    require('required_cross_file_checks' not in vc, 'Starter operative free-form cross-file checks remain')
    registry = vc.get('deterministic_contract_registry', {})
    require(registry.get('execution_semantics') == 'DETERMINISTIC_PIPELINE', 'Starter deterministic contract registry missing')
    require(registry.get('inference_policy') == 'PROHIBITED', 'Starter deterministic contract registry inference policy mismatch')
    require(registry.get('prose_authority') == 'NON_OPERATIVE_DESCRIPTION', 'Starter deterministic contract prose boundary mismatch')
    dp_starter = starter.get('compiler_contract', {}).get('deterministic_pipeline_non_inference', {})
    require(dp_starter.get('required') is True, 'Starter missing deterministic-pipeline non-inference mirror')
    require(dp_starter.get('inference_policy') == 'PROHIBITED', 'Starter deterministic pipeline inference policy mismatch')
    require('AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE' in starter.get('authority_contract', {}).get('floor_invariants_required', []), 'Starter missing floor 025 requirement')
    require('AIR-FLOOR-026-DETERMINISTIC-CONTRACT-MACHINE-REPRESENTATION' in starter.get('authority_contract', {}).get('floor_invariants_required', []), 'Starter missing floor 026 requirement')
    require(starter.get('compiler_contract', {}).get('deterministic_contract_machine_representation', {}).get('required') is True, 'Starter missing deterministic contract representation mirror')

    handoff = parsed[ROOT / 'prompts' / 'AIR_HANDOFF_CARD_TEMPLATE.json']['AIR_HANDOFF_CARD']
    m = re.search(r'(?m)^CANONICAL_HANDOFF_SCHEMA_VERSION:\s*(\S+)\s*$', core)
    require(bool(m), 'Core canonical handoff schema header missing')
    canonical_schema = m.group(1)
    require(handoff['SCHEMA_VERSION'] == handoff['schema_version'] == canonical_schema, 'Handoff schema mismatch')
    require(handoff['card_revision'] == EXPECTED_HANDOFF_CARD_REVISION, 'Handoff card revision mismatch')
    manifest = handoff['schema_manifest']
    declared = set(manifest['required_fields']) | set(manifest.get('optional_fields', []))
    undeclared = sorted(set(handoff) - declared)
    require(not undeclared, f'Handoff root fields missing from schema manifest: {undeclared}')
    require('runtime_drift_hardening_schema_extension' in declared, 'Handoff drift extension not declared')
    restored_starter = handoff.get('profile_stack', {}).get('starter_profile', {})
    require(restored_starter.get('SYSTEM_DESIGNATION') == starter.get('SYSTEM_DESIGNATION'), 'Handoff Starter designation mismatch')
    require(restored_starter.get('PROMPT_VERSION') == starter.get('PROMPT_VERSION'), 'Handoff Starter version mismatch')
    sc = manifest.get('schema_compatibility_contract', {})
    require('canonical_schema_version' not in sc, 'Handoff duplicated canonical_schema_version literal remains')
    require('starter_identity_version_required' not in sc, 'Handoff duplicated starter_identity_version_required literal remains')
    require(sc.get('canonical_schema_version_source') == 'AIR_CORE_RUNTIME_V2.CANONICAL_HANDOFF_SCHEMA_VERSION', 'Handoff canonical schema source mismatch')
    require(sc.get('starter_identity_version_source') == 'AIR_DEFAULT_STARTER_V2.PROMPT_VERSION', 'Handoff Starter version source mismatch')

    routes = parse_core_routes(core)
    for rid in ['RT.ACTIVATE', 'RT.ALIGN', 'RT.AMEND', 'RT.TASK_SWITCH', 'RT.APPROVAL_RESOLVE', 'RT.ACTION', 'RT.RECEIPT', 'RT.HANDOFF_CREATE']:
        require(rid in routes, f'missing Core route {rid}')
    require('AIR_ALIGNMENT_CHECK' in routes['RT.ALIGN']['produces'] and 'AIR_VALIDATION_REPORT' in routes['RT.ALIGN']['produces'], 'RT.ALIGN pair missing')
    require('AIR_PROJECT_INITIALIZATION_BRIEF_WHEN_FIRST_ACTIVATION' in routes['RT.ACTIVATE']['produces'], 'RT.ACTIVATE missing init brief emission token')
    require('AIR_PROJECT_EXECUTION_MAP_WHEN_FIRST_ACTIVATION' in routes['RT.ACTIVATE']['produces'], 'RT.ACTIVATE missing execution map emission token')
    require('AIR_ARTIFACT' in routes['RT.AMEND']['produces'], 'RT.AMEND missing revised artifact emission')
    require('AIR_PROJECT_EXECUTION_MAP' in routes['RT.TASK_SWITCH']['produces'] and 'AIR_ARTIFACT' in routes['RT.TASK_SWITCH']['produces'], 'RT.TASK_SWITCH emission closure incomplete')
    deterministic_routes = {'RT.BOOT', 'RT.ONBOARD', 'RT.HANDOFF_RESTORE', 'RT.TURN', 'RT.ALIGN', 'RT.APPROVAL_RESOLVE', 'RT.ACTION', 'RT.RECEIPT', 'RT.HANDOFF_CREATE', 'RT.TASK_SWITCH'}
    for rid in sorted(deterministic_routes):
        require(rid in routes, f'missing deterministic Core route {rid}')
        require(routes[rid].get('execution_semantics') == 'DETERMINISTIC_PIPELINE', f'{rid}: execution_semantics mismatch')
        require(routes[rid].get('inference_policy') == 'PROHIBITED', f'{rid}: inference_policy mismatch')
        require(routes[rid].get('step_order') == 'STRICT', f'{rid}: step_order mismatch')
        for key in ['missing_input_behavior', 'unknown_condition_behavior', 'conflict_behavior']:
            require(routes[rid].get(key) == 'FAIL_CLOSED', f'{rid}: {key} mismatch')
        require('AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE' in routes[rid].get('does_not_bypass', ''), f'{rid}: floor 025 bypass protection missing')

    route_map = parsed[ROOT / 'catalog' / 'AIR_RUNTIME_ROUTE_MAP.json']
    require(route_map['MAP_VERSION'] == EXPECTED_ROUTE_MAP_VERSION, 'Route Map version mismatch')
    require(route_map.get('emission_closure', {}).get('core_patch_marker') == 'AIR_CLOSED_WORLD_EMISSION_CLOSURE_V1', 'Route Map missing emission closure metadata')
    require(route_map['source_of_truth']['sha256'] == metas['AIR_CORE_RUNTIME.md']['sha256'], 'Route Map Core hash mismatch')
    route_map_by_id = {r['route_id']: r for r in route_map['routes']}
    require('AIR_PROJECT_INITIALIZATION_BRIEF_WHEN_FIRST_ACTIVATION' in route_map_by_id['RT.ACTIVATE']['produces'], 'Route Map RT.ACTIVATE stale')
    require('AIR_ARTIFACT' in route_map_by_id['RT.AMEND']['produces'], 'Route Map RT.AMEND stale')
    dp_map = route_map.get('deterministic_pipeline_contract', {})
    require(dp_map.get('core_patch_marker') == 'AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1', 'Route Map deterministic pipeline contract missing')
    require(dp_map.get('inference_policy') == 'PROHIBITED', 'Route Map deterministic inference policy mismatch')
    require(set(dp_map.get('declared_route_ids', [])) == deterministic_routes, 'Route Map deterministic route set mismatch')
    for rid in sorted(deterministic_routes):
        rr = route_map_by_id[rid]
        require(rr.get('execution_semantics') == 'DETERMINISTIC_PIPELINE', f'Route Map {rid}: execution_semantics mismatch')
        require(rr.get('inference_policy') == 'PROHIBITED', f'Route Map {rid}: inference_policy mismatch')
        require(rr.get('step_order') == 'STRICT', f'Route Map {rid}: step_order mismatch')
        for key in ['missing_input_behavior', 'unknown_condition_behavior', 'conflict_behavior']:
            require(rr.get(key) == 'FAIL_CLOSED', f'Route Map {rid}: {key} mismatch')

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
        walk_current(parsed[p], lambda node, loc, owner=p: check_ref(node, loc, owner))

    def reject_stale_peer_hash(node: Any, loc: tuple[str, ...]) -> None:
        if isinstance(node, dict):
            bad = [k for k in node if re.match(r'^t\d+_observed_manifest_sha256$', k)]
            require(not bad, f'stale construction-time peer manifest hash keys remain at {".".join(loc)}: {bad}')
    for p in sorted(ROOT.glob('profiles/**/*.json')):
        walk_current(parsed[p], reject_stale_peer_hash)

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
        if isinstance(node, str) and 'SET_006' in node and 'BEHAVIORAL_REVALIDATION_PASS' in node:
            behavioral_pass_claims.append(f'{owner}:{".".join(loc)}')
    for p in sorted(ROOT.glob('profiles/**/*.json')):
        walk_current(parsed[p], lambda node, loc, owner=p: collect_behavioral_pass(node, loc, owner))
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
                if isinstance(node, str) and 'SET_006' in node and 'BEHAVIORAL_REVALIDATION_PASS' in node:
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


    # R7 lifecycle/version/history truth and package reseal.
    require('Patch marker: AIR_SPECIALIST_PACKAGE_INDEX_LIFECYCLE_V1' in core, 'R7 candidate lifecycle marker missing')
    lifecycle = index.get('candidate_lifecycle_contract', {})
    require(lifecycle.get('current_candidate_state') == R7_CANDIDATE_STATE, 'R7 current candidate lifecycle mismatch')
    require(lifecycle.get('candidate_states_are_release_sealed') is False, 'R7 candidate state incorrectly release-sealed')
    require(index.get('catalog_scope', {}).get('catalog_completeness_claim') == R7_INDEX_COMPLETENESS, 'R7 Index completeness identity mismatch')
    require(index.get('validation_state', {}).get('static_validation') == R7_STATIC_PASS, 'R7 Index static validation state mismatch')
    require(index.get('validation_state', {}).get('behavioral_revalidation') == R7_BEHAVIOR_PENDING, 'R7 Index behavioral validation must remain pending without replay evidence')
    for entry in index['entries']:
        require(entry.get('availability_state') == R7_CANDIDATE_STATE, f'R7 candidate availability mismatch: {entry.get("package_identity")}')
    hist_release = index.get('catalog_scope', {}).get('historical_release_catalogs', [])
    require(hist_release == [{
        'kit_release': '0.7.0',
        'foundation_identity': 'AIR_FOUNDATION_2_5_0_OBJECT_CONTRACT_SET_004',
        'index_generation': 'V070',
        'catalog_completeness_claim': 'COMPLETE_FOR_AIR_2_5_0_SET_004_V070_RELEASE_SPECIALIST_CATALOG',
        'state': 'RELEASED_HISTORICAL_NON_OPERATIVE',
    }], 'R7 historical v0.7.0 catalog identity mismatch')

    expected_current_foundation_state = 'OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_' + EXPECTED_FOUNDATION_ID
    current_identity_count = 0
    for pp in sorted(ROOT.glob('profiles/**/*.json')):
        oo = parsed[pp]
        ir = oo.get('integration_refresh') if isinstance(oo, dict) else None
        if isinstance(ir, dict) and 'foundation_identity_state' in ir:
            current_identity_count += 1
            require(ir['foundation_identity_state'] == expected_current_foundation_state, f'{pp}: R7 current Foundation identity stale')
    require(current_identity_count == 21, f'R7 current Foundation identity carrier count changed: {current_identity_count}')

    for mp in sorted(ROOT.glob('profiles/**/*PACKAGE_MANIFEST.json')):
        mo = parsed[mp]
        for comp in mo.get('components', []):
            cp = mp.parent / comp['filename']
            co = parsed[cp]
            canonical_status = str(co.get('STATUS') or co.get('status') or '')
            require(comp.get('status') == canonical_status, f'{mp}: R7 component status mirror mismatch {comp["filename"]}')
            expected_availability = 'VALIDATED_AVAILABLE_UNBOUND' if 'STATIC_VALIDATED' in canonical_status else 'AVAILABLE_UNVALIDATED'
            require(comp.get('availability_state') == expected_availability, f'{mp}: R7 component availability mirror mismatch {comp["filename"]}')

    gov_manifest = parsed[ROOT / 'profiles' / 'governance specialist' / 'AIR_AI_GOVERNANCE_SPECIALIST_PACKAGE_MANIFEST.json']
    expected_roles = [c.get('role') for c in gov_manifest.get('components', [])]
    require(gov_manifest.get('failure_mode_integration_contract', {}).get('component_roles_observed') == expected_roles and all(expected_roles), 'R7 Governance component role mirror mismatch')

    sfv_method = parsed[ROOT / 'profiles' / 'specification first verification specialist' / 'AIR_SPECIFICATION_FIRST_VERIFICATION_METHOD_PACK.json']
    sfv_vc = sfv_method.get('validation_contract', {})
    require('required_package_version' not in sfv_vc, 'R7 SFV stale required_package_version literal remains')
    require(sfv_vc.get('required_package_version_source') == '$.package_version' and sfv_vc.get('required_package_version_check') == 'EQUAL_TO_CANONICAL_TOP_LEVEL_PACKAGE_VERSION', 'R7 SFV package version source/check missing')

    cea_manifest = parsed[ROOT / 'profiles' / 'capability ecology architect' / 'AIR_CAPABILITY_ECOLOGY_ARCHITECT_PACKAGE_MANIFEST.json']
    require(cea_manifest.get('t7_change_record', {}).get('package_version') == '2.4.0', 'R7 T7 historical package_version rewritten')
    require(cea_manifest.get('t7_change_record', {}).get('source_package_version') == '2.3.9', 'R7 T7 historical source version rewritten')

    inventory = parsed[ROOT / 'tests' / 'deterministic_contract_inventory.json']
    require(inventory.get('inventory_id') == 'AIR_SET007_DETERMINISTIC_CONTRACT_INVENTORY_V1', 'deterministic contract inventory identity mismatch')
    require(inventory.get('typed_deterministic_check_count') == len(registry.get('checks', [])), 'deterministic contract inventory count mismatch')
    require(inventory.get('migrated_validation_expectation_count') == len(vc.get('validation_expectations', [])), 'validation expectation inventory count mismatch')
    require(inventory.get('legacy_required_cross_file_checks_operational_state') == 'REMOVED_AS_OPERATIVE_FREE_FORM_AUTHORITY', 'legacy operative prose inventory state mismatch')

    fixtures = parsed[ROOT / 'tests' / 'air_contract_fixtures.json']
    require(fixtures.get('fixture_set') == 'AIR_SET007_REGRESSION_FIXTURES_V1', 'fixture identity mismatch')
    require(len(fixtures.get('emission_closure_cases', [])) >= 5, 'insufficient emission fixtures')
    require(len(fixtures.get('copywriting_behavior_cases', [])) >= 3, 'insufficient Copywriting behavior fixtures')
    require(len(fixtures.get('semantic_reseal_negative_cases', [])) >= 3, 'insufficient semantic reseal negative fixtures')
    require(len(fixtures.get('validation_spine_negative_cases', [])) >= 4, 'insufficient validation spine negative fixtures')
    require(len(fixtures.get('routine_boot_negative_cases', [])) >= 3, 'insufficient routine boot negative fixtures')
    require(len(fixtures.get('deterministic_pipeline_negative_cases', [])) >= 5, 'insufficient deterministic pipeline negative fixtures')
    require(len(fixtures.get('deterministic_contract_representation_negative_cases', [])) >= 6, 'insufficient deterministic contract representation fixtures')
    require(len(fixtures.get('emission_closure_cases', [])) >= 8, 'insufficient emission closure fixtures')
    require(len(fixtures.get('handoff_negative_cases', [])) >= 3, 'insufficient handoff provenance fixtures')
    require(len(fixtures.get('material_action_transaction_negative_cases', [])) >= 9, 'insufficient material action transaction fixtures')

    r7_ids = {x.get('id') for x in fixtures.get('r7_lifecycle_reseal_cases', [])}
    require({
        'R7-LC-01-CANDIDATE-NOT-RELEASED',
        'R7-LC-02-BEHAVIORAL-EVIDENCE-BOUNDARY',
        'R7-LC-03-HISTORY-IMMUTABLE',
        'R7-LC-04-SFV-PACKAGE-VERSION-SOURCE',
        'R7-LC-05-GOVERNANCE-COMPONENT-ROLES',
    } <= r7_ids, 'R7 lifecycle/reseal regression fixtures missing')

    print('AIR v0.7.2 set-007 candidate deterministic validation: PASS')
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
    print('Routine boot coherence: PASS')
    print('Deterministic pipeline non-inference contract: PASS')
    print(f'Deterministic contract registry: PRESENT ({len(registry.get("checks", []))} typed checks)')
    print('Deterministic contract prose authority: NON_OPERATIVE')
    print('Deterministic contract inventory: PRESENT')
    print('Behavioral replay fixtures: PRESENT (not evidence that model evaluation has run)')
    print('Validation spine regression fixtures: PRESENT')
    print('Behavioral transaction contract fixtures: PRESENT')

if __name__ == '__main__':
    try:
        main()
    except ValidationError as exc:
        raise SystemExit(f'AIR release validation FAILED: {exc}')
