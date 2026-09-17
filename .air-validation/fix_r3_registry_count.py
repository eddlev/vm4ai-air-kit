from pathlib import Path
p=Path('tools/validate_air_r3_remediation.py')
t=p.read_text(encoding='utf-8')
old="req(len(starter['validation_contract']['deterministic_contract_registry']['checks'])==90,'R1 registry lost')"
new="req(len(starter['validation_contract']['deterministic_contract_registry']['checks'])==102,'R1 registry lost')"
if t.count(old)!=1:
    raise SystemExit(f'R3 registry carry-forward anchor count {t.count(old)} != 1')
p.write_text(t.replace(old,new,1),encoding='utf-8')
print('R3 deterministic-registry carry-forward: 90 -> 102 PASS')
