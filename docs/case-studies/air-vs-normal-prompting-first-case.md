# Case Study — AIR vs Normal Prompting (First Public Example)

## Subtitle
A practical comparison of baseline prompting and AIR-guided live-session compilation in a continuity-sensitive project workflow.

---

## 1. Problem

This case study examines the difference between:

- **normal prompting**
- and **AIR-guided live-session work**

in the context of a persistent, structured project workflow.

The core question is:

> What changes when the model is asked to operate under an explicit AIR runtime contract instead of a normal conversational prompt?

This case does not attempt formal benchmarking.
Its purpose is to show observable operational differences in:
- contract handling
- continuity
- artifact structure
- gap surfacing
- and handoff readiness

---

## 2. Initial setup

The project context involved long-running structured work where:
- multiple contracts emerged over time,
- task scope narrowed into sub-problems,
- continuity across sessions mattered,
- and incorrect contract activation created real confusion.

The live AIR setup included:
- an activation prompt
- an in-session update prompt
- an in-session patch prompt
- a generic handoff-card flow
- a default starter profile
- and later, project-specific AIR contracts

The baseline comparison condition was ordinary prompting without explicit:
- AIR session activation
- orbit state
- contract activation artifact
- handoff structure
- artifact-first output law

---

## 3. Baseline (normal prompting) behavior

Under normal prompting, several recurring behaviors appeared.

### 3.1 Prose-first response
The model often answered in readable narrative form before the operative state of the task had been stabilized.

### 3.2 Policy acknowledgment without runtime switch
The model could often understand the intended policy or contract, but would fail to materialize it as active governing state.

This showed up as:
- describing the right contract,
- but not actually activating it,
- or referring to the correct contract as a “candidate” rather than the governing one.

### 3.3 Silent blending of adjacent context
When several related task layers were nearby, the model often mixed:
- old task framing,
- supporting context,
- and newly attached contracts

without clearly declaring which one governed.

### 3.4 High continuity cost
To continue work, large amounts of transcript often had to be replayed, because the active task state was not compactly encoded.

### 3.5 Smoother-than-warranted completion
The baseline model often favored readable completion over explicit surfacing of:
- missing vectors
- blockers
- degraded modes
- unsupported assumptions

---

## 4. Expected AIR behavior

Under correct AIR execution, the session should instead do the following:

### 4.1 Activate a governing contract explicitly
The active contract should be made visible through runtime state rather than inferred from prose.

### 4.2 Place the contract into the orbit model
The session should distinguish between:
- Orbit 0 governing contract
- supporting outer-orbit contracts
- prior context that remains relevant but non-governing

### 4.3 Emit state before analysis
The model should emit:
- `AIR_SESSION`
before
- `AIR_ARTIFACT`

### 4.4 Surface incompleteness explicitly
Missing or unsupported parts should appear as:
- `missing_vectors`
- `obligations`
- `blockers`
- `degraded_execution_mode`
- `dependency_edges`

### 4.5 Support handoff continuity
The resulting state should be compact enough to move into another session through a handoff card rather than a full transcript replay.

---

## 5. AIR-guided behavior

After introducing AIR prompts and contracts, the session behavior improved in several specific ways.

### 5.1 Contract interpretation improved
The model became much better at identifying:
- which contract matched the current active topic
- which contract belonged in supporting orbit
- when a narrower trust/task layer should govern instead of a broader project contract

### 5.2 Artifact quality improved
The model began to produce more useful structured outputs, including:
- selected vectors
- missing vectors
- blockers
- dependency edges
- degraded modes
- referential trace
- implementation notes

This made the work more:
- inspectable
- continuable
- and implementation-oriented

### 5.3 Fail-closed behavior improved
Compared with ordinary prompting, the AIR-guided runs were more likely to:
- refuse unsupported claims
- distinguish what was present from what was merely implied
- surface missing backend/session/trust layers instead of assuming them

### 5.4 Handoff quality improved
The handoff-card concept significantly reduced the need to replay full transcripts.

The work became easier to continue through:
- active contract ID
- task key
- topic
- selected/missing vectors
- blockers
- next recommended step

rather than conversational replay.

---

## 6. AIR failure modes that still appeared

AIR did not immediately eliminate all session problems.

Several important failure modes still occurred.

### 6.1 Correct contract, incorrect activation
The model could identify the right contract but still fail to activate it.

This often appeared as:
- “best candidate for Orbit 0”
- “ready for promotion”
- “if we continue from here, I’ll treat this as governing”

This was a major lesson:
**agreement with the contract is not the same as runtime activation.**

### 6.2 Wrong contract precedence
In some runs, the model activated a broader earlier contract instead of the newly attached specialized contract.

This showed that:
- the runtime law was partly understood
- but contract precedence still needed tighter prompt enforcement

### 6.3 Prose-first fallback
Even under AIR prompting, the model sometimes answered in explanatory prose instead of emitting explicit runtime/session state.

### 6.4 Token waste through prompt echoing
Long activation prompts and attached files sometimes caused the model to respond with verbose restatement, increasing token costs unnecessarily.

---

## 7. Fixes introduced during the experiment

Several improvements were made to correct the above problems.

### 7.1 Explicit Orbit 0 promotion rule
A new rule was added:

- if exactly one AIR profile JSON is attached, its `SYSTEM_DESIGNATION` must become `active_orbit_0_contract` unless explicitly overridden

This fixed a major source of contract ambiguity.

### 7.2 AIR_SESSION-before-artifact rule
The session was required to emit explicit session state before any artifact or narrative explanation.

### 7.3 Update prompt for new contracts
A dedicated in-session update prompt was introduced to:
- fold a new contract into runtime state
- promote it if governing
- attach it as a sub-contract if narrower

### 7.4 Patch prompt for drift
A dedicated in-session patch prompt was introduced to:
- restate active AIR state
- reassert Orbit 0
- restore `AIR_ARTIFACT_FIRST`
- avoid narrative drift

### 7.5 Handoff-card generation
A generic AIR handoff-card instruction/template was added so that session continuity could move through structured state rather than transcript replay.

### 7.6 Minimal execution mode
A minimal-output rule was introduced to reduce:
- prompt echoing
- long audits
- unnecessary narrative

---

## 8. Result after adjustment

After these adjustments, AIR-guided runs became significantly more reliable than baseline prompting for persistent project work.

The clearest improvements were:

- better explicit contract handling
- better separation of active vs supporting context
- stronger blocker/missing-vector surfacing
- more implementation-ready artifact structure
- cleaner continuation between sessions
- reduced confusion when task scope narrowed into specialized contracts

AIR still required discipline and careful prompting, but it produced a better operational workflow than ordinary prompting for this class of work.

---

## 9. Comparative summary

## Normal prompting
Strong at:
- speed
- ease
- low-friction interaction
- casual exploration

Weak at:
- explicit contract activation
- state continuity
- scope governance
- handoff
- fail-closed behavior
- structured incompleteness

## AIR-guided prompting
Strong at:
- explicit runtime framing
- contract activation
- orbit-aware context handling
- blocker surfacing
- artifact-first outputs
- handoff continuity

Weak at:
- setup overhead
- prompt discipline requirements
- susceptibility to verbosity if output minimization is not enforced
- remaining model-dependent variation in activation correctness

---

## 10. Main takeaway

The most important lesson from this case study is:

> AIR’s value is not that it makes the model “sound smarter.”
> Its value is that it makes live session state more explicit, governable, and continuable.

In baseline prompting, the model often produced readable outputs.
Under AIR, the session became more like a controlled compile context.

That difference mattered whenever:
- the work persisted,
- the task narrowed,
- the contract mattered,
- or continuity had to survive beyond one conversation.

---

## 11. Practical conclusion

For short-lived or casual tasks, normal prompting is often enough.

For persistent structured work, AIR provides a more stable operating model because it makes explicit:
- what is active
- what governs
- what is missing
- what is blocked
- and what should carry forward into the next session

This is the practical reason to use AIR.

---

## 12. Suggested follow-up case studies

- contract activation failure and repair
- handoff continuity across sessions
- AIR vs normal prompting in technical trust/protocol work
- AIR vs normal prompting in high-dimensional creative work
- cross-model AIR comparison