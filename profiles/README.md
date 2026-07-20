# AIR Specialist Packages

Each specialist has one dedicated folder under `profiles/<specialist name>/`.

A complete specialist package contains four functional components:

1. **Specialist profile** — capability posture, rubric, blocking conditions and review behavior.
2. **Domain pack** — terminology, source expectations, domain constraints and failure modes.
3. **Method** — reusable procedure and evidence-to-advance gates.
4. **Executor** — bounded callable operation contract. It is not an autonomous agent and gains no authority from the folder or name.

Each folder also contains an `AIR SPECIALIST PACKAGE MANIFEST.json` that records component roles and hashes. Package membership does not bind the specialist or authorize execution.
