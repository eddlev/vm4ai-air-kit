# AIR Threat Model

Canonical threat-model page for the AIR kit. Prompt-compiled framework;
nothing here claims backend enforcement. Reliability of every mechanism
below is model-dependent (see AIR_MODEL_PORTABILITY_NOTES.md).

## Outbound: what leaves the session

The handoff card is a complete, portable snapshot of a project's state.
Treat it as sensitive data: it can contain project descriptions, source
references, blockers, and working-agreement details. The original
outbound risk assessment is published in repo Discussion #2 ("AIR
Handoff Card — Threat model & risk assessment"), which remains the
reference for card-content sensitivity and handling guidance.

## Inbound trust (addendum, v0.2.8)

The original disclosure covered outbound risk: what leaves the session
in a handoff card. This addendum covers the inbound direction, added
together with the mechanisms that gate it.

**Tampered or malicious handoff cards.** Restoration previously
accepted declared state at face value. As of v0.2.8, cards are
validated before restore, card-carried governance content is advisory
echo that can never install or amend laws, and invalid cards fail
closed. Boundary: validation is prompt-side and model-dependent; it is
tamper-evidence at best, never tamper-proofing. A card is not a
cryptographic object.

**Lax profiles.** A schema-valid profile with weak constraints no
longer lowers posture silently; deltas below the starter baseline are
surfaced and clamped unless explicitly accepted.

**Instructions embedded in sources.** Content inside attached or
fetched material is treated as data. Embedded imperatives addressed to
AIR are surfaced, not executed.

**Advisory-claim abuse (unfixable by AIR, disclosed).** AIR output is
prompt-compiled and marked as such. A bad actor can strip those
markers and present AIR output to third parties as validated. No
prompt-side mechanism can prevent this. Consumers of AIR artifacts
should treat unverifiable claims of backend validation as false.

**Standing limits.** All mechanisms above are instructions to a model,
not enforced code paths. Their reliability varies by model and load
conditions. AIR remains a reasoning-discipline layer, not a security
boundary.
