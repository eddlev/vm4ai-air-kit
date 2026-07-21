"""AIR project workspace constants and documents."""

from __future__ import annotations

from typing import Any

WORKSPACE_SCHEMA_VERSION = 1
REGISTRY_SCHEMA_VERSION = 1

REQUIRED_DIRECTORIES = (
    "state/sessions",
    "state/checkpoints",
    "state/decisions",
    "bundles/specifications",
    "bundles/compiled",
    "bundles/receipts",
    "bundles/validation",
    "handoffs/cards",
    "handoffs/envelopes",
    "handoffs/verification",
    "handoffs/acceptance",
    "trust/public-keys",
    "trust/anchors",
    "signatures/envelopes",
    "signatures/verification",
    "evidence/sources",
    "evidence/tests",
    "evidence/operator",
    "evidence/models",
    "evidence/release",
    "exports/prompt-sets",
    "exports/reports",
    "exports/release-candidates",
    "logs/operations",
    "logs/validation",
    "tmp",
)


def empty_registry() -> dict[str, Any]:
    return {"schema_version": REGISTRY_SCHEMA_VERSION, "projects": []}


def empty_trust_store() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "status": "UNCONFIGURED_STAGE_4_MIGRATION_PENDING",
        "keys": [],
        "claim_boundary": "This placeholder does not establish trust or authorize signing operations.",
    }
