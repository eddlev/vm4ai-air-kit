"""Small deterministic TOML writer for AIR-owned configuration shapes."""

from __future__ import annotations

import json
from typing import Any

from vm4ai_air.errors import ConfigurationError


def _scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(_scalar(item) for item in value) + "]"
    raise ConfigurationError(f"Unsupported TOML value type: {type(value).__name__}")


def dumps(value: dict[str, Any]) -> str:
    top_scalars: list[str] = []
    sections: list[str] = []
    for key, item in value.items():
        if isinstance(item, dict):
            section_lines = [f"[{key}]"]
            for child_key, child_value in item.items():
                if isinstance(child_value, dict):
                    raise ConfigurationError("Nested TOML tables deeper than one level are not supported")
                if child_value is None:
                    continue
                section_lines.append(f"{child_key} = {_scalar(child_value)}")
            sections.append("\n".join(section_lines))
        elif item is not None:
            top_scalars.append(f"{key} = {_scalar(item)}")
    blocks = []
    if top_scalars:
        blocks.append("\n".join(top_scalars))
    blocks.extend(sections)
    return "\n\n".join(blocks) + "\n"
