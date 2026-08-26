# AIR empirical evaluation

This directory is the empirical evaluation surface for AIR.

AIR already separates deterministic release evidence from model-dependent evidence. The repository `tests/` harness covers claims that can be checked as `REPRODUCIBLE_EXECUTABLE`. Model, judge, tool-use, and long-horizon task evaluations belong here as `REPLAYABLE_EVALUATION`: their inputs, procedure, model/tool identities, trajectories, and repeated-run stability must be recorded.

## Core question

The primary experiment is not "how good is AIR?" in isolation. It is:

> Holding the model, tools, task, environment, and budget policy constant, what changes when AIR is added?

AIR should therefore be evaluated as a project-governance/runtime intervention around a host model.

## Experimental conditions

The suite reserves five conditions:

- `BASE` — task and environment instructions without AIR.
- `CONTROL` — a strong conventional project prompt with comparable instructional richness, but without AIR formal objects or AIR-specific governance mechanisms.
- `AIR` — the current public AIR foundation and approved task-local configuration.
- `AIR_NO_SFV` — AIR with the Specification-First Verification mechanism removed for ablation studies.
- `AIR_NO_CONTINUITY` — AIR with Handoff/continuity mechanisms removed for ablation studies.

`BASE` versus `AIR` is the minimum matched comparison. `CONTROL` is required before attributing gains to AIR rather than to prompt length or generic structure. Ablations are required before attributing gains to a particular AIR mechanism.

## What to measure

The initial metric families are:

- benchmark-native task success
- scope violation rate
- approval violation rate
- false-closure rate
- unsupported-evidence rate
- ambiguity handling / rescope detection
- specification-adequacy detection
- interruption recovery rate
- state-loss rate after interruption
- human review burden
- execution overhead: tokens, latency, tool calls, approvals, and cost
- run-to-run consistency

Definitions and scoring rules live in `AIR_EVAL_PROTOCOL_V0_1.md`.

## AIR-specific evaluation suite

`air-eval-suite.json` defines perturbation templates aimed at AIR's own claims: scope integrity, approval boundaries, evidence integrity, specification adequacy, continuity, prompt-injection resistance, and false-closure resistance.

These are **task templates**, not claimed benchmark results. A template becomes empirical evidence only when it is instantiated in a concrete environment, run under recorded conditions, and scored with the protocol.

## External benchmark targets

The initial external targets are:

- Terminal-Bench 2 — end-to-end terminal work
- MCP-Atlas — multi-step MCP/tool use
- TheAgentCompany — simulated professional work
- PaperBench — long-horizon AI research replication
- RE-Bench — ML research-engineering work

Adapters for these benchmarks are not yet claimed implemented. The evaluation contract is intentionally framework-neutral so that Inspect AI, Harbor, or benchmark-native harnesses can write into the same AIR run-record format.

## Run records

Every empirical run should preserve at least:

- task/suite identity
- experimental condition
- model/provider identity and relevant inference settings
- AIR source revision and prompt hashes when AIR is active
- tool/environment identities
- input and perturbation identity
- complete or externally archived trajectory reference
- task-native result
- AIR-specific metric values
- judge identity and rubric when a judge is used
- tokens, latency, tool calls, approvals, and cost when observable
- interruption/recovery events when applicable
- failure or invalid-run reason

The machine-readable contract is `air-eval-run.schema.json`.

## Reporting discipline

Prefer task-native or deterministic graders. Use blinded human or model judging only where necessary, and report judge identity separately from the system under test.

Report matched results by task and model, repeated-run stability, uncertainty intervals, and overhead. Do not collapse capability, governance reliability, and cost into a single unexplained score.

Negative results remain results. AIR may improve governance while increasing cost or reducing throughput; those trade-offs must remain visible.

## Structural validation

The repository CI validates the evaluation contract itself without calling any model APIs:

```bash
python evals/validate_eval_suite.py
```

A green structural check proves only that the evaluation definitions are internally consistent. It does **not** prove that AIR performs better than a baseline.
