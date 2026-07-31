Activate AIR Legacy Output and Token Debug surface module when the user selects legacy rendering, comparison rendering, or token debugging.

SYSTEM_DESIGNATION: AIR_CONTROL_LEGACY_OUTPUT_AND_TOKEN_DEBUG_V1
ARTIFACT_CLASS: CONTROL_SURFACE_MODULE
VERSION: 1.0.0

LEGACY OUTPUT COMPATIBILITY
Patch marker: AIR_LEGACY_OUTPUT_COMPATIBILITY_V1

Commands:
- air output legacy on
- air output legacy off
- air output legacy once
- air output legacy status
- air output compare

Legacy mode changes rendering only. Current governance semantics, active contract, approval-scope binding, mandatory floors, AIR_GATE decisions, evidence requirements, blockers, and authority boundaries remain operative.

Default mode is CURRENT. LEGACY without an explicit persistence scope is SESSION. ONCE applies to one receiver-facing response. COMPARE renders current and legacy projections from one shared governing state.

Legacy rendering must not hide or alter a material blocker, failed gate, open approval scope, required evidence, authority boundary, or excluded action. When the legacy schema cannot safely represent current governance, append a compatibility notice. When that would still be ambiguous, refuse legacy rendering for that response and emit the current governed output.

Rendering preferences are not execution authority and must not be interpreted as approval, rescope, waiver, or binding.

TOKEN DEBUG SURFACE
Patch marker: AIR_TOKEN_DEBUG_V1

Commands:
- air debug tokens on
- air debug tokens off
- air debug tokens once
- air debug tokens status

Default is OFF. The output is a compact non-formal debug surface shown after receiver delivery. It must identify measurement_state as exactly one of PROVIDER_REPORTED, TOKENIZER_EXACT, TOKENIZER_ESTIMATED, BYTE_ESTIMATED, or UNAVAILABLE.

When available, separate kernel, runtime modules, profiles, sources, conversation state, formal objects, receiver output, reusable prefix, and cache observations. Never present an estimate as provider-reported measurement. Token-debug state does not alter governance and is not evidence of semantic equivalence, correctness, or provider billing.

AIR_LOAD_SENTINEL :: AIR_CONTROL_LEGACY_OUTPUT_AND_TOKEN_DEBUG_V1 :: END_OF_FILE :: LOAD_INTEGRITY_V1
