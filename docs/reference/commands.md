# Command Reference

## Terminal command namespace

### General

| Command | Purpose |
|---|---|
| `air --version` | Show package, resource-set, digest, and resource-origin information |
| `air help` | Show terminal command help |
| `air doctor` | Check installation, resources, paths, configuration, registry, and active project |
| `air paths` | Show resolved application paths |

### Configuration

| Command | Purpose |
|---|---|
| `air config show` | Show effective configuration after precedence resolution |
| `air config validate` | Validate configuration schema and constraints |
| `air config write-default` | Create the default user configuration |

### Resources

| Command | Purpose |
|---|---|
| `air resources list` | List canonical resources |
| `air resources show RESOURCE` | Show metadata for one resource |
| `air resources search QUERY` | Search aliases, headings, paths, and semantic markers |
| `air resources verify [RESOURCE]` | Verify one resource or the complete installed set |
| `air resources materialize RESOURCE --purpose TEXT` | Copy one resource to the versioned cache with a receipt |


### Boot

| Command | Purpose |
|---|---|
| `air boot validate [--module ID]` | Validate boot resources, graph safety, and semantic closure |
| `air boot plan --trigger TRIGGER` | Produce a deterministic dependency-closed plan without authorizing execution |
| `air boot compile --trigger TRIGGER --output FILE` | Write a deterministic modular or Complete AIR Prompt Set fallback bundle |
| `air boot receipt --trigger TRIGGER --output FILE` | Write a local compile receipt without writing a bundle |
| `air boot compare --trigger TRIGGER` | Compare selected bundle bytes with the Complete AIR Prompt Set |
| `air boot q1d` | Show the full 11-section beginner orientation without project activation |
| `air boot contracts` | List Stage 3 task, authorization, and continuation contracts |
| `air boot status` | Show installed boot, resource, and semantic-closure state |

Unknown-trigger fallback is a review result, not ordinary success. JSON output reports `decision: REVIEW` and the terminal process exits with status `4`.

Compiled resource frames are length-delimited: each declared digest covers the exact `size_bytes` segment embedded after its frame header. Bundle and receipt targets are cooperatively locked and post-write verified as one output transaction.

### Projects

| Command | Purpose |
|---|---|
| `air project init NAME` | Create and register an isolated workspace |
| `air project list` | List registered projects |
| `air project show [PROJECT]` | Show an explicit or active project |
| `air project use PROJECT` | Select a project explicitly |
| `air project validate [PROJECT]` | Validate structure, registration, symlink boundaries, and private-key separation |

Use `--json` before the subcommand for machine-readable output:

```bash
air --json doctor
```

## Reserved later-stage terminal namespaces

The following names remain architectural reservations rather than Stage 3 implementations:

```text
air handoff ...
air policy ...
air upgrade ...
air rollback ...
```

MCP and coding-tool adapters will call the shared boot and contract services rather than maintaining separate AIR logic.

## AIR conversational commands

Prompt-side commands such as `air status`, `air gate`, `air ask`, and `air handoff` operate inside an AIR conversation. They are not proof that the terminal application ran.
