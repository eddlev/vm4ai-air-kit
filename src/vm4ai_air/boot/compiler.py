"""Installed-resource-backed AIR modular boot service."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from vm4ai_air.errors import BootError
from vm4ai_air.io import atomic_write_bytes, atomic_write_json, utc_now
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


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _as_string_list(value: object, field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise BootError(f"AIR boot field {field} must be an array of non-empty strings")
    return list(value)


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
        entry: Mapping[str, Any],
        path_field: str,
    ) -> None:
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
        passed = digest == observed_digest and size == observed_size
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
        if sentinel is not None:
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                self._check(checks, f"{label}_SENTINEL", False, f"not UTF-8: {path}")
            else:
                self._check(
                    checks,
                    f"{label}_SENTINEL",
                    isinstance(sentinel, str) and text.rstrip().endswith(sentinel),
                    path,
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
            for dependency in self._modules[module_id].get("dependencies", []):
                if dependency in self._modules:
                    cycle = visit(dependency)
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

    def validate(self, *, module_id: str | None = None) -> dict[str, Any]:
        checks: list[dict[str, Any]] = []
        self._check(
            checks,
            "MANIFEST_IDENTITY",
            self.manifest.get("SYSTEM_DESIGNATION") == "AIR_BOOT_MODULE_MANIFEST_V1"
            and self.manifest.get("version") == "2.0.0",
            f"{self.manifest.get('SYSTEM_DESIGNATION')} {self.manifest.get('version')}",
        )
        self._check(
            checks,
            "STARTER_IDENTITY",
            self.starter.get("SYSTEM_DESIGNATION") == "AIR_BOOT_STARTER_PROFILE_V1"
            and self.starter.get("version") == "2.0.0",
            f"{self.starter.get('SYSTEM_DESIGNATION')} {self.starter.get('version')}",
        )
        self._check(
            checks,
            "SEMANTIC_CLOSURE_IDENTITY",
            self.semantic_closure.get("schema_id") == "AIR_BOOT_SEMANTIC_CLOSURE"
            and self.semantic_closure.get("schema_version") == "1.0.0",
            f"{self.semantic_closure.get('schema_id')} {self.semantic_closure.get('schema_version')}",
        )

        self._verify_declared_resource(
            checks,
            label="KERNEL_RESOURCE",
            entry=self.manifest.get("kernel", {}),
            path_field="relative_path",
        )
        self._verify_declared_resource(
            checks,
            label="STARTER_RESOURCE",
            entry=self.manifest.get("boot_starter", {}),
            path_field="relative_path",
        )
        self._verify_declared_resource(
            checks,
            label="SEMANTIC_CLOSURE_RESOURCE",
            entry=self.manifest.get("semantic_closure", {}),
            path_field="relative_path",
        )
        self._verify_declared_resource(
            checks,
            label="COMPILE_RECEIPT_SCHEMA_RESOURCE",
            entry=self.manifest.get("compile_receipt_schema", {}),
            path_field="relative_path",
        )
        self._verify_declared_resource(
            checks,
            label="COMPILE_RECEIPT_TEMPLATE_RESOURCE",
            entry=self.manifest.get("compile_receipt_template", {}),
            path_field="relative_path",
        )
        for index, entry in enumerate(self.manifest.get("canonical_monolith", [])):
            if isinstance(entry, Mapping):
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
            self._verify_declared_resource(
                checks,
                label=f"MODULE_RESOURCE_{current_id}",
                entry=module,
                path_field="relative_path",
            )
            dependencies = module.get("dependencies", [])
            conflicts = module.get("conflicts", [])
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

        closure_modules = self.semantic_closure.get("required_modules", {})
        closure_valid = isinstance(closure_modules, Mapping)
        if closure_valid:
            for trigger, required in closure_modules.items():
                if not isinstance(trigger, str) or not isinstance(required, list) or any(
                    module not in self._modules for module in required
                ):
                    closure_valid = False
                    break
        self._check(checks, "SEMANTIC_TRIGGER_CLOSURE", closure_valid, "required_modules")
        session_floor = {
            "AIR_RUNTIME_ENTRY_AND_ACTIVATION_V1",
            "AIR_CONTROL_ENTRY_VISIBILITY_AND_ONBOARDING_V1",
            "AIR_CONTROL_Q1D_BEGINNER_ORIENTATION_V1",
            "AIR_RUNTIME_POLICY_AND_HANDOFF_SECURITY_V1",
            "AIR_CONTROL_POLICY_HANDOFF_AND_PORTABILITY_V1",
        }
        declared_session = (
            set(closure_modules.get("SESSION_ENTRY", []))
            if isinstance(closure_modules, Mapping)
            else set()
        )
        self._check(
            checks,
            "SESSION_ENTRY_Q1_BRANCH_CLOSURE",
            session_floor.issubset(declared_session),
            ", ".join(sorted(declared_session)),
        )

        declared_complete = self.semantic_closure.get("complete_prompt_set")
        complete_valid = isinstance(declared_complete, list) and tuple(declared_complete) == COMPLETE_PROMPT_SET
        self._check(checks, "COMPLETE_PROMPT_SET_INTEGRATION", complete_valid, str(declared_complete))

        q1d = self._modules.get(Q1D_MODULE_ID)
        q1d_valid = q1d is not None
        q1d_missing: list[str] = []
        if q1d:
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
                "Validation proves observed resource integrity, dependency closure, and declared semantic contracts. "
                "It does not prove model-equivalent behavior, execution authorization, or project correctness."
            ),
        }

    def _known_triggers(self) -> set[str]:
        result = {"SESSION_ENTRY", "Q1_D_ORIENTATION"}
        for module in self._modules.values():
            result.update(module.get("triggers", []))
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
            if module_id in selected:
                dependencies = self._modules[module_id].get("dependencies", [])
            else:
                selected.add(module_id)
                dependencies = self._modules[module_id].get("dependencies", [])
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
            for dependency in self._modules[module_id].get("dependencies", []):
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
        unknown = sorted(normalized - self._known_triggers())
        if unknown:
            if fallback != "FULL_MONOLITH":
                raise BootError("Unknown AIR boot trigger", details={"unknown_triggers": unknown})
            plan_basis = {
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
            if module.get("load_class") == "SESSION_ENTRY" or normalized.intersection(module.get("triggers", []))
        }
        selected.update(self._semantic_requirements(normalized))
        selected = self._dependency_closure(selected)
        conflicts: list[tuple[str, str]] = []
        for module_id in selected:
            for conflict in self._modules[module_id].get("conflicts", []):
                if conflict in selected:
                    conflicts.append((module_id, str(conflict)))
        if conflicts:
            raise BootError("AIR boot plan contains conflicting modules", details={"conflicts": conflicts})
        planned = self._ordered_modules(selected)
        plan_basis = {
            "boot_mode": "LOCAL_BUNDLED",
            "requested_triggers": sorted(normalized),
            "planned_modules": planned,
            "fallback_state": "NOT_REQUIRED",
            "manifest_version": self.manifest.get("version"),
            "resource_set_version": self.resolver.resource_set_version,
        }
        return {
            "decision": "PASS",
            **plan_basis,
            "plan_id": _sha256(_canonical_json(plan_basis)),
            "unknown_triggers": [],
            "authorization_decision": "NOT_EVALUATED",
            "next_action": "Review the plan, then compile or supply it to the selected host.",
        }

    def _resource_record(self, path: str) -> dict[str, Any]:
        data = self.resolver.read_bytes(path)
        return {"relative_path": path, "sha256": _sha256(data), "size_bytes": len(data)}

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
        records = [self._resource_record(path) for path in deduped]
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
            "resources": records,
            "claim_boundary": (
                "This deterministic bundle records exact selected bytes. Loading it is not execution authorization, "
                "proof of model-equivalent behavior, or permission for mutating actions."
            ),
        }
        parts = [
            "# AIR Deterministic Boot Bundle",
            "",
            "```json",
            json.dumps(bundle_manifest, ensure_ascii=False, indent=2, sort_keys=True),
            "```",
            "",
        ]
        for path in deduped:
            text = self.resolver.read_text(path).rstrip()
            parts.extend(
                [
                    f"<!-- AIR_RESOURCE_BEGIN {path} -->",
                    text,
                    f"<!-- AIR_RESOURCE_END {path} -->",
                    "",
                ]
            )
        data = ("\n".join(parts).rstrip() + "\n").encode("utf-8")
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
        if output.exists() and not overwrite:
            raise BootError(f"AIR boot receipt output already exists: {output}")
        compiled = self.compile(triggers, fallback=fallback)
        receipt = self.receipt(compiled)
        atomic_write_json(output, receipt)
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
            "manifest_version": self.manifest.get("version"),
            "semantic_closure_version": self.semantic_closure.get("schema_version"),
            "module_count": len(self._modules),
            "complete_prompt_set_available": all(self.resolver.resolve(path) for path in COMPLETE_PROMPT_SET),
            "q1d_orientation_available": Q1D_MODULE_ID in self._modules,
            "network_required": False,
            "authorization_decision": "NOT_EVALUATED",
            "validation": validation,
        }
