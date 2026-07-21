# AIR Project Workspaces

Every AIR project has a UUID and a separately registered workspace.

## Create a project

```bash
air project init "Example Project" --use
```

Use a custom workspace or reference a source repository:

```bash
air project init "Example Project" \
  --workspace /path/to/air-workspaces/example \
  --source /path/to/source-repository \
  --use
```

PowerShell:

```powershell
air project init "Example Project" `
  --workspace "D:\AIR Projects\example" `
  --source "C:\dev\example" `
  --use
```

The source repository and AIR workspace are separate concepts. AIR does not silently create project state in the current directory.

## Select and inspect

```bash
air project list
air project use <project-id-or-name>
air project show
air project validate
```

Changing directories does not change the active AIR project.

## Workspace classes

- `state/`: project and session state;
- `bundles/`: specifications, compiled output, receipts, validation;
- `handoffs/`: cards, envelopes, verification, acceptance;
- `trust/`: public keys, trust policy, continuity anchors;
- `signatures/`: signature envelopes and verification;
- `evidence/`: sources, tests, operator evidence, model runs, release evidence;
- `exports/`: prompt sets, reports, release candidates;
- `logs/`: operation and validation records;
- `tmp/`: disposable project-local temporary files.

## Key boundary

Private signing keys belong under the global AIR keystore, not in project workspaces. `air project validate` fails when common private-key files or PEM markers are found outside the permitted public-key area.
