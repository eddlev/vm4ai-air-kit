# Changelog

## v0.3.0

- Uses a function-oriented repository taxonomy: canonical system prompts in `prompts/`, complete specialist packages in `profiles/<specialist name>/`, and implementation/support assets in `runtime/<function>/`.
- Removes duplicate prompt and specialist payloads from `runtime/`.
- Adds package manifests plus bounded Grounding Executor and Capability Ecology Method components so each specialist package has profile, domain, method, and executor roles.

- Aligns the public monolithic prompts and grounding profiles with the approved WS7 file set.
- Adds the self-contained modular runtime, Boot Kernel, 22-module graph, local planner/bundler, load receipts, and portability evidence.
- Makes **OBJECT_ALL** the default formal-object visibility mode: every formal object that is created, restored, updated, or made operative is printed canonically, without manufacturing future-step objects.
- Adds the artifact lifecycle, source/control registry, human-to-machine translator, capability construction adapters, deterministic policy package, handoff integrity tooling, Capability Ecology Architect, and Domain Capability Registry.
- Adds operator, architecture, dependency, installation, troubleshooting, rollback, release, command, object, and local-tool documentation.
- Adds the WS7 tool-runtime-outage recovery case study.

### Claim boundary

AIR remains a prompt-native framework. Optional local tools provide tool-observed evidence; they do not provide general execution authorization, legal compliance, guaranteed correctness, or the private AIR backend/client runtime.
