# AIR Starter Version Consistency Hotfix

Generated: 2026-08-04T20:49:00+02:00

## Defect

`AIR_DEFAULT_STARTER_PROFILE.json` declared `PROMPT_VERSION` `2.1.0` while `validation_contract.required_version` remained `2.0.0`. Normal boot therefore correctly failed load-integrity validation before onboarding.

## Correction

- Starter version advanced to `2.1.1`.
- `validation_contract.required_version` advanced to `2.1.1`.
- `required_version_source = TOP_LEVEL_PROMPT_VERSION` and an explicit equality rule were added.
- Boot regression cases were added for current-version acceptance, mismatch rejection, and transport-counter handling.
- Exact Starter hash references were refreshed through all three specialist packages.
- Package integration versions advanced to `2.2.1` only for components whose bytes changed.

## Boundary

No Core, Control Surface, Governance Supplement, or Handoff Template behavior changed. No specialist functional doctrine changed. Package component changes outside the Starter are exact identity and integration metadata refreshes only.

## Validation

166/166 summary-mode checks passed.
