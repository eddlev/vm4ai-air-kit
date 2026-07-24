# Changelog

## 0.5.0.dev0 - Stage 3 deterministic modular boot

- Added installed-resource-backed boot validation, dependency planning, deterministic bundle compilation, and separate compile receipts.
- Added an explicit semantic-closure contract and Complete AIR Prompt Set fallback for unknown triggers.
- Added the complete 11-section Q1-D beginner orientation as a dedicated dependency-closed module.
- Added transport-neutral task, authorization, and continuation contracts for future local MCP and coding-tool adapters.
- Replaced the repository-relative boot implementation with a compatibility adapter to the shared service.
- Kept handoff signing, policy execution, MCP hosting, plugins, release, and publication separately gated.

### Fixed during Stage 3 review

- Boot validation now requires the kernel, starter, semantic-closure, Complete AIR Prompt Set, receipt, and Markdown-module structural contracts instead of accepting merely self-consistent bytes.
- Derived Markdown modules are pinned to an independent decomposition-map and exact module-content contract, so marker-only replacements fail even when manifest digests are rebuilt.
- Deterministic bundles now embed exact length-framed resource bytes whose declared digests match the embedded segments.
- Bundle and receipt output pairs now use shared target locks, post-write verification, and rollback under one transaction boundary.
- Every modular and fallback plan identifier now binds the package version, resource-set version, and full source-tree digest.
- Mutating authorization envelopes now require an explicit actor and approval provenance; neutral non-mutating envelopes default to `UNSPECIFIED`. The published JSON Schema enforces the same conditional rule.
- Unknown-trigger review results now use a distinct nonzero terminal exit code.
- Empirical session-entry remediation now hard-locks Q1 until an explicit selector is supplied; startup phrases such as `Start a new AIR project.` cannot silently bind Q1=A.
- Session-entry bundles now treat unenumerated host memory, prior uploads, and hidden project files as untrusted for current project-state claims.
- Bundle metadata now caps host verification claims at prompt-declared or unverified unless current-session tool evidence or a separately supplied compile receipt is visible.

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

- Deterministic modular boot and complete Q1-D orientation closure are implemented in the 0.5.0 development line.
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
