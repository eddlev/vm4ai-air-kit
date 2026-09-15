from __future__ import annotations

import subprocess

SOURCE_COMMIT = '45c3b93cd527ccd158920fb1ea266fd3b48910ef'
PATH = 'tools/apply_r1_remediation.py'

subprocess.run(['git', 'fetch', '--no-tags', 'origin', SOURCE_COMMIT], check=True)
raw = subprocess.run(
    ['git', 'show', f'{SOURCE_COMMIT}:{PATH}'],
    check=True,
    capture_output=True,
    text=True,
).stdout

# Localized carrier-language repair only.
assert raw.count(': false') == 3, raw.count(': false')
assert raw.count(': true') == 2, raw.count(': true')
fixed = raw.replace(': false', ': False').replace(': true', ': True')

# Net-scope accounting: permit excluding the transport bootstrap only after its
# bytes are proven identical to pinned main.
old_scope = """changed = sorted(x for x in sh('git', 'diff', '--name-only', PINNED_MAIN, capture=True).splitlines() if x)\nuntracked = sorted(x for x in sh('git', 'ls-files', '--others', '--exclude-standard', capture=True).splitlines() if x)\ncombined = sorted(set(changed + untracked))\nassert combined == PERMANENT_PATHS, (combined, PERMANENT_PATHS)\nassert (ROOT / 'tools/apply_r1_remediation.py').read_bytes() == subprocess.run(['git','show',PINNED_MAIN + ':tools/apply_r1_remediation.py'],cwd=ROOT,check=True,capture_output=True).stdout\n"""
new_scope = """bootstrap_rel = 'tools/apply_r1_remediation.py'\ncanonical_bootstrap = subprocess.run(['git','show',PINNED_MAIN + ':' + bootstrap_rel],cwd=ROOT,check=True,capture_output=True).stdout\nassert (ROOT / bootstrap_rel).read_bytes() == canonical_bootstrap\nchanged = sorted(x for x in sh('git', 'diff', '--name-only', PINNED_MAIN, capture=True).splitlines() if x)\nuntracked = sorted(x for x in sh('git', 'ls-files', '--others', '--exclude-standard', capture=True).splitlines() if x)\ncombined = sorted(set(changed + untracked) - {bootstrap_rel})\nassert combined == PERMANENT_PATHS, (combined, PERMANENT_PATHS)\n"""
assert fixed.count(old_scope) == 1, fixed.count(old_scope)
fixed = fixed.replace(old_scope, new_scope, 1)

# Transport-commit accounting: the cleanup commit must stage exactly the 11
# product paths plus the byte-verified restoration of this temporary bootstrap.
old_stage = """sh('git', 'add', '-A')\nstaged = sorted(x for x in sh('git', 'diff', '--cached', '--name-only', capture=True).splitlines() if x)\nassert staged == PERMANENT_PATHS, (staged, PERMANENT_PATHS)\n"""
new_stage = """sh('git', 'add', '-A')\nstaged = sorted(x for x in sh('git', 'diff', '--cached', '--name-only', capture=True).splitlines() if x)\nexpected_staged = sorted(PERMANENT_PATHS + [bootstrap_rel])\nassert staged == expected_staged, (staged, expected_staged)\n"""
assert fixed.count(old_stage) == 1, fixed.count(old_stage)
fixed = fixed.replace(old_stage, new_stage, 1)
assert ': false' not in fixed and ': true' not in fixed

exec(compile(fixed, f'{SOURCE_COMMIT}:{PATH}', 'exec'), {'__name__': '__main__'})
