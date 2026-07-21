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

The following names are architectural reservations, not Stage 2 implementations:

```text
air bundle ...
air handoff ...
air policy ...
air upgrade ...
air rollback ...
```

## AIR conversational commands

Prompt-side commands such as `air status`, `air gate`, `air ask`, and `air handoff` operate inside an AIR conversation. They are not proof that the terminal application ran.
