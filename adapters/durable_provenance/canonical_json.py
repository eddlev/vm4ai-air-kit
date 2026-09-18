"""Canonical JSON helpers for AIR durable provenance.

Canonical form: UTF-8, no BOM, lexicographically sorted object keys, array order
preserved, no insignificant whitespace, and no NaN/Infinity.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json_text(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def canonical_json_bytes(value: Any) -> bytes:
    return canonical_json_text(value).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))
