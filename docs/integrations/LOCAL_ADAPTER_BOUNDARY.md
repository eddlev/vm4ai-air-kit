# Local Adapter Boundary

Stage 3 makes AIR reusable by local coding tools without making any host or protocol part of AIR's core.

## Shared services

Adapters must call the same installed services used by the terminal application:

- `vm4ai_air.boot.BootCompiler` for validation, planning, deterministic compilation, Q1-D orientation, and status;
- task packet, authorization envelope, and continuation packet builders under `vm4ai_air.boot`;
- the shared resource resolver, application paths, workspace manager, and atomic I/O services.

Adapters must not reimplement AIR module selection, approval rules, resource verification, or continuation semantics.

## Future local MCP adapter

The preferred first MCP form is an optional local `stdio` server. It should be read-only by default, restricted to registered AIR projects, and unable to execute arbitrary shell commands or browse arbitrary filesystem roots.

Potential resources include validated AIR bundles, project state, receipts, and contract schemas. Potential tools include boot validation, boot planning, project status, and project validation. Mutating tools require explicit capability-specific authorization plus approval provenance.

AIR as an MCP host or general orchestrator is a later and higher-risk design problem.

## Future coding-tool adapters

Codex and other coding tools may consume AIR through the terminal command, a local MCP adapter, or a thin plugin/skill package. The plugin is a distribution and activation surface, not a separate AIR implementation.

When AIR orchestrates a coding harness directly, the richer harness-native protocol should be preferred over flattening every event into generic MCP calls.

## Authority boundary

- A loaded bundle is not execution authorization.
- A task packet defines scope but grants no capability.
- An authorization envelope denies every omitted capability. A mutating capability requires an explicit actor and an `approval_ref` identifying the approval source; AIR never manufactures `USER_APPROVED` provenance.
- A continuation packet preserves the current step and pending approvals; it does not approve the next recommended step.
- Push, merge, tag, release, publication, destructive actions, and external network use remain distinct gates.
