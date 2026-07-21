"""AIR package identity."""

from __future__ import annotations

PACKAGE_DISTRIBUTION = "vm4ai-air"
PACKAGE_IMPORT = "vm4ai_air"
CONSOLE_COMMAND = "air"
__version__ = "0.5.0.dev0"


def base_version_payload() -> dict[str, str]:
    return {
        "distribution": PACKAGE_DISTRIBUTION,
        "import_package": PACKAGE_IMPORT,
        "command": CONSOLE_COMMAND,
        "package_version": __version__,
    }
