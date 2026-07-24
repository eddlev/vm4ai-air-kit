# AIR User Guide

## Choose a use route

### Complete AIR Prompt Set

Use the three canonical files in `prompts/` when you want the complete prompt-native fallback.

### Installed local application

Use the `air` terminal command when you want verified installed resources, local project workspaces, diagnostics, and local evidence.

Public installation is not enabled yet. Use a reviewed development wheel.

## First local project

```bash
air doctor
air project init "My Project" --use
air project show
air project validate
```

AIR creates a user-scoped workspace rather than writing project state into the current directory.

## Working with resources

```bash
air resources search "capability ecology"
air resources show "AIR CAPABILITY ECOLOGY ARCHITECT"
air resources verify
```

The resolver searches installed metadata, aliases, headings, and semantic markers. It does not claim semantic understanding equivalent to a model or external search service.

## Continue in an AI session

Use `air boot validate`, `air boot plan`, and `air boot compile` for deterministic installed-resource bundles. The Complete AIR Prompt Set remains the visible fallback when a trigger is unknown or a host cannot use the modular route.

Do not infer behavioral equivalence merely because the local bundle validates; host/model behavior still requires empirical testing.

## Local evidence

Examples of local tool evidence include:

- package and resource versions;
- file sizes and digests;
- materialization receipts;
- project registration and validation receipts;
- executed test output.

These do not automatically establish semantic correctness, authorization, or backend enforcement.
