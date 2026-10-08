from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(".").resolve()
VAL = ROOT / "tools" / "validate_air_v081_repository.py"
PYTHON = sys.executable


def run(root: Path) -> int:
    return subprocess.run([PYTHON, str(VAL), str(root), "--quick"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    if run(ROOT) != 0:
        raise SystemExit("v0.8.1 mutation baseline failed")

    cases = []
    def add(name, fn): cases.append((name, fn))

    add("V081-N01-VERSION-ROLLBACK", lambda d: (d / "VERSION").write_text("0.8.0\n", encoding="utf-8"))

    def stale_rev24(d: Path):
        p = d / "source/prompts/AIR_DEFAULT_STARTER_PROFILE.json"; o = load(p)
        o["handoff_contract"]["revision_identity_contract"]["current_template_revision"] = 24; dump(p, o)
    add("V081-N02-STALE-CURRENT-REV24", stale_rev24)

    def drop_tier2_command(d: Path):
        p = d / "source/prompts/AIR_DEFAULT_STARTER_PROFILE.json"; o = load(p)
        m = o["compiler_contract"]["progressive_runtime_retrieval_mirror"]
        m["user_boot_profile_dispatch"]["TIER_2_TARGETED_SOURCE"]["selection_aliases"].remove(m["canonical_first_message_commands"]["explicit_tier2"]); dump(p, o)
    add("V081-N03-DROP-TIER2-CANONICAL-COMMAND", drop_tier2_command)

    def drop_boundary_guard(d: Path):
        p = d / "source/prompts/AIR_DEFAULT_STARTER_PROFILE.json"; o = load(p)
        o["compiler_contract"]["progressive_runtime_retrieval_mirror"].pop("exact_section_boundary_guard"); dump(p, o)
    add("V081-N04-DROP-TIER0-BOUNDARY-GUARD", drop_boundary_guard)

    def core_drift(d: Path):
        p = d / "source/prompts/AIR_CORE_RUNTIME.md"; p.write_bytes(p.read_bytes() + b"\nV081_MUTANT\n")
    add("V081-N05-CANONICAL-SOURCE-DRIFT", core_drift)

    def runtime_drift(d: Path):
        p = d / "air_p/compiled/AIR_P_RUNTIME_REFERENCE_INDEX.json"; p.write_bytes(p.read_bytes() + b"\n")
    add("V081-N06-CHECKED-IN-RUNTIME-DRIFT", runtime_drift)

    def specialist_drift(d: Path):
        p = d / "specialists/grounding/AIR_GROUNDING_SPECIALIST.json"; p.write_bytes(p.read_bytes() + b"\n")
    add("V081-N07-SPECIALIST-CARRY-FORWARD-DRIFT", specialist_drift)

    def profiles_reintroduced(d: Path):
        p = d / "profiles/legacy"; p.mkdir(parents=True); (p / "README.txt").write_text("obsolete\n", encoding="utf-8")
    add("V081-N08-OBSOLETE-PROFILES-REINTRODUCED", profiles_reintroduced)

    def workflow_stale(d: Path):
        p = d / ".github/workflows/air-reproducibility.yml"; p.write_text(p.read_text().replace("python3 tools/validate_air_suite.py", "python3 tools/validate_air_v074_release_seal.py"), encoding="utf-8")
    add("V081-N09-STALE-V074-WORKFLOW", workflow_stale)

    def readme_command_missing(d: Path):
        p = d / "README.md"; p.write_text(p.read_text().replace("Start a new AIR-P project. Tier3 boot.", "Tier3 command removed"), encoding="utf-8")
    add("V081-N10-README-COMMAND-MISSING", readme_command_missing)

    def unmanifested_source_extra(d: Path):
        p = d / "source/UNMANIFESTED.txt"; p.write_text("must fail closure\n", encoding="utf-8")
    add("V081-N11-UNMANIFESTED-SOURCE-EXTRA", unmanifested_source_extra)

    def unmanifested_runtime_extra(d: Path):
        p = d / "air_p/UNMANIFESTED.txt"; p.write_text("must fail closure\n", encoding="utf-8")
    add("V081-N12-UNMANIFESTED-RUNTIME-EXTRA", unmanifested_runtime_extra)

    killed = 0
    with tempfile.TemporaryDirectory(prefix="air-v081-mutations-") as td:
        base = Path(td)
        for name, fn in cases:
            dst = base / name
            shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            fn(dst)
            if run(dst) == 0:
                raise SystemExit(f"mutation {name} SURVIVED v0.8.1 repository validator")
            print(f"{name}: KILLED")
            killed += 1
    print(f"AIR v0.8.1 repository mutation suite: PASS ({killed}/{len(cases)} mutants killed)")


if __name__ == "__main__":
    main()
