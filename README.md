[![AIR by VM4AI — Configure. Organize. Execute.](https://github.com/eddlev/air-brand/raw/main/github/readme-header.png)](https://vm4ai.com)

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Framework](https://img.shields.io/badge/framework-prompt--based-9A8F80?labelColor=1A1613)](https://vm4ai.com)
[![Release](https://img.shields.io/badge/release-v0.3.0-FF5A1F?labelColor=1A1613)](https://github.com/eddlev/vm4ai-air-kit/releases)

**Structure for AI work. Configure. Organize. Execute.**

AIR is a prompt-native project runtime for capable language-model interfaces. It turns a loose chat into explicit project state, active-step execution, visible blockers, evidence gates, continuity, and receiver-facing delivery.

This repository contains two ways to use AIR:

1. **Full prompt boot** — attach the monolithic prompt files in `prompts/`.
2. **Local modular boot** — use the self-contained runtime in `runtime/` and load only the modules selected for the active trigger.

AIR is cooperative, not autonomous. The user controls intent and approvals. AIR structures the work and surfaces uncertainty, evidence requirements, and the next allowed action.

## Important claim boundary

The public AIR Kit is prompt-based. It does not provide the private AIR backend/client runtime and does not, by itself, provide backend enforcement, guaranteed correctness, legal compliance, repository alignment, autonomous execution, or cryptographic trust.

The optional local tools can produce **tool-observed** evidence such as file digests, module plans, local policy results, signatures, and continuity checks. Tool-observed evidence is not general execution authorization.

## Start here

- [Beginner Quick Start](docs/QUICK_START.md)
- [Complete Operator Guide](docs/OPERATOR_GUIDE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Installation matrix](docs/INSTALLATION_MATRIX.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## Full prompt boot

Attach:

- `prompts/AIR CORE RUNTIME.md`
- `prompts/AIR CONTROL SURFACE.md`
- `prompts/AIR DEFAULT STARTER PROFILE.json`

Then type:

```text
Start a new AIR project.
```

AIR must ask Q1 rather than inferring the branch from the boot request.

The approved visibility default is **OBJECT_ALL**: every formal object actually created, restored, updated, or made operative is printed canonically. AIR does not manufacture future-step objects merely to print them.

## Modular local boot

Validate the bundled module graph:

```bash
python runtime/boot/tools/air-boot.py validate-manifest
```

Plan a new-project bundle:

```bash
python runtime/boot/tools/air-boot.py plan --trigger NEW_PROJECT
```

Build a local prompt bundle:

```bash
python runtime/boot/tools/air-boot.py bundle \
  --trigger NEW_PROJECT \
  --output air-new-project.md
```

The modular boot tool uses local files, the Python standard library, and no network service. Module selection and digest checks do not authorize subsequent actions.

## Repository layout

| Path | Purpose |
|---|---|
| `prompts/` | Canonical system-prompt bundle |
| `profiles/` | Complete specialist packages, one folder per specialist: profile, domain pack, method, executor |
| `runtime/` | Function-oriented boot, modules, artifact lifecycle, policy, handoff, and source/control implementation assets |
| `docs/` | Quick start, operator guide, architecture, references, tools, recovery, and release guidance |
| `examples/` | Copyable local examples and sample invocations |

The boot manifest is at `runtime/boot/AIR BOOT MODULE MANIFEST.json` and uses repository-root-relative paths. `runtime/` contains no duplicate copies of files from `prompts/` or `profiles/`.

## Core commands

Prompt-side controls include:

```text
air status
air help
air object all
air compact
air verbose
air evidence
air gate
air handoff
air patch plan
```

Commands cannot bypass AIR_GATE, evidence requirements, safety boundaries, or explicit approval gates. See [Command reference](docs/reference/commands.md).

## Optional local tools

- [Boot and module planner](docs/tools/boot.md)
- [Handoff signing and continuity verifier](docs/tools/handoff.md)
- [Local OPA policy adapter](docs/tools/opa.md)

## Documentation index

- [Operator Guide](docs/OPERATOR_GUIDE.md)
- [User Guide](docs/AIR_USER_GUIDE.md)
- [Model Portability Notes](docs/AIR_MODEL_PORTABILITY_NOTES.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Glossary](docs/GLOSSARY.md)
- [Dependencies](docs/DEPENDENCIES.md)
- [Prompt-only vs tool-evaluated modes](docs/PROMPT_VS_TOOL_MODES.md)
- [Update and rollback](docs/UPDATE_ROLLBACK.md)
- [Release process](docs/RELEASES.md)

## Release line

This file set is the v0.3.0 release line. Repository merge, tag creation, release-asset publication, and public announcement remain separately controlled operations.

## License

The project is licensed under Apache-2.0. The AIR and VM4AI names and brand marks are not granted by that software/content licence; see `NOTICE` and the [brand repository](https://github.com/eddlev/air-brand).
