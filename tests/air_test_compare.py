#!/usr/bin/env python3
"""Compare independent AIR executable test runs and issue a deterministic claim only when justified."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--required-identical-runs", type=int, default=3)
    args = parser.parse_args()

    runs = [json.loads(Path(p).read_text(encoding="utf-8")) for p in args.runs]
    if len(runs) < args.required_identical_runs:
        raise SystemExit("insufficient independent runs for deterministic release-grade claim")

    suite_ids = {r["suite_id"] for r in runs}
    suite_hashes = {r["suite_sha256"] for r in runs}
    input_hashes = {r["fixture_set_sha256"] for r in runs}
    env_fingerprints = {r["environment_fingerprint"] for r in runs}
    decision_fingerprints = [r["decision_fingerprint"] for r in runs]
    all_pass = all(r["decision"] == "PASS" for r in runs)
    identities_match = len(suite_ids) == len(suite_hashes) == len(input_hashes) == len(env_fingerprints) == 1
    decisions_identical = len(set(decision_fingerprints)) == 1
    network_enforced = all(r.get("network_policy") == "DISABLED_ENFORCED_DOCKER" for r in runs)

    unstable = []
    by_id = {}
    for r in runs:
        for t in r["per_test_results"]:
            by_id.setdefault(t["id"], []).append((t["decision"], t.get("observed")))
    for test_id, values in sorted(by_id.items()):
        if len({json.dumps(v, sort_keys=True, ensure_ascii=False) for v in values}) > 1:
            unstable.append(test_id)

    deterministic = all_pass and identities_match and decisions_identical and network_enforced and not unstable
    state = "DETERMINISTIC_CONFIRMED" if deterministic else "FLAKY_OR_NONDETERMINISTIC"
    combined_payload = {
        "suite_id": next(iter(suite_ids)) if len(suite_ids) == 1 else sorted(suite_ids),
        "suite_sha256": next(iter(suite_hashes)) if len(suite_hashes) == 1 else sorted(suite_hashes),
        "fixture_set_sha256": next(iter(input_hashes)) if len(input_hashes) == 1 else sorted(input_hashes),
        "environment_fingerprint": next(iter(env_fingerprints)) if len(env_fingerprints) == 1 else sorted(env_fingerprints),
        "decision_fingerprints": decision_fingerprints,
        "unstable_test_ids": unstable,
        "state": state
    }
    report = {
        "record_schema_version": "1.0.0",
        "reproducibility_class": "REPRODUCIBLE_EXECUTABLE",
        "reproducibility_state": state,
        "required_independent_runs": args.required_identical_runs,
        "observed_run_count": len(runs),
        "all_runs_passed": all_pass,
        "run_identities_match": identities_match,
        "decision_fingerprints_identical": decisions_identical,
        "network_isolation_enforced": network_enforced,
        "unstable_test_ids": unstable,
        "run_ids": [r["run_id"] for r in runs],
        "decision_fingerprints": decision_fingerprints,
        "result_fingerprint": sha256_bytes(canonical_json(combined_payload)),
        "claim": (
            f"{runs[0]['tests_passed']}/{runs[0]['tests_total']} PASS — REPRODUCIBLE_EXECUTABLE — "
            f"{len(runs)}/{len(runs)} isolated executions identical"
            if deterministic
            else "REPRODUCIBILITY_FAILURE — do not report a deterministic pass claim"
        ),
        "claim_boundary": "Deterministic confirmation applies only to the executable definitions, inputs, environment identity, and observations represented by these runs."
    }
    Path(args.output).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(report["claim"])
    return 0 if deterministic else 1


if __name__ == "__main__":
    raise SystemExit(main())
