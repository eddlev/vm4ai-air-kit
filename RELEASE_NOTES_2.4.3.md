# AIR 2.4.3 — prepared release notes

> **Prepared release notes.** The GitHub Release is the publication authority. This file describes the current 2.4.3 source candidate and should be reconciled against the final release commit before publication.

## What changed

AIR 2.4.3 hardens the prompt-layer runtime around continuity, visible execution state, drift recovery, and release evidence.

### Runtime persistence and drift recovery

- AIR remains the controlling prompt-layer runtime after valid activation or Handoff restoration until the user explicitly ends AIR itself or a higher-precedence host/safety constraint prevents continuation.
- Task-level stop, blocker, rejection, review state, or backend unavailability does not silently deactivate AIR.
- Loss of runtime application, disappearance of the bound Orbit 0 contract, skipped required reconciliation, or silent fallback to ordinary/default host-model behavior routes through the runtime watchdog and alignment-recovery surface.

### Suspicion is not proof

- A user/operator report that AIR appears to have fallen back now triggers watchdog evaluation.
- The report itself is not enough to classify `DRIFT_DETECTED`.
- AIR distinguishes reported drift suspicion from established drift and records the evaluated result.

### Periodic alignment preflight

- Periodic alignment is evaluated at substantive user-turn entry.
- When due, `AIR_ALIGNMENT_CHECK` followed by `AIR_VALIDATION_REPORT` is a mandatory same-response formal-object pair.
- Lifecycle handlers, compact-object mode, or another watchdog check cannot silently defer or replace that pair.
- Discovering a missed required object later creates a visible process defect; late correction does not rewrite history as if the original emission was compliant.

### Intent-resolution hardening

The 2.4.3 executable contract includes the current intent-resolution gate/surface markers and verifies that they remain present in the release foundation. The goal is to stop materially ambiguous intent from being silently converted into operative project state.

### Stronger evidence and reproducibility contract

- AIR distinguishes executable reproducibility from model/evaluator replayability and manual review.
- Release-grade executable checks require external run identity, exact inputs/environment, repeated isolated executions, and matching decision fingerprints.
- A bare pass-count claim such as `150/150 tests passed` is not sufficient deterministic evidence.
- The repository reproducibility workflow runs the release manifest three times in separate network-disabled Docker containers and compares the resulting fingerprints.

### Specialist layer re-sealed to AIR 2.4.3

The specialist layer is aligned to the 2.4.3 foundation and current 2.3.6 package line.

Current package families include Grounding, AI Governance, Capability Ecology Architect, and the complete **Specification-First Verification Specialist Package 2.3.6**.

The SFV package now has a coherent domain package, method pack, specialist profile, executor layer, and package manifest. It remains a non-agent capability package: loading it does not transfer project authority away from the bound AIR artifact.

### Foundation versions

| Component | Version |
| --- | ---: |
| AIR Core Runtime | 2.4.3 |
| AIR Control Surface | 2.4.3 |
| AIR Governance Supplement | 2.2.0 |
| AIR Default Starter | 2.4.3 |
| AIR Handoff schema | 2.2.0 |
| Specialist package line | 2.3.6 |

## Public/release surface

The prepared 2.4.3 release also aligns the repository with the current AIR brand and website:

- Brand promise: **AI work, carried forward.**
- Brand signature: **Focused. Fluid. AIR.**
- README prioritizes the user problem and continuation outcome before implementation detail.
- `START_HERE.md` provides a short path for new projects, imports, and Handoff continuation.
- `COMPATIBILITY.md` separates maintainer-observed host behavior from certification/guarantees.
- The release-asset builder produces a deterministic `AIR-core.zip`, versioned copy, manifest, and SHA-256 checksums from the exact five-file foundation.

## Upgrade note

Use a coherent current foundation. Do not mix stale Core, Control, Starter, Governance, or Handoff components from different release sets merely because individual files still parse.

For a new session, load the current five-file foundation together. For Handoff continuation, load that same coherent foundation plus the populated Handoff Card being restored.

## Assurance boundary

AIR 2.4.3 remains a prompt-based runtime contract. This release does **not** claim:

- deterministic backend enforcement from the prompt-only kit
- hidden chain-of-thought or latent-state access
- guaranteed tool execution or correctness
- universal host/model compatibility
- legal, regulatory, security, or production certification

Claims about repositories, tests, deployments, sources, operator actions, or backend events require the corresponding external evidence.
