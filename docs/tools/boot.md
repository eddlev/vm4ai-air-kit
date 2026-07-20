# Local Boot Tool

**Path:** `runtime/boot/tools/air-boot.py`

## Purpose

Validate the module manifest, plan modules by trigger, build a local prompt bundle, and emit a load receipt.

## Authority boundary

The tool validates local files and plans loading. It does not authorize the action described by the prompt bundle.

## Dependencies

Python 3 standard library only. Network and package installation are not required.

## Commands

```bash
python runtime/boot/tools/air-boot.py validate-manifest
python runtime/boot/tools/air-boot.py validate-module AIR_RUNTIME_ENTRY_AND_ACTIVATION_V1
python runtime/boot/tools/air-boot.py plan --trigger NEW_PROJECT
python runtime/boot/tools/air-boot.py bundle --trigger NEW_PROJECT --output air-bundle.md
python runtime/boot/tools/air-boot.py receipt --trigger NEW_PROJECT --output receipt.json
python runtime/boot/tools/air-boot.py compare --triggers NEW_PROJECT
python runtime/boot/tools/air-boot.py status
```

Outputs must not overwrite existing files unless `--overwrite` is supplied.

## Failure behavior

Unsafe paths, missing files, digest mismatches, sentinel mismatches, duplicate IDs, unresolved dependencies, and cycles fail validation. Unknown triggers require review or monolith fallback.
