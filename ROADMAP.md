# AIR Prompt Runtime Roadmap

This roadmap is for the prompt-version AIR repository.

It does not cover the private backend implementation except where prompt-side compatibility or public documentation requires mention.

## Roadmap principles

- keep the prompt-version repo honest about scope
- strengthen AIR as a prompt-native runtime
- preserve map-first, active-step-only execution
- add agent-bridge capability without turning AIR into the agent runtime
- improve usability before increasing complexity

## Current status

### v0.1.0 — Initial public prompt runtime
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
- tested behavior on ChatGPT 5.4, Claude Sonnet 4.6, and Gemini Thinking

## Near-term roadmap

### v0.1.1 — Prompt/runtime polish
Goal:
Tighten the public prompt kit and improve first-use clarity.

Planned:
- improve README and quick-start clarity
- add cleaner visual assets for repo and posts
- standardize repo description and topics
- refine release notes and public-facing language
- document Gemini Thinking boot note clearly

Success criteria:
- new users can boot AIR from the README without extra explanation
- repo clearly reads as prompt-version only
- no ambiguity between public prompt kit and private backend

### v0.2.0 — Agent Execution Bridge
Goal:
Allow prompt-version AIR to generate structured execution specs for external agent runtimes like OpenClaw.

Planned:
- define `AGENT_EXECUTION_SPEC`
- add rules for when AIR may emit agent-ready instructions
- keep agent execution external to AIR
- add documentation and examples
- add operator guidance for AIR -> agent -> AIR loop

Success criteria:
- AIR can produce one clean, active-step-specific agent execution spec
- the spec is concrete enough for an external agent to act on
- AIR remains the planning/control layer, not the execution runtime

### v0.3.0 — Stronger continuation and governance
Goal:
Make continuation, orbit discipline, and state handoff more robust.

Planned:
- refine handoff card semantics
- make orbit model more visible in docs
- improve restoration flow for continuation sessions
- add guidance for multi-session project progression
- document conflict handling and degraded state more explicitly

Success criteria:
- continuation works reliably with less operator correction
- handoff cards feel like real restoration objects
- orbit model is understandable to new users

## Mid-term roadmap

### v0.4.0 — Specialized prompt profiles
Goal:
Add specialized public prompt profiles for distinct project classes while keeping the default starter simple.

Potential additions:
- technical / architecture profile
- research synthesis profile
- GTM / narrative profile
- compliance / evidence-heavy profile

Rules:
- keep starter profile as the default
- do not fragment the public repo into prompt sprawl
- specialized profiles must remain compatible with the same AIR runtime laws

Success criteria:
- specialized profiles improve fit without breaking the common runtime model
- users can still understand the default path quickly

### v0.5.0 — Public evaluation and examples
Goal:
Show how AIR behaves in practice across real project scenarios.

Planned:
- example project boots
- example handoff flow
- example active-step artifact progression
- example agent execution bridge output
- comparison between generic chat workflow vs AIR runtime workflow

Success criteria:
- users can see AIR in action without guessing how it works
- examples reinforce the actual workflow rather than abstract theory

## Longer-term direction

### Backend-connected AIR
This remains outside the public prompt-only repo for now.

Longer-term goals may include:
- backend compilation of AIR artifacts
- stronger typed state and validation
- automated project map updates
- direct agent orchestration
- runtime persistence beyond prompt-only continuity

Public prompt repo role in that future:
- remain the public prompt-native layer
- remain useful even without backend access
- stay honest about what is prompt-only vs backend-backed

## Non-goals for the prompt-version repo

These are not current goals for this repository:
- publishing an SDK
- pretending the prompt kit is a backend runtime
- turning AIR into an autonomous agent executor
- bloating the repo with too many profiles too early
- replacing the private backend repo with markdown abstractions

## Working model

AIR should continue to operate as:

1. project activation
2. roadmap creation
3. active-step artifact generation
4. optional agent execution bridge
5. state handoff
6. continuation

That is the spine.

Everything added to the prompt-version repo should strengthen that flow, not blur it.
