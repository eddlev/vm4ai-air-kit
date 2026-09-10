from __future__ import annotations
import json,re,sys,unicodedata
from pathlib import Path
from urllib.parse import unquote

PROFILE='AIR_TARGET_PLATFORM_NORMALIZATION_PORTABLE_V1'
UNKNOWN='APPLY_PORTABLE_PROFILE_FAIL_CLOSED_ON_UNAVAILABLE_STRICTER_TARGET_RULE'
SENT={
'DC-SENTINEL-CORE':('AIR_CORE_RUNTIME.md','AIR_LOAD_SENTINEL :: AIR_CORE_RUNTIME :: END_OF_FILE :: LOAD_INTEGRITY_V2'),
'DC-SENTINEL-CONTROL':('AIR_CONTROL_SURFACE.md','AIR_LOAD_SENTINEL :: AIR_CONTROL_SURFACE :: END_OF_FILE :: LOAD_INTEGRITY_V2'),
'DC-SENTINEL-GOV':('AIR_GOV.md','AIR_LOAD_SENTINEL :: AIR_HR_GOVERNANCE_SUPPLEMENT :: END_OF_FILE :: LOAD_INTEGRITY_V2')}
RESERVED={'CON','PRN','AUX','NUL'}|{f'COM{i}' for i in range(1,10)}|{f'LPT{i}' for i in range(1,10)}
R8_IDS=['AIR-AUD-002','AIR-AUD-012','AIR-AUD-015','AIR-AUD-071']
class E(Exception): pass
def req(c,m):
    if not c: raise E(m)
def reject(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise E('duplicate JSON key '+k)
        d[k]=v
    return d
def load(p): return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=reject)
def norm_key(name:str)->str:
    return unicodedata.normalize('NFKC',unquote(name)).casefold().rstrip(' .')
def portable_valid(name:str)->bool:
    k=norm_key(name)
    if not k or any(ord(ch)<32 or ch in '/\\' for ch in k): return False
    stem=k.split('.',1)[0].upper()
    return stem not in RESERVED

def main(root:Path):
    p=root/'prompts'; core=(p/'AIR_CORE_RUNTIME.md').read_text(encoding='utf-8'); control=(p/'AIR_CONTROL_SURFACE.md').read_text(encoding='utf-8')
    starter=load(p/'AIR_DEFAULT_STARTER_PROFILE.json'); card=load(p/'AIR_HANDOFF_CARD_TEMPLATE.json')['AIR_HANDOFF_CARD']
    checks={c['check_id']:c for c in starter['validation_contract']['deterministic_contract_registry']['checks']}
    for cid,(name,literal) in SENT.items():
        req(cid in checks,f'{cid}: typed sentinel check missing')
        req(checks[cid].get('expected')==literal,f'{cid}: typed sentinel expectation mismatch')
        actual=(p/name).read_text(encoding='utf-8').rstrip().splitlines()[-1]
        req(actual==literal,f'{cid}: actual terminal sentinel mismatch')
    refs=[
      'AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-CORE].expected',
      'AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-CONTROL].expected',
      'AIR_DEFAULT_STARTER_V2.validation_contract.deterministic_contract_registry.checks[DC-SENTINEL-GOV].expected']
    req(all(x in core for x in refs),'R8 sentinel declaration does not resolve all typed expectations')
    req(refs[1] in control,'R8 Control sentinel declaration does not resolve typed expectation')
    sentinel_block=core[core.index('Expected Markdown sentinel literals are owned'):core.index('Check timing:')]
    req('AIR_LOAD_SENTINEL ::' not in sentinel_block,'R8 sentinel declaration duplicates literal')

    mu=re.search(r'Canonical Unicode mark, reproduced verbatim inside a monospaced context:\n\n([^\n]+)',core); ma=re.search(r'ASCII fallback for rendering-limited environments:\n\n([^\n]+)',core)
    req(mu and ma,'R8 Core boot mark literals missing')
    unicode_mark=mu.group(1); ascii_mark=ma.group(1)
    req(unicode_mark=='━━━┤○├━━━[●]━━━┤○├━━━','R8 Core Unicode boot mark changed unexpectedly')
    req(ascii_mark=='---(o)---[*]---(o)---','R8 Core ASCII boot mark changed unexpectedly')
    req('AIR_BOOT_BRAND_MARK_M2' in control and 'AIR_CORE_RUNTIME_V2 section `AIR BOOT BRAND MARK LAW`' in control,'R8 Control boot mark is not Core-owned')
    for old in ['━━━━━━━━●━━━━━━━━━━━    A I R','=========o=========    A I R','full three-line boot mark','heavy rail and `A I R`']:
        req(old not in control,f'R8 Control old boot mark variant remains: {old}')
    req('must not be substituted for the boot mark' in control,'R8 separate signature substitution guard missing')

    qblock=core[core.index('Q1-D required orientation order:'):core.index('Claim boundary:',core.index('Q1-D required orientation order:'))]
    cmds=['air -o on','air -o -min','air -t on','air -t off']
    req('explain all four canonical system modifiers' in qblock,'R8 Q1D four-modifier wording missing')
    req(all(cmd in qblock for cmd in cmds),'R8 Q1D modifier set incomplete')
    req('explain only the two system modifiers' not in core,'R8 stale two-modifier wording remains')

    req('Unicode normalization form: NFKC.' in core,'R8 Core NFKC normalization form missing')
    req(f'target-platform normalization profile: {PROFILE}.' in core,'R8 Core target-platform profile missing')
    req(f'when target_platform is null or unknown, apply {PROFILE}' in core,'R8 Core unknown-target behavior missing')
    fid=starter['local_profile_policies']['file_identity_and_delivery']
    req(fid.get('unicode_normalization_form')=='NFKC','R8 Starter normalization form mismatch')
    req(fid.get('target_platform_normalization_profile')==PROFILE,'R8 Starter target-platform profile mismatch')
    req(fid.get('unknown_target_platform_behavior')==UNKNOWN,'R8 Starter unknown target policy mismatch')
    dc=checks['DC-FOUNDATION-NORMALIZED-COLLISION']
    req(dc.get('unicode_normalization_form')=='NFKC','R8 collision check normalization form mismatch')
    req(dc.get('target_platform_normalization_profile')==PROFILE,'R8 collision check platform profile mismatch')
    req(dc.get('unknown_target_platform_behavior')==UNKNOWN,'R8 collision check unknown-target mismatch')
    req(set(dc.get('portable_reserved_basename_stems',[]))==RESERVED,'R8 portable reserved basename set mismatch')
    for section in [card['platform_state'],card['file_identity_and_delivery_state']]:
        req(section.get('unicode_normalization_form')=='NFKC','R8 Handoff NFKC carrier mismatch')
        req(section.get('target_platform_normalization_profile')==PROFILE,'R8 Handoff profile carrier mismatch')
    req(card['platform_state'].get('unknown_target_platform_behavior')==UNKNOWN,'R8 Handoff unknown-target behavior mismatch')
    req(card['file_identity_and_delivery_state'].get('target_platform_profile_resolution_state')=='PORTABLE_BASELINE_REQUIRED_WHEN_TARGET_UNKNOWN','R8 Handoff target profile resolution state mismatch')

    names=[x['canonical_filename'] for x in starter['authority_contract']['required_files']]
    req(all(re.fullmatch(r'[A-Za-z0-9_.-]+',n) for n in names),'R8 canonical ASCII positive path failed')
    keys=[norm_key(n) for n in names]; req(len(keys)==len(set(keys)),'R8 canonical names collide under portable profile')
    req(norm_key('ＡIR_CORE_RUNTIME.md')==norm_key('AIR_CORE_RUNTIME.md'),'R8 NFKC compatibility collision negative control failed')
    req(not portable_valid('CON.json') and not portable_valid('com1.txt'),'R8 portable reserved-name negative control failed')
    req(portable_valid('AIR_CORE_RUNTIME.md'),'R8 canonical portable-name positive control failed')
    print('R8 remediation validation: PASS')
    print('r8_findings',len(R8_IDS))
    print('sentinel_refs',3)
    print('boot_mark_source','CORE_ONLY')
    print('q1d_modifiers',4)
    print('unicode_normalization','NFKC')
    print('target_platform_profile',PROFILE)
    print('canonical_ascii_names',len(names))
    print('unicode_collision_negative','PASS')
    print('reserved_name_negative','PASS')

if __name__=='__main__':
    try: main(Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve())
    except (E,KeyError,ValueError) as e:
        print('R8 remediation validation: FAIL:',e,file=sys.stderr); raise SystemExit(1)
