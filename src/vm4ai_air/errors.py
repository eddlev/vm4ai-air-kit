"""AIR application exception hierarchy."""

from __future__ import annotations


class AirError(Exception):
    """Base class for expected AIR failures."""

    code = "AIR_ERROR"
    exit_code = 2

    def __init__(self, message: str, *, details: dict[str, object] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def as_dict(self) -> dict[str, object]:
        return {
            "decision": "ERROR",
            "error_code": self.code,
            "error": self.message,
            "details": self.details,
        }


class ConfigurationError(AirError):
    code = "AIR_CONFIGURATION_ERROR"


class ResourceError(AirError):
    code = "AIR_RESOURCE_ERROR"
    exit_code = 3


class ResourceIntegrityError(ResourceError):
    code = "AIR_RESOURCE_INTEGRITY_ERROR"


class BootError(AirError):
    code = "AIR_BOOT_ERROR"
    exit_code = 3


class WorkspaceError(AirError):
    code = "AIR_WORKSPACE_ERROR"


class LockError(AirError):
    code = "AIR_LOCK_ERROR"
    exit_code = 4


class EnvironmentError(AirError):
    code = "AIR_ENVIRONMENT_ERROR"
    exit_code = 4
