# AIR v0.3.0 — Modular Runtime and Function-Oriented Repository

AIR v0.3.0 introduces the modular runtime, integrated documentation, complete specialist packaging, and the OBJECT_ALL formal-object visibility default while retaining the Complete AIR Prompt Set path.

## Highlights

- **Clean repository taxonomy:** system prompts live in `prompts/`; complete specialist packages live in `profiles/<specialist name>/`; runtime implementation assets are grouped by function under `runtime/`.
- **No duplicated prompt/profile payloads:** the modular manifest references canonical files across the repository root.
- **Complete specialist packages:** each package contains a specialist profile, domain pack, method, executor, and package manifest.
- **22-module graph preserved:** the WS7 module graph remains unchanged in count and dependency behavior; only repository-relative paths changed.
- **OBJECT_ALL visibility:** every formal AIR object actually created, restored, updated, or made operative is printed canonically without manufacturing future-step objects.
- **Local tools:** modular boot, handoff signing/verification, and optional local OPA policy evaluation remain bounded and separately documented.
- **Integrated documentation:** quick start, operator guide, architecture, repository structure, installation, dependencies, troubleshooting, rollback, and release guidance.

## Repository structure

```text
prompts/                         canonical system prompts
profiles/<specialist name>/     profile + domain + method + executor
runtime/boot/                    kernel, manifest, receipts, evidence, tool
runtime/modules/                 derived runtime and control modules
runtime/artifact-lifecycle/      shared method and evaluation packs
runtime/policy/                  deterministic policy and OPA adapter
runtime/handoff/                 templates, schemas, policy, executor, tool
runtime/source-control/          registry, adapters, source manifests
```

The first unreleased v0.3.0 candidate duplicated system prompts and specialist assets inside `runtime/`. This structure-revised candidate removes those copies and supersedes that candidate.

## Migration from v0.2.5

1. Back up the current repository or installed AIR files.
2. Replace the prompt/profile files as one coherent v0.3.0 set.
3. Add the function-oriented `runtime/`, expanded `docs/`, `examples/`, `CHANGELOG.md`, and `release/` paths.
4. Validate from the repository root:

   ```bash
   python runtime/boot/tools/air-boot.py validate-manifest
   ```

5. Run a `NEW_PROJECT` plan and bundle smoke test.
6. Keep the previous release archive until operator acceptance.

Do not merge the earlier unreleased v0.3.0 overlay with this structure-revised overlay.

## Optional dependencies

- Modular boot uses Python 3 standard library only.
- Handoff signing/verification uses the pinned packages in `runtime/handoff/tools/requirements.txt`.
- OPA policy execution requires a local OPA binary; prompt-simulated policy posture remains an explicitly limited fallback.

## Claim boundary

AIR is prompt-native. Model behavior varies by provider, interface, context limits, and load conditions. Local hashes, signatures, policy results, and boot checks are tool-observed evidence, not general authorization or a guarantee of correctness, safety, compliance, or backend enforcement.
