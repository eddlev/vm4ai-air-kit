from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path('.')

class ValidationError(Exception):
    pass


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValidationError(msg)


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def main() -> None:
    core = (ROOT / 'prompts/AIR_CORE_RUNTIME.md').read_text(encoding='utf-8')
    control = (ROOT / 'prompts/AIR_CONTROL_SURFACE.md').read_text(encoding='utf-8')
    starter = load('prompts/AIR_DEFAULT_STARTER_PROFILE.json')
    handoff = load('prompts/AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']
    route_map = load('catalog/AIR_RUNTIME_ROUTE_MAP.json')
    fixtures = load('tests/air_contract_fixtures.json')

    core_markers = [
        'AIR_TRANSITION_EMISSION_TRANSACTION_V1',
        'AIR_DETERMINISTIC_PROJECTION_ORDER_INTEGRITY_V1',
        'AIR_FORMAL_OBJECT_CONSTRUCTOR_VALIDATION_V1',
        'AIR_MATERIAL_ACTION_TRANSACTION_V1',
        'AIR_HANDOFF_PROVENANCE_FIDELITY_V1',
        'AIR_NEW_TASK_BINDING_TRANSACTION_V2',
        'AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_V1',
    ]
    for marker in core_markers:
        require(('Patch marker: ' + marker) in core, f'missing Core behavioral hardening marker {marker}')
    for marker in [
        'AIR_CONTROL_TRANSITION_EMISSION_TRANSACTION_RENDERER_V1',
        'AIR_CONTROL_MATERIAL_ACTION_TRANSACTION_RENDERER_V1',
        'AIR_CONTROL_FORMAL_OBJECT_CONSTRUCTOR_GUARD_V1',
        'AIR_CONTROL_HANDOFF_PROVENANCE_RENDERER_V1',
        'AIR_PRIMARY_USER_VISIBLE_RESPONSE_SURFACE_V1',
        'AIR_COGNITIVE_SCOPE_AUTHORITY_ISOLATION_SURFACE_V1',
    ]:
        require(('Patch marker: ' + marker) in control, f'missing Control hardening marker {marker}')

    cc = starter.get('compiler_contract', {})
    trans = cc.get('transition_emission_transaction', {})
    require(trans.get('required') is True, 'Starter transition emission transaction missing')
    require(trans.get('orbit_transition_atomic_bundle') == ['AIR_SESSION', 'AIR_PROJECT_EXECUTION_MAP', 'AIR_ARTIFACT'], 'Starter Orbit transition bundle mismatch')
    require(trans.get('failure_behavior') == 'FAIL_CLOSED_BEFORE_ORDINARY_CONTINUATION', 'Starter transition failure behavior mismatch')

    mat = cc.get('material_action_transaction', {})
    expected = [
        'TURN_ENTRY_ALIGNMENT', 'CURRENT_ARTIFACT_BOUND', 'CURRENT_TASK_ARTIFACT_EXACT_MATCH',
        'CURRENT_ARTIFACT_BENCHMARK_ADMISSIBLE', 'CURRENT_ARTIFACT_PRECHECK_ADMISSIBLE',
        'CURRENT_ARTIFACT_PRIMARY_VISIBLE_AND_ACCOUNTED', 'ACTIVE_LEASE', 'NON_NULL_RESOURCE_SCOPE_PIN',
        'CURRENT_APPROVAL_WHEN_REQUIRED', 'CURRENT_AIR_GATE_ALLOW', 'AIR_ACTION_AUTHORIZATION_EMITTED',
        'AUTHORITY_OBJECTS_LEDGER_COMMITTED', 'EFFECT_ATTEMPT', 'OBSERVED_EFFECT_EVIDENCE', 'POST_MATERIAL_EFFECT_ALIGNMENT',
        'CANONICAL_AIR_ACTION_RECEIPT', 'POST_EFFECT_ARTIFACT_RECONCILIATION'
    ]
    require(mat.get('ordered_pre_and_post_effect_states') == expected, 'Starter material action transaction sequence mismatch')
    require(mat.get('post_effect_alignment_profile') == 'POST_MATERIAL_EFFECT', 'Starter post-effect alignment profile mismatch')
    require(mat.get('receipt_record_class') == 'ACTION_RECEIPT_RECORD', 'Starter receipt record class mismatch')
    require(mat.get('authorization_receipt_exact_match_required') is True, 'Starter authorization/receipt identity match not required')
    require(mat.get('prior_review_gate_may_be_reused_as_allow') is False, 'Starter improperly allows REVIEW Gate reuse as ALLOW')
    nt=cc.get('new_task_binding_transaction', {})
    require(nt.get('ordered_states') == ['NEW_TASK_BOUNDARY_LATCHED','NEW_TASK_IDENTITY_RESOLVED','EXACT_TASK_ARTIFACT_COMPILED','TASK_BENCHMARK_DERIVED','ARTIFACT_PRECHECK_ADMISSIBLE','ATOMIC_ORBIT_0_BINDING_COMMITTED','PRIMARY_USER_VISIBLE_ARTIFACT_EMITTED','ARTIFACT_SURFACED_LEDGER_ACCOUNTED','NEW_TASK_EXECUTION_ELIGIBLE'], 'new-task transaction sequence mismatch')
    require(nt.get('direct_action_or_material_delivery_before_completion') == 'PROHIBITED', 'new-task direct execution bypass allowed')
    cs=cc.get('cognitive_scope_authority_isolation', {})
    require(cs.get('required') is True and cs.get('cognition_to_control') == 'PROHIBITED', 'cognitive scope authority isolation missing')
    require(cs.get('validated_contribution_ingress') == 'EXPLICIT_DECLARED_INGESTION_ONLY', 'cognitive scope ingestion boundary missing')
    require(cs.get('authority_escape_failure_class') == 'COGNITIVE_AUTHORITY_ESCAPE', 'cognitive authority escape failure class missing')
    require('prior_hold_gate_may_be_reused_as_allow' not in mat, 'Starter retains undefined HOLD Gate mirror')

    ctor = cc.get('formal_object_constructor_validation', {})
    require(ctor.get('required') is True, 'Starter formal constructor validation missing')
    require('CURRENT_EVALUATION_BASIS_WHEN_REQUIRED' in ctor.get('checks', []), 'constructor evaluation-basis check missing')
    require('ACTION_RECEIPT_AUTHORIZATION_REF_MATCHES_CONSUMED_AUTHORIZATION' in ctor.get('checks', []), 'constructor auth-ref check missing')
    require('FAILURE_MODE_RESERVED_LEDGER_ENTRY_REF_VALID' in ctor.get('checks', []), 'failure-mode reserved ledger-entry constructor check missing')

    led = cc.get('surfaced_object_ledger', {})
    reserve = led.get('failure_record_entry_reservation', {})
    require(led.get('entry_reference_field') == 'ledger_entry_ref', 'surfaced ledger entry reference field missing')
    require(reserve.get('reservation_state') == 'RESERVED_NOT_EMITTED_NOT_AUTHORITY', 'failure record ledger reservation gained visibility/authority')
    require(reserve.get('commit_rule') == 'COMMIT_ONLY_AFTER_EXACT_CANONICAL_OBJECT_VISIBLE_EMISSION_WITH_MATCHING_REF_AND_HASH', 'failure record ledger reservation commit rule mismatch')
    fm = cc.get('failure_mode_registry', {})
    expected_failure_sequence = [
        'RESERVE_NEXT_LEDGER_ENTRY_REF',
        'CONSTRUCT_FAILURE_RECORD_WITH_RESERVED_SOURCE_LEDGER_ENTRY_REF',
        'CANONICALIZE_AND_HASH_FAILURE_RECORD',
        'VISIBLY_EMIT_FAILURE_RECORD',
        'COMMIT_MATCHING_USER_VISIBLE_EMITTED_LEDGER_ENTRY_WITH_EXACT_HASH',
        'ONLY_THEN_SOURCE_LEDGER_ENTRY_REF_RESOLVES',
    ]
    require(fm.get('first_emission_transaction') == expected_failure_sequence, 'failure-mode first-emission ledger transaction mismatch')
    require(fm.get('source_ledger_entry_ref_semantics') == 'SELF_FIRST_COMMITTED_SURFACED_LEDGER_ENTRY', 'failure-mode self-ledger reference semantics mismatch')

    proj = cc.get('deterministic_projection_order_integrity', {})
    require(proj.get('required') is True, 'Starter deterministic projection order contract missing')
    require(proj.get('order_policy') == 'EXACT_DECLARED_ORDER', 'Starter projection order policy mismatch')
    require(proj.get('commuting_operations_may_reorder') is False, 'Starter allows commuting-step reorder')

    hp = cc.get('handoff_provenance_fidelity', {})
    require(hp.get('historical_authorization_policy') == 'OBSERVED_SURFACED_CANONICAL_OBJECT_ONLY', 'Starter handoff authorization provenance policy mismatch')
    require(hp.get('unsurfaced_authorization_reconstruction') == 'PROHIBITED', 'Starter allows authorization reconstruction')

    ags = handoff.get('action_governance_state', {})
    policy = ags.get('provenance_policy', {})
    require(policy.get('historical_authorization_recording') == 'OBSERVED_SURFACED_CANONICAL_OBJECT_ONLY', 'Handoff observed-only authorization policy missing')
    require(policy.get('unsurfaced_authorization_reconstruction') == 'PROHIBITED', 'Handoff authorization reconstruction not prohibited')
    require(policy.get('retroactive_authorization_prohibited') is True, 'Handoff retrospective authorization boundary missing')
    forbidden = handoff.get('schema_manifest', {}).get('forbidden_states', [])
    require(any('Historical AIR_ACTION_AUTHORIZATION synthesized' in x for x in forbidden), 'Handoff false-history forbidden state missing')
    require('ledger_entry_ref' in handoff.get('surfaced_object_ledger_state', {}).get('entry_requirements', {}).get('required_fields', []), 'Handoff ledger history omits ledger_entry_ref')
    require(handoff.get('failure_mode_state', {}).get('source_ledger_entry_ref_semantics') == 'SELF_FIRST_COMMITTED_SURFACED_LEDGER_ENTRY', 'Handoff failure-mode ledger semantics mismatch')

    routes = {r['route_id']: r for r in route_map.get('routes', [])}
    bundle = routes['RT.TASK_SWITCH'].get('transition_emission_bundle', {})
    require(bundle.get('members') == ['AIR_SESSION', 'AIR_PROJECT_EXECUTION_MAP', 'AIR_ARTIFACT'], 'Route Map task-switch atomic bundle mismatch')
    require(bundle.get('atomic') is True, 'Route Map task-switch bundle not atomic')
    require(routes['RT.TASK_SWITCH'].get('execution_semantics') == 'DETERMINISTIC_PIPELINE' and routes['RT.TASK_SWITCH'].get('inference_policy') == 'PROHIBITED', 'Route Map task-switch is not deterministic')
    require(routes['RT.TASK_SWITCH'].get('new_task_binding_transaction', {}).get('direct_action_or_material_delivery_before_completion') == 'PROHIBITED', 'Route Map new-task bypass not prohibited')
    action = routes['RT.ACTION'].get('material_action_transaction', {})
    require(action.get('authorization_visible_before_effect') is True, 'Route Map action authorization visibility mismatch')
    require(action.get('resource_scope_pin_required') is True, 'Route Map action scope-pin requirement missing')
    require(action.get('post_effect_alignment_profile') == 'POST_MATERIAL_EFFECT', 'Route Map action post-effect profile mismatch')
    receipt = routes['RT.RECEIPT'].get('material_action_transaction', {})
    require(receipt.get('receipt_record_class') == 'ACTION_RECEIPT_RECORD', 'Route Map receipt record class mismatch')
    require(receipt.get('authorization_ref_match') == 'EXACT_CONSUMED_AUTHORIZATION', 'Route Map receipt authorization match mismatch')
    hroute = routes['RT.HANDOFF_CREATE'].get('handoff_provenance_policy', {})
    require(hroute.get('observed_object_identities_only') is True, 'Route Map handoff observed-only provenance missing')
    require(hroute.get('unsurfaced_authorization_reconstruction') == 'PROHIBITED', 'Route Map handoff reconstruction policy mismatch')

    emission_ids = {x.get('id') for x in fixtures.get('emission_closure_cases', [])}
    require({'EC-07-ORBIT-RESUME-ATOMIC-BUNDLE', 'EC-08-NEW-SIDE-TASK-ORBIT-BUNDLE'} <= emission_ids, 'Orbit transition regression fixtures missing')
    dp_ids = {x.get('id') for x in fixtures.get('deterministic_pipeline_negative_cases', [])}
    require('DP-05-FUTURE-PROJECTION-ORDER' in dp_ids, 'deterministic projection-order fixture missing')
    mat_ids = {x.get('id') for x in fixtures.get('material_action_transaction_negative_cases', [])}
    require({f'MAT-{i:02d}-' for i in range(1, 10)} == {next((prefix for prefix in {f'MAT-{i:02d}-' for i in range(1, 10)} if str(cid).startswith(prefix)), '') for cid in mat_ids if str(cid).startswith('MAT-')} - {''}, 'material action transaction fixture coverage incomplete')
    require('MAT-02-REVIEW-GATE-IMPLICITLY-UPGRADED' in mat_ids, 'REVIEW Gate regression fixture missing')
    ntb_ids={x.get('id') for x in fixtures.get('new_task_binding_barrier_negative_cases', [])}
    require({f'NTB-{i:02d}-' for i in range(1,9)} == {next((p for p in {f'NTB-{i:02d}-' for i in range(1,9)} if str(cid).startswith(p)), '') for cid in ntb_ids} - {''}, 'new-task barrier fixture coverage incomplete')
    asi={x.get('id') for x in fixtures.get('approval_scope_identity_cases', [])}; require({'ASI-01-SUFFIX-FREE-VALID','ASI-02-SUFFIX-NOT-REQUIRED','ASI-03-CHANGED-FINGERPRINT-REUSED-ID'} <= asi, 'approval identity fixtures missing')
    prs={x.get('id') for x in fixtures.get('primary_response_surface_cases', [])}; require('PRS-01-COLLAPSED-HOST-SURFACE-NOT-EMISSION' in prs, 'primary surface fixture missing')
    csa={x.get('id') for x in fixtures.get('cognitive_scope_authority_cases', [])}; require({'CSA-01-DIRECT-TASK-IDENTITY-MUTATION','CSA-03-DIRECT-APPROVAL-MUTATION','CSA-06-DETERMINISTIC-ROUTE-REORDER','CSA-P01-VALIDATED-EXPLICIT-INGESTION','CSA-P02-HANDOFF-NONAUTHORITY'} <= csa, 'cognitive scope fixtures missing')
    handoff_ids = {x.get('id') for x in fixtures.get('handoff_negative_cases', [])}
    require({'HC-02-FALSE-HISTORICAL-AUTHORIZATION', 'HC-03-PRIOR-EFFECT-AUTHORIZATION-UPGRADE'} <= handoff_ids, 'handoff provenance fixtures missing')
    failure_ids = {x.get('id') for x in fixtures.get('failure_mode_learning_cases', [])}
    require({'FM-07-FIRST-EMISSION-LEDGER-RESERVATION', 'FM-08-FAILURE-LEDGER-REF-MISMATCH'} <= failure_ids, 'failure-mode ledger regression fixtures missing')
    cw2 = next(x for x in fixtures.get('copywriting_behavior_cases', []) if x.get('id') == 'CW-BEH-02-MISSING-DOMAIN-TRUTH')
    joined = ' '.join(cw2.get('acceptable_runtime_outcomes', [])).lower()
    require('independently satisfiable source-supported remainder' in joined, 'CW-BEH-02 safe remainder outcome missing')
    require('no invented product or domain truth' in cw2.get('invariants', []), 'CW-BEH-02 no-invention invariant missing')


    # R6 package-local behavioral contradiction regressions.
    r6_cases = fixtures.get('r6_package_local_behavior_cases', [])
    r6_ids = {x.get('id') for x in r6_cases}
    require({
        'GOV-BEH-01-ALREADY-SATISFIED',
        'GOV-BEH-02-ONE-MISSING',
        'CW-BEH-04-FURTHER-SEARCH-NO-PASS',
        'CW-BEH-05-PASS-AND-STOPPED',
        'CW-BEH-06-PASS-BUT-FURTHER-SEARCH',
    } <= r6_ids, 'R6 package-local behavior fixtures missing')

    gov = load('profiles/governance specialist/AIR_AI_GOVERNANCE_SPECIALIST.json')
    boot = gov['source_layer']['source_access_boot_protocol']
    require(boot.get('visible_request_required') == 'CONDITIONAL_ON_MATERIAL_REQUIRED_INPUT_GAP', 'Governance boot request is not conditional')
    require(boot.get('pre_request_context_check_required') is True, 'Governance pre-request context check missing')
    decision = boot.get('request_decision_contract', {})
    all_ok = decision.get('all_material_inputs_available', {})
    one_gap = decision.get('material_required_input_gap_remaining', {})
    require(all_ok.get('emit_user_information_request') is False and all_ok.get('action') == 'ACKNOWLEDGE_CURRENT_SOURCE_ACCESS_STATE', 'Governance already-satisfied state still requests input')
    require(one_gap.get('emit_user_information_request') is True and one_gap.get('action') == 'REQUEST_SMALLEST_EXACT_MISSING_INPUT', 'Governance missing-input state does not request smallest exact input')
    require('request_once_at_boot' not in boot, 'Governance unconditional boot request list remains')
    require(not any(x == 'Ask for source inventory and access mode at boot before material governance mapping.' for x in gov.get('execution_constraints', [])), 'Governance unconditional boot execution constraint remains')
    require(gov['source_layer']['source_access_boot_protocol'].get('default_if_paid_material_absent') == 'PUBLIC_SOURCE_ONLY', 'Governance PUBLIC_SOURCE_ONLY fallback changed')

    cw = load('profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json')
    opt = cw.get('step_optimality_contribution_contract', {}).get('CW06_COMPARE_AND_SELECT', {})
    adv = opt.get('advance_to_cw07_requires', {})
    search = opt.get('further_search_branch', {})
    require(adv.get('candidate_contribution_state') == 'PASS_CANDIDATE', 'CW06 pass candidate requirement missing')
    require(adv.get('further_search_justified') is False, 'CW06 advance permits further search')
    require(adv.get('proportional_stopping_basis_recorded') is True, 'CW06 proportional stopping basis not required')
    require(adv.get('material_unresolved_domination') is False, 'CW06 advance permits unresolved domination')
    require(search.get('when', {}).get('further_search_justified') is True and search.get('advance_to_cw07') is False and search.get('next_step') == 'CW04_FORM_CANDIDATE_STRUCTURE', 'CW06 further-search branch does not remain in search/comparison')
    for coll in ('method_steps', 'ordered_steps'):
        step = next(x for x in cw[coll] if x.get('step_id') == 'CW06_COMPARE_AND_SELECT')
        require(step.get('branch_contract_ref') == 'step_optimality_contribution_contract.CW06_COMPARE_AND_SELECT', f'CW06 branch ref missing in {coll}')
        require(step.get('further_search_route') == 'CW04_FORM_CANDIDATE_STRUCTURE', f'CW06 further-search route missing in {coll}')
        joined = ' '.join(step.get('evidence_to_advance', []))
        require(' or further search is justified' not in joined, f'CW06 premature OR condition remains in {coll}')
        require('further_search_justified is false' in joined and 'proportional_stopping_basis_recorded is true' in joined, f'CW06 stopping evidence incomplete in {coll}')
    require(cw.get('authority_boundary', {}).get('positive_material_execution_authority_source') == 'SOLE_BOUND_ORBIT_0_AIR_ARTIFACT', 'Copywriting authority boundary changed')

    print('AIR behavioral transaction contract validation: PASS')
    print('Orbit transition atomic bundle: PASS')
    print('Material action deterministic transaction: PASS')
    print('Formal object constructor guard: PASS')
    print('Failure record ledger first-emission transaction: PASS')
    print('Handoff observed-only provenance: PASS')
    print('Deterministic projection order integrity: PASS')
    print('CW-BEH-02 safe partial fulfillment fixture: PRESENT')

if __name__ == '__main__':
    try:
        main()
    except ValidationError as exc:
        print(f'AIR behavioral transaction contract validation: FAIL: {exc}', file=sys.stderr)
        raise SystemExit(1)
