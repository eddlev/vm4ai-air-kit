# AIR Configuration

AIR uses versioned TOML configuration.

## Effective precedence

```text
command-line overlay
> environment variables
> user config.toml
> packaged defaults
```

Show the effective configuration:

```bash
air config show
```

Validate it:

```bash
air config validate
```

Create the default file:

```bash
air config write-default
```

## Environment variables

| Variable | Purpose |
|---|---|
| `AIR_HOME` | Put all AIR roots under one explicit base; useful for testing and portable development |
| `AIR_CONFIG_HOME` | Override configuration root |
| `AIR_DATA_HOME` | Override data root |
| `AIR_STATE_HOME` | Override state root |
| `AIR_CACHE_HOME` | Override cache root |
| `AIR_LOG_HOME` | Override log root |
| `AIR_WORKSPACE_ROOT` | Override the default location for new project workspaces |
| `AIR_STRICT_RESOURCES` | Set installed-resource strictness (`true` or `false`) |
| `AIR_RESOURCE_ROOT` | Explicit authoring-source override for development only |

`AIR_RESOURCE_ROOT` is never an automatic repository search. It must be set deliberately and must contain `prompts/`, `profiles/`, and `runtime/`. `air doctor` reports the override as development evidence rather than installed-wheel evidence.

## Security

Do not place passwords, recovery codes, private keys, or publishing tokens in AIR configuration. AIR has no telemetry path, and attempts to enable telemetry are rejected.
