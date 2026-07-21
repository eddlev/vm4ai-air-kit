# AIR Release Process

## Development line

The installable runtime is currently `0.4.0.dev0`. It is not a public release.

## Required pre-release evidence

Before a release candidate may advance:

1. pin the repository base commit;
2. build wheel and source distribution once;
3. validate package metadata;
4. inspect embedded canonical resources and generated manifest;
5. install the wheel in a fresh environment outside the repository;
6. run cross-platform source, integration, and package tests;
7. complete modular boot, Q1-D, handoff, signature, policy, upgrade, rollback, and cross-model stages;
8. reconcile every deliberate deferral;
9. obtain explicit release approval.

## Workflow separation

- `ci.yml` runs source and integration tests across supported operating systems and Python versions.
- `package.yml` builds and validates distributions, runs isolated installed-wheel tests, and smoke-tests pipx installation.
- A publishing workflow does not exist yet and may not be added or enabled without separate approval.

## Future publishing

The approved target is GitHub Actions with PyPI Trusted Publishing and short-lived OIDC credentials. No password or long-lived publishing token should be stored in the repository.

Trusted Publisher configuration, package-name creation, publication, tag, GitHub release, and public announcement remain separate approval gates.

## Claim boundary

A built artifact, metadata pass, signature, provenance attestation, or successful command is not proof of semantic completeness, universal compatibility, security, or authorization to publish.
