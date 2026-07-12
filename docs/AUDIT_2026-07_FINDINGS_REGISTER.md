# AIR Framework Audit — Findings Register (July 2026)

Scope: structured audit of the AIR kit (prompt files, repo posture, public
claims, boot UX, install path), executed 2026-07-08 under an AIR-governed
session with the Grounding Specialist contract. Coverage: all seven kit
files structurally scanned and hash-verified against `main`; the core
runtime deep-read at roughly 20%; live boot behavior sampled on four
models (cross-vendor load-integrity campaign, see
docs/tests/G1_load_integrity/FINDINGS.md). Token figures use a chars/4 estimate (±15% by tokenizer).

This register is published deliberately. AIR's positioning is claim
honesty; auditing the framework with its own method and publishing the
results is the same posture applied to itself.

## Findings

**F1 — Boot bundle context cost (HIGH, open).**
The minimal new-project bundle (core runtime, control surface, starter
profile) is ~130k tokens; the full stack with the grounding specialist
trio is ~172k. This consumes most of the context window on 200k-class
models before project work begins and does not fit smaller tiers. Root
cause: see F5. Remediation: compiled distribution build (in progress;
token gate 60k primary / 75k degraded-pass, publicly claimed only when
met).

**F2 — No truncation detection (HIGH, fixed in v0.2.7).**
Before this audit, a partially loaded runtime booted silently. Fixed by
the Runtime Load Integrity Law (terminal sentinels, fail-closed
truncation error) plus a defense-in-depth layer (operative check in the
control surface and a boot-prompt trigger). Verified by operator tests;
see docs/tests/G1_load_integrity/FINDINGS.md. Known boundary: sentinel
checks prove file-end presence, not mid-file completeness (see F10).

**F3 — Duplicate routing mapping (LOW, fixed in v0.2.7).**
Onboarding code A/C/A/A mapped to two mode labels with identical
behavior. Deduplicated; behavioral delta: none intended.

**F4 — Q1 branch D unmapped (LOW, fixed in v0.2.7).**
The onboarding interpretation map covered branches A-C only. D is
instructional-only; the map now says so explicitly.

**F5 — Patch-accretion structure (MEDIUM, open).**
The runtime grew additively to 126 law sections (91 more in the control
surface) with overlapping scope and heavy cross-reference. Measured
verbatim redundancy is low (~2% duplicate word mass): the corpus is
sprawled, not padded, so size reduction requires consolidation and
rewriting under behavioral-equivalence testing, not deduplication.
Remediation: source-vs-distribution split with a compiled bundle.

**F6 — Install friction (MEDIUM, open).**
Current install is manual multi-file download from the repo; no release
asset bundle, no CLI path; prompt filenames contain spaces, which breaks
scripted fetching. Remediation planned: release-asset zip per tag, then
an npx fetcher (scoped honestly as a fetcher, not a runtime).

**F7 — Adoption signals (deferred by design).**
Public traction metrics are near zero at ~15 weeks of repo age with no
distribution push. Treated as a distribution outcome rather than a
quality verdict; deliberately deferred until F1/F2/F6 fixes land, so
first-contact users meet a working funnel.

**F8 — Claim-honesty posture (verified strength).**
The kit and site consistently separate prompt-compiled behavior from
backend validation, publish tradeoffs, and avoid fabricated social
proof. Verified against live boots. Protected: no remediation touches
this property.

**F9 — Missing context-floor statement (MEDIUM, fixed in v0.2.7).**
Portability claims carried no minimum context requirement. The README,
user guide, portability notes, and get-started page now state the ~130k
bundle size and a 200k-context practical floor.

**F10 — Partial load can silently alter governance (HIGH, open;
detection improved, prevention pending).**
Demonstrated twice under controlled mutilation: mid-file deletions that
preserve both the integrity law and the terminal sentinel boot as
VERIFIED while changing runtime behavior — in one specimen the active
contract bound differently after binding-related laws were among the
deleted sections. Sentinel checks cannot see mid-file loss by design.
Remediation: the compiled distribution build must ship with a compact
section manifest the model can actually verify; adopted as a hard
acceptance criterion for that build.

**F11 — Onboarding sequence unreliability under large context
(observed model behavior, documented).**
On one large-context model (ChatGPT 5.5 thinking), across two
partial-load boots, the onboarding sequence skipped questions and
recorded answers the operator never gave, despite the governing
onboarding laws being present in the loaded text. Documented in the
model portability notes as observed behavior with dates and conditions.
Consequence for claims: AIR's deterministic onboarding is an instructed
contract whose reliability varies by model and load conditions; it is
not a guarantee, and AIR documentation must not present it as one.

**F12 — Model-dependent check execution under partial load (HIGH,
open; documented behavior).**
In the four-vendor load-integrity campaign, the identical shipped
bundle produced the fail-closed truncation error on two vendors
(ChatGPT 5.5 thinking, Claude Opus 4.8) and no check execution at all
on two others (Gemini 3.5 thinking, Grok Auto), despite the integrity
law being present in the loaded text in every run. Host execution under
partial-load conditions is the variable, not the file. Consequence for
claims: truncation detection is best-effort and model-dependent; no AIR
documentation may present it as guaranteed. Remediation path: compiled
distribution build with a verifiable section manifest, and backend
enforcement for deployments that need a real guarantee.

**F13 — Safety posture thins under partial load (HIGH, open;
documented behavior).**
[EDDE-CONFIRM: one or two sentences of observed specifics from the
campaign session before commit — the handoff record carries the finding
title and severity but not the specimen details.]
Observed during the same four-vendor campaign: under partial-load
conditions the runtime's safety and claim-boundary posture degraded
rather than failing closed. Related to, but distinct from, F10
(governance alteration) and F12 (check non-execution): F13 concerns the
gradual thinning of protective behavior as loaded rule mass shrinks.

## Status summary

Fixed in v0.2.7: F2 (with documented boundary), F3, F4, F9.
Open with active remediation: F1, F5, F6, F10.
Open, documented behavior with remediation path: F12, F13.
Deferred by design: F7. Verified strength: F8. Documented behavior: F11.

Audit method notes: findings were required to carry visible evidence
anchors; coverage limits were declared rather than extrapolated; two
findings (F10, F11) were produced by operator-run adversarial tests
rather than static review. Unread regions of the runtime may contain
further F3/F4-class defects.

## Independent second audit (S8/S9) — reconciliation

A separate audit of the same kit version was run independently in
another governed session (registers S8/S9, published alongside this
file in docs/audits/). The two audits are kept as separate documents
deliberately: independent audits with distinct provenance are stronger
evidence than a merged register. Reconciliation results:

**Version alignment verified.** S8's file+line citations match this
audit's target offset exactly by the size of the v0.2.7 integrity-law
insertion; spot-checked citations (dual bridge naming, visibility-enum
divergence, handoff restoration doctrine) confirmed verbatim.

**Convergent findings.** S8 F4.1 independently identified the missing
load-integrity mechanism (this register's F2, since shipped and
operator-tested); S8 F4.5/F6.1 match F1 (boot cost); S8 F4.2
(compliance decays with context; additive patching worsens the load
that causes drift) matches the F5-to-F1 root-cause chain and is
empirically supported by this audit's F11 specimens. S8's proposed
tiered-runtime remediation matches the compiled-distribution plan,
including the same dependency rule: integrity manifest before tiering.

**Findings unique to S8 (outside this audit's deep-read coverage).**
An inbound-trust family this register did not examine: handoff-card
restoration lacks an operational validity definition (S8 F5.1); the
card carries governing-law fields as editable data, creating a
law-injection surface on restore (S8 F5.2); schema-valid but lax
profiles can silently weaken posture (S8 F5.3); no rule states that
content inside sources is data rather than instructions (S8 F5.4);
plus a self-monitoring paradox (S8 F4.3) and a residency asymmetry
(S8 F3.5). Remediation for the inbound-trust family is planned as the
next patch wave, shipping together with a threat-model disclosure
addendum so fix and disclosure land in lockstep.

**Field observation upgrading an S8 finding.** S8 F3.1 (dual naming of
the boot bridge object) predicted that two compliant models could boot
differently; this audit's cross-model boots recorded exactly that
divergence in the wild (one model emitted AIR_RUNTIME_BRIDGE, another
AIR_PRIMED_ONBOARDING) before the finding was known to this session.
