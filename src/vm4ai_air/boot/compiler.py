"""Installed-resource-backed AIR modular boot service."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from contextlib import ExitStack
from pathlib import Path
from typing import Any

from vm4ai_air.errors import BootError
from vm4ai_air.io import FileLock, atomic_write_bytes, atomic_write_json, utc_now
from vm4ai_air.paths import AppPaths
from vm4ai_air.resources import ResourceResolver
from vm4ai_air.resources.build import strict_json_loads
from vm4ai_air.version import __version__

BOOT_MANIFEST_PATH = "runtime/boot/AIR BOOT MODULE MANIFEST.json"
BOOT_STARTER_PATH = "runtime/boot/AIR BOOT STARTER PROFILE.json"
SEMANTIC_CLOSURE_PATH = "runtime/boot/AIR BOOT SEMANTIC CLOSURE.json"
Q1D_MODULE_ID = "AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1"
COMPLETE_PROMPT_SET = (
    "prompts/AIR CORE RUNTIME.md",
    "prompts/AIR CONTROL SURFACE.md",
    "prompts/AIR DEFAULT STARTER PROFILE.json",
)
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_SAFE_TRIGGER = re.compile(r"^[A-Z][A-Z0-9_]*$")
_KERNEL_SENTINEL = "AIR_LOAD_SENTINEL :: AIR_BOOT_KERNEL :: END_OF_FILE :: LOAD_INTEGRITY_V1"
_EXPECTED_BOOT_MODES = ("FULL_MONOLITH", "MANUAL_MODULAR", "LOCAL_BUNDLED", "HOST_ADAPTER")
_EXPECTED_LOAD_CLASSES = (
    "KERNEL_MANDATORY",
    "SESSION_ENTRY",
    "MANDATORY_WHEN_MATERIAL_EXECUTION",
    "TASK_TRIGGERED",
    "EVIDENCE_TRIGGERED",
    "TOOL_OPTIONAL",
    "DATA_OPTIONAL",
    "MONOLITH_FALLBACK",
)
_EXPECTED_FALLBACK_ORDER = (
    "REQUEST_MISSING_LOCAL_MODULE",
    "USE_VALIDATED_LOCAL_BUNDLE",
    "FULL_MONOLITH",
    "EVIDENCE_REQUIRED",
)
_EXPECTED_MANDATORY_FLOOR = {
    "LOAD_INTEGRITY",
    "ACTIVE_CONTRACT",
    "AIR_GATE",
    "EVIDENCE_FAIL_CLOSED",
    "SOURCE_DATA_NOT_INSTRUCTION",
    "APPROVAL_AND_RESCOPE",
    "AUTHENTICATION_NOT_AUTHORIZATION",
    "DEPENDENCY_SOVEREIGNTY",
    "MODULE_GRAPH_SAFETY",
    "VISIBLE_FALLBACK",
    "ALL_CREATED_FORMAL_OBJECTS_VISIBLE",
}
_EXPECTED_SESSION_ENTRY_GUARDS = {
    "q1_selector_state": "LOCKED_UNTIL_EXPLICIT_SELECTOR",
    "accepted_q1_inputs": ["A", "B", "C", "D", "Q1=A", "Q1=B", "Q1=C", "Q1=D"],
    "reserved_non_selection_inputs": ["Start a new AIR project.", "Import this project into AIR."],
    "nonselector_action": "RENDER_Q1_AND_WAIT",
    "context_scope": "CURRENT_VISIBLE_MESSAGES_AND_EXPLICIT_CURRENT_ATTACHMENTS_ONLY",
    "unenumerated_context": "UNTRUSTED_FOR_PROJECT_STATE",
    "verification_claim_ceiling_without_current_session_evidence": "PROMPT_DECLARED_OR_UNVERIFIED",
}
_KERNEL_REQUIRED_MARKERS = (
    "Activate AIR Boot Kernel for this session.",
    "SYSTEM_DESIGNATION: AIR_BOOT_KERNEL_V1",
    "ARTIFACT_CLASS: BOOT_RUNTIME",
    "VERSION: 1.1.0",
    "PATCH_MARKER: AIR_Q1_EXPLICIT_SELECTION_LOCK_V1",
    "PATCH_MARKER: AIR_CURRENT_SESSION_CONTEXT_BOUNDARY_V1",
    "PATCH_MARKER: AIR_VERIFICATION_PROVENANCE_CEILING_V1",
    "MANDATORY KERNEL FLOOR",
    "Q1 EXPLICIT SELECTION LOCK",
    'The exact phrases "Start a new AIR project." and "Import this project into AIR."',
    "CURRENT-SESSION CONTEXT BOUNDARY",
    "Account memory, project memory, prior chats, prior uploads",
    "VERIFICATION PROVENANCE CEILING",
    "Without that evidence, verification_level must remain PROMPT_DECLARED or UNVERIFIED.",
    "BOOT SEQUENCE",
    "MODULE FAILURE AND FALLBACK",
    "CLAIM BOUNDARY",
)
_Q1D_REQUIRED_HEADINGS = (
    "1. No prior AIR knowledge required",
    "2. What AIR is",
    "3. Cooperative work",
    "4. What AIR is not",
    "5. You can talk normally",
    "6. The six questions",
    "7. Files and source-light work",
    "8. Handoff",
    "9. Essential help commands",
    "10. Optional example-project invitation",
    "11. Return to Q1",
)
_EXPECTED_SEMANTIC_REQUIREMENTS = {
    "SESSION_ENTRY": {
        "AIR_RUNTIME_ENTRY_AND_ACTIVATION_V1",
        "AIR_CONTROL_ENTRY_VISIBILITY_AND_ONBOARDING_V1",
        "AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1",
        "AIR_RUNTIME_POLICY_AND_HANDOFF_SECURITY_V1",
        "AIR_CONTROL_POLICY_HANDOFF_AND_PORTABILITY_V1",
    },
    "NEW_PROJECT": {
        "AIR_RUNTIME_ENTRY_AND_ACTIVATION_V1",
        "AIR_CONTROL_ENTRY_VISIBILITY_AND_ONBOARDING_V1",
        "AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1",
    },
    "Q1_D_ORIENTATION": {
        "AIR_RUNTIME_ENTRY_AND_ACTIVATION_V1",
        "AIR_CONTROL_ENTRY_VISIBILITY_AND_ONBOARDING_V1",
        "AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1",
    },
    "MATERIAL_EXECUTION": {"AIR_RUNTIME_CONTRACT_GATE_AND_EXECUTION_V1"},
    "MUTATION": {"AIR_RUNTIME_CONTRACT_GATE_AND_EXECUTION_V1"},
    "CODING": {
        "AIR_RUNTIME_CONTRACT_GATE_AND_EXECUTION_V1",
        "AIR_RUNTIME_CODING_REPOSITORY_AND_RELEASE_V1",
        "AIR_CONTROL_CODING_REPOSITORY_AND_RELEASE_V1",
    },
    "REPOSITORY": {
        "AIR_RUNTIME_CONTRACT_GATE_AND_EXECUTION_V1",
        "AIR_RUNTIME_CODING_REPOSITORY_AND_RELEASE_V1",
        "AIR_CONTROL_CODING_REPOSITORY_AND_RELEASE_V1",
    },
    "HANDOFF_CONTINUATION": {
        "AIR_RUNTIME_ENTRY_AND_ACTIVATION_V1",
        "AIR_CONTROL_ENTRY_VISIBILITY_AND_ONBOARDING_V1",
        "AIR_RUNTIME_POLICY_AND_HANDOFF_SECURITY_V1",
        "AIR_CONTROL_POLICY_HANDOFF_AND_PORTABILITY_V1",
    },
    "IMPORT_NON_AIR_PROJECT": {
        "AIR_RUNTIME_ENTRY_AND_ACTIVATION_V1",
        "AIR_CONTROL_ENTRY_VISIBILITY_AND_ONBOARDING_V1",
        "AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1",
    },
}
_EXPECTED_SESSION_BRANCHES = {
    "Q1_A_NEW_PROJECT": "CLOSED_BY_ENTRY_MODULES",
    "Q1_B_IMPORT_NON_AIR_PROJECT": "CLOSED_BY_ENTRY_MODULES",
    "Q1_C_HANDOFF_CONTINUATION": "CLOSED_BY_POLICY_AND_HANDOFF_MODULES",
    "Q1_D_BEGINNER_ORIENTATION": "CLOSED_BY_AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1",
}
_DECOMPOSITION_MAP_PATH = "runtime/boot/evidence/AIR WS7 MODULE DECOMPOSITION MAP.json"
_DECOMPOSITION_MAP_SHA256 = "cb651920a4e9f7bc02b106022903b5ed0400336dcbadb3e99e51dc6b21c7a601"
_DERIVED_MODULE_CONTRACTS: dict[str, tuple[str, str, int, int]] = {
    "AIR_RUNTIME_ENTRY_AND_ACTIVATION_V1": (
        "fcf6df4f91cbe1397abe143d4f51d1a4e8c63e7c655d2058b030c9cd934cadf7",
        "prompts/AIR CORE RUNTIME.md",
        17,
        35539,
    ),
    "AIR_RUNTIME_CONTRACT_GATE_AND_EXECUTION_V1": (
        "519e25406a22a81f84dcad86325a35b5634d9bce25d85cfb32211868faef223f",
        "prompts/AIR CORE RUNTIME.md",
        44,
        89554,
    ),
    "AIR_RUNTIME_ARTIFACT_LIFECYCLE_V1": (
        "31b6a8b7d0515be3597917bd56fa332a8ba6404bf4ff1f6a15c1e7b59cfb251f",
        "prompts/AIR CORE RUNTIME.md",
        11,
        20770,
    ),
    "AIR_RUNTIME_SOURCE_TRANSLATION_AND_CAPABILITY_V1": (
        "50a88eff3028b7351eeaff83523074d4497534ddedff9d2569410d840f2afe81",
        "prompts/AIR CORE RUNTIME.md",
        12,
        35197,
    ),
    "AIR_RUNTIME_METHOD_EXECUTOR_AND_SPECIALIST_V1": (
        "898203cdde6bf1731d2eb74f7c3e943c0b8b51889baafea1a0595b5eac3c5baf",
        "prompts/AIR CORE RUNTIME.md",
        8,
        30112,
    ),
    "AIR_RUNTIME_POLICY_AND_HANDOFF_SECURITY_V1": (
        "844ebe96a0033e1ccc4723ebd28c8908106fbbf948ca515ca7e74cc0c1ca8e32",
        "prompts/AIR CORE RUNTIME.md",
        4,
        11481,
    ),
    "AIR_RUNTIME_GROUNDING_DISCOVERY_AND_RESEARCH_V1": (
        "ec3b4ac2ddfd403bc1dd0b829066fc6b387065fc1ad7eb2123bef4e33cabe224",
        "prompts/AIR CORE RUNTIME.md",
        33,
        60461,
    ),
    "AIR_RUNTIME_CODING_REPOSITORY_AND_RELEASE_V1": (
        "b1a8e55944fe931082846170077df37d6f16f731e8d5bee137d2434cdff2a24b",
        "prompts/AIR CORE RUNTIME.md",
        12,
        13563,
    ),
    "AIR_CONTROL_ENTRY_VISIBILITY_AND_ONBOARDING_V1": (
        "fc8a1fdaa2f087bb97be1d52c87a1a0f8e4f370488381f0354d600ae908586bc",
        "prompts/AIR CONTROL SURFACE.md",
        47,
        51616,
    ),
    "AIR_CONTROL_ARTIFACT_SOURCE_AND_CAPABILITY_V1": (
        "54d2476c34d2cd624c660efeb75400d42c0aeadba48cbf2982a4a84e0d72b4f6",
        "prompts/AIR CONTROL SURFACE.md",
        35,
        40394,
    ),
    "AIR_CONTROL_POLICY_HANDOFF_AND_PORTABILITY_V1": (
        "d49af40d151faa0ff00ea14dc0d396b86ac9d8b62868064137ab621cc0ca3eaa",
        "prompts/AIR CONTROL SURFACE.md",
        7,
        16024,
    ),
    "AIR_CONTROL_CODING_REPOSITORY_AND_RELEASE_V1": (
        "9da914baf10ac6e71cf892d7bf072aea44aae9a7d39dca883d16332033102c13",
        "prompts/AIR CONTROL SURFACE.md",
        16,
        17761,
    ),
}
_SOURCE_CHUNK_MARKER = re.compile(rb"<!-- AIR_SOURCE_CHUNK_BEGIN (?P<meta>\{[^\n]+\}) -->")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _as_string_list(value: object, field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise BootError(f"AIR boot field {field} must be an array of non-empty strings")
    return list(value)


def _missing_keys(value: object, required: Sequence[str]) -> list[str]:
    if not isinstance(value, Mapping):
        return list(required)
    return [key for key in required if key not in value]


class BootCompiler:
    """Validate, plan, and compile AIR boot bundles from the shared resource resolver."""

    def __init__(self, resolver: ResourceResolver, *, paths: AppPaths | None = None) -> None:
        self.resolver = resolver
        self.paths = paths or resolver.paths
        self.manifest = self._load_json(BOOT_MANIFEST_PATH)
        self.starter = self._load_json(BOOT_STARTER_PATH)
        self.semantic_closure = self._load_json(SEMANTIC_CLOSURE_PATH)
        self._modules = self._module_index()
        self._manifest_order = {module_id: index for index, module_id in enumerate(self._modules)}

    @classmethod
    def from_environment(
        cls,
        *,
        environment: Mapping[str, str] | None = None,
        paths: AppPaths | None = None,
    ) -> BootCompiler:
        resolved_paths = paths or AppPaths.resolve(environment)
        resolver = ResourceResolver.from_environment(environment=environment, paths=resolved_paths)
        return cls(resolver, paths=resolved_paths)

    def _load_json(self, resource: str) -> dict[str, Any]:
        value = strict_json_loads(self.resolver.read_text(resource), source=resource)
        if not isinstance(value, dict):
            raise BootError(f"AIR boot JSON resource must contain an object: {resource}")
        return value

    def _module_index(self) -> dict[str, dict[str, Any]]:
        modules = self.manifest.get("modules")
        if not isinstance(modules, list) or not modules:
            raise BootError("AIR boot manifest has no modules")
        result: dict[str, dict[str, Any]] = {}
        for raw in modules:
            if not isinstance(raw, Mapping):
                raise BootError("AIR boot module entries must be objects")
            module = dict(raw)
            module_id = module.get("module_id")
            if not isinstance(module_id, str) or not module_id:
                raise BootError("AIR boot module has no module_id")
            if module_id in result:
                raise BootError(f"Duplicate AIR boot module_id: {module_id}")
            result[module_id] = module
        return result

    def _check(self, checks: list[dict[str, Any]], name: str, passed: bool, detail: str, **extra: Any) -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail, **extra})

    def _verify_declared_resource(
        self,
        checks: list[dict[str, Any]],
        *,
        label: str,
        entry: object,
        path_field: str,
        require_sentinel: bool = False,
        required_markers: Sequence[str] = (),
    ) -> None:
        if not isinstance(entry, Mapping):
            self._check(checks, label, False, "entry must be an object")
            return
        path = entry.get(path_field)
        digest = entry.get("sha256")
        size = entry.get("size_bytes")
        if not isinstance(path, str) or not path:
            self._check(checks, label, False, f"missing {path_field}")
            return
        try:
            data = self.resolver.read_bytes(path)
        except Exception as exc:
            self._check(checks, label, False, f"cannot read {path}: {exc}")
            return
        observed_digest = _sha256(data)
        observed_size = len(data)
        digest_valid = isinstance(digest, str) and _SHA256.fullmatch(digest) is not None
        size_valid = isinstance(size, int) and not isinstance(size, bool) and size >= 0
        passed = digest_valid and size_valid and digest == observed_digest and size == observed_size
        self._check(
            checks,
            label,
            passed,
            path,
            expected_sha256=digest,
            observed_sha256=observed_digest,
            expected_size_bytes=size,
            observed_size_bytes=observed_size,
        )

        sentinel = entry.get("terminal_sentinel")
        sentinel_required_and_missing = require_sentinel and (not isinstance(sentinel, str) or not sentinel.strip())
        if sentinel_required_and_missing:
            self._check(checks, f"{label}_SENTINEL", False, f"required terminal_sentinel missing: {path}")
        if sentinel is not None or required_markers:
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                self._check(checks, f"{label}_TEXT_CONTRACT", False, f"not UTF-8: {path}")
                return
            if sentinel is not None and not sentinel_required_and_missing:
                self._check(
                    checks,
                    f"{label}_SENTINEL",
                    isinstance(sentinel, str) and text.rstrip().endswith(sentinel),
                    path,
                )
            if required_markers:
                missing = [marker for marker in required_markers if marker not in text]
                self._check(
                    checks,
                    f"{label}_TEXT_CONTRACT",
                    not missing,
                    "complete" if not missing else f"missing: {', '.join(missing)}",
                )

    def _dependency_cycle(self) -> list[str] | None:
        visiting: list[str] = []
        done: set[str] = set()

        def visit(module_id: str) -> list[str] | None:
            if module_id in done:
                return None
            if module_id in visiting:
                start = visiting.index(module_id)
                return visiting[start:] + [module_id]
            visiting.append(module_id)
            dependencies = self._modules[module_id].get("dependencies", [])
            if not isinstance(dependencies, list):
                return [module_id, "INVALID_DEPENDENCIES"]
            for dependency in dependencies:
                if dependency in self._modules:
                    cycle = visit(str(dependency))
                    if cycle:
                        return cycle
            visiting.pop()
            done.add(module_id)
            return None

        for module_id in self._modules:
            cycle = visit(module_id)
            if cycle:
                return cycle
        return None

    def _validate_manifest_contract(self, checks: list[dict[str, Any]]) -> None:
        required = (
            "SYSTEM_DESIGNATION",
            "artifact_class",
            "version",
            "status",
            "kernel",
            "boot_starter",
            "canonical_monolith",
            "boot_modes",
            "load_order_classes",
            "security_policy",
            "modules",
            "fallback_order",
            "unknown_trigger_behavior",
            "partial_load_claim",
            "semantic_closure",
            "compile_receipt_schema",
            "compile_receipt_template",
            "claim_boundary",
        )
        missing = _missing_keys(self.manifest, required)
        self._check(checks, "MANIFEST_STRUCTURE", not missing, "complete" if not missing else f"missing: {missing}")
        self._check(
            checks,
            "MANIFEST_IDENTITY",
            self.manifest.get("SYSTEM_DESIGNATION") == "AIR_BOOT_MODULE_MANIFEST_V1"
            and self.manifest.get("artifact_class") == "MODULE_MANIFEST"
            and self.manifest.get("version") == "2.0.0"
            and self.manifest.get("status") == "STAGE_3_DETERMINISTIC_MODULAR_BOOT",
            f"{self.manifest.get('SYSTEM_DESIGNATION')} {self.manifest.get('version')}",
        )
        boot_modes = self.manifest.get("boot_modes")
        self._check(
            checks,
            "MANIFEST_BOOT_MODES",
            isinstance(boot_modes, Mapping) and tuple(boot_modes) == _EXPECTED_BOOT_MODES,
            str(list(boot_modes) if isinstance(boot_modes, Mapping) else boot_modes),
        )
        load_classes = self.manifest.get("load_order_classes")
        self._check(
            checks,
            "MANIFEST_LOAD_CLASSES",
            isinstance(load_classes, list) and tuple(load_classes) == _EXPECTED_LOAD_CLASSES,
            str(load_classes),
        )
        self._check(
            checks,
            "MANIFEST_FALLBACK_POLICY",
            tuple(self.manifest.get("fallback_order", [])) == _EXPECTED_FALLBACK_ORDER
            and self.manifest.get("unknown_trigger_behavior") == "REVIEW_AND_FULL_MONOLITH_FALLBACK"
            and self.manifest.get("partial_load_claim") == "MAY_NOT_CLAIM_FULL_AIR_WITHOUT_SEMANTIC_CLOSURE",
            str(self.manifest.get("unknown_trigger_behavior")),
        )
        policy = self.manifest.get("security_policy")
        expected_policy = {
            "local_relative_paths_only": True,
            "remote_urls_allowed": False,
            "absolute_paths_allowed": False,
            "parent_traversal_allowed": False,
            "symlink_escape_allowed": False,
            "embedded_commands_allowed": False,
            "duplicate_ids_allowed": False,
            "dependency_cycles_allowed": False,
            "module_self_approval_allowed": False,
            "module_can_relax_kernel_floor": False,
            "authenticated_content_bypasses_injection_checks": False,
            "module_load_is_execution_authorization": False,
        }
        self._check(
            checks,
            "MANIFEST_SECURITY_POLICY",
            isinstance(policy, Mapping) and all(policy.get(key) is value for key, value in expected_policy.items()),
            "fail-closed" if isinstance(policy, Mapping) else "missing",
        )
        canonical = self.manifest.get("canonical_monolith")
        canonical_paths = [entry.get("file") for entry in canonical] if isinstance(canonical, list) else []
        canonical_shape = (
            isinstance(canonical, list)
            and len(canonical) == len(COMPLETE_PROMPT_SET)
            and tuple(canonical_paths) == COMPLETE_PROMPT_SET
            and all(isinstance(entry, Mapping) for entry in canonical)
        )
        self._check(checks, "CANONICAL_PROMPT_SET_DECLARATION", canonical_shape, str(canonical_paths))

    def _validate_starter_contract(self, checks: list[dict[str, Any]]) -> None:
        required = (
            "SYSTEM_DESIGNATION",
            "PROFILE_KIND",
            "version",
            "status",
            "boot_modes",
            "default_boot_mode",
            "canonical_recovery_mode",
            "kernel",
            "manifest",
            "mandatory_floor",
            "session_entry",
            "dependency_policy",
            "security",
            "fallback_order",
            "claim_boundary",
            "object_visibility",
            "repository_layout",
            "semantic_closure",
        )
        missing = _missing_keys(self.starter, required)
        self._check(checks, "STARTER_STRUCTURE", not missing, "complete" if not missing else f"missing: {missing}")
        self._check(
            checks,
            "STARTER_IDENTITY",
            self.starter.get("SYSTEM_DESIGNATION") == "AIR_BOOT_STARTER_PROFILE_V1"
            and self.starter.get("PROFILE_KIND") == "BOOT_PROFILE"
            and self.starter.get("version") == "2.0.0"
            and self.starter.get("status") == "STAGE_3_DETERMINISTIC_MODULAR_BOOT",
            f"{self.starter.get('SYSTEM_DESIGNATION')} {self.starter.get('version')}",
        )
        self._check(
            checks,
            "STARTER_BOOT_POLICY",
            tuple(self.starter.get("boot_modes", [])) == _EXPECTED_BOOT_MODES
            and self.starter.get("default_boot_mode") == "LOCAL_BUNDLED"
            and self.starter.get("canonical_recovery_mode") == "FULL_MONOLITH"
            and tuple(self.starter.get("fallback_order", [])) == _EXPECTED_FALLBACK_ORDER,
            str(self.starter.get("default_boot_mode")),
        )
        mandatory = self.starter.get("mandatory_floor")
        self._check(
            checks,
            "STARTER_MANDATORY_FLOOR",
            isinstance(mandatory, list) and _EXPECTED_MANDATORY_FLOOR.issubset(set(mandatory)),
            str(mandatory),
        )
        session_entry = self.starter.get("session_entry")
        self._check(
            checks,
            "STARTER_SESSION_ENTRY",
            isinstance(session_entry, Mapping)
            and session_entry.get("required_load_classes") == ["KERNEL_MANDATORY", "SESSION_ENTRY"]
            and session_entry.get("unknown_trigger") == "REVIEW_OR_FALLBACK_MONOLITH"
            and session_entry.get("partial_load_claim") == "PROHIBITED",
            str(session_entry),
        )
        session_entry_guards = self.starter.get("session_entry_guards")
        self._check(
            checks,
            "STARTER_SESSION_ENTRY_GUARDS",
            isinstance(session_entry_guards, Mapping)
            and dict(session_entry_guards) == _EXPECTED_SESSION_ENTRY_GUARDS,
            str(session_entry_guards),
        )
        dependency = self.starter.get("dependency_policy")
        security = self.starter.get("security")
        self._check(
            checks,
            "STARTER_LOCAL_DEPENDENCY_POLICY",
            isinstance(dependency, Mapping)
            and dependency.get("network_required") is False
            and dependency.get("package_manager_required") is False
            and dependency.get("plugin_or_skill_required") is False,
            str(dependency),
        )
        self._check(
            checks,
            "STARTER_SECURITY_POLICY",
            isinstance(security, Mapping)
            and all(
                security.get(key) is False
                for key in (
                    "remote_module_urls_allowed",
                    "absolute_paths_allowed",
                    "parent_traversal_allowed",
                    "symlink_escape_allowed",
                    "manifest_commands_allowed",
                    "module_self_approval_allowed",
                    "authenticated_content_bypasses_injection_checks",
                    "module_load_is_execution_authorization",
                )
            ),
            "fail-closed" if isinstance(security, Mapping) else "missing",
        )
        kernel = self.starter.get("kernel")
        manifest_ref = self.starter.get("manifest")
        semantic_ref = self.starter.get("semantic_closure")
        manifest_kernel = self.manifest.get("kernel")
        self._check(
            checks,
            "STARTER_KERNEL_BINDING",
            isinstance(kernel, Mapping)
            and isinstance(manifest_kernel, Mapping)
            and kernel.get("file") == manifest_kernel.get("relative_path") == "runtime/boot/AIR BOOT KERNEL.md"
            and kernel.get("designation") == manifest_kernel.get("module_id") == "AIR_BOOT_KERNEL_V1"
            and kernel.get("version") == manifest_kernel.get("version") == "1.1.0"
            and kernel.get("sha256") == manifest_kernel.get("sha256")
            and kernel.get("size_bytes") == manifest_kernel.get("size_bytes"),
            str(kernel),
        )
        self._check(
            checks,
            "STARTER_MANIFEST_BINDING",
            isinstance(manifest_ref, Mapping)
            and manifest_ref.get("file") == BOOT_MANIFEST_PATH
            and manifest_ref.get("designation") == "AIR_BOOT_MODULE_MANIFEST_V1"
            and manifest_ref.get("version") == "2.0.0",
            str(manifest_ref),
        )
        self._check(
            checks,
            "STARTER_SEMANTIC_BINDING",
            isinstance(semantic_ref, Mapping)
            and semantic_ref.get("file") == SEMANTIC_CLOSURE_PATH
            and semantic_ref.get("designation") == "AIR_BOOT_SEMANTIC_CLOSURE"
            and semantic_ref.get("version") == "1.0.0",
            str(semantic_ref),
        )

    def _validate_semantic_contract(self, checks: list[dict[str, Any]]) -> None:
        required = (
            "schema_id",
            "schema_version",
            "status",
            "complete_prompt_set",
            "required_modules",
            "q1d",
            "unknown_trigger_behavior",
            "fallback_bundle_id",
            "adapter_contract",
            "claim_boundary",
            "session_entry_reachable_branches",
        )
        missing = _missing_keys(self.semantic_closure, required)
        self._check(
            checks,
            "SEMANTIC_CLOSURE_STRUCTURE",
            not missing,
            "complete" if not missing else f"missing: {missing}",
        )
        self._check(
            checks,
            "SEMANTIC_CLOSURE_IDENTITY",
            self.semantic_closure.get("schema_id") == "AIR_BOOT_SEMANTIC_CLOSURE"
            and self.semantic_closure.get("schema_version") == "1.0.0"
            and self.semantic_closure.get("status") == "STAGE_3_ACTIVE",
            f"{self.semantic_closure.get('schema_id')} {self.semantic_closure.get('schema_version')}",
        )
        declared_complete = self.semantic_closure.get("complete_prompt_set")
        self._check(
            checks,
            "COMPLETE_PROMPT_SET_INTEGRATION",
            isinstance(declared_complete, list) and tuple(declared_complete) == COMPLETE_PROMPT_SET,
            str(declared_complete),
        )
        self._check(
            checks,
            "UNKNOWN_TRIGGER_CONTRACT",
            self.semantic_closure.get("unknown_trigger_behavior") == "REVIEW_AND_FULL_MONOLITH_FALLBACK"
            and self.semantic_closure.get("fallback_bundle_id") == "COMPLETE_AIR_PROMPT_SET",
            str(self.semantic_closure.get("unknown_trigger_behavior")),
        )
        q1d = self.semantic_closure.get("q1d")
        self._check(
            checks,
            "Q1D_SEMANTIC_CONTRACT",
            isinstance(q1d, Mapping)
            and q1d.get("module_id") == Q1D_MODULE_ID
            and q1d.get("required_section_count") == 11
            and q1d.get("instructional_only") is True
            and q1d.get("project_activation_allowed") is False
            and q1d.get("example_invitation_required") is True
            and q1d.get("example_execution_optional") is True
            and q1d.get("reachable_from_new_project_bundle") is True,
            str(q1d),
        )
        adapter = self.semantic_closure.get("adapter_contract")
        self._check(
            checks,
            "ADAPTER_BOUNDARY_CONTRACT",
            isinstance(adapter, Mapping)
            and adapter.get("shared_service") == "vm4ai_air.boot.BootCompiler"
            and adapter.get("cli") == "air boot"
            and adapter.get("network_required") is False,
            str(adapter),
        )
        branches = self.semantic_closure.get("session_entry_reachable_branches")
        self._check(checks, "SESSION_ENTRY_BRANCH_CONTRACT", branches == _EXPECTED_SESSION_BRANCHES, str(branches))

        declared = self.semantic_closure.get("required_modules")
        closure_valid = isinstance(declared, Mapping)
        missing_requirements: list[str] = []
        if closure_valid:
            for trigger, required_modules in declared.items():
                if not isinstance(trigger, str) or not _SAFE_TRIGGER.fullmatch(trigger):
                    closure_valid = False
                    break
                if not isinstance(required_modules, list) or any(
                    not isinstance(module, str) or module not in self._modules for module in required_modules
                ):
                    closure_valid = False
                    break
            for trigger, expected in _EXPECTED_SEMANTIC_REQUIREMENTS.items():
                observed = declared.get(trigger)
                if not isinstance(observed, list) or set(observed) != expected:
                    missing_requirements.append(trigger)
        self._check(
            checks,
            "SEMANTIC_TRIGGER_CLOSURE",
            closure_valid and not missing_requirements,
            "complete" if closure_valid and not missing_requirements else f"missing/invalid: {missing_requirements}",
        )

    def _validate_derived_module_contracts(
        self,
        checks: list[dict[str, Any]],
        *,
        module_id: str | None = None,
    ) -> None:
        try:
            map_bytes = self.resolver.read_bytes(_DECOMPOSITION_MAP_PATH)
            source_map = strict_json_loads(map_bytes.decode("utf-8"), source=_DECOMPOSITION_MAP_PATH)
        except (BootError, UnicodeDecodeError) as exc:
            self._check(checks, "DERIVED_MODULE_SOURCE_MAP", False, str(exc))
            return
        map_valid = (
            _sha256(map_bytes) == _DECOMPOSITION_MAP_SHA256
            and isinstance(source_map, Mapping)
            and source_map.get("SYSTEM_DESIGNATION") == "AIR_WS7_MODULE_DECOMPOSITION_MAP_V1"
            and source_map.get("artifact_class") == "SOURCE_SPAN_MAP"
            and isinstance(source_map.get("chunks"), list)
        )
        self._check(
            checks,
            "DERIVED_MODULE_SOURCE_MAP",
            map_valid,
            _DECOMPOSITION_MAP_PATH,
            expected_sha256=_DECOMPOSITION_MAP_SHA256,
            observed_sha256=_sha256(map_bytes),
        )
        if not map_valid:
            return

        chunks_by_module: dict[str, list[Mapping[str, Any]]] = {}
        for raw_chunk in source_map["chunks"]:
            if not isinstance(raw_chunk, Mapping):
                self._check(checks, "DERIVED_MODULE_SOURCE_MAP_CHUNKS", False, "chunk must be an object")
                return
            chunk_module_id = raw_chunk.get("module_id")
            if not isinstance(chunk_module_id, str):
                self._check(checks, "DERIVED_MODULE_SOURCE_MAP_CHUNKS", False, "chunk module_id missing")
                return
            chunks_by_module.setdefault(chunk_module_id, []).append(raw_chunk)

        selected_ids = (
            [module_id]
            if module_id in _DERIVED_MODULE_CONTRACTS
            else list(_DERIVED_MODULE_CONTRACTS)
            if module_id is None
            else []
        )
        for current_id in selected_ids:
            expected_digest, expected_source, expected_count, expected_bytes = _DERIVED_MODULE_CONTRACTS[current_id]
            module = self._modules.get(current_id)
            if not isinstance(module, Mapping):
                self._check(checks, f"DERIVED_MODULE_CONTENT_{current_id}", False, "module missing")
                continue
            relative_path = module.get("relative_path")
            try:
                module_bytes = self.resolver.read_bytes(str(relative_path))
            except Exception as exc:
                self._check(checks, f"DERIVED_MODULE_CONTENT_{current_id}", False, str(exc))
                continue

            chunks = chunks_by_module.get(current_id, [])
            chunk_shape_valid = (
                len(chunks) == expected_count
                and all(
                    isinstance(chunk.get("source_file"), str)
                    and isinstance(chunk.get("start_line"), int)
                    and isinstance(chunk.get("end_line"), int)
                    and isinstance(chunk.get("sha256"), str)
                    and _SHA256.fullmatch(str(chunk.get("sha256"))) is not None
                    and isinstance(chunk.get("bytes"), int)
                    for chunk in chunks
                )
                and sum(int(chunk["bytes"]) for chunk in chunks) == expected_bytes
            )
            marker_metadata: list[dict[str, Any]] = []
            marker_valid = True
            for match in _SOURCE_CHUNK_MARKER.finditer(module_bytes):
                try:
                    marker = strict_json_loads(match.group("meta").decode("utf-8"), source=str(relative_path))
                except (BootError, UnicodeDecodeError):
                    marker_valid = False
                    break
                if not isinstance(marker, dict):
                    marker_valid = False
                    break
                marker_metadata.append(marker)
            expected_markers = [
                {
                    "source": chunk["source_file"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "sha256": chunk["sha256"],
                }
                for chunk in chunks
            ]
            manifest_contract_valid = (
                module.get("authoritative_source") == "DERIVED_FROM_APPROVED_WS6_MONOLITH"
                and module.get("source_span_map_ref") == _DECOMPOSITION_MAP_PATH
                and module.get("source_file") == expected_source
                and module.get("source_span_count") == expected_count
                and module.get("source_span_bytes") == expected_bytes
                and module.get("sha256") == expected_digest
            )
            content_valid = (
                _sha256(module_bytes) == expected_digest
                and chunk_shape_valid
                and marker_valid
                and marker_metadata == expected_markers
            )
            self._check(
                checks,
                f"DERIVED_MODULE_CONTENT_{current_id}",
                manifest_contract_valid and content_valid,
                str(relative_path),
                expected_sha256=expected_digest,
                observed_sha256=_sha256(module_bytes),
                expected_source_span_count=expected_count,
                observed_source_span_count=len(marker_metadata),
                expected_source_span_bytes=expected_bytes,
                observed_source_span_bytes=(
                    sum(int(chunk["bytes"]) for chunk in chunks) if chunk_shape_valid else None
                ),
            )

    def _validate_receipt_contract_resources(self, checks: list[dict[str, Any]]) -> None:
        try:
            schema = self._load_json("runtime/boot/schemas/AIR BOOT COMPILE RECEIPT SCHEMA.json")
            template = self._load_json("runtime/boot/templates/AIR BOOT COMPILE RECEIPT TEMPLATE.json")
        except BootError as exc:
            self._check(checks, "COMPILE_RECEIPT_CONTRACT", False, exc.message)
            return
        required_receipt_fields = {
            "schema_id",
            "schema_version",
            "created_at_utc",
            "package_version",
            "resource_set_version",
            "plan_id",
            "boot_mode",
            "requested_triggers",
            "bundle_sha256",
            "resource_count",
            "authorization_decision",
            "claim_boundary",
        }
        schema_required = schema.get("required")
        schema_valid = (
            schema.get("$id") == "urn:air:boot:compile-receipt:1"
            and schema.get("type") == "object"
            and schema.get("additionalProperties") is False
            and isinstance(schema_required, list)
            and set(schema_required) == required_receipt_fields
        )
        template_valid = (
            template.get("schema_id") == "AIR_BOOT_COMPILE_RECEIPT"
            and template.get("schema_version") == "1.0.0"
            and template.get("authorization_decision") == "NOT_EVALUATED"
        )
        self._check(
            checks,
            "COMPILE_RECEIPT_CONTRACT",
            schema_valid and template_valid,
            "complete" if schema_valid and template_valid else "schema or template mismatch",
        )

    def validate(self, *, module_id: str | None = None) -> dict[str, Any]:
        checks: list[dict[str, Any]] = []
        self._validate_manifest_contract(checks)
        self._validate_starter_contract(checks)
        self._validate_semantic_contract(checks)
        self._validate_receipt_contract_resources(checks)
        self._validate_derived_module_contracts(checks, module_id=module_id)

        kernel_entry = self.manifest.get("kernel")
        self._check(
            checks,
            "KERNEL_DECLARATION",
            isinstance(kernel_entry, Mapping)
            and kernel_entry.get("module_id") == "AIR_BOOT_KERNEL_V1"
            and kernel_entry.get("relative_path") == "runtime/boot/AIR BOOT KERNEL.md"
            and kernel_entry.get("version") == "1.1.0"
            and kernel_entry.get("terminal_sentinel") == _KERNEL_SENTINEL,
            str(kernel_entry),
        )
        self._verify_declared_resource(
            checks,
            label="KERNEL_RESOURCE",
            entry=kernel_entry,
            path_field="relative_path",
            require_sentinel=True,
            required_markers=_KERNEL_REQUIRED_MARKERS,
        )
        self._verify_declared_resource(
            checks,
            label="STARTER_RESOURCE",
            entry=self.manifest.get("boot_starter"),
            path_field="relative_path",
        )
        self._verify_declared_resource(
            checks,
            label="SEMANTIC_CLOSURE_RESOURCE",
            entry=self.manifest.get("semantic_closure"),
            path_field="relative_path",
        )
        self._verify_declared_resource(
            checks,
            label="COMPILE_RECEIPT_SCHEMA_RESOURCE",
            entry=self.manifest.get("compile_receipt_schema"),
            path_field="relative_path",
        )
        self._verify_declared_resource(
            checks,
            label="COMPILE_RECEIPT_TEMPLATE_RESOURCE",
            entry=self.manifest.get("compile_receipt_template"),
            path_field="relative_path",
        )

        canonical = self.manifest.get("canonical_monolith")
        if isinstance(canonical, list):
            for index, entry in enumerate(canonical):
                self._verify_declared_resource(
                    checks,
                    label=f"COMPLETE_PROMPT_RESOURCE_{index + 1}",
                    entry=entry,
                    path_field="file",
                )

        load_classes = set(_as_string_list(self.manifest.get("load_order_classes"), "load_order_classes"))
        target_modules = [module_id] if module_id else list(self._modules)
        if module_id and module_id not in self._modules:
            raise BootError(f"Unknown AIR boot module: {module_id}")
        for current_id in target_modules:
            module = self._modules[current_id]
            relative_path = module.get("relative_path")
            markdown_module = isinstance(relative_path, str) and relative_path.lower().endswith((".md", ".markdown"))
            markers = (
                f"SYSTEM_DESIGNATION: {current_id}",
                f"ARTIFACT_CLASS: {module.get('artifact_class')}",
            ) if markdown_module else ()
            self._verify_declared_resource(
                checks,
                label=f"MODULE_RESOURCE_{current_id}",
                entry=module,
                path_field="relative_path",
                require_sentinel=markdown_module,
                required_markers=markers,
            )
            required_fields = (
                "module_id",
                "artifact_class",
                "version",
                "relative_path",
                "sha256",
                "size_bytes",
                "load_class",
                "triggers",
                "purpose",
                "dependencies",
                "conflicts",
                "terminal_sentinel",
                "authoritative_source",
            )
            missing = _missing_keys(module, required_fields)
            self._check(
                checks,
                f"MODULE_STRUCTURE_{current_id}",
                not missing,
                "complete" if not missing else f"missing: {missing}",
            )
            dependencies = module.get("dependencies")
            conflicts = module.get("conflicts")
            valid_dependencies = isinstance(dependencies, list) and all(item in self._modules for item in dependencies)
            valid_conflicts = isinstance(conflicts, list) and all(
                item in self._modules and item != current_id for item in conflicts
            )
            valid_triggers = isinstance(module.get("triggers"), list) and all(
                isinstance(item, str) and _SAFE_TRIGGER.fullmatch(item) for item in module.get("triggers", [])
            )
            self._check(checks, f"MODULE_DEPENDENCIES_{current_id}", valid_dependencies, current_id)
            self._check(checks, f"MODULE_CONFLICTS_{current_id}", valid_conflicts, current_id)
            self._check(
                checks,
                f"MODULE_LOAD_CLASS_{current_id}",
                module.get("load_class") in load_classes,
                str(module.get("load_class")),
            )
            self._check(checks, f"MODULE_TRIGGERS_{current_id}", valid_triggers, current_id)

        cycle = self._dependency_cycle()
        self._check(checks, "DEPENDENCY_GRAPH_ACYCLIC", cycle is None, "none" if cycle is None else " -> ".join(cycle))

        q1d = self._modules.get(Q1D_MODULE_ID)
        q1d_valid = q1d is not None
        q1d_missing: list[str] = []
        if q1d and isinstance(q1d.get("relative_path"), str):
            q1d_text = self.resolver.read_text(str(q1d["relative_path"]))
            q1d_missing = [heading for heading in _Q1D_REQUIRED_HEADINGS if heading not in q1d_text]
            q1d_valid = not q1d_missing and "Do not activate a project" in q1d_text
        self._check(
            checks,
            "Q1D_BEGINNER_ORIENTATION_CLOSURE",
            q1d_valid,
            "complete" if q1d_valid else ", ".join(q1d_missing) or "module missing",
        )

        failed = [check for check in checks if check["status"] == "FAIL"]
        return {
            "decision": "PASS" if not failed else "FAIL",
            "manifest_version": self.manifest.get("version"),
            "resource_set_version": self.resolver.resource_set_version,
            "module_count": len(self._modules),
            "checks": checks,
            "failed_count": len(failed),
            "claim_boundary": (
                "Validation proves observed resource integrity, required document structure, dependency closure, and "
                "declared semantic contracts. It does not prove model-equivalent behavior, execution authorization, "
                "or project correctness."
            ),
        }

    def _known_triggers(self) -> set[str]:
        result = {"SESSION_ENTRY", "Q1_D_ORIENTATION"}
        for module in self._modules.values():
            triggers = module.get("triggers", [])
            if isinstance(triggers, list):
                result.update(str(trigger) for trigger in triggers)
        return result

    def _semantic_requirements(self, triggers: set[str]) -> set[str]:
        required: set[str] = set()
        declared = self.semantic_closure.get("required_modules", {})
        if isinstance(declared, Mapping):
            for trigger in triggers | {"SESSION_ENTRY"}:
                values = declared.get(trigger, [])
                if isinstance(values, list):
                    required.update(str(value) for value in values)
        return required

    def _dependency_closure(self, selected: set[str]) -> set[str]:
        def add(module_id: str) -> None:
            if module_id not in self._modules:
                raise BootError(f"Semantic closure references unknown module: {module_id}")
            if module_id not in selected:
                selected.add(module_id)
            dependencies = self._modules[module_id].get("dependencies", [])
            if not isinstance(dependencies, list):
                raise BootError(f"AIR boot module dependencies must be an array: {module_id}")
            for dependency in dependencies:
                add(str(dependency))

        for module_id in list(selected):
            add(module_id)
        return selected

    def _ordered_modules(self, selected: set[str]) -> list[str]:
        order_classes = _as_string_list(self.manifest.get("load_order_classes"), "load_order_classes")
        class_rank = {name: index for index, name in enumerate(order_classes)}
        result: list[str] = []
        emitted: set[str] = set()

        def emit(module_id: str) -> None:
            if module_id in emitted:
                return
            dependencies = self._modules[module_id].get("dependencies", [])
            if not isinstance(dependencies, list):
                raise BootError(f"AIR boot module dependencies must be an array: {module_id}")
            for dependency in dependencies:
                emit(str(dependency))
            emitted.add(module_id)
            result.append(module_id)

        for module_id in sorted(
            selected,
            key=lambda item: (
                class_rank.get(str(self._modules[item].get("load_class")), len(class_rank)),
                self._manifest_order[item],
                item,
            ),
        ):
            emit(module_id)
        return result

    def _resource_identity(self) -> dict[str, str]:
        return {
            "package_version": __version__,
            "resource_set_version": self.resolver.resource_set_version,
            "source_tree_digest": self.resolver.source_tree_digest,
        }

    def plan(
        self,
        triggers: Sequence[str] = (),
        *,
        fallback: str = "FULL_MONOLITH",
    ) -> dict[str, Any]:
        validation = self.validate()
        if validation["decision"] != "PASS":
            raise BootError("AIR boot resources failed validation", details={"validation": validation})
        normalized = {trigger.strip().upper() for trigger in triggers if trigger.strip()}
        if not normalized:
            normalized = {"SESSION_ENTRY"}
        unsafe = sorted(trigger for trigger in normalized if not _SAFE_TRIGGER.fullmatch(trigger))
        if unsafe:
            raise BootError("Unsafe AIR boot trigger", details={"unsafe_triggers": unsafe})
        unknown = sorted(normalized - self._known_triggers())
        identity = self._resource_identity()
        if unknown:
            if fallback != "FULL_MONOLITH":
                raise BootError("Unknown AIR boot trigger", details={"unknown_triggers": unknown})
            plan_basis = {
                **identity,
                "boot_mode": "FULL_MONOLITH",
                "requested_triggers": sorted(normalized),
                "unknown_triggers": unknown,
                "resources": list(COMPLETE_PROMPT_SET),
                "fallback_state": "UNKNOWN_TRIGGER_FULL_MONOLITH",
            }
            return {
                "decision": "REVIEW",
                **plan_basis,
                "plan_id": _sha256(_canonical_json(plan_basis)),
                "planned_modules": [],
                "authorization_decision": "NOT_EVALUATED",
                "next_action": "Review the unknown trigger or continue with the Complete AIR Prompt Set fallback.",
            }

        selected = {
            module_id
            for module_id, module in self._modules.items()
            if module.get("load_class") == "SESSION_ENTRY"
            or (isinstance(module.get("triggers"), list) and normalized.intersection(module.get("triggers", [])))
        }
        selected.update(self._semantic_requirements(normalized))
        selected = self._dependency_closure(selected)
        conflicts: list[tuple[str, str]] = []
        for module_id in selected:
            module_conflicts = self._modules[module_id].get("conflicts", [])
            if not isinstance(module_conflicts, list):
                raise BootError(f"AIR boot module conflicts must be an array: {module_id}")
            for conflict in module_conflicts:
                if conflict in selected:
                    conflicts.append((module_id, str(conflict)))
        if conflicts:
            raise BootError("AIR boot plan contains conflicting modules", details={"conflicts": conflicts})
        planned = self._ordered_modules(selected)
        plan_basis = {
            **identity,
            "boot_mode": "LOCAL_BUNDLED",
            "requested_triggers": sorted(normalized),
            "planned_modules": planned,
            "fallback_state": "NOT_REQUIRED",
            "manifest_version": self.manifest.get("version"),
        }
        return {
            "decision": "PASS",
            **plan_basis,
            "plan_id": _sha256(_canonical_json(plan_basis)),
            "unknown_triggers": [],
            "authorization_decision": "NOT_EVALUATED",
            "next_action": "Review the plan, then compile or supply it to the selected host.",
        }

    def _resource_record(self, path: str) -> tuple[dict[str, Any], bytes]:
        data = self.resolver.read_bytes(path)
        return {"relative_path": path, "sha256": _sha256(data), "size_bytes": len(data)}, data

    @staticmethod
    def _resource_frame(record: Mapping[str, Any], data: bytes) -> bytes:
        frame_metadata = {
            "relative_path": record["relative_path"],
            "sha256": record["sha256"],
            "size_bytes": record["size_bytes"],
        }
        header = b"<!-- AIR_RESOURCE_BEGIN " + _canonical_json(frame_metadata).rstrip(b"\n") + b" -->\n"
        footer = f"\n<!-- AIR_RESOURCE_END {record['relative_path']} -->\n".encode()
        return header + data + footer

    def compile(self, triggers: Sequence[str] = (), *, fallback: str = "FULL_MONOLITH") -> dict[str, Any]:
        plan = self.plan(triggers, fallback=fallback)
        if plan["boot_mode"] == "FULL_MONOLITH":
            paths = list(COMPLETE_PROMPT_SET)
        else:
            paths = [
                str(self.manifest["kernel"]["relative_path"]),
                BOOT_MANIFEST_PATH,
                BOOT_STARTER_PATH,
                SEMANTIC_CLOSURE_PATH,
            ] + [str(self._modules[module_id]["relative_path"]) for module_id in plan["planned_modules"]]
        deduped = list(dict.fromkeys(paths))
        resources = [self._resource_record(path) for path in deduped]
        records = [record for record, _data in resources]
        bundle_manifest = {
            "schema_id": "AIR_DETERMINISTIC_BOOT_BUNDLE",
            "schema_version": "1.0.0",
            "package_version": __version__,
            "resource_set_version": self.resolver.resource_set_version,
            "source_tree_digest": self.resolver.source_tree_digest,
            "boot_mode": plan["boot_mode"],
            "requested_triggers": plan["requested_triggers"],
            "plan_id": plan["plan_id"],
            "authorization_decision": "NOT_EVALUATED",
            "fallback_state": plan["fallback_state"],
            "session_entry_guards": dict(_EXPECTED_SESSION_ENTRY_GUARDS),
            "host_context_boundary": {
                "current_session_sources": "VISIBLE_USER_MESSAGES_AND_EXPLICIT_CURRENT_ATTACHMENTS",
                "unenumerated_host_context": "UNTRUSTED_FOR_PROJECT_STATE",
                "isolation_unprovable_action": "SET_CONTEXT_PROVENANCE_UNRESOLVED_AND_IGNORE_FOR_STATE",
            },
            "host_verification_claim_ceiling": {
                "bundle_hashes_and_sizes": "COMPILE_TIME_DECLARATIONS",
                "loading_bundle_alone": "NOT_TOOL_OBSERVED",
                "tool_observed_requires": "CURRENT_SESSION_TOOL_RESULT_OR_SEPARATELY_SUPPLIED_COMPILE_RECEIPT",
                "without_evidence": "PROMPT_DECLARED_OR_UNVERIFIED",
            },
            "framing": {
                "format": "AIR_RESOURCE_LENGTH_FRAMED_V1",
                "size_field": "size_bytes",
                "digest_scope": "exact_resource_bytes",
            },
            "resources": records,
            "claim_boundary": (
                "This deterministic bundle records exact selected bytes at compile time. A host model that merely "
                "receives the file has not performed digest verification. Loading it is not execution authorization, "
                "proof of model-equivalent behavior, or permission for mutating actions."
            ),
        }
        header = (
            "# AIR Deterministic Boot Bundle\n\n"
            "## Mandatory session-entry guards\n\n"
            "- `Start a new AIR project.` is activation intent only. It does not select Q1=A. While Q1 is active, "
            "advance only after an explicit A-D selector or explicit `Q1=<letter>` choice; otherwise render Q1 again "
            "and wait.\n"
            "- Current project state may use only visible current-session messages and files explicitly attached or "
            "identified in this session. Unenumerated host memory, prior uploads, hidden project files, and prior "
            "session state are untrusted for project-state claims.\n"
            "- The SHA-256 values below are compile-time metadata. Receiving this file alone does not justify "
            "`TOOL_OBSERVED`, `CRYPTOGRAPHICALLY_VERIFIED`, or N-of-N resource-verification claims. "
            "Such claims require a visible current-session tool result or separately supplied compile receipt.\n\n"
            "The resource frames below are length-delimited. The first `size_bytes` bytes after each frame header are "
            "the exact resource bytes covered by that frame's compile-time SHA-256 declaration.\n\n"
            "```json\n"
            f"{json.dumps(bundle_manifest, ensure_ascii=False, indent=2, sort_keys=True)}\n"
            "```\n\n"
        ).encode()
        data = header + b"".join(self._resource_frame(record, resource_data) for record, resource_data in resources)
        return {
            "decision": "PASS" if plan["decision"] == "PASS" else "REVIEW",
            "plan": plan,
            "bundle_manifest": bundle_manifest,
            "bundle_bytes": data,
            "bundle_sha256": _sha256(data),
            "resource_count": len(records),
        }

    def receipt(self, compiled: Mapping[str, Any]) -> dict[str, Any]:
        plan = compiled["plan"]
        return {
            "schema_id": "AIR_BOOT_COMPILE_RECEIPT",
            "schema_version": "1.0.0",
            "created_at_utc": utc_now(),
            "package_version": __version__,
            "resource_set_version": self.resolver.resource_set_version,
            "plan_id": plan["plan_id"],
            "boot_mode": plan["boot_mode"],
            "requested_triggers": plan["requested_triggers"],
            "bundle_sha256": compiled["bundle_sha256"],
            "resource_count": compiled["resource_count"],
            "authorization_decision": "NOT_EVALUATED",
            "claim_boundary": (
                "This receipt proves only the observed local compilation and bundle digest. It grants no execution, "
                "mutation, merge, release, or publication permission."
            ),
        }

    def _ensure_output_safe(self, output: Path) -> None:
        """Protect canonical authoring resources from bundle-output mutation."""

        root = self.resolver.root
        if not isinstance(root, Path):
            return
        resolved = output.expanduser().resolve()
        source_root = root.resolve()
        for name in ("prompts", "profiles", "runtime"):
            canonical = (source_root / name).resolve()
            if resolved == canonical or resolved.is_relative_to(canonical):
                raise BootError(
                    "AIR boot output may not overwrite canonical authoring resources",
                    details={"output": str(resolved), "protected_root": str(canonical)},
                )

    @staticmethod
    def _snapshot_file(path: Path) -> tuple[bool, bytes | None]:
        if not path.exists():
            return False, None
        if not path.is_file():
            raise BootError(f"AIR boot output exists but is not a file: {path}")
        try:
            return True, path.read_bytes()
        except OSError as exc:
            raise BootError(f"Cannot snapshot AIR boot output before writing: {path}: {exc}") from exc

    @staticmethod
    def _restore_file(path: Path, snapshot: tuple[bool, bytes | None]) -> None:
        existed, data = snapshot
        if existed:
            if data is None:
                raise OSError(f"Missing rollback bytes for {path}")
            atomic_write_bytes(path, data)
        else:
            path.unlink(missing_ok=True)

    @staticmethod
    def _lock_path(path: Path) -> Path:
        resolved = path.expanduser().resolve()
        return resolved.parent / f".{resolved.name}.air-boot.lock"

    def _target_locks(self, *targets: Path | None) -> ExitStack:
        stack = ExitStack()
        lock_paths = sorted({self._lock_path(path) for path in targets if path is not None}, key=str)
        try:
            for lock_path in lock_paths:
                stack.enter_context(FileLock(lock_path, timeout=30.0, stale_after=300.0))
        except Exception:
            stack.close()
            raise
        return stack

    @staticmethod
    def _verify_written_pair(output: Path, expected_digest: str, receipt_output: Path | None) -> None:
        observed = _sha256(output.read_bytes())
        if observed != expected_digest:
            raise OSError(f"bundle digest mismatch after write: expected {expected_digest}, observed {observed}")
        if receipt_output is not None:
            receipt = strict_json_loads(receipt_output.read_text(encoding="utf-8"), source=str(receipt_output))
            if not isinstance(receipt, Mapping) or receipt.get("bundle_sha256") != expected_digest:
                raise OSError("receipt does not reference the written bundle digest")

    def write_bundle(
        self,
        output: Path,
        triggers: Sequence[str] = (),
        *,
        fallback: str = "FULL_MONOLITH",
        overwrite: bool = False,
        receipt_output: Path | None = None,
    ) -> dict[str, Any]:
        self._ensure_output_safe(output)
        if receipt_output:
            self._ensure_output_safe(receipt_output)
            if output.expanduser().resolve() == receipt_output.expanduser().resolve():
                raise BootError("AIR boot bundle and receipt outputs must be different files")

        with self._target_locks(output, receipt_output):
            if output.exists() and not overwrite:
                raise BootError(f"AIR boot output already exists: {output}")
            if receipt_output and receipt_output.exists() and not overwrite:
                raise BootError(f"AIR boot receipt output already exists: {receipt_output}")

            output_snapshot = self._snapshot_file(output)
            receipt_snapshot = self._snapshot_file(receipt_output) if receipt_output else None
            compiled = self.compile(triggers, fallback=fallback)
            receipt = self.receipt(compiled)
            try:
                atomic_write_bytes(output, compiled["bundle_bytes"])
                if receipt_output:
                    atomic_write_json(receipt_output, receipt)
                self._verify_written_pair(output, compiled["bundle_sha256"], receipt_output)
            except Exception as exc:
                rollback_errors: list[str] = []
                try:
                    self._restore_file(output, output_snapshot)
                except OSError as rollback_exc:
                    rollback_errors.append(f"bundle output: {rollback_exc}")
                if receipt_output and receipt_snapshot is not None:
                    try:
                        self._restore_file(receipt_output, receipt_snapshot)
                    except OSError as rollback_exc:
                        rollback_errors.append(f"receipt output: {rollback_exc}")
                message = "AIR boot bundle write failed"
                message += "; rollback was incomplete" if rollback_errors else " and was rolled back"
                raise BootError(
                    message,
                    details={"cause": str(exc), "rollback_errors": rollback_errors},
                ) from exc
        return {
            "decision": compiled["decision"],
            "output": str(output),
            "receipt_output": str(receipt_output) if receipt_output else None,
            "bundle_sha256": compiled["bundle_sha256"],
            "plan": compiled["plan"],
            "receipt": receipt,
        }

    def write_receipt(
        self,
        output: Path,
        triggers: Sequence[str] = (),
        *,
        fallback: str = "FULL_MONOLITH",
        overwrite: bool = False,
    ) -> dict[str, Any]:
        self._ensure_output_safe(output)
        with self._target_locks(output):
            if output.exists() and not overwrite:
                raise BootError(f"AIR boot receipt output already exists: {output}")
            snapshot = self._snapshot_file(output)
            compiled = self.compile(triggers, fallback=fallback)
            receipt = self.receipt(compiled)
            try:
                atomic_write_json(output, receipt)
                observed = strict_json_loads(output.read_text(encoding="utf-8"), source=str(output))
                if not isinstance(observed, Mapping) or observed.get("bundle_sha256") != compiled["bundle_sha256"]:
                    raise OSError("written receipt failed post-write verification")
            except Exception as exc:
                rollback_errors: list[str] = []
                try:
                    self._restore_file(output, snapshot)
                except OSError as rollback_exc:
                    rollback_errors.append(str(rollback_exc))
                message = "AIR boot receipt write failed"
                message += "; rollback was incomplete" if rollback_errors else " and was rolled back"
                raise BootError(message, details={"cause": str(exc), "rollback_errors": rollback_errors}) from exc
        return {"decision": compiled["decision"], "output": str(output), "receipt": receipt}

    def compare(self, triggers: Sequence[str] = ()) -> dict[str, Any]:
        plan = self.plan(triggers)
        complete_bytes = sum(len(self.resolver.read_bytes(path)) for path in COMPLETE_PROMPT_SET)
        compiled = self.compile(triggers)
        selected_bytes = len(compiled["bundle_bytes"])
        return {
            "decision": plan["decision"],
            "requested_triggers": plan["requested_triggers"],
            "complete_prompt_set_bytes": complete_bytes,
            "compiled_bundle_bytes": selected_bytes,
            "ratio": selected_bytes / complete_bytes if complete_bytes else None,
            "planned_modules": plan["planned_modules"],
            "claim_boundary": "Byte comparison does not measure behavioral equivalence or quality.",
        }

    def q1d_orientation(self) -> dict[str, Any]:
        plan = self.plan(["Q1_D_ORIENTATION"])
        module = self._modules[Q1D_MODULE_ID]
        return {
            "decision": "PASS",
            "module_id": Q1D_MODULE_ID,
            "relative_path": module["relative_path"],
            "plan_id": plan["plan_id"],
            "content": self.resolver.read_text(str(module["relative_path"])),
            "activation_state": "NOT_ACTIVATED",
            "next_action": "Return to Q1 after the user declines or completes the optional example.",
        }

    def status(self) -> dict[str, Any]:
        validation = self.validate()
        return {
            "decision": validation["decision"],
            "package_version": __version__,
            "resource_origin": self.resolver.origin,
            "resource_set_version": self.resolver.resource_set_version,
            "source_tree_digest": self.resolver.source_tree_digest,
            "manifest_version": self.manifest.get("version"),
            "semantic_closure_version": self.semantic_closure.get("schema_version"),
            "module_count": len(self._modules),
            "complete_prompt_set_available": all(self.resolver.resolve(path) for path in COMPLETE_PROMPT_SET),
            "q1d_orientation_available": Q1D_MODULE_ID in self._modules,
            "network_required": False,
            "authorization_decision": "NOT_EVALUATED",
            "validation": validation,
        }
