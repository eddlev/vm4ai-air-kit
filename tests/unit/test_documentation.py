from __future__ import annotations

import re
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
