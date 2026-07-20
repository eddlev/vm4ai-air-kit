# AIR Beginner Quick Start

AIR is a set of prompt files and optional local tools that help an AI session work as a governed project rather than an unstructured chat.

## Choose a boot path

### Full prompt boot

Use this when your model has enough context for the complete prompt files.

Attach the three files in `prompts/`:

1. `AIR CORE RUNTIME.md`
2. `AIR CONTROL SURFACE.md`
3. `AIR DEFAULT STARTER PROFILE.json`

Then say:

```text
Start a new AIR project.
```

AIR asks six onboarding questions. Q1 chooses new project, import, continuation, or beginner orientation. AIR must not guess Q1 from your boot sentence.

### Modular boot

Use this when you want a smaller local bundle selected from the module graph.

```bash
python runtime/boot/tools/air-boot.py validate-manifest
python runtime/boot/tools/air-boot.py bundle --trigger NEW_PROJECT --output air-new-project.md
```

Attach `air-new-project.md` to the model and start the project normally.

## What you should see

AIR should show its formal objects. The default is `OBJECT_ALL`: every object that AIR actually instantiates or changes is printed. Planned future artifacts remain planned until their step becomes active.

## Continuing later

Ask AIR to generate a handoff card. In a new session attach:

- `prompts/AIR CORE RUNTIME.md` or a suitable modular bundle
- the handoff card
- optionally `prompts/AIR CONTROL SURFACE.md`

Then say:

```text
Continue project from handoff card.
```

## Boundaries

AIR prompt behavior is not backend enforcement. A local tool result proves only what that tool observed. Signatures authenticate the signed payload under a configured key; they do not authorize general execution or prove legal identity.
