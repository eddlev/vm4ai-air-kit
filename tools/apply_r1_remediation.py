from __future__ import annotations

import subprocess

SOURCE_COMMIT = '45c3b93cd527ccd158920fb1ea266fd3b48910ef'
PATH = 'tools/apply_r1_remediation.py'

# The Actions checkout is depth=1. Fetch exactly the failed carrier source commit
# so the localized language repair can be applied without reconstructing its payload.
subprocess.run(['git', 'fetch', '--no-tags', 'origin', SOURCE_COMMIT], check=True)
raw = subprocess.run(
    ['git', 'show', f'{SOURCE_COMMIT}:{PATH}'],
    check=True,
    capture_output=True,
    text=True,
).stdout

# Localized carrier-language repair only: the evidence object is Python source,
# so JSON boolean literals must use Python capitalization.
assert raw.count(': false') == 3, raw.count(': false')
assert raw.count(': true') == 2, raw.count(': true')
fixed = raw.replace(': false', ': False').replace(': true', ': True')
assert ': false' not in fixed and ': true' not in fixed

exec(compile(fixed, f'{SOURCE_COMMIT}:{PATH}', 'exec'), {'__name__': '__main__'})
