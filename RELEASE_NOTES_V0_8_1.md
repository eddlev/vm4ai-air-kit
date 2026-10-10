# AIR Kit v0.8.1 — Release Candidate Notes (R133)

> Public AIR Kit version: **v0.8.1 release candidate** — not yet promoted.  
> Candidate: `R23-AMRS6-V0.8.1-R133-CANDIDATE-R3-20261009`  
> Client artifact: `AIR_P_COMPLETE_CLIENT_RELEASE_20261009_R23_V0_8_1_R133_CANDIDATE_R3.zip`  
> SHA-256: `e66b8d4a761d374d2023d9190db8a266303a0ee9afaafd1dbf89ce348b331730`  
> Latest published release: [v0.8.0](https://github.com/eddlev/vm4ai-air-kit/releases/tag/v0.8.0)

## What changed since v0.8.0

v0.8.1 keeps the AMRS-6 R23 runtime identities promoted in v0.8.0 (Core 2.9.0, Control 2.7.0, Governance 2.4.0, Starter 2.7.0, Handoff schema 2.3.0 / template revision 26, Route Map 1.2.5, Specialist Index 1.3.15) and changes the following.

### Repository alignment

- The repository now carries the compiled AIR-P client runtime (`air_p/`), the canonical source tree (`source/`), the law-source package and the five Specialist distributions. Before v0.8.1, the repository's `prompts/`, `catalog/` and `profiles/` still held v0.7.4-era files while v0.8.0 shipped only as a release ZIP.
- `profiles/` is replaced by `specialists/`; the Specialist packages and `catalog/AIR_SPECIALIST_PACKAGE_INDEX.json` are carried forward byte-for-byte from the v0.8.0 client.
- CI no longer routes through the v0.7.4 release seal. `tools/validate_air_suite.py` enforces the v0.8.1 source-and-runtime contract.

### Boot dispatch and Handoff metadata (R131)

- The five canonical first messages are explicit: `Start a new AIR-P project.` (default, Tier0) plus explicit `Tier0`–`Tier3` boot requests.
- Tier0 retrieval is bounded by an exact-section guard: adjacent context outside the allowed boundary is discarded before model-visible ingestion.
- Stale current-Handoff metadata in the Starter is reconciled to template revision 26.

### Deterministic law-source resolution (R132)

- 25 Starter deterministic checks now bind to a single exact, SHA-pinned `law_source/...` body (installed as `air_p/law_package/...`) instead of the Core prompt. Tier3 resolves each binding by exact path, byte length and SHA-256, and fails closed on any mismatch.

### First-activation emission latch (R133)

- New Control section `AIR_CONTROL_FIRST_ACTIVATION_EMISSION_LATCH_V1` and Starter contract `$.compiler_contract.first_activation_emission_latch`, reachable through two new SHA-pinned direct anchors (runtime reference index: 17 → 19 anchors).
- When the final required Q6 or Q6D answer is accepted, AIR must finish onboarding resolution (including Q4D base and every Q6D subchoice), activate through `RT.ACTIVATE`, and visibly emit `AIR_RUNTIME_BRIDGE`, `AIR_SESSION`, `AIR_PROJECT_INITIALIZATION_BRIEF`, `AIR_PROJECT_EXECUTION_MAP` and `AIR_ARTIFACT`, each as an object-name line plus a fenced JSON block, before any task-domain work.
- Neither `ALL_OBJECTS` nor explicit minimum mode can hide these objects. If construction, binding, validation or emission fails, activation blocks; a missed emission cannot be made retrospectively compliant.
- No new Core law, backend authority, execution permission or formal object type is introduced.

## Source lineage

| Revision | Canonical source tuple (SHA-256) | Changed source files |
| --- | --- | --- |
| R130 | — | v0.8.0 baseline |
| R131 | `d4678f03448f35c713c11565069715c6fd168bda50601b04a445e86f0f0fce64` | compiler engine, compiler tests, Starter |
| R133 | `a7c4208d0bbbed201af504541809e183eeb5f4cac7755f91e00db84b388a9198` | compiler engine, compiler entrypoint, compiler tests, Control, Starter |

The deltas are recorded in `release/SOURCE_DELTA_R130_TO_R131_V081_CANDIDATE.json` and `release/SOURCE_DELTA_R131_TO_R133_V081_CANDIDATE.json`. The 114 law-package members are unchanged.

## Runtime identity

- Runtime state: `R23_AMRS4F_PACKAGE_ENABLED_SEMANTIC_OWNER_CUTOVER`; target AMRS: 6
- 113 components, 22 routes, 22 control events, 21 formal objects, 83 laws, 28 floor invariants
- 137 deterministic checks; 11-contract Tier0 turn-governance kernel; 19 direct runtime-reference anchors
- Client runtime aggregate (140 `air_p/` files): `4c258a738db3b7129f9509cff1d73dfe1cbef099678327226bf69a508ca2c701`
- Derived 142-file build inventory: `404cb452c24c7627f91ea9aa211a3057b2335d8cd242a0de8349401b8accdf06`
- Control SHA-256: `8d37232f4784507bd52d141ceec9f75907cb37e9999a3111bfb2cb7dbe615fe0`
- Starter SHA-256: `811351c68660ab290b3637f972fff4389ba1f1d9af72232bd0a9c7c65b53bbd0`

## Validation and acceptance status

Completed:

- static deterministic release closure of the candidate client: 180 distribution pins, 179 boot-manifest pins, 140 `air_p/` client files, zero script payloads;
- recorded candidate build evidence: 76/76 compiler unit tests, 137/137 deterministic checks, 19/19 direct runtime-reference anchors and three byte-identical builds.

Not yet run for this candidate:

- fresh-session Tier3 integrity audit;
- first-activation (Q6/Q6D → `RT.ACTIVATE`) visible-emission behavioral acceptance;
- end-to-end boot-performance acceptance.

Static integrity does not establish host-model behavior. v0.8.1 is promoted to a release only after these acceptance checks pass and a separate release decision is made.
