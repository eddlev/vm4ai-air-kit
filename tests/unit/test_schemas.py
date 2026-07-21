from __future__ import annotations

import json
from pathlib import Path

from jsonschema.validators import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def test_package_owned_json_schemas_are_valid() -> None:
    schemas = sorted((ROOT / "src" / "vm4ai_air" / "schemas").glob("*.schema.json"))
    assert schemas
    for path in schemas:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
