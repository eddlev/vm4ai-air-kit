# AIR Command Reference

| Command | Purpose | Posture |
|---|---|---|
| `air status` | Show active project, step, objects, blockers, and load state | Read-only |
| `air help` | Describe commands and gates | Read-only |
| `air object all` | Print all current formal objects | Read-only |
| `air compact` | Reduce optional surface detail | Presentation only |
| `air verbose` | Expand visible state | Presentation only |
| `air quiet` | Suppress optional chatter, not required objects | Presentation only |
| `air task` | Show or steer the current task | May require rescope |
| `air scope` | Inspect active scope | Read-only unless changed |
| `air evidence` | Show evidence state | Read-only |
| `air sources` | Show source plan and blockers | Read-only |
| `air gate` | Show current AIR_GATE decision | Read-only |
| `air approve?` | Show exactly what approval would authorize | Read-only |
| `air handoff` | Generate continuation object | Handoff gate |
| `air patch plan` | Plan a file-backed patch | Read-only planning |
| `air patch` | Execute an approved file-backed patch | Mutation/evidence gates |

No command bypasses governing contracts, evidence, approval, or safety constraints.
