[![AIR by VM4AI — Configure. Organize. Execute.](https://github.com/eddlev/air-brand/raw/main/github/readme-header.png)](https://vm4ai.com)

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Framework](https://img.shields.io/badge/framework-prompt--runtime-9A8F80?labelColor=1A1613)](https://vm4ai.com/how-it-works.html)
[![Latest release](https://img.shields.io/github/v/release/eddlev/vm4ai-air-kit?label=release&labelColor=1A1613&color=FF5A1F)](https://github.com/eddlev/vm4ai-air-kit/releases)

**Structure for serious AI work. Configure. Organize. Execute.**

AIR (AI Resource) is a portable prompt-runtime framework for turning a loose AI conversation into cooperative project work with an explicit working contract: scope, one active step, uncertainty handling, evidence boundaries, approval gates, review, and handoff continuity.

AIR works inside capable chat/model interfaces. It does **not** turn a probabilistic host model into deterministic infrastructure. AIR records expose AIR's declared prompt-layer state; external actions and claims still require external evidence.

**Start here:** [How AIR works](https://vm4ai.com/how-it-works.html) · [Website](https://vm4ai.com/) · [Brand kit](https://github.com/eddlev/air-brand) · [Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions)

---

## Why use AIR?

AIR is useful when you want the AI session itself to keep a disciplined working contract instead of relying on a growing pile of conversational context. It can help you:

- keep exactly one material step active at a time
- surface blockers and material uncertainty instead of silently guessing
- establish what is allowed, forbidden, and required for closure
- keep claims bounded to available evidence
- route to specialist/domain/method support when the task needs it
- preserve compact project state across sessions and compatible model interfaces
- keep human direction and approval explicit

For the architecture, Orbit model, capability layers, handoff model, and visual explanations, see **[How AIR works](https://vm4ai.com/how-it-works.html)**.

## Quick start

For a fresh AIR project, attach the **current five foundation files** from [`prompts/`](prompts/):

1. `AIR_CORE_RUNTIME.md`
2. `AIR_CONTROL_SURFACE.md`
3. `AIR_GOV.md`
4. `AIR_DEFAULT_STARTER_PROFILE.json`
5. `AIR_HANDOFF_CARD_TEMPLATE.json`

Then type:

```text
Start a new AIR project.
```

AIR verifies the required files, emits the required fresh-boot session record, and begins onboarding at Q1. The activation phrase does **not** silently answer Q1.

### Context-window note

The complete files must fit in the host interface without truncation. Tokenization, attachment handling, and context limits vary by provider and model, so this repository does not claim one universal token threshold. If a host cannot load the complete required foundation set, do not treat a partial load as a valid AIR boot.

## Continue a project

A Handoff Card carries recorded AIR project state into a new compatible session. The receiving AIR runtime validates and rebinds that state; it does not guarantee byte-for-byte identical inference or hidden-state transfer.

Use the current foundation files required by the runtime plus your populated `AIR_HANDOFF_CARD`, then choose the handoff-continuation branch during onboarding.

## Assurance boundary

The public AIR Kit is prompt-based. It can materially shape how a host model approaches and reviews work, but it does not independently provide:

- backend or hook-level enforcement
- guaranteed tool execution
- tamper-evident or signed receipts
- hidden chain-of-thought or latent-state telemetry
- guaranteed correctness
- legal, regulatory, security, or production certification

When a claim depends on something outside the prompt runtime—tests, repository state, deployment, a source, an operator action, a tool call, or a backend event—the corresponding external evidence is required.

A host adapter or backend can strengthen the same contract with deterministic hooks, permission interception, independent tests, receipts, and action blocking. Those capabilities must not be attributed to the prompt-only kit unless they actually exist and are evidenced.

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
  specification first method pack/

docs/
  current regression material + historical audit/patch records
```

The files under `prompts/` are the current foundation. Specialist and method packages are **available but unbound** until selected, validated for the task, and bound according to the runtime. Historical audit and patch records are evidence/history, not current runtime authority.

## Machine-readable records

AIR uses structured records (often JSON) because they are portable and machine-readable. **JSON is a representation, not the assurance claim.** A model-generated AIR record documents declared AIR state; it is not independent proof merely because it is structured.

## License and brand

The project code and prompt materials are licensed under Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

The AIR/VM4AI names and brand marks are separate from the code license. Reusable logos, visualizations, design tokens, and the “Made with AIR” mark live in the [AIR brand repository](https://github.com/eddlev/air-brand).

---

The AIR brand system and vm4ai.com are developed using AIR with human review and approval. See the public site for the current account and examples.
