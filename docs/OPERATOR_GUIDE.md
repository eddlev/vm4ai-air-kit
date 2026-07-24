# AIR Operator Guide

## 1. Interfaces

AIR now has two distinct command surfaces.

### Terminal commands

Run in PowerShell, Command Prompt, Bash, zsh, or another terminal:

```text
air --version
air doctor
air project init
air resources verify
```

These commands execute local Python code and can produce local tool evidence.

### AIR conversational commands

Type inside an AIR-enabled AI conversation:

```text
air status
air gate
air ask
air handoff
```

These are prompt-side controls. They are not automatically terminal commands and do not prove local tool execution.

## 2. Operating model

AIR separates:

1. project purpose and scope;
2. the one current active step;
3. formal project artifacts;
4. the benchmark used to evaluate work;
5. the receiver-facing delivery;
6. local file and tool evidence.

Keep prompt-declared, file-observed, tool-observed, operator-witnessed, cryptographically verified, and backend-enforced states separate.

## 3. Installation health

Run:

```bash
air --version
air doctor
air paths
air resources verify
```

`air --version` should report both package and resource-set versions. `air doctor` may return `WARN` when an explicit development override is active; this is not an installed-wheel failure, but it is not installed-wheel evidence either.

## 4. Project workspaces

Create and select explicitly:

```bash
air project init "Project Name" --use
air project list
air project show
air project validate
```

Changing the current directory does not select another project.

Every project has separate state, bundles, handoffs, signatures, anchors, evidence, exports, and logs.

## 5. Installed resources

List or search:

```bash
air resources list --prefix prompts
air resources search "Q1-D orientation"
air resources show "prompts/AIR CORE RUNTIME.md"
```

Verify:

```bash
air resources verify
```

Materialize for an external tool or attachment:

```bash
air resources materialize \
  "prompts/AIR CORE RUNTIME.md" \
  --purpose "attach Complete AIR Prompt Set resource"
```

The receipt records the source digest, resource-set version, destination path, and purpose.

## 6. Source and patching

Repository mutations require the exact current source set. A prior summary, generated fragment, filename, or remembered tree is not enough.

Before patching:

1. confirm branch and commit;
2. confirm the worktree is clean or classify every existing change;
3. identify every affected file and generated derivative;
4. distinguish source files from build artifacts;
5. run the relevant tests after the complete change set.

## 7. Private keys

Private keys belong under the global AIR keystore boundary. Do not place them in a project workspace, repository, evidence folder, export, or chat.

`air project validate` detects common private-key files and PEM markers. A pass is a bounded local scan, not proof that no secret exists.

## 8. Stage boundaries

Stage 2 implements the shared package substrate only.

The following remain later work:

- modular boot and Q1-D refresh;
- handoff and signing migration;
- policy migration;
- upgrade and rollback commands;
- publishing.

Do not use architecture documentation as proof that a later command already exists.

## 9. Completion reporting

Every material delivery should separate:

- implemented;
- tests written;
- tests executed;
- unverified;
- deliberately deferred;
- blocked by environment or approval.

## Deterministic boot

Validate the installed boot graph and semantic closure:

```bash
air boot validate
```

Plan and compile a task-specific bundle:

```bash
air boot plan --trigger CODING --trigger REPOSITORY
air boot compile --trigger CODING --trigger REPOSITORY --output air-coding-bundle.md --receipt air-coding-bundle.receipt.json
```

Use `air boot q1d` to inspect the complete beginner orientation. The command does not activate a project. Unknown triggers return `REVIEW`, use the Complete AIR Prompt Set fallback unless fallback is explicitly disabled, and exit with status `4` so automation must handle the review state explicitly.
