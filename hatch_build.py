"""Hatch build hook for the verified installed AIR resource set."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vm4ai_air.resources.build import (  # noqa: E402
    BUNDLES_NAME,
    INDEX_NAME,
    MANIFEST_NAME,
    RECEIPT_NAME,
    write_generated_metadata,
)
from vm4ai_air.version import __version__  # noqa: E402

try:
    from hatchling.builders.hooks.plugin.interface import BuildHookInterface
except ImportError:  # Allows direct local validation without Hatchling installed.

    class BuildHookInterface:  # type: ignore[no-redef]
        PLUGIN_NAME = "custom"


class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict[str, object]) -> None:
        root = Path(self.root).resolve()
        staging = root / ".air-build" / self.target_name
        if staging.exists():
            shutil.rmtree(staging)
        generated = staging / "generated"
        write_generated_metadata(root, generated, __version__)

        if self.target_name != "wheel":
            return

        force_include = build_data.setdefault("force_include", {})
        if not isinstance(force_include, dict):
            raise RuntimeError("Hatch build_data.force_include must be a mapping")
        for source_root in ("prompts", "profiles", "runtime"):
            force_include[str(root / source_root)] = f"vm4ai_air/resources/air/{source_root}"
        for name in (MANIFEST_NAME, INDEX_NAME, BUNDLES_NAME, RECEIPT_NAME):
            force_include[str(generated / name)] = f"vm4ai_air/resources/air/{name}"

    def clean(self, versions: list[str]) -> None:
        staging = Path(self.root).resolve() / ".air-build"
        if staging.exists():
            shutil.rmtree(staging)
