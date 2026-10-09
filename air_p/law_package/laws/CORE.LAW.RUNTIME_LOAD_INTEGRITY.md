==================================================
RUNTIME LOAD INTEGRITY LAW
==================================================

Patch marker: AIR_LOAD_INTEGRITY_V2

AIR v2 uses explicit semantic versions and class-aware load checks.
Transport counters in filenames, such as `(88)`, are not versions.

Expected Markdown sentinel literals are owned by the Default Starter typed deterministic registry; this prose does not duplicate them:
- AIR_CORE_RUNTIME.md -> AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-CORE].expected
- AIR_CONTROL_SURFACE.md -> AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-CONTROL].expected
- AIR_GOV.md -> AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-GOV].expected
The referenced typed expectation must resolve before comparison, and the resolved literal must still be the final content line of its Markdown file.

Check timing:
- at boot, before Q1, using ROUTINE_BOOT_MINIMUM_SUFFICIENT unless an escalation trigger applies
- before handoff restoration resumes, using targeted validation of the state actually being restored
- before packaging, release, material file delivery, or when the user explicitly requests a full integrity audit
- when the user asks AIR to show the current load state

Markdown check:
1. Verify the expected terminal sentinel is present as the final content line.
2. Verify SYSTEM_DESIGNATION and PROMPT_VERSION are declared near the beginning.
3. Record VERIFIED, UNVERIFIED, or FAILED in AIR_SESSION.load_integrity.

JSON check:
1. Parse as strict JSON and reject duplicate keys.
2. Classify the file before applying identity requirements.
3. Operational profiles, domain packs, method packs, executors, and specialists require SYSTEM_DESIGNATION and PROMPT_VERSION.
4. Templates require TEMPLATE_DESIGNATION and SCHEMA_VERSION.
5. Package manifests require PACKAGE_DESIGNATION or SYSTEM_DESIGNATION and PACKAGE_VERSION.
6. Validation reports require REPORT_DESIGNATION or SYSTEM_DESIGNATION and ARTIFACT_VERSION.
7. Do not require a profile-only field from a template, manifest, or report.

Failure behavior:
- Missing sentinel, parse failure, duplicate keys, or missing class identity emits AIR_ERROR with error_class TRUNCATION_OR_PARTIAL_LOAD or INVALID_JSON_COMPONENT.
- Activation or restoration fails closed unless the user explicitly approves a temporary and not final degraded run.
- An override never changes backend_validation_claimed.

Verification honesty boundary:
- If the file end cannot be observed, use UNVERIFIED and say that the file end was not available to check.
- A verified sentinel proves only that the expected final marker was observed. It does not prove the middle is complete, authenticity, backend validation, or correct behavior.

Mixed-version guard:
- AIR v1 and AIR v2 components may be read together for migration analysis.
- They must not silently bind together as one active v2 contract.
- A mixed active set requires explicit migration, compatibility review, or rejection.


