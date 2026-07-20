# AIR Dependency Matrix

| Component | Mandatory | Dependency | Fallback |
|---|---:|---|---|
| Prompt boot | Yes for prompt use | LLM interface capable of loading the selected files | None; use a smaller modular bundle if context is insufficient |
| Modular boot tool | Optional | Python 3 standard library | Attach monolithic prompt files manually |
| Handoff signer/verifier | Optional | `rfc8785`, `cryptography` from pinned requirements | Structural unauthenticated handoff inspection |
| OPA adapter | Optional | OPA binary; wrapper shell; Python 3 or jq for envelope handling | Prompt-simulated policy posture with explicit limitation |
| Source adapters | Optional | Referenced datasets and licence/access conditions | Local source-light or user-supplied evidence route |

Optional dependencies never become baseline AIR requirements merely because their adapters are shipped.
