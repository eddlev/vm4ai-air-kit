# AIR Installed Runtime Architecture

**Development line:** `0.4.0.dev0`
**Distribution:** `vm4ai-air`
**Python import package:** `vm4ai_air`
**Terminal command:** `air`
**Python floor:** 3.11

## 1. Goals

The installed runtime must:

- work without a repository clone;
- carry canonical AIR resources inside the installed distribution;
- expose one coherent terminal command;
- keep every AIR project in a separate registered workspace;
- keep private keys outside project artifacts;
- support deterministic resource verification and local retrieval;
- retain the Complete AIR Prompt Set as the reliable fallback;
- provide a substrate for later boot, handoff, signing, policy, upgrade, and rollback migrations.

## 2. Non-goals in Stage 2

Stage 2 does not migrate or claim completion of:

- modular bundle compilation;
- Q1-D beginner-orientation changes;
- handoff cryptographic commands;
- OPA policy execution;
- self-upgrade or rollback execution;
- PyPI publication.

Those capabilities must consume this substrate in their approved later stages.

## 3. Package structure

```text
src/vm4ai_air/
  __init__.py
  __main__.py
  cli.py
  errors.py
  paths.py
  version.py
  config/
  diagnostics/
  io/
  resources/
  schemas/
  workspace/
```

The `src/` layout prevents accidental imports from the repository root from masquerading as installed-package evidence.

## 4. Build contract

`pyproject.toml` uses PEP 517/PEP 621 metadata and Hatchling.

`hatch_build.py` is the only build-time bridge from repository authoring resources into the wheel. It does not edit canonical source files.

Generated files:

```text
AIR INSTALLED RESOURCE MANIFEST.json
AIR RESOURCE INDEX.json
AIR INSTALLED BUNDLE DEFINITIONS.json
AIR RESOURCE BUILD RECEIPT.json
```

The manifest carries:

- package version;
- authoring release line;
- resource-set version;
- aggregate source-tree digest;
- one record per canonical file;
- logical resource ID;
- repository-relative authoring path;
- package path;
- media type;
- size and SHA-256 digest;
- aliases, headings, semantic markers, and terminal sentinel where present.

The resource-set version is content-derived. A package version and resource-set version are reported separately.

## 5. Resource resolver contract

All runtime consumers use `ResourceResolver`.

Supported operations:

- resolve by logical ID, canonical path, or unambiguous alias;
- list and search metadata;
- read text or bytes;
- verify one resource or the complete set;
- materialize a resource into a versioned cache with a receipt.

Default resolution uses `importlib.resources` and the installed package. An explicit `AIR_RESOURCE_ROOT` environment variable is available for development and tests only. Diagnostics must disclose when that override is active.

No consumer may assume that an installed resource is a permanent ordinary filesystem path. External tools receive a materialized cache path and provenance receipt.

## 6. Configuration and path contract

Resolved path classes:

- configuration;
- data;
- state;
- cache;
- logs.

Environment overrides:

```text
AIR_HOME
AIR_CONFIG_HOME
AIR_DATA_HOME
AIR_STATE_HOME
AIR_CACHE_HOME
AIR_LOG_HOME
AIR_WORKSPACE_ROOT
AIR_RESOURCE_ROOT   development only
```

Configuration precedence:

```text
command-line overlay
> AIR_* environment variables
> user configuration
> packaged defaults
```

AIR has no telemetry path. `application.telemetry_enabled` must remain false.

## 7. Project registry and workspace contract

The global registry lives under the user data root. Each record contains:

- project UUID;
- name and slug;
- absolute workspace path;
- optional source-repository path;
- creation time;
- status.

The current working directory never silently selects a project. Selection occurs only through explicit `air project use` or an explicit project identifier.

Workspace creation uses:

- a staging directory;
- required directory construction;
- atomic promotion to the final path;
- locked registry update;
- local operation receipts;
- cleanup on failed registration.

Required workspace classes:

```text
state/
bundles/
handoffs/
trust/
signatures/
evidence/
exports/
logs/
tmp/
```

## 8. Private-key boundary

The global private keystore is:

```text
DATA_ROOT/keystore/
```

Project workspaces may contain public keys, trust policy, signature envelopes, and verification evidence, but not private key material. Workspace validation detects common private-key file names and PEM markers and fails closed.

The Stage 2 keystore is a reserved boundary. Signing behaviour migrates in Stage 4.

## 9. Atomicity and locking

AIR-owned files use same-directory temporary files, file flush, `fsync`, and `os.replace`.

Registry mutation uses a cooperative exclusive lock file with:

- exclusive creation;
- process and host metadata;
- timeout;
- bounded stale-lock recovery;
- ownership token before removal.

These mechanisms reduce partial-write and concurrent-update risk. They do not replace operating-system access control or transactional databases.

## 10. Diagnostics

`air doctor` performs read-only checks of:

- package identity;
- application path availability and writability;
- effective configuration;
- installed-resource origin and verification;
- project registry readability;
- active-project workspace validity.

A doctor pass is installation evidence, not proof of AIR semantic correctness or release readiness.

## 11. Test architecture

Source and integration tests cover:

- atomic writes and lock failure;
- path override behaviour;
- configuration precedence and rejection;
- complete canonical resource inventory;
- Complete AIR Prompt Set bundle identity;
- resource verification, search, and materialization;
- project isolation and explicit selection;
- private-key boundary enforcement;
- CLI execution outside the repository directory.

Package tests build and install both the wheel and source distribution into fresh virtual environments, remove development overrides, execute outside the repository, verify installed resources, create a project, validate it, and confirm the import path belongs to that environment.

CI separates source tests from installed-distribution tests. The source matrix covers Python 3.11-3.14 on Windows, macOS, and Linux. The installed-distribution factor matrix covers all three operating-system families while sampling the oldest and newest supported Python versions without duplicating every source-matrix combination.

## 12. Migration sequence

1. **Stage 2:** package substrate, resolver, configuration, workspace, diagnostics.
2. **Stage 3:** modular boot migration, semantic bundle closure, Complete AIR Prompt Set integration, Q1-D refresh.
3. **Stage 4:** handoff and signature migration onto global keystore and project workspaces.
4. **Stage 5:** policy and remaining local functions.
5. **Stage 6:** full cross-platform, failure-path, regression, cross-model, release, upgrade, and rollback validation.

## 13. Compatibility

Legacy repository scripts remain unchanged in Stage 2. They continue to use repository-relative paths and are not the installed application implementation.

Later migration wrappers must delegate to shared package functions rather than duplicate logic. Removal requires the approved compatibility window and separate review.
