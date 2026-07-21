# Local Boot Tool

## Current status

`runtime/boot/tools/air-boot.py` is the v0.3.0 repository-relative compatibility implementation.

It validates the legacy boot manifest, plans modules by trigger, builds a prompt bundle, and emits a load receipt. It derives its source boundary from the repository tree and therefore is not the installed runtime implementation.

## Legacy commands

```bash
python runtime/boot/tools/air-boot.py validate-manifest
python runtime/boot/tools/air-boot.py plan --trigger NEW_PROJECT
python runtime/boot/tools/air-boot.py bundle --trigger NEW_PROJECT --output air-bundle.md
```

## Stage 3 migration

Stage 3 must:

- move boot behaviour onto the shared installed resource resolver;
- write bundles and receipts into the active project workspace;
- add semantic-surface and branch-closure validation;
- retain the Complete AIR Prompt Set fallback;
- update Q1-D for the installed framework;
- regenerate derived modules, decomposition evidence, hashes, and manifests;
- run behavioural and cross-model regressions.

A valid legacy manifest or digest check does not prove the bundle can execute every reachable onboarding branch.
