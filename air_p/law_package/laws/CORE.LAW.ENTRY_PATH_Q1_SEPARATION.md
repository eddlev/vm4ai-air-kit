==================================================
ENTRY LAW
==================================================

Patch marker: AIR_ENTRY_PATH_Q1_SEPARATION_V1

Detect which entry path applies. Entry-path selection is not onboarding-answer selection.

Use FIRST ACTIVATION FLOW if the user indicates:
- start a new AIR project
- start onboarding
- new project
- import project
- adapt this project to AIR
- or equivalent first-start intent

This sets only entry_path. It leaves Q1 = UNANSWERED and current_onboarding_question = Q1.

Use HANDOFF CONTINUATION FLOW only when a valid AIR_HANDOFF_CARD is supplied or the user explicitly selects the continuation route.

If both fresh-start intent and a valid handoff are present, ask which route the user wants unless the user explicitly resolves the conflict. Do not silently convert route selection into Q1=A/B/C/D.

