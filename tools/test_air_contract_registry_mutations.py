from __future__ import annotations
import json, shutil, tempfile
from pathlib import Path
from validate_air_r1_remediation import E, load as strict_load, eval_registry

ROOT=Path('.').resolve(); STARTER=Path('prompts/AIR_DEFAULT_STARTER_PROFILE.json')
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def temp_prompts():
    td=tempfile.TemporaryDirectory(); t=Path(td.name); shutil.copytree(ROOT/'prompts',t/'prompts'); return td,t

def mutate_check(c:dict,t:Path):
    op=c['operator']
    if op=='FILE_EXISTS': c['file']='prompts/__MISSING_CONTRACT_MUTANT__'
    elif op in {'MARKDOWN_HEADER_EQUALS_LITERAL','MARKDOWN_FINAL_LINE_EQUALS_LITERAL','JSON_EQUALS_LITERAL','JSON_ARRAY_CONTAINS_LITERAL','TEXT_CONTAINS_LITERAL'}: c['expected']='__AIR_CONTRACT_MUTANT_IMPOSSIBLE__'
    elif op=='MARKDOWN_HEADER_EQUALS_REGISTRY_VALUE': c['registry_value_path']='$.validation_contract.deterministic_contract_registry.foundation_prompt_version_contract.__MISSING__'
    elif op=='JSON_EQUALS_REFERENCE': c['right']['path']='$.__AIR_CONTRACT_MUTANT_MISSING__'
    elif op=='JSON_EQUALS_MARKDOWN_HEADER': c['right']['header']='__AIR_CONTRACT_MUTANT_MISSING__'
    elif op=='JSON_ROOT_KEYS_DECLARED_BY_MANIFEST': c['required_path']='$.__AIR_CONTRACT_MUTANT_MISSING__'
    elif op=='JSON_SUBTREE_TEXT_NOT_CONTAINS_LITERAL': c['expected']='NON_OPERATIVE_DESCRIPTION'
    elif op=='JSON_PATH_ABSENT':
        if c['left']['file'].endswith('AIR_HANDOFF_CARD_TEMPLATE.json'):
            c['left']['path']='$.AIR_HANDOFF_CARD.schema_version'
        else:
            c['left']['path']='$.PROMPT_VERSION'
    elif op=='TEXT_NOT_CONTAINS_LITERAL':
        p=t/c['file']; c['expected']=next(x for x in p.read_text(encoding='utf-8').splitlines() if x.strip())
    elif op=='STRICT_JSON_PARSE_NO_DUPLICATES':
        bad=t/'prompts/__AIR_DUPLICATE_MUTANT__.json'; bad.write_text('{"x":1,"x":2}\n',encoding='utf-8'); c['file']='prompts/__AIR_DUPLICATE_MUTANT__.json'
    elif op=='FOUNDATION_MANIFEST_EXACT': c['manifest_path']='$.__AIR_CONTRACT_MUTANT_MISSING__'
    elif op=='FOUNDATION_FILENAME_COLLISION_FREE': (t/'prompts/air_core_runtime.md').write_text('collision mutant\n',encoding='utf-8')
    else: raise RuntimeError(f'no mutation strategy for {op}')

def expect_fail(cid,t):
    try:
        starter=strict_load(t/STARTER); eval_registry(t,starter)
    except (E,KeyError) as exc:
        msg=str(exc)
        if cid not in msg: raise SystemExit(f'{cid}: failed without check id; {msg!r}')
        print(f'{cid}: KILLED'); return
    raise SystemExit(f'{cid}: mutation SURVIVED')

def main():
    source=load(ROOT/STARTER); checks=source['validation_contract']['deterministic_contract_registry']['checks']; killed=0
    for src in checks:
        td,t=temp_prompts()
        try:
            starter=load(t/STARTER); c=next(x for x in starter['validation_contract']['deterministic_contract_registry']['checks'] if x['check_id']==src['check_id'])
            mutate_check(c,t); save(t/STARTER,starter); expect_fail(src['check_id'],t); killed+=1
        finally: td.cleanup()
    td,t=temp_prompts()
    try:
        starter=load(t/STARTER); starter['validation_contract']['deterministic_contract_registry']['checks'][0]['operator']='INFER_THIS_RULE'; save(t/STARTER,starter)
        try: eval_registry(t,strict_load(t/STARTER)); raise SystemExit('DCR-META-UNKNOWN-OPERATOR survived')
        except E as exc:
            if 'unsupported operator' not in str(exc): raise
            print('DCR-META-UNKNOWN-OPERATOR: KILLED')
    finally: td.cleanup()
    td,t=temp_prompts()
    try:
        starter=load(t/STARTER); starter['validation_contract']['deterministic_contract_registry']['coverage_contract']['declared_check_count']+=1; save(t/STARTER,starter)
        try: eval_registry(t,strict_load(t/STARTER)); raise SystemExit('DCR-META-COVERAGE survived')
        except E as exc:
            if 'declared registry count mismatch' not in str(exc): raise
            print('DCR-META-COVERAGE: KILLED')
    finally: td.cleanup()
    print(f'AIR deterministic contract mutation suite: PASS ({killed}/{len(checks)} registered checks killed + 2 meta-mutants)')
if __name__=='__main__': main()
