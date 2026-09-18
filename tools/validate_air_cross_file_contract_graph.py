#!/usr/bin/env python3
"""Build and validate the AIR cross-file contract graph.

The graph is derived from the candidate checkout on every run. It is validation
evidence only and never becomes semantic, binding, approval, or execution authority.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

VALIDATOR_IDENTITY = "AIR_CROSS_FILE_CONTRACT_GRAPH_VALIDATOR_V1"

NODE_CLASSES = {
    "FILE", "PATCH_MARKER", "ROUTE", "CONTROL_EVENT", "DEPENDENCY",
    "FORMAL_OBJECT", "STATE", "PROFILE_PACKAGE_COMPONENT", "MANIFEST",
    "CATALOG_ENTRY", "VALIDATION_CHECK", "BEHAVIORAL_SCENARIO",
    "MUTATION", "MIGRATION",
}
EDGE_CLASSES = {
    "OWNS", "MIRRORS", "PRODUCES", "CONSUMES", "RENDERS", "SERIALIZES",
    "RESTORES", "VALIDATES", "MUTATES_FOR_NEGATIVE_TEST", "DEPENDS_ON",
    "INDEXES", "PACKAGES",
}


class GraphError(Exception):
    pass


def reject_dupes(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise GraphError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_dupes)


def build_graph(root: Path) -> dict[str, Any]:
    manifest = load(root / "tests/air_full_surface_coverage_manifest.json")
    scenarios = load(root / "tests/air_full_surface_scenario_matrix.json")
    route_map = load(root / "catalog/AIR_RUNTIME_ROUTE_MAP.json")
    starter = load(root / "prompts/AIR_DEFAULT_STARTER_PROFILE.json")
    index = load(root / "catalog/AIR_SPECIALIST_PACKAGE_INDEX.json")
    handoff = load(root / "prompts/AIR_HANDOFF_CARD_TEMPLATE.json")["AIR_HANDOFF_CARD"]
    core_text = (root / "prompts/AIR_CORE_RUNTIME.md").read_text(encoding="utf-8")

    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, str]] = []
    errors: list[str] = []
    ownership: dict[str, set[str]] = defaultdict(set)

    def node(node_id: str, node_class: str, **attrs: Any) -> str:
        if node_class not in NODE_CLASSES:
            errors.append(f"UNKNOWN_NODE_CLASS:{node_class}:{node_id}")
        prior = nodes.get(node_id)
        current = {"node_id": node_id, "node_class": node_class, **attrs}
        if prior and prior.get("node_class") != node_class:
            errors.append(f"NODE_CLASS_CONFLICT:{node_id}:{prior.get('node_class')}:{node_class}")
        nodes[node_id] = {**(prior or {}), **current}
        return node_id

    def edge(src: str, dst: str, edge_class: str) -> None:
        if edge_class not in EDGE_CLASSES:
            errors.append(f"UNKNOWN_EDGE_CLASS:{edge_class}:{src}->{dst}")
        if src not in nodes:
            errors.append(f"EDGE_SOURCE_MISSING:{src}")
        if dst not in nodes:
            errors.append(f"EDGE_TARGET_MISSING:{dst}")
        edges.append({"from": src, "to": dst, "edge_class": edge_class})
        if edge_class == "OWNS":
            ownership[dst].add(src)

    file_paths = [r["canonical_path"] for r in manifest.get("files", [])]
    file_nodes = {p: node(f"FILE::{p}", "FILE", canonical_path=p) for p in file_paths}
    core_file = file_nodes.get("prompts/AIR_CORE_RUNTIME.md")
    starter_file = file_nodes.get("prompts/AIR_DEFAULT_STARTER_PROFILE.json")
    route_file = file_nodes.get("catalog/AIR_RUNTIME_ROUTE_MAP.json")
    index_file = file_nodes.get("catalog/AIR_SPECIALIST_PACKAGE_INDEX.json")
    handoff_file = file_nodes.get("prompts/AIR_HANDOFF_CARD_TEMPLATE.json")

    # Patch markers across behavior-bearing Markdown prompts.
    marker_re = re.compile(r"Patch marker:\s*([A-Z0-9_.-]+)")
    for path in [p for p in file_paths if p.startswith("prompts/") and p.endswith(".md")]:
        text = (root / path).read_text(encoding="utf-8")
        for marker in sorted(set(marker_re.findall(text))):
            mid = node(f"PATCH_MARKER::{marker}", "PATCH_MARKER", marker=marker)
            edge(file_nodes[path], mid, "OWNS")

    # Core formal-object catalog.
    formal_re = re.compile(r"^-\s+(AIR_[A-Z0-9_]+):\s+[A-Z0-9_]+", re.MULTILINE)
    for name in sorted(set(formal_re.findall(core_text))):
        oid = node(f"FORMAL_OBJECT::{name}", "FORMAL_OBJECT", object_name=name)
        if core_file:
            edge(core_file, oid, "OWNS")

    # Routes, dependencies, states and route-map mirrors.
    routes = route_map.get("routes", [])
    route_ids = {r.get("route_id") for r in routes}
    route_nodes = {}
    for route in routes:
        rid = route.get("route_id")
        if not rid:
            errors.append("ROUTE_WITHOUT_ID")
            continue
        rn = node(f"ROUTE::{rid}", "ROUTE", route_id=rid, semantic_owner=route.get("semantic_owner"))
        route_nodes[rid] = rn
        if core_file:
            edge(core_file, rn, "OWNS")
        if route_file:
            edge(route_file, rn, "MIRRORS")
        for dep in route.get("requires", []):
            dn = node(f"DEPENDENCY::{dep}", "DEPENDENCY", dependency_id=dep)
            edge(rn, dn, "DEPENDS_ON")
        for produced in route.get("produces", []):
            sn = node(f"STATE::{produced}", "STATE", state_id=produced)
            edge(rn, sn, "PRODUCES")
        for nxt in route.get("allowed_next_routes", route.get("allowed_next", [])):
            if nxt in route_ids:
                edge(rn, node(f"ROUTE::{nxt}", "ROUTE", route_id=nxt), "DEPENDS_ON")

    # Typed control-event registry must be bijective with routes.
    events = starter.get("compiler_contract", {}).get("runtime_control_event_registry", {}).get("events", [])
    event_by_route: dict[str, list[str]] = defaultdict(list)
    event_ids = set()
    for event in events:
        eid, rid = event.get("event_id"), event.get("route_id")
        if not eid or not rid:
            errors.append("CONTROL_EVENT_MISSING_ID_OR_ROUTE")
            continue
        if eid in event_ids:
            errors.append(f"DUPLICATE_CONTROL_EVENT:{eid}")
        event_ids.add(eid)
        en = node(f"CONTROL_EVENT::{eid}", "CONTROL_EVENT", event_id=eid, route_id=rid)
        if starter_file:
            edge(starter_file, en, "OWNS")
        if rid not in route_nodes:
            errors.append(f"CONTROL_EVENT_ORPHAN_ROUTE:{eid}:{rid}")
        else:
            edge(en, route_nodes[rid], "CONSUMES")
        event_by_route[rid].append(eid)
    for route in routes:
        rid = route.get("route_id")
        declared = route.get("control_event_ref")
        if not declared:
            errors.append(f"ROUTE_WITHOUT_CONTROL_EVENT_REF:{rid}")
        elif declared not in event_ids:
            errors.append(f"ROUTE_CONTROL_EVENT_MISSING:{rid}:{declared}")
        if len(event_by_route.get(rid, [])) != 1:
            errors.append(f"ROUTE_EVENT_CARDINALITY:{rid}:{len(event_by_route.get(rid, []))}")

    # Deterministic validation checks.
    checks = starter.get("validation_contract", {}).get("deterministic_contract_registry", {}).get("checks", [])
    for check in checks:
        cid = check.get("check_id")
        if not cid:
            errors.append("VALIDATION_CHECK_WITHOUT_ID")
            continue
        cn = node(f"VALIDATION_CHECK::{cid}", "VALIDATION_CHECK", operator=check.get("operator"))
        if starter_file:
            edge(starter_file, cn, "OWNS")
        path = check.get("file")
        if path in file_nodes:
            edge(cn, file_nodes[path], "VALIDATES")

    # Package manifests and component closure.
    basename_to_paths: dict[str, list[str]] = defaultdict(list)
    for path in file_paths:
        basename_to_paths[Path(path).name].append(path)

    manifest_paths = [p for p in file_paths if p.startswith("profiles/") and p.endswith("PACKAGE_MANIFEST.json")]
    manifest_nodes = {}
    for path in manifest_paths:
        mn = node(f"MANIFEST::{path}", "MANIFEST", canonical_path=path)
        manifest_nodes[path] = mn
        edge(file_nodes[path], mn, "OWNS")
        data = load(root / path)
        for comp in data.get("components", []):
            filename = comp.get("filename")
            matches = basename_to_paths.get(filename, [])
            if len(matches) != 1:
                errors.append(f"MANIFEST_COMPONENT_RESOLUTION:{path}:{filename}:{len(matches)}")
                continue
            cp = matches[0]
            cn = node(f"PROFILE_PACKAGE_COMPONENT::{cp}", "PROFILE_PACKAGE_COMPONENT", canonical_path=cp, status=comp.get("status"), availability_state=comp.get("availability_state"))
            edge(mn, cn, "PACKAGES")
            edge(cn, file_nodes[cp], "SERIALIZES")

    # Specialist index must resolve exactly to on-disk manifests.
    indexed_manifest_paths = set()
    for entry in index.get("entries", []):
        pid = entry.get("package_identity")
        mf = entry.get("manifest_filename")
        en = node(f"CATALOG_ENTRY::{pid}", "CATALOG_ENTRY", package_identity=pid, manifest_filename=mf)
        if index_file:
            edge(index_file, en, "OWNS")
        matches = basename_to_paths.get(mf, [])
        if len(matches) != 1:
            errors.append(f"CATALOG_MANIFEST_RESOLUTION:{pid}:{mf}:{len(matches)}")
            continue
        mp = matches[0]
        indexed_manifest_paths.add(mp)
        edge(en, manifest_nodes.get(mp) or node(f"MANIFEST::{mp}", "MANIFEST", canonical_path=mp), "INDEXES")
        if entry.get("executor_component_state") in {"DRAFT", "AVAILABLE_UNVALIDATED", "EXECUTOR_DRAFT_UNVALIDATED"}:
            errors.append(f"CATALOG_EXECUTOR_STALE_DRAFT:{pid}")
    for mp in manifest_paths:
        if mp not in indexed_manifest_paths:
            errors.append(f"ON_DISK_MANIFEST_NOT_INDEXED:{mp}")

    # Behavioral scenario graph.
    for scenario in scenarios.get("scenarios", []):
        sid = scenario.get("scenario_id")
        if not sid:
            errors.append("SCENARIO_WITHOUT_ID")
            continue
        sn = node(f"BEHAVIORAL_SCENARIO::{sid}", "BEHAVIORAL_SCENARIO", surface=scenario.get("surface"))
        if core_file:
            edge(sn, core_file, "VALIDATES")

    # Critical mutation suites are explicit graph nodes.
    for suite, target in [
        ("AIR_FULL_SURFACE_INTEGRITY_MUTATION_SUITE_V1", core_file),
        ("AIR_DURABLE_PROVENANCE_PROVIDER_MUTATION_SUITE_V1", handoff_file),
    ]:
        mn = node(f"MUTATION::{suite}", "MUTATION", suite=suite)
        if target:
            edge(mn, target, "MUTATES_FOR_NEGATIVE_TEST")

    # Supported Handoff migrations.
    migrations = handoff.get("schema_manifest", {}).get("revision_migration_contracts", {})
    for migration_id in migrations:
        mn = node(f"MIGRATION::{migration_id}", "MIGRATION", migration_id=migration_id)
        if handoff_file:
            edge(handoff_file, mn, "OWNS")
            edge(mn, handoff_file, "RESTORES")

    # Single-owner integrity for semantically owned route/formal-object nodes.
    for node_id, owners in ownership.items():
        cls = nodes[node_id].get("node_class")
        if cls in {"ROUTE", "FORMAL_OBJECT"} and len(owners) != 1:
            errors.append(f"CONTRADICTORY_OWNERSHIP:{node_id}:{sorted(owners)}")

    degree = defaultdict(int)
    for e in edges:
        degree[e["from"]] += 1
        degree[e["to"]] += 1
    operative = {"ROUTE", "CONTROL_EVENT", "VALIDATION_CHECK", "BEHAVIORAL_SCENARIO", "MIGRATION", "MANIFEST", "CATALOG_ENTRY"}
    for node_id, attrs in nodes.items():
        if attrs.get("node_class") in operative and degree[node_id] == 0:
            errors.append(f"ORPHAN_OPERATIVE_NODE:{node_id}")

    return {
        "validator_identity": VALIDATOR_IDENTITY,
        "node_class_registry": sorted(NODE_CLASSES),
        "edge_class_registry": sorted(EDGE_CLASSES),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": sorted(nodes.values(), key=lambda x: x["node_id"]),
        "edges": sorted(edges, key=lambda x: (x["from"], x["edge_class"], x["to"])),
        "errors": errors,
        "decision": "PASS" if not errors else "FAIL",
        "positive_execution_authority": "NONE",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--write-graph")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    report = build_graph(Path(args.root).resolve())
    if args.write_graph:
        Path(args.write_graph).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        print(f"{report['decision']} {VALIDATOR_IDENTITY}: nodes={report['node_count']} edges={report['edge_count']} errors={len(report['errors'])}")
        for error in report["errors"]:
            print(f"- {error}")
    return 0 if report["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
