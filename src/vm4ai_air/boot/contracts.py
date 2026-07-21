"""Reusable Stage 3 contracts for coding tools and future local adapters."""

from __future__ import annotations

import json
import uuid
from collections.abc import Mapping, Sequence
from importlib import resources as importlib_resources
from typing import Any

from vm4ai_air.errors import BootError
from vm4ai_air.io import utc_now

_CONTRACTS: dict[str, tuple[str, tuple[str, ...]]] = {
    "task": (
        "AIR_TASK_PACKET",
        (
            "schema_id",
            "schema_version",
            "task_id",
            "title",
            "objective",
            "source_context",
            "approved_scope",
            "excluded_scope",
            "acceptance_criteria",
            "active_step",
            "evidence_requirements",
            "claim_boundary",
        ),
    ),
    "authorization": (
        "AIR_AUTHORIZATION_ENVELOPE",
        (
            "schema_id",
            "schema_version",
            "authorization_id",
            "task_id",
            "issued_at_utc",
            "actor",
            "capabilities",
            "restrictions",
            "default_policy",
            "claim_boundary",
        ),
    ),
    "continuation": (
        "AIR_CONTINUATION_PACKET",
        (
            "schema_id",
            "schema_version",
            "continuation_id",
            "task_id",
            "created_at_utc",
            "completed_steps",
            "current_step",
            "next_recommended_step",
            "repository_state",
            "authorization_ref",
            "evidence",
            "blockers",
            "pending_approvals",
            "claim_boundary",
        ),
    ),
}


CONTRACT_SCHEMA_FILES = {
    "task": "air-task-packet.schema.json",
    "authorization": "air-authorization-envelope.schema.json",
    "continuation": "air-continuation-packet.schema.json",
}


def load_contract_schema(kind: str) -> dict[str, Any]:
    """Load a contract schema from the installed package without repository-relative paths."""

    filename = CONTRACT_SCHEMA_FILES.get(kind)
    if filename is None:
        raise BootError(f"Unknown AIR contract kind: {kind}")
    node = importlib_resources.files("vm4ai_air").joinpath("schemas", filename)
    try:
        value = json.loads(node.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise BootError(f"Cannot load installed AIR contract schema {filename}: {exc}") from exc
    if not isinstance(value, dict):
        raise BootError(f"Installed AIR contract schema must be an object: {filename}")
    return value

_CAPABILITY_KEYS = (
    "inspect",
    "modify_worktree",
    "run_tests",
    "commit",
    "push",
    "open_pr",
    "mark_ready",
    "merge",
    "tag",
    "release",
    "publish",
    "destructive_actions",
)


def _strings(values: Sequence[str] | None, field: str) -> list[str]:
    result: list[str] = []
    for value in values or ():
        if not isinstance(value, str) or not value.strip():
            raise BootError(f"{field} must contain only non-empty strings")
        result.append(value.strip())
    return result


def validate_contract(document: Mapping[str, Any], kind: str) -> dict[str, Any]:
    """Validate the stable structural floor without requiring a runtime JSON Schema dependency."""

    if kind not in _CONTRACTS:
        raise BootError(f"Unknown AIR contract kind: {kind}")
    schema_id, required = _CONTRACTS[kind]
    errors: list[str] = []
    allowed = set(required)
    unknown_fields = sorted(set(document) - allowed)
    if unknown_fields:
        errors.append(f"unknown fields: {', '.join(unknown_fields)}")
    if document.get("schema_id") != schema_id:
        errors.append(f"schema_id must be {schema_id}")
    if document.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    for field in required:
        if field not in document:
            errors.append(f"missing required field: {field}")

    common_nonempty = {
        "task": ("task_id", "title", "objective", "active_step", "claim_boundary"),
        "authorization": (
            "authorization_id",
            "task_id",
            "issued_at_utc",
            "actor",
            "claim_boundary",
        ),
        "continuation": (
            "continuation_id",
            "task_id",
            "created_at_utc",
            "current_step",
            "next_recommended_step",
            "claim_boundary",
        ),
    }
    for field in common_nonempty[kind]:
        value = document.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a non-empty string")

    list_fields = {
        "task": ("approved_scope", "excluded_scope", "acceptance_criteria", "evidence_requirements"),
        "authorization": ("restrictions",),
        "continuation": ("completed_steps", "blockers", "pending_approvals"),
    }
    for field in list_fields[kind]:
        value = document.get(field)
        if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
            errors.append(f"{field} must be an array of non-empty strings")
    if kind == "task":
        if not isinstance(document.get("source_context"), Mapping):
            errors.append("source_context must be an object")
        criteria = document.get("acceptance_criteria")
        if isinstance(criteria, list) and not criteria:
            errors.append("acceptance_criteria must contain at least one item")
    elif kind == "authorization":
        if document.get("default_policy") != "DENY_UNLESS_TRUE":
            errors.append("default_policy must be DENY_UNLESS_TRUE")
        capabilities = document.get("capabilities")
        if not isinstance(capabilities, Mapping):
            errors.append("capabilities must be an object")
        else:
            unknown = sorted(set(capabilities) - set(_CAPABILITY_KEYS))
            missing = sorted(set(_CAPABILITY_KEYS) - set(capabilities))
            if unknown:
                errors.append(f"unknown capabilities: {', '.join(unknown)}")
            if missing:
                errors.append(f"missing capabilities: {', '.join(missing)}")
            for key, value in capabilities.items():
                if not isinstance(value, bool):
                    errors.append(f"capability {key} must be boolean")
    else:
        if not isinstance(document.get("repository_state"), Mapping):
            errors.append("repository_state must be an object")
        evidence = document.get("evidence")
        if not isinstance(evidence, list) or any(not isinstance(item, Mapping) for item in evidence):
            errors.append("evidence must be an array of objects")
        authorization_ref = document.get("authorization_ref")
        if authorization_ref is not None and (
            not isinstance(authorization_ref, str) or not authorization_ref.strip()
        ):
            errors.append("authorization_ref must be null or a non-empty string")
    return {"decision": "PASS" if not errors else "FAIL", "kind": kind, "errors": errors}


def build_task_packet(
    *,
    title: str,
    objective: str,
    approved_scope: Sequence[str],
    excluded_scope: Sequence[str],
    acceptance_criteria: Sequence[str],
    active_step: str,
    evidence_requirements: Sequence[str] = (),
    source_context: Mapping[str, Any] | None = None,
    task_id: str | None = None,
) -> dict[str, Any]:
    document = {
        "schema_id": "AIR_TASK_PACKET",
        "schema_version": "1.0.0",
        "task_id": task_id or str(uuid.uuid4()),
        "title": title.strip(),
        "objective": objective.strip(),
        "source_context": dict(source_context or {}),
        "approved_scope": _strings(approved_scope, "approved_scope"),
        "excluded_scope": _strings(excluded_scope, "excluded_scope"),
        "acceptance_criteria": _strings(acceptance_criteria, "acceptance_criteria"),
        "active_step": active_step.strip(),
        "evidence_requirements": _strings(evidence_requirements, "evidence_requirements"),
        "claim_boundary": (
            "This packet records task scope and acceptance intent. It is not execution authorization, "
            "proof of completion, or permission to exceed the authorization envelope."
        ),
    }
    result = validate_contract(document, "task")
    if result["decision"] != "PASS":
        raise BootError("Cannot build AIR task packet", details={"errors": result["errors"]})
    return document


def build_authorization_envelope(
    *,
    task_id: str,
    capabilities: Mapping[str, bool] | None = None,
    restrictions: Sequence[str] = (),
    actor: str = "USER_APPROVED",
    authorization_id: str | None = None,
    issued_at_utc: str | None = None,
) -> dict[str, Any]:
    supplied = dict(capabilities or {})
    unknown_capabilities = sorted(set(supplied) - set(_CAPABILITY_KEYS))
    if unknown_capabilities:
        raise BootError(
            "Cannot build AIR authorization envelope with unknown capabilities",
            details={"unknown_capabilities": unknown_capabilities},
        )
    invalid_capabilities = sorted(key for key, value in supplied.items() if not isinstance(value, bool))
    if invalid_capabilities:
        raise BootError(
            "AIR authorization capabilities must be explicit boolean values",
            details={"invalid_capabilities": invalid_capabilities},
        )
    normalized = {key: supplied.get(key, False) for key in _CAPABILITY_KEYS}
    document = {
        "schema_id": "AIR_AUTHORIZATION_ENVELOPE",
        "schema_version": "1.0.0",
        "authorization_id": authorization_id or str(uuid.uuid4()),
        "task_id": task_id,
        "issued_at_utc": issued_at_utc or utc_now(),
        "actor": actor,
        "capabilities": normalized,
        "restrictions": _strings(restrictions, "restrictions"),
        "default_policy": "DENY_UNLESS_TRUE",
        "claim_boundary": (
            "Authorization is capability-specific and task-bound. Omitted or false capabilities remain denied. "
            "This envelope does not prove identity, safety, correctness, or successful execution."
        ),
    }
    result = validate_contract(document, "authorization")
    if result["decision"] != "PASS":
        raise BootError("Cannot build AIR authorization envelope", details={"errors": result["errors"]})
    return document


def build_continuation_packet(
    *,
    task_id: str,
    completed_steps: Sequence[str],
    current_step: str,
    next_recommended_step: str,
    evidence: Sequence[Mapping[str, Any]] = (),
    blockers: Sequence[str] = (),
    pending_approvals: Sequence[str] = (),
    repository_state: Mapping[str, Any] | None = None,
    authorization_ref: str | None = None,
    continuation_id: str | None = None,
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    document = {
        "schema_id": "AIR_CONTINUATION_PACKET",
        "schema_version": "1.0.0",
        "continuation_id": continuation_id or str(uuid.uuid4()),
        "task_id": task_id,
        "created_at_utc": created_at_utc or utc_now(),
        "completed_steps": _strings(completed_steps, "completed_steps"),
        "current_step": current_step.strip(),
        "next_recommended_step": next_recommended_step.strip(),
        "repository_state": dict(repository_state or {}),
        "authorization_ref": authorization_ref,
        "evidence": [dict(item) for item in evidence],
        "blockers": _strings(blockers, "blockers"),
        "pending_approvals": _strings(pending_approvals, "pending_approvals"),
        "claim_boundary": (
            "This packet preserves observed continuation state. The current step governs over the recommended next "
            "step, and no pending approval is granted by carrying the packet forward."
        ),
    }
    result = validate_contract(document, "continuation")
    if result["decision"] != "PASS":
        raise BootError("Cannot build AIR continuation packet", details={"errors": result["errors"]})
    return document
