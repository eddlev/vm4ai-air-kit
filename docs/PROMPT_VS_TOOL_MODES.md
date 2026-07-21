# Prompt-side and Local Tool-evaluated Modes

| Property | Prompt-side AIR | Installed/local tool observation |
|---|---|---|
| Runtime origin | `PROMPT_COMPILED` | Still prompt-compiled unless a real backend exists |
| Canonical resources | Files attached or loaded by the AI interface | Build-verified resources embedded in the installed package |
| File hashes | Model-declared or file-layer observed | Calculated by local code from observed bytes |
| Project state | Conversation artifacts and handoffs | Registered project workspace files and receipts |
| Module selection | Model interpretation or legacy manifest plan | Stage 3 migration pending |
| Policy decision | `PROMPT_SIMULATED` | Stage 5 local OPA migration pending |
| Handoff trust | Structural/unauthenticated | Stage 4 signature and local-anchor migration pending |
| Execution authorization | AIR_GATE plus user approval | AIR_GATE plus user approval; local tool results do not replace it |
| Compliance claim | Not established | Not established |
| Backend enforcement | Not established | Not established by the installed application |

Use the strongest evidence class actually available and retain its limitations.

A package install, resource digest, operation receipt, or passing local test proves only the bounded observation it records.
