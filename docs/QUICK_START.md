# AIR Quick Start

## Prompt-only route

Attach the Complete AIR Prompt Set:

- `prompts/AIR CORE RUNTIME.md`
- `prompts/AIR CONTROL SURFACE.md`
- `prompts/AIR DEFAULT STARTER PROFILE.json`

Then type inside the AI conversation:

```text
Start a new AIR project.
```

AIR must ask Q1 rather than inferring your branch.

## Installed development route

PyPI publication is not enabled yet. Build the current development package from a clean checkout.

PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install ".[test]"
python -m build
pipx install .\dist\vm4ai_air-0.4.0.dev0-py3-none-any.whl
```

POSIX shell:

```bash
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install '.[test]'
python -m build
pipx install dist/vm4ai_air-0.4.0.dev0-py3-none-any.whl
```

Verify:

```bash
air --version
air doctor
air paths
air resources verify
```

Successful version output reports both the Python package version and the AIR resource-set version.

## Create a project workspace

```bash
air project init "My First AIR Project" --use
air project show
air project validate
```

The workspace is registered under the platform-specific AIR data root unless you specify `--workspace` or configure `AIR_WORKSPACE_ROOT`.

## Search installed AIR resources

```bash
air resources search "handoff continuity"
air resources show "prompts/AIR CORE RUNTIME.md"
air resources materialize "prompts/AIR CORE RUNTIME.md" --purpose "attach to an AI session"
```

Materialization copies a resource into the AIR cache and writes a provenance receipt. It does not authorize the consuming action.

## Important Stage 2 boundary

The installed substrate currently manages resources, configuration, diagnostics, and project workspaces. Modular bundle compilation, Q1-D refresh, handoff/signing commands, policy execution, upgrades, rollback, and publishing remain assigned to later approved stages.
