# Explicit Contract Activation and Orbit Law

## Subtitle
Why AIR treats active contract selection, orbit placement, and session-state materialization as runtime law rather than conversational implication.

---

## Abstract

AIR is built on a simple observation:

> in persistent AI work, understanding the right contract is not the same as operating under the right contract.

This distinction matters because many live-session failures are not failures of reasoning in the narrow sense.
They are failures of **activation**, **precedence**, and **state handling**.

A model may:
- identify the correct narrowed task,
- describe the correct governing contract,
- and preserve the right constraints semantically,

while still failing to:
- activate that contract,
- place prior contracts correctly,
- and govern the session under the right active frame.

AIR addresses this problem by making two things explicit:

1. **contract activation**
2. **orbit law**

This paper explains why AIR treats both as runtime concerns, not conversational conveniences.

---

## 1. Problem statement

In ordinary prompt-based interaction, active control is often inferred rather than declared.

The user says something.
The model responds.
The session continues.
Instructions accumulate.

This usually works well enough in short, low-friction interactions.

It becomes unreliable when:
- the work persists over time,
- multiple contracts or task layers emerge,
- the active topic narrows,
- continuity must survive session boundaries,
- or prior context remains relevant but should no longer govern.

In those conditions, the model often shows a familiar pattern:

- it recognizes the correct contract,
- but treats it as descriptive rather than binding,
- or preserves too much prior context as equally active,
- or fails to distinguish the current governing layer from outer supporting layers.

The result is not always obvious failure.
More often, it is soft failure:
- blended scope,
- ambiguous precedence,
- incorrect active frame,
- or prose that sounds aligned while the underlying state remains wrong.

AIR treats this as a structural problem.

---

## 2. Why contract activation must be explicit

### 2.1 Understanding is not activation

A model can understand a contract in several incomplete ways:

- as a suggestion,
- as a summary,
- as a candidate active frame,
- as a likely next direction,
- or as one relevant layer among others

None of those are sufficient for AIR.

AIR requires the model to move from:
- “this seems like the right contract”
to
- “this contract is now governing the session”

That transition must be explicit.

### 2.2 The failure mode AIR is trying to avoid

Without explicit activation, the model often responds with phrases like:
- this is the best candidate for Orbit 0
- this should govern if we continue in this direction
- this sits immediately around the current task
- this is ready for promotion

These phrases indicate recognition without state transition.

That is not enough for persistent work.

A session cannot safely continue under “ready for promotion” if the contract already governs the active topic.
At that point, AIR requires activation, not interpretation.

### 2.3 Why this matters operationally

When activation remains implicit:
- broader earlier context can continue to dominate,
- specialized subcontracts can remain semi-backgrounded,
- handoff quality degrades,
- and session continuation depends on the user repeatedly correcting scope.

This increases both:
- token cost,
- and cognitive overhead.

Explicit activation reduces that cost by making the active governing state visible and checkable.

---

## 3. AIR’s answer: session-state materialization

AIR does not leave active governance inside conversational implication.

It requires session-state materialization.

That means the session should emit:
- `AIR_SESSION`
before
- `AIR_ARTIFACT`

This turns runtime control into a structured visible object.

### 3.1 What AIR_SESSION is for

`AIR_SESSION` exists to answer, explicitly:

- what contract is active?
- what topic does it govern?
- what task is bound to it?
- what supporting contracts remain in outer orbit?
- what governs on conflict?
- what runtime law is active?

Without these answers, the artifact may still be useful, but the session remains under-governed.

### 3.2 Why prose is not enough

A prose statement like:
- “I’ll treat this as the governing contract”
is weaker than a structured activation object.

Prose is easy to blur, reinterpret, or partially ignore.

A structured activation object is:
- easier to inspect,
- easier to hand off,
- easier to compare,
- and easier to patch if drift occurs.

That is why AIR prefers state emission over state narration.

---

## 4. Orbit law: why current context needs structure

Activation alone is not enough.

Persistent work also needs a way to distinguish:
- what is currently governing,
- what is recent and strongly relevant,
- what is supporting but not governing,
- and what is historical but potentially retrievable.

Normal prompting often collapses all of these into one soft memory field.

That is convenient in the short term and unstable over time.

AIR’s answer is orbit law.

---

## 5. The AIR orbit model

AIR uses four orbits:

- **Orbit 0** = active contract / active task kernel
- **Orbit 1** = hot recent verified context
- **Orbit 2** = warm prior relevant design decisions
- **Orbit 3** = cold archive / deferred alternatives

This model allows the session to preserve continuity without flattening all prior context into one undifferentiated working set.

### 5.1 Orbit 0
Orbit 0 is the current governing layer.

This is the answer to:
- what is active right now?
- what should control interpretation?
- what governs if something conflicts?

### 5.2 Orbit 1
Orbit 1 contains context that is still highly relevant but is no longer necessarily governing.

This might include:
- recently active contracts,
- recently verified task constraints,
- or the immediate parent layer of a now-active sub-contract.

### 5.3 Orbit 2
Orbit 2 contains warm supporting project memory:
- prior decisions,
- established design constraints,
- partially relevant earlier contracts,
- and context that still matters but should not compete directly with the active contract.

### 5.4 Orbit 3
Orbit 3 contains cold archive or deferred alternatives:
- past options,
- earlier forks,
- dormant concepts,
- and context worth preserving without keeping it close to the active kernel.

---

## 6. Why Orbit 0 governs

One of AIR’s central rules is:

> Orbit 0 governs on conflict.

This rule exists because continuity without precedence becomes ambiguity.

If all contracts remain equally alive, then narrowing cannot truly happen.
The session becomes a blended field rather than an active governed compile context.

Orbit 0 provides a stable answer to:
- which contract wins,
- which layer is active,
- and what should be preserved only as support.

That does not erase prior contracts.
It orders them.

### 6.1 Promotion, not erasure
AIR does not assume that a new governing contract destroys all earlier context.

Instead:
- new active-topic contract -> promote to Orbit 0
- earlier relevant contracts -> remain in outer orbits unless retired

This is important because project continuity often depends on preserving prior context without allowing it to over-govern the current narrowed task.

### 6.2 Why retirement must be explicit
AIR also treats retirement as explicit.

A prior contract should not silently disappear.
It should either:
- remain in outer orbit,
- be superseded explicitly,
- or be retired explicitly.

This is a runtime hygiene rule.
It reduces confusion later.

---

## 7. Contract narrowing and sub-contracts

One of the most important uses of orbit law is handling sub-contracts.

A broad project often narrows into:
- a trust sub-problem,
- a GTM sub-problem,
- a creative sub-problem,
- a relational continuity sub-problem,
- or another specialized contract layer.

Without explicit activation and orbit placement, the broader frame tends to stay too active.

AIR’s solution is:

- identify the narrower governing contract
- activate it explicitly
- move it into Orbit 0
- preserve the broader contract in outer orbit as parent/support

This gives AIR a way to narrow without forgetting.

That is one of the main practical benefits of orbit law.

---

## 8. Why orbit law improves handoff continuity

Handoff is where orbit law becomes especially valuable.

Without structured orbit state, continuation tends to depend on:
- large transcript replay,
- vague summary,
- or model inference about what still matters

That is expensive and fragile.

With orbit law, the handoff can preserve:
- active Orbit 0 contract
- task key
- topic
- parent/supporting contracts
- degraded mode
- blockers
- missing vectors
- next recommended step

This means the next session can load the active state much more cleanly.

In other words:

- transcript replay carries history
- orbit-aware handoff carries governance

AIR prefers the latter.

---

## 9. Why this is different from normal prompting

Normal prompting often leaves governance implicit.

The model is expected to infer:
- what is currently active,
- what is still relevant,
- what has been superseded,
- and what the user most likely wants to govern now.

That can work surprisingly often.
It also fails quietly.

AIR makes a different choice.

It says:
- active governance should not be inferred if it can be stated
- state transitions should not be silent if they can be materialized
- prior context should not be blended if it can be orbited
- narrowed work should not remain conceptually “candidate” if it is already governing

This is not merely more formal prompting.
It is a different theory of session control.

---

## 10. Why activation and orbit law belong together

Explicit contract activation without orbit law would still leave prior context poorly organized.

Orbit law without explicit activation would still leave the active layer ambiguous.

AIR therefore needs both.

### 10.1 Activation answers:
- what is governing?

### 10.2 Orbit law answers:
- where does everything else belong?

Together they provide:
- active control
- continuity
- narrowing
- handoff stability
- conflict resolution

That combination is what makes AIR more than a prompt style.

---

## 11. Failure patterns that justify the design

The need for explicit activation and orbit law became obvious through repeated live-session failures such as:

- correct contract identified but not activated
- new contract treated as candidate rather than governing
- broader prior contract staying too active
- supporting context blended back into Orbit 0
- session continuing under prose interpretation rather than runtime state
- handoff depending on transcript replay instead of state transfer

These failures all pointed to the same conclusion:

> state must be explicit, ordered, and emitted.

That is the reason AIR_SESSION exists.

---

## 12. Practical implications

Treating activation and orbit law as runtime law has several practical consequences.

### 12.1 Better patchability
If the session drifts, AIR can patch the state by:
- restating active Orbit 0 contract
- restating supporting outer-orbit contracts
- restating task binding
- restoring artifact-first mode

This is much harder if the active state only lives inside prose.

### 12.2 Better profile transitions
The default starter profile can give way to specialized profiles cleanly because:
- specialized profile can be promoted to Orbit 0
- starter profile can remain in outer orbit as bootstrap context

### 12.3 Better model comparison
Activation and orbit law create clearer criteria for evaluating model behavior:
- did it activate the right contract?
- did it preserve the right outer-orbit support?
- did it avoid blended scope?
- did it materialize state correctly?

This makes AIR behavior more inspectable.

---

## 13. Limitations

Explicit activation and orbit law improve control, but they do not solve everything.

Current limitations include:
- some models still describe state better than they truly bind to it
- prompts must still be carefully written
- session law can still be obeyed partially rather than fully
- handoff quality still depends on the correctness of the prior active state
- orbit modeling is more explicit than ordinary prompting, but still depends on model compliance

These are real limitations.
They do not weaken the design logic.
They explain why AIR must continue refining its runtime kit.

---

## 14. Conclusion

AIR treats explicit contract activation and orbit law as runtime law because persistent AI work requires more than conversational implication.

It requires:
- clear governance,
- explicit current control,
- structured support context,
- continuity without flattening,
- and handoff that preserves state rather than only story.

The core lesson is simple:

> in long-running work, the question is not only what the model understands.
> The question is what the session is actually running under.

Explicit contract activation answers that question.
Orbit law keeps the rest of the project intelligible around it.

That is why both are central to AIR.

---

## Suggested follow-up papers

- geometry classes in AIR
- fail-closed reasoning under incomplete evidence
- AIR handoff continuity as state persistence
- runtime patching and drift correction