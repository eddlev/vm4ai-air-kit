from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path('.')
STARTER = Path('prompts/AIR_DEFAULT_STARTER_PROFILE.json')

class ContractValidationError(Exception):
    pass


def reject_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in out:
            raise ContractValidationError(f'duplicate JSON key: {k}')
        out[k] = v
    return out


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=reject_dupes)
    except Exception as exc:
        raise ContractValidationError(f'{path}: strict JSON parse failed: {exc}') from exc


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise ContractValidationError(msg)


def json_path_get(obj: Any, path: str) -> Any:
    if not isinstance(path, str) or not path.startswith('$.'):
        raise ContractValidationError(f'unsupported JSON path: {path!r}')
    cur = obj
    for part in path[2:].split('.'):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(path)
        cur = cur[part]
    return cur


def json_path_exists(obj: Any, path: str) -> bool:
    try:
        json_path_get(obj, path)
        return True
    except KeyError:
        return False


def header_value(text: str, key: str) -> str:
    m = re.search(rf'(?m)^{re.escape(key)}:\s*(\S+)\s*$', text)
    if not m:
        raise ContractValidationError(f'missing markdown header {key}')
    return m.group(1)


def abs_path(root: Path, rel: str) -> Path:
    p = root / rel
    return p


def json_value(root: Path, spec: dict[str, Any]) -> Any:
    path = abs_path(root, spec['file'])
    require(path.is_file(), f'missing referenced file {spec["file"]}')
    return json_path_get(load_json(path), spec['path'])


def markdown_header(root: Path, spec: dict[str, Any]) -> str:
    path = abs_path(root, spec['file'])
    require(path.is_file(), f'missing referenced file {spec["file"]}')
    return header_value(path.read_text(encoding='utf-8'), spec['header'])


IMPLEMENTED_OPERATORS = {
    'FILE_EXISTS',
    'MARKDOWN_HEADER_EQUALS_LITERAL',
    'MARKDOWN_FINAL_LINE_EQUALS_LITERAL',
    'JSON_EQUALS_LITERAL',
    'JSON_EQUALS_REFERENCE',
    'JSON_EQUALS_MARKDOWN_HEADER',
    'JSON_ROOT_KEYS_DECLARED_BY_MANIFEST',
    'JSON_ARRAY_CONTAINS_LITERAL',
    'JSON_PATH_ABSENT',
    'JSON_SUBTREE_TEXT_NOT_CONTAINS_LITERAL',
    'TEXT_CONTAINS_LITERAL',
    'TEXT_NOT_CONTAINS_LITERAL',
}


def execute_check(root: Path, check: dict[str, Any]) -> None:
    cid = check['check_id']
    op = check['operator']
    require(check.get('on_failure') == 'FAIL_CLOSED', f'{cid}: on_failure must be FAIL_CLOSED')
    require(op in IMPLEMENTED_OPERATORS, f'{cid}: unknown deterministic contract operator {op}')

    if op == 'FILE_EXISTS':
        require(abs_path(root, check['file']).is_file(), f'{cid}: required file missing: {check["file"]}')
    elif op == 'MARKDOWN_HEADER_EQUALS_LITERAL':
        path = abs_path(root, check['file'])
        actual = header_value(path.read_text(encoding='utf-8'), check['header'])
        require(actual == check['expected'], f'{cid}: header {check["header"]} mismatch: {actual!r} != {check["expected"]!r}')
    elif op == 'MARKDOWN_FINAL_LINE_EQUALS_LITERAL':
        path = abs_path(root, check['file'])
        lines = path.read_text(encoding='utf-8').rstrip().splitlines()
        actual = lines[-1] if lines else None
        require(actual == check['expected'], f'{cid}: final content line mismatch')
    elif op == 'JSON_EQUALS_LITERAL':
        actual = json_value(root, check['left'])
        require(actual == check['expected'], f'{cid}: value mismatch: {actual!r} != {check["expected"]!r}')
    elif op == 'JSON_EQUALS_REFERENCE':
        left = json_value(root, check['left'])
        right = json_value(root, check['right'])
        require(left == right, f'{cid}: reference mismatch: {left!r} != {right!r}')
    elif op == 'JSON_EQUALS_MARKDOWN_HEADER':
        left = json_value(root, check['left'])
        right = markdown_header(root, check['right'])
        require(left == right, f'{cid}: JSON/header mismatch: {left!r} != {right!r}')
    elif op == 'JSON_ROOT_KEYS_DECLARED_BY_MANIFEST':
        obj = load_json(abs_path(root, check['file']))
        root_obj = json_path_get(obj, check['root_path'])
        required = json_path_get(obj, check['required_path'])
        optional = json_path_get(obj, check['optional_path'])
        require(isinstance(root_obj, dict) and isinstance(required, list) and isinstance(optional, list), f'{cid}: invalid manifest closure operands')
        declared = set(required) | set(optional)
        unknown = sorted(set(root_obj) - declared)
        require(not unknown, f'{cid}: undeclared root fields: {unknown}')
    elif op == 'JSON_ARRAY_CONTAINS_LITERAL':
        actual = json_value(root, check['left'])
        require(isinstance(actual, list), f'{cid}: expected array operand')
        require(check['expected'] in actual, f'{cid}: array missing required literal {check["expected"]!r}')
    elif op == 'JSON_SUBTREE_TEXT_NOT_CONTAINS_LITERAL':
        actual = json_value(root, check['left'])
        rendered = json.dumps(actual, ensure_ascii=False)
        require(check['expected'] not in rendered, f'{cid}: forbidden duplicated/stale text remains in subtree: {check["expected"]!r}')
    elif op == 'JSON_PATH_ABSENT':
        path = abs_path(root, check['left']['file'])
        obj = load_json(path)
        require(not json_path_exists(obj, check['left']['path']), f'{cid}: forbidden duplicate path exists: {check["left"]["path"]}')
    elif op == 'TEXT_CONTAINS_LITERAL':
        text = abs_path(root, check['file']).read_text(encoding='utf-8')
        require(check['expected'] in text, f'{cid}: required text marker missing: {check["expected"]!r}')
    elif op == 'TEXT_NOT_CONTAINS_LITERAL':
        text = abs_path(root, check['file']).read_text(encoding='utf-8')
        require(check['expected'] not in text, f'{cid}: forbidden duplicated/stale text remains: {check["expected"]!r}')


def main(root: Path) -> None:
    starter_path = root / STARTER
    starter = load_json(starter_path)
    vc = starter.get('validation_contract', {})
    registry = vc.get('deterministic_contract_registry')
    require(isinstance(registry, dict), 'missing validation_contract.deterministic_contract_registry')
    require(registry.get('execution_semantics') == 'DETERMINISTIC_PIPELINE', 'registry execution_semantics mismatch')
    require(registry.get('inference_policy') == 'PROHIBITED', 'registry inference_policy mismatch')
    require(registry.get('prose_authority') == 'NON_OPERATIVE_DESCRIPTION', 'registry prose authority mismatch')
    checks = registry.get('checks')
    require(isinstance(checks, list) and checks, 'deterministic contract registry checks missing')
    require(all(isinstance(c, dict) for c in checks), 'operative deterministic registry contains free-form predicate')
    ids = [c.get('check_id') for c in checks]
    require(all(isinstance(x, str) and x for x in ids), 'deterministic check missing check_id')
    require(len(ids) == len(set(ids)), 'duplicate deterministic check_id')

    cov = registry.get('coverage_contract', {})
    declared = len(checks)
    unknown = [(c.get('check_id'), c.get('operator')) for c in checks if c.get('operator') not in IMPLEMENTED_OPERATORS]
    require(not unknown, f'unknown deterministic contract operator(s): {unknown}')
    implemented = sum(1 for c in checks if c.get('operator') in IMPLEMENTED_OPERATORS)
    require(cov.get('declared_check_count') == declared, f'coverage declared_check_count mismatch: {cov.get("declared_check_count")} != {declared}')
    require(cov.get('implemented_check_count_required') == declared, 'coverage implemented_check_count_required mismatch')
    require(cov.get('executed_check_count_required') == declared, 'coverage executed_check_count_required mismatch')
    for key in ['unimplemented_allowed','unexecuted_allowed','duplicate_check_ids_allowed','unknown_operators_allowed']:
        require(cov.get(key) == 0, f'coverage {key} must be 0')
    require(implemented == declared, f'deterministic contract implementation coverage incomplete: {implemented}/{declared}')

    executed = 0
    for check in checks:
        try:
            execute_check(root, check)
        except KeyError as exc:
            raise ContractValidationError(f"{check['check_id']}: unresolved deterministic reference {exc}") from exc
        except ContractValidationError as exc:
            msg = str(exc)
            if check['check_id'] not in msg:
                raise ContractValidationError(f"{check['check_id']}: {msg}") from exc
            raise
        executed += 1
    require(executed == declared, f'deterministic contract execution coverage incomplete: {executed}/{declared}')

    # Free-form validation expectations are permitted only as explicitly non-operative descriptions.
    expectations = vc.get('validation_expectations', [])
    require(isinstance(expectations, list), 'validation_expectations must be an array')
    for item in expectations:
        require(isinstance(item, dict), 'validation_expectation must be typed object')
        require(item.get('authority') == 'NON_OPERATIVE_DESCRIPTION', f'{item.get("expectation_id")}: validation expectation gained operative authority')

    print('AIR deterministic contract registry validation: PASS')
    print(f'Registered deterministic checks: {declared}')
    print(f'Implemented deterministic checks: {implemented}/{declared}')
    print(f'Executed deterministic checks: {executed}/{declared}')
    print('Unimplemented: 0')
    print('Unexecuted: 0')

if __name__ == '__main__':
    try:
        root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
        main(root)
    except (ContractValidationError, KeyError) as exc:
        raise SystemExit(f'AIR deterministic contract registry validation FAILED: {exc}')
