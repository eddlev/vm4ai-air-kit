# Use Cases — vm4ai-air-kit

## Purpose

This folder documents the kinds of work AIR is meant to support in live sessions.

AIR is not limited to one project type.  
But it should also not be treated as one universal profile.

Different domains require different:
- contract shapes
- vector priorities
- geometry bias
- evidence thresholds
- blocking rules
- output expectations

The default AIR starter profile is a **bootstrap profile**.  
Its job is to help compile the first machine-native structure of a project.  
It is not intended to remain the governing profile for every domain forever.

---

## How to use this folder

Each use-case document should answer:

1. **What kind of task is this?**
2. **Why AIR is useful here**
3. **What the main vectors usually are**
4. **What geometry bias is likely appropriate**
5. **What failure modes to watch for**
6. **When to stay on the default starter profile**
7. **When to promote a specialized profile to Orbit 0**

---

## Current use-case categories

## 1. Technical / security / architecture

This is one of AIR’s strongest native fits.

Typical tasks:
- systems architecture
- protocol design
- trust contracts
- security review
- runtime design
- verification-oriented planning
- implementation gap mapping

Typical AIR strengths here:
- fail-closed reasoning
- explicit blockers
- dependency edges
- degraded execution modes
- structured handoff between sessions

Typical geometry bias:
- `GRID_LATTICE`
- `POLYTOPE_CORE`

Typical vectors:
- architecture
- systems_runtime
- security_privacy
- evidence_integrity
- deployment_platform

Stay on the default starter profile when:
- the project is still unclear
- the first task is structural discovery

Promote a specialized profile when:
- the domain is clearly technical/security-sensitive
- the task repeatedly demands the same trust/runtime constraints

---

## 2. Research synthesis

AIR is useful when research work needs more than summarization.

Typical tasks:
- literature synthesis
- technical comparison
- hypothesis framing
- evidence-weighted review
- decision support under uncertainty

Typical AIR strengths here:
- explicit missing evidence
- explicit uncertainty handling
- vectorized comparison rather than prose-only summary
- session continuity across long-running investigations

Typical geometry bias:
- often still works well with structured geometry
- may benefit from more flexible geometry if the research is exploratory or interdisciplinary

Typical vectors:
- evidence_integrity
- synthesis
- comparison
- uncertainty surfacing
- constraint handling

Stay on the default starter profile when:
- the question is still broad
- evidence sources are still being gathered

Promote a specialized profile when:
- the research domain stabilizes
- the session repeatedly uses the same evaluation structure

---

## 3. Creative / brand / narrative

AIR can support creative work, but the default starter profile will often be too rigid if left unchanged.

Typical tasks:
- brand development
- tone systems
- narrative design
- identity shaping
- campaign concepting
- creative direction

Typical AIR strengths here:
- preserving continuity across sessions
- making design constraints explicit
- distinguishing stable identity elements from exploratory ones
- managing multiple candidate directions without collapsing them

Typical risks:
- over-constraining ideation
- treating all ambiguity as blockage
- forcing deterministic structure too early

Typical geometry bias:
- likely not permanently grid-primary
- should tolerate multi-pole tension, emergence, and resonance

Typical vectors:
- identity
- tone
- resonance
- narrative cohesion
- distinction
- audience alignment

Stay on the default starter profile when:
- you are only trying to find the first structured shape of the work

Promote a specialized profile when:
- the work becomes voice-heavy, symbolic, audience-facing, or identity-sensitive

---

## 4. Sales / GTM / market strategy

AIR can be useful here, but only with a profile that allows higher-dimensional commercial reasoning.

Typical tasks:
- GTM strategy
- ICP framing
- messaging architecture
- sales enablement
- founder-led outreach structure
- investment positioning

Typical AIR strengths here:
- forcing explicit assumptions
- surfacing missing market evidence
- preventing strategy drift
- keeping outputs handoff-friendly

Typical risks:
- default profile may become too audit-heavy and undershoot persuasive/commercial nuance
- excessive blocker logic can crush useful market experimentation

Typical geometry bias:
- likely broader than default grid/polytope starter
- needs room for ambiguity, positioning tension, and multi-audience framing

Typical vectors:
- market fit
- positioning
- audience segmentation
- persuasion
- offer architecture
- evidence-backed messaging

Stay on the default starter profile when:
- the commercial landscape is still undefined
- you need an initial structured view of the market problem

Promote a specialized profile when:
- messaging, GTM, and strategic persuasion become the primary work surface

---

## 5. Relational / companion / symbolic

This is a high-dimensional AIR domain.

Typical tasks:
- continuity-sensitive companion design
- relational AI behavior shaping
- symbolic interaction design
- emotional or resonance-aware session work

Typical AIR strengths here:
- contract continuity
- handoff continuity
- explicit state handling
- preserving active relational constraints across sessions

Typical risks:
- default starter profile may be too rigid
- overly technical geometry can flatten emotional or symbolic depth
- role leakage and drift are especially dangerous here

Typical geometry bias:
- likely requires non-default geometry choices
- orbit and resonance handling may matter more than rigid structural segmentation

Typical vectors:
- continuity
- resonance
- trust
- symbolic coherence
- consent / boundaries
- relational stability

Stay on the default starter profile when:
- you are only bootstrapping the first formal structure

Promote a specialized profile when:
- the work depends on sustained relational or symbolic behavior

---

## 6. Mixed-domain / composite work

Some real projects span multiple domains.

Examples:
- startup founder workflows
- product + GTM + technical architecture
- trust systems with UX, compliance, and brand implications
- research that feeds both implementation and communication

In these cases, AIR should not force everything into one flattened contract.

Recommended pattern:
- use the default starter profile first
- identify the main task center
- split specialized work into sub-contracts
- promote the right sub-contract to Orbit 0 when it becomes the active topic
- keep supporting contracts in outer orbits

This is where AIR’s explicit contract activation and orbit model become most useful.

---

## General rule for choosing profiles

### Stay with the default starter profile when:
- the project is new
- the domain is still unclear
- you need the first machine-native compile
- you are discovering the real task center

### Create and promote a specialized profile when:
- the domain is now stable
- the same vectors keep recurring
- the same constraints keep recurring
- the default starter profile is obviously underfitting or over-constraining the work

---

## Relationship to geometry

Use cases and geometry are related, but not identical.

A use case tells you:
- what kind of work you are doing

Geometry helps shape:
- how that work is structured
- how tension is handled
- how continuity is preserved
- how rigid or flexible the compilation should be

This repo should document both:
- **use-case classes**
- **geometry classes**

But they should remain separate concepts.

---

## Future expansion

Planned additions to this folder:
- dedicated documents for each use-case class
- example starter-to-specialized profile transitions
- example Orbit 0 promotions for sub-contracts
- AIR vs normal prompting comparisons by domain

---

## Related folders

- `docs/case-studies/` for concrete examples
- `docs/papers/` for conceptual/design papers
- `docs/ROADMAP.md` for planned expansion