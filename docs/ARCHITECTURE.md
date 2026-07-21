# AIR Repository and Runtime Architecture

## Architecture planes

AIR separates authoring source, installed application code, installed canonical resources, and mutable project workspaces.

### 1. Canonical authoring source

The repository keeps one authoritative checked-in copy of each AIR resource:

```text
prompts/
profiles/
runtime/
```

`prompts/` contains the Complete AIR Prompt Set. `profiles/` contains specialist packages. `runtime/` contains boot, module, artifact-lifecycle, policy, handoff, and source-control resources.

### 2. Installable application

Python application code lives under:

```text
src/vm4ai_air/
```

The package exposes one terminal command:

```text
air
```

All consumers must use shared resource, configuration, path, I/O, and workspace interfaces. They must not derive a repository root from the current working directory or script location.

### 3. Installed canonical resource set

`src/vm4ai_air/version.py` is the single package-version source. Hatchling reads that file for distribution metadata, and the build hook uses the same value in generated resource metadata.

During wheel construction, `hatch_build.py`:

1. inventories `prompts/`, `profiles/`, and `runtime/`;
2. strictly parses every JSON file;
3. verifies declared and canonical prompt sentinels;
4. calculates sizes and SHA-256 digests;
5. generates a resource manifest, index, bundle definitions, and build receipt;
6. includes the verified source set under `vm4ai_air/resources/air/` in the wheel.

The wheel copy is a generated release artifact. It is not a second authoring source. Runtime loading recomputes and validates the aggregate manifest identity before the resource set is accepted.

### 4. Global local-application state

AIR resolves platform-specific configuration, data, state, cache, and log roots with `platformdirs`.

Global data includes:

- the project registry;
- the private keystore boundary;
- shared trust and migration state;
- operation receipts;
- installed-resource materialization cache.

### 5. Per-project mutable workspace

Every AIR project has an immutable UUID and one registered workspace. Bundles, receipts, handoffs, signatures, anchors, evidence, exports, logs, and project state remain separated by project.

Private signing keys are prohibited from ordinary project workspaces.

## Authority boundaries

- Package installation does not authorize project or repository actions.
- A resource manifest proves only the observed packaged file relationship.
- A written test is not an executed test.
- A passing structural check is not semantic or behavioural correctness.
- A signature authenticates an observed payload under a configured key; it does not authorize execution.
- Prompt-side state is not backend enforcement.

See [Installed Runtime Architecture](INSTALLED_RUNTIME_ARCHITECTURE.md) for the detailed contracts.
