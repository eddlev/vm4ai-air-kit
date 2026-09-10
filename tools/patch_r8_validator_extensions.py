from __future__ import annotations
from pathlib import Path


def replace_once_or_present(path: Path, old: str, new: str, label: str) -> None:
    s=path.read_text(encoding='utf-8')
    if new in s:
        return
    if old not in s:
        raise SystemExit(f'R8 validator extension {label}: anchor missing')
    path.write_text(s.replace(old,new,1),encoding='utf-8')

boot=Path('tools/validate_air_boot.py')
import_old="from validate_air_r1_remediation import E as R1ValidationError, eval_registry\n"
replace_once_or_present(boot,import_old,import_old+"from validate_air_r8_remediation import E as R8ValidationError, main as validate_r8\n",'boot import')
old="    require(len(starter.get('authority_contract', {}).get('required_files', [])) == 5, 'R1 Foundation authority manifest must contain five roles')\n    print('AIR routine boot consumer validation: PASS')\n"
new="    require(len(starter.get('authority_contract', {}).get('required_files', [])) == 5, 'R1 Foundation authority manifest must contain five roles')\n    try:\n        validate_r8(root)\n    except (R8ValidationError, KeyError, ValueError) as exc:\n        raise BootValidationError(f'R8 presentation/portability boot check failed: {exc}') from exc\n    print('AIR routine boot consumer validation: PASS')\n"
replace_once_or_present(boot,old,new,'boot call')

release=Path('tools/validate_air_release.py')
import_old="from typing import Any\n"
replace_once_or_present(release,import_old,import_old+"from validate_air_r8_remediation import E as R8ValidationError, main as validate_r8\n",'release import')
old="    require((ROOT / 'VERSION').read_text(encoding='utf-8').strip() == EXPECTED_KIT_VERSION, 'VERSION mismatch')\n"
new=old+"    try:\n        validate_r8(ROOT.resolve())\n    except (R8ValidationError, KeyError, ValueError) as exc:\n        raise ValidationError(f'R8 presentation/portability release check failed: {exc}') from exc\n"
replace_once_or_present(release,old,new,'release call')

suite=Path('tools/validate_air_suite.py')
old="    run_stage('r7_lifecycle_version_history_reseal', [py, 'tools/validate_air_r7_remediation.py'])\n    run_stage('routine_boot', [py, 'tools/validate_air_boot.py'])\n"
new="    run_stage('r7_lifecycle_version_history_reseal', [py, 'tools/validate_air_r7_remediation.py'])\n    run_stage('r8_low_risk_presentation_portability', [py, 'tools/validate_air_r8_remediation.py'])\n    run_stage('routine_boot', [py, 'tools/validate_air_boot.py'])\n"
replace_once_or_present(suite,old,new,'suite validation stage')
old="        run_stage('r7_lifecycle_version_history_reseal_mutations', [py, 'tools/test_air_r7_mutations.py', '.', 'tools/validate_air_r7_remediation.py'])\n        run_stage('behavioral_transaction_mutations', [py, 'tools/test_air_behavioral_contract_mutations.py'])\n"
new="        run_stage('r7_lifecycle_version_history_reseal_mutations', [py, 'tools/test_air_r7_mutations.py', '.', 'tools/validate_air_r7_remediation.py'])\n        run_stage('r8_low_risk_presentation_portability_mutations', [py, 'tools/test_air_r8_mutations.py', '.', 'tools/validate_air_r8_remediation.py'])\n        run_stage('behavioral_transaction_mutations', [py, 'tools/test_air_behavioral_contract_mutations.py'])\n"
replace_once_or_present(suite,old,new,'suite mutation stage')

mut=Path('tools/test_air_validator_mutations.py')
s=mut.read_text(encoding='utf-8')
if "PASS (12/12 mutants killed)" not in s:
    old="print('AIR validator mutation suite: PASS (8/8 mutants killed)')\n"
    if old not in s: raise SystemExit('R8 validator extension generic mutation anchor missing')
    extra=r'''
def r8_control_boot_owner(t: Path) -> None:
    p=t/'prompts'/'AIR_CONTROL_SURFACE.md'; x=p.read_text(encoding='utf-8')
    x=x.replace('patch marker AIR_BOOT_BRAND_MARK_M2','patch marker BROKEN_BOOT_OWNER',1); p.write_text(x,encoding='utf-8')

def r8_q1d_four_modifier_help(t: Path) -> None:
    p=t/'prompts'/'AIR_CORE_RUNTIME.md'; x=p.read_text(encoding='utf-8')
    x=x.replace('explain all four canonical system modifiers','explain only the two system modifiers',1); p.write_text(x,encoding='utf-8')

def r8_starter_normalization_form(t: Path) -> None:
    p=t/'prompts'/'AIR_DEFAULT_STARTER_PROFILE.json'; o=json.loads(p.read_text(encoding='utf-8'))
    o['local_profile_policies']['file_identity_and_delivery']['unicode_normalization_form']='NFC'
    p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def r8_handoff_unknown_target_policy(t: Path) -> None:
    p=t/'prompts'/'AIR_HANDOFF_CARD_TEMPLATE.json'; o=json.loads(p.read_text(encoding='utf-8'))
    o['AIR_HANDOFF_CARD']['platform_state']['unknown_target_platform_behavior']='INFER_PLATFORM'
    p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

boot_mutation('R8-GEN-01-CONTROL-BOOT-MARK-OWNER', r8_control_boot_owner, 'R8 presentation/portability boot check failed')
boot_mutation('R8-GEN-02-Q1D-FOUR-MODIFIER-HELP', r8_q1d_four_modifier_help, 'R8 presentation/portability boot check failed')
boot_mutation('R8-GEN-03-STARTER-UNICODE-NORMALIZATION-FORM', r8_starter_normalization_form, 'R8 presentation/portability boot check failed')
boot_mutation('R8-GEN-04-HANDOFF-UNKNOWN-TARGET-POLICY', r8_handoff_unknown_target_policy, 'R8 presentation/portability boot check failed')
print('AIR validator mutation suite: PASS (12/12 mutants killed)')
'''
    mut.write_text(s.replace(old,extra,1),encoding='utf-8')

print('R8 boot/release/suite/generic-mutation validator extensions applied')
