# Changelog

## Unreleased — v0.4.0 development line

### Added

- Standards-based Python packaging under the approved `vm4ai-air` distribution identity.
- The unified `air` terminal command with version, diagnostics, path, configuration, installed-resource, and project-workspace commands.
- Build-time verification and wheel inclusion of canonical AIR resources from `prompts/`, `profiles/`, and `runtime/`.
- A single resource resolver for installed resources, explicit development-source overrides, local search, verification, and materialization receipts.
- Platform-aware global configuration, data, state, cache, log, project, and keystore paths.
- A registered, isolated workspace for every AIR project with atomic state writes and operation receipts.
- Cross-platform source, integration, and installed-wheel test foundations.

### Changed

- User-facing documentation now uses **Complete AIR Prompt Set** instead of “monolithic.”
- Ordinary installed use no longer depends on cloning the repository or executing scripts from repository-relative paths.
- The supported Python floor for the new installed runtime is Python 3.11.

### Fixed during Stage 2 review

- Resource materialization now verifies source bytes before copying or issuing a PASS receipt.
- Installed manifests now validate schema, canonical roots, resource identities, and aggregate content identity.
- Unsafe path-like resource identifiers fail closed.
- Project receipt failures roll back project creation or active-project selection.
- Private-key detection now covers every workspace directory, including `trust/public-keys/`.
- Diagnostics now distinguish missing active state from corrupt state and check existing root writability.
- Installed-distribution CI now covers Windows, macOS, and Linux through a bounded factor matrix without duplicate feature-push runs.
- Historical v0.3.0 release artifacts remain byte-stable.

### Deferred by approved project stage

- Modular boot migration and semantic-completeness repair, including the updated Q1-D beginner orientation, are assigned to Stage 3.
- Handoff and signature migration are assigned to Stage 4.
- Policy and remaining local-function migration are assigned to Stage 5.
- PyPI publishing, Trusted Publisher configuration, merge, tag, and release creation remain separately blocked.

## v0.3.0

- Uses a function-oriented repository taxonomy: canonical system prompts in `prompts/`, complete specialist packages in `profiles/<specialist name>/`, and implementation/support assets in `runtime/<function>/`.
- Removes duplicate prompt and specialist payloads from `runtime/`.
- Adds package manifests plus bounded Grounding Executor and Capability Ecology Method components so each specialist package has profile, domain, method, and executor roles.
- Aligns the public Complete AIR Prompt Set and grounding profiles with the approved WS7 file set.
- Adds the self-contained modular runtime, Boot Kernel, 22-module graph, local planner/bundler, load receipts, and portability evidence.
- Makes **OBJECT_ALL** the default formal-object visibility mode: every formal object that is created, restored, updated, or made operative is printed canonically, without manufacturing future-step objects.
- Adds the artifact lifecycle, source/control registry, human-to-machine translator, capability construction adapters, deterministic policy package, handoff integrity tooling, Capability Ecology Architect, and Domain Capability Registry.
- Adds operator, architecture, dependency, installation, troubleshooting, rollback, release, command, object, and local-tool documentation.
- Adds the WS7 tool-runtime-outage recovery case study.

### Claim boundary

AIR remains a prompt-native framework. Optional local tools provide tool-observed evidence; they do not provide general execution authorization, legal compliance, guaranteed correctness, or the private AIR backend/client runtime.
