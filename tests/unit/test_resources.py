from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from vm4ai_air.errors import ResourceError, ResourceIntegrityError
from vm4ai_air.paths import AppPaths
from vm4ai_air.resources import ResourceResolver
from vm4ai_air.resources.build import (
    BUNDLES_NAME,
    MANIFEST_NAME,
    build_bundle_definitions,
    build_manifest,
    write_generated_metadata,
)
from vm4ai_air.version import __version__

ROOT = Path(__file__).resolve().parents[2]


def test_manifest_covers_complete_canonical_surface() -> None:
    manifest = build_manifest(ROOT, __version__)
    paths = {item["relative_path"] for item in manifest["resources"]}
    assert manifest["resource_count"] == len(paths)
    assert "prompts/AIR CORE RUNTIME.md" in paths
    assert "profiles/grounding specialist/AIR GROUNDING SPECIALIST.json" in paths
    assert "runtime/boot/AIR BOOT MODULE MANIFEST.json" in paths
    assert manifest["source_tree_digest"].startswith("sha256:")


def test_complete_air_prompt_set_bundle_is_explicit() -> None:
    manifest = build_manifest(ROOT, __version__)
    bundles = build_bundle_definitions(manifest)
    complete = next(item for item in bundles["bundles"] if item["bundle_id"] == "COMPLETE_AIR_PROMPT_SET")
    assert complete["display_name"] == "Complete AIR Prompt Set"
    assert len(complete["resources"]) == 3


def test_generated_metadata_and_source_override_resolver(tmp_path: Path) -> None:
    output = tmp_path / "generated"
    write_generated_metadata(ROOT, output, __version__)
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


def test_canonical_resource_path_still_resolves(tmp_path: Path) -> None:
    environment = {"AIR_HOME": str(tmp_path / "home"), "AIR_RESOURCE_ROOT": str(ROOT)}
    resolver = ResourceResolver.from_environment(environment=environment, paths=AppPaths.resolve(environment))
    record = resolver.resolve("prompts/AIR CORE RUNTIME.md")
    assert record["relative_path"] == "prompts/AIR CORE RUNTIME.md"


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
    assert result["receipt"]["source_sha256"] == hashlib.sha256(materialized.read_bytes()).hexdigest()


def test_materialization_refuses_corrupted_source_bytes(tmp_path: Path) -> None:
    manifest = build_manifest(ROOT, __version__)
    record = next(item for item in manifest["resources"] if item["relative_path"] == "prompts/AIR CORE RUNTIME.md")
    source = tmp_path / record["relative_path"]
    source.parent.mkdir(parents=True)
    source.write_bytes(b"corrupted resource bytes")
    paths = AppPaths.resolve({"AIR_HOME": str(tmp_path / "air-home")})
    resolver = ResourceResolver(tmp_path, manifest, origin="TEST", paths=paths)

    assert resolver.verify(record["relative_path"])["decision"] == "FAIL"
    with pytest.raises(ResourceIntegrityError, match="Refusing to materialize corrupted AIR resource"):
        resolver.materialize(record["relative_path"], purpose="must-fail")
    assert not paths.materialized_resources_root.exists()


def test_manifest_rejects_path_traversal(tmp_path: Path) -> None:
    manifest = build_manifest(ROOT, __version__)
    manifest["resources"][0]["package_path"] = "../outside.txt"
    with pytest.raises(ResourceIntegrityError, match="Unsafe resource manifest path"):
        ResourceResolver(tmp_path, manifest, origin="TEST", paths=AppPaths.resolve({"AIR_HOME": str(tmp_path)}))


@pytest.mark.parametrize(
    "field",
    ["schema_version", "canonical_roots", "authoring_release_line", "resource_set_version", "source_tree_digest"],
)
def test_manifest_requires_aggregate_identity_fields(tmp_path: Path, field: str) -> None:
    manifest = build_manifest(ROOT, __version__)
    manifest.pop(field)
    with pytest.raises(ResourceIntegrityError):
        ResourceResolver(tmp_path, manifest, origin="TEST", paths=AppPaths.resolve({"AIR_HOME": str(tmp_path)}))


def test_manifest_recomputes_aggregate_identity(tmp_path: Path) -> None:
    manifest = build_manifest(ROOT, __version__)
    manifest["resources"][0]["sha256"] = "0" * 64
    with pytest.raises(ResourceIntegrityError, match="aggregate source-tree digest"):
        ResourceResolver(tmp_path, manifest, origin="TEST", paths=AppPaths.resolve({"AIR_HOME": str(tmp_path)}))


def test_manifest_requires_canonical_resource_id(tmp_path: Path) -> None:
    manifest = build_manifest(ROOT, __version__)
    manifest["resources"][0]["resource_id"] = "air://wrong"
    with pytest.raises(ResourceIntegrityError, match="invalid resource_id"):
        ResourceResolver(tmp_path, manifest, origin="TEST", paths=AppPaths.resolve({"AIR_HOME": str(tmp_path)}))


@pytest.mark.parametrize(
    "identifier",
    [
        "../prompts/AIR CORE RUNTIME.md",
        "/prompts/AIR CORE RUNTIME.md",
        "./prompts/AIR CORE RUNTIME.md",
        r"C:\prompts\AIR CORE RUNTIME.md",
    ],
)
def test_resolver_rejects_unsafe_user_identifiers(tmp_path: Path, identifier: str) -> None:
    environment = {"AIR_HOME": str(tmp_path / "home"), "AIR_RESOURCE_ROOT": str(ROOT)}
    resolver = ResourceResolver.from_environment(environment=environment, paths=AppPaths.resolve(environment))
    with pytest.raises(ResourceError, match="Unsafe AIR resource identifier"):
        resolver.resolve(identifier)
