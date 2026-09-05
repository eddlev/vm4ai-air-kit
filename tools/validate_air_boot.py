from __future__ import annotations

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
