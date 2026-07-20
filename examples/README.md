# AIR Examples

## New project modular bundle

```bash
python ../runtime/boot/tools/air-boot.py --root .. bundle --trigger NEW_PROJECT --output new-project.md
```

## Material patch bundle

```bash
python ../runtime/boot/tools/air-boot.py --root .. bundle --trigger PATCH_ARTIFACT --trigger MATERIAL_EXECUTION --output patch-project.md
```

## Prompt-side continuation

```text
Continue project from handoff card.
```

Examples demonstrate invocation only. They do not prove the host model executed every rule or that a downstream task succeeded.
