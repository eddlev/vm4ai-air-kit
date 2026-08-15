from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "prompts/AIR_HANDOFF_CARD_TEMPLATE.json"
MANIFEST = ROOT / "tests/air-test-manifest.json"


def strict_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def replace_once(text, old, new):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected exactly one occurrence of {old!r}; found {count}")
    return text.replace(old, new, 1)


text = HANDOFF.read_text(encoding="utf-8")
text = replace_once(text, '"card_revision": 6,', '"card_revision": 7,')
text = replace_once(text, '"governance_supplement_version": "2.0.0"', '"governance_supplement_version": "2.2.0"')
text = replace_once(text, '"governance_floor_version": "2.0.0"', '"governance_floor_version": "2.1.0"')
text = replace_once(text, '"registry_version": "2.0.0"', '"registry_version": "2.1.0"')
json.loads(text, object_pairs_hook=strict_object)
HANDOFF.write_text(text, encoding="utf-8")

card = json.loads(text, object_pairs_hook=strict_object)["AIR_HANDOFF_CARD"]
assert card["SCHEMA_VERSION"] == "2.2.0"
assert card["schema_version"] == "2.2.0"
assert card["card_revision"] == 7
assert card["profile_stack"]["starter_profile"]["PROMPT_VERSION"] == "2.4.1"
gov = card["governance_state"]
assert gov["governance_supplement_designation"] == "AIR_HR_GOVERNANCE_SUPPLEMENT_V2"
assert gov["governance_supplement_version"] == "2.2.0"
assert gov["governance_floor_version"] == "2.1.0"
assert gov["floor_invariant_reference"]["registry_version"] == "2.1.0"

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"), object_pairs_hook=strict_object)
if "prompts/AIR_GOV.md" not in manifest["material_inputs"]:
    manifest["material_inputs"].append("prompts/AIR_GOV.md")

new_tests = [
    {
        "id": "AIR-HANDOFF-GOV-001",
        "type": "text_contains",
        "path": "prompts/AIR_GOV.md",
        "text": "PROMPT_VERSION: 2.2.0",
        "requirement": "Governance Supplement identity is pinned as a material compatibility input."
    },
    {
        "id": "AIR-HANDOFF-GOV-002",
        "type": "text_contains",
        "path": "prompts/AIR_GOV.md",
        "text": "- governance_floor_version = 2.1.0",
        "requirement": "Governance declares the current handoff governance floor version."
    },
    {
        "id": "AIR-HANDOFF-GOV-003",
        "type": "text_contains",
        "path": "prompts/AIR_GOV.md",
        "text": "- registry_version = 2.1.0",
        "requirement": "Governance declares the current canonical floor registry version."
    },
    {
        "id": "AIR-HANDOFF-GOV-004",
        "type": "json_value_equals",
        "path": "prompts/AIR_HANDOFF_CARD_TEMPLATE.json",
        "json_path": "AIR_HANDOFF_CARD.governance_state.governance_supplement_version",
        "expected": "2.2.0",
        "requirement": "Handoff serialized Governance Supplement version matches the current supplement."
    },
    {
        "id": "AIR-HANDOFF-GOV-005",
        "type": "json_value_equals",
        "path": "prompts/AIR_HANDOFF_CARD_TEMPLATE.json",
        "json_path": "AIR_HANDOFF_CARD.governance_state.governance_floor_version",
        "expected": "2.1.0",
        "requirement": "Handoff serialized governance floor matches the current Governance carrier shape."
    },
    {
        "id": "AIR-HANDOFF-GOV-006",
        "type": "json_value_equals",
        "path": "prompts/AIR_HANDOFF_CARD_TEMPLATE.json",
        "json_path": "AIR_HANDOFF_CARD.governance_state.floor_invariant_reference.registry_version",
        "expected": "2.1.0",
        "requirement": "Handoff serialized floor registry version matches current Governance."
    },
    {
        "id": "AIR-HANDOFF-GOV-007",
        "type": "json_value_equals",
        "path": "prompts/AIR_HANDOFF_CARD_TEMPLATE.json",
        "json_path": "AIR_HANDOFF_CARD.card_revision",
        "expected": 7,
        "requirement": "Template revision advances for the corrected serialized defaults without changing Handoff schema identity."
    }
]
existing = {test["id"] for test in manifest["tests"]}
for test in new_tests:
    if test["id"] in existing:
        raise RuntimeError(f"test already exists: {test['id']}")
    manifest["tests"].append(test)
MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

subprocess.run([
    "python", "tests/air_test_runner.py",
    "--manifest", "tests/air-test-manifest.json",
    "--output", "/tmp/group2-precheck.json",
    "--run-index", "1"
], cwd=ROOT, check=True)

subprocess.run(["git", "config", "user.name", "AIR repair workflow"], cwd=ROOT, check=True)
subprocess.run(["git", "config", "user.email", "actions@users.noreply.github.com"], cwd=ROOT, check=True)
subprocess.run(["git", "rm", ".github/group2_patch.py", ".github/workflows/group2-handoff-fix.yml"], cwd=ROOT, check=True)
subprocess.run(["git", "add", "prompts/AIR_HANDOFF_CARD_TEMPLATE.json", "tests/air-test-manifest.json"], cwd=ROOT, check=True)
subprocess.run(["git", "commit", "-m", "Group 2: align Handoff governance defaults"], cwd=ROOT, check=True)
subprocess.run(["git", "push", "origin", "HEAD"], cwd=ROOT, check=True)
