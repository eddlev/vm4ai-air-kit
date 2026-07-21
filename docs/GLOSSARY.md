# AIR Glossary

**AIR_ARTIFACT** — Formal task object containing execution state, method, evidence, blockers, benchmark state, and delivery state.

**AIR_GATE** — Decision boundary for material execution, mutation, approval, closure, handoff, and rescope.

**Active contract** — Current scope, allowed actions, stop conditions, and evidence requirements.

**Artifact plane** — Formal objects used to govern and review work.

**Backend-compiled** — State produced by an actual AIR backend. Never infer this from prompt behaviour or local tools.

**Benchmark identity** — Synthetic task-fitted judge composed from constraints, vectors, and evidence expectations.

**Complete AIR Prompt Set** — The canonical three-file prompt-native fallback under `prompts/`.

**Domain Package** — Referential domain constraints and terminology. It cannot govern Orbit 0 by itself.

**Executor** — Bounded callable operation contract; not an agent.

**Handoff card** — Structured continuation object for restoring project state.

**Installed resource set** — The build-verified copy of canonical AIR resources carried inside the Python wheel.

**Materialization receipt** — Local record connecting an installed resource ID and digest to a cache path and declared purpose.

**Method Pack** — Reusable procedure with evidence-to-advance gates.

**OBJECT_ALL** — Visibility mode that prints every instantiated or changed formal object without inventing future objects.

**Orbit 0** — Current active task or contract centre.

**Package version** — Version of the installed Python application code.

**Project workspace** — Registered, project-isolated local directory containing mutable AIR state, bundles, handoffs, evidence, exports, and logs.

**Prompt-compiled** — AIR behaviour instructed within a model session, without backend enforcement.

**Receiver delivery state** — Whether evaluated output is delivered, held for review, rejected, or awaiting evidence.

**Resource-set version** — Content-derived identity of the canonical resources embedded in a package build.

**Specialist** — Reusable capability and evaluation posture.

**Tool-observed** — Result produced by a local tool. It is stronger than model self-report for that observation, but limited to the tool's scope.
