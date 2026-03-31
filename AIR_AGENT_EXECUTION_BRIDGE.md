# AIR Agent Execution Bridge

This document defines the prompt-version bridge between AIR and external AI agent runtimes such as OpenClaw.

AIR does not replace the agent runtime.

AIR does:
- define the current active step
- determine whether the step is ready for execution
- surface blockers and dependencies
- generate a structured execution specification for the agent

The agent runtime does:
- execute tools
- call APIs
- modify files
- run commands
- return outputs and evidence

## Core rule

AIR defines the work.
The agent executes the work.

AIR should only emit an agent execution spec when:
- the current active step is clear
- dependencies are explicit
- blockers are either resolved or explicitly accepted
- inputs and outputs can be stated concretely

If those conditions are not met, AIR should not emit an execution spec as if the step were ready.

## AGENT_EXECUTION_SPEC

```json
{
  "AGENT_EXECUTION_SPEC": {
    "spec_version": "1.0",
    "runtime_origin": "PROMPT_COMPILED",
    "project_id": null,
    "task_id": null,
    "active_step_id": null,
    "active_step_label": null,
    "objective": null,
    "execution_mode": "SINGLE_STEP",
    "agent_target": null,
    "inputs": [],
    "required_context": [],
    "instructions": [],
    "constraints": [],
    "dependencies": [],
    "blockers": [],
    "assumptions": [],
    "tools_allowed": [],
    "tools_disallowed": [],
    "expected_outputs": [],
    "output_format": null,
    "validation_checks": [],
    "failure_conditions": [],
    "handoff_on_completion": [],
    "evidence_requirements": [],
    "notes_for_operator": []
  }
}
```

## Field definitions

### `spec_version`
Version of the execution spec schema.

### `runtime_origin`
Where the AIR state came from.
Typical values:
- `PROMPT_COMPILED`
- `BACKEND_COMPILED`

### `project_id`
Optional stable identifier for the project.

### `task_id`
Optional stable identifier for the broader task.

### `active_step_id`
Identifier for the current active step in the project map.

### `active_step_label`
Human-readable name of the current active step.

### `objective`
The exact outcome the agent is expected to produce.

### `execution_mode`
Recommended values:
- `SINGLE_STEP`
- `MULTI_ACTION_SINGLE_GOAL`
- `BATCH_SUPPORTING_ACTIONS`

Default recommendation:
- prefer `SINGLE_STEP`

### `agent_target`
The external execution system.
Examples:
- `OpenClaw`
- `Codex`
- `Custom Agent`

### `inputs`
Explicit inputs the agent should use.
Examples:
- file paths
- prompt files
- prior artifact names
- repo locations
- user-provided constraints

### `required_context`
Context that must remain visible during execution.

### `instructions`
The ordered instructions the agent should follow.

These should be executable, concrete, and step-scoped.

### `constraints`
Hard limits on execution.

### `dependencies`
Requirements that must already exist before the agent runs.

### `blockers`
Reasons execution should stop or remain provisional.

### `assumptions`
Explicit assumptions the operator is allowing for this execution.

### `tools_allowed`
Tools or capabilities the agent is allowed to use.

### `tools_disallowed`
Tools or capabilities the agent must not use.

### `expected_outputs`
What the agent is expected to return.

### `output_format`
The shape the result should take.

### `validation_checks`
How AIR or the operator will verify success.

### `failure_conditions`
Conditions that make the run invalid even if something was produced.

### `handoff_on_completion`
What AIR should do after the agent succeeds.

### `evidence_requirements`
What proof of execution must be returned.

### `notes_for_operator`
Anything AIR wants the human operator to know before or after execution.

## Emission rules

AIR should emit `AGENT_EXECUTION_SPEC` only when:
- the current active step is ready for execution
- the requested work is concrete enough for an agent
- the step has a clear success condition

AIR should not emit it when:
- the project is still in exploration only
- blockers would make execution speculative
- the step is not yet the current active step
- the request is still missing critical inputs

## Minimal recommended pattern

When AIR hands off to an agent, prefer this sequence:

1. update the project execution map
2. identify the current active step
3. emit one `AGENT_EXECUTION_SPEC`
4. let the agent execute
5. verify outputs
6. update the map again

Do not emit multiple large execution specs by default.
Keep it active-step only.
