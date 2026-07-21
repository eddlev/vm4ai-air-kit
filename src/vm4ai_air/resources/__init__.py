"""Installed AIR canonical-resource access."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .resolver import ResourceResolver

__all__ = ["ResourceResolver"]


def __getattr__(name: str) -> Any:
    if name == "ResourceResolver":
        from .resolver import ResourceResolver

        return ResourceResolver
    raise AttributeError(name)
