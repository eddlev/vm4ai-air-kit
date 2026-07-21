# Stage 2 Local Validation Record

**Source baseline:** archive of repository commit `c9335fa7351619260e58662187b0188e1e43f9a0`
**Archive SHA-256:** `011f82147508e2d8dac224fb5a5f824b12f43a0a0b04eec028150470e296c7a7`
**Implementation version:** `0.4.0.dev0`

## Executed in the implementation environment

### Source and integration tests

```text
PYTHONPATH=src python -m pytest -m "not package" -q
```

Observed result at implementation time:

```text
21 passed, 2 deselected
```

### Distribution build

```text
python -m build --no-isolation
```

Observed artifacts:

```text
vm4ai_air-0.4.0.dev0-py3-none-any.whl
vm4ai_air-0.4.0.dev0.tar.gz
```

The wheel contained the generated resource manifest, the Complete AIR Prompt Set resources, profiles, and runtime resources. The source distribution retained the canonical authoring directories needed to rebuild the wheel.

### Metadata validation

```text
python -m twine check dist/*
```

Observed result: both distributions passed.

### Reproducible build check

The wheel and source distribution were each built twice with the same `SOURCE_DATE_EPOCH`. The corresponding SHA-256 digests matched byte-for-byte across both builds.

### Lint and formatting validation

```text
ruff check src tests hatch_build.py
```

Observed result: all checks passed.

### Installed-distribution tests

```text
AIR_TEST_WHEEL=<built-wheel> AIR_TEST_SDIST=<built-sdist> python -m pytest -m package -q
```

Observed result:

```text
2 passed, 21 deselected
```

The tests installed both the wheel and source distribution into separate fresh virtual environments, ran `pip check`, removed source overrides, ran outside the repository directory, verified packaged resources, created and validated a project workspace, ran diagnostics, and confirmed the import path belonged to the test environment.

### pipx smoke test

The built wheel was installed through pipx into an isolated application environment. The `air` entry point reported package version `0.4.0.dev0`, installed resource origin, and a content-derived resource-set version. `air --json doctor` returned `PASS` with zero failed checks. The package was then uninstalled through pipx.

## Not executed in this environment

- Windows execution;
- macOS execution;
- Python 3.11, 3.12, or 3.14 execution;
- GitHub Actions workflows;
- concurrency stress beyond bounded lock tests;
- interrupted-process fault injection;
- modular boot or Q1-D behavioural validation;
- handoff, signing, or policy migration tests;
- upgrade, rollback, or publication.

CI and operator execution must supply those evidence classes. This document records observed local execution only and must not be upgraded into universal compatibility or release approval.
