[![AIR by VM4AI — Configure. Organize. Execute.](https://github.com/eddlev/air-brand/raw/main/github/readme-header.png)](https://vm4ai.com)

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Framework](https://img.shields.io/badge/framework-prompt--runtime-9A8F80?labelColor=1A1613)](https://vm4ai.com/how-it-works.html)
[![Latest release](https://img.shields.io/github/v/release/eddlev/vm4ai-air-kit?label=release&labelColor=1A1613&color=FF5A1F)](https://github.com/eddlev/vm4ai-air-kit/releases)

**Structure for serious AI work. Configure. Organize. Execute.**

AIR (AI Resource) is a portable prompt-runtime framework for turning a loose AI conversation into cooperative project work with an explicit working contract: scope, one active step, uncertainty handling, evidence boundaries, approval gates, review, and handoff continuity.

AIR works inside capable chat/model interfaces. It does **not turn a probabilistic host model into deterministic infrastructure**. AIR records expose declared prompt-layer state; claims about tests, tools, repositories, deployments, sources, or backend events still require the corresponding external evidence.

**Start here:** [How AIR works](https://vm4ai.com/how-it-works.html) · [Website](https://vm4ai.com/) · [Brand kit](https://github.com/eddlev/air-brand) · [Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions)

---

## Why use AIR?

AIR is useful when you want the AI session itself to keep a disciplined working contract instead of relying on an ever-growing pile of conversational context. It can help you:

- keep one material step active at a time
- surface blockers and material ambiguity instead of silently guessing
- make allowed, forbidden, approval-gated, and closure conditions explicit
- keep claims bounded to available evidence
- route to specialist, domain, or method support when the task needs it
- preserve compact project state across sessions and compatible model interfaces
- keep human direction, review, and approval visible

For the Orbit model, capability layers, handoff model, and visual architecture, see **[How AIR works](https://vm4ai.com/how-it-works.html)**.

## Quick start

For a fresh AIR project, attach the **current five foundation files** from [`prompts/`](prompts/):

1. [`prompts/AIR_CORE_RUNTIME.md`](prompts/AIR_CORE_RUNTIME.md)
2. [`prompts/AIR_CONTROL_SURFACE.md`](prompts/AIR_CONTROL_SURFACE.md)
3. [`prompts/AIR_GOV.md`](prompts/AIR_GOV.md)
4. [`prompts/AIR_DEFAULT_STARTER_PROFILE.json`](prompts/AIR_DEFAULT_STARTER_PROFILE.json)
5. [`prompts/AIR_HANDOFF_CARD_TEMPLATE.json`](prompts/AIR_HANDOFF_CARD_TEMPLATE.json)

Then type:

```text
Start a new AIR project.
```

AIR validates the supplied foundation, emits the required fresh-boot state, and begins onboarding at Q1. The activation phrase does **not** silently answer Q1.

### Context-window and load-integrity note

The complete required files must fit in the host interface without truncation. Tokenization, attachment handling, and context limits vary by provider and model, so this repository does **not** claim one universal token threshold. A partial or truncated foundation load is not a valid AIR boot.

## Continue a project

An `AIR_HANDOFF_CARD` carries recorded AIR project state into a new compatible session. The receiving AIR runtime validates and rebinds that state; a handoff does not promise byte-for-byte identical inference or hidden-state transfer.

Load the current foundation required by the runtime together with the populated Handoff Card, choose the continuation branch, and continue from the restored active state. The Handoff Card is a continuity object; it does not replace the runtime foundation.

## Assurance boundary

The public AIR Kit is prompt-based cooperative behavioral governance. It can materially shape how a host model frames, executes, reviews, and hands off work, but the prompt-only kit does not independently provide:

- deterministic backend or hook-level enforcement
- guaranteed tool execution
- tamper-evident or signed receipts
- hidden chain-of-thought or latent-state telemetry
- guaranteed correctness
- legal, regulatory, security, or production certification

When a claim depends on something outside the prompt runtime—tests, repository state, deployment state, a source, an operator action, a tool call, or a backend event—the matching external evidence is required.

A client, tool gateway, or backend can strengthen the same contract with deterministic hooks, permission interception, independent tests, receipts, and action blocking. Those capabilities must not be attributed to the prompt-only kit unless they actually exist and are evidenced.

## Test evidence and reproducibility

AIR separates the request to surface evidence from the independent proof that an execution was reproducible.

- `air -t off` is the default `SUMMARY_ONLY` test-evidence mode.
- `air -t on` enables `FULL_TEST_EVIDENCE` for subsequent runs. It does not retroactively reconstruct missing evidence.
- `REPRODUCIBLE_EXECUTABLE` is for executable checks whose run identity, exact inputs, environment, randomness/network policy, and repeated results are externally recorded and compared.
- `REPLAYABLE_EVALUATION` is for model/evaluator runs that can be replayed from recorded inputs but are not claimed deterministic in the executable sense.
- `MANUAL_REVIEW_REQUIRED` stays separate from automated pass counts.

For a release-grade deterministic claim, AIR requires an external run identity and repeatability evidence, including exact suite/input identities and isolated repeat executions with matching decision fingerprints. A naked `150/150 passed` is not enough to establish determinism.

The repository's permanent reproducibility workflow implements this contract for the executable AIR release checks.

## Canonical system modifiers

The current system-modifier surface is intentionally small:

```text
air -o on
air -o -min
air -t on
air -t off
```

These are prompt-side controls. They do not bypass approval, evidence, scope, or release gates.

## Repository map

```text
prompts/
  AIR_CORE_RUNTIME.md
  AIR_CONTROL_SURFACE.md
  AIR_GOV.md
  AIR_DEFAULT_STARTER_PROFILE.json
  AIR_HANDOFF_CARD_TEMPLATE.json

profiles/
  grounding specialist/
  governance specialist/
  capability ecology architect/

methods/
  specification-first verification material

docs/
  current regression material + historical audit/patch records

tests/
  deterministic/replayable AIR verification harness
```

The files under `prompts/` are the current foundation. Specialist, domain, and method packages are **available but unbound** until selected, compatibility-validated, approved when required, and bound according to the runtime. Historical patch and audit records are evidence/history, not current runtime authority.

## Machine-readable records

AIR uses structured records, often JSON, because they are portable and machine-readable. **JSON is a representation, not the assurance claim.** A model-generated AIR record documents surfaced or source-supported AIR state according to its evidence class; it is not independent proof merely because it is structured.

## Documentation

- [How AIR works](https://vm4ai.com/how-it-works.html) — public architecture and visual explanation
- [`docs/AIR_DRIFT_REGRESSION_MATRIX.md`](docs/AIR_DRIFT_REGRESSION_MATRIX.md) — current drift/regression expectations
- [`docs/AIR_MODEL_PORTABILITY_NOTES.md`](docs/AIR_MODEL_PORTABILITY_NOTES.md) — empirical portability notes
- [`docs/`](docs/) — additional current guidance and historical audit records

## License and brand

The project code and prompt materials are licensed under Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

The AIR/VM4AI names and brand marks are separate from the code license. Reusable logos, visualizations, design tokens, and the “Made with AIR” mark live in the [AIR brand repository](https://github.com/eddlev/air-brand).

---

The AIR brand system and vm4ai.com are developed using AIR with human review and approval. See the public site for the current account and examples.
