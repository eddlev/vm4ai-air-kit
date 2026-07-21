# Stage 3 Local Validation Record

**Development version:** `0.5.0.dev0`
**Scope:** deterministic modular boot, semantic Q1 branch closure, complete Q1-D orientation, Complete AIR Prompt Set fallback, and adapter-facing contracts
**Environment:** Linux / Python 3.13 implementation container
**Claim boundary:** local implementation evidence only; Windows, macOS, additional Python versions, and cross-model behavior remain CI or operator evidence.

## Source and regression tests

```text
Ruff: PASS
pytest -m "not package": 78 passed, 2 deselected
```

The regression set covers:

- declared kernel, starter, semantic-closure, receipt-schema, Complete AIR Prompt Set, and module byte verification;
- required kernel, starter, semantic-closure, and Markdown-module structure even when a source tree is rebuilt self-consistently after tampering;
- independent decomposition-map and exact-content binding for every derived Markdown module, including rejection of marker-only replacements;
- dependency graph safety and deterministic ordering;
- full Q1 session-entry branch closure;
- complete 11-section Q1-D orientation and no-activation boundary;
- visible unknown-trigger fallback to the Complete AIR Prompt Set;
- byte-deterministic compilation for normalized equivalent trigger sets;
- exact length-framed embedded bytes whose per-resource digests match the embedded segments;
- fallback plan identity bound to package version, resource-set version, and full source-tree digest;
- protection against writing bundle output into canonical authoring roots;
- transactional bundle/receipt output rollback, shared-target concurrency locking, post-write verification, and same-path rejection;
- task, authorization, and continuation contract builders and schemas, including fail-closed capability typing and explicit approval provenance for mutating capabilities in both Python and JSON Schema validation;
- the repository-relative `air-boot.py` compatibility adapter.

## Distribution validation

```text
wheel build: PASS
source distribution build: PASS
Twine metadata check: PASS for both distributions
isolated wheel installation test: PASS
isolated source-distribution installation test: PASS
package tests: 2 passed, 78 deselected
```

Each isolated distribution test installs into a fresh virtual environment, runs `pip check`, executes outside the repository, verifies packaged resources, validates Stage 3 boot closure, loads an installed contract schema, compiles a bundle, and validates a project workspace.

The general implementation container has a pre-existing unrelated `moviepy`/`pillow` dependency conflict, so a global `python -m pip check` is not clean evidence for AIR. The fresh wheel and source-distribution environments both completed their scoped `pip check` successfully.

## Installed application smoke test

The wheel was installed through pipx and invoked through the pipx environment's exact executable path outside the repository.

Observed results:

- `air --json boot validate` — PASS;
- default `air --json boot plan` — `SESSION_ENTRY`, with Q1-D and handoff-continuation closure present;
- coding/repository bundle and separate receipt creation — PASS;
- installed authorization schema loading — PASS;
- `air --json boot q1d` — complete orientation present and `activation_state = NOT_ACTIVATED`;
- uninstall — PASS.

## Resource and graph evidence

```text
installed AIR resources: 73
boot modules: 23
boot validation checks: 216
boot validation failures: 0
resource set: v0.5.0-dev+sha256.f5fed5d74899
source tree digest: sha256:f5fed5d748994c1d968a6f0a00325c95f5379a5c347f52288219d9e3434dfd66
```

These values identify this local candidate only. Documentation edits or other canonical resource changes legitimately change the resource-set digest.

## Reproducible build

Two wheel and source-distribution builds using the same `SOURCE_DATE_EPOCH` were byte-for-byte identical.

## Stage 3 review remediation

The structured review reproduced five defects: optional structural checks in self-consistent packages, resource digests that could differ from normalized embedded text, concurrent bundle/receipt interleaving, fallback plan IDs not bound to the resource set, and authorization builders that could synthesize `USER_APPROVED`. A follow-up adversarial review found two narrower gaps: marker-only derived modules could still pass, and the published JSON Schema did not yet enforce approval provenance. The completed remediation converts all seven reproductions into fail-closed contracts and regression tests and adds a distinct terminal review exit for unknown-trigger fallback.

## Still required after remediation push

- Windows 11 / Python 3.13 operator validation of the remediation commit;
- GitHub Actions source matrix on Windows, macOS, and Linux with Python 3.11-3.14 for the remediation commit;
- installed-distribution factor matrix on all three operating-system families for the remediation commit;
- final structured review of the remediation diff;
- empirical cross-model tests for Q1 behavior, Q1-D rendering, active-step preservation, blockers, evidence gates, and receiver-facing delivery.

## Intentionally deferred

- local MCP server implementation;
- Codex or other coding-tool plugin packaging;
- AIR acting as an MCP host;
- handoff signing and trust-anchor migration;
- local policy execution;
- upgrade and rollback commands;
- tag, release, PyPI publication, and public announcement;
- publication of the AI-agent incident case study before primary-source verification and safe fixture reproduction.
