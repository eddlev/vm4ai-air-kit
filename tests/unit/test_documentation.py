from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ACTION = re.compile(r"uses:\s+[^@\s]+@([0-9a-f]{40})(?:\s|$)")


def test_relative_markdown_links_exist() -> None:
    files = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
    missing: list[str] = []
    for document in files:
        text = document.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = raw.split("#", 1)[0].strip()
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (document.parent / target).resolve()
            if not resolved.exists():
                missing.append(f"{document.relative_to(ROOT)} -> {raw}")
    assert not missing, "Missing documentation links:\n" + "\n".join(missing)


def test_user_facing_documentation_uses_complete_prompt_set_term() -> None:
    files = [
        ROOT / "README.md",
        ROOT / "runtime" / "README.md",
        ROOT / "examples" / "README.md",
        *sorted((ROOT / "docs").rglob("*.md")),
    ]
    offenders = [
        str(path.relative_to(ROOT))
        for path in files
        if re.search(r"\bmonolithic\b", path.read_text(encoding="utf-8"), flags=re.IGNORECASE)
    ]
    assert not offenders, f"Legacy user-facing terminology remains in: {offenders}"


def test_github_actions_are_pinned_and_no_publish_workflow_exists() -> None:
    workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    assert {path.name for path in workflows} == {"ci.yml", "package.yml"}
    for workflow in workflows:
        text = workflow.read_text(encoding="utf-8")
        uses_lines = [line for line in text.splitlines() if "uses:" in line]
        assert uses_lines
        assert len(ACTION.findall(text)) == len(uses_lines), f"Unpinned action in {workflow.name}"
        assert "pypi" not in workflow.name.casefold()
        assert "pypa/gh-action-pypi-publish" not in text


def test_package_version_has_one_source_and_ci_discovers_artifacts() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert "version" not in pyproject["project"]
    assert "version" in pyproject["project"]["dynamic"]
    assert pyproject["tool"]["hatch"]["version"]["path"] == "src/vm4ai_air/version.py"

    package_workflow = (ROOT / ".github" / "workflows" / "package.yml").read_text(encoding="utf-8")
    assert "0.4.0.dev0" not in package_workflow
    assert "AIR_TEST_DIST_DIR" in package_workflow


def test_ci_does_not_duplicate_feature_branch_push_and_pr_runs() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert '"feature/**"' not in workflow
    assert "pull_request:" in workflow
    assert "- main" in workflow


def test_historical_release_manifest_remains_valid() -> None:
    import hashlib
    import json

    manifest_path = ROOT / "release" / "v0.3.0" / "REPOSITORY_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    release_note = next(item for item in manifest["entries"] if item["path"] == "release/v0.3.0/RELEASE_NOTES.md")
    observed = hashlib.sha256((ROOT / release_note["path"]).read_bytes()).hexdigest()
    assert observed == release_note["sha256"]
