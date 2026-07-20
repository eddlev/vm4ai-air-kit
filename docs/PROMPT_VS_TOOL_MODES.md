# Prompt-only and Tool-evaluated Modes

| Property | Prompt-only | Tool-evaluated |
|---|---|---|
| Runtime origin | `PROMPT_COMPILED` | Still prompt-compiled unless a backend exists |
| File hashes | Model-declared or file-layer observed | Calculated by local tool |
| Module selection | Model interpretation | Manifest-driven local plan |
| Policy decision | `PROMPT_SIMULATED` | OPA tool result with provenance |
| Handoff trust | Structural/unauthenticated | Signature and local anchor evaluation |
| Execution authorization | AIR_GATE + user approval | AIR_GATE + user approval; tool result does not replace it |
| Compliance claim | Not established | Not established |
| Backend enforcement | Not established | Not established by these tools |

Use the strongest evidence class actually available and retain its limitations.
