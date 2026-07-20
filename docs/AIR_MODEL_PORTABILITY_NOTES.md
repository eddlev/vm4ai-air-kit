# AIR Model Portability Notes

AIR is prompt-native and provider-neutral in design, but actual rule following, context loading, tool access, and handoff restoration vary by model and interface.

## Practical guidance

- Prefer modular boot when the monolithic bundle consumes too much context.
- Treat terminal-sentinel checks as end-of-file evidence, not proof that every middle section loaded.
- Verify that Q1 is asked and that onboarding answers are not invented.
- Record model, interface, date, bundle, context condition, and observed failure when reporting portability issues.
- Do not generalize one successful boot into a permanent compatibility claim.

## Fallback

When a host cannot reliably load the selected bundle, reduce the module set or use a different capable host. Preserve project state with a handoff card, but keep structural and cryptographic trust states distinct.
