# AIR Development and Testing

## Requirements

- Python 3.11 or newer;
- a clean repository checkout;
- network access for first-time dependency installation;
- no publishing credentials for ordinary development.

## Create a development environment

PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

POSIX shell:

```bash
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[test]'
```

## Source and integration tests

The source test route uses an explicit canonical-source override:

PowerShell:

```powershell
$env:AIR_HOME = "$PWD\.air-local"
$env:AIR_RESOURCE_ROOT = "$PWD"
python -m pytest -m "not package"
```

POSIX shell:

```bash
AIR_HOME="$PWD/.air-local" \
AIR_RESOURCE_ROOT="$PWD" \
python -m pytest -m 'not package'
```

This is development-source evidence, not installed-wheel evidence.

## Build distributions

```bash
python -m build
python -m twine check dist/*
```

The build must produce both:

```text
dist/vm4ai_air-0.4.0.dev0-py3-none-any.whl
dist/vm4ai_air-0.4.0.dev0.tar.gz
```

## Installed-wheel test

PowerShell:

```powershell
$env:AIR_TEST_WHEEL = (Resolve-Path .\dist\vm4ai_air-0.4.0.dev0-py3-none-any.whl)
python -m pytest -m package
```

POSIX shell:

```bash
AIR_TEST_WHEEL="$PWD/dist/vm4ai_air-0.4.0.dev0-py3-none-any.whl" \
python -m pytest -m package
```

The package test creates a fresh virtual environment and runs outside the repository without `AIR_RESOURCE_ROOT` or `PYTHONPATH`.

## Development CLI

```bash
AIR_HOME="$PWD/.air-local" AIR_RESOURCE_ROOT="$PWD" python -m vm4ai_air --version
AIR_HOME="$PWD/.air-local" AIR_RESOURCE_ROOT="$PWD" python -m vm4ai_air doctor
```

## Evidence boundary

Record separately:

- files generated;
- tests written;
- tests executed;
- operating systems and Python versions actually exercised;
- failures and retries;
- unverified platforms or behaviours;
- deliberate deferrals.
