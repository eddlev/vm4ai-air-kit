# v0.3.0 Repository Structure

## Canonical placement

```text
prompts/
  AIR CORE RUNTIME.md
  AIR CONTROL SURFACE.md
  AIR DEFAULT STARTER PROFILE.json

profiles/
  grounding specialist/
    specialist profile
    domain pack
    method
    executor
    package manifest
  capability ecology architect/
    specialist profile
    domain pack
    method
    executor
    package manifest

runtime/
  boot/
  modules/
  artifact-lifecycle/
  policy/
  handoff/
    templates/AIR HANDOFF CARD TEMPLATE.json
  source-control/
```

The earlier v0.3.0 candidate copied prompt and specialist payloads into `runtime/`. This revision removes those copies. The boot manifest now resolves canonical files from the repository root.

## Migration from the earlier candidate

Discard the earlier unreleased v0.3.0 overlay. Do not merge both trees. Use this structure-revised overlay as one coherent set.
