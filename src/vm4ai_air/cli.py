"""Unified ``air`` command-line interface."""

from __future__ import annotations

import argparse
import json
import os
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from vm4ai_air.config import ConfigManager
from vm4ai_air.diagnostics import run_doctor
from vm4ai_air.errors import AirError
from vm4ai_air.paths import AppPaths
from vm4ai_air.resources import ResourceResolver
from vm4ai_air.version import base_version_payload
from vm4ai_air.workspace import WorkspaceManager


def _json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def _human_version(payload: Mapping[str, Any]) -> str:
    lines = [f"{payload['distribution']} {payload['package_version']}"]
    lines.append(f"AIR resources: {payload.get('resource_set_version', 'UNAVAILABLE')}")
    lines.append(f"Resource origin: {payload.get('resource_origin', 'UNAVAILABLE')}")
    return "\n".join(lines)


def _human_doctor(payload: Mapping[str, Any]) -> str:
    lines = [f"AIR doctor: {payload['decision']}"]
    for check in payload.get("checks", []):
        lines.append(f"[{check['status']}] {check['name']}: {check['detail']}")
    return "\n".join(lines)


def _human_paths(payload: Mapping[str, Any]) -> str:
    return "\n".join(f"{key}: {value}" for key, value in payload.items())


def _human_projects(payload: Sequence[Mapping[str, Any]]) -> str:
    if not payload:
        return "No AIR projects are registered."
    lines = []
    for project in payload:
        lines.append(f"{project['project_id']}  {project['name']}  {project['workspace_path']}")
    return "\n".join(lines)


def _emit(value: Any, *, json_mode: bool, formatter: Callable[[Any], str] | None = None) -> None:
    if json_mode:
        print(_json_dump(value))
    elif formatter:
        print(formatter(value))
    elif isinstance(value, str):
        print(value)
    else:
        print(_json_dump(value))


def _resolver(environment: Mapping[str, str], paths: AppPaths) -> ResourceResolver:
    return ResourceResolver.from_environment(environment=environment, paths=paths)


def _version_payload(environment: Mapping[str, str], paths: AppPaths) -> dict[str, Any]:
    payload: dict[str, Any] = base_version_payload()
    try:
        resolver = _resolver(environment, paths)
        payload.update(
            {
                "resource_set_version": resolver.resource_set_version,
                "source_tree_digest": resolver.source_tree_digest,
                "resource_origin": resolver.origin,
            }
        )
    except AirError as exc:
        payload.update(
            {
                "resource_set_version": "UNAVAILABLE",
                "resource_origin": "UNAVAILABLE",
                "resource_error": exc.message,
            }
        )
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="air",
        description="AIR local runtime, installed resources, and project workspaces",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--version", action="store_true", help="show package and resource-set versions")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("help", help="show this command menu")
    sub.add_parser("doctor", help="check installation, resources, paths, and active project")
    sub.add_parser("paths", help="show resolved AIR application paths")

    config = sub.add_parser("config", help="inspect or validate AIR user configuration")
    config_sub = config.add_subparsers(dest="config_command", required=True)
    config_sub.add_parser("show", help="show effective configuration")
    config_sub.add_parser("validate", help="validate effective configuration")
    config_write = config_sub.add_parser("write-default", help="create the default user configuration")
    config_write.add_argument("--overwrite", action="store_true")

    resources = sub.add_parser("resources", help="inspect installed canonical AIR resources")
    resource_sub = resources.add_subparsers(dest="resource_command", required=True)
    resource_list = resource_sub.add_parser("list", help="list resources")
    resource_list.add_argument("--prefix")
    resource_show = resource_sub.add_parser("show", help="show resource metadata")
    resource_show.add_argument("resource")
    resource_show.add_argument("--content", action="store_true", help="include UTF-8 content")
    resource_search = resource_sub.add_parser("search", help="search resource metadata and headings")
    resource_search.add_argument("query")
    resource_search.add_argument("--limit", type=int, default=20)
    resource_verify = resource_sub.add_parser("verify", help="verify one resource or the complete set")
    resource_verify.add_argument("resource", nargs="?")
    resource_materialize = resource_sub.add_parser("materialize", help="copy a resource to a versioned cache")
    resource_materialize.add_argument("resource")
    resource_materialize.add_argument("--purpose", required=True)

    project = sub.add_parser("project", help="manage isolated AIR project workspaces")
    project_sub = project.add_subparsers(dest="project_command", required=True)
    project_init = project_sub.add_parser("init", help="create and register a project workspace")
    project_init.add_argument("name")
    project_init.add_argument("--workspace")
    project_init.add_argument("--source")
    project_init.add_argument("--use", action="store_true", help="select the new project as active")
    project_sub.add_parser("list", help="list registered projects")
    project_show = project_sub.add_parser("show", help="show a project; defaults to the active project")
    project_show.add_argument("project", nargs="?")
    project_use = project_sub.add_parser("use", help="select an active project explicitly")
    project_use.add_argument("project")
    project_validate = project_sub.add_parser("validate", help="validate a project workspace")
    project_validate.add_argument("project", nargs="?")
    return parser


def _run(args: argparse.Namespace, *, environment: Mapping[str, str]) -> tuple[Any, Callable[[Any], str] | None, int]:
    paths = AppPaths.resolve(environment)
    if args.version:
        return _version_payload(environment, paths), _human_version, 0
    if args.command in {None, "help"}:
        return None, None, 0
    if args.command == "doctor":
        result = run_doctor(environment=environment)
        return result, _human_doctor, 0 if result["decision"] in {"PASS", "WARN"} else 3
    if args.command == "paths":
        return paths.as_dict(), _human_paths, 0
    if args.command == "config":
        manager = ConfigManager(paths, environment=environment)
        if args.config_command == "show":
            return manager.load(), None, 0
        if args.config_command == "validate":
            result = manager.validate()
            return result, None, 0 if result["decision"] == "PASS" else 2
        if args.config_command == "write-default":
            path = manager.write_default(overwrite=args.overwrite)
            return {"decision": "PASS", "path": str(path)}, None, 0
    if args.command == "resources":
        resolver = _resolver(environment, paths)
        if args.resource_command == "list":
            return resolver.list(prefix=args.prefix), None, 0
        if args.resource_command == "show":
            record = resolver.resolve(args.resource)
            result: dict[str, Any] = {"decision": "PASS", "resource": record}
            if args.content:
                result["content"] = resolver.read_text(args.resource)
            return result, None, 0
        if args.resource_command == "search":
            return resolver.search(args.query, limit=args.limit), None, 0
        if args.resource_command == "verify":
            result = resolver.verify(args.resource) if args.resource else resolver.verify_all()
            return result, None, 0 if result["decision"] == "PASS" else 3
        if args.resource_command == "materialize":
            return resolver.materialize(args.resource, purpose=args.purpose), None, 0
    if args.command == "project":
        manager = WorkspaceManager(paths, environment=environment)
        if args.project_command == "init":
            return (
                manager.init_project(
                    args.name,
                    workspace_path=args.workspace,
                    source_path=args.source,
                    make_active=args.use,
                ),
                None,
                0,
            )
        if args.project_command == "list":
            projects = manager.list_projects()
            return projects, _human_projects, 0
        if args.project_command == "show":
            return manager.show_project(args.project), None, 0
        if args.project_command == "use":
            return manager.use_project(args.project), None, 0
        if args.project_command == "validate":
            result = manager.validate_project(args.project)
            return result, None, 0 if result["decision"] == "PASS" else 3
    raise AirError("Unknown AIR command state")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command in {None, "help"} and not args.version:
        parser.print_help()
        return 0
    environment = dict(os.environ)
    try:
        value, formatter, exit_code = _run(args, environment=environment)
        if value is not None:
            _emit(value, json_mode=args.json, formatter=formatter)
        return exit_code
    except AirError as exc:
        _emit(exc.as_dict(), json_mode=args.json)
        return exc.exit_code
    except KeyboardInterrupt:
        _emit(
            {"decision": "ERROR", "error_code": "AIR_INTERRUPTED", "error": "Operation interrupted"},
            json_mode=args.json,
        )
        return 130
    except Exception as exc:  # pragma: no cover - defensive top-level boundary
        _emit(
            {
                "decision": "ERROR",
                "error_code": "AIR_UNEXPECTED_ERROR",
                "error": f"Unexpected failure: {exc}",
            },
            json_mode=True,
        )
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
