from __future__ import annotations
import json, sys
from pathlib import Path

PROFILE='AIR_TARGET_PLATFORM_NORMALIZATION_PORTABLE_V1'
UNKNOWN='APPLY_PORTABLE_PROFILE_FAIL_CLOSED_ON_UNAVAILABLE_STRICTER_TARGET_RULE'
RESERVED=['CON','PRN','AUX','NUL']+[f'COM{i}' for i in range(1,10)]+[f'LPT{i}' for i in range(1,10)]

def replace_once(text: str, old: str, new: str, label: str) -> str:
    old_n=text.count(old); new_n=text.count(new)
    if old_n == 1 and new_n == 0:
        return text.replace(old,new,1)
    if old_n == 0 and new_n == 1:
        return text
    raise SystemExit(f'R8 patch {label}: expected one old or one new block, got old={old_n} new={new_n}')

def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def dump(path: Path, obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def main(root: Path):
    core_p=root/'prompts/AIR_CORE_RUNTIME.md'
    control_p=root/'prompts/AIR_CONTROL_SURFACE.md'
    starter_p=root/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'
    handoff_p=root/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'

    core=core_p.read_text(encoding='utf-8')
    core=replace_once(core,
'''Expected markdown sentinels:
- AIR_CORE_RUNTIME.md ends with:
- AIR_CONTROL_SURFACE.md ends with:
  AIR_LOAD_SENTINEL :: AIR_CONTROL_SURFACE :: END_OF_FILE :: LOAD_INTEGRITY_V2
- AIR_GOV.md ends with:
  AIR_LOAD_SENTINEL :: AIR_HR_GOVERNANCE_SUPPLEMENT :: END_OF_FILE :: LOAD_INTEGRITY_V2
''',
'''Expected Markdown sentinel literals are owned by the Default Starter typed deterministic registry; this prose does not duplicate them:
- AIR_CORE_RUNTIME.md -> AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-CORE].expected
- AIR_CONTROL_SURFACE.md -> AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-CONTROL].expected
- AIR_GOV.md -> AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-GOV].expected
The referenced typed expectation must resolve before comparison, and the resolved literal must still be the final content line of its Markdown file.
''','core sentinel declaration')

    core=replace_once(core,
'''Normalized collision check:
Before boot, binding, validation, packaging, handoff, or delivery, compute and compare at least:
1. raw basename
2. percent-decoded basename
3. Unicode-normalized basename
4. case-folded basename
5. target-platform-normalized basename
''',
'''Normalized collision check:
Canonical portable normalization contract:
- Unicode normalization form: NFKC.
- target-platform normalization profile: AIR_TARGET_PLATFORM_NORMALIZATION_PORTABLE_V1.
- portable collision-key sequence: percent-decode the basename once, normalize with Unicode NFKC, case-fold, then trim trailing ASCII space or period.
- portable invalid-name guard: reject an empty normalized basename, path separators, control characters, and case-insensitive reserved device stems CON, PRN, AUX, NUL, COM1-COM9, and LPT1-LPT9 whether bare or followed by an extension.
- when target_platform is null or unknown, apply AIR_TARGET_PLATFORM_NORMALIZATION_PORTABLE_V1 and do not infer a more permissive platform.
- when a known target requires stricter filename rules, apply them in addition to the portable profile; if the required stricter target rule/profile is unavailable, fail closed for binding, packaging, handoff, or delivery.
- target-specific rules may narrow acceptance but may not weaken this portable baseline.

Before boot, binding, validation, packaging, handoff, or delivery, compute and compare at least:
1. raw basename
2. percent-decoded basename
3. Unicode-NFKC-normalized basename
4. case-folded basename
5. AIR_TARGET_PLATFORM_NORMALIZATION_PORTABLE_V1 basename
''','core normalization contract')

    core=replace_once(core,
'''9. explain only the two system modifiers:
   - air -o on: show every generated AIR object
   - air -o -min: show only required AIR objects
10. offer an optional, dynamically generated example AIR project
''',
'''9. explain all four canonical system modifiers, distinguishing the two independent families:
   - air -o on: show every generated AIR object
   - air -o -min: show only required AIR objects
   - air -t on: use expanded evidence presentation/packages for subsequent runs
   - air -t off: use standard evidence presentation; default
   `-o` changes AIR object visibility only; `-t` changes evidence presentation/packaging only and never changes evidence obligations.
10. offer an optional, dynamically generated example AIR project
''','core Q1D modifier help')
    core_p.write_text(core,encoding='utf-8')

    control=control_p.read_text(encoding='utf-8')
    control=replace_once(control,
'''This file participates in Runtime Load Integrity.
Its terminal sentinel is:


At boot or continuation restoration, AIR must:
''',
'''This file participates in Runtime Load Integrity.
Its expected terminal sentinel is owned by AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-CONTROL].expected.
This surface does not duplicate a second sentinel literal; resolve that typed expectation and compare it to the actual final content line.

At boot or continuation restoration, AIR must:
''','control sentinel declaration')
    control=replace_once(control,
'''When the boot validation passed and the run is not an explicitly approved degraded run, print the fixed AIR boot mark immediately after the welcome and before Q1, in a monospaced context:

      ╌╌╌╌╌╌╌╌╌╌╌
━━━━━━━━●━━━━━━━━━━━    A I R
   ╌╌╌╌╌╌╌╌╌╌╌╌╌

If U+254C dashed rails do not render reliably, use the fixed ASCII fallback instead:

   - - - - - - - -
  =========o=========    A I R
    - - - - - - -
''',
'''When boot validation passed and the run is not an explicitly approved degraded run, render the Core-owned canonical AIR boot brand mark exactly as defined by AIR_CORE_RUNTIME_V2 section `AIR BOOT BRAND MARK LAW` (patch marker AIR_BOOT_BRAND_MARK_M2), immediately after the welcome and before Q1 in a monospaced context.
Control defines no second boot-mark glyph sequence. Use Core's exact canonical Unicode mark; when rendering is limited, use Core's exact ASCII fallback. Do not synthesize, rebalance, or locally substitute either literal.
''','control boot mark source')
    control=replace_once(control,
'''Color applies only to symbol + label and is never semantic authority. Ember is reserved for SEM_ACTIVE and active-dot identity elements. The full boot mark, when color is available, uses Brass for the heavy rail and `A I R`, Ember for the active dot, and muted foreground for dashed rails. Do not recolor the boot mark outside this palette.
''',
'''Color applies only to symbol + label and is never semantic authority. Ember is reserved for SEM_ACTIVE and active-dot identity elements. The Core-owned boot mark may receive color only as a non-semantic renderer overlay that preserves every canonical Core glyph byte-for-byte; it must never introduce local rail, label, or glyph variants.
''','control boot color wording')
    control=replace_once(control,
'''The full three-line boot mark appears only after passed boot validation at the fresh boot moment. It is never used as decoration on documents, posts, headers, dividers, partial output, or explicitly approved degraded runs. The one-line signature `━━━━━━●━━━  AIR` remains available for README/footer/handoff contexts when AIR context is established.
''',
'''The Core-owned canonical boot mark appears only after passed boot validation at the fresh boot moment. It is never used as decoration on documents, posts, headers, dividers, partial output, or explicitly approved degraded runs. The separate one-line signature `━━━━━━●━━━  AIR` remains available for README/footer/handoff contexts when AIR context is established and must not be substituted for the boot mark.
''','control negative-space wording')
    control_p.write_text(control,encoding='utf-8')

    starter=load(starter_p)
    fid=starter['local_profile_policies']['file_identity_and_delivery']
    fid['unicode_normalization_form']='NFKC'
    fid['target_platform_normalization_profile']=PROFILE
    fid['unknown_target_platform_behavior']=UNKNOWN
    fid['platform_reserved_basename_policy']='REJECT_PORTABLE_DEVICE_STEMS_CASE_INSENSITIVE_WITH_OR_WITHOUT_EXTENSION'
    check=next(c for c in starter['validation_contract']['deterministic_contract_registry']['checks'] if c['check_id']=='DC-FOUNDATION-NORMALIZED-COLLISION')
    check['unicode_normalization_form']='NFKC'
    check['target_platform_normalization_profile']=PROFILE
    check['unknown_target_platform_behavior']=UNKNOWN
    check['portable_reserved_basename_stems']=RESERVED
    dump(starter_p,starter)

    handoff=load(handoff_p)
    card=handoff['AIR_HANDOFF_CARD']
    ps=card['platform_state']
    ps['unicode_normalization_form']='NFKC'
    ps['target_platform_normalization_profile']=PROFILE
    ps['unknown_target_platform_behavior']=UNKNOWN
    fs=card['file_identity_and_delivery_state']
    fs['unicode_normalization_form']='NFKC'
    fs['target_platform_normalization_profile']=PROFILE
    fs['target_platform_profile_resolution_state']='PORTABLE_BASELINE_REQUIRED_WHEN_TARGET_UNKNOWN'
    dump(handoff_p,handoff)
    print('R8 semantic presentation/portability patch applied')

if __name__=='__main__':
    main(Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve())
