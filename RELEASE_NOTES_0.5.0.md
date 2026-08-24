# AIR Kit v0.5.0

**AI work, carried forward.**

AIR Kit v0.5.0 packages the current AIR runtime foundation and aligns the public repository, brand, onboarding surface, release evidence, and download path around the same product story.

> **Versioning note:** `v0.5.0` is the public AIR Kit release version. The bundled runtime components keep their own component versions: Core/Control/Starter `2.4.3`, Governance/Handoff `2.2.0`, and the current specialist package line `2.3.6`.

## Highlights

- Brand v2 positioning: **AI work, carried forward.**
- README rebuilt around the user problem, outcome, quick start, and direct download path.
- `START_HERE.md` added for new-project, import, and Handoff continuation routes.
- `COMPATIBILITY.md` separates maintainer observations from certification or universal compatibility claims.
- Deterministic `AIR-core.zip` packaging added with a machine-readable manifest and SHA-256 checksums.
- Release-grade executable evidence remains backed by three isolated, network-disabled runs plus decision-fingerprint comparison.
- Specification-First Verification is represented as the complete non-agent **2.3.6 specialist package**, not a standalone experimental method pack.

## Runtime persistence and drift recovery

The bundled AIR 2.4.3 foundation hardens prompt-layer continuity and visible runtime discipline:

- AIR remains the controlling prompt-layer runtime after valid activation or Handoff restoration until the user explicitly ends AIR itself or a higher-precedence host/safety constraint prevents continuation.
- Task-level stop, blocker, rejection, review state, or backend unavailability does not silently deactivate AIR.
- Loss of runtime application, disappearance of the bound Orbit 0 contract, skipped required reconciliation, or silent fallback to ordinary/default host-model behavior routes through the runtime watchdog and alignment-recovery surface.

## Suspicion is not proof

- A user/operator report that AIR appears to have fallen back triggers watchdog evaluation.
- The report itself is not enough to classify `DRIFT_DETECTED`.
- AIR distinguishes reported drift suspicion from established drift and records the evaluated result.

## Periodic alignment preflight

- Periodic alignment is evaluated at substantive user-turn entry.
- When due, `AIR_ALIGNMENT_CHECK` followed by `AIR_VALIDATION_REPORT` is a mandatory same-response formal-object pair.
- Lifecycle handlers, compact-object mode, or another watchdog check cannot silently defer or replace that pair.
- Discovering a missed required object later creates a visible process defect; late correction does not rewrite history as if the original emission was compliant.

## Intent-resolution hardening

The 2.4.3 executable contract includes the current intent-resolution gate/surface markers and verifies that they remain present in the release foundation. Material ambiguity must not be silently converted into operative project state.

## Stronger evidence and reproducibility contract

- AIR distinguishes executable reproducibility from model/evaluator replayability and manual review.
- Release-grade executable checks require external run identity, exact inputs/environment, repeated isolated executions, and matching decision fingerprints.
- A bare pass-count claim such as `150/150 tests passed` is not sufficient deterministic evidence.
- The repository reproducibility workflow runs the release manifest three times in separate network-disabled Docker containers and compares the resulting fingerprints.

## Specialist layer

The specialist layer is aligned to the 2.4.3 foundation and current 2.3.6 package line.

Current package families include Grounding, AI Governance, Capability Ecology Architect, and the complete **Specification-First Verification Specialist Package 2.3.6**.

The SFV package includes a domain package, method pack, specialist profile, executor layer, and package manifest. It remains a non-agent capability package: loading it does not transfer project authority away from the bound AIR artifact.

## Included component versions

| Component | Version |
| --- | ---: |
| AIR Kit release | 0.5.0 |
| AIR Core Runtime | 2.4.3 |
| AIR Control Surface | 2.4.3 |
| AIR Governance Supplement | 2.2.0 |
| AIR Default Starter | 2.4.3 |
| AIR Handoff schema | 2.2.0 |
| Specialist package line | 2.3.6 |

## Download and start

The release asset pipeline produces:

- `AIR-core.zip` — stable download name for the current AIR Kit core bundle
- `AIR-v0.5.0-core.zip` — version-pinned copy of the same bundle bytes
- `AIR_CORE_MANIFEST.json` — packaged-file identities, versions, hashes, release/version provenance, and assurance boundary
- `SHA256SUMS.txt` — SHA-256 checksums for the generated release assets

After extracting the core bundle, attach the five AIR foundation files to a capable AI session and send:

```text
Start a new AIR project.
```

See `START_HERE.md` for new-project, import, and Handoff continuation routes.

## Upgrade note

Use a coherent current foundation. Do not mix stale Core, Control, Starter, Governance, or Handoff components from different release sets merely because individual files still parse.

For a new session, load the current five-file foundation together. For Handoff continuation, load that same coherent foundation plus the populated Handoff Card being restored.

## Assurance boundary

AIR remains a prompt-based runtime contract. v0.5.0 does **not** claim:

- deterministic backend enforcement from the prompt-only kit
- hidden chain-of-thought or latent-state access
- guaranteed tool execution or correctness
- universal host/model compatibility
- legal, regulatory, security, or production certification

Claims about repositories, tests, deployments, sources, operator actions, or backend events require the corresponding external evidence.
