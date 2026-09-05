from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path('.')
FLOOR25 = 'AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE'
DETERMINISTIC_ROUTES = {
    'RT.BOOT',
    'RT.ONBOARD',
    'RT.HANDOFF_RESTORE',
    'RT.TURN',
    'RT.ALIGN',
    'RT.ACTION',
    'RT.RECEIPT',
    'RT.HANDOFF_CREATE',
}
SENTINELS = {
    'AIR_CORE_RUNTIME.md': 'AIR_LOAD_SENTINEL :: AIR_CORE_RUNTIME :: END_OF_FILE :: LOAD_INTEGRITY_V2',
    'AIR_CONTROL_SURFACE.md': 'AIR_LOAD_SENTINEL :: AIR_CONTROL_SURFACE :: END_OF_FILE :: LOAD_INTEGRITY_V2',
    'AIR_GOV.md': 'AIR_LOAD_SENTINEL :: AIR_HR_GOVERNANCE_SUPPLEMENT :: END_OF_FILE :: LOAD_INTEGRITY_V2',
}
FOUNDATION_VERSIONS = {
    'AIR_CORE_RUNTIME.md': '2.6.0',
    'AIR_CONTROL_SURFACE.md': '2.6.0',
    'AIR_GOV.md': '2.3.0',
    'AIR_DEFAULT_STARTER_PROFILE.json': '2.6.0',
    'AIR_HANDOFF_CARD_TEMPLATE.json': '2.3.0',
    'AIR_RUNTIME_ROUTE_MAP.json': '1.1.0',
}


def fail(msg: str) -> None:
    raise SystemExit(msg)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def metadata(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        'sha256': hashlib.sha256(raw).hexdigest(),
        'size_bytes': len(raw),
        'line_count': len(raw.decode('utf-8').splitlines()),
    }


def ensure_terminal_sentinel(path: Path, sentinel: str) -> None:
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [line for line in lines if line.strip() != sentinel]
    while lines and not lines[-1].strip():
        lines.pop()
    lines.extend(['', sentinel])
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def add_floor_to_lists(obj: Any) -> bool:
    changed = False
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k in {'required_floor_invariants', 'floor_invariants_required'} and isinstance(v, list):
                if FLOOR25 not in v:
                    v.append(FLOOR25)
                    changed = True
            if add_floor_to_lists(v):
                changed = True
    elif isinstance(obj, list):
        for v in obj:
            if add_floor_to_lists(v):
                changed = True
    return changed


def patch_core() -> None:
    path = ROOT / 'prompts' / 'AIR_CORE_RUNTIME.md'
    text = path.read_text(encoding='utf-8')
    floor24 = '- AIR-FLOOR-024-COGNITIVE-CONTRIBUTION-NONAUTHORITY-AND-BENCHMARK-COMPILATION: MII cognitive nodes, specialists, translators, domain packages, methods, and other processors may generate candidate contributions but never positive execution authority. Their results become operative only after validation and compilation into or explicit reference by the sole bound Orbit 0 AIR_ARTIFACT benchmark.'
    floor25 = '- AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE: when Core declares a pipeline or route segment DETERMINISTIC_PIPELINE, AIR has no inference authority over its required inputs, conditions, ordering, transitions, outputs, or pass/fail criteria. Execute the declared pipeline exactly; missing, ambiguous, conflicting, invalid, or unavailable required state fails closed or requests the smallest exact required input. MII, Specialists, heuristics, historical state, and contextual likelihood may not fill deterministic pipeline slots unless an explicit pipeline step invokes and validates that contribution.'
    if FLOOR25 not in text:
        if floor24 not in text:
            fail('Core floor 024 anchor not found')
        text = text.replace(floor24, floor24 + '\n' + floor25, 1)
    alias24 = '- AIR-FLOOR-024 => AIR-FLOOR-024-COGNITIVE-CONTRIBUTION-NONAUTHORITY-AND-BENCHMARK-COMPILATION'
    alias25 = '- AIR-FLOOR-025 => AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE'
    if alias25 not in text:
        if alias24 not in text:
            fail('Core alias 024 anchor not found')
        text = text.replace(alias24, alias24 + '\n' + alias25, 1)

    law_marker = 'Patch marker: AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1'
    if law_marker not in text:
        anchor = '==================================================\nACTIVE-STATE RECONCILIATION LAW\n=================================================='
        if anchor not in text:
            fail('Core active-state law anchor not found')
        law = '''==================================================
DETERMINISTIC PIPELINE NON-INFERENCE LAW
==================================================

Patch marker: AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1
Floor invariant: AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE

Core principle:
When a Core-owned route or pipeline is explicitly classified as DETERMINISTIC_PIPELINE, AIR must follow the declared pipeline exactly. Deterministic pipeline state is not a cognitive completion task.

Rules:
1. inference_policy = PROHIBITED for undeclared or unresolved deterministic slots.
2. AIR must not infer, interpolate, repair, substitute, reorder, skip, widen, narrow, optimize, or silently default a deterministic pipeline input, condition, transition, output, or pass/fail criterion.
3. Missing, ambiguous, conflicting, invalid, or unavailable required deterministic state routes to FAIL_CLOSED or the smallest exact AIR_REQUIRED_INPUT_REQUEST defined by the pipeline.
4. A router or classifier may resolve whether a declared condition is satisfied when the condition definition permits classification; it may not invent the consequence. Once a deterministic route is selected, the declared table/pipeline owns the consequence.
5. MII, Specialists, translators, methods, heuristics, remembered context, historical state, and contextual likelihood cannot fill deterministic pipeline slots unless the deterministic pipeline explicitly declares an invocation step, input/output schema, validation rule, and acceptance boundary for that contribution.
6. Cognitive output must not contaminate deterministic control state. A cognitive result becomes usable inside a deterministic pipeline only at an explicit declared ingestion step after validation.
7. step_order = STRICT unless the pipeline itself declares a different deterministic partial order.
8. unknown_condition_behavior, missing_input_behavior, and conflict_behavior default to FAIL_CLOSED for deterministic pipelines.
9. A deterministic pipeline may not downgrade itself to a cognitive/advisory path merely to continue execution.

Canonical deterministic runtime route set for this Foundation candidate:
- RT.BOOT
- RT.ONBOARD
- RT.HANDOFF_RESTORE
- RT.TURN
- RT.ALIGN
- RT.ACTION
- RT.RECEIPT
- RT.HANDOFF_CREATE

The route set is explicit and closed for this candidate. Routes not listed above are not made deterministic by analogy.

'''
        text = text.replace(anchor, law + anchor, 1)

    intro = "Each [AIR_ROUTE] block is canonical route metadata. `requires` names route-entry dependencies, `produces` names state/object effects, `allowed_next` names acyclic same-turn forward edges, `invalidates` names state that becomes stale, and `does_not_bypass` names mandatory dependencies that remain in force. Optional `alignment_interlock`, `alignment_profile`, and `alignment_interlock_point` fields declare a Core-owned RT.ALIGN evaluation that must run at the stated interlock point without being modeled as a cyclic `allowed_next` edge."
    intro2 = intro + " Optional `execution_semantics`, `inference_policy`, `step_order`, `missing_input_behavior`, `unknown_condition_behavior`, and `conflict_behavior` fields classify deterministic route execution under AIR-FLOOR-025. These fields may constrain a route but may not grant inference authority."
    if intro in text and 'Optional `execution_semantics`' not in text:
        text = text.replace(intro, intro2, 1)

    parts = text.split('[AIR_ROUTE]')
    out = [parts[0]]
    for part in parts[1:]:
        lines = part.splitlines()
        rid = None
        for line in lines[:12]:
            if line.startswith('id='):
                rid = line.split('=', 1)[1].strip()
                break
        if rid in DETERMINISTIC_ROUTES:
            if not any(line.startswith('execution_semantics=') for line in lines):
                insert_at = next((i + 1 for i, line in enumerate(lines) if line.startswith('semantic_owner=')), 2)
                meta_lines = [
                    'execution_semantics=DETERMINISTIC_PIPELINE',
                    'inference_policy=PROHIBITED',
                    'step_order=STRICT',
                    'missing_input_behavior=FAIL_CLOSED',
                    'unknown_condition_behavior=FAIL_CLOSED',
                    'conflict_behavior=FAIL_CLOSED',
                ]
                lines[insert_at:insert_at] = meta_lines
            for i, line in enumerate(lines):
                if line.startswith('does_not_bypass='):
                    vals = line.split('=', 1)[1].split(';') if line.split('=', 1)[1] else []
                    if FLOOR25 not in vals:
                        vals.append(FLOOR25)
                    lines[i] = 'does_not_bypass=' + ';'.join(vals)
                    break
        out.append('[AIR_ROUTE]' + '\n'.join(lines))
    text = ''.join(out)
    path.write_text(text, encoding='utf-8')
    ensure_terminal_sentinel(path, SENTINELS[path.name])


def patch_control() -> None:
    path = ROOT / 'prompts' / 'AIR_CONTROL_SURFACE.md'
    ensure_terminal_sentinel(path, SENTINELS[path.name])


def patch_governance() -> None:
    path = ROOT / 'prompts' / 'AIR_GOV.md'
    text = path.read_text(encoding='utf-8')
    old = '9. The active registry includes AIR-FLOOR-021 through AIR-FLOOR-024. Governance may tighten them but may not redefine alignment-evaluation dependency, semantic fidelity, epistemic sufficiency, or MII contribution authority.'
    new = '9. The active registry includes AIR-FLOOR-021 through AIR-FLOOR-025. Governance may tighten them but may not redefine alignment-evaluation dependency, semantic fidelity, epistemic sufficiency, MII contribution authority, or deterministic-pipeline non-inference.'
    if old in text:
        text = text.replace(old, new, 1)
    sub = '- Governance findings are candidate benchmark/governance contributions until compiled into or explicitly referenced by the bound Orbit 0 AIR_ARTIFACT.'
    add = sub + '\n- Governance may not infer, substitute, optimize, reorder, skip, or default a Core-declared DETERMINISTIC_PIPELINE step or slot; AIR-FLOOR-025 remains Core-owned.'
    if 'Governance may not infer, substitute, optimize, reorder, skip, or default a Core-declared DETERMINISTIC_PIPELINE' not in text:
        if sub not in text:
            fail('Governance route subordination anchor not found')
        text = text.replace(sub, add, 1)
    path.write_text(text, encoding='utf-8')
    ensure_terminal_sentinel(path, SENTINELS[path.name])


def patch_starter() -> str:
    path = ROOT / 'prompts' / 'AIR_DEFAULT_STARTER_PROFILE.json'
    obj = load(path)
    version = obj['PROMPT_VERSION']
    obj['validation_contract']['required_version'] = version
    for i, item in enumerate(obj['validation_contract'].get('required_retests', [])):
        if isinstance(item, str) and item == 'Handoff Template restored starter profile version equals 2.5.0 and startup files may include AIR_RUNTIME_ROUTE_MAP.json without granting it semantic authority':
            obj['validation_contract']['required_retests'][i] = f'Handoff Template restored starter profile version equals {version} and startup files may include AIR_RUNTIME_ROUTE_MAP.json without granting it semantic authority'
    floors = obj['authority_contract'].setdefault('floor_invariants_required', [])
    if FLOOR25 not in floors:
        floors.append(FLOOR25)
    obj.setdefault('compiler_contract', {})['deterministic_pipeline_non_inference'] = {
        'required': True,
        'core_patch_marker': 'AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1',
        'floor_invariant': FLOOR25,
        'execution_semantics': 'DETERMINISTIC_PIPELINE',
        'inference_policy': 'PROHIBITED',
        'step_order': 'STRICT',
        'missing_input_behavior': 'FAIL_CLOSED',
        'unknown_condition_behavior': 'FAIL_CLOSED',
        'conflict_behavior': 'FAIL_CLOSED',
        'cognitive_contamination_rule': 'MII_OR_OTHER_COGNITIVE_OUTPUT_MAY_ENTER_ONLY_AT_EXPLICIT_DECLARED_AND_VALIDATED_PIPELINE_INGESTION_STEP',
        'declared_runtime_routes': sorted(DETERMINISTIC_ROUTES),
        'non_inference_rule': 'Do not infer. Follow the declared deterministic pipeline.'
    }
    add_floor_to_lists(obj)
    dump(path, obj)
    return version


def patch_handoff(starter_version: str) -> None:
    path = ROOT / 'prompts' / 'AIR_HANDOFF_CARD_TEMPLATE.json'
    root = load(path)
    card = root['AIR_HANDOFF_CARD']
    sp = card['profile_stack']['starter_profile']
    sp['SYSTEM_DESIGNATION'] = 'AIR_DEFAULT_STARTER_V2'
    sp['PROMPT_VERSION'] = starter_version
    dump(path, root)


def route_line_numbers(core_text: str) -> dict[str, int]:
    lines = core_text.splitlines()
    out: dict[str, int] = {}
    for i, line in enumerate(lines):
        if line == '[AIR_ROUTE]':
            for j in range(i + 1, min(i + 8, len(lines))):
                if lines[j].startswith('id='):
                    out[lines[j].split('=', 1)[1].strip()] = i + 1
                    break
    return out


def patch_route_map() -> None:
    path = ROOT / 'catalog' / 'AIR_RUNTIME_ROUTE_MAP.json'
    obj = load(path)
    core_path = ROOT / 'prompts' / 'AIR_CORE_RUNTIME.md'
    obj['source_of_truth']['sha256'] = metadata(core_path)['sha256']
    rule = 'deterministic_pipeline_contract mirrors Core AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1; declared deterministic routes prohibit inference and fail closed on unresolved pipeline state.'
    if rule not in obj.setdefault('rules', []):
        obj['rules'].append(rule)
    obj['deterministic_pipeline_contract'] = {
        'core_patch_marker': 'AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1',
        'floor_invariant': FLOOR25,
        'execution_semantics': 'DETERMINISTIC_PIPELINE',
        'inference_policy': 'PROHIBITED',
        'step_order': 'STRICT',
        'missing_input_behavior': 'FAIL_CLOSED',
        'unknown_condition_behavior': 'FAIL_CLOSED',
        'conflict_behavior': 'FAIL_CLOSED',
        'declared_route_ids': sorted(DETERMINISTIC_ROUTES),
        'rule': 'Do not infer. Follow the declared deterministic pipeline. This metadata mirrors Core and has no independent semantic authority.'
    }
    line_map = route_line_numbers(core_path.read_text(encoding='utf-8'))
    for route in obj['routes']:
        rid = route['route_id']
        if rid in DETERMINISTIC_ROUTES:
            route['execution_semantics'] = 'DETERMINISTIC_PIPELINE'
            route['inference_policy'] = 'PROHIBITED'
            route['step_order'] = 'STRICT'
            route['missing_input_behavior'] = 'FAIL_CLOSED'
            route['unknown_condition_behavior'] = 'FAIL_CLOSED'
            route['conflict_behavior'] = 'FAIL_CLOSED'
            if FLOOR25 not in route.setdefault('does_not_bypass', []):
                route['does_not_bypass'].append(FLOOR25)
        for key in ['execution_semantics', 'inference_policy', 'step_order', 'missing_input_behavior', 'unknown_condition_behavior', 'conflict_behavior']:
            if rid not in DETERMINISTIC_ROUTES:
                route.pop(key, None)
        if rid in line_map and isinstance(route.get('source_anchor'), dict):
            route['source_anchor']['line'] = line_map[rid]
    dump(path, obj)


def patch_fixtures() -> None:
    path = ROOT / 'tests' / 'air_contract_fixtures.json'
    obj = load(path)
    obj['routine_boot_negative_cases'] = [
        {'id': 'RB-01-DISPLACED-TERMINAL-SENTINEL', 'invalid_if': 'a required markdown Foundation sentinel exists but is not the final content line'},
        {'id': 'RB-02-STARTER-SELF-VERSION-MISMATCH', 'invalid_if': 'AIR_DEFAULT_STARTER_PROFILE PROMPT_VERSION differs from validation_contract.required_version'},
        {'id': 'RB-03-HANDOFF-STARTER-VERSION-MISMATCH', 'invalid_if': 'Handoff profile_stack.starter_profile identity/version differs from the current Default Starter'}
    ]
    obj['deterministic_pipeline_negative_cases'] = [
        {'id': 'DP-01-MISSING-REQUIRED-INPUT', 'invalid_if': 'DETERMINISTIC_PIPELINE fills a missing required input by inference instead of FAIL_CLOSED or exact required-input request'},
        {'id': 'DP-02-REORDER-OR-SKIP', 'invalid_if': 'DETERMINISTIC_PIPELINE reorders, skips, optimizes away, or silently defaults a declared step'},
        {'id': 'DP-03-COGNITIVE-CONTAMINATION', 'invalid_if': 'MII, Specialist, heuristic, remembered, or contextual output fills a deterministic slot without an explicit declared ingestion and validation step'},
        {'id': 'DP-04-ROUTER-CONSEQUENCE-INVENTION', 'invalid_if': 'router/classifier identifies a condition but invents or substitutes the consequence instead of following the declared route table'}
    ]
    dump(path, obj)


def write_boot_validator() -> None:
    path = ROOT / 'tools' / 'validate_air_boot.py'
    content = r'''from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

class BootValidationError(Exception):
    pass

def reject_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in out:
            raise BootValidationError(f'duplicate JSON key: {k}')
        out[k] = v
    return out

def load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=reject_dupes)
    except Exception as exc:
        raise BootValidationError(f'{path}: strict JSON parse failed: {exc}') from exc

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise BootValidationError(msg)

def header_value(text: str, key: str) -> str:
    m = re.search(rf'(?m)^{re.escape(key)}:\s*(\S+)\s*$', text)
    if not m:
        raise BootValidationError(f'missing markdown header {key}')
    return m.group(1)

def main(root: Path) -> None:
    prompts = root / 'prompts'
    expected = {
        'AIR_CORE_RUNTIME.md': ('AIR_CORE_RUNTIME_V2', 'AIR_LOAD_SENTINEL :: AIR_CORE_RUNTIME :: END_OF_FILE :: LOAD_INTEGRITY_V2'),
        'AIR_CONTROL_SURFACE.md': ('AIR_CONTROL_SURFACE_V2', 'AIR_LOAD_SENTINEL :: AIR_CONTROL_SURFACE :: END_OF_FILE :: LOAD_INTEGRITY_V2'),
        'AIR_GOV.md': ('AIR_HR_GOVERNANCE_SUPPLEMENT_V2', 'AIR_LOAD_SENTINEL :: AIR_HR_GOVERNANCE_SUPPLEMENT :: END_OF_FILE :: LOAD_INTEGRITY_V2'),
    }
    markdown_versions: dict[str, str] = {}
    for name, (designation, sentinel) in expected.items():
        path = prompts / name
        require(path.is_file(), f'missing Foundation file {name}')
        text = path.read_text(encoding='utf-8')
        lines = text.rstrip().splitlines()
        require(bool(lines) and lines[-1] == sentinel, f'{name}: terminal sentinel is not the final content line')
        require(header_value(text, 'SYSTEM_DESIGNATION') == designation, f'{name}: designation mismatch')
        markdown_versions[name] = header_value(text, 'PROMPT_VERSION')
    starter = load(prompts / 'AIR_DEFAULT_STARTER_PROFILE.json')
    require(starter.get('SYSTEM_DESIGNATION') == 'AIR_DEFAULT_STARTER_V2', 'Starter designation mismatch')
    require(starter.get('canonical_role') == 'DEFAULT_STARTER_PROFILE', 'Starter canonical_role mismatch')
    require(starter.get('PROMPT_VERSION') == starter.get('validation_contract', {}).get('required_version'), 'Starter PROMPT_VERSION != validation_contract.required_version')
    dp = starter.get('compiler_contract', {}).get('deterministic_pipeline_non_inference', {})
    require(dp.get('required') is True and dp.get('inference_policy') == 'PROHIBITED', 'Starter deterministic-pipeline non-inference mirror missing')
    handoff_root = load(prompts / 'AIR_HANDOFF_CARD_TEMPLATE.json')
    card = handoff_root.get('AIR_HANDOFF_CARD', {})
    require(card.get('TEMPLATE_DESIGNATION') == 'AIR_HANDOFF_CARD_TEMPLATE_V2', 'Handoff designation mismatch')
    require(card.get('SCHEMA_VERSION') == card.get('schema_version') == '2.3.0', 'Handoff schema mismatch')
    restored = card.get('profile_stack', {}).get('starter_profile', {})
    require(restored.get('SYSTEM_DESIGNATION') == starter.get('SYSTEM_DESIGNATION'), 'Handoff Starter designation mismatch')
    require(restored.get('PROMPT_VERSION') == starter.get('PROMPT_VERSION'), 'Handoff Starter version mismatch')
    core = (prompts / 'AIR_CORE_RUNTIME.md').read_text(encoding='utf-8')
    require('Patch marker: AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1' in core, 'Core deterministic-pipeline law missing')
    require('AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE' in core, 'Core floor 025 missing')
    print('AIR routine boot consumer validation: PASS')
    print(f"Core={markdown_versions['AIR_CORE_RUNTIME.md']} Control={markdown_versions['AIR_CONTROL_SURFACE.md']} Starter={starter['PROMPT_VERSION']} Handoff={card['schema_version']} rev{card['card_revision']}")

if __name__ == '__main__':
    try:
        root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
        main(root)
    except BootValidationError as exc:
        raise SystemExit(f'AIR routine boot validation FAILED: {exc}')
'''
    path.write_text(content, encoding='utf-8')


def patch_release_validator() -> None:
    path = ROOT / 'tools' / 'validate_air_release.py'
    text = path.read_text(encoding='utf-8')
    text = text.replace("    require((ROOT / 'tools' / 'validate_air_release.py').is_file(), 'missing permanent validator')\n", "    require((ROOT / 'tools' / 'validate_air_release.py').is_file(), 'missing permanent validator')\n    require((ROOT / 'tools' / 'validate_air_boot.py').is_file(), 'missing independent routine-boot validator')\n    require((ROOT / 'tools' / 'test_air_validator_mutations.py').is_file(), 'missing validator mutation suite')\n", 1)
    anchor = "    require('Patch marker: AIR_CONTROL_CLOSED_WORLD_EMISSION_RENDERER_V1' in control, 'missing Control emission renderer closure')\n"
    block = anchor + "\n    gov = (ROOT / 'prompts' / 'AIR_GOV.md').read_text(encoding='utf-8')\n    expected_sentinels = {\n        'AIR_CORE_RUNTIME.md': 'AIR_LOAD_SENTINEL :: AIR_CORE_RUNTIME :: END_OF_FILE :: LOAD_INTEGRITY_V2',\n        'AIR_CONTROL_SURFACE.md': 'AIR_LOAD_SENTINEL :: AIR_CONTROL_SURFACE :: END_OF_FILE :: LOAD_INTEGRITY_V2',\n        'AIR_GOV.md': 'AIR_LOAD_SENTINEL :: AIR_HR_GOVERNANCE_SUPPLEMENT :: END_OF_FILE :: LOAD_INTEGRITY_V2',\n    }\n    for name, body in [('AIR_CORE_RUNTIME.md', core), ('AIR_CONTROL_SURFACE.md', control), ('AIR_GOV.md', gov)]:\n        lines = body.rstrip().splitlines()\n        require(bool(lines) and lines[-1] == expected_sentinels[name], f'{name}: terminal sentinel is not final content line')\n    require('Patch marker: AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1' in core, 'missing Core deterministic-pipeline non-inference law')\n    require('AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE' in core, 'missing Core floor 025')\n"
    if 'expected_sentinels = {' not in text:
        if anchor not in text:
            fail('release validator Control marker anchor missing')
        text = text.replace(anchor, block, 1)
    starter_anchor = "    require(starter.get('compiler_contract', {}).get('closed_world_emission_closure', {}).get('required') is True, 'Starter missing closed-world emission closure mirror')\n"
    starter_block = starter_anchor + "    require(starter.get('validation_contract', {}).get('required_version') == starter.get('PROMPT_VERSION'), 'Starter self-version mismatch')\n    require(FLOOR25 if False else True, '') if False else None\n    dp_starter = starter.get('compiler_contract', {}).get('deterministic_pipeline_non_inference', {})\n    require(dp_starter.get('required') is True, 'Starter missing deterministic-pipeline non-inference mirror')\n    require(dp_starter.get('inference_policy') == 'PROHIBITED', 'Starter deterministic pipeline inference policy mismatch')\n    require('AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE' in starter.get('authority_contract', {}).get('floor_invariants_required', []), 'Starter missing floor 025 requirement')\n"
    if 'dp_starter = starter.get' not in text:
        text = text.replace(starter_anchor, starter_block, 1)
    # remove intentionally unreachable placeholder if present
    text = text.replace("    require(FLOOR25 if False else True, '') if False else None\n", '')
    hand_anchor = "    require('runtime_drift_hardening_schema_extension' in declared, 'Handoff drift extension not declared')\n"
    hand_block = hand_anchor + "    restored_starter = handoff.get('profile_stack', {}).get('starter_profile', {})\n    require(restored_starter.get('SYSTEM_DESIGNATION') == starter.get('SYSTEM_DESIGNATION'), 'Handoff Starter designation mismatch')\n    require(restored_starter.get('PROMPT_VERSION') == starter.get('PROMPT_VERSION'), 'Handoff Starter version mismatch')\n"
    if 'restored_starter = handoff.get' not in text:
        text = text.replace(hand_anchor, hand_block, 1)
    route_anchor = "    require('AIR_PROJECT_EXECUTION_MAP' in routes['RT.TASK_SWITCH']['produces'] and 'AIR_ARTIFACT' in routes['RT.TASK_SWITCH']['produces'], 'RT.TASK_SWITCH emission closure incomplete')\n"
    route_block = route_anchor + "    deterministic_routes = {'RT.BOOT', 'RT.ONBOARD', 'RT.HANDOFF_RESTORE', 'RT.TURN', 'RT.ALIGN', 'RT.ACTION', 'RT.RECEIPT', 'RT.HANDOFF_CREATE'}\n    for rid in sorted(deterministic_routes):\n        require(rid in routes, f'missing deterministic Core route {rid}')\n        require(routes[rid].get('execution_semantics') == 'DETERMINISTIC_PIPELINE', f'{rid}: execution_semantics mismatch')\n        require(routes[rid].get('inference_policy') == 'PROHIBITED', f'{rid}: inference_policy mismatch')\n        require(routes[rid].get('step_order') == 'STRICT', f'{rid}: step_order mismatch')\n        for key in ['missing_input_behavior', 'unknown_condition_behavior', 'conflict_behavior']:\n            require(routes[rid].get(key) == 'FAIL_CLOSED', f'{rid}: {key} mismatch')\n        require('AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE' in routes[rid].get('does_not_bypass', ''), f'{rid}: floor 025 bypass protection missing')\n"
    if 'deterministic_routes = {' not in text:
        text = text.replace(route_anchor, route_block, 1)
    map_anchor = "    require('AIR_ARTIFACT' in route_map_by_id['RT.AMEND']['produces'], 'Route Map RT.AMEND stale')\n"
    map_block = map_anchor + "    dp_map = route_map.get('deterministic_pipeline_contract', {})\n    require(dp_map.get('core_patch_marker') == 'AIR_DETERMINISTIC_PIPELINE_NON_INFERENCE_V1', 'Route Map deterministic pipeline contract missing')\n    require(dp_map.get('inference_policy') == 'PROHIBITED', 'Route Map deterministic inference policy mismatch')\n    require(set(dp_map.get('declared_route_ids', [])) == deterministic_routes, 'Route Map deterministic route set mismatch')\n    for rid in sorted(deterministic_routes):\n        rr = route_map_by_id[rid]\n        require(rr.get('execution_semantics') == 'DETERMINISTIC_PIPELINE', f'Route Map {rid}: execution_semantics mismatch')\n        require(rr.get('inference_policy') == 'PROHIBITED', f'Route Map {rid}: inference_policy mismatch')\n        require(rr.get('step_order') == 'STRICT', f'Route Map {rid}: step_order mismatch')\n        for key in ['missing_input_behavior', 'unknown_condition_behavior', 'conflict_behavior']:\n            require(rr.get(key) == 'FAIL_CLOSED', f'Route Map {rid}: {key} mismatch')\n"
    if 'dp_map = route_map.get' not in text:
        text = text.replace(map_anchor, map_block, 1)
    fixture_anchor = "    require(len(fixtures.get('semantic_reseal_negative_cases', [])) >= 3, 'insufficient semantic reseal negative fixtures')\n"
    fixture_block = fixture_anchor + "    require(len(fixtures.get('routine_boot_negative_cases', [])) >= 3, 'insufficient routine boot negative fixtures')\n    require(len(fixtures.get('deterministic_pipeline_negative_cases', [])) >= 4, 'insufficient deterministic pipeline negative fixtures')\n"
    if "routine_boot_negative_cases" not in text:
        text = text.replace(fixture_anchor, fixture_block, 1)
    print_anchor = "    print('Handoff semantic card_revision receipts: PASS')\n"
    print_block = print_anchor + "    print('Routine boot coherence: PASS')\n    print('Deterministic pipeline non-inference contract: PASS')\n"
    if "print('Routine boot coherence: PASS')" not in text:
        text = text.replace(print_anchor, print_block, 1)
    path.write_text(text, encoding='utf-8')


def write_mutation_suite() -> None:
    path = ROOT / 'tools' / 'test_air_validator_mutations.py'
    content = r'''from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path('.').resolve()
BOOT = ROOT / 'tools' / 'validate_air_boot.py'
RELEASE = ROOT / 'tools' / 'validate_air_release.py'

def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def expect_fail(name: str, proc: subprocess.CompletedProcess[str], expected: str) -> None:
    if proc.returncode == 0:
        raise SystemExit(f'mutation {name} SURVIVED validator')
    if expected not in proc.stdout:
        raise SystemExit(f'mutation {name} failed for wrong reason; expected {expected!r}; output={proc.stdout!r}')
    print(f'{name}: KILLED')

def boot_mutation(name: str, mutator, expected: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        shutil.copytree(ROOT / 'prompts', t / 'prompts')
        mutator(t)
        p = run([sys.executable, str(BOOT), str(t)], ROOT)
        expect_fail(name, p, expected)

def full_mutation(name: str, mutator, expected: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        t = Path(td) / 'repo'
        shutil.copytree(ROOT, t, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
        mutator(t)
        p = run([sys.executable, 'tools/validate_air_release.py'], t)
        expect_fail(name, p, expected)

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

boot_mutation('RB-01-DISPLACED-TERMINAL-SENTINEL', displaced_sentinel, 'terminal sentinel is not the final content line')
boot_mutation('RB-02-STARTER-SELF-VERSION-MISMATCH', starter_self_version, 'Starter PROMPT_VERSION != validation_contract.required_version')
boot_mutation('RB-03-HANDOFF-STARTER-VERSION-MISMATCH', handoff_starter_version, 'Handoff Starter version mismatch')
full_mutation('DP-ROUTE-INFERENCE-POLICY', route_inference_policy, 'Route Map RT.BOOT: inference_policy mismatch')
print('AIR validator mutation suite: PASS (4/4 mutants killed)')
'''
    path.write_text(content, encoding='utf-8')


def recursive_refresh(obj: Any, owner_name: str, metas: dict[str, dict[str, Any]]) -> bool:
    changed = False
    if isinstance(obj, dict):
        ref = obj.get('filename') or obj.get('canonical_filename')
        if isinstance(ref, str) and ref in metas and ref != owner_name:
            m = metas[ref]
            for key in ['sha256', 'observed_sha256']:
                if key in obj and obj[key] != m['sha256']:
                    obj[key] = m['sha256']; changed = True
            if 'size_bytes' in obj and obj['size_bytes'] != m['size_bytes']:
                obj['size_bytes'] = m['size_bytes']; changed = True
            if 'line_count' in obj and obj['line_count'] != m['line_count']:
                obj['line_count'] = m['line_count']; changed = True
            if ref in FOUNDATION_VERSIONS and 'version' in obj and obj['version'] != FOUNDATION_VERSIONS[ref]:
                obj['version'] = FOUNDATION_VERSIONS[ref]; changed = True
            if ref == 'AIR_HANDOFF_CARD_TEMPLATE.json' and 'card_revision' in obj and obj['card_revision'] != 16:
                obj['card_revision'] = 16; changed = True
        if add_floor_to_lists(obj):
            changed = True
        for v in obj.values():
            if recursive_refresh(v, owner_name, metas):
                changed = True
    elif isinstance(obj, list):
        for v in obj:
            if recursive_refresh(v, owner_name, metas):
                changed = True
    return changed


def index_by_basename() -> dict[str, Path]:
    paths = [
        *(ROOT / 'prompts').glob('*'),
        *(ROOT / 'catalog').glob('*.json'),
        *(ROOT / 'profiles').glob('**/*.json'),
    ]
    out: dict[str, Path] = {}
    for p in paths:
        if p.is_file():
            if p.name in out:
                fail(f'duplicate basename {p.name}')
            out[p.name] = p
    return out


def current_metas() -> dict[str, dict[str, Any]]:
    return {name: metadata(path) for name, path in index_by_basename().items()}


def reseal_profiles_and_index() -> None:
    # First refresh Foundation/Route Map refs and floor requirements in non-manifest components.
    metas = current_metas()
    manifests: list[Path] = []
    for p in sorted((ROOT / 'profiles').glob('**/*.json')):
        obj = load(p)
        if p.name.endswith('PACKAGE_MANIFEST.json'):
            manifests.append(p)
            continue
        if recursive_refresh(obj, p.name, metas):
            dump(p, obj)

    # Then rebuild component metadata inside manifests using final component bytes.
    metas = current_metas()
    for p in manifests:
        obj = load(p)
        recursive_refresh(obj, p.name, metas)
        for c in obj.get('components', []):
            name = c.get('filename')
            if name in metas:
                c['sha256'] = metas[name]['sha256']
                c['size_bytes'] = metas[name]['size_bytes']
                c['line_count'] = metas[name]['line_count']
        dump(p, obj)

    # Refresh index against final manifest bytes and all live references.
    metas = current_metas()
    ip = ROOT / 'catalog' / 'AIR_SPECIALIST_PACKAGE_INDEX.json'
    idx = load(ip)
    recursive_refresh(idx, ip.name, metas)
    for entry in idx.get('entries', []):
        name = entry.get('manifest_filename')
        if name in metas:
            entry['manifest_sha256'] = metas[name]['sha256']
    dump(ip, idx)

    # One final live-reference pass over manifests/index after index serialization is not needed for self refs,
    # but manifests may reference freshly updated component bytes only; verify no additional mutation is required.


def assert_no_known_boot_defect() -> None:
    for name, sentinel in SENTINELS.items():
        text = (ROOT / 'prompts' / name).read_text(encoding='utf-8')
        if not text.rstrip().splitlines() or text.rstrip().splitlines()[-1] != sentinel:
            fail(f'{name} sentinel not terminal after patch')
    starter = load(ROOT / 'prompts' / 'AIR_DEFAULT_STARTER_PROFILE.json')
    if starter['PROMPT_VERSION'] != starter['validation_contract']['required_version']:
        fail('Starter self-version mismatch remains')
    handoff = load(ROOT / 'prompts' / 'AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']
    if handoff['profile_stack']['starter_profile']['PROMPT_VERSION'] != starter['PROMPT_VERSION']:
        fail('Handoff Starter version mismatch remains')


def main() -> None:
    if (ROOT / 'VERSION').read_text(encoding='utf-8').strip() != '0.7.1':
        fail('unexpected kit version')
    patch_core()
    patch_control()
    patch_governance()
    starter_version = patch_starter()
    patch_handoff(starter_version)
    patch_route_map()
    patch_fixtures()
    write_boot_validator()
    patch_release_validator()
    write_mutation_suite()
    reseal_profiles_and_index()
    assert_no_known_boot_defect()
    print('bounded routine-boot + deterministic-pipeline correction applied')
    print('deterministic routes:', ', '.join(sorted(DETERMINISTIC_ROUTES)))

if __name__ == '__main__':
    main()
