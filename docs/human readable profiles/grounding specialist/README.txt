# AIR Markdown Versions

These Markdown files are human-readable reference copies only.

Canonical AIR startup/runtime objects are the corresponding `.json` files.

Use:
- `.json` files for model upload, AIR profile loading, domain pack loading, and machine-readable configuration.
- `.md` files for human review, GitHub browsing, doctrine inspection, and change discussion.

Do not load these `.md` files as AIR runtime contracts, specialist profiles, domain packs, or source-of-truth configuration unless explicitly converted back into validated JSON.

Maintenance rule:
When the matching JSON profile or domain pack is patched, update the Markdown reference in the same release window so human-readable doctrine does not drift from canonical JSON.
