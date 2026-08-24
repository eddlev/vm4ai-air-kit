# AIR compatibility notes

AIR is prompt-based. Compatibility therefore depends on the host interface and model being able to load the complete AIR foundation and follow its required instruction, object, binding, evidence, and continuity discipline.

This page records **maintainer-observed compatibility**, not vendor certification. Provider behavior, model versions, context windows, attachment handling, system instructions, and product guardrails can change independently of AIR.

## Maintainer-observed matrix

| Host / model family | Observed status | Scope of observation |
| --- | --- | --- |
| ChatGPT / capable frontier models | Working in maintainer use | New-project work, structured objects, sustained project execution, Handoff-style continuity. Host/model versions still matter. |
| Claude / capable frontier models | Working in maintainer use | Sustained AIR project work and structured continuity observed. |
| Gemini / capable frontier models | Working in maintainer use | Sustained AIR project work and structured continuity observed. |
| Grok / capable frontier models | Working in maintainer use | Sustained AIR project work observed; host-specific context behavior can affect continuity. |
| Mistral / capable frontier models | Working in maintainer tests | AIR foundation and structured work observed on sufficiently capable configurations. |
| Selected frontier local models | Variable / configuration-dependent | Some sufficiently capable local models have run AIR; weaker models or constrained context windows may fail to hold the full contract reliably. |
| GitHub Copilot tested configuration | Not viable in maintainer test | The tested setup's instruction/guardrail/context constraints interfered with reliable AIR operation. This is **not** a permanent claim about every Copilot product or future configuration. |
| Other hosts / model versions | Untested or unverified | No compatibility claim is made until there is direct evidence. |

## What “working” means here

A host is not considered compatible merely because it can echo AIR vocabulary or emit JSON.

A useful compatibility observation should include enough of the following to show that the host can actually sustain the contract:

- load the complete coherent five-file foundation without material truncation
- preserve AIR as the controlling prompt-layer runtime once activated
- keep exactly one bound Orbit 0 task/artifact during material execution
- emit required canonical AIR objects when their triggers occur
- respect approval, scope, evidence, ambiguity, and action-governance boundaries
- create and restore recorded Handoff state without pretending hidden state was transferred
- recover visibly from detected runtime drift instead of silently falling back to ordinary/default behavior

Different use cases exercise different parts of AIR, so one successful boot is weaker evidence than sustained project work plus Handoff/recovery behavior.

## Why results can differ

AIR runs inside the host rather than replacing it. Differences can come from:

- model instruction-following capability
- available context window and effective attachment budget
- host system instructions and safety constraints
- whether files are fully available to the model
- tool and connector behavior
- model/provider updates during a project
- session summarization or context-management behavior outside AIR

AIR does not erase those host limitations.

## Report a compatibility result

Please post field reports in [GitHub Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) using a compact format like this:

```text
Platform/provider:
Model/version (if visible):
AIR version:
Route: new project / import / Handoff continuation
How the foundation was loaded: attachments / project files / prompt / other
What you tested:
Result: working / partial / failed
Observed limitation or failure:
Reproduction notes:
```

Useful reports include failures. A specific limitation is more valuable than a generic “works for me.”

## Claim boundary

This matrix is first-party observational evidence from AIR maintainers unless a row explicitly says otherwise. It is not an independent benchmark, vendor endorsement, certification, guarantee of future compatibility, or claim that every model/version on a named platform behaves identically.
