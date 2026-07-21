# AIR Troubleshooting

## `air` is not found

Check the installer:

```bash
pipx list
python -m pip show vm4ai-air
```

When using pipx, ensure its binary directory is on `PATH`. Open a new terminal after installation.

## `air --version` says resources are unavailable

You may be running an editable/source import without packaged resources.

For installed use, install the built wheel. For deliberate development use only:

PowerShell:

```powershell
$env:AIR_RESOURCE_ROOT = (Resolve-Path .)
```

POSIX:

```bash
export AIR_RESOURCE_ROOT="$PWD"
```

The override root must contain `prompts/`, `profiles/`, and `runtime/`. `air doctor` will report the development override.

## Resource verification fails

Run:

```bash
air --version
air resources verify
air doctor
```

Do not replace individual installed resource files. Reinstall the exact wheel or roll back to a previously tested whole package.

## Project command says no active project

Select one explicitly:

```bash
air project list
air project use <project-id-or-name>
```

AIR never selects a project from the current directory.

## Project validation finds a private key

Move the private key out of the workspace and into the global AIR keystore boundary. Do not paste it into chat or commit it to Git.

The current Stage 2 implementation reserves the keystore boundary; signing commands migrate in Stage 4.

## Registry lock timeout

Another AIR process may be updating the project registry. Wait for it to finish and retry. A lock older than the bounded stale interval may be recovered automatically.

Do not manually delete a fresh lock while another process may still own it.

## Build cannot download Hatchling or dependencies

Use a network-enabled development environment or a controlled internal package mirror. Building a wheel requires the declared build dependencies.

Source tests passing without a built wheel do not satisfy installed-distribution validation.

## A later-stage command is missing

Bundle, handoff, policy, upgrade, rollback, and publishing commands are intentionally not implemented in Stage 2. Consult the project execution map rather than treating their architecture as shipped behaviour.
