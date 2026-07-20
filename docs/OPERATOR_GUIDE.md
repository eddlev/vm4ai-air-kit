# AIR Operator Guide

## 1. Operating model

AIR separates five things that ordinary chat often mixes together:

1. **Project state** — purpose, scope, constraints, and roadmap.
2. **Active step** — the single current execution centre, called Orbit 0.
3. **Artifact plane** — formal AIR objects used for execution and review.
4. **Benchmark plane** — the task-fitted standard used to judge work.
5. **Receiver plane** — the output delivered after evaluation permits it.

AIR is prompt-compiled unless a backend artifact is actually supplied. Keep that boundary visible.

## 2. Boot choices

### Monolithic boot

Attach the files under `prompts/`. This is the easiest path and the highest context-cost path.

### Modular boot

The boot tool uses the repository root as its path-safety boundary; runtime functions live under `runtime/`. Its manifest selects entry and task modules by trigger. Validate before bundling.

```bash
python runtime/boot/tools/air-boot.py validate-manifest
python runtime/boot/tools/air-boot.py status
python runtime/boot/tools/air-boot.py compare --triggers NEW_PROJECT
```

## 3. Onboarding

AIR asks Q1-Q6 one at a time.

- **Q1** selects new, import, continuation, or orientation.
- **Q2** controls review strictness.
- **Q3** controls ambiguity posture.
- **Q4** selects continuity priorities.
- **Q5** defines the project and initial sources.
- **Q6** defines the working agreement and delivery form.

Q1 is never silently inferred. Q2-Q6 may use only visibly permitted, correctable inference under the runtime rules.

## 4. Object visibility

The approved default is `OBJECT_ALL`.

- Every formal object created, restored, updated, or made operative is printed separately.
- A compact summary cannot substitute for the actual formal object.
- AIR does not create future-step objects solely to display them.
- Required blockers, errors, handoff objects, and safety gates cannot be hidden.

Useful controls:

```text
air object all
air compact
air verbose
air quiet
air status
```

Reduced visibility changes presentation, not governance.

## 5. Sources and patching

Before material patching, AIR must request or confirm the exact source set in the current session. Prior output, remembered filenames, and conversation summaries do not satisfy the patch-source gate.

The operator provides source truth and approves irreversible or external actions. AIR must report which files it used and what evidence supports closure.

## 6. Capability layers

- A **Specialist** changes reusable judgment and review posture.
- A **Domain Package** supplies terminology, standards, failure modes, and evidence expectations.
- A **Method** defines task-local procedure.
- A **Method Pack** standardizes a recurring low-variance procedure.
- An **Executor** is a bounded operation contract, not an autonomous agent.
- A **Policy Pack** returns a policy decision; it does not grant scope.
- An **Evaluation Pack** defines tests; it does not prove they ran.

Generation and binding remain approval-separated.

## 7. Evidence and decisions

AIR_GATE decisions include `ALLOW`, `REVIEW`, `REJECT`, `RESCOPE_REQUIRED`, and `EVIDENCE_REQUIRED`.

Distinguish:

- prompt-declared state;
- file-observed state;
- tool-observed state;
- operator-witnessed state;
- cryptographically verified payload state;
- backend-enforced state.

Do not upgrade one evidence class into another by wording.

## 8. Handoff continuity

Prompt-only handoffs can restore declared state but are structurally unauthenticated. The optional local verifier can sign, verify, and maintain a continuity anchor. Verification, restoration, and authorization are separate decisions.

See [Handoff tool](tools/handoff.md).

## 9. Local policy evaluation

The OPA adapter is optional and local-first. It does not download OPA, open a public port, or send data to a central AIR service. If OPA is absent, AIR remains prompt-native and should report the missing tool rather than inventing a tool result.

## 10. Completion

A step closes only when the scoped output exists, required evidence is present, blockers are stated, approval state is honest, and the next transition is explicit. A written method or cited source is not execution evidence.
