# Reporting AIR Bugs and Behavioral Regressions

Thank you for testing AIR.

## Use GitHub Issues for reproducible bugs

A strong AIR bug report should include:

- **AIR version / release tag**
- **Provider and model**
- **Host/platform** (ChatGPT, Claude, Gemini, local runtime, API harness, etc.)
- **Environment notes** (memory available/disabled, browser/network policy, relevant tools/connectors)
- **Exact reproduction steps**
- **Expected AIR behavior**
- **Observed behavior**
- **Visible AIR output**, especially formal AIR objects when relevant
- **Attachments or handoff card**, if the defect concerns continuation/restoration
- **Reproducibility**: once, intermittent, or consistently reproducible

Please redact secrets, credentials, private source material, and personal data before posting.

## Use GitHub Discussions for

- usage questions,
- design discussion,
- feature ideas,
- integration experiences,
- portability observations,
- and behavior that is interesting but not yet a reproducible defect.

## Security-sensitive findings

Do **not** post exploitable security details in a public issue or discussion.

Use the repository's private vulnerability/security reporting mechanism where one is enabled. If no private path is currently configured, contact the maintainer through an existing private project channel before public disclosure.

## What happens after a report

AIR development favors a short feedback loop:

1. reproduce or classify the report;
2. identify the affected semantic/runtime contract;
3. patch the smallest correct surface;
4. add or update a regression case;
5. run change-sensitive validation;
6. publish a preview patch when the evidence supports it.
