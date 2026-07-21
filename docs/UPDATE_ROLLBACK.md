# AIR Update and Rollback

## Current development boundary

Stage 2 defines package and workspace identities but does not implement self-update or rollback commands. Operators must not infer those commands exist from the architecture.

## Package update invariant

Treat each installed package and its embedded AIR resource set as one coherent identity.

Never mix:

- application code from one version;
- a resource manifest from another version;
- selected prompt or module files copied from a third version.

`air --version` reports package and resource-set versions separately so mismatches can be detected.

## Workspace migration invariant

Future schema migrations must:

1. lock affected state;
2. validate the current schema;
3. create a backup or snapshot;
4. write an operation journal;
5. perform atomic writes;
6. validate the migrated result;
7. retain the previous snapshot until operator acceptance.

## Current manual package rollback

Until Stage 6 completes governed update and rollback commands:

1. record the currently installed version with `air --version`;
2. retain the previously tested wheel;
3. install the exact prior wheel through the same installer used originally;
4. run `air doctor` and `air resources verify`;
5. do not downgrade project schema data unless a reviewed migration path exists.

A package rollback is not automatically a project-data rollback.

## Legacy repository rollback

For the v0.3.0 repository-relative tool set, restore the complete prior repository release rather than individual manifest or module files.

Repository merge, tag, release, PyPI publication, and rollback approval remain distinct actions.
