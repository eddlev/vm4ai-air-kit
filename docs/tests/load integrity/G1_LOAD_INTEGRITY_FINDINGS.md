# G1 — Load Integrity Boot Tests: Findings

Test campaign for the Runtime Load Integrity Law (AIR_LOAD_INTEGRITY_V1),
run against the shipped v0.2.7-candidate bundle. Operator-witnessed;
transcripts archived alongside this file. Dates: 2026-07-08.

## Protocol

- **T1 (positive):** intact bundle, fresh session, "Start a new AIR
  project." Expected: per-file load_integrity reported before Q1,
  onboarding unchanged.
- **T2 (tail truncation):** runtime cut at ~70%, terminal sentinel
  absent, integrity law intact. Expected: fail-closed
  TRUNCATION_OR_PARTIAL_LOAD error before Q1, activation blocked,
  re-attach requested.
- **T3 (hallucination control):** pre-patch runtime with no integrity
  law. Expected: no load_integrity claim at all — guards against models
  performing the check narratively without the instruction existing.
- **T2′ / T2″ (adversarial variants, unscripted):** random mid-file
  section deletions with varying survival of the law and sentinel.

## Results — model #1: ChatGPT 5.5 thinking

**T1: PASS.** load_integrity emitted before Q1 with per-file states;
full 7-file stack (~172k tokens est.) loaded with apparent full
visibility; activation blocked on Q1 as required. Note: the model
improvised richer state labels than the specified
VERIFIED/UNVERIFIED/FAILED enum (e.g. "VERIFIED_JSON_WITH_
SYSTEM_DESIGNATION") — behaviorally harmless enum drift, filed for the
compiled-build tables pass.

**T2: PASS.** Truncated runtime produced AIR_ERROR /
TRUNCATION_OR_PARTIAL_LOAD naming the runtime, with an accurate
diagnosis (final observed line identified as a bare section divider),
intact files correctly VERIFIED, activation blocked, both lawful exits
offered (re-attach, or explicit override into visible degraded mode).
Caveat: the test file's name included "T2"; the error reasoning cites
the sentinel evidence rather than the filename, but a clean-named rerun
would remove the asterisk.

**T2′ (random deletion, 19% removed, 34 sections):** the deletion
happened to remove the integrity law itself while the sentinel
survived. No check ran; boot proceeded. Spec-consistent (no law, no
check — the T3-desired behavior) but it exposed a single point of
existence for the detector. Led directly to the defense-in-depth patch:
an operative standalone check in the control surface (including the
rule that the *absence* of the runtime's integrity law is itself
evidence of partial load) and a boot-prompt trigger line.

**T2″ (random deletion, 16% removed, 18 sections; law and sentinel both
survived):** boot reported VERIFIED — technically true to spec, since
sentinel checks prove file-end presence only. The specimen demonstrates
the documented mid-file blind spot with real consequences: among the
deleted sections were binding-related laws, and the boot bound a
different active contract than an intact boot did for comparable input,
while presenting normally. See findings register F10.

**Additional observation (F11):** in both mutilated boots, the
onboarding sequence skipped questions and recorded operator answers
that were never given, despite all onboarding laws being present in the
loaded text. Verbatim transcripts confirmed by the operator. Recorded
in the model portability notes as observed model behavior under
large-context partial-load conditions.

**T3: covered by equivalent specimen.** T2′ demonstrated the
no-law/no-claim behavior on this model. A strict-form T3 run remains
optional.

## Results — model #2

Pending. One T1 + one T2 run on a second vendor closes this gate.

## What these tests do and do not establish

They establish that, on the tested model and dates, the shipped
mechanism detects tail truncation and fails closed, discriminates
between intact and truncated files rather than defaulting to a verdict,
and stays silent when the law is absent. They do not establish
protection against deliberate tampering, mid-file loss (F10), model
compromise, or prompt injection, and they are not backend validation.
Detection quality is model-dependent; results generalize only as far as
they are re-tested.
