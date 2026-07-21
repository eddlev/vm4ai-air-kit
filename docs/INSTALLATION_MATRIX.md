# AIR Installation Matrix

| Mode | Windows | macOS | Linux | Dependencies | Repository clone required |
|---|---|---|---|---|---|
| Complete AIR Prompt Set | Supported | Supported | Supported | Capable AI interface | No, when obtained from a release bundle |
| Installed development wheel | Supported target; CI required | Supported target; CI required | Executed locally and CI target | Python 3.11+, `platformdirs` | No after wheel creation |
| Editable development install | Supported | Supported | Supported | Python 3.11+, Hatchling/test dependencies | Yes |
| Legacy modular boot script | Compatibility path | Compatibility path | Compatibility path | Python standard library | Yes |
| Legacy handoff tool | Compatibility path | Compatibility path | Compatibility path | pinned handoff dependencies | Yes |
| Legacy OPA adapter | Compatibility path | Compatibility path | Compatibility path | operator-installed OPA | Yes |

## Recommended user installation

After package approval and publication, the recommended route will be:

```bash
pipx install vm4ai-air
```

Publication is currently blocked. Use a reviewed local wheel:

```bash
pipx install dist/vm4ai_air-0.4.0.dev0-py3-none-any.whl
```

## Python support

The installed runtime requires Python 3.11 or newer. The required CI matrix is Python 3.11–3.14 on Windows, macOS, and Linux.

## Permissions

The application does not require administrator privileges, system services, public listeners, or a central AIR service. It creates user-scoped directories only when a command needs them.

Private signing keys must remain outside project workspaces under the global AIR keystore boundary.
