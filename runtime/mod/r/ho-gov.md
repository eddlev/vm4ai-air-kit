Activate AIR Handoff Governance State module when a handoff is created, restored, validated, signed, or compared.
SYSTEM_DESIGNATION: AIR_RUNTIME_HANDOFF_GOVERNANCE_STATE_V1
ARTIFACT_CLASS: RUNTIME_MODULE
VERSION: 1.0.0

The canonical AIR_HANDOFF_CARD_TEMPLATE 1.3.0 remains readable. New handoffs using this module have effective schema version 1.4.0 and include a nested governance_state object conforming to runtime/ho/s/gov.json.

Required governance_state fields are prompt_edition, governance_floor_version, open_approval_gate, active_framework_projections, source_rights_states, token_debug_preference, and restricted_source_text_included=false.

An open approval gate must preserve gate_id, exact question, authorized_action_ids, excluded_action_ids, received-but-unapplied input, scope_binding_check, and next permitted action. Restoration cannot convert missing fields in a 1.3.0 card into approval. Missing governance state restores as LEGACY_HANDOFF_GOVERNANCE_UNKNOWN and routes material execution to REVIEW until current state is re-established.

Handoff carries source identities, editions, digests, rights states, and projection references only. Paid, restricted, confidential, or licensed source text is excluded.

Edition restoration changes representation only. It cannot weaken current governance or bypass MO validation status.

AIR_LOAD_SENTINEL :: AIR_RUNTIME_HANDOFF_GOVERNANCE_STATE_V1 :: END_OF_FILE :: LOAD_INTEGRITY_V1
