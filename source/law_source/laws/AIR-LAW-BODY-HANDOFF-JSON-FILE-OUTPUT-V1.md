==================================================
HANDOFF JSON FILE OUTPUT LAW
==================================================

Patch marker: AIR_HANDOFF_STRICT_JSON_OUTPUT_V3
Patch marker: AIR_HANDOFF_FILE_DELIVERY_V1

When the user requests final AIR_HANDOFF_CARD output:
- construct the card as current governed state, never as inline chat text
- serialize exactly one top-level root key AIR_HANDOFF_CARD into AIR_HANDOFF_CARD.json using a JSON serializer
- use UTF-8 with no BOM
- require schema_version = Core CANONICAL_HANDOFF_SCHEMA_VERSION
- require template_revision = Core CANONICAL_HANDOFF_TEMPLATE_REVISION and a valid positive user_revision for the generated lineage
- require the legacy root card_revision field to be absent from current generated output
- reopen the exact written bytes and require strict JSON parse, duplicate-key rejection, one-root validation, schema validation, surfaced-object provenance validation, and failure-mode integrity validation
- emit normal chat-side AIR governance records, an external file delivery receipt, the download link, and the normal runtime anchor where otherwise required
- if downloadable file creation or exact post-write validation is unavailable, fail closed with no inline fallback

RT.ALIGN and all dependencies required to construct the card still execute. DEP.HANDOFF_GENERATION_EVALUATION must be satisfied, and the file root carries that generation provenance only through the current evaluation_basis field required by schema. A separate root handoff_generation_evaluation carrier is prohibited. No prior-session or serialized evaluation becomes current execution authority on restore.

