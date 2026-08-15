from pathlib import Path
import json
import shutil

ROOT = Path('.')

# 1. Remove repository-local documentation completely.
docs = ROOT / 'docs'
if not docs.exists():
    raise SystemExit('docs/ is unexpectedly absent before cleanup')
shutil.rmtree(docs)

# 2. Rewrite README as the public gateway, not a duplicate docs tree.
readme_path = ROOT / 'README.md'
readme = readme_path.read_text(encoding='utf-8')

if '## Why AIR is prompt-based' in readme:
    raise SystemExit('README already contains prompt-based rationale; refusing duplicate insertion')

marker = '---\n\n## Why use AIR?'
if readme.count(marker) != 1:
    raise SystemExit('README Why use AIR marker not found exactly once')

why_prompt = '''---\n\n## Why AIR is prompt-based\n\nAIR uses a prompt-based core deliberately. The working contract is expressed in portable text and machine-readable records so the project can travel with the user instead of being owned by one vendor runtime.\n\n- **Vendor independence** — AIR does not require one provider's private project state, permission model, or agent runtime to define the project contract. Platform-specific features can be used as adapters without becoming the AIR core.\n- **Platform-agnostic core** — Orbit, artifacts, gates, evidence boundaries, approval state, and Handoff are designed to remain recognizable across compatible model interfaces even when host capabilities differ.\n- **Cross-platform portability** — users can move work when models or platforms change without rebuilding the project's explicit governance and execution state from scratch.\n- **Multi-session continuity** — the Handoff Card serializes explicit project state so a compatible receiving session can validate, rebind, and continue the work instead of relying on hidden conversation state.\n- **Progressive enforcement** — the portable prompt layer can work without dedicated infrastructure, while future host hooks, gateways, and workflow adapters can add deterministic permissions, receipts, and action blocking where the platform supports them.\n\nThat portability is the reason the AIR core is prompt-based. Its assurance limitations are also why AIR keeps deterministic host enforcement separate and requires external evidence for claims that depend on tools, repositories, deployments, or backend events.\n\n## Why use AIR?'''
readme = readme.replace(marker, why_prompt, 1)

old_modifier_tail = 'These are prompt-side controls. They do not bypass approval, evidence, scope, or release gates.'
new_modifier_tail = 'AIR defaults to `ALL_OBJECTS`; `air -o -min` is an explicit compact visibility mode selected by the user or restored from a valid explicit prior selection.\n\nThese are prompt-side controls. They do not bypass approval, evidence, scope, or release gates.'
if readme.count(old_modifier_tail) != 1:
    raise SystemExit('README modifier tail not found exactly once')
readme = readme.replace(old_modifier_tail, new_modifier_tail, 1)

map_start = readme.index('## Repository map\n')
map_end = readme.index('## Machine-readable records\n')
new_map = '''## Repository map\n\n```text\nprompts/\n  AIR_CORE_RUNTIME.md\n  AIR_CONTROL_SURFACE.md\n  AIR_GOV.md\n  AIR_DEFAULT_STARTER_PROFILE.json\n  AIR_HANDOFF_CARD_TEMPLATE.json\n\nprofiles/\n  grounding specialist/\n  governance specialist/\n  capability ecology architect/\n  specification first method pack/\n\ntests/\n  executable AIR verification harness\n\n.github/\n  workflows/\n    repository CI and reproducibility contract\n```\n\nThe files under `prompts/` are the current foundation. Specialist, domain, and method material lives under `profiles/` and is **available but unbound** until selected, compatibility-validated, approved when required, and bound according to the runtime. The standalone Specification-First Verification Method Pack remains a single experimental method pack under `profiles/` until further package work is justified.\n\n'''
readme = readme[:map_start] + new_map + readme[map_end:]

doc_start = readme.index('## Documentation\n')
doc_end = readme.index('## License and brand\n')
new_docs = '''## Documentation\n\n- [How AIR works](https://vm4ai.com/how-it-works.html) — public architecture and visual explanation\n- [VM4AI website](https://vm4ai.com/) — current public documentation, examples, and release guidance\n- [GitHub Discussions](https://github.com/eddlev/vm4ai-air-kit/discussions) — questions, implementation discussion, and community patterns\n\n'''
readme = readme[:doc_start] + new_docs + readme[doc_end:]

old_footer = 'The AIR brand system and vm4ai.com are developed using AIR with human review and approval. See the public site for the current account and examples.'
new_footer = 'The AIR brand system and [vm4ai.com](https://vm4ai.com/) are developed using AIR with human review and approval. See the public site for the current account and examples.'
if readme.count(old_footer) != 1:
    raise SystemExit('README footer not found exactly once')
readme = readme.replace(old_footer, new_footer, 1)

for forbidden in ('methods/', 'docs/', 'historical audit records', 'AIR_MODEL_PORTABILITY_NOTES'):
    if forbidden in readme:
        raise SystemExit(f'forbidden README repository-doc reference remains: {forbidden}')

required_readme = [
    '## Why AIR is prompt-based',
    '**Vendor independence**',
    '**Platform-agnostic core**',
    '**Cross-platform portability**',
    '**Multi-session continuity**',
    '**Progressive enforcement**',
    'AIR defaults to `ALL_OBJECTS`',
    '[vm4ai.com](https://vm4ai.com/)',
    'specification first method pack/',
]
for value in required_readme:
    if value not in readme:
        raise SystemExit(f'missing required README text: {value}')

readme_path.write_text(readme, encoding='utf-8')

# 3. Remove all docs dependencies/tests, then add permanent cleanup assertions.
manifest_path = ROOT / 'tests' / 'air-test-manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['material_inputs'] = [p for p in manifest['material_inputs'] if not p.startswith('docs/')]
manifest['tests'] = [t for t in manifest['tests'] if not str(t.get('id', '')).startswith('DOC6-')]

new_tests = [
    {
        'id': 'CLEANUP-001', 'requirement': 'Repository-local docs tree is absent',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'file_exists', 'path': 'docs', 'expected': False
    },
    {
        'id': 'CLEANUP-002', 'requirement': 'README explains why AIR is prompt-based',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'text_contains', 'path': 'README.md', 'text': '## Why AIR is prompt-based', 'expected': True
    },
    {
        'id': 'CLEANUP-003', 'requirement': 'README states vendor independence rationale',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'text_contains', 'path': 'README.md', 'text': '**Vendor independence**', 'expected': True
    },
    {
        'id': 'CLEANUP-004', 'requirement': 'README states platform-agnostic core rationale',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'text_contains', 'path': 'README.md', 'text': '**Platform-agnostic core**', 'expected': True
    },
    {
        'id': 'CLEANUP-005', 'requirement': 'README states cross-platform portability rationale',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'text_contains', 'path': 'README.md', 'text': '**Cross-platform portability**', 'expected': True
    },
    {
        'id': 'CLEANUP-006', 'requirement': 'README states multi-session continuity rationale',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'text_contains', 'path': 'README.md', 'text': '**Multi-session continuity**', 'expected': True
    },
    {
        'id': 'CLEANUP-007', 'requirement': 'README states progressive enforcement rationale',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'text_contains', 'path': 'README.md', 'text': '**Progressive enforcement**', 'expected': True
    },
    {
        'id': 'CLEANUP-008', 'requirement': 'README states ALL_OBJECTS default',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'text_contains', 'path': 'README.md', 'text': 'AIR defaults to `ALL_OBJECTS`', 'expected': True
    },
    {
        'id': 'CLEANUP-009', 'requirement': 'README footer links vm4ai.com',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'text_contains', 'path': 'README.md', 'text': '[vm4ai.com](https://vm4ai.com/)', 'expected': True
    },
    {
        'id': 'CLEANUP-010', 'requirement': 'README no longer advertises nonexistent root methods directory',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'text_not_contains', 'path': 'README.md', 'text': 'methods/', 'expected': True
    },
    {
        'id': 'CLEANUP-011', 'requirement': 'README no longer links repository-local docs tree',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'text_not_contains', 'path': 'README.md', 'text': 'docs/', 'expected': True
    },
    {
        'id': 'CLEANUP-012', 'requirement': 'README no longer describes historical audit records as current tree content',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'text_not_contains', 'path': 'README.md', 'text': 'historical audit records', 'expected': True
    },
    {
        'id': 'CLEANUP-013', 'requirement': 'No root methods directory is introduced',
        'test_class': 'REPRODUCIBLE_EXECUTABLE', 'type': 'file_exists', 'path': 'methods', 'expected': False
    },
]
existing_ids = {t.get('id') for t in manifest['tests']}
for test in new_tests:
    if test['id'] in existing_ids:
        raise SystemExit(f'duplicate test id: {test["id"]}')
manifest['tests'].extend(new_tests)

if any(p.startswith('docs/') for p in manifest['material_inputs']):
    raise SystemExit('docs material input remains')
if any(str(t.get('id', '')).startswith('DOC6-') for t in manifest['tests']):
    raise SystemExit('DOC6 test remains')
if len(manifest['tests']) != 345:
    raise SystemExit(f'unexpected test count after cleanup: {len(manifest["tests"])}')

manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('repository cleanup applied; tests=345')
