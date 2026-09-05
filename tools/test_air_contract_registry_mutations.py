from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path('.').resolve()
VALIDATOR = ROOT / 'tools' / 'validate_air_contract_registry.py'
STARTER = Path('prompts/AIR_DEFAULT_STARTER_PROFILE.json')


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(VALIDATOR), str(root)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def copy_prompts() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    td = tempfile.TemporaryDirectory()
    t = Path(td.name)
    shutil.copytree(ROOT / 'prompts', t / 'prompts')
    return td, t


def mutate_check(check: dict, root: Path) -> None:
    op = check['operator']
    if op == 'FILE_EXISTS':
        check['file'] = 'prompts/__MISSING_CONTRACT_MUTANT__'
    elif op in {'MARKDOWN_HEADER_EQUALS_LITERAL','MARKDOWN_FINAL_LINE_EQUALS_LITERAL','JSON_EQUALS_LITERAL','JSON_ARRAY_CONTAINS_LITERAL','TEXT_CONTAINS_LITERAL'}:
        check['expected'] = '__AIR_CONTRACT_MUTANT_IMPOSSIBLE__'
    elif op == 'JSON_EQUALS_REFERENCE':
        check['right']['path'] = '$.__AIR_CONTRACT_MUTANT_MISSING__'
    elif op == 'JSON_EQUALS_MARKDOWN_HEADER':
        check['right']['header'] = '__AIR_CONTRACT_MUTANT_MISSING__'
    elif op == 'JSON_ROOT_KEYS_DECLARED_BY_MANIFEST':
        check['required_path'] = '$.__AIR_CONTRACT_MUTANT_MISSING__'
    elif op == 'JSON_SUBTREE_TEXT_NOT_CONTAINS_LITERAL':
        check['expected'] = 'NON_OPERATIVE_DESCRIPTION'
    elif op == 'JSON_PATH_ABSENT':
        file = check['left']['file']
        if file.endswith('AIR_HANDOFF_CARD_TEMPLATE.json'):
            check['left']['path'] = '$.AIR_HANDOFF_CARD.schema_version'
        else:
            check['left']['path'] = '$.PROMPT_VERSION'
    elif op == 'TEXT_NOT_CONTAINS_LITERAL':
        p = root / check['file']
        first = next((line for line in p.read_text(encoding='utf-8').splitlines() if line.strip()), '')
        check['expected'] = first
    else:
        raise RuntimeError(f'no mutation strategy for {op}')


def expect_specific_fail(cid: str, proc: subprocess.CompletedProcess[str]) -> None:
    if proc.returncode == 0:
        raise SystemExit(f'contract mutation {cid} SURVIVED')
    if cid not in proc.stdout:
        raise SystemExit(f'contract mutation {cid} failed without identifying its check; output={proc.stdout!r}')
    print(f'{cid}: KILLED')


def main() -> None:
    source = load(ROOT / STARTER)
    checks = source['validation_contract']['deterministic_contract_registry']['checks']
    killed = 0
    for src in checks:
        td, t = copy_prompts()
        try:
            starter = load(t / STARTER)
            target = next(c for c in starter['validation_contract']['deterministic_contract_registry']['checks'] if c['check_id'] == src['check_id'])
            mutate_check(target, t)
            save(t / STARTER, starter)
            proc = run(t)
            expect_specific_fail(src['check_id'], proc)
            killed += 1
        finally:
            td.cleanup()

    # Meta-mutant: unknown operator must fail closed.
    td, t = copy_prompts()
    try:
        starter = load(t / STARTER)
        starter['validation_contract']['deterministic_contract_registry']['checks'][0]['operator'] = 'INFER_THIS_RULE'
        save(t / STARTER, starter)
        proc = run(t)
        if proc.returncode == 0 or 'unknown deterministic contract operator' not in proc.stdout:
            raise SystemExit(f'DCR-META-UNKNOWN-OPERATOR not killed; output={proc.stdout!r}')
        print('DCR-META-UNKNOWN-OPERATOR: KILLED')
    finally:
        td.cleanup()

    # Meta-mutant: coverage count mismatch must fail before execution claim.
    td, t = copy_prompts()
    try:
        starter = load(t / STARTER)
        starter['validation_contract']['deterministic_contract_registry']['coverage_contract']['declared_check_count'] += 1
        save(t / STARTER, starter)
        proc = run(t)
        if proc.returncode == 0 or 'coverage declared_check_count mismatch' not in proc.stdout:
            raise SystemExit(f'DCR-META-COVERAGE not killed; output={proc.stdout!r}')
        print('DCR-META-COVERAGE: KILLED')
    finally:
        td.cleanup()

    print(f'AIR deterministic contract mutation suite: PASS ({killed}/{len(checks)} registered checks killed + 2 meta-mutants)')

if __name__ == '__main__':
    main()
