# AIR User Guide

For a fast start, use [QUICK_START.md](QUICK_START.md). For complete operating doctrine, use [OPERATOR_GUIDE.md](OPERATOR_GUIDE.md).

AIR is a prompt-native project runtime that makes project state, active steps, blockers, evidence, approvals, and delivery decisions explicit.

## Basic workflow

1. Boot with the monolithic or modular path.
2. Complete Q1-Q6 onboarding.
3. Review the project initialization brief and execution map.
4. Work only on the active step.
5. Provide exact source files for patching.
6. Review AIR_GATE and evidence state before closure or mutation.
7. Generate a handoff card before moving sessions.

## Visibility

The default is `OBJECT_ALL`. Formal objects are visible by default, while planned future artifacts remain uncreated.

## Local tools

The boot planner, handoff verifier, and OPA adapter are optional. Each tool's output is limited to its observed scope and does not create backend enforcement.

## More information

- [Architecture](ARCHITECTURE.md)
- [Commands](reference/commands.md)
- [Capability layers](reference/capability-layers.md)
- [Troubleshooting](TROUBLESHOOTING.md)
