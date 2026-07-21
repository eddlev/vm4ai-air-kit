[![AIR by VM4AI — Configure. Organize. Execute.](https://github.com/eddlev/air-brand/raw/main/github/readme-header.png)](https://vm4ai.com)

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Framework](https://img.shields.io/badge/framework-prompt--native-9A8F80?labelColor=1A1613)](https://vm4ai.com)
[![Development](https://img.shields.io/badge/development-v0.5.0.dev0-FF5A1F?labelColor=1A1613)](CHANGELOG.md)

**Structure for AI work. Configure. Organize. Execute.**

AIR is a prompt-native project runtime with an optional local Python application. It turns loose chat work into explicit project state, active-step execution, visible blockers, evidence gates, continuity, and receiver-facing delivery.

AIR remains cooperative rather than autonomous. The user controls intent, source truth, approvals, credentials, and irreversible actions. AIR structures the work, challenges weak assumptions, and keeps claims within the available evidence.

## Development status

The repository is moving from repository-relative local scripts to an installable application.

The current v0.5.0 development line provides:

- a `vm4ai-air` Python distribution;
- one installed `air` terminal command;
- packaged canonical AIR resources from `prompts/`, `profiles/`, and `runtime/`;
- resource verification, search, and materialization;
- platform-aware application paths and configuration;
- a separate registered workspace for every AIR project;
- installation diagnostics and version reporting;
- source, integration, and installed-distribution tests;
- deterministic installed-resource boot validation, planning, and compilation;
- complete Q1-D beginner-orientation closure;
- reusable task, authorization, and continuation contracts for future local adapters.

The following remain intentionally assigned to later project stages:

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
pipx install dist/vm4ai_air-0.5.0.dev0-py3-none-any.whl
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

air boot validate
air boot plan --trigger NEW_PROJECT
air boot plan --trigger Q1_D_ORIENTATION
air boot compile --trigger CODING --trigger REPOSITORY --output air-bundle.md
air boot q1d
air boot status
```

These are **terminal commands**. Prompt-side commands typed inside an AIR conversation, such as `air status` or `air gate`, are a separate interface.

## Installed command surface through Stage 3

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

air boot validate
air boot plan --trigger NEW_PROJECT
air boot plan --trigger Q1_D_ORIENTATION
air boot compile --trigger CODING --trigger REPOSITORY --output air-bundle.md
air boot q1d
air boot status
```

Handoff signing, policy execution, upgrade, rollback, release, publication, MCP hosting, and coding-tool plugins remain separately gated. `air boot` compiles prompt bundles; it does not authorize the host to execute tools.

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
- [Stage 3 Local Validation](docs/validation/STAGE_3_LOCAL_VALIDATION.md)
- [Local Adapter Boundary](docs/integrations/LOCAL_ADAPTER_BOUNDARY.md)
- [AI Agent Incident Case Study Plan](docs/research/AI_AGENT_INCIDENT_CASE_STUDY_PLAN.md)
- [Installation Matrix](docs/INSTALLATION_MATRIX.md)
- [Configuration](docs/CONFIGURATION.md)
- [Project Workspaces](docs/PROJECT_WORKSPACES.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Update and Rollback](docs/UPDATE_ROLLBACK.md)

## Release boundary

This branch is a development candidate, not a public release. Package-name commitment, Trusted Publisher configuration, repository merge, tag creation, PyPI publication, release assets, and public announcement remain separately controlled operations.

## Licence

The project is licensed under Apache-2.0. The AIR and VM4AI names and brand marks are not granted by that software/content licence; see `NOTICE` and the brand repository.
