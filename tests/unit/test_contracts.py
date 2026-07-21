from __future__ import annotations

import json
from pathlib import Path

from jsonschema import validate

from vm4ai_air.boot import (
    build_authorization_envelope,
    build_continuation_packet,
    build_task_packet,
    load_contract_schema,
    validate_contract,
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "src" / "vm4ai_air" / "schemas"


def schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def test_stage3_contract_builders_match_json_schemas() -> None:
    task = build_task_packet(
        title="Stage 3",
        objective="Compile deterministic boot bundles",
        approved_scope=["boot"],
        excluded_scope=["publication"],
        acceptance_criteria=["tests pass"],
        active_step="implementation",
        evidence_requirements=["CI"],
    )
    authorization = build_authorization_envelope(
        task_id=task["task_id"],
        capabilities={"inspect": True, "modify_worktree": True, "run_tests": True},
        restrictions=["no push", "no merge", "no publication"],
        actor="USER",
        approval_ref="conversation:stage3-contract-test",
    )
    continuation = build_continuation_packet(
        task_id=task["task_id"],
        completed_steps=["architecture"],
        current_step="implementation",
        next_recommended_step="review",
        pending_approvals=["push"],
        authorization_ref=authorization["authorization_id"],
    )

    assert validate_contract(task, "task")["decision"] == "PASS"
    assert validate_contract(authorization, "authorization")["decision"] == "PASS"
    assert validate_contract(continuation, "continuation")["decision"] == "PASS"
    assert authorization["capabilities"]["merge"] is False
    assert authorization["capabilities"]["publish"] is False

    assert load_contract_schema("task")["$id"] == "urn:air:task-packet:1"

    validate(task, schema("air-task-packet.schema.json"))
    validate(authorization, schema("air-authorization-envelope.schema.json"))
    validate(continuation, schema("air-continuation-packet.schema.json"))


def test_authorization_builder_rejects_truthy_non_boolean_capabilities() -> None:
    import pytest

    from vm4ai_air.errors import BootError

    with pytest.raises(BootError, match="explicit boolean"):
        build_authorization_envelope(task_id="task", capabilities={"merge": "false"})  # type: ignore[dict-item]


def test_authorization_builder_rejects_unknown_capabilities() -> None:
    import pytest

    from vm4ai_air.errors import BootError

    with pytest.raises(BootError, match="unknown capabilities"):
        build_authorization_envelope(task_id="task", capabilities={"superuser": True})  # type: ignore[dict-item]


def test_task_builder_rejects_empty_acceptance_criteria() -> None:
    import pytest

    from vm4ai_air.errors import BootError

    with pytest.raises(BootError, match="Cannot build AIR task packet"):
        build_task_packet(
            title="Task",
            objective="Objective",
            approved_scope=[],
            excluded_scope=[],
            acceptance_criteria=[],
            active_step="design",
        )


def test_mutating_authorization_requires_explicit_approval_provenance() -> None:
    import pytest

    from vm4ai_air.errors import BootError

    with pytest.raises(BootError, match="explicit actor"):
        build_authorization_envelope(task_id="task", capabilities={"merge": True})

    with pytest.raises(BootError, match="approval_ref"):
        build_authorization_envelope(task_id="task", capabilities={"merge": True}, actor="USER")


def test_nonmutating_authorization_uses_neutral_unapproved_default() -> None:
    authorization = build_authorization_envelope(task_id="task", capabilities={"inspect": True})
    assert authorization["actor"] == "UNSPECIFIED"
    assert authorization["approval_ref"] is None
    assert authorization["capabilities"]["merge"] is False
    assert validate_contract(authorization, "authorization")["decision"] == "PASS"


def test_forged_mutating_authorization_fails_validation() -> None:
    authorization = build_authorization_envelope(task_id="task", capabilities={"inspect": True})
    authorization["actor"] = "USER_APPROVED"
    authorization["capabilities"]["merge"] = True
    result = validate_contract(authorization, "authorization")
    assert result["decision"] == "FAIL"
    assert any("approval_ref" in error for error in result["errors"])
