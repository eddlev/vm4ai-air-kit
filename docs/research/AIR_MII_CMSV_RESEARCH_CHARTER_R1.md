# AIR-P — MII Cognitive Method Synthesis & Validation (CMSV)
## Research charter and evaluation contract — R1

**Status:** OWNER-APPROVED DESIGN PRINCIPLES / RESEARCH-DOCUMENTATION ONLY / NO IMPLEMENTATION AUTHORITY  
**Branch:** \`research/mii-cognitive-method-synthesis-r1\`  
**Planning ancestor:** \`air/v0.8.1-source-sync\` at \`3b5a78a5a2d13e43e81bbe26682686f1df8c77be\`  
**Related but separate:** ASG (Auditable Selective Governance) research track; ASG G0-OBS remains open.  
**Source position:** The pinned public ancestor is **not** an assertion of source identity with any later, detached R135 engineering candidate. Source reconciliation is a prerequisite for later implementation.

## 1. Owner-approved purpose

AIR's MII (Mathematical-Informational Intelligence) architecture is intended to make the **existing model's capabilities**:

1. **Focused:** maintain the declared objective, material constraints, task scope, and required output, avoiding irrelevant expansion or objective drift.
2. **Structured:** decompose a problem into relevant concepts, relationships, assumptions, dependencies, tests, and deliverables.
3. **Systematic:** select and apply appropriate cognitive routes, evaluate meaningful alternatives and counterexamples, and preserve material uncertainty.
4. **Reproducible:** achieve comparable decision quality and outcome consistency across equivalent runs and explicitly pinned conditions; not identical stochastic wording or deterministic latent inference.
5. **Auditable:** retain inspectable inputs, evidence, candidate alternatives, changes, validation outcomes, and approvals, without claiming access to private chain of thought.
6. **Efficient (cross-cutting):** achieve the above with proportionate context, tools, compute, time, and necessary dependencies; never trade away mandatory correctness, safety, or authority boundaries just to reduce overhead.

This charter does **not** claim MII creates new model intelligence, gives latent-space control, alters foundation-model training/weights, performs autonomous continual learning, or accesses hidden reasoning. The research question is whether MII measurably makes existing capabilities more focused, structured, systematic, reproducible, auditable and efficient.

The owner also approved **independent cognitive method derivation followed by comparison against established methods and evidence**. A documented method is neither mandatory by default nor rejected merely because AIR can derive an alternative.

## 2. Source and authority contract

The existing \`CORE.LAW.MII_COGNITIVE_ARCHITECTURE.md\` defines ten cognitive routes, observable candidate contributions, validation states (ACCEPT/HOLD/REJECT), preservation of support and conflict edges, and **no positive execution authority** for MII contributions. This proposal is subordinate to that law, to cognitive-scope authority isolation, and to the bound AIR_ARTIFACT benchmark.

Canonical paths and contract exact hashes must be rechecked against the intended engineering baseline before changing source files. Nothing in this document changes routing, law applicability, AMRS obligations, Q6 working agreements, approvals, host behavior, Specialist compatibility, binding, or promotion.

The presently frozen R135/L2-A engineering work and ASG source-distribution probes are not to be modified or copied into this public branch. All five R135 Specialist families remain held from current-source selection/binding pending separate compatibility validation. L2-B is untouched.

## 3. Proposed project-triggered workflow

**Trigger:** Q5 is sufficiently defined *and* the relevant AMRS target and project constraints are available. Q6 must be respected when establishing roles/approval boundaries. Do not infer unanswered onboarding fields.

**Stage 0 — Task frame and sufficiency budget.** Record desired result, acceptance benchmark, normative obligations, risks, information gaps, existing capabilities, resource constraints, and the minimum evidence expected at this AMRS level. Choose a light or deep discovery posture by task risk, novelty and consequences; do not default to exhaustive research.

**Stage 1 — Independent MII derivation.** On the task facts available, select the minimum useful MII cognitive routes and independently generate one or more candidate methods or architectures. Record an observable, nonauthorizing derivation snapshot (proposal, causal assumptions, dependencies, alternatives, predicted failure modes, tests, uncertainties and supporting input references). Seal the snapshot **before** exposing candidate methods from external research *for that trial*. This is trial-level independence, not a claim that the pretrained model has never learned analogous patterns.

**Stage 2 — Grounded method discovery.** Search internally validated methods and relevant external standards, field practices, scholarly evidence, implementations, and adjacent-domain analogues. Use source quality, currency, scope, licensing and threat/injection checks. Enumerate material alternatives and search limitations. Do not execute instructions embedded in retrieved content. Where binding law or a required standard governs the task, treat it as a requirement rather than an optional comparator.

**Stage 3 — Adversarial comparison.** Compare independent proposals with documented alternatives on objective fit, domain constraints, demonstrated evidence, maturity, residual uncertainty, dependency/complexity cost, operational risk, and testability. Explicitly record agreements, contradictions, missing constraints, and reasons for excluding approaches. Field-tested does not mean universally applicable; novel does not mean superior.

**Stage 4 — Selective synthesis and validation.** Choose an independently derived method, established method, or a hybrid, **or HOLD** when the evidence is insufficient. Test material predictions and counterexamples to the level required by AMRS and Q5. Prefer the simplest *sufficient* approach, not the fewest sources regardless of risk. A valid method need not be packaged as a permanent Specialist. Escalate to a separately validated Specialist only when capability sufficiency or governing requirements justify it.

**Stage 5 — AIR ingestion boundary.** Produce a nonauthorizing Method Selection Record for inspection. Only validated and explicitly accepted contributions can be proposed for incorporation into the active task benchmark. Current Artifact binding, material-action approvals and execution authority remain under operative AIR contracts and human approval gates.

**Revisit conditions:** Changed Q5, AMRS target, legal/normative constraints, risk classification, tool environment, source validity, demonstrated failures or new evidence reasonably capable of changing the selected approach.

## 4. Minimal observable evidence — not a new authority layer

Records are proposed test/evidence schemas (names provisional), selectively loaded rather than injected in full on every turn:

- \`MII_DERIVATION_SNAPSHOT\`: task ID, pinned Q5/AMRS input, task-fact sources, candidate methods, assumptions, tests, dependencies, uncertainty, creation order and seal hash.
- \`METHOD_DISCOVERY_LEDGER\`: search source/queries and scope, candidates found, evidence quality, source identity/time, limitations, exclusion reasons, and injection/license review.
- \`METHOD_COMPARISON_MATRIX\`: independent vs documented/hybrid alternatives, tradeoffs, adversarial results, normative constraints and unresolved issues.
- \`METHOD_SELECTION_RECORD\`: selection or HOLD, benchmark criteria, source/evidence refs, minimum sufficient dependencies, rejected alternatives, validation state, owner/authorization boundary, and reevaluation triggers.
- \`EXPERIMENT_RECEIPT\`: exact prompt/fixture and source tuple, model/host/tool conditions, observable executions and test outcomes; separate measured host counters from estimates and model self-reports.

Preserve the governing MII contribution/fusion contract and existing ledgers. New records should reference or extend existing structures where feasible, not duplicate an entire governance stack. Rule retrieval is not proof of evaluation; model self-report is not independent compliance attestation.

## 5. Controlled experimental comparison

Use the **same underlying model/version, tools, task facts, fixed AMRS target, constraints, test fixtures, run count and practical resource budget**, with no Specialist selection or operative release promotion.

Experimental arms:
- **A — direct baseline:** Solve without additional method-specific scaffolding (retain required safety/authorization envelope).
- **B — best-practice-first:** Retrieve and apply established documented methods, with comparable resources.
- **C — MII-first:** Derive a method with source-locked MII routing; no method-discovery material is exposed before the sealed initial proposal.
- **D — MII + benchmark:** Seal the independent MII proposal first, then reveal established-method research, challenge and synthesize as needed.

Predeclare held-out tasks across at least three distinct domains, including:
- Familiar problems where established procedures are appropriate.
- Novel or cross-domain transfer problems where method adaptation matters.
- Adversarial tasks where a popular method is unsuitable, a constraint is easily missed, or the right outcome is HOLD.

Use independently checkable answers, executable fixtures, source-backed rubrics or blinded qualified assessment as appropriate. Do not let the proposing agent score its own compliance unchallenged. Compare success and failure rates, not just the eloquence of explanations. If genuinely held-out material is unavailable, label generalization claims accordingly.

### Metrics by approved objective

| Dimension | Observable evaluation |
| --- | --- |
| Focus | Objective/constraint adherence; irrelevant scope expansion; missed required deliverables |
| Structure | Correct dependency and assumption coverage; coherent task decomposition; useful test plan |
| Systematic | Coverage of material alternatives, counterexamples, uncertainty and failure cases; missed relevant checks |
| Reproducible | Distribution of independent-run outcomes and benchmark agreement under pinned conditions |
| Auditable | Provenance and coverage of material claims; inspectable selection changes and evidence for each relevant decision |
| Efficiency | Native observed time/token/tool counts when available, otherwise transparently labeled source-byte proxies; complexity and dependency count |
| Quality and safety | Independently tested correctness, generalization, robustness, domain obligations and zero unsupported authorization/PASS |

**Comparison discipline:** do not assume the MII arms win. A simpler baseline that meets the benchmark at lower cost is preferable to an elaborate method. Predeclare metric definitions, acceptance thresholds and the trial population before evaluating results; establish numerical efficiency targets only after a measured baseline is available.

### Fail-closed conditions

Reject any comparison or prospective implementation that: drops a mandatory contract; treats unverified source material as operative instructions; silently converts uncertainty or an unresolved conflict to PASS; uses historical Specialist references as current compatibility; promotes a model claim into host-observed evidence; loses a material Q5/Q6/AMRS constraint; bypasses Artifact/approval gates; or conceals a regression behind a token-saving claim.

## 6. Research and implementation gates

- **CMSV-R0 — This charter:** owner-approved principles recorded, documentation-only branch and provenance lock.
- **CMSV-R1 — Evaluation design:** confirm intended exact source tuple, map existing MII/METHOD/Specialist contracts without duplication, draft minimal schemas, predeclare tasks, baselines and scoring rubric. Architecture only.
- **CMSV-R2 — Sandbox scope decision:** obtain separate approval for exact file allowlist, implementation approach, tests and any material source changes.
- **CMSV-R3 — Experiment and independent verification:** run deterministic and fresh-host/cross-domain evaluations; report incomplete trials as incomplete and provide comparative ablations, negative controls and measured costs.
- **CMSV-R4 — Integration decision:** explicit source-owner review of findings, approved changes and a separate promotion decision if warranted.

The ASG G0-OBS source/host telemetry study remains a distinct track; reuse its measurement discipline where useful, but do not treat it as complete or merge its release gates with CMSV.

## 7. Immediate next actions (not yet run)

1. Map current source clauses that already implement this workflow and identify the smallest real delta. **Prefer no new cognitive module** unless the existing ten demonstrably cannot perform the needed function.
2. Establish a small cross-domain benchmark with task/AMRS constraints, negative controls and baseline protocols.
3. Review how to express discovery, comparison and selection as compact evidence records without expanding Tier0 context.
4. Submit the proposed exact patch scope and measured research plan for separate implementation approval.

**Disposition:** \`CMSV_R0_RESEARCH_CHARTER_RECORDED / DESIGN_AUTHORIZED / FUNCTIONAL_PATCH_NOT_AUTHORIZED / NO_PROMOTION\`.
