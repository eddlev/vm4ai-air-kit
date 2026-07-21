# AIR Dependency Matrix

| Component | Mandatory | Dependency | Fallback |
|---|---:|---|---|
| Installed `air` application | Yes for installed use | Python 3.11+, `platformdirs` | Complete AIR Prompt Set |
| Package build | Development/release only | Hatchling, `build` | None for producing an official wheel |
| Package metadata validation | Development/release only | Twine | Manual archive inspection is insufficient for release closure |
| Source and integration tests | Development only | Pytest | None for test evidence |
| Installed-resource resolver | Baseline | Python standard library plus packaged AIR resources | Explicit `AIR_RESOURCE_ROOT` for development only |
| Project workspace manager | Baseline | Python standard library, `platformdirs` | None for installed project isolation |
| Deterministic boot compiler | Installed local application | Python 3.11+ and packaged AIR resources | Complete AIR Prompt Set |
| Legacy `air-boot.py` adapter | Compatibility only | Same installed Python services plus explicit source override | `air boot` commands |
| Handoff signer/verifier | Stage 4 migration | `rfc8785`, `cryptography` | Structural unauthenticated inspection |
| OPA adapter | Stage 5 migration | operator-controlled OPA binary | Prompt-simulated policy posture with limitation |
| Source adapters | Optional | referenced datasets and licence/access conditions | user-supplied or source-light evidence route |

Optional dependencies never become baseline AIR requirements merely because an adapter is shipped.

The installed application does not introduce telemetry, a central AIR service, automatic package downloads, or hidden credential handling.
