from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

OLD_FOUNDATION = 'AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005'
NEW_FOUNDATION = 'AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006'
OLD_SET_TOKEN = 'OBJECT_CONTRACT_SET_005'
NEW_SET_TOKEN = 'OBJECT_CONTRACT_SET_006'
HISTORY_KEYS = {
    'source_baseline', 'mainline_release_binding', 't7_change_record',
    'historical_release_catalogs', 'source_candidate_manifest', 'change_history',
    'release_history', 'historical_records',
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old == new:
        return text
    old_n = text.count(old)
    new_n = text.count(new)
    if old_n == 1 and new_n == 0:
        return text.replace(old, new, 1)
    if old_n == 0 and new_n >= 1:
        return text
    raise SystemExit(f'v0.7.2 patch {label}: expected one old or existing new block, old={old_n} new={new_n}')


def replace_literal(text: str, old: str, new: str, label: str, expected_min: int = 1) -> str:
    n = text.count(old)
    if n >= expected_min:
        return text.replace(old, new)
    if new in text:
        return text
    raise SystemExit(f'v0.7.2 patch {label}: missing anchor {old!r}')


def current_transform(obj: Any, path: tuple[str, ...] = ()) -> Any:
    if any(p in HISTORY_KEYS or p.startswith('historical_') for p in path):
        return obj
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out[k] = current_transform(v, path + (str(k),))
        return out
    if isinstance(obj, list):
        return [current_transform(v, path + (str(i),)) for i, v in enumerate(obj)]
    if isinstance(obj, str):
        s = obj.replace(OLD_FOUNDATION, NEW_FOUNDATION)
        s = s.replace(OLD_SET_TOKEN, NEW_SET_TOKEN)
        s = s.replace('ALIGNED_TO_AIR_2_6_0_OBJECT_CONTRACT_SET_005', 'ALIGNED_TO_AIR_2_6_1_OBJECT_CONTRACT_SET_006')
        s = s.replace('OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005', 'OPERATIVE_COMPATIBILITY_AUTHORITY_EXACT_HASH_SET_AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006')
        return s
    return obj


def update_dependency_versions(obj: Any, path: tuple[str, ...] = ()) -> None:
    if any(p in HISTORY_KEYS or p.startswith('historical_') for p in path):
        return
    if isinstance(obj, dict):
        filename = obj.get('filename') or obj.get('canonical_filename')
        if filename == 'AIR_CORE_RUNTIME.md' and 'version' in obj:
            obj['version'] = '2.6.1'
        elif filename == 'AIR_CONTROL_SURFACE.md' and 'version' in obj:
            obj['version'] = '2.6.1'
        elif filename == 'AIR_GOV.md' and 'version' in obj:
            obj['version'] = '2.3.1'
        elif filename == 'AIR_DEFAULT_STARTER_PROFILE.json' and 'version' in obj:
            obj['version'] = '2.6.1'
        elif filename == 'AIR_HANDOFF_CARD_TEMPLATE.json':
            if 'version' in obj:
                obj['version'] = '2.3.0'
            if 'card_revision' in obj:
                obj['card_revision'] = 17
        elif filename == 'AIR_RUNTIME_ROUTE_MAP.json' and 'version' in obj:
            obj['version'] = '1.2.0'
        tv = obj.get('target_foundation_versions')
        if isinstance(tv, dict):
            for k, v in [('core','2.6.1'),('control','2.6.1'),('governance','2.3.1'),('starter','2.6.1'),('handoff_schema','2.3.0')]:
                if k in tv:
                    tv[k] = v
        for k, v in obj.items():
            update_dependency_versions(v, path + (str(k),))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            update_dependency_versions(v, path + (str(i),))


def patch_core(root: Path) -> None:
    p = root / 'prompts/AIR_CORE_RUNTIME.md'
    t = p.read_text(encoding='utf-8')
    t = replace_once(t, 'PROMPT_VERSION: 2.6.0', 'PROMPT_VERSION: 2.6.1', 'Core version')

    old = '''Every open material human-approval scope must declare exactly two operative response tokens derived from approval_scope_id:\n- AIR_APPROVE::<approval_scope_id>\n- AIR_REJECT::<approval_scope_id>\n\nThe approval request must print both tokens. Only an exact declared token resolves the approval scope deterministically. Natural-language assent, refusal, acknowledgement, momentum, or paraphrase may be interpreted conversationally but has no approval/rejection authority; AIR must request one of the exact declared tokens.\n'''
    new = '''Every open material human-approval scope must declare exactly two operative response tokens derived from approval_scope_id:\n- AIR_APPROVE::<approval_scope_id>\n- AIR_REJECT::<approval_scope_id>\n\nApproval-scope identity law:\n- approval_scope_id is a concise unique semantic identifier for the currently open material scope. A revision suffix such as `_V1` is optional and has no authority meaning.\n- every material scope also carries approval_scope_fingerprint = SHA-256 of canonical UTF-8 JSON over exactly: gate_id, exact_gate_question, requested_action, authorized_action_ids, excluded_action_ids, required_evidence, stop_conditions, expiry_or_completion_condition. Object keys are lexicographically sorted; arrays retain declared order unless their owning field is explicitly defined as a set elsewhere.\n- the current approval-scope registry must reject reuse of an approval_scope_id when the canonical material-scope fingerprint differs from the fingerprint previously associated with that id. A materially changed scope must receive a new distinct approval_scope_id.\n- superseded, changed-fingerprint, expired, revoked, completed, rejected, or otherwise non-current scope tokens have no approval authority.\n- restored scopes must revalidate both the exact token pair and approval_scope_fingerprint before approval resolution can consume either token.\n\nThe approval request must print both tokens. Only an exact declared token for the current fingerprint-validated scope resolves the approval scope deterministically. Natural-language assent, refusal, acknowledgement, momentum, or paraphrase may be interpreted conversationally but has no approval/rejection authority; AIR must request one of the exact declared tokens.\n'''
    t = replace_once(t, old, new, 'approval scope identity law')

    old = '''Failure capture triggers include formal validation failure, AIR_ERROR, rejected execution caused by an execution defect, failed benchmark criterion, operator-confirmed execution defect, unexpected/mismatched material effect, regression, or explicit user correction identifying a failed strategy. Root cause, corrective constraint, or applicability must not be invented when evidence is insufficient.\n'''
    new = '''Failure capture triggers include formal validation failure, AIR_ERROR, rejected execution caused by an execution defect, failed benchmark criterion, operator-confirmed execution defect, unexpected/mismatched material effect, regression, explicit user correction identifying a failed strategy, or attempted task/material execution blocked because the exact task-specific Artifact/benchmark/precheck/binding/visible-accounting barrier was not satisfied. Root cause, corrective constraint, or applicability must not be invented when evidence is insufficient.\n\nFailure-capture routing is mandatory for execution-defect rejection. RT.RECOVERY must evaluate whether the evidenced failure meets the reusable-failure trigger contract before ending the response. When it does, construct and visibly emit AIR_FAILURE_MODE_RECORD through the canonical first-emission ledger reservation transaction. When it does not, preserve the failure evidence and reason capture was not applicable; never silently drop an execution-defect rejection.\n'''
    t = replace_once(t, old, new, 'failure capture routing')

    old = '''Canonical deterministic runtime route set for this Foundation candidate:\n- RT.BOOT\n- RT.ONBOARD\n- RT.HANDOFF_RESTORE\n- RT.TURN\n- RT.ALIGN\n- RT.APPROVAL_RESOLVE\n- RT.ACTION\n- RT.RECEIPT\n- RT.HANDOFF_CREATE\n'''
    new = '''Canonical deterministic runtime route set for this Foundation candidate:\n- RT.BOOT\n- RT.ONBOARD\n- RT.HANDOFF_RESTORE\n- RT.TURN\n- RT.ALIGN\n- RT.TASK_SWITCH\n- RT.APPROVAL_RESOLVE\n- RT.ACTION\n- RT.RECEIPT\n- RT.HANDOFF_CREATE\n'''
    t = replace_once(t, old, new, 'deterministic route set')

    old = '''[AIR_ROUTE]\nid=RT.TASK_SWITCH\nsemantic_owner=AIR_CORE_RUNTIME\ntrigger=TASK_OR_STEP_REPLACEMENT classified as new independent task\ntrigger_authority=NON_OPERATIVE_DESCRIPTION\ncontrol_event_ref=CE-RT-TASK_SWITCH\nrequires=DEP.CURRENT_EVALUATION_BASIS;DEP.NEW_TASK_IDENTITY_RESOLVED\nproduces=NEW_TASK_ARTIFACT_CANDIDATE;ORBIT_TRANSITION;AIR_SESSION_WHEN_ORBIT_CHANGED;AIR_PROJECT_EXECUTION_MAP;AIR_ARTIFACT\nallowed_next=RT.CAPABILITY_RESOLVE|RT.COGNITIVE_RESOLVE|RT.MORPHOLOGY_BIND\ninvalidates=PRIOR_TASK_EXECUTION_BINDING_AFTER_ATOMIC_REPLACEMENT\ndoes_not_bypass=DEP.NEW_TASK_ARTIFACT;DEP.ARTIFACT_PRECHECK;AIR-FLOOR-013\ntransition_emission_bundle=ORBIT_TRANSITION_ATOMIC_BUNDLE\ntransition_emission_bundle_members=AIR_SESSION;AIR_PROJECT_EXECUTION_MAP;AIR_ARTIFACT\ntransition_emission_bundle_condition=ORBIT_STATE_CHANGED_OR_TASK_BINDING_CHANGED\ntransition_emission_bundle_atomic=true\nfailure_route=RT.RECOVERY\n'''
    new = '''[AIR_ROUTE]\nid=RT.TASK_SWITCH\nsemantic_owner=AIR_CORE_RUNTIME\nexecution_semantics=DETERMINISTIC_PIPELINE\ninference_policy=PROHIBITED\nstep_order=STRICT\nmissing_input_behavior=FAIL_CLOSED\nunknown_condition_behavior=FAIL_CLOSED\nconflict_behavior=FAIL_CLOSED\ntrigger=TASK_OR_STEP_REPLACEMENT classified as new independent task\ntrigger_authority=NON_OPERATIVE_DESCRIPTION\ncontrol_event_ref=CE-RT-TASK_SWITCH\nrequires=DEP.CURRENT_EVALUATION_BASIS;DEP.NEW_TASK_BOUNDARY_LATCHED;DEP.NEW_TASK_IDENTITY_RESOLVED;DEP.NEW_TASK_ARTIFACT_COMPILED;DEP.NEW_TASK_BENCHMARK_DERIVED;DEP.NEW_TASK_PRECHECK_ADMISSIBLE;DEP.NEW_TASK_BINDING_READY\nproduces=NEW_TASK_ARTIFACT_CANDIDATE;NEW_TASK_BINDING_TRANSACTION_STATE;ORBIT_TRANSITION;AIR_SESSION_WHEN_ORBIT_CHANGED;AIR_PROJECT_EXECUTION_MAP;AIR_ARTIFACT;NEW_TASK_ARTIFACT_VISIBLE_ACCOUNTING_STATE\nallowed_next=RT.CAPABILITY_RESOLVE|RT.COGNITIVE_RESOLVE|RT.MORPHOLOGY_BIND\ninvalidates=PRIOR_TASK_EXECUTION_BINDING_AFTER_ATOMIC_REPLACEMENT\ndoes_not_bypass=DEP.NEW_TASK_ARTIFACT;DEP.ARTIFACT_PRECHECK;DEP.NEW_TASK_ARTIFACT_VISIBLE_ACCOUNTED;AIR-FLOOR-013;AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE;AIR-FLOOR-026-DETERMINISTIC-CONTRACT-MACHINE-REPRESENTATION\ntransaction_contract=AIR_NEW_TASK_BINDING_TRANSACTION_V2\ntransaction_sequence=NEW_TASK_BOUNDARY_LATCHED;COMPILE_EXACT_TASK_ARTIFACT;DERIVE_TASK_BENCHMARK;ARTIFACT_PRECHECK_ADMISSIBLE;ATOMIC_BIND_ORBIT_0;PRIMARY_USER_VISIBLE_ARTIFACT_EMISSION;ARTIFACT_SURFACED_LEDGER_ACCOUNTING;NEW_TASK_EXECUTION_ELIGIBLE\ntransition_emission_bundle=ORBIT_TRANSITION_ATOMIC_BUNDLE\ntransition_emission_bundle_members=AIR_SESSION;AIR_PROJECT_EXECUTION_MAP;AIR_ARTIFACT\ntransition_emission_bundle_condition=ORBIT_STATE_CHANGED_OR_TASK_BINDING_CHANGED\ntransition_emission_bundle_atomic=true\nfailure_route=RT.RECOVERY\n'''
    t = replace_once(t, old, new, 'RT.TASK_SWITCH')

    t = replace_once(
        t,
        'requires=DEP.CURRENT_EVALUATION_BASIS;DEP.ARTIFACT_BOUND;DEP.LEASE_ACTIVE;DEP.SCOPE_MATCH;DEP.APPROVAL_PRECONDITION_SATISFIED;DEP.GATE_ALLOW;DEP.AUTHORITY_LEDGER_COMMITTED\n',
        'requires=DEP.CURRENT_EVALUATION_BASIS;DEP.ARTIFACT_BOUND;DEP.CURRENT_TASK_ARTIFACT_EXACT_MATCH;DEP.CURRENT_ARTIFACT_BENCHMARK_ADMISSIBLE;DEP.CURRENT_ARTIFACT_PRECHECK_ADMISSIBLE;DEP.CURRENT_ARTIFACT_VISIBLE_ACCOUNTED;DEP.LEASE_ACTIVE;DEP.SCOPE_MATCH;DEP.APPROVAL_PRECONDITION_SATISFIED;DEP.GATE_ALLOW;DEP.AUTHORITY_LEDGER_COMMITTED\n',
        'RT.ACTION requires'
    )
    t = replace_once(
        t,
        'pre_effect_sequence=TURN_ENTRY_ALIGNMENT;CURRENT_ARTIFACT;ACTIVE_LEASE;NON_NULL_RESOURCE_SCOPE_PIN;CURRENT_APPROVAL_WHEN_REQUIRED;AIR_GATE_ALLOW;AIR_ACTION_AUTHORIZATION_EMITTED\n',
        'pre_effect_sequence=TURN_ENTRY_ALIGNMENT;CURRENT_ARTIFACT;CURRENT_TASK_ARTIFACT_EXACT_MATCH;CURRENT_ARTIFACT_BENCHMARK_ADMISSIBLE;CURRENT_ARTIFACT_PRECHECK_ADMISSIBLE;CURRENT_ARTIFACT_PRIMARY_VISIBLE_AND_ACCOUNTED;ACTIVE_LEASE;NON_NULL_RESOURCE_SCOPE_PIN;CURRENT_APPROVAL_WHEN_REQUIRED;AIR_GATE_ALLOW;AIR_ACTION_AUTHORIZATION_EMITTED;AUTHORITY_OBJECTS_LEDGER_COMMITTED\n',
        'RT.ACTION sequence'
    )
    t = replace_once(
        t,
        'produces=RECOVERY_STATE;AIR_ERROR_OR_RECOVERY_RECORDS;SAFE_NEXT_ACTION\n',
        'produces=RECOVERY_STATE;FAILURE_CAPTURE_EVALUATION;AIR_ERROR_OR_RECOVERY_RECORDS;AIR_FAILURE_MODE_RECORD_WHEN_REUSABLE;SAFE_NEXT_ACTION\n',
        'RT.RECOVERY failure capture'
    )

    barrier_anchor = '''If the new AIR_ARTIFACT is missing, invalid, unbound, REVIEW-blocked, or REJECTED, the new task has not entered AIR-governed execution and must not be executed as ordinary/default host-model continuation.\n\nImmutability:\n'''
    barrier_new = '''If the new AIR_ARTIFACT is missing, invalid, unbound, REVIEW-blocked, or REJECTED, the new task has not entered AIR-governed execution and must not be executed as ordinary/default host-model continuation.\n\nPatch marker: AIR_NEW_TASK_BINDING_TRANSACTION_V2\n\nOnce semantic classification has latched NEW_TASK_BOUNDARY, inference authority over the task-transition consequence ends. The deterministic new-task binding transaction owns the consequence.\n\nRequired typed order:\n1. NEW_TASK_BOUNDARY_STATE = LATCHED_NEW_TASK.\n2. Resolve a distinct current task identity.\n3. Compile the exact task-specific AIR_ARTIFACT candidate.\n4. Derive that exact Artifact revision's execution_benchmark_profile.\n5. Run ARTIFACT_PRECHECK and obtain an admissible binding state.\n6. Perform the atomic Orbit 0 binding transaction.\n7. Emit the newly bound AIR_ARTIFACT on the primary user-visible response surface together with required transition records.\n8. Commit the exact emitted Artifact identity/revision to AIR_SURFACED_OBJECT_LEDGER.\n9. Only then may action or material receiver delivery for the new task become eligible.\n\nThere is no direct NEW_TASK_BOUNDARY -> RT.ACTION or NEW_TASK_BOUNDARY -> material RT.DELIVER edge. `some bound Artifact`, a prior-task Artifact, an unbenchmarked revision, a failed/unresolved precheck, an unaccounted Artifact, or an Artifact present only on a host reasoning/progress/collapsed surface does not satisfy the transaction.\n\nPre-effect violation: fail closed, perform no new-task material effect or material delivery, classify the attempted path as non-compliant, enter RT.RECOVERY, and run failure-capture evaluation.\n\nObserved external bypass effect: the external fact cannot be discarded. Preserve it as AIR_PRIOR_EFFECT_RECORD with the authority state that actually existed; exclude it from compliant AIR action history, completion evidence, benchmark evidence, approval history, and stage progression; run failure-capture evaluation; never retroactively authorize it.\n\nImmutability:\n'''
    t = replace_once(t, barrier_anchor, barrier_new, 'new task deterministic transaction law')

    old = '''Required sequence, in order:\n1. TURN_ENTRY alignment pair for the approval/effect user turn.\n2. Exactly one current controlling AIR_ARTIFACT with ACTIVE lease.\n3. A non-null resource_scope_pin bound to the exact material target and action class.\n4. Current approval when approval is required.\n5. A current AIR_GATE constructed from the current evaluation basis with decision = ALLOW. A prior REVIEW Gate does not become ALLOW by implication when approval later arrives; construct and emit the new current ALLOW Gate.\n6. One canonical single-use AIR_ACTION_AUTHORIZATION with decision = ALLOW, exact target, active lease, non-null resource_scope_pin_ref, current Gate ref, and approval basis. The authorization must be emitted before the effect attempt.\n7. Only after steps 1-6 are satisfied may the material effect be attempted.\n8. Capture observed effect evidence.\n9. Run RT.ALIGN with evaluation_profile exactly POST_MATERIAL_EFFECT. STATE_TRANSITION is not an alias for this required profile.\n10. Construct and emit canonical AIR_ACTION_RECEIPT using ACTION_RECEIPT_RECORD, current evaluation_basis, action_id, intended_target, actual_target, execution_evidence, result, effect_ids, state_comparison, and the remaining Core-owned receipt fields as applicable.\n11. receipt.authorization_ref must exactly match the single-use authorization consumed by the effect.\n12. Reconcile and, when emitted, construct the post-effect AIR_ARTIFACT with current post-effect evaluation_basis before receiver-facing success or closure.\n'''
    new = '''Required sequence, in order:\n1. TURN_ENTRY alignment pair for the approval/effect user turn.\n2. Exactly one current controlling AIR_ARTIFACT whose task_key and artifact_revision exactly match the current action task/revision.\n3. That exact Artifact revision has an admissible execution_benchmark_profile and current admissible ARTIFACT_PRECHECK result.\n4. That exact Artifact identity/revision has been emitted on the primary user-visible response surface and accounted in AIR_SURFACED_OBJECT_LEDGER.\n5. The controlling Artifact has ACTIVE lease.\n6. A non-null resource_scope_pin is bound to the exact material target and action class.\n7. Current approval when approval is required.\n8. A current AIR_GATE constructed from the current evaluation basis with decision = ALLOW. A prior REVIEW Gate does not become ALLOW by implication when approval later arrives; construct and emit the new current ALLOW Gate.\n9. One canonical single-use AIR_ACTION_AUTHORIZATION with decision = ALLOW, exact target, active lease, non-null resource_scope_pin_ref, current Gate ref, and approval basis. The authorization must be emitted before the effect attempt.\n10. Commit the Gate and Authorization to AIR_SURFACED_OBJECT_LEDGER.\n11. Only after steps 1-10 are satisfied may the material effect be attempted.\n12. Capture observed effect evidence.\n13. Run RT.ALIGN with evaluation_profile exactly POST_MATERIAL_EFFECT. STATE_TRANSITION is not an alias for this required profile.\n14. Construct and emit canonical AIR_ACTION_RECEIPT using ACTION_RECEIPT_RECORD, current evaluation_basis, action_id, intended_target, actual_target, execution_evidence, result, effect_ids, state_comparison, and the remaining Core-owned receipt fields as applicable.\n15. receipt.authorization_ref must exactly match the single-use authorization consumed by the effect.\n16. Reconcile and, when emitted, construct the post-effect AIR_ARTIFACT with current post-effect evaluation_basis before receiver-facing success or closure.\n'''
    t = replace_once(t, old, new, 'material action strict sequence')

    t = replace_once(
        t,
        'No effect call is permitted when any predecessor is missing, stale, REVIEW, null, mismatched, un-emitted, or schema-invalid. If an effect is nevertheless observed, do not synthesize missing predecessors; record it through AIR_PRIOR_EFFECT_RECORD with the state that actually existed at effect time.\n',
        'No effect call is permitted when any predecessor is missing, stale, REVIEW, null, mismatched, un-emitted, only host-collapsed/reasoning-visible, unaccounted, or schema-invalid. If an effect is nevertheless observed, do not synthesize missing predecessors; record it through AIR_PRIOR_EFFECT_RECORD with the state that actually existed at effect time and run failure-capture evaluation.\n',
        'material effect bypass recovery'
    )

    t = replace_once(
        t,
        'AIR maintains a prompt-layer append-only surfaced-object ledger for every canonical formal AIR object actually emitted in the governed session. A committed ledger entry is valid only for a canonical object actually emitted earlier in the same visible response or a prior response already carrying a valid ledger entry.',
        'AIR maintains a prompt-layer append-only surfaced-object ledger for every canonical formal AIR object actually emitted in the governed session. For a formal object whose Core law requires user-visible emission, `emitted` means emitted on the primary user-visible response surface. Placement only inside host reasoning, progress, trace, collapsed `Worked for ...`, expandable internal-work, or comparable non-primary surfaces does not satisfy required visible emission and is not eligible for USER_VISIBLE_EMITTED accounting. AIR does not claim control over host UI routing; if the host cannot place a required object on the primary response surface, the affected governed transition/effect remains blocked. A committed ledger entry is valid only for a canonical object actually emitted earlier in the same primary visible response or a prior response already carrying a valid ledger entry.',
        'primary response surface ledger rule'
    )

    p.write_text(t, encoding='utf-8')


def patch_control(root: Path) -> None:
    p = root / 'prompts/AIR_CONTROL_SURFACE.md'
    t = p.read_text(encoding='utf-8')
    t = replace_once(t, 'PROMPT_VERSION: 2.6.0', 'PROMPT_VERSION: 2.6.1', 'Control version')
    anchor = '''The visible surface must:\n1. keep ordinary conversation available when formal structure is not required\n2. print required AIR records when their trigger occurs\n'''
    replacement = '''The visible surface must:\n1. keep ordinary conversation available when formal structure is not required\n2. print required AIR records when their trigger occurs\n'''
    if anchor not in t and 'Patch marker: AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1' not in t:
        raise SystemExit('Control purpose anchor missing')
    if 'Patch marker: AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1' not in t:
        marker = '''\n==================================================\nPRIMARY USER-VISIBLE RESPONSE SURFACE LAW\n==================================================\n\nPatch marker: AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1\nFloor invariants reinforced: AIR-FLOOR-007-VISIBLE-STATE-EMISSION and AIR-FLOOR-021-CURRENT-ALIGNMENT-EVALUATION-DEPENDENCY\n\nWhen Core requires a formal AIR object to be visible, Control must place that canonical object on the primary user-visible assistant response surface. A host reasoning panel, progress trace, collapsed `Worked for ...` section, expandable internal-work panel, or comparable non-primary surface does not discharge the visibility obligation.\n\nControl must not claim that AIR can determine or override host UI routing. If a host diverts a required formal object away from the primary response surface and AIR cannot also place it in the primary response, the affected transition/effect remains unsatisfied and must fail closed or enter recovery according to Core.\n\nA required object becomes eligible for `USER_VISIBLE_EMITTED` surfaced-object-ledger state only after the exact canonical object is present on the primary response surface. Late re-emission may repair future eligibility but does not retroactively make an earlier effect compliant.\n\n'''
        insertion = '==================================================\nLOAD INTEGRITY SURFACE LAW\n==================================================\n'
        t = t.replace(insertion, marker + insertion, 1)

    old = '''Whenever AIR opens a material human-approval scope, print the exact operative responses:\n- AIR_APPROVE::<approval_scope_id>\n- AIR_REJECT::<approval_scope_id>\n\nDo not describe a paraphrase as approval/rejection authority. On an exact token response, render the current TURN_ENTRY pair first. APPROVE then renders current ALLOW Gate, matching Authorization when applicable, and AIR_SURFACED_OBJECT_LEDGER before any effect. REJECT renders current REJECT Gate plus ledger/reconciliation and performs no effect. Ambiguous/non-exact responses route to REVIEW and request the exact token.\n'''
    new = '''Whenever AIR opens a material human-approval scope, print the exact operative responses:\n- AIR_APPROVE::<approval_scope_id>\n- AIR_REJECT::<approval_scope_id>\n\nA suffix such as `_V1` is optional; do not add revision ceremony merely for token naming. The safety property is the exact current approval_scope_id plus its validated approval_scope_fingerprint. If material scope changes after tokens are declared, visibly supersede the old scope, require a new distinct approval_scope_id, and print the new token pair. Never present an old token as authority for the changed scope.\n\nDo not describe a paraphrase as approval/rejection authority. On an exact token response, render the current TURN_ENTRY pair first. APPROVE then renders current ALLOW Gate, matching Authorization when applicable, and AIR_SURFACED_OBJECT_LEDGER before any effect. REJECT renders current REJECT Gate plus ledger/reconciliation and performs no effect. Ambiguous/non-exact, stale, superseded, or fingerprint-invalid responses route to REVIEW and request the exact current token.\n'''
    t = replace_once(t, old, new, 'Control approval renderer')

    marker = 'Patch marker: AIR_ACTIVE_STEP_ORBIT_DISCIPLINE_V2\n'
    if 'Patch marker: AIR_CONTROL_NEW_TASK_BINDING_TRANSACTION_V1' not in t:
        add = '''\nPatch marker: AIR_CONTROL_NEW_TASK_BINDING_TRANSACTION_V1\nFor NEW_TASK_BOUNDARY, do not render receiver-facing new-task execution as available until the exact new AIR_ARTIFACT, its task-specific benchmark, admissible ARTIFACT_PRECHECK, atomic binding result, primary-surface Artifact emission, and surfaced-object accounting are all current. Show the blocker rather than silently continuing with a prior or merely available Artifact.\n'''
        t = t.replace(marker, marker + add, 1)

    t = t.replace('Handoff restoration rendering rules for rev16:', 'Handoff restoration rendering rules for rev17:', 1)
    p.write_text(t, encoding='utf-8')


def patch_gov(root: Path) -> None:
    p = root / 'prompts/AIR_GOV.md'
    t = p.read_text(encoding='utf-8')
    t = replace_once(t, 'PROMPT_VERSION: 2.3.0', 'PROMPT_VERSION: 2.3.1', 'Governance version')
    t = replace_once(t, '- approval_scope_id\n- gate_id\n', '- approval_scope_id\n- approval_scope_fingerprint\n- gate_id\n', 'Governance approval fingerprint field')
    t = replace_once(
        t,
        'For a material scope, operational_response_tokens is valid only when it is the exact two-element set derived from approval_scope_id: AIR_APPROVE::<approval_scope_id> and AIR_REJECT::<approval_scope_id>, with no substitution, alias, duplicate, or extra token. Restored scopes must re-run this derivation check before Core approval resolution can consume the set.\n',
        'For a material scope, operational_response_tokens is valid only when it is the exact two-element set derived from approval_scope_id: AIR_APPROVE::<approval_scope_id> and AIR_REJECT::<approval_scope_id>, with no substitution, alias, duplicate, or extra token. A revision suffix such as `_V1` is optional and carries no independent authority. approval_scope_fingerprint must match the Core canonical material-scope fingerprint. Restored scopes must re-run both token derivation and fingerprint/current-id validation before Core approval resolution can consume the set.\n',
        'Governance token/fingerprint rule'
    )
    old = '''11. If the received response is ambiguous, mismatched, multiple, stale, invalid, or validation reveals materially different scope/effects, the responsive approval does not apply or must be reacquired before binding.\n'''
    new = '''11. If the received response is ambiguous, mismatched, multiple, stale, invalid, or validation reveals materially different scope/effects, the responsive approval does not apply or must be reacquired before binding.\n12. approval_scope_id must be unique to one canonical material-scope fingerprint for its recorded lifecycle. Reusing the same id for materially different scope is invalid; the prior tokens become superseded and the changed scope requires a new distinct id.\n13. approval_scope_fingerprint is evidence of scope identity, not additional execution authority. Matching a fingerprint does not bypass exact-token, Gate, Authorization, ledger, lease, scope-pin, or Receipt requirements.\n'''
    t = replace_once(t, old, new, 'Governance scope reuse rules')
    t = replace_once(
        t,
        'A material approval scope must declare exact AIR_APPROVE::<approval_scope_id> and AIR_REJECT::<approval_scope_id> response tokens. Natural-language assent/refusal has no operative approval-state authority unless it exactly equals a declared literal. Approval/rejection resolution is Core-owned deterministic control state; Governance may tighten but not reinterpret it.\n',
        'A material approval scope must declare exact AIR_APPROVE::<approval_scope_id> and AIR_REJECT::<approval_scope_id> response tokens and a valid current approval_scope_fingerprint. Revision suffixes are optional. Natural-language assent/refusal has no operative approval-state authority unless it exactly equals a declared literal. A token tied to a superseded id/fingerprint pair has no authority. Approval/rejection resolution is Core-owned deterministic control state; Governance may tighten but not reinterpret it.\n',
        'Governance deterministic approval rule'
    )
    p.write_text(t, encoding='utf-8')


def patch_starter(root: Path) -> None:
    p = root / 'prompts/AIR_DEFAULT_STARTER_PROFILE.json'
    o = load(p)
    o['PROMPT_VERSION'] = '2.6.1'
    fvc=o['validation_contract']['deterministic_contract_registry']['foundation_prompt_version_contract']
    fvc['CORE']='2.6.1'; fvc['CONTROL']='2.6.1'; fvc['GOVERNANCE']='2.3.1'
    b = o['baseline_defaults']
    b['required_formal_object_rendering_rule'] = (
        'When Core requires a chat formal object, render the canonical JSON object on the primary user-visible assistant response surface. '
        'ALL_OBJECTS versus MINIMUM_REQUIRED_OBJECTS changes optional repetition only; it never permits prose, key/value lists, pseudo-JSON, tables, provider-native cards, host reasoning/progress panels, collapsed `Worked for ...` sections, or comparable non-primary surfaces to substitute for required Session, Artifact, alignment, binding, recovery, Gate, Authorization, Receipt, surfaced-object ledger, failure-mode, or method-evidence-waiver records. AIR_HANDOFF_CARD payload is the separate file-only delivery artifact governed by AIR_HANDOFF_FILE_DELIVERY_V1 and is never inlined in chat.'
    )
    b['required_emission_preflight_rule'] = (
        'Before visible response composition, determine every formal AIR object required on the current response. After ARTIFACT_BOUND_EXECUTION, the current turn alignment evaluation and its required AIR_ALIGNMENT_CHECK plus coupled AIR_VALIDATION_REPORT are resolved before semantic route dispatch. Lifecycle-transition objects then render using the appropriate current evaluation basis. Required user-visible emission is satisfied only on the primary response surface; host reasoning/progress/collapsed surfaces do not discharge the duty. MINIMUM_REQUIRED_OBJECTS cannot defer, downgrade, reorder, or substitute for a required object. A late correction records a prior visibility/process miss but does not retroactively make the missed response compliant.'
    )

    cc = o['compiler_contract']
    deterministic = cc['deterministic_pipeline_non_inference']['deterministic_route_ids']
    if 'RT.TASK_SWITCH' not in deterministic:
        deterministic.append('RT.TASK_SWITCH')
        deterministic.sort()

    cc['new_task_binding_transaction'] = {
        'required': True,
        'semantic_owner': 'AIR_CORE_RUNTIME_V2',
        'core_patch_marker': 'AIR_NEW_TASK_BINDING_TRANSACTION_V2',
        'execution_semantics': 'DETERMINISTIC_PIPELINE',
        'inference_policy': 'PROHIBITED_AFTER_NEW_TASK_BOUNDARY_LATCH',
        'ordered_states': [
            'NEW_TASK_BOUNDARY_LATCHED',
            'NEW_TASK_IDENTITY_RESOLVED',
            'EXACT_TASK_ARTIFACT_COMPILED',
            'TASK_BENCHMARK_DERIVED',
            'ARTIFACT_PRECHECK_ADMISSIBLE',
            'ATOMIC_ORBIT_0_BINDING_COMMITTED',
            'PRIMARY_USER_VISIBLE_ARTIFACT_EMITTED',
            'ARTIFACT_SURFACED_LEDGER_ACCOUNTED',
            'NEW_TASK_EXECUTION_ELIGIBLE',
        ],
        'direct_action_or_material_delivery_before_completion': 'PROHIBITED',
        'prior_task_authority_transfer': 'PROHIBITED',
        'pre_effect_failure_behavior': 'FAIL_CLOSED_NONCOMPLIANT_ATTEMPT_TO_RT_RECOVERY_AND_FAILURE_CAPTURE_EVALUATION',
        'observed_bypass_effect_behavior': 'PRESERVE_AS_PRIOR_EFFECT_EXCLUDE_FROM_COMPLIANT_HISTORY_AND_RUN_FAILURE_CAPTURE_EVALUATION',
    }

    mat = cc['material_action_transaction']
    mat['ordered_pre_and_post_effect_states'] = [
        'TURN_ENTRY_ALIGNMENT',
        'CURRENT_ARTIFACT_BOUND',
        'CURRENT_TASK_ARTIFACT_EXACT_MATCH',
        'CURRENT_ARTIFACT_BENCHMARK_ADMISSIBLE',
        'CURRENT_ARTIFACT_PRECHECK_ADMISSIBLE',
        'CURRENT_ARTIFACT_PRIMARY_VISIBLE_AND_ACCOUNTED',
        'ACTIVE_LEASE',
        'NON_NULL_RESOURCE_SCOPE_PIN',
        'CURRENT_APPROVAL_WHEN_REQUIRED',
        'CURRENT_AIR_GATE_ALLOW',
        'AIR_ACTION_AUTHORIZATION_EMITTED',
        'AUTHORITY_OBJECTS_LEDGER_COMMITTED',
        'EFFECT_ATTEMPT',
        'OBSERVED_EFFECT_EVIDENCE',
        'POST_MATERIAL_EFFECT_ALIGNMENT',
        'CANONICAL_AIR_ACTION_RECEIPT',
        'POST_EFFECT_ARTIFACT_RECONCILIATION',
    ]
    mat['exact_current_task_artifact_required'] = True
    mat['artifact_benchmark_admissibility_required'] = True
    mat['artifact_precheck_admissibility_required'] = True
    mat['artifact_primary_visible_accounting_required'] = True

    reg = cc['runtime_control_event_registry']
    events = {e['route_id']: e for e in reg['events']}
    events['RT.TASK_SWITCH']['guards'] = [
        {'operator':'STATE_PRESENT','path':'CURRENT_EVALUATION_BASIS'},
        {'operator':'STATE_EQUALS','path':'NEW_TASK_BOUNDARY_STATE','expected':'LATCHED_NEW_TASK'},
        {'operator':'STATE_EQUALS','path':'NEW_TASK_IDENTITY_RESOLUTION_STATE','expected':'RESOLVED'},
        {'operator':'STATE_EQUALS','path':'NEW_TASK_ARTIFACT_COMPILATION_STATE','expected':'COMPILED'},
        {'operator':'STATE_EQUALS','path':'NEW_TASK_BENCHMARK_STATE','expected':'DERIVED'},
        {'operator':'STATE_EQUALS','path':'NEW_TASK_PRECHECK_ADMISSIBILITY_STATE','expected':'ADMISSIBLE_FOR_BINDING'},
        {'operator':'STATE_EQUALS','path':'NEW_TASK_BINDING_READINESS_STATE','expected':'READY'},
    ]
    action_guards = events['RT.ACTION']['guards']
    prefixes = [
        {'operator':'STATE_PRESENT','path':'CURRENT_EVALUATION_BASIS'},
        {'operator':'STATE_PRESENT','path':'CURRENT_BOUND_ARTIFACT'},
        {'operator':'STATE_EQUALS','path':'CURRENT_TASK_ARTIFACT_MATCH_STATE','expected':'EXACT_MATCH'},
        {'operator':'STATE_EQUALS','path':'CURRENT_ARTIFACT_BENCHMARK_STATE','expected':'ADMISSIBLE'},
        {'operator':'STATE_EQUALS','path':'CURRENT_ARTIFACT_PRECHECK_STATE','expected':'ADMISSIBLE'},
        {'operator':'STATE_EQUALS','path':'CURRENT_ARTIFACT_VISIBLE_ACCOUNTING_STATE','expected':'PRIMARY_VISIBLE_AND_ACCOUNTED'},
    ]
    events['RT.ACTION']['guards'] = prefixes + action_guards[2:]

    ar = cc['approval_response_resolution']
    ar['approval_scope_id_revision_suffix_required'] = False
    ar['approval_scope_fingerprint_required'] = True
    ar['approval_scope_fingerprint_algorithm'] = 'SHA256_CANONICAL_JSON_V1'
    ar['approval_scope_fingerprint_fields'] = [
        'gate_id','exact_gate_question','requested_action','authorized_action_ids','excluded_action_ids',
        'required_evidence','stop_conditions','expiry_or_completion_condition'
    ]
    ar['scope_id_reuse_rule'] = 'SAME_APPROVAL_SCOPE_ID_WITH_DIFFERENT_FINGERPRINT_INVALID_REQUIRES_NEW_DISTINCT_ID'
    ar['superseded_token_authority'] = 'NONE'
    ar['restored_scope_fingerprint_validation_required'] = True

    fm = cc['failure_mode_registry']
    fm['execution_defect_rejection_capture_required'] = True
    fm['new_task_binding_barrier_failure_trigger'] = 'NEW_TASK_BINDING_BARRIER_REJECT'
    fm['recovery_capture_rule'] = 'RT_RECOVERY_EVALUATES_REUSABLE_FAILURE_CAPTURE_BEFORE_END_RESPONSE'

    dump(p, o)


def patch_handoff(root: Path) -> None:
    p = root / 'prompts/AIR_HANDOFF_CARD_TEMPLATE.json'
    doc = load(p)
    h = doc['AIR_HANDOFF_CARD']
    h['card_revision'] = 17
    h['profile_stack']['starter_profile']['PROMPT_VERSION'] = '2.6.1'
    if 'governance_supplement_version' in h.get('governance_state', {}):
        h['governance_state']['governance_supplement_version'] = '2.3.1'

    ps = h['execution_state']['patch_state']
    ps.update({
        'repository_source_ref': None,
        'repository_source_commit': None,
        'repository_source_tree': None,
        'tracked_file_count': None,
        'reconciled_file_count': None,
        'unclassified_file_count': None,
        'reconciliation_state': 'NOT_EVALUATED',
        'disposition_matrix_ref': None,
        'post_patch_reconciliation_required': False,
        'post_patch_reconciliation_state': 'NOT_APPLICABLE',
    })

    sm = h['schema_manifest']
    for rule in sm.get('conditional_rules', []):
        if rule.get('id') == 'HC-COND-APPROVAL':
            req = rule['requirements']
            fp = 'open_approval_scope.approval_scope_fingerprint'
            if fp not in req:
                req.insert(1, fp)
    vr = sm['validation_registry']
    if 'APPROVAL_SCOPE_IDENTITY_FINGERPRINT_VALID' not in vr['allowed_operators']:
        vr['allowed_operators'].append('APPROVAL_SCOPE_IDENTITY_FINGERPRINT_VALID')
    vr['operator_semantics']['APPROVAL_SCOPE_IDENTITY_FINGERPRINT_VALID'] = (
        'For a non-null material open scope, recompute SHA-256 canonical JSON over the Core-owned fingerprint field set; require equality with approval_scope_fingerprint; require the approval_scope_id not be associated with a different prior lifecycle fingerprint; revision suffixes are optional. Produce OPEN_APPROVAL_SCOPE_IDENTITY_VALIDATION_STATE=VALIDATED_CURRENT_UNIQUE_SCOPE_FINGERPRINT only on success.'
    )
    vr['operator_semantics']['PATCH_ACTIVITY_REQUIREMENTS_VALID'] = (
        'ACTIVE_FILE_MUTATION_OR_PATCH requires nonempty source_inventory, replacement_policy, mutation_scope, validation_plan and last_validation_state carrier. When repository patch reconciliation is material, repository_source_ref/source_commit/source_tree, tracked_file_count, reconciled_file_count, unclassified_file_count, reconciliation_state, disposition_matrix_ref, and post-patch reconciliation state must be present; completion requires tracked_file_count=reconciled_file_count, unclassified_file_count=0, reconciliation_state=PASS, and required post-patch reconciliation=PASS.'
    )
    apr = vr['rules']['HC-VALIDATE-APPROVAL']['predicates']
    if not any(x.get('path') == '$.open_approval_scope.approval_scope_fingerprint' for x in apr):
        apr.insert(1, {'operator':'PATH_EXISTS','path':'$.open_approval_scope.approval_scope_fingerprint'})
    if not any(x.get('operator') == 'APPROVAL_SCOPE_IDENTITY_FINGERPRINT_VALID' for x in apr):
        apr.append({'operator':'APPROVAL_SCOPE_IDENTITY_FINGERPRINT_VALID','path':'$.open_approval_scope'})

    scm = sm['schema_compatibility_contract']
    scm['card_revision_compatibility'] = 'REV17_SCHEMA_2_3_0_WITH_EXPLICIT_PATCH_RECONCILIATION_APPROVAL_FINGERPRINT_AND_MIGRATION_FROM_REV16_REV15_REV14_REV13_AND_SCHEMA_2_2_0_REV12_AND_EARLIER'
    scm['rev16_to_rev17_migration_contract_ref'] = 'AIR_HANDOFF_CARD.schema_manifest.revision_migration_contracts.REV16_TO_REV17'

    contracts = sm['revision_migration_contracts']
    contracts['REV16_TO_REV17'] = {
        'source_schema_version': '2.3.0',
        'source_card_revision': 16,
        'target_schema_version': '2.3.0',
        'target_card_revision': 17,
        'apply_before_current_required_carrier_check': True,
        'nested_additions': {
            'execution_state.patch_state': [
                'repository_source_ref','repository_source_commit','repository_source_tree',
                'tracked_file_count','reconciled_file_count','unclassified_file_count',
                'reconciliation_state','disposition_matrix_ref',
                'post_patch_reconciliation_required','post_patch_reconciliation_state'
            ],
            'open_approval_scope_when_non_null': ['approval_scope_fingerprint']
        },
        'approval_scope_migration_rule': 'MISSING_PRE_REV17_FINGERPRINT_IS_NOT_INFERRED; NON_NULL_OPEN_SCOPE_ROUTES_REVIEW_AND_REACQUISITION_UNLESS_EXACT_SCOPE_FINGERPRINT_CAN_BE_RECOMPUTED_FROM_COMPLETE_EXPLICIT_FIELDS_AND_ID_HISTORY_VALIDATED',
        'patch_state_migration_rule': 'ADD_RECONCILIATION_CARRIERS_WITH_UNRESOLVED_SAFE_DEFAULTS; DO_NOT CLAIM PRIOR_FULL_REPOSITORY_RECONCILIATION',
        'history_synthesis': 'PROHIBITED'
    }
    mig = h['migration_state']['compatibility_rules']
    mig['v2_3_rev16_to_rev17_patch_and_approval_identity'] = 'Rev16 cards remain valid schema-2.3.0 migration input. Add patch-reconciliation carriers with unresolved safe defaults. Do not infer a missing approval fingerprint; a non-null open approval scope requires exact recomputation from complete explicit fields plus scope-id history validation or routes to REVIEW/reacquisition.'
    h['migration_state']['revision_migration_path'] = None

    def revise_rev_strings(x: Any, path: tuple[str,...]=()) -> Any:
        if any(part in HISTORY_KEYS or part.startswith('historical_') for part in path):
            return x
        if isinstance(x, dict):
            return {k: revise_rev_strings(v, path+(str(k),)) for k,v in x.items()}
        if isinstance(x, list):
            return [revise_rev_strings(v, path+(str(i),)) for i,v in enumerate(x)]
        if isinstance(x, str):
            return x.replace('rev16 may record', 'rev17 may record').replace('rendering rules for rev16', 'rendering rules for rev17')
        return x
    h2 = revise_rev_strings(h)
    doc['AIR_HANDOFF_CARD'] = h2
    dump(p, doc)


def patch_readme(root: Path) -> None:
    p = root / 'README.md'
    t = p.read_text(encoding='utf-8')
    t = t.replace('foundation-2.6.0-', 'foundation-2.6.1-', 1)
    if '## Development candidate - AIR Kit v0.7.2' not in t:
        anchor = 'See the [v0.7.1 release](https://github.com/eddlev/vm4ai-air-kit/releases/tag/v0.7.1) for the detailed change and validation record.\n'
        block = '''\n\n## Development candidate - AIR Kit v0.7.2\n\nThis branch prepares **AIR Kit v0.7.2**. The latest published release remains v0.7.1 until a v0.7.2 tag/release is actually published.\n\nv0.7.2 hardens AIR's control spine around new-task Artifact binding, exact task-to-Artifact action checks, failure capture, repository patch reconciliation, approval-scope identity reuse, Handoff revision 17, and required formal-object visibility.\n\n### Best practices\n\n**Thinking Effort.** AIR does not currently require a specific ChatGPT Thinking Effort setting. For day-to-day AIR use, **High** is a reasonable starting point. **Extra High** may be useful for unusually difficult analysis or architecture work, but there is not currently evidence that Thinking Effort causes or prevents AIR runtime drift. Treat cross-effort observations as empirical host-behavior evidence, not AIR execution authority.\n\n**Known ChatGPT presentation issue.** AIR formal records have occasionally been observed inside ChatGPT's collapsed **`Worked for ...`** section rather than in the main response. Expanding that section reveals the records. This has so far only been observed on ChatGPT; the cause has not been isolated between AIR response-surface behavior and host UI routing. AIR formal records are structured governance records, not hidden reasoning or chain of thought. If expected records appear missing in ChatGPT, check that section and include the behavior in any bug report.\n'''
        if anchor not in t:
            raise SystemExit('README release anchor missing')
        t = t.replace(anchor, anchor + block, 1)
    human = 'The exact approval token authorizes only the scope AIR described.\n'
    repl = 'The exact approval token authorizes only the scope AIR described. A version suffix such as `_V1` is optional; AIR must issue a new distinct scope ID if the material scope changes, so old tokens cannot silently authorize a different action.\n'
    if human in t:
        t = t.replace(human, repl, 1)
    p.write_text(t, encoding='utf-8')


def patch_fixtures(root: Path) -> None:
    p = root / 'tests/air_contract_fixtures.json'
    o = load(p)
    o['fixture_set'] = 'AIR_SET006_REGRESSION_FIXTURES_V1'
    o['fixture_version'] = '1.2.0'
    o['foundation_identity'] = NEW_FOUNDATION
    o['purpose'] = 'Permanent deterministic and replayable regression definitions for AIR Kit v0.7.2 control-spine hardening and retained v0.7.1 defect classes. Fixtures are test definitions, not proof that a model evaluation ran.'
    nt = [
        {'id':'NTB-01-MISSING-NEW-TASK-ARTIFACT','invalid_if':'NEW_TASK_BOUNDARY reaches material action or receiver-facing material delivery without compiling the distinct task-specific AIR_ARTIFACT.'},
        {'id':'NTB-02-PRIOR-OR-WRONG-TASK-ARTIFACT','invalid_if':'RT.ACTION accepts a bound Artifact whose task_key or revision does not exactly match the current action task/revision.'},
        {'id':'NTB-03-MISSING-TASK-BENCHMARK','invalid_if':'New-task execution proceeds when the exact current Artifact revision lacks an admissible task-specific execution_benchmark_profile.'},
        {'id':'NTB-04-PRECHECK-NONADMISSIBLE','invalid_if':'New-task execution proceeds when ARTIFACT_PRECHECK is missing, unresolved, REVIEW-blocked, or rejected rather than admissible for binding.'},
        {'id':'NTB-05-UNBOUND-ARTIFACT','invalid_if':'New-task material execution proceeds before atomic Orbit 0 ACTIVE_EXECUTION_BINDING commits.'},
        {'id':'NTB-06-ARTIFACT-NOT-PRIMARY-VISIBLE-ACCOUNTED','invalid_if':'New-task execution treats an Artifact as emitted/accounted when it was not emitted on the primary user-visible response surface and ledgered as that exact identity/revision.'},
        {'id':'NTB-07-DIRECT-BOUNDARY-ACTION-BYPASS','invalid_if':'A direct NEW_TASK_BOUNDARY to RT.ACTION or material RT.DELIVER edge bypasses the ordered new-task binding transaction.'},
        {'id':'NTB-08-OBSERVED-BYPASS-RETROACTIVE-UPGRADE','invalid_if':'An externally observed bypass effect is retrospectively counted as compliant action/completion/benchmark/approval history instead of prior-effect truth plus failure-capture evaluation.'},
    ]
    o['new_task_binding_barrier_negative_cases'] = nt
    o['approval_scope_identity_cases'] = [
        {'id':'ASI-01-SUFFIX-FREE-VALID','valid_when':'A suffix-free approval_scope_id has the exact declared token pair, valid current fingerprint, and unique id-to-fingerprint lifecycle mapping.'},
        {'id':'ASI-02-SUFFIX-NOT-REQUIRED','invalid_if':'Approval validation requires `_V1` or any revision suffix despite otherwise valid scope identity.'},
        {'id':'ASI-03-CHANGED-FINGERPRINT-REUSED-ID','invalid_if':'A material-scope fingerprint changes but AIR reuses the same approval_scope_id or accepts its old token pair.'},
    ]
    o['primary_response_surface_cases'] = [
        {'id':'PRS-01-COLLAPSED-HOST-SURFACE-NOT-EMISSION','invalid_if':'A required formal AIR object located only in host reasoning/progress/collapsed `Worked for ...`/expandable internal-work surface is counted USER_VISIBLE_EMITTED for a required primary-response obligation.'},
    ]
    o['repository_patch_reconciliation_cases'] = [
        {'id':'RPR-01-UNCLASSIFIED-TRACKED-FILE','invalid_if':'Repository patch completion is claimed with any tracked source file unclassified.'},
        {'id':'RPR-02-POST-PATCH-RECONCILIATION-MISSING','invalid_if':'Repository patch completion is claimed before the complete tracked-file inventory is reconciled again against the final patched state.'},
    ]
    dump(p, o)


def patch_inventory(root: Path) -> None:
    p = root / 'tests/deterministic_contract_inventory.json'
    o = load(p)
    o['inventory_id'] = 'AIR_SET006_DETERMINISTIC_CONTRACT_INVENTORY_V1'
    o['foundation_identity'] = NEW_FOUNDATION
    o['claim_boundary'] = 'This inventory covers deterministic five-file Foundation load/cross-file compatibility predicates for SET_006. Runtime behavioral laws, including the deterministic task-switch/action transaction, and replayable model behavior remain separately validated and are not reclassified as deterministic executable evidence.'
    dump(p, o)


def patch_profiles(root: Path) -> None:
    for p in sorted((root / 'profiles').glob('**/*.json')):
        o = load(p)
        o = current_transform(o)
        update_dependency_versions(o)
        dump(p, o)


def update_route_map(root: Path) -> None:
    p = root / 'catalog/AIR_RUNTIME_ROUTE_MAP.json'
    o = load(p)
    core_p = root / 'prompts/AIR_CORE_RUNTIME.md'
    core = core_p.read_text(encoding='utf-8')
    o['MAP_VERSION'] = '1.2.0'
    o['source_of_truth']['prompt_version'] = '2.6.1'
    o['source_of_truth']['sha256'] = hashlib.sha256(core_p.read_bytes()).hexdigest()
    lines = {ln.split('=',1)[1]: i for i, ln in enumerate(core.splitlines(),1) if ln.startswith('id=RT.')}
    routes = {r['route_id']: r for r in o['routes']}
    for rid, line in lines.items():
        if rid in routes:
            routes[rid]['source_anchor']['line'] = line
    task = routes['RT.TASK_SWITCH']
    task.update({
        'requires': ['DEP.CURRENT_EVALUATION_BASIS','DEP.NEW_TASK_BOUNDARY_LATCHED','DEP.NEW_TASK_IDENTITY_RESOLVED','DEP.NEW_TASK_ARTIFACT_COMPILED','DEP.NEW_TASK_BENCHMARK_DERIVED','DEP.NEW_TASK_PRECHECK_ADMISSIBLE','DEP.NEW_TASK_BINDING_READY'],
        'produces': ['NEW_TASK_ARTIFACT_CANDIDATE','NEW_TASK_BINDING_TRANSACTION_STATE','ORBIT_TRANSITION','AIR_SESSION_WHEN_ORBIT_CHANGED','AIR_PROJECT_EXECUTION_MAP','AIR_ARTIFACT','NEW_TASK_ARTIFACT_VISIBLE_ACCOUNTING_STATE'],
        'does_not_bypass': ['DEP.NEW_TASK_ARTIFACT','DEP.ARTIFACT_PRECHECK','DEP.NEW_TASK_ARTIFACT_VISIBLE_ACCOUNTED','AIR-FLOOR-013','AIR-FLOOR-025-DETERMINISTIC-PIPELINE-NON-INFERENCE','AIR-FLOOR-026-DETERMINISTIC-CONTRACT-MACHINE-REPRESENTATION'],
        'execution_semantics': 'DETERMINISTIC_PIPELINE',
        'inference_policy': 'PROHIBITED',
        'step_order': 'STRICT',
        'missing_input_behavior': 'FAIL_CLOSED',
        'unknown_condition_behavior': 'FAIL_CLOSED',
        'conflict_behavior': 'FAIL_CLOSED',
        'new_task_binding_transaction': {
            'contract': 'AIR_NEW_TASK_BINDING_TRANSACTION_V2',
            'ordered_states': ['NEW_TASK_BOUNDARY_LATCHED','NEW_TASK_IDENTITY_RESOLVED','EXACT_TASK_ARTIFACT_COMPILED','TASK_BENCHMARK_DERIVED','ARTIFACT_PRECHECK_ADMISSIBLE','ATOMIC_ORBIT_0_BINDING_COMMITTED','PRIMARY_USER_VISIBLE_ARTIFACT_EMITTED','ARTIFACT_SURFACED_LEDGER_ACCOUNTED','NEW_TASK_EXECUTION_ELIGIBLE'],
            'direct_action_or_material_delivery_before_completion': 'PROHIBITED',
            'failure_behavior': 'FAIL_CLOSED_TO_RT.RECOVERY_AND_FAILURE_CAPTURE_EVALUATION'
        }
    })
    action = routes['RT.ACTION']
    action['requires'] = ['DEP.CURRENT_EVALUATION_BASIS','DEP.ARTIFACT_BOUND','DEP.CURRENT_TASK_ARTIFACT_EXACT_MATCH','DEP.CURRENT_ARTIFACT_BENCHMARK_ADMISSIBLE','DEP.CURRENT_ARTIFACT_PRECHECK_ADMISSIBLE','DEP.CURRENT_ARTIFACT_VISIBLE_ACCOUNTED','DEP.LEASE_ACTIVE','DEP.SCOPE_MATCH','DEP.APPROVAL_PRECONDITION_SATISFIED','DEP.GATE_ALLOW','DEP.AUTHORITY_LEDGER_COMMITTED']
    action['material_action_transaction']['current_task_artifact_exact_match_required'] = True
    action['material_action_transaction']['artifact_benchmark_admissible_required'] = True
    action['material_action_transaction']['artifact_precheck_admissible_required'] = True
    action['material_action_transaction']['artifact_primary_visible_accounted_required'] = True
    recovery = routes['RT.RECOVERY']
    recovery['produces'] = ['RECOVERY_STATE','FAILURE_CAPTURE_EVALUATION','AIR_ERROR_OR_RECOVERY_RECORDS','AIR_FAILURE_MODE_RECORD_WHEN_REUSABLE','SAFE_NEXT_ACTION']
    dp = o.get('deterministic_pipeline_contract', {})
    ids = dp.get('declared_route_ids', [])
    if 'RT.TASK_SWITCH' not in ids:
        ids.append('RT.TASK_SWITCH')
    dp['declared_route_ids'] = sorted(set(ids))
    dp['route_count'] = len(dp['declared_route_ids']) if 'route_count' in dp else dp.get('route_count')
    dump(p, o)


def patch_index(root: Path) -> None:
    p = root / 'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'
    o = load(p)
    o = current_transform(o)
    update_dependency_versions(o)
    o['INDEX_VERSION'] = '1.3.1'
    o['status'] = 'AIR_2_6_1_OBJECT_CONTRACT_SET_006_FIVE_PACKAGE_INDEX_V072_CANDIDATE_STATIC_VALIDATED'
    o['catalog_scope']['catalog_completeness_claim'] = 'COMPLETE_FOR_AIR_2_6_1_OBJECT_CONTRACT_SET_006_V072_CANDIDATE_SPECIALIST_CATALOG'
    o['foundation_compatibility_catalog']['identity'] = NEW_FOUNDATION
    rm = o['foundation_adjacent_compatibility_catalog']['runtime_route_map']
    rm['version'] = '1.2.0'
    vs = o['validation_state']
    vs['decision'] = 'STATIC_VALIDATED_CANDIDATE_PENDING_REPLAYABLE_BEHAVIORAL_REVALIDATION'
    vs['foundation_identity_closure'] = 'PASS_' + NEW_FOUNDATION
    if 'handoff_rev16_catalog_compatibility' in vs:
        vs['handoff_rev17_catalog_compatibility'] = vs.pop('handoff_rev16_catalog_compatibility').replace('rev16','rev17').replace('REV16','REV17')
    vs['static_validation'] = 'PASS_R7_DETERMINISTIC_STATIC_SUITE'
    vs['behavioral_revalidation'] = 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'
    vs['release_publication_state'] = 'EXTERNAL_RELEASE_STATE_NOT_RUNTIME_AUTHORITY'
    vs['operative_lifecycle_coherence'] = 'PASS_V072_CANDIDATE_LIFECYCLE'
    vs['component_internal_foundation_compatibility'] = 'PASS_SET_006_EXACT_RECEIPTS'
    for e in o['entries']:
        e['foundation_compatibility_identity'] = NEW_FOUNDATION
        e['availability_state'] = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'
    lc = o['candidate_lifecycle_contract']
    lc['current_candidate_state'] = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'
    dump(p, o)


def patch_release_validator(root: Path) -> None:
    p = root / 'tools/validate_air_release.py'
    t = p.read_text(encoding='utf-8')
    reps = [
        ("EXPECTED_KIT_VERSION = '0.7.1'", "EXPECTED_KIT_VERSION = '0.7.2'"),
        ("EXPECTED_FOUNDATION_ID = 'AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005'", "EXPECTED_FOUNDATION_ID = 'AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006'"),
        ("EXPECTED_ROUTE_MAP_VERSION = '1.1.0'", "EXPECTED_ROUTE_MAP_VERSION = '1.2.0'"),
        ("EXPECTED_INDEX_VERSION = '1.3.0'", "EXPECTED_INDEX_VERSION = '1.3.1'"),
        ('EXPECTED_HANDOFF_CARD_REVISION = 16', 'EXPECTED_HANDOFF_CARD_REVISION = 17'),
        ("'AIR_CORE_RUNTIME.md': '2.6.0'", "'AIR_CORE_RUNTIME.md': '2.6.1'"),
        ("'AIR_CONTROL_SURFACE.md': '2.6.0'", "'AIR_CONTROL_SURFACE.md': '2.6.1'"),
        ("'AIR_GOV.md': '2.3.0'", "'AIR_GOV.md': '2.3.1'"),
        ("'AIR_DEFAULT_STARTER_PROFILE.json': '2.6.0'", "'AIR_DEFAULT_STARTER_PROFILE.json': '2.6.1'"),
        ("'AIR_RUNTIME_ROUTE_MAP.json': '1.1.0'", "'AIR_RUNTIME_ROUTE_MAP.json': '1.2.0'"),
        ("R7_INDEX_COMPLETENESS = 'COMPLETE_FOR_AIR_2_6_0_OBJECT_CONTRACT_SET_005_V071_RELEASE_SPECIALIST_CATALOG'", "R7_INDEX_COMPLETENESS = 'COMPLETE_FOR_AIR_2_6_1_OBJECT_CONTRACT_SET_006_V072_CANDIDATE_SPECIALIST_CATALOG'"),
        ("R7_CANDIDATE_STATE = 'RELEASE_CATALOG_ENTRY'", "R7_CANDIDATE_STATE = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'"),
        ("require('PROMPT_VERSION: 2.6.0' in core", "require('PROMPT_VERSION: 2.6.1' in core"),
        ("require('PROMPT_VERSION: 2.6.0' in control", "require('PROMPT_VERSION: 2.6.1' in control"),
        ("require(starter['PROMPT_VERSION'] == '2.6.0'", "require(starter['PROMPT_VERSION'] == '2.6.1'"),
        ("print('AIR v0.7.1 set-005 deterministic validation: PASS')", "print('AIR v0.7.2 set-006 candidate deterministic validation: PASS')"),
    ]
    for old, new in reps:
        t = replace_once(t, old, new, 'release validator '+old[:28])
    anchor = "require('Patch marker: AIR_DETERMINISTIC_CONTRACT_MACHINE_REPRESENTATION_V1' in core, 'missing deterministic contract representation law')\n"
    extra = anchor + "    require('Patch marker: AIR_NEW_TASK_BINDING_TRANSACTION_V2' in core, 'missing v0.7.2 new-task binding transaction')\n    require('Patch marker: AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1' in control, 'missing v0.7.2 primary response surface law')\n    require('PROMPT_VERSION: 2.3.1' in gov, 'Governance version mismatch')\n"
    if "AIR_NEW_TASK_BINDING_TRANSACTION_V2' in core" not in t:
        t = replace_once(t, anchor, extra, 'release v072 markers')
    p.write_text(t, encoding='utf-8')


def patch_r7_validator(root: Path) -> None:
    p = root / 'tools/validate_air_r7_remediation.py'
    t = p.read_text(encoding='utf-8')
    replacements = [
        ("FOUNDATION_ID='AIR_FOUNDATION_2_6_0_OBJECT_CONTRACT_SET_005'", "FOUNDATION_ID='AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006'"),
        ("idx['status']=='AIR_2_6_0_OBJECT_CONTRACT_SET_005_FIVE_PACKAGE_INDEX_V071_RELEASE_SEALED'", "idx['status']=='AIR_2_6_1_OBJECT_CONTRACT_SET_006_FIVE_PACKAGE_INDEX_V072_CANDIDATE_STATIC_VALIDATED'"),
        ("idx['catalog_scope']['catalog_completeness_claim']=='COMPLETE_FOR_AIR_2_6_0_OBJECT_CONTRACT_SET_005_V071_RELEASE_SPECIALIST_CATALOG'", "idx['catalog_scope']['catalog_completeness_claim']=='COMPLETE_FOR_AIR_2_6_1_OBJECT_CONTRACT_SET_006_V072_CANDIDATE_SPECIALIST_CATALOG'"),
        ("lc.get('current_candidate_state')=='RELEASE_CATALOG_ENTRY'", "lc.get('current_candidate_state')=='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'"),
        ("req(e['availability_state']=='RELEASE_CATALOG_ENTRY','006 index entry lifecycle mismatch')", "req(e['availability_state']=='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION','006 index entry lifecycle mismatch')"),
    ]
    for old, new in replacements:
        t = replace_once(t, old, new, 'R7 validator')
    p.write_text(t, encoding='utf-8')


def patch_r3_validator(root: Path) -> None:
    p = root / 'tools/validate_air_r3_remediation.py'
    t = p.read_text(encoding='utf-8')
    t = t.replace("req(len(starter['validation_contract']['deterministic_contract_registry']['checks'])==80,'R1 registry lost')", "req(len(starter['validation_contract']['deterministic_contract_registry']['checks'])==80,'R1 registry lost')")
    old = "rc=sm['revision_migration_contracts']['REV15_TO_REV16']; req(rc['apply_before_current_required_carrier_check'] is True,'072 order flag false'); seq=sm['validation_sequence']; req(seq.index('source card revision detection and applicable revision migration check') < seq.index('required-carrier check after applicable migration'),'072 sequence migration after required carriers'); req(rc['history_synthesis']=='PROHIBITED','072 history synthesis not prohibited')"
    new = "rc=sm['revision_migration_contracts']['REV15_TO_REV16']; req(rc['apply_before_current_required_carrier_check'] is True,'072 order flag false'); rc17=sm['revision_migration_contracts']['REV16_TO_REV17']; req(rc17['apply_before_current_required_carrier_check'] is True,'v072 rev16->17 order flag false'); req(rc17['history_synthesis']=='PROHIBITED','v072 rev16->17 history synthesis not prohibited'); seq=sm['validation_sequence']; req(seq.index('source card revision detection and applicable revision migration check') < seq.index('required-carrier check after applicable migration'),'072 sequence migration after required carriers'); req(rc['history_synthesis']=='PROHIBITED','072 history synthesis not prohibited')"
    t = replace_once(t, old, new, 'R3 migration contracts')
    old2 = "migrated=mod.migrate_rev15_to_rev16(src,{'AIR_HANDOFF_CARD':H})['AIR_HANDOFF_CARD']\n    req(migrated['card_revision']==16,'072 target rev');"
    new2 = "migrated=mod.migrate_to_current(src,{'AIR_HANDOFF_CARD':H})['AIR_HANDOFF_CARD']\n    req(migrated['card_revision']==17,'072 target rev');"
    t = replace_once(t, old2, new2, 'R3 current migration target')
    p.write_text(t, encoding='utf-8')


def patch_r3_mutations(root: Path) -> None:
    p = root / 'tools/test_air_r3_mutations.py'
    t = p.read_text(encoding='utf-8')
    if 'R3-N15-REV16-TO-REV17-MIGRATION-ORDER' not in t:
        anchor = "    cases.append(('R3-N14-REV15-MIGRATION-ORDER', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['revision_migration_contracts']['REV15_TO_REV16'].__setitem__('apply_before_current_required_carrier_check',False))))\n"
        extra = anchor + "    cases.append(('R3-N15-REV16-TO-REV17-MIGRATION-ORDER', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['revision_migration_contracts']['REV16_TO_REV17'].__setitem__('apply_before_current_required_carrier_check',False))))\n    cases.append(('R3-N16-APPROVAL-FINGERPRINT-VALIDATION', mutate_json('prompts/AIR_HANDOFF_CARD_TEMPLATE.json', lambda o:o['AIR_HANDOFF_CARD']['schema_manifest']['validation_registry']['allowed_operators'].remove('APPROVAL_SCOPE_IDENTITY_FINGERPRINT_VALID'))))\n"
        t = replace_once(t, anchor, extra, 'R3 mutations v072')
    p.write_text(t, encoding='utf-8')


def patch_migration_tool(root: Path) -> None:
    p = root / 'tools/migrate_air_handoff.py'
    old = p.read_text(encoding='utf-8')
    if 'def migrate_rev16_to_rev17' not in old:
        marker = '\ndef main():\n'
        add = r'''

def migrate_rev16_to_rev17(doc: dict[str,Any], current_template_doc: dict[str,Any])->dict[str,Any]:
    if set(doc)!= {'AIR_HANDOFF_CARD'}: raise MigrationError('expected exactly one AIR_HANDOFF_CARD root')
    if set(current_template_doc)!= {'AIR_HANDOFF_CARD'}: raise MigrationError('current template root invalid')
    src=doc['AIR_HANDOFF_CARD']; tmpl=current_template_doc['AIR_HANDOFF_CARD']
    if src.get('schema_version')!='2.3.0' or src.get('SCHEMA_VERSION')!='2.3.0': raise MigrationError('source is not schema 2.3.0')
    if src.get('card_revision')!=16: raise MigrationError('source card_revision is not 16')
    contract=tmpl.get('schema_manifest',{}).get('revision_migration_contracts',{}).get('REV16_TO_REV17')
    if not contract or contract.get('apply_before_current_required_carrier_check') is not True: raise MigrationError('current rev17 migration contract missing')
    out=copy.deepcopy(doc); c=out['AIR_HANDOFF_CARD']; c['card_revision']=17
    ps=c.setdefault('execution_state',{}).setdefault('patch_state',{})
    defaults=tmpl['execution_state']['patch_state']
    for k in contract['nested_additions']['execution_state.patch_state']:
        ps.setdefault(k,copy.deepcopy(defaults.get(k)))
    scope=c.get('open_approval_scope')
    if isinstance(scope,dict) and scope.get('approval_scope_fingerprint') is None:
        scope['approval_state']='REVIEW_REQUIRED'
    old_ms=c.get('migration_state') if isinstance(c.get('migration_state'),dict) else {}
    ms=copy.deepcopy(tmpl['migration_state'])
    if isinstance(old_ms,dict):
        for k in ['legacy_q4_c_state','legacy_q4_d_state','legacy_prompt_mode_state','legacy_orbit_state','legacy_active_contract_state','legacy_governance_state','unresolved_legacy_states','legacy_history_state']:
            if k in old_ms: ms[k]=copy.deepcopy(old_ms[k])
    ms['source_schema_version']='2.3.0'; ms['source_card_revision']=16; ms['migration_required']=True
    ms['migration_decision']='MIGRATED_REV16_TO_REV17_PENDING_CURRENT_ALIGNMENT_REBINDING_AND_APPROVAL_SCOPE_REVALIDATION'
    ms['revision_migration_path']='REV16_TO_REV17'
    ms['source_schema_manifest_sha256']=canonical_sha(src.get('schema_manifest',{}))
    c['migration_state']=ms; c['schema_manifest']=copy.deepcopy(tmpl['schema_manifest'])
    required=set(tmpl['schema_manifest']['required_fields']); missing=sorted(required-set(c))
    if missing: raise MigrationError('rev16 input missing current required root carriers after declared migration: '+', '.join(missing))
    return out


def migrate_to_current(doc: dict[str,Any], current_template_doc: dict[str,Any])->dict[str,Any]:
    rev=doc.get('AIR_HANDOFF_CARD',{}).get('card_revision')
    if rev==15:
        mid=migrate_rev15_to_rev16(doc,current_template_doc)
        return migrate_rev16_to_rev17(mid,current_template_doc)
    if rev==16:
        return migrate_rev16_to_rev17(doc,current_template_doc)
    if rev==17:
        return copy.deepcopy(doc)
    raise MigrationError(f'unsupported source card_revision {rev!r}')
'''
        if marker not in old:
            raise SystemExit('migration main anchor missing')
        old = old.replace(marker, add + marker, 1)
    old = old.replace("out=migrate_rev15_to_rev16(inp,tmpl)", "out=migrate_to_current(inp,tmpl)")
    p.write_text(old, encoding='utf-8')


def patch_control_validator(root: Path) -> None:
    p = root / 'tools/validate_air_control_plane.py'
    t = p.read_text(encoding='utf-8')
    if 'v0.7.2 new-task binding transaction missing' not in t:
        anchor = "    req('AIR_GOVERNANCE_FAILURE_MODE_LEARNING_V1' in gov, 'missing Governance failure learning rule')\n"
        extra = anchor + "    req('AIR_NEW_TASK_BINDING_TRANSACTION_V2' in core, 'v0.7.2 new-task binding transaction missing')\n    req('AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1' in control, 'v0.7.2 primary response surface rule missing')\n    req('approval_scope_fingerprint' in gov, 'v0.7.2 approval fingerprint governance missing')\n"
        t = replace_once(t, anchor, extra, 'control validator markers')
    anchor2 = "    req(ar['natural_language_paraphrase_authority']=='NONE','natural-language approval has authority')\n"
    extra2 = anchor2 + "    req(ar.get('approval_scope_id_revision_suffix_required') is False,'approval scope suffix incorrectly required')\n    req(ar.get('approval_scope_fingerprint_required') is True,'approval fingerprint not required')\n    req(ar.get('scope_id_reuse_rule')=='SAME_APPROVAL_SCOPE_ID_WITH_DIFFERENT_FINGERPRINT_INVALID_REQUIRES_NEW_DISTINCT_ID','scope-id fingerprint reuse barrier missing')\n"
    if "scope-id fingerprint reuse barrier missing" not in t:
        t = replace_once(t, anchor2, extra2, 'control validator approval identity')
    anchor3 = "    req(mat['authority_ledger_required_before_effect'] is True,'authority ledger barrier missing')\n"
    extra3 = anchor3 + "    req(mat.get('exact_current_task_artifact_required') is True,'exact current task Artifact backstop missing')\n    req(mat.get('artifact_benchmark_admissibility_required') is True,'Artifact benchmark backstop missing')\n    req(mat.get('artifact_precheck_admissibility_required') is True,'Artifact precheck backstop missing')\n    req(mat.get('artifact_primary_visible_accounting_required') is True,'Artifact primary visibility/accounting backstop missing')\n    nt=cc.get('new_task_binding_transaction',{}); req(nt.get('required') is True and nt.get('inference_policy')=='PROHIBITED_AFTER_NEW_TASK_BOUNDARY_LATCH','new-task typed transaction missing')\n    req(nt.get('ordered_states',[])[-1:] == ['NEW_TASK_EXECUTION_ELIGIBLE'],'new-task transaction order incomplete')\n"
    if "exact current task Artifact backstop missing" not in t:
        t = replace_once(t, anchor3, extra3, 'control validator action backstop')
    anchor4 = "    routes={r['route_id']:r for r in rmap['routes']}\n"
    extra4 = anchor4 + "    ts=routes['RT.TASK_SWITCH']; req(ts.get('execution_semantics')=='DETERMINISTIC_PIPELINE' and ts.get('inference_policy')=='PROHIBITED','RT.TASK_SWITCH not deterministic')\n    req('DEP.NEW_TASK_ARTIFACT_COMPILED' in ts.get('requires',[]) and 'DEP.NEW_TASK_ARTIFACT_VISIBLE_ACCOUNTED' in ts.get('does_not_bypass',[]),'RT.TASK_SWITCH exact Artifact barriers missing')\n"
    if "RT.TASK_SWITCH not deterministic" not in t:
        t = replace_once(t, anchor4, extra4, 'control validator route task switch')
    anchor5 = "    fm=cc['failure_mode_registry']; req(fm['pre_retry_query_required'] is True,'failure-mode pre-retry query missing');"
    replacement5 = "    fm=cc['failure_mode_registry']; req(fm['pre_retry_query_required'] is True,'failure-mode pre-retry query missing'); req(fm.get('execution_defect_rejection_capture_required') is True,'execution-defect capture requirement missing'); req(fm.get('recovery_capture_rule')=='RT_RECOVERY_EVALUATES_REUSABLE_FAILURE_CAPTURE_BEFORE_END_RESPONSE','recovery failure-capture route missing');"
    if "execution-defect capture requirement missing" not in t:
        t = replace_once(t, anchor5, replacement5, 'control validator failure capture')
    p.write_text(t, encoding='utf-8')


def patch_control_mutations(root: Path) -> None:
    p = root / 'tools/test_air_control_plane_mutations.py'
    t = p.read_text(encoding='utf-8')
    if "wrong task Artifact accepted" not in t:
        anchor = "    cases.append(('surfaced ledger reduced to authority-only',m16))\n"
        extra = anchor + r'''    def m17(d):
        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['material_action_transaction']['exact_current_task_artifact_required']=False; save(p,o)
    cases.append(('wrong task Artifact accepted',m17))
    def m18(d):
        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); e=next(x for x in o['compiler_contract']['runtime_control_event_registry']['events'] if x['route_id']=='RT.TASK_SWITCH'); e['guards']=e['guards'][:1]; save(p,o)
    cases.append(('task switch new-task guards removed',m18))
    def m19(d):
        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['material_action_transaction']['artifact_benchmark_admissibility_required']=False; save(p,o)
    cases.append(('Artifact benchmark backstop removed',m19))
    def m20(d):
        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['material_action_transaction']['artifact_precheck_admissibility_required']=False; save(p,o)
    cases.append(('Artifact precheck backstop removed',m20))
    def m21(d):
        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['material_action_transaction']['artifact_primary_visible_accounting_required']=False; save(p,o)
    cases.append(('Artifact primary visibility backstop removed',m21))
    def m22(d):
        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['approval_response_resolution']['scope_id_reuse_rule']='REUSE_ALLOWED'; save(p,o)
    cases.append(('approval scope fingerprint reuse allowed',m22))
    def m23(d):
        p=d/'prompts/AIR_CONTROL_SURFACE.md'; x=p.read_text(encoding='utf-8').replace('Patch marker: AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1','Patch marker: REMOVED_PRIMARY_SURFACE',1); p.write_text(x,encoding='utf-8')
    cases.append(('primary response surface rule removed',m23))
    def m24(d):
        p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['failure_mode_registry']['execution_defect_rejection_capture_required']=False; save(p,o)
    cases.append(('execution defect failure capture removed',m24))
'''
        t = replace_once(t, anchor, extra, 'control mutation expansion')
    p.write_text(t, encoding='utf-8')


def patch_behavioral_validator(root: Path) -> None:
    p = root / 'tools/validate_air_behavioral_contracts.py'
    t = p.read_text(encoding='utf-8')
    if "'AIR_NEW_TASK_BINDING_TRANSACTION_V2'" not in t:
        t = t.replace("        'AIR_HANDOFF_PROVENANCE_FIDELITY_V1',\n", "        'AIR_HANDOFF_PROVENANCE_FIDELITY_V1',\n        'AIR_NEW_TASK_BINDING_TRANSACTION_V2',\n", 1)
    if "'AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1'" not in t:
        t = t.replace("        'AIR_CONTROL_HANDOFF_PROVENANCE_RENDERER_V1',\n", "        'AIR_CONTROL_HANDOFF_PROVENANCE_RENDERER_V1',\n        'AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1',\n", 1)
    old_expected = """    expected = [\n        'TURN_ENTRY_ALIGNMENT', 'CURRENT_ARTIFACT_BOUND', 'ACTIVE_LEASE', 'NON_NULL_RESOURCE_SCOPE_PIN',\n        'CURRENT_APPROVAL_WHEN_REQUIRED', 'CURRENT_AIR_GATE_ALLOW', 'AIR_ACTION_AUTHORIZATION_EMITTED',\n        'AUTHORITY_OBJECTS_LEDGER_COMMITTED', 'EFFECT_ATTEMPT', 'OBSERVED_EFFECT_EVIDENCE', 'POST_MATERIAL_EFFECT_ALIGNMENT',\n        'CANONICAL_AIR_ACTION_RECEIPT', 'POST_EFFECT_ARTIFACT_RECONCILIATION'\n    ]\n"""
    new_expected = """    expected = [\n        'TURN_ENTRY_ALIGNMENT', 'CURRENT_ARTIFACT_BOUND', 'CURRENT_TASK_ARTIFACT_EXACT_MATCH',\n        'CURRENT_ARTIFACT_BENCHMARK_ADMISSIBLE', 'CURRENT_ARTIFACT_PRECHECK_ADMISSIBLE',\n        'CURRENT_ARTIFACT_PRIMARY_VISIBLE_AND_ACCOUNTED', 'ACTIVE_LEASE', 'NON_NULL_RESOURCE_SCOPE_PIN',\n        'CURRENT_APPROVAL_WHEN_REQUIRED', 'CURRENT_AIR_GATE_ALLOW', 'AIR_ACTION_AUTHORIZATION_EMITTED',\n        'AUTHORITY_OBJECTS_LEDGER_COMMITTED', 'EFFECT_ATTEMPT', 'OBSERVED_EFFECT_EVIDENCE', 'POST_MATERIAL_EFFECT_ALIGNMENT',\n        'CANONICAL_AIR_ACTION_RECEIPT', 'POST_EFFECT_ARTIFACT_RECONCILIATION'\n    ]\n"""
    t = replace_once(t, old_expected, new_expected, 'behavioral expected action sequence')
    anchor = "    require(mat.get('prior_review_gate_may_be_reused_as_allow') is False, 'Starter improperly allows REVIEW Gate reuse as ALLOW')\n"
    extra = anchor + "    nt=cc.get('new_task_binding_transaction', {})\n    require(nt.get('ordered_states') == ['NEW_TASK_BOUNDARY_LATCHED','NEW_TASK_IDENTITY_RESOLVED','EXACT_TASK_ARTIFACT_COMPILED','TASK_BENCHMARK_DERIVED','ARTIFACT_PRECHECK_ADMISSIBLE','ATOMIC_ORBIT_0_BINDING_COMMITTED','PRIMARY_USER_VISIBLE_ARTIFACT_EMITTED','ARTIFACT_SURFACED_LEDGER_ACCOUNTED','NEW_TASK_EXECUTION_ELIGIBLE'], 'new-task transaction sequence mismatch')\n    require(nt.get('direct_action_or_material_delivery_before_completion') == 'PROHIBITED', 'new-task direct execution bypass allowed')\n"
    if 'new-task transaction sequence mismatch' not in t:
        t = replace_once(t, anchor, extra, 'behavioral new task transaction')
    anchor2 = "    require(bundle.get('atomic') is True, 'Route Map task-switch bundle not atomic')\n"
    extra2 = anchor2 + "    require(routes['RT.TASK_SWITCH'].get('execution_semantics') == 'DETERMINISTIC_PIPELINE', 'Route Map task-switch is not deterministic')\n    require(routes['RT.TASK_SWITCH'].get('new_task_binding_transaction', {}).get('direct_action_or_material_delivery_before_completion') == 'PROHIBITED', 'Route Map new-task bypass not prohibited')\n"
    if 'Route Map task-switch is not deterministic' not in t:
        t = replace_once(t, anchor2, extra2, 'behavioral route task switch')
    anchor3 = "    require('MAT-02-REVIEW-GATE-IMPLICITLY-UPGRADED' in mat_ids, 'REVIEW Gate regression fixture missing')\n"
    extra3 = anchor3 + "    ntb_ids={x.get('id') for x in fixtures.get('new_task_binding_barrier_negative_cases', [])}\n    require({f'NTB-{i:02d}-' for i in range(1,9)} == {next((p for p in {f'NTB-{i:02d}-' for i in range(1,9)} if str(cid).startswith(p)), '') for cid in ntb_ids} - {''}, 'new-task barrier fixture coverage incomplete')\n    asi={x.get('id') for x in fixtures.get('approval_scope_identity_cases', [])}; require({'ASI-01-SUFFIX-FREE-VALID','ASI-02-SUFFIX-NOT-REQUIRED','ASI-03-CHANGED-FINGERPRINT-REUSED-ID'} <= asi, 'approval identity fixtures missing')\n    prs={x.get('id') for x in fixtures.get('primary_response_surface_cases', [])}; require('PRS-01-COLLAPSED-HOST-SURFACE-NOT-EMISSION' in prs, 'primary surface fixture missing')\n"
    if 'new-task barrier fixture coverage incomplete' not in t:
        t = replace_once(t, anchor3, extra3, 'behavioral fixture coverage')
    p.write_text(t, encoding='utf-8')


def patch_behavioral_mutations(root: Path) -> None:
    p = root / 'tools/test_air_behavioral_contract_mutations.py'
    t = p.read_text(encoding='utf-8')
    if "new_task_transaction" not in t:
        anchor = "    ('route_bundle', mutate_route_bundle),\n"
        funcs_anchor = "\n\nMUTATIONS = [\n"
        funcs = r'''

def mutate_new_task_transaction(root: Path):
    p=root/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; x=load(p)
    x['compiler_contract']['new_task_binding_transaction']['ordered_states'].remove('ARTIFACT_SURFACED_LEDGER_ACCOUNTED'); dump(p,x)


def mutate_new_task_route_determinism(root: Path):
    p=root/'catalog/AIR_RUNTIME_ROUTE_MAP.json'; x=load(p)
    r=next(r for r in x['routes'] if r['route_id']=='RT.TASK_SWITCH'); r['inference_policy']='ALLOWED'; dump(p,x)
'''
        t = t.replace(funcs_anchor, funcs + funcs_anchor, 1)
        t = replace_once(t, anchor, anchor + "    ('new_task_transaction', mutate_new_task_transaction),\n    ('new_task_route_determinism', mutate_new_task_route_determinism),\n", 'behavioral mutation cases')
    p.write_text(t, encoding='utf-8')


def write_v072_seal_validator(root: Path) -> None:
    p = root / 'tools/validate_air_v072_release_seal.py'
    p.write_text(r'''from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
FOUNDATION='AIR_FOUNDATION_2_6_1_OBJECT_CONTRACT_SET_006'
STATUS='AIR_2_6_1_OBJECT_CONTRACT_SET_006_FIVE_PACKAGE_INDEX_V072_CANDIDATE_STATIC_VALIDATED'
COMPLETE='COMPLETE_FOR_AIR_2_6_1_OBJECT_CONTRACT_SET_006_V072_CANDIDATE_SPECIALIST_CATALOG'
CANDIDATE='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'
class E(Exception): pass
def req(c,m):
    if not c: raise E(m)
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    req((ROOT/'VERSION').read_text().strip()=='0.7.2','AIR Kit VERSION is not 0.7.2')
    core=(ROOT/'prompts/AIR_CORE_RUNTIME.md').read_text(); control=(ROOT/'prompts/AIR_CONTROL_SURFACE.md').read_text(); gov=(ROOT/'prompts/AIR_GOV.md').read_text(); starter=load(ROOT/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'); card=load(ROOT/'prompts/AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']; idx=load(ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'); rmap=load(ROOT/'catalog/AIR_RUNTIME_ROUTE_MAP.json')
    req('PROMPT_VERSION: 2.6.1' in core,'Core not 2.6.1'); req('PROMPT_VERSION: 2.6.1' in control,'Control not 2.6.1'); req('PROMPT_VERSION: 2.3.1' in gov,'Governance not 2.3.1'); req(starter['PROMPT_VERSION']=='2.6.1','Starter not 2.6.1'); req(card['schema_version']=='2.3.0' and card['card_revision']==17,'Handoff not schema 2.3.0 rev17')
    req('AIR_NEW_TASK_BINDING_TRANSACTION_V2' in core,'new-task binding transaction absent'); req('AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1' in control,'primary response surface law absent'); req('approval_scope_fingerprint' in gov,'approval fingerprint governance absent')
    nt=starter['compiler_contract']['new_task_binding_transaction']; req(nt['required'] is True and nt['ordered_states'][-1]=='NEW_TASK_EXECUTION_ELIGIBLE','Starter new-task transaction invalid')
    events={e['route_id']:e for e in starter['compiler_contract']['runtime_control_event_registry']['events']}; req(len(events['RT.TASK_SWITCH']['guards'])>=7,'Task-switch typed guards incomplete'); req(len(events['RT.ACTION']['guards'])>=12,'Action exact Artifact guards incomplete')
    req(rmap['MAP_VERSION']=='1.2.0','Route Map not 1.2.0'); routes={r['route_id']:r for r in rmap['routes']}; req(routes['RT.TASK_SWITCH'].get('execution_semantics')=='DETERMINISTIC_PIPELINE','Task Switch not deterministic in Route Map'); req('RT.TASK_SWITCH' in rmap['deterministic_pipeline_contract']['declared_route_ids'],'Task Switch absent from deterministic route catalog')
    req(idx['INDEX_VERSION']=='1.3.1','Index not 1.3.1'); req(idx['status']==STATUS,'Index candidate status mismatch'); req(idx['catalog_scope']['catalog_completeness_claim']==COMPLETE,'Index completeness mismatch'); req(idx['foundation_compatibility_catalog']['identity']==FOUNDATION,'Index Foundation mismatch'); req(idx['candidate_lifecycle_contract']['current_candidate_state']==CANDIDATE,'Index candidate lifecycle mismatch'); req(idx['validation_state']['behavioral_revalidation']=='PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE','unsupported behavioral PASS'); req(idx['validation_state']['release_publication_state']=='EXTERNAL_RELEASE_STATE_NOT_RUNTIME_AUTHORITY','publication boundary changed')
    req(len(idx['entries'])==5,'Index package count');
    for e in idx['entries']:
        req(e['package_version']=='2.5.0','Specialist package version changed'); req(e['foundation_compatibility_identity']==FOUNDATION,'Specialist Foundation compatibility stale'); req(e['availability_state']==CANDIDATE,'Specialist index availability not candidate'); m=list((ROOT/'profiles').glob('**/'+e['manifest_filename'])); req(len(m)==1,'manifest target missing'); req(e['manifest_sha256']==sha(m[0]),'manifest hash stale')
    fx=load(ROOT/'tests/air_contract_fixtures.json'); req(fx['foundation_identity']==FOUNDATION,'fixtures Foundation stale'); req(len(fx.get('new_task_binding_barrier_negative_cases',[]))==8,'new-task fixtures incomplete'); req(len(fx.get('approval_scope_identity_cases',[]))>=3,'approval identity fixtures incomplete'); req(len(fx.get('repository_patch_reconciliation_cases',[]))>=2,'repo reconciliation fixtures incomplete')
    print('AIR v0.7.2 candidate-seal validation: PASS'); print('foundation',FOUNDATION); print('handoff_revision',17); print('specialist_packages',5); print('behavioral_evidence','PENDING'); print('publication_state','EXTERNAL_ONLY')
if __name__=='__main__':
    try: main()
    except (E,KeyError,ValueError) as e:
        print('AIR v0.7.2 candidate-seal validation: FAIL:',e,file=sys.stderr); raise SystemExit(1)
''', encoding='utf-8')


def write_v072_seal_mutations(root: Path) -> None:
    p = root / 'tools/test_air_v072_release_seal_mutations.py'
    p.write_text(r'''from __future__ import annotations
import json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path('.').resolve(); VAL=ROOT/'tools/validate_air_v072_release_seal.py'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def run(d): return subprocess.run([sys.executable,str(VAL),str(d)],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode
def main():
    if run(ROOT)!=0: raise SystemExit('v0.7.2 candidate-seal mutation baseline failed')
    cases=[]
    def add(n,f): cases.append((n,f))
    def idxmut(fn):
        def m(d): p=d/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'; o=load(p); fn(o); dump(p,o)
        return m
    add('V072-N01-STATUS-STALE',idxmut(lambda o:o.__setitem__('status','STALE')))
    add('V072-N02-ENTRY-RELEASED-PREMATURELY',idxmut(lambda o:o['entries'][0].__setitem__('availability_state','RELEASE_CATALOG_ENTRY')))
    add('V072-N03-UNSUPPORTED-BEHAVIORAL-PASS',idxmut(lambda o:o['validation_state'].__setitem__('behavioral_revalidation','BEHAVIORAL_REVALIDATION_PASS')))
    def m4(d): p=d/'prompts/AIR_DEFAULT_STARTER_PROFILE.json'; o=load(p); o['compiler_contract']['new_task_binding_transaction']['ordered_states'].remove('ARTIFACT_SURFACED_LEDGER_ACCOUNTED'); dump(p,o)
    add('V072-N04-NEW-TASK-ACCOUNTING-REMOVED',m4)
    def m5(d): p=d/'prompts/AIR_CONTROL_SURFACE.md'; p.write_text(p.read_text().replace('AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1','REMOVED_PRIMARY_SURFACE',1))
    add('V072-N05-PRIMARY-SURFACE-REMOVED',m5)
    for name,fn in cases:
        with tempfile.TemporaryDirectory(prefix='v072-seal-mut-') as td:
            d=Path(td)/'repo'; shutil.copytree(ROOT,d,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc')); fn(d)
            if run(d)==0: raise SystemExit('MUTATION SURVIVED: '+name)
            print(name+': KILLED')
    print(f'AIR v0.7.2 candidate-seal mutation suite: PASS ({len(cases)}/{len(cases)})')
if __name__=='__main__': main()
''', encoding='utf-8')


def patch_suite(root: Path) -> None:
    p = root / 'tools/validate_air_suite.py'
    t = p.read_text(encoding='utf-8')
    t = replace_once(t, "run_stage('v071_release_seal', [py, 'tools/validate_air_v071_release_seal.py'])", "run_stage('v072_candidate_seal', [py, 'tools/validate_air_v072_release_seal.py'])", 'suite v072 seal')
    t = replace_once(t, "run_stage('v071_release_seal_mutations', [py, 'tools/test_air_v071_release_seal_mutations.py'])", "run_stage('v072_candidate_seal_mutations', [py, 'tools/test_air_v072_release_seal_mutations.py'])", 'suite v072 seal mutations')
    p.write_text(t, encoding='utf-8')


def patch_version(root: Path) -> None:
    (root / 'VERSION').write_text('0.7.2\n', encoding='utf-8')


def patch_r3_handoff_mutation_compat(root: Path) -> None:
    pass


def patch_current_json_identity(root: Path) -> None:
    patch_profiles(root)


def patch_repo_reconciliation_contract(root: Path) -> None:
    pass


def main(root: Path) -> None:
    patch_core(root)
    patch_control(root)
    patch_gov(root)
    patch_starter(root)
    patch_handoff(root)
    patch_readme(root)
    patch_fixtures(root)
    patch_inventory(root)
    patch_migration_tool(root)
    patch_release_validator(root)
    patch_r7_validator(root)
    patch_r3_validator(root)
    patch_r3_mutations(root)
    patch_control_validator(root)
    patch_control_mutations(root)
    patch_behavioral_validator(root)
    patch_behavioral_mutations(root)
    patch_suite(root)
    write_v072_seal_validator(root)
    write_v072_seal_mutations(root)
    patch_version(root)
    patch_current_json_identity(root)
    update_route_map(root)
    patch_index(root)
    print('AIR v0.7.2 hardening semantic patch applied')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('root', nargs='?', default='.')
    args = ap.parse_args()
    main(Path(args.root).resolve())
