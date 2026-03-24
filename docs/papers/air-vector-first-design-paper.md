# AIR Vector-First Design Paper

## Subtitle
Why AIR uses vector-primary compilation, explicit contract activation, orbit-based state handling, and fail-closed artifact-first outputs in live AI sessions.

---

## Abstract

AIR is a live-session compiler/runtime framework for structured AI work.

It was developed to address recurring weaknesses in normal prompting:
- prose-first drift,
- implicit state,
- poor continuity across sessions,
- weak handling of uncertainty,
- and silent blending of incompatible instructions or task frames.

AIR addresses these problems by making four things explicit:

1. **vectors as the operative layer**
2. **contracts as active runtime state**
3. **orbit-based handling of current vs supporting context**
4. **artifact-first, fail-closed output discipline**

The core claim of AIR is that live AI work improves when the session is treated less like a conversational exchange and more like a stateful compile context.

This paper explains the design intent behind AIR, why it is vector-first, why contract activation matters, why orbit state is necessary, and why AIR favors explicit missing vectors, blockers, obligations, and degraded modes over optimistic prose.

---

## 1. Problem statement

Normal prompting often works well for:
- one-off questions,
- short summaries,
- casual brainstorming,
- and loosely bounded rewriting.

It often works less well for live project sessions that require:
- continuity across multiple turns or sessions,
- explicit task governance,
- stable handling of narrowing or shifting scope,
- auditable reasoning boundaries,
- and reliable handoff from one session to another.

In these longer and more structured contexts, several failure modes appear repeatedly.

### 1.1 Prose-first drift
The model defaults into readable narrative before the operative structure of the task has been stabilized.

This leads to:
- confident explanation before state is clear,
- high token usage,
- and outputs that sound complete while leaving key execution gaps implicit.

### 1.2 Implicit contract handling
The model often “understands” instructions without explicitly activating them as governing state.

This leads to:
- acknowledged but unapplied policies,
- incorrect prioritization between old and new instructions,
- and ambiguous control of the active topic.

### 1.3 Silent blending
When multiple adjacent topics or instructions coexist, the model often blends them without declaring:
- what is active,
- what is supporting,
- what is superseded,
- and what is in conflict.

This is especially dangerous in:
- technical design,
- security-sensitive reasoning,
- long-running product work,
- relational or symbolic continuity-sensitive use cases,
- and multi-domain founder workflows.

### 1.4 Weak handoff continuity
Long projects frequently require continuation in a new session.

Normal prompting tends to make continuity expensive because:
- too much transcript must be replayed,
- the active task is poorly summarized,
- and prior state is carried as prose rather than structured runtime information.

### 1.5 Overconfidence under missing evidence
Standard prompting tends to prefer completion over explicit incompleteness.

That creates a recurring problem:
- unsupported assumptions are smoothed over,
- missing infrastructure is implied,
- confidence is simulated where AIR would rather expose a blocker.

---

## 2. AIR’s core design answer

AIR responds to these weaknesses by changing the unit of control.

Instead of treating the live session primarily as:
- a conversation,
- a roleplay,
- or a sequence of loosely constrained prompts,

AIR treats the session as:
- a **runtime-bound contract space**
- with an **active task kernel**
- operating on a **vectorized problem structure**
- under an **artifact-first output law**

This produces five central AIR moves:

1. **vector-primary reasoning**
2. **explicit contract activation**
3. **orbit-based context handling**
4. **fail-closed evidence discipline**
5. **handoff-oriented state persistence**

---

## 3. Why vector-first?

AIR is vector-primary.

That means:
- vectors are the operative layer
- roles are referential anchors only

### 3.1 Why not role-first?
Role-first prompting is often attractive because it is intuitive:
- “act like an architect”
- “behave like a strategist”
- “take the role of a researcher”

But role-first approaches have a weakness:
they compress too much of the task into a persona-like abstraction.

That often produces:
- stylistic coherence without operational precision,
- persuasive framing without explicit dependency logic,
- and implied competence instead of surfaced missing coverage.

Roles are useful as references.
They are not precise enough to be the primary execution layer.

### 3.2 What vectors provide
Vectors allow AIR to represent work in a way that is:
- more composable,
- more auditable,
- more comparable across sessions,
- and less dependent on personality framing.

A vector can correspond to:
- a capability,
- a missing layer,
- a required function,
- a trust boundary,
- an unresolved dependency,
- or a task-bearing dimension of the project.

This means AIR can say:
- what is present,
- what is missing,
- what is blocked,
- what is supporting,
- and what governs.

That is much more useful for live implementation-oriented work than saying:
- “this needs an architect”
- “this sounds strategic”
- or “this needs security expertise”

### 3.3 Why this matters in practice
Vector-first design is especially useful when:
- the project spans domains,
- the active topic narrows over time,
- missing layers matter,
- continuity must survive session boundaries,
- or multiple subcontracts emerge beneath a shared project center.

In those contexts, vectors preserve structure better than roles.

---

## 4. Explicit contract activation

AIR does not assume that an instruction has become active just because it was said.

A contract must be **activated**.

This is one of AIR’s key departures from normal prompting.

### 4.1 Why activation matters
Without explicit activation, models tend to:
- acknowledge instructions without binding to them,
- describe the correct contract without switching state,
- and treat governing contracts as “candidates” or “ready for promotion” rather than active runtime law.

This is a major source of hidden session failure.

### 4.2 AIR’s solution
AIR requires explicit session-state materialization.

In a proper AIR session, the model should emit:
- `AIR_SESSION`
before
- `AIR_ARTIFACT`

That session state should make visible:
- which contract is active,
- what topic/task it governs,
- what supporting contracts remain in orbit,
- and how conflicts are resolved.

This is the difference between:
- “I understand the contract”
and
- “I am operating under the contract”

### 4.3 Contract activation as runtime law
AIR treats contract activation as stateful, not rhetorical.

That allows:
- sub-contract promotion,
- parent/child contract relations,
- contract supersession,
- contract retirement,
- and conflict handling

to become explicit rather than implied.

---

## 5. Orbit-based state handling

AIR uses orbit state to handle continuity and topic layering.

### 5.1 Why orbit state exists
In long-running projects, not all prior context is equally active.

Some context is:
- currently governing,
- some is recent and highly relevant,
- some is supporting,
- some is archived but still potentially retrievable.

Normal prompting often collapses all of this into one undifferentiated memory blob.

That causes:
- blending,
- drift,
- wrong-priority recall,
- and difficulty deciding what should govern.

### 5.2 AIR orbit model
AIR uses four orbits:

- **Orbit 0** = active contract / active task kernel
- **Orbit 1** = hot recent verified context
- **Orbit 2** = warm prior relevant design decisions
- **Orbit 3** = cold archive / deferred alternatives

This gives AIR a principled way to represent:
- current governance,
- supporting context,
- and historical continuity
without flattening all of them into one pile.

### 5.3 Orbit 0 governs
One of AIR’s most important rules is:

**Orbit 0 governs on conflict.**

Earlier contracts do not disappear automatically.
They remain in outer orbit unless explicitly retired.

This preserves continuity while still making active control explicit.

### 5.4 Why this matters
Orbit state matters most when:
- a new contract narrows the topic,
- a specialized profile replaces a starter profile,
- multiple subprojects exist inside a shared project,
- or a session must be resumed later without replaying the entire transcript.

---

## 6. Fail-closed evidence discipline

AIR is intentionally conservative under uncertainty.

### 6.1 What fail-closed means
If something is not evidenced, AIR should not quietly invent it.

Instead, it should surface uncertainty explicitly through:
- `missing_vectors`
- `obligations`
- `blockers`
- `degraded_execution_mode`
- `dependency_edges`
- `vector_family_state_summary`

### 6.2 Why this matters
This is particularly important in:
- security and trust reasoning,
- architecture work,
- product planning,
- market or strategy work with incomplete evidence,
- and any context where false completeness is more dangerous than explicit incompleteness.

### 6.3 AIR’s stance
AIR prefers:
- explicit incompleteness
over
- smooth narrative overreach

That choice can feel harsher than normal prompting, but it is more operationally honest.

---

## 7. Artifact-first output

AIR is artifact-first.

That means the model should emit the structured AIR output before giving a narrative explanation.

### 7.1 Why artifact-first?
Because the operative result should not be buried under commentary.

Artifact-first output:
- reduces ambiguity,
- improves reuse,
- makes handoff cleaner,
- and reduces the chance that readable prose substitutes for actual structure.

### 7.2 AIR vs prose-first prompting
In prose-first prompting:
- explanation often arrives before the task is structurally stabilized

In AIR:
- state and artifact come first
- narrative is secondary
- narrative may be omitted entirely in minimal execution mode

This is especially useful for:
- long-running project work,
- multi-session continuity,
- implementation handoff,
- and cross-model comparison

---

## 8. Handoff continuity

AIR is designed for work that continues.

### 8.1 Why handoff matters
Without a compact handoff structure, continuation depends on:
- replaying large transcripts,
- re-explaining project state,
- and hoping the model infers the right active frame from too much prose.

That is inefficient and unstable.

### 8.2 AIR’s solution
AIR uses handoff cards derived from active session state.

A handoff card should summarize:
- active contract
- task key
- topic
- parent/supporting contracts
- degraded mode
- selected vectors
- missing vectors
- blockers
- dependency edges
- next recommended step
- runtime law

That makes continuity:
- lighter,
- clearer,
- and less dependent on raw transcript carryover.

---

## 9. Why AIR is not one universal geometry

The public AIR starter profile uses a structured bias:
- `GRID_LATTICE`
- `POLYTOPE_CORE`

This is appropriate for:
- deterministic compilation
- technical/safety-sensitive work
- architecture and trust-oriented scoping
- auditability-first tasks

But AIR is not intended to lock all work into one geometry forever.

### 9.1 Why geometry must vary
Different domains need different structural behavior.

A technical trust contract is not shaped like:
- a creative brand system,
- a GTM strategy,
- a relational symbolic continuity problem,
- or a high-dimensional marketing/narrative space.

### 9.2 AIR’s broader geometry intent
AIR should eventually support multiple geometry families, including:
- standard structured geometries,
- more fluid or multi-pole geometries,
- and experimental/radical geometries for different task domains.

This means:
- the default starter is a bootstrap profile,
- not a universal final profile.

---

## 10. AIR vs normal prompting

AIR should not be understood as “better prompting” in the trivial sense.

It is better understood as a different control model.

### 10.1 Normal prompting optimizes for:
- ease
- speed
- naturalness
- readable outputs

### 10.2 AIR optimizes for:
- explicit governance
- continuity
- structured incompleteness
- stateful task control
- reusable artifacts
- handoff stability

### 10.3 AIR’s tradeoff
AIR is not always the best tool for:
- casual ideation
- playful freeform interaction
- short one-off answers
- minimal-friction chatting

AIR becomes valuable when:
- the work is persistent,
- the consequences of drift matter,
- the contract matters,
- and the structure must survive multiple turns or sessions.

---

## 11. Current limitations

AIR is still evolving.

Current limitations include:
- contract activation can still fail if prompts are underspecified
- some models “understand” contracts better than they truly activate them
- artifact normalization varies by model
- geometry handling is broader in concept than in current public tooling
- use-case specific profiles are still being expanded

These are not reasons to avoid AIR.
They are reasons to treat the framework honestly as developing but already useful.

---

## 12. Conclusion

AIR exists because live project work needs more than good prose.

It needs:
- active contract control,
- explicit session state,
- orbit-aware continuity,
- vector-primary structure,
- fail-closed evidence handling,
- and reusable artifacts that survive beyond one conversation.

The core intuition behind AIR is simple:

**when the work becomes persistent, the session must become stateful.**

Vector-first design, explicit contract activation, orbit-based context handling, and artifact-first outputs are all consequences of that one shift.

AIR is therefore not merely a prompt style.

It is a framework for making live AI work more governable, inspectable, and continuable.

---

## Suggested follow-up papers

- AIR vs normal prompting
- explicit contract activation and orbit law
- geometry classes in AIR
- fail-closed reasoning in live sessions
- handoff continuity as runtime state persistence