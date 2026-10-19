# AIR-P — Auditable Selective Governance (ASG) Patch Plan R1

Status: RESEARCH_PLAN_ONLY / NOT_AN_IMPLEMENTATION_APPROVAL / NO_RELEASE_AUTHORITY
Track: isolated efficiency, observability and continuation-fidelity experiment
Research branch: research/auditable-selective-governance-r1
Planning base: air/v0.8.1-source-sync (not an assertion that this ref is the latest internal engineering source)
Source authority: unchanged canonical AIR contracts and applicable law bodies

## 1. Goal

Reduce model-visible runtime context while improving the ability to audit rule selection, contract evaluation, and handoff/restoration fidelity. Optimize the actual loaded token footprint, not the size of the complete release archive.

AIR's existing Tier0–Tier3 profiles, package-enabled applicability router, runtime reference index, law-source hashes, and handoff checkpoint/delta boundary are the starting architecture. This is not a replacement for the AIR governing source library.

Research hypotheses:
- An exact, compact, pinned retrieval index may reduce repeat ingestion without losing mandatory source coverage.
- A closed-world expected-rule computation combined with retrieval/evaluation receipts can detect absent required rules as well as consulted ones.
- A per-record handoff disposition walk can make generation completeness and restoration divergence testable.
- Post-compaction index reload and state reconciliation can help where the host exposes reliable boundaries or explicit checkpoints.
- Fewer prompts do not necessarily mean better control. Compare measured alternatives rather than assuming any retrieval design wins.

## 2. Authority and isolation

1. The canonical Core, Control, Governance, Starter, law bodies, predicates, and source-owner contracts remain authoritative. Derived indexes, ledgers, reports and any model-produced statements are navigation or evidence only.
2. This research branch is initially DOCUMENTATION-ONLY. It does not authorize changes to operative AIR-P sources, current release artifacts, L2-A/L2-B semantics, repository main, deployments, or candidate promotion.
3. The sealed internal nonpromoted candidate is an offline benchmark/reference and must not be copied into this public repository without distinct authorization and an exact-source synchronization gate.
4. A GitHub branch or passing engineering suite does not constitute AIR Gate approval, active Artifact binding, law resolution CURRENT, host acknowledgment, or promotion.
5. No fabricated retrieval, rule-evaluation, compaction, cross-provider or backend-enforcement evidence. Unknown states remain explicit.
6. Existing mandatory guards and negative controls must fail closed; specifically preserve mixed include/exclude law-predicate conflicts rather than hiding them by smaller context or shortcut fallbacks.
7. Do not quote private correspondence, disclose unpublished source deltas, or import third-party implementation code until provenance, licensing, security and scope review.

## 3. Required baseline lock — ASG-G0 (before implementation)

- Resolve which exact internal AIR-P authoring source tuple is the intended experiment baseline. Verify file preimage hashes, package-enabled router identity, law count, floor index, compiler/rebuild identity, and frozen candidate provenance.
- Reconcile that tuple with this branch's public source-sync ref. Public ref similarity is not proof of exact source equivalence. Do not patch against a convenient but stale branch.
- Capture the minimum model-visible payloads actually requested or provided for Tier0, Tier1, Tier2, Tier3, Q1, Q5, Q6, an ordinary task, and a continuation. Distinguish source archive bytes, transmitted text, retrieved text, and inferred token estimates.
- Pin a tokenizer/model identifier and measurement method; record when host-side token usage or compaction signals are unavailable.
- Preserve the existing frozen L2-A candidate and unresolved L2-B conflict as independent baseline negatives. Do not substitute a synthetic Q6 vector for a newly observed live runtime trace.
- Produce G0_BASELINE_LOCK.json, BASELINE_CONTEXT_CENSUS.json and a signed-off source-gap decision; none is committed to this public branch without a separate disclosure check.

Exit condition: exact source reconciliation is evidenced, and baseline measurement/negative controls are fixed before performance experimentation.

## 4. Proposed patch slices (provisional source paths, not an authorized edit list)

### ASG-01 — compact exact-source index

Design a small, schema-validated navigation index carrying canonical identity, source hash, source range/subtree locator, rule/claim identifier, typed activation trigger, dependency edges, and escalation/invalidator conditions. Define Tier0 always-on dependency closure independently of optional rule retrieval. Do not use natural-language similarity as an authorization substitute.

Potential new authoring artifact: catalog/AIR_COMPACT_GOVERNANCE_INDEX.json.
Potential derived artifact: air_p/compiled/AIR_P_ASG_NAVIGATION_INDEX.json.

A roughly 3,800-token index from external research is a comparator, NOT a hard AIR budget; optimize from measured AIR baselines.

### ASG-02 — complete applicability / missed-trigger detection

For each task vector, deterministically compute the expected applicable and potentially conflicting rule set from pinned law metadata BEFORE counting retrieved rules. Maintain explicit positive, negative, none and mixed cases. Distinguish unknown/ambiguous predicates from exclusion. Verify closure dependencies, global floors and staleness invalidators.

Output: expected_rule_set, excluded_with_proof, unresolved_conflicts and coverage_failures.
Invariant: if a mandatory rule is missing, stale, or conflicted, no successful authorization or CURRENT law-resolution claim is allowed.

### ASG-03 — Rule Application Ledger

Proposed evidence-event fields: task/Artifact identity and state, source tuple, rule ID, required status, trigger evidence, source path/hash, retrieval event/locator, deterministic evaluation evidence, outcome, observer/evidence class, and time/order reference.

Minimum distinguishable states:
- NOT_REQUIRED_WITH_PROOF
- REQUIRED_NOT_RETRIEVED
- RETRIEVED_NOT_EVALUATED
- EVALUATED_SATISFIED
- EVALUATED_BLOCKED
- UNKNOWN_OR_UNOBSERVABLE
- UNRESOLVED_CONFLICT

A retrieval receipt proves a source was fetched by the observed tool, not that the model followed it. A model's own claim of compliance is SELF_REPORT, not independent enforcement evidence. Prefer testable evaluator and host receipts where available. The ledger is NONAUTHORITATIVE and never grants approval.

Potential derived schema: air_p/compiled/AIR_P_RULE_APPLICATION_LEDGER_CONTRACT.json.

### ASG-04 — generation-time forced walk

Enumerate each material input record under an explicit completeness scope before generating a handoff. Give each a disposition: PRESERVED_EXACT, SUMMARIZED_WITH_PROVENANCE, REFERENCED_PINNED, SUPERSEDED_WITH_LINEAGE, EXCLUDED_WITH_REASON, or UNRESOLVED. Preserve decisions, approvals with their original scope/expiry, blockers, unresolved questions, source identity and task intent distinctly.

Hard fail if any material input is unaccounted for; never infer lost historical provenance or transfer past authorization into the receiving session.

Potential derived schema: air_p/compiled/AIR_P_HANDOFF_DISPOSITION_LEDGER_CONTRACT.json.

### ASG-05 — restoration and compaction checkpoint reconciliation

At explicit handoff/restoration, verify source pins, record dispositions, canonical project state, unresolved conflicts, and active task identity. Treat all restored state as nonauthorizing until current-session verification and required rebinding. For compaction, only claim automatic reinjection when a real host event/hook is observed; otherwise require an explicit checkpoint/reload action. Verify reloaded index and required source closure.

Preserve strict vs portable provenance and the original handoff schema's authority boundaries.

### ASG-06 — measured comparison and ablation harness

Compare the same pinned task fixtures under:
A. existing source-locked Tier0–Tier3 runtime;
B. compact always-on kernel and source-locked index;
C. the same kernel with event-ledger and selective retrieval.

For each arm record: input/retrieved token estimate or observed count, boot/Q1 completion, required-rule recall and precision, missed-trigger rate, conflict correctness, unsupported PASS rate, handoff generation coverage, restored material-state parity, time/cost where observed, and divergence across independent repeats/models.

A simpler compact direct-spec baseline must be included: conditional retrieval may not outperform it. Benchmark every schema, tool boundary, and model/provider under the same frozen source/evaluation fixtures.

## 5. Regression matrix / acceptance invariants

Required minimum test families:
1. Normal Tier0 boot, Tier1 navigation, exact-target Tier2, explicit Tier3 deep audit and silent expansion rejection.
2. Q1/entry-path separation and Q5-S/Q6 source-backed selection, including an independently observed live vector only when actually supplied.
3. All 83 package-router rows and 28 floor entries (or the exact frozen counts verified by ASG-G0), with dependency closure and unknown metadata.
4. Historical mixed positive/negative floor-invariant Q6 case must remain UNRESOLVED_CONFLICT, never silent EXCLUDE or CURRENT.
5. Missing, stale, wrong-hash, wrong-namespace, duplicate or ambiguous source/index/rule IDs fail closed.
6. Retrieved-only entries cannot become EVALUATED_SATISFIED without eligible evaluator evidence.
7. Forced walk rejects one omitted, contradicted, superseded-without-lineage or unauthorized approval-state record.
8. Restoration across handoff/compaction does not reactivate a previously granted authorization, license an unbound Artifact, or invent host events.
9. Controlled ablations and repeated GPT-6/cross-provider tests separate deterministic static checks from actual host behavioral evidence.

Predeclared correctness gates:
- Zero unsafe PASS outcomes in the fixed negative-control set.
- All required rules in each deterministic fixture either have verified applicability/evaluation closure or force an explicit fail-closed state.
- Every material handoff record has a disposition with source provenance, or generation is blocked.
- No rule-evaluation or compaction signal is presented as observed without actual evidence.
- Generated artifacts must be deterministic from pinned inputs and preserve unchanged canonical law bodies unless separately authorized.

Efficiency threshold: fix a measurable improvement target AFTER G0's context census but BEFORE comparing variant results. Never sacrifice the correctness gates to hit a token budget.

## 6. Gate sequence and intended commits

ASG-G0: source identity and context footprint baseline (research; no source edits).
ASG-G1: schemas and test fixtures reviewed; exact edit-scope and approvals defined.
ASG-G2: separately approved, isolated sandbox implementation only, feature-off by default, reversible diffs.
ASG-G3: deterministic rebuild, independent negative controls, reproducible differential benchmark and fresh-session tests.
ASG-G4: separate source-owner approval for any source integration, public disclosure, release or promotion.

Suggested implementation commits AFTER G2 authorization, individually auditable:
1. schemas and fixture contracts;
2. compact-index compiler output and validation;
3. applicability coverage and Rule Application Ledger;
4. forced-walk disposition/restore reconciliation;
5. benchmark harness and reports.

Stop conditions: any source drift, lost mandatory guard, unsafe PASS, fabricated observation, unaccounted handoff material, unauthorized source update, or regression in existing binding/approval boundaries.

## 7. Open decisions (owner approval required)

- Exact experimental baseline and which unpublished source files may be staged privately.
- Whether the first patch is primarily a compiler/navigation enhancement or a runtime response-surface change.
- Which retrieval and evaluation events are independently observable on target hosts.
- Fixed benchmark population and token-efficiency threshold after baseline measurement.
- Whether any future law-predicate or authority-contract amendment is necessary; those changes are NOT in this research authorization.

## 8. Workstream status

Branch creation and this document are planning artifacts only. No functional patch, live model validation, promotion, release, or operative AIR-P source change is represented by this plan.

Research references (public):
- https://arxiv.org/abs/2605.28969
- https://www.base-layer.ai/research
- https://github.com/agulaya24/BaseLayer
