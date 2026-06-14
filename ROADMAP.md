# AIR Prompt Runtime Roadmap

This roadmap is for the public prompt-based AIR Kit.

It does not cover the private AIR backend/client runtime.

## Scope

This repository is limited to prompt-native AIR.

In scope:

- AIR prompt files
- starter profiles
- optional specialist profiles
- handoff templates
- public documentation
- prompt-side usage guidance
- prompt-side model portability notes
- examples and case studies for prompt-native AIR

Out of scope:

- backend validation
- runtime enforcement
- signed or tamper-evident contracts
- autonomous agent execution
- private AIR backend/client features
- speculative backend-connected public roadmap

## Roadmap principles

- keep the public prompt kit honest about scope
- strengthen AIR as a prompt-native runtime
- preserve map-first, active-step-only execution
- improve first-use clarity
- preserve model portability
- avoid speculative feature promises
- avoid prompt sprawl unless a profile has concrete public value

## Current status

### v0.1.0 - Initial public prompt runtime

Status: released

Delivered:

- AIR Core Runtime Prompt
- AIR Control Surface Prompt
- AIR Default Starter Profile
- AIR Handoff Card Template
- README for prompt-version usage
- orientation-first startup
- project execution map
- active-step-only artifact discipline
- handoff continuity

## Current objective

### v0.1.1 - Public prompt-kit clarity and portability patch

Goal:

Make the public AIR Kit easier to boot, easier to understand, and more honest about prompt-only scope.

Planned:

- remove obsolete agent bridge material from the public kit
- update README with prompt-only scope
- add AIR User Guide
- add model portability notes
- add strict boot guidance for models that reinterpret AIR
- add Q1 tutorial path documentation
- document declaration-first workflow conventions
- document cross-model handoff testing results
- keep backend/runtime claims out of public prompt-kit documentation

Success criteria:

- new users can boot AIR from the README without extra explanation
- README clearly describes AIR Kit as prompt-based only
- docs explain what AIR is and is not
- model portability notes give practical boot and handoff guidance
- no public documentation implies backend validation, runtime enforcement, signed contracts, or autonomous agent execution

## Candidate prompt-only improvements

These are concrete prompt-kit improvements that may be worth adding if they remain useful and non-speculative.

### Better examples

Possible additions:

- example new-project boot
- example import flow
- example handoff card
- example continuation session
- example AIR help response
- example AIR compact vs verbose response
- example REVIEW_GATE and REJECT_REPORT

Value:

Examples make AIR easier to understand without adding new runtime claims.

### Compatibility test log

Possible additions:

- small public table of tested model behavior
- status labels for boot and handoff tests
- recommended prompt variants per model class
- known failure modes

Value:

This supports model portability without pretending compatibility is permanent.

### Prompt-kit release checklist

Possible additions:

- README check
- prompt file consistency check
- Q1-Q5 check
- handoff template check
- model portability note check
- claim boundary check
- mojibake/encoding check

Value:

This helps keep the public kit clean after prompt changes.

### Lightweight case studies

Possible additions:

- small project planning case
- coding-planning case
- research synthesis case
- handoff continuation case
- ambiguity handling case

Value:

Case studies demonstrate AIR behavior without requiring backend features.

### Additional specialist profiles

Possible additions only if clearly useful:

- research synthesis specialist
- technical architecture review specialist
- product strategy specialist
- documentation/rewrite specialist

Rules:

- do not add profiles just to fill the repo
- each profile must have a clear public prompt-side use case
- each profile must remain compatible with AIR Core Runtime
- each profile must preserve prompt/backend claim boundaries

## Non-goals

The public prompt-version repo will not aim to:

- publish an SDK
- pretend the prompt kit is a backend runtime
- provide runtime enforcement
- provide signed or tamper-evident artifacts
- act as an autonomous agent executor
- promise provider-independent reliability
- bloat the repo with too many profiles too early
- replace the private backend/client implementation

## Working model

AIR should continue to operate as:

1. project activation
2. project map creation
3. current active-step artifact generation
4. review and receiver delivery
5. handoff
6. continuation

The public kit should remain useful without backend access.
