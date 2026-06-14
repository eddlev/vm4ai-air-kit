# AIR User Guide

AIR is a prompt-based AI project runtime.

It helps an AI session behave less like a loose chatbot and more like a structured project runtime. AIR creates a project flow, tracks the active step, surfaces blockers, preserves continuity, and helps decide what can be delivered, what needs review, and what should stop.

AIR is prompt-native. The public AIR Kit does not include a backend runtime, signed contracts, or automatic enforcement outside the model session.

## What AIR is

AIR is a prompt framework for governed AI work.

It helps with:

- starting projects in a controlled way
- defining the current active step
- keeping future steps in a roadmap instead of executing everything at once
- surfacing blockers and missing evidence
- preserving project continuity through handoff cards
- distinguishing discussion, execution, review, and delivery
- keeping claims bounded to available evidence

## What AIR is not

AIR is not:

- a backend runtime
- an autonomous agent executor
- a guarantee of truth
- a replacement for testing
- a signed or tamper-evident contract system
- a tool runner
- a magic shield against bad model behavior

AIR can improve prompt-side discipline, but prompt-side discipline is not backend validation.

## Recommended boot bundle

For a new project, attach:

- `prompts/AIR CORE RUNTIME.md`
- `prompts/AIR CONTROL SURFACE.md`
- `prompts/AIR DEFAULT STARTER PROFILE.json`

Then say:

```text
Start a new AIR project.
