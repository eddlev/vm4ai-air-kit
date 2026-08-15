# AIR test reproducibility harness

This harness provides external executable evidence for claims that AIR classifies as `REPRODUCIBLE_EXECUTABLE`.

It does **not** make model inference deterministic. Model- or judge-dependent evaluations remain `REPLAYABLE_EVALUATION` and must report their recorded inputs, procedure, model/tool identity when available, and stability across repeated runs.

## Release-grade executable check

The GitHub Actions workflow runs the same manifest in three separate Docker containers with:

- the repository mounted read-only
- network disabled with Docker `--network none`
- `TZ=UTC`
- stable locale settings
- `PYTHONHASHSEED=0`
- an explicit AIR test seed
- one resolved container image identity reused for all three executions

Each run produces a run record with suite and input hashes, source revision, runner/runtime/environment identity, per-test results, and a decision fingerprint. `air_test_compare.py` issues `DETERMINISTIC_CONFIRMED` only when all required runs pass and their identities and decision fingerprints agree.

If they diverge, the harness exits non-zero and reports `FLAKY_OR_NONDETERMINISTIC`.

## Local use

Run the suite in an isolated environment three times, then compare the run records:

```bash
python tests/air_test_runner.py --manifest tests/air-test-manifest.json --output run-1.json --run-index 1
python tests/air_test_runner.py --manifest tests/air-test-manifest.json --output run-2.json --run-index 2
python tests/air_test_runner.py --manifest tests/air-test-manifest.json --output run-3.json --run-index 3
python tests/air_test_compare.py --runs run-1.json run-2.json run-3.json --output determinism-report.json --required-identical-runs 3
```

A local run without enforced network isolation or a recorded immutable environment may still be useful, but it must preserve that reproducibility limitation and should not be presented as hermetic release evidence.

## Claim boundary

A green harness result proves only the checks that actually ran against the recorded inputs and environment. It does not prove untested intent, hidden reasoning, external side effects, regulatory conformity, or semantic correctness beyond the test definitions.
