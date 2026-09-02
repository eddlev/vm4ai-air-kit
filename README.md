<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-light.svg?v=20260830-air250">
    <img src="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-dark.svg?v=20260830-air250" alt="AIR by VM4AI — Focused. Fluid. AIR. AI work, carried forward." width="100%">
  </picture>
</p>

# AIR by VM4AI

[![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)](LICENSE)
[![Foundation](https://img.shields.io/badge/foundation-2.5.0-C9A227?labelColor=1A1613)](prompts/AIR_CORE_RUNTIME.md)
![Channel](https://img.shields.io/badge/channel-preview-FF5A1F?labelColor=1A1613)

**AI work, carried forward.**

AIR (**AI Resource**) is a prompt-based project runtime for sustained AI work. It carries explicit project state across sessions and compatible AI platforms through a governed five-file Foundation and Handoff.

AIR is prompt-compiled and host-model governed. It is not a hidden-memory system or backend enforcement layer.

[Get started](https://vm4ai.com/get-started.html) · [How AIR works](https://vm4ai.com/how-it-works.html) · [Documentation](https://vm4ai.com/air-docs.html) · [Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) · [Issues](https://github.com/eddlev/vm4ai-air-kit/issues)

## Current release

**AIR Kit v0.6.0-preview.1** carries the AIR Foundation **2.5.0** Preview / Development release.

| Component | Version |
| --- | ---: |
| AIR Kit | `0.6.0-preview.1` |
| Core Runtime | `2.5.0` |
| Control Surface | `2.5.0` |
| Default Starter | `2.5.0` |
| Governance Supplement | `2.3.0` |
| Handoff schema | `2.3.0` |
| Specialist packages | `2.4.0` |
| Runtime Route Map | `1.0.0` |
| Specialist Package Index | `1.1.1` |

Preview means the release is available for real use and field feedback without claiming Stable behavioral certification, universal provider/model compatibility, deterministic LLM behavior, or backend enforcement.

## Start AIR

Attach all five files from [`prompts/`](prompts/) to a fresh compatible AI session:

1. `AIR_CORE_RUNTIME.md`
2. `AIR_CONTROL_SURFACE.md`
3. `AIR_GOV.md`
4. `AIR_DEFAULT_STARTER_PROFILE.json`
5. `AIR_HANDOFF_CARD_TEMPLATE.json`

Then send:

```text
Start a new AIR project.
```

To continue an existing AIR project, load the same current Foundation together with the populated `AIR_HANDOFF_CARD` from the previous session and choose the continuation route. Handoff carries recorded project state; the destination session revalidates and rebinds execution authority.

## Repository structure

```text
catalog/   discovery metadata for routes and Specialist packages
profiles/  optional reusable Specialist capability packages
prompts/   canonical five-file AIR Foundation
```

### `prompts/`

The canonical AIR runtime distribution. These five files are the complete Foundation required for a normal AIR boot.

### `catalog/`

Foundation-adjacent discovery metadata:

- `AIR_RUNTIME_ROUTE_MAP.json`
- `AIR_SPECIALIST_PACKAGE_INDEX.json`

The catalog improves discovery and route salience. It does not independently create selection, approval, binding, or execution authority.

### `profiles/`

Optional Specialist capability packages currently include:

- Capability Ecology Architect
- AI Governance Specialist
- Grounding Specialist
- Specification-First Verification Specialist

Availability does not automatically select or bind a Specialist. AIR validates package identity and task fit before use.

## Compatibility and evidence boundary

Compatibility is empirical and configuration-dependent. Provider/model versions, context budget, attachment handling, system instructions, available tools, and host behavior can affect AIR.

The Foundation and package files are versioned and integrity-checked. Those checks establish repository/package integrity; they do not prove external tool effects, factual correctness, deterministic model inference, or provider certification.

For implementation guidance, compatibility notes, testing methodology, and release information, use the [VM4AI documentation](https://vm4ai.com/air-docs.html) and GitHub Releases.

## Community and bugs

Use [GitHub Issues](https://github.com/eddlev/vm4ai-air-kit/issues) for reproducible defects and [GitHub Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) for questions, integrations, portability observations, design discussion, and feature ideas.

Do not post exploitable security details publicly.

## License and brand

The project code and prompt materials are licensed under **Apache-2.0**; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

AIR/VM4AI names and brand marks are separate from the code license. Reusable brand assets live in [eddlev/air-brand](https://github.com/eddlev/air-brand).

---

**Built with AIR, reviewed by a human.**
