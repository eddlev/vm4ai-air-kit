# AIR Runtime Functions

The `runtime/` directory is organized by function. It is not a second copy of the repository.

- `boot/` — Boot Kernel, manifest, load receipts, evidence, and the local boot planner/bundler.
- `modules/` — derived runtime and control modules.
- `artifact-lifecycle/` — shared artifact construction/assurance method and evaluation packs.
- `policy/` — deterministic policy plus the optional local OPA adapter.
- `handoff/` — continuity, trust, signing/verification, schemas, templates, executor, and tool.
- `source-control/` — source/control registry, adapters, and source manifests.

System-prompt assets are canonical only under `prompts/`. Handoff templates are canonical under `runtime/handoff/templates/`. Specialist packages are canonical only under `profiles/<specialist name>/` and contain a specialist profile, domain pack, method, and executor.

Run the boot tool from the repository root:

```bash
python runtime/boot/tools/air-boot.py validate-manifest
```

The boot manifest uses repository-root-relative paths and preserves the 22-module WS7 graph. Directory restructuring does not authorize module binding, execution, repository mutation, or publication.
