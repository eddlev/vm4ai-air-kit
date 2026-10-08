==================================================
TOOL GATEWAY ENFORCEMENT BOUNDARY LAW
==================================================

Patch marker: AIR_TOOL_GATEWAY_ENFORCEMENT_BOUNDARY_V2

Prompt-compiled AIR can surface and apply the interlock but cannot guarantee that a host model or tool runtime will never skip it.

When a backend, client wrapper, MCP gateway, connector proxy, or operator harness is available, the recommended enforcement contract is:
- reject material tool calls without a valid AIR_ACTION_AUTHORIZATION
- validate artifact id, revision, lease id, action id, target scope, and expiry
- consume authorization atomically with the tool call
- return evidence sufficient to construct AIR_ACTION_RECEIPT
- reject replay, target substitution, scope expansion, or stale authorization
- preserve an append-only authorization and receipt trace

Do not claim gateway enforcement unless tool or backend evidence proves it.

