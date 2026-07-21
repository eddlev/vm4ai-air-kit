from __future__ import annotations

import json
from pathlib import Path

from vm4ai_air.paths import AppPaths
from vm4ai_air.resources import ResourceResolver
from vm4ai_air.resources.build import (
    BUNDLES_NAME,
    MANIFEST_NAME,
    build_bundle_definitions,
    build_manifest,
    write_generated_metadata,
)

ROOT = Path(__file__).resolve().parents[2]


def test_manifest_covers_complete_canonical_surface() -> None:
    manifest = build_manifest(ROOT, "0.4.0.dev0")
    paths = {item["relative_path"] for item in manifest["resources"]}
    assert manifest["resource_count"] == len(paths)
    assert "prompts/AIR CORE RUNTIME.md" in paths
    assert "profiles/grounding specialist/AIR GROUNDING SPECIALIST.json" in paths
    assert "runtime/boot/AIR BOOT MODULE MANIFEST.json" in paths
    assert manifest["source_tree_digest"].startswith("sha256:")


def test_complete_air_prompt_set_bundle_is_explicit() -> None:
    manifest = build_manifest(ROOT, "0.4.0.dev0")
    bundles = build_bundle_definitions(manifest)
    complete = next(item for item in bundles["bundles"] if item["bundle_id"] == "COMPLETE_AIR_PROMPT_SET")
    assert complete["display_name"] == "Complete AIR Prompt Set"
    assert len(complete["resources"]) == 3


def test_generated_metadata_and_source_override_resolver(tmp_path: Path) -> None:
    output = tmp_path / "generated"
    write_generated_metadata(ROOT, output, "0.4.0.dev0")
    assert json.loads((output / MANIFEST_NAME).read_text(encoding="utf-8"))["resource_count"] > 50
    assert (output / BUNDLES_NAME).exists()

    environment = {"AIR_HOME": str(tmp_path / "home"), "AIR_RESOURCE_ROOT": str(ROOT)}
    resolver = ResourceResolver.from_environment(
        environment=environment,
        paths=AppPaths.resolve(environment),
    )
    assert resolver.origin == "EXPLICIT_SOURCE_OVERRIDE"
    result = resolver.verify_all()
    assert result["decision"] == "PASS"
    matches = resolver.search("Q1D beginner orientation")
    assert any("AIR CORE RUNTIME.md" in item["relative_path"] for item in matches)


def test_materialization_writes_receipt(tmp_path: Path) -> None:
    environment = {"AIR_HOME": str(tmp_path / "home"), "AIR_RESOURCE_ROOT": str(ROOT)}
    resolver = ResourceResolver.from_environment(
        environment=environment,
        paths=AppPaths.resolve(environment),
    )
    result = resolver.materialize(
        "prompts/AIR CORE RUNTIME.md",
        purpose="unit-test-external-tool-input",
    )
    materialized = Path(result["path"])
    assert materialized.exists()
    assert materialized.parent.joinpath("materialization-receipt.json").exists()


def test_manifest_rejects_path_traversal(tmp_path: Path) -> None:
    manifest = build_manifest(ROOT, "0.4.0.dev0")
    manifest["resources"][0]["package_path"] = "../outside.txt"
    try:
        ResourceResolver(tmp_path, manifest, origin="TEST", paths=AppPaths.resolve({"AIR_HOME": str(tmp_path)}))
    except Exception as exc:
        assert "Unsafe resource manifest path" in str(exc)
    else:
        raise AssertionError("Traversal entry was accepted")
