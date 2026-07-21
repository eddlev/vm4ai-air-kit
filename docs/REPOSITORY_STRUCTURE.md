# AIR Repository Structure

```text
.github/workflows/
  ci.yml
  package.yml

src/vm4ai_air/
  application code
  package-owned schemas

prompts/
  AIR CORE RUNTIME.md
  AIR CONTROL SURFACE.md
  AIR DEFAULT STARTER PROFILE.json

profiles/
  grounding specialist/
  capability ecology architect/

runtime/
  boot/
  modules/
  artifact-lifecycle/
  policy/
  handoff/
  source-control/

tests/
  unit/
  integration/
  package/

docs/
release/
examples/
```

## Canonical placement

The top-level `prompts/`, `profiles/`, and `runtime/` directories are the authoring source for canonical AIR resources.

The build hook copies the verified resource set into a wheel under:

```text
vm4ai_air/resources/air/
```

That wheel content is generated distribution output. Do not check in a second manually maintained resource copy under `src/`.

## Application code

All new local-runtime code belongs under `src/vm4ai_air/`. Shared behaviour must be implemented there before legacy wrappers delegate to it.

Repository-relative scripts under `runtime/*/tools/` are temporary compatibility surfaces until their approved migration stages.
