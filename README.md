[![AIR by VM4AI — Configure. Organize. Execute.](https://github.com/eddlev/air-brand/raw/main/github/readme-header.png)](https://vm4ai.com)

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Framework](https://img.shields.io/badge/framework-prompt--native-9A8F80?labelColor=1A1613)](https://vm4ai.com)
[![Development](https://img.shields.io/badge/development-v0.4.0.dev0-FF5A1F?labelColor=1A1613)](CHANGELOG.md)

**Structure for AI work. Configure. Organize. Execute.**

AIR is a prompt-native project runtime with an optional local Python application. It turns loose chat work into explicit project state, active-step execution, visible blockers, evidence gates, continuity, and receiver-facing delivery.

AIR remains cooperative rather than autonomous. The user controls intent, source truth, approvals, credentials, and irreversible actions. AIR structures the work, challenges weak assumptions, and keeps claims within the available evidence.

## Development status

The repository is moving from repository-relative local scripts to an installable application.

The current v0.4.0 development substrate provides:

- a `vm4ai-air` Python distribution;
- one installed `air` terminal command;
- packaged canonical AIR resources from `prompts/`, `profiles/`, and `runtime/`;
- resource verification, search, and materialization;
- platform-aware application paths and configuration;
- a separate registered workspace for every AIR project;
- installation diagnostics and version reporting;
- source, integration, and installed-wheel tests.

The following remain intentionally assigned to later project stages:

- modular boot migration and semantic-completeness repair;
- the updated Q1-D beginner orientation;
- handoff and signing migration;
- policy and remaining local-tool migration;
- PyPI publication and release approval.

A generated package, passing source test, valid signature, or structurally valid bundle does not by itself prove behavioural correctness, authorization, universal compatibility, or release readiness.

## Two ways to use AIR

### 1. Complete AIR Prompt Set

Attach:

- `prompts/AIR CORE RUNTIME.md`
- `prompts/AIR CONTROL SURFACE.md`
- `prompts/AIR DEFAULT STARTER PROFILE.json`

Then type this inside the AI conversation:

```text
Start a new AIR project.
```

This remains the complete prompt-native fallback.

### 2. Installed local application

The installed application carries canonical AIR resources inside the Python package and manages separate local project workspaces.

Public PyPI installation is not enabled yet. Build and install the current development wheel locally:

```bash
python -m pip install --upgrade build
python -m build
pipx install dist/vm4ai_air-0.4.0.dev0-py3-none-any.whl
```

Check the installation:

```bash
air --version
air doctor
air paths
air resources verify
```

Create an isolated project workspace:

```bash
air project init "My AIR Project" --use
air project show
air project validate
```

These are **terminal commands**. Prompt-side commands typed inside an AIR conversation, such as `air status` or `air gate`, are a separate interface.

## Installed command surface in Stage 2

```text
air --version
air doctor
air paths

air config show
air config validate
air config write-default

air resources list
air resources show
air resources search
air resources verify
air resources materialize

air project init
air project list
air project show
air project use
air project validate
```

Bundle, handoff, policy, upgrade, rollback, and release commands are reserved for their approved migration stages and must not be represented as implemented yet.

## Repository layout

| Path | Purpose |
|---|---|
| `src/vm4ai_air/` | Installable application substrate |
| `prompts/` | Canonical Complete AIR Prompt Set |
| `profiles/` | Canonical specialist packages |
| `runtime/` | Canonical runtime, module, policy, handoff, and source-control resources |
| `tests/` | Source, integration, and installed-distribution tests |
| `docs/` | Operator, architecture, development, and migration documentation |
| `.github/workflows/` | Pinned CI and package-validation workflows |

The top-level canonical resource directories remain the authoring source. The build hook verifies and copies them into the wheel as one release resource set; there are no separately maintained duplicate payloads under `src/`.

## Security and authority boundaries

- AIR does not ask for passwords, recovery codes, private signing keys, or long-lived publishing tokens.
- Private signing keys belong in the global AIR keystore, outside ordinary project workspaces.
- The installed resource manifest proves observed file relationships, sizes, and digests only.
- Resource verification is not behavioural validation.
- Local tool execution is not backend AIR enforcement.
- Authentication is not authorization.
- Repository mutation, merge, tag, release, and publication are distinct approval gates.

## Start here

- [Quick Start](docs/QUICK_START.md)
- [Installed Runtime Architecture](docs/INSTALLED_RUNTIME_ARCHITECTURE.md)
- [Operator Guide](docs/OPERATOR_GUIDE.md)
- [Development and Testing](docs/DEVELOPMENT.md)
- [Installation Matrix](docs/INSTALLATION_MATRIX.md)
- [Configuration](docs/CONFIGURATION.md)
- [Project Workspaces](docs/PROJECT_WORKSPACES.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Update and Rollback](docs/UPDATE_ROLLBACK.md)

## Release boundary

This branch is a development candidate, not a public release. Package-name commitment, Trusted Publisher configuration, repository merge, tag creation, PyPI publication, release assets, and public announcement remain separately controlled operations.

## Licence

The project is licensed under Apache-2.0. The AIR and VM4AI names and brand marks are not granted by that software/content licence; see `NOTICE` and the brand repository.
