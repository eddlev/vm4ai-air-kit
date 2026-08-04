[![AIR by VM4AI — Configure. Organize. Execute.](https://github.com/eddlev/air-brand/raw/main/github/readme-header.png)](https://vm4ai.com)

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Schema](https://img.shields.io/badge/schema-AIR__V2-FF5A1F?labelColor=1A1613)](prompts/AIR_CORE_RUNTIME.md)
[![Runtime](https://img.shields.io/badge/runtime-prompt--compiled-9A8F80?labelColor=1A1613)](#what-air-is)
[![Execution](https://img.shields.io/badge/execution-one%20Orbit%200-C9A227?labelColor=1A1613)](#the-execution-loop)

**Structure for serious AI work. Configure. Organize. Execute.**

AIR — **AI Resource** — is a prompt-layer compiler/runtime contract for turning an ordinary model session into structured project execution. The user directs intent, constraints, corrections, and approvals. AIR keeps the active task, evidence, scope, blockers, evaluation, delivery state, and continuity explicit.

**Website:** [vm4ai.com](https://vm4ai.com) · **Brand:** [eddlev/air-brand](https://github.com/eddlev/air-brand) · **Discussions:** [Ask and share](https://github.com/eddlev/vm4ai-air-kit/discussions)

---

## What AIR is

```mermaid
flowchart LR
    U[User intent<br/>constraints + approvals] --> B[Bootstrap + onboarding]
    B --> C[Compile AIR_ARTIFACT]
    C --> P{Binding precheck}
    P -->|pass| O[Exactly one Orbit 0<br/>active execution binding]
    P -->|missing or conflicting| R[Review / evidence / rescope]
    O --> E[Execute active step]
    E --> J[Task-scoped synthetic benchmark]
    J --> G{AIR_GATE}
    G -->|approve| D[Receiver-facing output]
    G -->|review| R
    G -->|reject| X[Reject report]
    D --> H[Update state or handoff]
    H --> O
```

AIR is **cooperative, not autonomous**. It does not create independent authority, legal status, professional credentials, backend enforcement, hidden-reasoning access, or guaranteed correctness.

Prompt-compiled AIR can improve structure, continuity, reviewability, and execution discipline inside a model session. It is not the private VM4AI backend/client runtime.

---

## The execution loop

```mermaid
stateDiagram-v2
    [*] --> Bootstrap
    Bootstrap --> BindingTransaction: onboarding + sources
    BindingTransaction --> BoundExecution: one candidate passes precheck
    BindingTransaction --> Recovery: missing / stale / conflicting state
    Recovery --> BindingTransaction: resolve and revalidate
    BoundExecution --> BindingTransaction: task switch or rebind
    BoundExecution --> Handoff: pause or continue elsewhere
    BoundExecution --> Complete: accepted output and closure
    Handoff --> BindingTransaction: restore + precheck
    Complete --> [*]
```

Three rules carry most of AIR's logic:

1. **One active artifact.** Material execution is authorized only by exactly one bound `AIR_ARTIFACT` in Orbit 0.
2. **Evidence before claims.** Unsupported, stale, ambiguous, or permission-blocked material claims route to review, evidence required, rescope, or rejection.
3. **Visible state changes.** Binding, task switches, blockers, approvals, handoff, mutation, and closure do not happen silently.

---

## Orbit model

```mermaid
flowchart TB
    O0[Orbit 0<br/>one executing task artifact]
    O1[Orbit 1<br/>near-term paused or queued artifacts]
    O2[Orbit 2<br/>deferred or dependency-blocked artifacts]

    O1 -->|promote through binding transaction| O0
    O0 -->|pause or task switch| O1
    O0 -->|defer| O2
    O2 -->|dependency resolved| O1
```

Orbit is task state, not conversational importance. Queued artifacts may inform planning, but they do not execute until promoted and bound.

---

## Runtime stack

```mermaid
flowchart TB
    CR[AIR_CORE_RUNTIME.md<br/>canonical state + lifecycle + gates]
    GV[AIR_GOV.md<br/>approval scope + source rights + governance]
    CS[AIR_CONTROL_SURFACE.md<br/>visible interaction + state rendering]
    DS[AIR_DEFAULT_STARTER_PROFILE.json<br/>conservative bootstrap capability posture]
    HC[AIR_HANDOFF_CARD_TEMPLATE.json<br/>portable continuation state]

    CR --> GV
    GV --> CS
    CS --> DS
    CR --> HC

    SP[Specialist profile<br/>capability posture] -. selected and compiled .-> CR
    DP[Domain package<br/>terminology + constraints + evidence] -. informs .-> SP
    MP[Method pack<br/>procedure + step gates] -. governs procedure .-> SP
    EX[Executor layer<br/>bounded operations] -. authorized by Orbit 0 .-> MP
```

The foundation is always subordinate to the Core Runtime's canonical object classes, lifecycle, gate decisions, binding rules, and floor invariants. Optional packages are **available, not active**, until validated, selected, and compiled into or referenced by the bound Orbit 0 artifact.

---

## Quick start

Attach the five canonical foundation files from [`prompts/`](prompts/):

```text
AIR_CORE_RUNTIME.md
AIR_CONTROL_SURFACE.md
AIR_GOV.md
AIR_DEFAULT_STARTER_PROFILE.json
AIR_HANDOFF_CARD_TEMPLATE.json
```

Then type:

```text
Start a new AIR project.
```

AIR verifies load integrity, prints the required boot state, says `Welcome to AIR.`, and begins at Q1. The activation phrase starts the bootstrap route; it does **not** answer Q1 for you.

### Continue from a handoff

Attach the relevant current foundation files plus your completed `AIR_HANDOFF_CARD`, then type:

```text
Continue project from handoff card.
```

A handoff is restoration input, not execution authority. AIR rechecks current files, sources, permissions, compatibility, approvals, and binding before resuming.

---

## Grounding package

The complete Grounding package lives in [`profiles/grounding specialist/`](profiles/grounding%20specialist/):

```text
AIR_GROUNDING_DOMAIN_PACKAGE.json
AIR_GROUNDING_METHOD_PACK.json
AIR_GROUNDING_SPECIALIST.json
AIR_GROUNDING_EXECUTOR.json
AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json
```

```mermaid
flowchart LR
    D[Domain package<br/>claim hygiene + viability + constraints]
    M[Method pack<br/>evidence-gated grounding procedure]
    S[Specialist<br/>cooperative challenge + task benchmark]
    E[Executor<br/>bounded authorized operations]
    A[Bound Orbit 0 AIR_ARTIFACT]

    D --> M
    D --> S
    M --> S
    D --> E
    M --> E
    S --> E
    A -->|sole positive execution authority| E
```

Use Grounding when ambitious, uncertain, frontier, or high-claim work needs reality binding without flattening the underlying ambition. It separates what is evidenced now, what is executable, what remains frontier work, what is blocked, and what is still unknown.

---

## Decision and delivery states

```mermaid
flowchart LR
    W[Work candidate] --> A{AIR_GATE}
    A -->|APPROVE| AO[APPROVED_OUTPUT]
    A -->|REVIEW / EVIDENCE_REQUIRED / RESCOPE_REQUIRED| RG[REVIEW_GATE]
    A -->|REJECT| RR[REJECT_REPORT]
```

An approval is scoped to the exact gate and authorized action identifiers. Approval of a plan does not automatically authorize file mutation, publication, deployment, release, storage, redistribution, or destructive action.

---

## Repository map

```text
prompts/                         AIR v2 foundation
profiles/grounding specialist/  complete Grounding package
docs/                            supporting documentation
README.md                        visual orientation and quick start
```

Canonical operational filenames use ASCII letters, numbers, underscores, hyphens, and periods. Transport counters such as `(10)` are not versions and are not retained in repository filenames.

---

## What AIR is for

AIR is useful when work benefits from explicit scope, active-step discipline, evidence-aware claims, review before delivery, reusable methods, specialist routing, or continuity across sessions. Typical uses include software and systems design, research synthesis, architecture and security review, product and operational planning, documentation work, governance-adjacent analysis, and long-running multi-step projects.

AIR is deliberately not “faster vibes.” It is a structure for making model-assisted work easier to inspect, challenge, continue, and trust proportionately.

---

## License

Licensed under the [Apache License 2.0](LICENSE). See [NOTICE](NOTICE) for attribution and project notices.
