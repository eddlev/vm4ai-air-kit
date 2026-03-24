# Case Studies — vm4ai-air-kit

## Purpose

This folder contains concrete examples of AIR in practice.

The goal of the case studies is to show what AIR changes in live sessions compared with normal prompting or loosely structured interaction.

Case studies should help answer questions like:

- What does AIR improve?
- Where does AIR still struggle?
- How does explicit contract activation change behavior?
- How does AIR behave across models?
- What happens when a task narrows into a sub-contract?
- What does a better handoff look like?

This folder is where AIR becomes demonstrable rather than only theoretical.

---

## What belongs here

Case studies should focus on **real session behavior**.

Good case studies include:
- a clear task or problem
- the starting context
- the contract or profile used
- the output produced
- the observed differences from baseline prompting
- what worked
- what failed
- what changed after patching, updating, or switching contracts

Case studies should be:
- sanitized
- reproducible where possible
- concise
- focused on one question at a time

---

## Recommended case study structure

Each case study should include the following sections.

### 1. Title
A short descriptive title.

Example:
- `callerwall_trust_contract_vs_baseline.md`
- `contract_activation_failure_and_fix.md`
- `gemini_vs_claude_air_artifact_comparison.md`

### 2. Problem
What was being attempted?

Example:
- compile a trust contract
- continue a live project across sessions
- switch from one AIR contract to another
- compare AIR vs normal prompting
- test handoff continuity

### 3. Initial setup
What was provided to the model?

Include:
- model used
- prompts used
- AIR profile used
- evidence/input attached
- whether this was a new session or continuation

### 4. Expected AIR behavior
What should have happened under correct AIR execution?

Examples:
- explicit `AIR_SESSION`
- correct Orbit 0 activation
- correct use of outer-orbit contracts
- artifact-first response
- fail-closed handling of uncertainty

### 5. Observed behavior
What actually happened?

Examples:
- prose-first answer
- contract treated as candidate instead of activated
- wrong active contract
- proper AIR artifact
- good blocker surfacing
- token blow-up due to prompt echoing

### 6. Analysis
Why did the model behave that way?

This section should focus on:
- contract handling
- orbit behavior
- artifact quality
- evidence discipline
- drift or blending
- model-specific strengths/weaknesses

### 7. Fix or adjustment
What changed after the issue was identified?

Examples:
- update activation prompt
- add explicit Orbit 0 promotion rule
- add minimal execution mode
- add handoff rule
- tighten artifact structure requirements

### 8. Result after adjustment
Did the fix work?

Describe:
- what improved
- what remained weak
- whether the case is now considered successful

### 9. Takeaways
Short bullet list of the main lessons.

---

## Categories of case studies

## 1. AIR vs normal prompting

These studies compare:
- baseline prompt behavior
- AIR-guided behavior

Good focus areas:
- drift resistance
- blocker surfacing
- fail-closed behavior
- state clarity
- handoff quality

Example questions:
- Does AIR reduce hallucinated confidence?
- Does AIR improve continuity?
- Does AIR produce more implementation-ready output?

---

## 2. Contract activation studies

These studies focus on whether the model correctly:
- activates the attached contract
- promotes it to Orbit 0
- preserves outer-orbit context
- avoids candidate/readiness limbo

Good focus areas:
- active contract precedence
- contract narrowing
- sub-contract promotion
- parent/child/sibling contract relations

These are especially important because AIR can fail even when the reasoning is good if the contract is not actually activated.

---

## 3. Orbit behavior studies

These studies focus on:
- Orbit 0 correctness
- outer-orbit context handling
- conflict handling
- promotion / supersession / retirement behavior

Good focus areas:
- whether prior contracts are silently blended
- whether the current active contract governs correctly
- whether state transitions are explicit

---

## 4. Handoff continuity studies

These studies focus on moving work from one session to the next.

Good focus areas:
- handoff card quality
- whether a new session rebinds to the correct task
- whether AIR can continue without full transcript replay
- whether the handoff remains compact and sufficient

---

## 5. Cross-model comparisons

These studies compare AIR behavior across models.

Examples:
- ChatGPT
- Gemini
- Claude

Good focus areas:
- contract activation correctness
- artifact normalization quality
- drift tendency
- prose-first vs artifact-first discipline
- quality of dependency edges
- quality of missing vector handling

These studies do not need formal benchmarking to be useful. Structured qualitative comparison is enough.

---

## 6. Domain-specific studies

These studies focus on how AIR behaves in different domains, for example:
- technical / security
- research synthesis
- creative / brand
- GTM / sales
- relational / symbolic

Good focus areas:
- whether the default starter profile was enough
- when a specialized profile became necessary
- whether geometry assumptions helped or constrained the work

---

## Suggested case study template

Use this structure when writing new case studies:

```md
# [Case Study Title]

## Problem

## Initial setup

## Expected AIR behavior

## Observed behavior

## Analysis

## Fix or adjustment

## Result after adjustment

## Takeaways