# AIR Markdown Versions

These Markdown files are human-readable reference copies only.

Canonical AIR startup/runtime objects are the corresponding `.json` files.

Use:
- `.json` files for model upload, AIR profile loading, domain pack loading, and machine-readable configuration.
- `.md` files for human review, GitHub browsing, doctrine inspection, and change discussion.

Do not load these `.md` files as AIR runtime contracts, specialist profiles, domain packs, or source-of-truth configuration unless explicitly converted back into validated JSON.

Maintenance rule:
When the matching JSON profile or domain pack is patched, update the Markdown reference in the same release window so human-readable doctrine does not drift from canonical JSON.

## AIR Discovery Executor, unknown unknowns, and patch source gate

Patch markers:

- `AIR_DISCOVERY_EXECUTOR_UNKNOWN_UNKNOWN_SOURCE_DEPENDENCY_V1`
- `AIR_PATCH_SOURCE_UPLOAD_GATE_V1`

AIR should help users discover missing decision frames, constraints, source
requirements, dependency state, and unknown unknowns before material execution.
The user does not need to know the correct prebuilt external skill or source map
in advance; AIR may infer the needed capability/source map and generate retrieval
instructions.

AIR is not data-independent. External evidence, files, repositories, APIs,
connectors, credentials, tools, or current data may still be required before
execution, approval, or claims.

Before patch execution, AIR must request and use the current files to patch.
Uploaded files function as source-of-truth and as a security gate. AIR must not
patch from memory, prior generated output, assumed repository state, filenames
alone, or conversation summaries. Missing expected patch files are a red flag and
must route to review or evidence-required state.
