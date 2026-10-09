#!/usr/bin/env python3
"""AIR-P AMRS4E integrated compiler entrypoint."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path

_ENGINE_PATH = Path(__file__).resolve().with_name("air_p_compiler_engine.py")
_ENGINE_SPEC = importlib.util.spec_from_file_location("air_p_compiler_engine", _ENGINE_PATH)
if _ENGINE_SPEC is None or _ENGINE_SPEC.loader is None:
    raise ImportError(f"Unable to load AIR-P compiler engine from {_ENGINE_PATH}")
ENGINE = importlib.util.module_from_spec(_ENGINE_SPEC)
_ENGINE_SPEC.loader.exec_module(ENGINE)


def default_source_root():
    env = os.environ.get("AIR_P_SOURCE_ROOT")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[2]


def default_source_paths(root=None):
    root = Path(root or default_source_root()).resolve()
    return {
        "CORE_RUNTIME": str(root / "prompts" / "AIR_CORE_RUNTIME.md"),
        "GOVERNANCE_SUPPLEMENT": str(root / "prompts" / "AIR_GOV.md"),
        "CONTROL_SURFACE": str(root / "prompts" / "AIR_CONTROL_SURFACE.md"),
        "DEFAULT_STARTER_PROFILE": str(root / "prompts" / "AIR_DEFAULT_STARTER_PROFILE.json"),
        "HANDOFF_CARD_TEMPLATE": str(root / "prompts" / "AIR_HANDOFF_CARD_TEMPLATE.json"),
        "RUNTIME_ROUTE_MAP": str(root / "catalog" / "AIR_RUNTIME_ROUTE_MAP.json"),
        "PACKAGE_SCHEMA": str(root / "air_p" / "schema" / "AIR_P_PACKAGE_SCHEMA.json"),
        "COMPONENT_METADATA_OVERLAY": str(root / "air_p" / "source" / "AIR_P_COMPONENT_METADATA_OVERLAY.json"),
        "LAW_APPLICABILITY_ROUTER": str(root / "catalog" / "AIR_LAW_APPLICABILITY_ROUTER.json"),
        "LAW_SOURCE_PACKAGE_SCHEMA": str(root / "law_source" / "AIR_LAW_SOURCE_PACKAGE_SCHEMA.json"),
        "LAW_SOURCE_LAW_ID_REGISTRY": str(root / "law_source" / "AIR_LAW_ID_REGISTRY.json"),
        "LAW_SOURCE_LAW_BODY_INDEX": str(root / "law_source" / "AIR_LAW_BODY_INDEX.json"),
        "LAW_SOURCE_FLOOR_INVARIANT_INDEX": str(root / "law_source" / "AIR_FLOOR_INVARIANT_INDEX.json"),
    }


def build_payloads(paths=None):
    return ENGINE.build_payloads(paths or default_source_paths())


def mutation_suite(payloads=None, paths=None):
    paths = paths or default_source_paths()
    payloads = payloads or ENGINE.build_payloads(paths)
    return ENGINE.mutation_suite(payloads, paths)


def payload_hash_map(payloads):
    return ENGINE.payload_hash_map(payloads)


def deterministic_check_mutation_coverage(paths=None):
    paths = paths or default_source_paths()
    starter = ENGINE.strict_json_load(paths["DEFAULT_STARTER_PROFILE"])
    return ENGINE.deterministic_check_mutation_coverage(starter, paths)


def validate_source_inputs(paths=None):
    return ENGINE.validate_source_inputs(paths or default_source_paths())


def parse_args():
    root = default_source_root()
    d = default_source_paths(root)
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--source-root", default=str(root))
    ap.add_argument("--core", default=None)
    ap.add_argument("--control", default=None)
    ap.add_argument("--gov", default=None)
    ap.add_argument("--starter", default=None)
    ap.add_argument("--handoff", default=None)
    ap.add_argument("--route-map", default=None)
    ap.add_argument("--package-schema", default=None)
    ap.add_argument("--component-overlay", default=None)
    ap.add_argument("--law-router", default=None)
    ap.add_argument("--law-source-package-schema", default=None)
    ap.add_argument("--law-source-law-id-registry", default=None)
    ap.add_argument("--law-source-law-body-index", default=None)
    ap.add_argument("--law-source-floor-invariant-index", default=None)
    ap.add_argument("--test-source", default=None)
    args = ap.parse_args()
    root = Path(args.source_root).resolve()
    d = default_source_paths(root)
    paths = {
        "CORE_RUNTIME": args.core or d["CORE_RUNTIME"],
        "GOVERNANCE_SUPPLEMENT": args.gov or d["GOVERNANCE_SUPPLEMENT"],
        "CONTROL_SURFACE": args.control or d["CONTROL_SURFACE"],
        "DEFAULT_STARTER_PROFILE": args.starter or d["DEFAULT_STARTER_PROFILE"],
        "HANDOFF_CARD_TEMPLATE": args.handoff or d["HANDOFF_CARD_TEMPLATE"],
        "RUNTIME_ROUTE_MAP": args.route_map or d["RUNTIME_ROUTE_MAP"],
        "PACKAGE_SCHEMA": args.package_schema or d["PACKAGE_SCHEMA"],
        "COMPONENT_METADATA_OVERLAY": args.component_overlay or d["COMPONENT_METADATA_OVERLAY"],
        "LAW_APPLICABILITY_ROUTER": args.law_router or d["LAW_APPLICABILITY_ROUTER"],
        "LAW_SOURCE_PACKAGE_SCHEMA": args.law_source_package_schema or d["LAW_SOURCE_PACKAGE_SCHEMA"],
        "LAW_SOURCE_LAW_ID_REGISTRY": args.law_source_law_id_registry or d["LAW_SOURCE_LAW_ID_REGISTRY"],
        "LAW_SOURCE_LAW_BODY_INDEX": args.law_source_law_body_index or d["LAW_SOURCE_LAW_BODY_INDEX"],
        "LAW_SOURCE_FLOOR_INVARIANT_INDEX": args.law_source_floor_invariant_index or d["LAW_SOURCE_FLOOR_INVARIANT_INDEX"],
    }
    return args, paths


def main():
    args, paths = parse_args()
    test_source = args.test_source
    if test_source is None:
        sibling = Path(__file__).resolve().parents[1] / "tests" / "test_air_p_compiler.py"
        if sibling.is_file():
            test_source = str(sibling)
    source_state = ENGINE.validate_source_inputs(paths)
    ENGINE.compile_package(args.output, paths, test_source=test_source)
    print(json.dumps({
        "decision": "PASS",
        "output": str(Path(args.output).resolve()),
        "runtime_state": source_state["runtime_state"],
        "reconstruction_contract": ENGINE.RECONSTRUCTION_CONTRACT,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
