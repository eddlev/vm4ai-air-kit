#!/usr/bin/env python3
"""Mutation checks for AIR cross-file contract graph validation."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(".").resolve()
PY = sys.executable


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run(root: Path) -> int:
    return subprocess.run(
        [PY, "tools/validate_air_cross_file_contract_graph.py", "--root", "."],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode


def mutate_route_event_orphan(root: Path) -> None:
    p = root / "catalog/AIR_RUNTIME_ROUTE_MAP.json"
    o = load(p)
    next(r for r in o["routes"] if r["route_id"] == "RT.ACTIVATE")["control_event_ref"] = "CE-DOES-NOT-EXIST"
    save(p, o)


def mutate_event_route_orphan(root: Path) -> None:
    p = root / "prompts/AIR_DEFAULT_STARTER_PROFILE.json"
    o = load(p)
    next(e for e in o["compiler_contract"]["runtime_control_event_registry"]["events"] if e["route_id"] == "RT.ACTIVATE")["route_id"] = "RT.DOES_NOT_EXIST"
    save(p, o)


def mutate_unindex_manifest(root: Path) -> None:
    p = root / "catalog/AIR_SPECIALIST_PACKAGE_INDEX.json"
    o = load(p)
    o["entries"] = [e for e in o["entries"] if e["manifest_filename"] != "AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json"]
    save(p, o)


def mutate_manifest_component(root: Path) -> None:
    p = root / "profiles/grounding specialist/AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json"
    o = load(p)
    o["components"][0]["filename"] = "DOES_NOT_EXIST.json"
    save(p, o)


def mutate_route_owner(root: Path) -> None:
    p = root / "catalog/AIR_RUNTIME_ROUTE_MAP.json"
    o = load(p)
    next(r for r in o["routes"] if r["route_id"] == "RT.ACTIVATE")["semantic_owner"] = "AIR_CONTROL_SURFACE"
    save(p, o)


def mutate_executor_catalog_state(root: Path) -> None:
    p = root / "catalog/AIR_SPECIALIST_PACKAGE_INDEX.json"
    o = load(p)
    e = next(e for e in o["entries"] if e["manifest_filename"] == "AIR_GROUNDING_SPECIALIST_PACKAGE_MANIFEST.json")
    e["executor_component_state"] = "AVAILABLE_UNVALIDATED"
    save(p, o)


MUTATIONS = [
    ("route_event_orphan", mutate_route_event_orphan),
    ("event_route_orphan", mutate_event_route_orphan),
    ("unindexed_manifest", mutate_unindex_manifest),
    ("manifest_component_orphan", mutate_manifest_component),
    ("route_owner_escape", mutate_route_owner),
    ("executor_catalog_state_mismatch", mutate_executor_catalog_state),
]


def main() -> int:
    if run(ROOT) != 0:
        raise SystemExit("cross-file graph mutation baseline failed")
    killed = 0
    for name, mutate in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix="air-graph-mut-") as td:
            dst = Path(td) / "repo"
            shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            mutate(dst)
            if run(dst) == 0:
                raise SystemExit("MUTATION SURVIVED: " + name)
            killed += 1
            print("KILLED", name)
    print(f"AIR cross-file contract graph mutation suite: PASS ({killed}/{len(MUTATIONS)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
