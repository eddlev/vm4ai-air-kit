from pathlib import Path
import json

ROOT = Path('.')
P = ROOT / 'prompts'

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one occurrence, found {count}')
    return text.replace(old, new, 1)

path = P / 'AIR_CORE_RUNTIME.md'
s = path.read_text(encoding='utf-8')
s = replace_once(s, 'PROMPT_VERSION: 2.4.0', 'PROMPT_VERSION: 2.4.1', 'core version')
old = '''Canonical test-evidence classes:\n- REPRODUCIBLE_EXECUTABLE\n- REPLAYABLE_EVALUATION\n- MANUAL_REVIEW_REQUIRED\n\nEvidence boundaries:\n- REPRODUCIBLE_EXECUTABLE requires actual executable definitions and observed run evidence.\n- REPLAYABLE_EVALUATION requires disclosed inputs, prompt or evaluation procedure when publishable, rubric, expected boundary, observed output, model or tool identity when available, and decision evidence.\n- MANUAL_REVIEW_REQUIRED requires the review question, evidence inspected, acceptance and rejection criteria, reviewer decision, and unresolved uncertainty.\n- Do not label manual, qualitative, model-judged, or prompt-side review as deterministic automated execution.\n- Do not expose hidden reasoning, private chain of thought, credentials, secrets, restricted source text, or unavailable backend logs.\n- Redaction or sanitization must be visible and must state what evidence class or reproducibility limit it creates.\n- A produced file is evidence only for what its content, identity, source, and execution record support.\n'''
new = '''Canonical test-evidence classes:\n- REPRODUCIBLE_EXECUTABLE\n- REPLAYABLE_EVALUATION\n- MANUAL_REVIEW_REQUIRED\n\nTest run identity minimum contract:\nEvery material run used to support a quantitative pass claim must preserve a test-run identity sufficient to distinguish the exact run from a model-authored summary. When available and applicable, preserve:\n- run_id\n- suite_id and suite_sha256 or equivalent immutable suite identity\n- definition_or_manifest_sha256\n- fixture_set_sha256 and exact material input hashes\n- source revision or commit identity\n- runner identity and runner version\n- runtime identity and environment fingerprint\n- working directory and exact execution command or argv\n- random seed or explicit NOT_APPLICABLE state\n- locale, timezone, clock policy, and other material nondeterminism controls\n- network policy and external dependency policy\n- repetition policy and observed run count\n- per-run decision fingerprint and combined result fingerprint\n- reproducibility class and reproducibility state\n\nDeterministic executable claim law:\n- REPRODUCIBLE_EXECUTABLE requires actual executable definitions and tool- or process-observed run evidence. A model-generated statement that tests passed cannot self-authorize this class.\n- A deterministic release-grade claim requires exact suite, fixture, material input, source revision, runner, runtime, and environment identities plus explicit nondeterminism controls.\n- Release-grade deterministic suites must run at least three independent executions in freshly reset or equivalently isolated environments when technically feasible.\n- All required executions must pass and their decision fingerprints must be identical.\n- Any pass/fail divergence, material output divergence covered by the test definition, unresolved clock/random/network dependence, or environment ambiguity sets reproducibility_state = FLAKY_OR_NONDETERMINISTIC.\n- FLAKY_OR_NONDETERMINISTIC results must not be summarized as deterministic even when the latest execution is green.\n- If network isolation cannot be enforced, declare the dependency and reproducibility limit. Do not imply hermetic execution.\n\nReplayable evaluation law:\n- REPLAYABLE_EVALUATION requires disclosed inputs, prompt or evaluation procedure when publishable, rubric, expected boundary, observed output, model or tool identity when available, and decision evidence.\n- Freeze model/provider identity, model configuration, prompts, tools made available, material tool outputs, fixtures, evaluator procedure, rubric, thresholds, and material seeds when supported.\n- Model-dependent or model-judged evaluations are not deterministic merely because temperature is zero or a seed is supplied.\n- A stability claim requires a predeclared repetition count and must report aggregate pass rate plus unstable case identifiers; at least three independent runs are required for a release-grade stability claim unless a stricter task-specific rule applies.\n\nManual review law:\n- MANUAL_REVIEW_REQUIRED requires the review question, evidence inspected, acceptance and rejection criteria, reviewer decision, and unresolved uncertainty.\n- Manual review items must not be silently folded into an automated X/X pass total. Split automated, replayable, and manual counts whenever classes are mixed.\n\nQuantitative pass-claim law:\n- A bare statement such as `150/150 tests passed` is insufficient for a deterministic or release-grade claim.\n- For REPRODUCIBLE_EXECUTABLE, pair the count with run identity, reproducibility state, evidence reference, and repetition result.\n- For REPLAYABLE_EVALUATION, say that the cases passed on the recorded run and explicitly state that the evaluation is not deterministic; include aggregate stability evidence when claimed.\n- For mixed evidence classes, report class-separated counts rather than one undifferentiated total.\n\nEvidence boundaries:\n- Do not label manual, qualitative, model-judged, or prompt-side review as deterministic automated execution.\n- Do not expose hidden reasoning, private chain of thought, credentials, secrets, restricted source text, or unavailable backend logs.\n- Redaction or sanitization must be visible and must state what evidence class or reproducibility limit it creates.\n- A produced file is evidence only for what its content, identity, source, and execution record support.\n- Passing verification demonstrates conformance only to the tests or evaluations that actually ran; intent reconciliation remains required before closure.\n'''
s = replace_once(s, old, new, 'core evidence law')
s = replace_once(s, '''- produced_test_evidence_refs\n- reproducibility_limits\n- rerun_required_for_full_evidence\n''', '''- produced_test_evidence_refs\n- test_run_identity_records\n- reproducibility_state\n- reproducibility_limits\n- unstable_test_ids when applicable\n- rerun_required_for_full_evidence\n''', 'core state carriers')
path.write_text(s, encoding='utf-8')

path = P / 'AIR_CONTROL_SURFACE.md'
s = path.read_text(encoding='utf-8')
s = replace_once(s, 'PROMPT_VERSION: 2.4.0', 'PROMPT_VERSION: 2.4.1', 'control version')
s = replace_once(s, '''When `air -t on` is active and tests are run, surface links or exact identities for the available test suite, run manifest, per-test results, run log, fixtures, and review README. Keep the prose summary compact.\n\nWhen `air -t off` is active:\n''', '''When `air -t on` is active and tests are run, surface links or exact identities for the available test suite, run manifest, per-test results, run log, fixtures, and review README. Keep the prose summary compact.\n\nQuantitative result surface:\n- Never use a naked `X/X passed` line as proof of deterministic execution.\n- For deterministic executable evidence, prefer: `150/150 PASS — REPRODUCIBLE_EXECUTABLE — run <id> — 3/3 isolated executions identical` when those facts are actually evidenced.\n- For replayable model/evaluator evidence, prefer: `150/150 cases passed on this recorded run — REPLAYABLE_EVALUATION — not deterministic`, followed by aggregate stability results when available.\n- For mixed evidence classes, split the totals, for example: `142 executable checks passed; 8 manual review items accepted`.\n- If required repeated runs diverge, surface `REPRODUCIBILITY_FAILURE` or `FLAKY_OR_NONDETERMINISTIC`, identify unstable tests, and do not collapse the latest green run into a deterministic pass claim.\n- A surfaced AIR record reports the evidence AIR received or observed; it is not independent proof unless the cited tool, runner, backend, or reviewer evidence supports the claim.\n\nWhen `air -t off` is active:\n''', 'control quantitative result surface')
path.write_text(s, encoding='utf-8')

path = P / 'AIR_DEFAULT_STARTER_PROFILE.json'
data = json.loads(path.read_text(encoding='utf-8'))
data['PROMPT_VERSION'] = '2.4.1'
contract = data['compiler_contract']['test_evidence_reproducibility_contract']
contract['test_run_identity_required_fields'] = ['run_id','suite_id','suite_sha256_or_equivalent','definition_or_manifest_sha256','fixture_set_sha256','material_input_hashes','source_revision','runner_identity','runner_version','runtime_identity','environment_fingerprint','working_directory','execution_command_or_argv','random_seed_or_not_applicable','nondeterminism_controls','network_policy','repetition_policy','observed_run_count','decision_fingerprints','result_fingerprint','reproducibility_class','reproducibility_state']
contract['release_grade_deterministic_rule'] = {'minimum_independent_executions':3,'environment_rule':'Use freshly reset or equivalently isolated environments when technically feasible.','pass_rule':'All required executions pass and decision fingerprints are identical.','failure_state':'FLAKY_OR_NONDETERMINISTIC','network_rule':'Enforce isolation when technically available; otherwise declare external dependencies and reproducibility limits.','model_self_attestation_is_evidence':False}
contract['replayable_evaluation_rule'] = {'deterministic_claim_allowed':False,'freeze_when_available':['model_provider_and_identity','model_configuration','prompts','tools_available','material_tool_outputs','fixtures','evaluator_procedure','rubric','thresholds','supported_seeds'],'release_grade_minimum_independent_runs_for_stability_claim':3,'report':['recorded_run_result','aggregate_pass_rate','unstable_case_ids','reproducibility_limits']}
contract['quantitative_pass_claim_rule'] = 'Bare X/X passed is insufficient for deterministic or release-grade claims. Pair executable counts with run identity and reproducibility state; label replayable evaluations as non-deterministic; split mixed evidence classes.'
data['typed_registries']['runtime_states']['test_reproducibility_state'] = ['UNVERIFIED','DETERMINISTIC_CONFIRMED','REPLAYABLE_ONLY','MANUAL_ONLY','FLAKY_OR_NONDETERMINISTIC']
data['validation_contract']['required_version'] = '2.4.1'
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

path = P / 'AIR_HANDOFF_CARD_TEMPLATE.json'
data = json.loads(path.read_text(encoding='utf-8'))
card = data['AIR_HANDOFF_CARD']
card['card_revision'] = 6
card['profile_stack']['starter_profile']['PROMPT_VERSION'] = '2.4.1'
state = card['test_evidence_state']
state['reproducibility_state'] = 'UNVERIFIED'
state['release_grade_minimum_independent_executions'] = 3
state['test_run_identity_records'] = []
state['unstable_test_ids'] = []
state['restoration_rule'] = 'Restore the declared mode and evidence references, then validate current files, inputs, environment, permissions, obligation state, and exact run identities. A prior SUMMARY_ONLY result cannot be reconstructed into FULL_TEST_EVIDENCE without a new authorized run. A deterministic claim survives restoration only when its executable definitions, immutable identities, environment fingerprint, repetition evidence, and result fingerprints remain verifiable. The toggle or a model-authored pass summary does not prove testing, determinism, compliance, audit sufficiency, or regulatory conformity.'
for cond in card['schema_manifest']['conditional_rules']:
    if cond.get('id') == 'HC-COND-TEST-EVIDENCE':
        reqs = cond['requirements']
        anchor = 'each run record declares REPRODUCIBLE_EXECUTABLE, REPLAYABLE_EVALUATION, or MANUAL_REVIEW_REQUIRED'
        i = reqs.index(anchor) + 1
        reqs[i:i] = ['material quantitative run records preserve exact test-run identity fields and reproducibility_state','deterministic release-grade claims preserve at least three independent isolated execution results when technically feasible and identical decision fingerprints','model-dependent evaluations remain non-deterministic and preserve aggregate stability evidence when claimed','mixed automated, replayable, and manual results preserve class-separated counts']
        break
else:
    raise RuntimeError('handoff test evidence conditional rule not found')
card['schema_manifest']['schema_compatibility_contract']['starter_identity_version_required'] = '2.4.1'
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

for p in [P/'AIR_DEFAULT_STARTER_PROFILE.json', P/'AIR_HANDOFF_CARD_TEMPLATE.json']:
    json.loads(p.read_text(encoding='utf-8'))
print('AIR reproducibility contract patch complete')
