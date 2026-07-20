# AIR Repository and Runtime Architecture

## Three canonical planes

### 1. System prompts — `prompts/`

The monolithic user-attached AIR system assets live only here:

- `AIR CORE RUNTIME.md`
- `AIR CONTROL SURFACE.md`
- `AIR DEFAULT STARTER PROFILE.json`

### 2. Specialist packages — `profiles/<specialist name>/`

Every specialist receives a dedicated folder containing:

- specialist profile;
- domain pack;
- method;
- executor;
- package manifest.

The folder packages related capability layers but does not bind or activate them.

### 3. Runtime functions — `runtime/<function>/`

`runtime/` is not a complete duplicate distribution. It contains implementation and support assets grouped by function:

- `boot/`
- `modules/`
- `artifact-lifecycle/`
- `policy/`
- `handoff/`
- `source-control/`

The Boot Module Manifest uses repository-root-relative paths. It may select canonical specialist files from `profiles/`, canonical prompt files from `prompts/`, and derived modules from `runtime/modules/` without duplicating their payloads.

## Authority boundaries

- Directory placement does not bind a profile.
- A Method Pack is a procedure, not proof that it ran.
- An Executor is a bounded operation contract, not an autonomous agent.
- A manifest or hash proves only the observed file relationship.
- AIR_GATE, active-contract authority, evidence requirements, and explicit approvals remain controlling.
