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

## Subsequent operator and CI evidence

After the implementation-environment run recorded above:

- Windows 11 with Python 3.13 completed the source, integration, build, metadata, installed-wheel, installed-source-distribution, and dependency checks successfully.
- The initial pull-request CI source matrix completed successfully on Windows, macOS, and Linux with Python 3.11, 3.12, 3.13, and 3.14.
- The initial package workflow completed successfully on Ubuntu with Python 3.13.

The Stage 2 review then identified integrity and transaction failure paths that the initial tests did not cover. The remediation adds regression tests for those defects and changes the package workflow to an installed-distribution factor matrix covering Linux/Python 3.11, Linux/Python 3.14, Windows/Python 3.13, and macOS/Python 3.12. The authoritative result for that remediation matrix is the corresponding GitHub Actions run; this committed record does not claim that a future run has passed.

The optional Ubuntu 24.04 operator smoke test remains supplementary rather than a merge gate.

## Stage 2 remediation execution in the implementation environment

The reviewed remediation source was then executed locally with the following observed results:

- Ruff source and test lint — pass;
- source, integration, regression, schema, and documentation tests — `44 passed, 2 deselected`;
- wheel and source-distribution build — pass;
- Twine metadata validation — both distributions passed;
- isolated wheel and source-distribution tests — `2 passed, 44 deselected`;
- pipx wheel installation, `air --version`, and `air --json doctor` — pass;
- installed resource verification — 69 resources, zero failures;
- two builds with the same `SOURCE_DATE_EPOCH` — byte-for-byte identical wheel and source distribution;
- `git diff --check` — pass.

This local remediation evidence is Linux/Python 3.13 evidence. The revised GitHub Actions source matrix and installed-distribution factor matrix remain the cross-platform gate after the remediation commit is pushed.
