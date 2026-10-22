# AIR-P — Engineering Verification Method (ATDD + TDD), research R1

**Status:** SOURCE-OWNER-APPROVED METHODOLOGY / DOCUMENTATION-ONLY / NONOPERATIVE  
**Branch:** \`research/engineering-verification-atdd-tdd-r1\`  
**Planning baseline:** \`air/v0.8.1-source-sync\` at \`3b5a78a5a2d13e43e81bbe26682686f1df8c77be\`  
**Scope:** Material AIR software, prompt-governance, evaluation, and integration changes. The rigor is proportional to Q5, Q6, target AMRS, impact and risk. Do not retrofit every historical patch into a purported test-first process.

## Design intent

- **ATDD:** Define verifiable *externally observable* requirements, positive cases, negative cases, explicit failure behavior, and evidence needed for acceptance **before** implementing a change.
- **TDD:** Where a component has a deterministic executable contract, write an executable test that detects the intended defect or missing functionality, observe **RED** on the relevant preimage, implement the minimal change, observe **GREEN**, and **REFACTOR** without regressing contracts.
- **LLM behavioral evaluation:** For model-dependent behavior, predeclare acceptance criteria, fresh-host/test conditions, adversarial populations, over-refusal controls, grading and resource budgets. Report empirical pass distributions instead of treating a single model response as deterministic proof.
- **Independent evidence:** Do not allow the model that proposes the change to be the sole judge of whether it passed. The verifier must have independent source/oracle access; model-produced claims and trace objects do not by themselves attest execution, backend enforcement or private reasoning.

ATDD establishes *what acceptable behavior is*; TDD verifies the deterministic implementation; fresh-session evaluation measures remaining stochastic behavior. This method is **subordinate** to existing AIR Core, Method Layer, AMRS, Artifact, AIR_GATE, authority and approval contracts, and introduces no new cognitive module, law, or positive authority.

## Existing canonical owners

1. **MII Cognitive Architecture:** structured candidate contributions and evidence; no automatic execution authority.
2. **Method Layer:** task-local \`AIR_ARTIFACT.method\`, evidence-to-advance, state gating; \`AIR_METHOD_PACK\` creation/promotion requires separately approved reuse.
3. **AMRS Stage Completion and Step Optimality:** target-relative completion envelope, material alternatives, proportional stopping, proof of completion.
4. **Cognitive Scope Authority Isolation:** cognition never directly mutates protected state.
5. **Decision Trace and Forced Walk:** material interpretive decisions require supported justifications; neither model explanations nor trace outputs represent hidden reasoning or grant authorization.

No duplicate \`PASS\`, \`CURRENT\`, or approval state may be constructed by this method. Research branch/source-sync documentation is not a claim of identity with later nonpromoted R135 detached candidates.

## Verification sequence for a material change

| Phase | Required output | What must fail closed |
| --- | --- | --- |
| E0 — Scope | Q5 objective, target AMRS, Q6 authority/roles, exact source tuple, impact and risk | Missing material task or authorization context |
| E1 — ATDD acceptance | Independently reviewable Given/When/Then cases, evidence class, oracle, negative/legitimate cases, explicit threshold or HOLD | Untestable claims, convenient self-grading, omitted necessary safe outcome |
| E2 — Baseline | Prior behavior, known defects and valid comparator pinned with environment/version | No observed baseline but improvement claimed |
| E3 — TDD Red | Deterministic regression fails on defective preimage and detects a realistic mutation | A test passes before fix but is called defect-reproducing |
| E4 — TDD Green / Refactor | Minimal implementation, tests pass, mutation control remains meaningful | Weakened oracle/tests, hidden failures, silent unapproved rescope |
| E5 — Integration and ATDD | Final assembled artifact checks, behavioral trials and negative controls, reproducible evidence | Passing unit tests substituted for delivery acceptance |
| E6 — Independent review | Correctness, maintainability, architecture, security, performance and explicit residual risks | Model-only or unsupported validation/PASS |
| E7 — AIR decision | Existing Artifact/AMRS/approval gates evaluate the evidence; promotion separately authorized | Method PASS interpreted as release approval |

For a purely prompt-level or interpretive change, **do not manufacture a deterministic RED test**. Use source/schema checks if applicable and independent observational ATDD experiments, with sample sizes and acceptance/error criteria declared in advance.

## Predeclared acceptance record (research-only evidence)

A change-specific record references canonical source/Artifact identities, never overrides them. At minimum it identifies: change ID, exact source tuple, Q5/Q6/AMRS refs, proposed behavior, hard constraints, acceptance cases and oracles, legitimate-success and attack-negative coverage, TDD preimage/failure evidence where applicable, observed trial/tool evidence, release/no-release status (informational only), residual risks, and explicit owner decision required for integration.

The record may use \`PASS | FAIL | INCOMPLETE | NOT_RUN\` as **test result evidence** only. It must never present those values as AIR_GATE or release authority.

## First application: Public-Facing Governance (PFG)

The detached PFG-R0 set has **26 synthetic cases** balanced between legitimate actions and proper no-action outcomes, with three proposed arms: baseline model, AIR prompt-layer governance, and AIR plus a **simulated** independent authorization gate.

ATDD must predeclare:
- Legitimate customer-order read/refund-request handling *without genuine money movement*.
- No cross-account reads, unsupported writes, policy-override-by-document, forged approvals, or invented host-validation claims.
- Correct behavior when an otherwise legitimate request contains attack-looking text (overblocking control).
- Separate evidence for (a) model action proposals, (b) actual simulation gate decisions, and (c) operator-observed source/tool return.
- Results by legitimate-success, unsafe proposal, false refusal, unauthorized action, audit fidelity and observed latency/cost; missing host counters remain unavailable.

The 26 fixtures and the gate tests already exist; this methodology **does not** imply the 78 proposed fresh model sessions have been approved or run. No genuine user/customer information, real refund API, or operative action is in scope.

## Regression precedent

A historical distribution discrepancy occurred when a manifest declared a new source digest while a final candidate ZIP retained an older installed route map. A **retrospective** test can verify RED on the historical candidate and GREEN on a separate reconciled detached probe. This is not historical proof that development followed TDD. For future packaging changes, make the same test fail **before** amending the relevant source/artifact, include a mutated-content negative control, then verify the *final packaged deliverable*.

## Acceptance criteria for this research-method definition

- Existing AIR laws and Q5/Q6/AMRS retain governing authority.
- Separate deterministic tests from empirically assessed model behavior.
- Positive user outcomes and negative adversarial outcomes both represented.
- Every PASS claim tied to observable evidence and exact source/environment.
- No hidden reasoning, host enforcement, continuous training or universal-determinism claims.
- Zero changes to operative AIR runtime or frozen R135/ASG/CMSV/PFG sources.
- Any new test harness or production integration beyond detached research must receive its own scoped authorization.

**Disposition:** \`ENGINEERING_VERIFICATION_METHOD_R1_APPROVED / METHOD_DOCUMENTED / OPERATIVE_INTEGRATION_NOT_AUTHORIZED / NO_PROMOTION\`.
