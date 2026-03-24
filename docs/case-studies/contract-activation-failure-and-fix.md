# Case Study — Contract Activation Failure and Fix

## Subtitle
Why identifying the right AIR contract is not enough, and how explicit activation rules improved live-session behavior.

---

## 1. Purpose

This case study documents one of the most important AIR failure modes:

> the model recognizes the correct governing contract, but does not actually activate it.

This is a critical distinction.

AIR depends not only on:
- correct interpretation,
but also on:
- correct runtime state transition.

This case shows:
- how that failure appeared,
- why it mattered,
- what changes were introduced,
- and how the resulting behavior improved.

---

## 2. Problem

In a live project session, the active topic narrowed from a broader project frame into a more specific contract layer.

The session already contained:
- prior project context,
- prior AIR reasoning,
- and earlier applied contract logic.

A new AIR contract was then attached and explicitly folded into the session.

The expectation under AIR was clear:
- if the attached contract governed the active topic,
- it should be promoted to Orbit 0,
- and the session should materialize that state explicitly.

Instead, the model often did something weaker:
- it described the contract as the best candidate,
- said it was ready for promotion,
- or said it would govern “if we continue from here.”

That meant the model had identified the right contract semantically, but had not actually switched runtime state.

---

## 3. Why this matters

This is not a cosmetic issue.

If AIR allows a contract to remain in a “candidate” or “ready” state when it should already govern, then the session remains vulnerable to:

- blended scope
- wrong precedence
- stale parent context overriding the specialized task
- ambiguity about what belongs in Orbit 0
- weaker handoff continuity
- prose that sounds aligned without being statefully correct

This is one of the clearest examples of why AIR needs:
- explicit activation law
- explicit session state
- explicit contract precedence

rather than informal agreement.

---

## 4. Initial setup

The live session already had:
- active project context
- prior transcript-derived AIR policy
- one or more earlier contracts in supporting orbit

A new contract was then attached and folded into the same session.

The model did several things correctly:
- it recognized the correct domain layer
- it named the right task surface
- it preserved the intended fail-closed rules
- it correctly identified the contract as the right next governing layer

But it still did not actually promote the contract to Orbit 0.

Instead, it described the contract as:
- a candidate
- ready for promotion
- or governing only if the next step continued in that direction

This was the central failure.

---

## 5. Expected AIR behavior

Under correct AIR execution, the following should have happened immediately after the new contract was attached and folded:

1. emit `AIR_SESSION`
2. explicitly set `active_orbit_0_contract`
3. bind the active topic and task key
4. list supporting outer-orbit contracts
5. declare conflict policy
6. stop describing readiness and instead materialize state

In other words:

- no “candidate”
- no “ready for promotion”
- no prose-first discussion of what would happen

The contract should have been activated, not merely interpreted.

---

## 6. Observed failure mode

The observed behavior followed a pattern:

### 6.1 Correct identification
The model correctly identified:
- which contract matched the narrowed topic
- what concrete task layer it governed
- what constraints it added

### 6.2 Incomplete activation
Instead of activating the contract, the model responded in prose and framed the contract as:
- the best candidate for Orbit 0
- ready for promotion
- governing if continued

### 6.3 Orbit ambiguity
In some cases, the contract was simultaneously treated as:
- highly relevant,
- likely governing,
- but still part of supporting orbit context

This weakened the difference between:
- **supporting context**
and
- **active governing state**

### 6.4 Consequence
The session remained semantically aligned but statefully unstable.

That made it possible for:
- broader earlier context
- adjacent project concerns
- or prior contract frames

to remain too active.

---

## 7. Root cause analysis

The core cause was that the runtime instructions were still too permissive in one crucial area:

they allowed the model to **describe** the correct contract without forcing it to **activate** the correct contract.

In other words, the model could satisfy the spirit of the instruction through explanation rather than state transition.

This exposed a general lesson:

> AIR needs explicit activation precedence rules, not just conceptual orbit language.

The model required a direct rule stating:
- when one contract is attached and clearly governs the active topic,
- that contract must become Orbit 0 immediately

Without that, the model could linger in a halfway state.

---

## 8. Fix introduced

The main fix was to tighten the activation prompt with explicit contract precedence.

A rule was added in substance:

- if exactly one AIR profile JSON is attached,
- its `SYSTEM_DESIGNATION` must become `active_orbit_0_contract`
- unless the user explicitly instructs otherwise

Additional clarifications were also introduced:

- do not describe candidate or readiness state when the governing contract is clear
- promote the governing contract to Orbit 0 immediately
- do not leave the governing contract in Orbit 1
- the runtime activation prompt is session law, not the parent contract
- emit `AIR_SESSION` before analysis or artifact

This changed the control model from:
- interpretive
to
- state-binding

---

## 9. Supporting fixes

The activation-precedence fix worked best together with several supporting changes.

### 9.1 In-session update prompt
A dedicated update prompt was added to:
- fold a new contract into the current AIR runtime session
- promote it if it governs the active topic
- attach it as a sub-contract if it is narrower
- emit `AIR_SESSION` only

This reduced ambiguity during mid-session contract changes.

### 9.2 In-session patch prompt
A patch prompt was added to restore AIR state when the model drifted.

It tells the model to:
- restate the active Orbit 0 contract
- restate supporting outer-orbit contracts
- restate task binding
- restore `AIR_ARTIFACT_FIRST`
- avoid commentary

This gave the workflow a realignment mechanism instead of requiring a full restart.

### 9.3 Handoff-card generation
A generic handoff-card flow was introduced so that active state could be moved forward without replaying large transcripts.

This reduced the chance that the next session would have to infer its own active contract from too much prose.

---

## 10. Result after the fix

After tightening contract precedence and adding explicit update/patch flows, the model’s behavior improved significantly.

The main improvements were:

- better immediate Orbit 0 activation
- less candidate/readiness limbo
- clearer separation between active and supporting contracts
- more reliable handling of narrower sub-contracts
- stronger AIR session-state materialization
- cleaner continuity between sessions

This did not make AIR perfect.
But it removed one of the most damaging failure modes in live use.

---

## 11. Lessons learned

### 11.1 Recognition is not activation
A model can identify the correct contract and still fail AIR execution if it does not switch into that contract explicitly.

### 11.2 Orbit language is not enough by itself
Without explicit activation law, orbit concepts can remain metaphorical instead of operational.

### 11.3 State must be emitted, not implied
If state is only described in prose, it remains too easy for the model to blend or drift.

### 11.4 Contract precedence must be explicit
The runtime must say exactly what happens when:
- a new contract is attached
- one contract clearly governs the active topic
- a contract is narrower than the parent task
- a replacement contract supersedes an earlier one

### 11.5 Patchability matters
Even with a good activation prompt, live sessions can drift.
A dedicated patch prompt is therefore part of AIR’s practical operating kit, not a convenience extra.

---

## 12. Comparative takeaway

This case highlights one of the clearest differences between AIR and normal prompting.

In normal prompting, the model can often get away with:
- sounding aligned
- paraphrasing the right interpretation
- and continuing in a roughly plausible direction

In AIR, that is not enough.

AIR requires:
- explicit activation
- explicit orbit placement
- explicit task binding
- and explicit conflict law

That makes AIR more demanding.
It also makes it more usable for persistent structured work.

---

## 13. Conclusion

This case demonstrates that one of AIR’s most important design requirements is:

> the governing contract must be activated explicitly, not merely understood.

That requirement emerged directly from live-session failure.

The contract activation fix was therefore not a cosmetic prompt adjustment.
It was a structural correction that made AIR more faithful to its own intended operating law.

This case is a good example of why AIR treats:
- session state,
- contract activation,
- and orbit handling

as runtime concerns rather than conversational niceties.

---

## 14. Follow-up

Suggested next related case studies:

- handoff continuity across sessions
- AIR vs normal prompting in trust/protocol design
- starter profile vs specialized profile
- cross-model comparison of contract activation correctness