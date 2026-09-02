# AIR test reproducibility harness

This harness provides executable evidence for repository/static claims classified as `REPRODUCIBLE_EXECUTABLE`.

The current manifest is aligned to **AIR v2.5.0-preview.1**, Foundation 2.5.0 / Governance-Handoff 2.3.0 / Specialist 2.4.0. It checks exact source hashes, strict JSON parsing, and current version/schema/evidence carriers.

It does **not** make model inference deterministic. Model-, judge-, tool-use-, and long-horizon evaluations remain `REPLAYABLE_EVALUATION` and must preserve their run identity, conditions, model/tool provenance when available, results, and reproducibility limits.

## Release channels

Preview releases use this executable/static evidence plus change-sensitive regression checks and targeted behavioral smoke. Stable releases require the broader repeated behavioral gate described in `RELEASE_CHANNEL_POLICY.md`.

## Local preview verification

A normal workstation run can establish that the executable checks pass repeatedly on the same local source and environment. It must **not** be reported as isolated deterministic confirmation unless the environment actually enforces the isolation contract.

```bash
python tests/air_test_runner.py --manifest tests/air-test-manifest.json --output run-1.json --run-index 1
python tests/air_test_runner.py --manifest tests/air-test-manifest.json --output run-2.json --run-index 2
python tests/air_test_runner.py --manifest tests/air-test-manifest.json --output run-3.json --run-index 3
```

For preview staging, require all three runs to pass and require the suite, fixture/input, and decision fingerprints to agree. Record the result as repeated local executable evidence, not as an isolated deterministic release-grade claim.

## Stable / isolated deterministic comparison

`air_test_compare.py` is intentionally stricter. Use it only when the run records truthfully show the required isolated environment, including enforced network isolation:

```bash
python tests/air_test_compare.py --runs run-1.json run-2.json run-3.json --output determinism-report.json --required-identical-runs 3
```

A green executable harness proves only the checks actually run against the recorded inputs/environment. It does not prove deterministic LLM inference, hidden model state, external side effects, universal compatibility, or semantic correctness beyond the test definitions.
