# AIR_Q5B_PROVIDER_PROVENANCE_MIGRATION_V1
# Legacy migration never fabricates provider identity/generation/instance/namespace/storage/authorization/retention/deletion facts.
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


class MigrationError(Exception):
    pass


def reject_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise MigrationError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_dupes)
    except Exception as exc:
        if isinstance(exc, MigrationError):
            raise
        raise MigrationError(f"{path}: strict JSON parse failed: {exc}") from exc


def canonical_sha(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def version_tuple(value: str) -> tuple[int, ...]:
    try:
        parts = tuple(int(part) for part in value.split("."))
    except Exception as exc:
        raise MigrationError(f"invalid numeric version {value!r}") from exc
    if not parts:
        raise MigrationError(f"invalid numeric version {value!r}")
    return parts


def require_one_root(doc: dict[str, Any]) -> dict[str, Any]:
    if set(doc) != {"AIR_HANDOFF_CARD"}:
        raise MigrationError("expected exactly one AIR_HANDOFF_CARD root")
    card = doc["AIR_HANDOFF_CARD"]
    if not isinstance(card, dict):
        raise MigrationError("AIR_HANDOFF_CARD must be an object")
    return card


def current_template_card(current_template_doc: dict[str, Any]) -> dict[str, Any]:
    tmpl = require_one_root(current_template_doc)
    if tmpl.get("TEMPLATE_DESIGNATION") != "AIR_HANDOFF_CARD_TEMPLATE_V2":
        raise MigrationError("current template designation mismatch")
    if tmpl.get("SCHEMA_VERSION") != "2.3.0" or tmpl.get("schema_version") != "2.3.0":
        raise MigrationError("current template must be schema 2.3.0")
    if tmpl.get("template_revision") != 20:
        raise MigrationError("current template must be template_revision 20")
    if "card_revision" in tmpl:
        raise MigrationError("current rev20 template must not emit card_revision")
    return tmpl


def _copy_missing_required_root_carriers(card: dict[str, Any], tmpl: dict[str, Any]) -> None:
    manifest = tmpl.get("schema_manifest", {})
    required = manifest.get("required_fields", [])
    if not isinstance(required, list):
        raise MigrationError("current template required_fields invalid")
    for field in required:
        if field not in card:
            card[field] = copy.deepcopy(tmpl.get(field))


def _normalize_visibility_authority(card: dict[str, Any], tmpl: dict[str, Any], legacy: bool) -> None:
    if "object_visibility_authority_state" in card and isinstance(card["object_visibility_authority_state"], dict):
        return
    state = copy.deepcopy(tmpl.get("object_visibility_authority_state", {}))
    if card.get("object_visibility_mode") == "MINIMUM_REQUIRED_OBJECTS" and legacy:
        state["authority_source"] = "LEGACY_UNVERIFIED_SELECTION"
        state["selection_evidence_ref"] = None
        state["restoration_state"] = "REVIEW_REQUIRED_CLAMP_TO_ALL_OBJECTS"
    else:
        state["authority_source"] = "IMMUTABLE_DEFAULT_BASELINE"
        state["selection_evidence_ref"] = None
        state["restoration_state"] = "MIGRATED_DEFAULT_PENDING_CURRENT_VALIDATION" if legacy else state.get("restoration_state")
    card["object_visibility_authority_state"] = state


def _normalize_non_authority_boundaries(card: dict[str, Any], tmpl: dict[str, Any]) -> None:
    ext = card.setdefault("extensions", {})
    if not isinstance(ext, dict):
        ext = {"legacy_extensions_value": copy.deepcopy(ext)}
        card["extensions"] = ext
    clamped = ext.setdefault("migration_clamped_history", {})

    scope = card.get("open_approval_scope")
    if scope not in (None, {}, []):
        clamped["open_approval_scope"] = copy.deepcopy(scope)
        card["open_approval_scope"] = None

    ag = card.get("action_governance_state")
    if isinstance(ag, dict):
        if ag.get("open_authorizations"):
            clamped["open_authorizations"] = copy.deepcopy(ag.get("open_authorizations"))
            ag["open_authorizations"] = []
        if "material_actions_authorized" in ag:
            ag["material_actions_authorized"] = False
        ag["restoration_effect"] = "NEW_AUTHORIZATION_REQUIRED_FOR_ANY_MATERIAL_ACTION"

    # Current transfer carriers are historical bootstrap provenance only.
    transfer = card.get("transfer_ownership_contract")
    if not isinstance(transfer, dict):
        card["transfer_ownership_contract"] = copy.deepcopy(tmpl.get("transfer_ownership_contract"))


def _normalize_legacy_history(card: dict[str, Any], tmpl: dict[str, Any], source_template_revision: int | None) -> None:
    # Missing legacy history is never treated as complete. Start a fresh current-session
    # durable boundary rather than reconstructing old chat turns.
    if "failure_mode_state" not in card or not isinstance(card.get("failure_mode_state"), dict):
        fm = copy.deepcopy(tmpl.get("failure_mode_state", {}))
        fm["state"] = "LEGACY_UNRECORDED_PRE_DURABLE_BOUNDARY"
        fm["records"] = []
        fm["history_completeness_state"] = "LEGACY_UNRECORDED_PRE_DURABLE_BOUNDARY"
        fm["positive_execution_authority"] = "NONE"
        if source_template_revision is not None:
            fm["legacy_source_template_revision"] = source_template_revision
        card["failure_mode_state"] = fm

    if "surfaced_object_ledger_state" not in card or not isinstance(card.get("surfaced_object_ledger_state"), dict):
        sl = copy.deepcopy(tmpl.get("surfaced_object_ledger_state", {}))
        sl["state"] = "LEGACY_UNRECORDED_PRE_DURABLE_BOUNDARY"
        sl["entries"] = []
        sl["completeness_state"] = "LEGACY_UNRECORDED_PRE_DURABLE_BOUNDARY"
        sl["positive_execution_authority"] = "NONE_HISTORY_ONLY"
        if isinstance(sl.get("provenance_capture"), dict):
            sl["provenance_capture"]["durability_state"] = "LEGACY_PRE_DURABLE_BOUNDARY"
            sl["provenance_capture"]["write_readback_state"] = "NOT_AVAILABLE_FOR_LEGACY_HISTORY"
            sl["provenance_capture"]["coverage_through_capture_cutoff"] = "LEGACY_HISTORY_UNRECORDED"
            sl["provenance_capture"]["strict_handoff_eligibility"] = "CURRENT_SESSION_CAPTURE_REQUIRED"
            sl["provenance_capture"]["historical_chat_turn_retrieval_required"] = False
            sl["provenance_capture"]["transcript_export_or_paste_fallback"] = "PROHIBITED"
            for _k in ("provider_identity","provider_class","provider_generation","provider_instance_id","project_namespace_id","project_namespace_fingerprint","storage_location_class","retention_policy","deletion_policy"):
                sl["provenance_capture"][_k] = None
            sl["provenance_capture"]["authorization_state_at_capture"] = "LEGACY_UNRECORDED"
            sl["provenance_capture"]["credentials_serialized"] = False
        card["surfaced_object_ledger_state"] = sl


def _finalize_current_card(
    source_doc: dict[str, Any],
    current_template_doc: dict[str, Any],
    *,
    source_schema_version: str,
    source_template_revision: int | None,
    source_user_revision: int | None,
    source_compatibility_profile: str,
    revision_semantics_source: str,
    migration_path: str,
    migration_decision: str,
) -> dict[str, Any]:
    src = require_one_root(source_doc)
    tmpl = current_template_card(current_template_doc)
    out = copy.deepcopy(source_doc)
    card = out["AIR_HANDOFF_CARD"]

    legacy_card_revision = card.pop("card_revision", None)
    card["TEMPLATE_DESIGNATION"] = tmpl["TEMPLATE_DESIGNATION"]
    card["template_designation"] = tmpl["template_designation"]
    card["SCHEMA_VERSION"] = tmpl["SCHEMA_VERSION"]
    card["schema_version"] = tmpl["schema_version"]
    card["template_revision"] = 20
    card["user_revision"] = source_user_revision
    card.setdefault("object_version", "2.0.0")
    card.setdefault("record_class", "TRANSFER_RECORD")
    card["backend_validation_claimed"] = False
    card["hidden_reasoning_claimed"] = False

    _normalize_visibility_authority(card, tmpl, legacy=True)
    if "profile_posture_acceptance_state" not in card:
        pa = copy.deepcopy(tmpl.get("profile_posture_acceptance_state", {}))
        pa["accepted_weaker_postures"] = []
        pa["history_state"] = "LEGACY_UNRECORDED"
        pa["restoration_state"] = "CLAMP_TO_DEFAULT_STARTER_BASELINE_PENDING_CURRENT_VALIDATION"
        card["profile_posture_acceptance_state"] = pa

    _normalize_legacy_history(card, tmpl, source_template_revision)
    _normalize_non_authority_boundaries(card, tmpl)
    _copy_missing_required_root_carriers(card, tmpl)
    mode = card.get("handoff_mode_state")
    if isinstance(mode, dict):
        mode["request_mode"] = "UNRESOLVED"
        mode["selected_mode"] = "UNRESOLVED"
        mode["selection_state"] = "NOT_EVALUATED"
        mode["selection_reason"] = None
        mode["strict_eligibility_state"] = "NOT_EVALUATED"
        mode["portable_eligibility_state"] = "NOT_EVALUATED"
        mode["historical_provenance_claim"] = "NOT_EVALUATED"
        mode["positive_execution_authority"] = "NONE"
        mode["restoration_state"] = "MIGRATED_INPUT_MODE_REEVALUATION_REQUIRED"

    ms = copy.deepcopy(tmpl.get("migration_state", {}))
    old_ms = src.get("migration_state") if isinstance(src.get("migration_state"), dict) else {}
    for key in [
        "legacy_q4_c_state", "legacy_q4_d_state", "legacy_prompt_mode_state",
        "legacy_orbit_state", "legacy_active_contract_state", "legacy_governance_state",
        "unresolved_legacy_states", "legacy_history_state",
    ]:
        if key in old_ms:
            ms[key] = copy.deepcopy(old_ms[key])
    ms["source_schema_version"] = source_schema_version
    ms["migration_required"] = True
    ms["migration_decision"] = migration_decision
    ms["revision_migration_path"] = migration_path
    ms["source_template_revision"] = source_template_revision
    ms["source_user_revision"] = source_user_revision
    ms["legacy_card_revision"] = legacy_card_revision
    ms["revision_semantics_source"] = revision_semantics_source
    ms["source_compatibility_profile"] = source_compatibility_profile
    ms["legacy_user_revision_state"] = "RECORDED_FROM_LEGACY_CARD_REVISION" if source_user_revision is not None and source_schema_version == "2.2.0" else ("PRESERVED_EXPLICIT" if source_user_revision is not None else "UNRECORDED")
    ms["user_revision_counting_epoch"] = "LEGACY_2_2_CARD_REVISION_COUNTER" if source_schema_version == "2.2.0" else ("EXPLICIT_USER_REVISION" if source_user_revision is not None else "STARTS_WITH_NEXT_SUCCESSFUL_REV20_HANDOFF")
    ms["source_schema_manifest_sha256"] = canonical_sha(src.get("schema_manifest", {}))
    card["migration_state"] = ms
    card["schema_manifest"] = copy.deepcopy(tmpl["schema_manifest"])

    # Current rev20 cards never emit legacy card_revision.
    card.pop("card_revision", None)

    required = set(tmpl["schema_manifest"]["required_fields"])
    missing = sorted(required - set(card))
    if missing:
        raise MigrationError("migrated card missing current required root carriers: " + ", ".join(missing))
    if card.get("template_revision") != 20 or "card_revision" in card:
        raise MigrationError("rev20 revision/mode state not normalized")
    if card.get("surfaced_object_ledger_state", {}).get("positive_execution_authority") != "NONE_HISTORY_ONLY":
        raise MigrationError("migrated surfaced-object history gained authority")
    return out


def migrate_legacy_2_2_floor(doc: dict[str, Any], current_template_doc: dict[str, Any]) -> dict[str, Any]:
    src = require_one_root(doc)
    if src.get("TEMPLATE_DESIGNATION") != "AIR_HANDOFF_CARD_TEMPLATE_V2" or src.get("template_designation") != "AIR_HANDOFF_CARD_TEMPLATE_V2":
        raise MigrationError("legacy 2.2 source template designation mismatch")
    if src.get("SCHEMA_VERSION") != "2.2.0" or src.get("schema_version") != "2.2.0":
        raise MigrationError("source is not schema 2.2.0")
    starter = src.get("profile_stack", {}).get("starter_profile", {})
    if starter.get("SYSTEM_DESIGNATION") != "AIR_DEFAULT_STARTER_V2":
        raise MigrationError("legacy 2.2 starter designation mismatch")
    starter_version = starter.get("PROMPT_VERSION")
    if not isinstance(starter_version, str) or version_tuple(starter_version) < version_tuple("2.4.3"):
        raise MigrationError("legacy 2.2 source is below the supported Starter 2.4.3 compatibility floor")
    user_revision = src.get("card_revision")
    if not isinstance(user_revision, int) or isinstance(user_revision, bool) or user_revision < 1:
        raise MigrationError("legacy 2.2 card_revision must be a positive user revision counter")
    return _finalize_current_card(
        doc,
        current_template_doc,
        source_schema_version="2.2.0",
        source_template_revision=None,
        source_user_revision=user_revision,
        source_compatibility_profile="AIR_HANDOFF_LEGACY_COMPAT_FLOOR_2_2_0_STARTER_2_4_3_V1",
        revision_semantics_source="LEGACY_2_2_CARD_REVISION_IS_USER_REVISION",
        migration_path="LEGACY_2_2_FLOOR_TO_REV19_TO_REV20",
        migration_decision="MIGRATED_LEGACY_2_2_FLOOR_TO_REV20_PENDING_CURRENT_ALIGNMENT_MODE_REEVALUATION_AND_ARTIFACT_REBINDING",
    )


def migrate_schema_2_3_pre_rev19(doc: dict[str, Any], current_template_doc: dict[str, Any]) -> dict[str, Any]:
    src = require_one_root(doc)
    if src.get("SCHEMA_VERSION") != "2.3.0" or src.get("schema_version") != "2.3.0":
        raise MigrationError("source is not schema 2.3.0")
    if src.get("template_revision") is not None:
        source_template_revision = src.get("template_revision")
    else:
        source_template_revision = src.get("card_revision")
    if not isinstance(source_template_revision, int) or isinstance(source_template_revision, bool):
        raise MigrationError("schema 2.3 pre-rev19 source template revision missing")
    tmpl = current_template_card(current_template_doc)
    contract = tmpl.get("schema_manifest", {}).get("revision_migration_contracts", {}).get("SCHEMA_2_3_PRE_REV19_TO_REV19", {})
    supported = contract.get("supported_source_template_revision_range", [13, 18])
    if not (isinstance(supported, list) and len(supported) == 2 and supported[0] <= source_template_revision <= supported[1]):
        raise MigrationError(f"unsupported schema 2.3 source template revision {source_template_revision}")
    explicit_user_revision = src.get("user_revision")
    if explicit_user_revision is not None and (not isinstance(explicit_user_revision, int) or isinstance(explicit_user_revision, bool) or explicit_user_revision < 1):
        raise MigrationError("explicit schema 2.3 user_revision must be a positive integer when present")
    return _finalize_current_card(
        doc,
        current_template_doc,
        source_schema_version="2.3.0",
        source_template_revision=source_template_revision,
        source_user_revision=explicit_user_revision,
        source_compatibility_profile="AIR_HANDOFF_SCHEMA_2_3_PRE_REV19_SUPPORTED_GENERATION",
        revision_semantics_source="SCHEMA_2_3_PRE_REV19_CARD_REVISION_IS_TEMPLATE_REVISION_WHEN_SPLIT_ABSENT",
        migration_path=f"SCHEMA_2_3_REV{source_template_revision}_TO_REV19_TO_REV20",
        migration_decision=f"MIGRATED_SCHEMA_2_3_REV{source_template_revision}_TO_REV20_PENDING_CURRENT_ALIGNMENT_MODE_REEVALUATION_AND_ARTIFACT_REBINDING",
    )


def migrate_schema_2_3_rev19(doc: dict[str, Any], current_template_doc: dict[str, Any]) -> dict[str, Any]:
    src = require_one_root(doc)
    if src.get("SCHEMA_VERSION") != "2.3.0" or src.get("schema_version") != "2.3.0":
        raise MigrationError("source is not schema 2.3.0")
    if src.get("template_revision") != 19 or "card_revision" in src:
        raise MigrationError("source is not canonical schema-2.3 rev19 input")
    user_revision = src.get("user_revision")
    if user_revision is not None and (not isinstance(user_revision, int) or isinstance(user_revision, bool) or user_revision < 1):
        raise MigrationError("rev19 user_revision must be a positive integer when present")
    return _finalize_current_card(
        doc, current_template_doc,
        source_schema_version="2.3.0",
        source_template_revision=19,
        source_user_revision=user_revision,
        source_compatibility_profile="AIR_HANDOFF_SCHEMA_2_3_REV19_SUPPORTED_GENERATION",
        revision_semantics_source="REV19_SPLIT_REVISION_FIELDS_PRESERVED",
        migration_path="SCHEMA_2_3_REV19_TO_REV20",
        migration_decision="MIGRATED_SCHEMA_2_3_REV19_TO_REV20_PENDING_CURRENT_ALIGNMENT_MODE_REEVALUATION_AND_ARTIFACT_REBINDING",
    )


def migrate_to_current(doc: dict[str, Any], current_template_doc: dict[str, Any]) -> dict[str, Any]:
    src = require_one_root(doc)
    tmpl = current_template_card(current_template_doc)
    schema = src.get("schema_version")
    schema_caps = src.get("SCHEMA_VERSION")
    if schema != schema_caps:
        raise MigrationError("source SCHEMA_VERSION/schema_version mismatch")

    if schema == "2.2.0":
        return migrate_legacy_2_2_floor(doc, current_template_doc)
    if schema != "2.3.0":
        raise MigrationError(f"unsupported source schema_version {schema!r}")

    if src.get("template_revision") == 20:
        if "card_revision" in src:
            raise MigrationError("rev20 card must not contain legacy card_revision")
        out = copy.deepcopy(doc)
        card = out["AIR_HANDOFF_CARD"]
        if set(card) - (set(tmpl["schema_manifest"]["required_fields"]) | set(tmpl["schema_manifest"].get("optional_fields", []))):
            raise MigrationError("current rev20 card contains undeclared root fields")
        return out
    if src.get("template_revision") == 19:
        return migrate_schema_2_3_rev19(doc, current_template_doc)

    return migrate_schema_2_3_pre_rev19(doc, current_template_doc)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--template", default="prompts/AIR_HANDOFF_CARD_TEMPLATE.json")
    ap.add_argument("--output")
    args = ap.parse_args()
    inp = load_json(Path(args.input))
    tmpl = load_json(Path(args.template))
    out = migrate_to_current(inp, tmpl)
    txt = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        Path(args.output).write_text(txt, encoding="utf-8")
    else:
        print(txt, end="")


if __name__ == "__main__":
    try:
        main()
    except MigrationError as exc:
        raise SystemExit(f"AIR Handoff migration FAILED: {exc}")
