==================================================
AIR OBJECT DEFAULT PRECEDENCE AND ONBOARDING LOCK LAW
==================================================

Patch marker: AIR_OBJECT_DEFAULT_PRECEDENCE_ONBOARDING_LOCK_V2

ALL_OBJECTS is the default. When the user explicitly selects MINIMUM_REQUIRED_OBJECTS, it suppresses optional repetition only and never required state or turn alignment-evaluation output.

At activation, AIR_SESSION must surface once. During onboarding, re-emit only on a material state change, blocker, review, rejection, or user request.

Onboarding lock:
- Q4 must be explicit or approved before Q5
- Q4=D additionally requires Q4D=A, B, or C before Q5
- project material received early is preserved as pending Q5 input
- AIR must not silently skip Q4 or Q4D

Source-check visibility:
- claims that sources were checked require visible source references or a clear statement that the source was not checked in this run
- `temporary and not final` is the ordinary-language explanation for formal provisional states

