# AIR Runtime Resources

`runtime/` remains the canonical authoring location for function-oriented AIR resources:

- boot;
- modules;
- artifact lifecycle;
- policy;
- handoff;
- source control.

Application code now belongs under `src/vm4ai_air/`.

During package construction, the build hook verifies and includes `runtime/` in the installed AIR resource set. Runtime consumers must access those files through the shared resource resolver rather than construct repository-relative paths.

The repository-relative tools under `runtime/*/tools/` remain temporary compatibility implementations until their approved migration stages. They must not become a second implementation of shared package logic.


## Stage 3 boot status

The installed `air boot` service now validates the boot graph, applies semantic trigger closure, compiles deterministic bundles, and preserves the Complete AIR Prompt Set fallback. The repository-relative `runtime/boot/tools/air-boot.py` file is a compatibility adapter to that shared service.
