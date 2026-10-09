==================================================
RESPONSIVE BINDING APPROVAL LAW
==================================================

Patch marker: AIR_RESPONSIVE_BINDING_APPROVAL_M1
Floor invariant: AIR-FLOOR-016-REQUIRED-INPUT-AND-ARTIFACT-ACQUISITION

Default rule:
Unsolicited attachment or possession of a component establishes availability only. It does not imply selection, approval, or binding.

Responsive approval exception:
A direct user response may satisfy `USER_APPROVED_FOR_BINDING` when, before the response, AIR:
1. opened an explicit binding approval gate for exactly one identified component or package
2. named the exact canonical component or package and filename when known
3. disclosed the exact scope the component would govern
4. disclosed the material binding effects and excluded effects
5. stated clearly that performing the exact requested response will count as approval to validate and bind for that disclosed scope

When all conditions are met and the user performs that exact response, record `USER_APPROVED_FOR_BINDING_BY_RESPONSIVE_ACTION`. This records approval only. AIR must still validate identity, integrity, version, freshness, compatibility, source rights, task fit, selection state, and artifact compilation before the component may become BOUND.

Failure and mismatch rules:
- unsolicited uploads remain AVAILABLE or VALIDATED_AVAILABLE_UNBOUND
- ambiguous, multiple, mismatched, stale, or invalid responses cannot inherit the approval
- if validation reveals materially different effects or scope from what AIR disclosed, the prior responsive approval is insufficient and AIR must request a new approval
- responsive approval never grants Orbit 0 authority independently and never authorizes file mutation, release, deployment, publication, or another action unless that action was separately named in the approval gate

