# AIR Installation Matrix

AIR does not require a conventional installation for prompt-only use.

| Mode | Windows | macOS | Linux | Dependencies | Network |
|---|---|---|---|---|---|
| Monolithic prompt boot | Supported | Supported | Supported | Capable LLM interface | Provider-dependent |
| Modular boot | Python 3.10+; `.cmd`/PowerShell wrappers | Python 3.10+; shell wrapper | Python 3.10+; shell wrapper | Python standard library | Not required |
| Handoff integrity tool | Python 3.10+ | Python 3.10+ | Python 3.10+ | Pinned packages in `runtime/handoff/tools/requirements.txt` | Not required after install |
| OPA local CLI | PowerShell or direct OPA CLI | shell + OPA | shell + OPA | OPA; Python 3 or jq depending wrapper | Not required |
| OPA loopback server | Supported | Supported | Supported | OPA | Loopback only |

## Prompt-only setup

Download the repository or release archive and attach files from `prompts/`.

## Modular setup

Keep the repository taxonomy intact. The module manifest uses paths relative to the repository root.

```bash
python runtime/boot/tools/air-boot.py validate-manifest
```

## Permissions

The shipped tools do not require administrator privileges, system services, or public network listeners. Store signing keys outside the repository and restrict their filesystem permissions.
