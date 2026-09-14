from pathlib import Path
import base64, hashlib, json, shutil, subprocess, sys, zlib

ROOT=(Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path('.').resolve())
EXPECTED_MAIN='a809c842dc5007430c19d21afd8d6525a9e0d3de'
CW='AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2'
FOUNDATION='AIR_FOUNDATION_2_6_3_OBJECT_CONTRACT_SET_008'
BEH_PASS='PASS_REPLAYABLE_MODEL_HOST_EVIDENCE'
EVID_REL='tests/AIR_PUBLIC_SURFACE_COPYWRITING_SET008_BEHAVIORAL_EVIDENCE_V1.json'
EVID_SHA='948dfcf7f9dfe1839e06475bb7566521b56430d2fb141cb96065e1e8fd45769d'
EVID_ID='AIR_BEHAVIORAL_EVIDENCE_PUBLIC_SURFACE_COPYWRITING_SET008_20260914_V1'
PENDING_STATUS='V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING'
PASS_STATUS='V2_5_0_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND'
MAN_PENDING='PACKAGE_COMPLETE_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_AVAILABLE_UNBOUND_REPLAYABLE_BEHAVIORAL_REVALIDATION_PENDING'
MAN_PASS='PACKAGE_COMPLETE_OBJECT_CONTRACT_SET_008_RESEAL_STATIC_VALIDATED_REPLAYABLE_BEHAVIORAL_VALIDATED_AVAILABLE_UNBOUND'
PERM={
 'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST.json',
 'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json',
 'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json',
 'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',
 'tools/validate_air_r7_remediation.py',
 'tools/test_air_r7_mutations.py',
 'tools/validate_air_v073_release_seal.py',
 'tools/test_air_v073_release_seal_mutations.py',
 EVID_REL,
}
EVID_Z='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'

def sh(*args,capture=False):
 p=subprocess.run(list(args),cwd=ROOT,text=True,capture_output=capture,check=True)
 return p.stdout.strip() if capture else ''
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def meta(p):
 b=p.read_bytes(); return {'sha256':hashlib.sha256(b).hexdigest(),'size_bytes':len(b),'line_count':len(b.decode().splitlines())}
def one(text,a,b,label):
 n=text.count(a)
 if n!=1: raise SystemExit(f'{label}: expected one anchor, found {n}')
 return text.replace(a,b,1)

def clean_ephemeral():
 for d in ROOT.rglob('__pycache__'):
  if d.is_dir(): shutil.rmtree(d,ignore_errors=True)
 for p in ROOT.rglob('*.pyc'):
  try:p.unlink()
  except FileNotFoundError:pass

def main():
 sh('git','fetch','origin','main')
 if sh('git','rev-parse','origin/main',capture=True)!=EXPECTED_MAIN: raise SystemExit('main drift')
 initial=set(filter(None,sh('git','diff','--name-only','origin/main',capture=True).splitlines()))
 if initial!={'tools/apply_r1_remediation.py'}: raise SystemExit(f'unexpected carrier staging diff: {sorted(initial)}')

 evb=zlib.decompress(base64.b64decode(EVID_Z))
 if hashlib.sha256(evb).hexdigest()!=EVID_SHA: raise SystemExit('embedded evidence hash mismatch')
 evp=ROOT/EVID_REL; evp.parent.mkdir(parents=True,exist_ok=True); evp.write_bytes(evb)
 ev=load(evp)
 if ev.get('evidence_id')!=EVID_ID or ev.get('summary',{}).get('pass_count')!=6 or ev.get('summary',{}).get('scenario_count')!=6 or ev.get('summary',{}).get('behavioral_revalidation_result')!='PASS_ON_CURRENT_MODEL_HOST': raise SystemExit('behavioral evidence content mismatch')

 cwdir=ROOT/'profiles/public surface copywriting specialist'
 comp_names=['AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST.json','AIR_PUBLIC_SURFACE_COPYWRITING_METHOD_PACK.json']
 for name in comp_names:
  p=cwdir/name; o=load(p)
  if o.get('STATUS')!=PENDING_STATUS: raise SystemExit(name+' unexpected pre-promotion status')
  o['STATUS']=PASS_STATUS; dump(p,o)

 manp=cwdir/'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json'; man=load(manp)
 if man.get('status')!=MAN_PENDING: raise SystemExit('manifest pre-promotion status mismatch')
 man['status']=MAN_PASS
 man['foundation_compatibility']['state']='COORDINATED_SET_008_RESEAL_STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED'
 pvs=man['package_validation_state']
 if pvs.get('behavioral_revalidation')!='PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE': raise SystemExit('manifest behavior pre-state mismatch')
 pvs['behavioral_revalidation']=BEH_PASS
 pvs['release_catalog_registration']='INCLUDED_IN_SET_008_V073_RELEASE_CATALOG'
 receipt={'evidence_id':EVID_ID,'filename':EVID_REL,'sha256':EVID_SHA,'size_bytes':len(evb),'line_count':len(evb.decode().splitlines()),'model_host':'ChatGPT / GPT-5.6 Sol','scenario_count':6,'pass_count':6,'result':BEH_PASS,'source_main_commit':EXPECTED_MAIN,'cross_host_equivalence_claimed':False}
 man['behavioral_evidence_receipt']=receipt
 for c in man['components']:
  cp=cwdir/c['filename']; m=meta(cp)
  c.update(m); c['status']=load(cp)['STATUS']; c['availability_state']='VALIDATED_AVAILABLE_UNBOUND'
 man['generated_at']='2026-09-14T22:02:00Z'
 dump(manp,man)

 idxp=ROOT/'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json'; idx=load(idxp)
 if idx.get('INDEX_VERSION')!='1.3.4': raise SystemExit('index pre-version mismatch')
 idx['INDEX_VERSION']='1.3.5'
 prog=idx['validation_state']['set008_static_revalidation_progress']
 if prog.get('behavioral_revalidation_ready_package_identities')!=[CW]: raise SystemExit('index behavioral-ready pre-state mismatch')
 prog['behavioral_revalidation_ready_package_identities']=[]
 prog['behavioral_revalidation_passed_package_identities']=[CW]
 prog['behavioral_revalidation_passed_count']=1
 ce=next(e for e in idx['entries'] if e['package_identity']==CW)
 if ce.get('availability_state')!='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION': raise SystemExit('index copywriting pre-state mismatch')
 ce['availability_state']='RELEASE_CATALOG_ENTRY'
 ce['current_foundation_compatibility_state']='STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED'
 ce['behavioral_revalidation_state']=BEH_PASS
 ce['behavioral_evidence_ref']={'evidence_id':EVID_ID,'filename':EVID_REL,'sha256':EVID_SHA,'model_host':'ChatGPT / GPT-5.6 Sol','scenario_count':6,'pass_count':6,'cross_host_equivalence_claimed':False}
 ce['manifest_sha256']=meta(manp)['sha256']
 dump(idxp,idx)
 idx_sha=meta(idxp)['sha256']

 r7p=ROOT/'tools/validate_air_r7_remediation.py'; s=r7p.read_text(encoding='utf-8')
 s=one(s,"BEHAVIOR_PENDING='PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'","BEHAVIOR_PENDING='PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE'\nBEHAVIOR_PASS='PASS_REPLAYABLE_MODEL_HOST_EVIDENCE'",'r7 behavior constant')
 s=one(s,"PENDING_BEHAVIOR='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'","PENDING_BEHAVIOR='RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'\nRELEASED='RELEASE_CATALOG_ENTRY'",'r7 release constant')
 s=one(s,"req(idx.get('INDEX_VERSION')=='1.3.4','Copywriting SET_008 index version mismatch')","req(idx.get('INDEX_VERSION')=='1.3.5','Copywriting SET_008 behavioral promotion index version mismatch')",'r7 index version')
 old="req(prog.get('passed_package_identities')==[CW_PACKAGE] and prog.get('passed_count')==1 and prog.get('pending_count')==4 and prog.get('behavioral_revalidation_ready_package_identities')==[CW_PACKAGE],'R7 SET_008 progress carrier mismatch')"
 new="req(prog.get('passed_package_identities')==[CW_PACKAGE] and prog.get('passed_count')==1 and prog.get('pending_count')==4 and prog.get('behavioral_revalidation_ready_package_identities')==[] and prog.get('behavioral_revalidation_passed_package_identities')==[CW_PACKAGE] and prog.get('behavioral_revalidation_passed_count')==1,'R7 SET_008 progress carrier mismatch')"
 s=one(s,old,new,'r7 progress')
 s=one(s,"req(e['availability_state']==PENDING_BEHAVIOR,'Copywriting index lifecycle not pending behavioral revalidation')","req(e['availability_state']==RELEASED,'Copywriting index lifecycle not released after behavioral revalidation')",'r7 index release')
 s=one(s,"req(e.get('current_foundation_compatibility_state')=='STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING','Copywriting SET_008 state mismatch')","req(e.get('current_foundation_compatibility_state')=='STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED' and e.get('behavioral_revalidation_state')==BEHAVIOR_PASS,'Copywriting SET_008 behavioral state mismatch')",'r7 index behavior state')
 old="st=str(o.get('status') or '')\n  req('STATIC_VALIDATED' in st and 'BEHAVIORAL_REVALIDATION_PENDING' in st and 'STATIC_CONTRACT_VALIDATION_PENDING' not in st,f'{p}: top lifecycle not R7 static-pass/behavior-pending')"
 new="st=str(o.get('status') or '')\n  is_cw=CW_DIR in str(p)\n  if is_cw:req('STATIC_VALIDATED' in st and 'REPLAYABLE_BEHAVIORAL_VALIDATED' in st and 'BEHAVIORAL_REVALIDATION_PENDING' not in st,f'{p}: Copywriting top lifecycle not behavioral-pass')\n  else:req('STATIC_VALIDATED' in st and 'BEHAVIORAL_REVALIDATION_PENDING' in st and 'STATIC_CONTRACT_VALIDATION_PENDING' not in st,f'{p}: top lifecycle not R7 static-pass/behavior-pending')"
 s=one(s,old,new,'r7 manifest lifecycle')
 s=one(s,"if 'behavioral_revalidation' in pvs:req(pvs['behavioral_revalidation']==BEHAVIOR_PENDING,f'{p}: behavioral validation not pending')","if 'behavioral_revalidation' in pvs:req(pvs['behavioral_revalidation']==(BEHAVIOR_PASS if is_cw else BEHAVIOR_PENDING),f'{p}: behavioral validation state mismatch')",'r7 manifest behavior')
 s=one(s,"req(cwman['foundation_compatibility'].get('state')=='COORDINATED_SET_008_RESEAL_STATIC_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING','Copywriting manifest SET_008 state mismatch')","req(cwman['foundation_compatibility'].get('state')=='COORDINATED_SET_008_RESEAL_STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED','Copywriting manifest SET_008 behavioral state mismatch')",'r7 manifest state')
 anchor="req(cpvs.get('foundation_reseal')=='PASS_COORDINATED_SET_008_RESEAL' and cpvs.get('component_internal_foundation_compatibility')=='PASS_SET_008_EXACT_RECEIPTS','Copywriting SET_008 manifest validation state mismatch')"
 insert=anchor+"\n req(cpvs.get('behavioral_revalidation')==BEHAVIOR_PASS and cpvs.get('release_catalog_registration')=='INCLUDED_IN_SET_008_V073_RELEASE_CATALOG','Copywriting behavioral promotion state mismatch')\n evp=ROOT/'"+EVID_REL+"'; req(evp.is_file(),'Copywriting behavioral evidence file missing'); ev=load(evp); er=cwman.get('behavioral_evidence_receipt',{})\n req(meta(evp)['sha256']==EVID_SHA if False else True,'unreachable')"
 # replace with explicit checks without introducing a hidden constant dependency
 insert=anchor+"\n evp=ROOT/'"+EVID_REL+"'; req(evp.is_file(),'Copywriting behavioral evidence file missing'); ev=load(evp); er=cwman.get('behavioral_evidence_receipt',{})\n req(meta(evp)['sha256']=='"+EVID_SHA+"' and er.get('sha256')=='"+EVID_SHA+"','Copywriting behavioral evidence hash mismatch')\n req(ev.get('evidence_id')=='"+EVID_ID+"' and ev.get('summary',{}).get('pass_count')==6 and ev.get('summary',{}).get('scenario_count')==6 and ev.get('summary',{}).get('behavioral_revalidation_result')=='PASS_ON_CURRENT_MODEL_HOST','Copywriting behavioral evidence result mismatch')\n req(er.get('result')==BEHAVIOR_PASS and er.get('model_host')=='ChatGPT / GPT-5.6 Sol' and er.get('cross_host_equivalence_claimed') is False,'Copywriting behavioral evidence receipt mismatch')"
 s=one(s,anchor,insert,'r7 evidence receipt')
 s=one(s,"print('behavioral_evidence CURRENTLY_PENDING')","print('behavioral_evidence PASS_REPLAYABLE_MODEL_HOST_EVIDENCE')",'r7 print')
 r7p.write_text(s,encoding='utf-8')

 r7mp=ROOT/'tools/test_air_r7_mutations.py'; s=r7mp.read_text(encoding='utf-8')
 add="add('R7-N24-COPYWRITING-BEHAVIORAL-ROLLBACK','catalog/AIR_SPECIALIST_PACKAGE_INDEX.json',jfn(lambda o:next(e for e in o['entries'] if e['package_identity']=='AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2').__setitem__('availability_state','RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION')))\nadd('R7-N25-COPYWRITING-EVIDENCE-RECEIPT-STALE','profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json',jfn(lambda o:o['behavioral_evidence_receipt'].__setitem__('sha256','0'*64)))\nadd('R7-N26-COPYWRITING-EVIDENCE-PASSCOUNT-STALE','tests/AIR_PUBLIC_SURFACE_COPYWRITING_SET008_BEHAVIORAL_EVIDENCE_V1.json',jfn(lambda o:o['summary'].__setitem__('pass_count',5)))\n"
 s=one(s,"if run(ROOT)!=0:raise SystemExit('R7-MUTATION-BASELINE failed')",add+"if run(ROOT)!=0:raise SystemExit('R7-MUTATION-BASELINE failed')",'r7 mutation append')
 r7mp.write_text(s,encoding='utf-8')

 v73p=ROOT/'tools/validate_air_v073_release_seal.py'; s=v73p.read_text(encoding='utf-8')
 s=one(s,"PENDING_BEHAVIOR = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'","PENDING_BEHAVIOR = 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION'\nRELEASED = 'RELEASE_CATALOG_ENTRY'\nBEHAVIOR_PASS = 'PASS_REPLAYABLE_MODEL_HOST_EVIDENCE'",'v73 constants')
 s=one(s,"'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json': '82c7af9464bd7fb048284a858abc94178fb04937971d44a38aa95183c2ffd510'","'catalog/AIR_SPECIALIST_PACKAGE_INDEX.json': '"+idx_sha+"'",'v73 index hash')
 s=one(s,"req(index['INDEX_VERSION'] == '1.3.4', 'Index version mismatch')","req(index['INDEX_VERSION'] == '1.3.5', 'Index behavioral-promotion version mismatch')",'v73 index version')
 s=one(s,"req(ce['availability_state'] == PENDING_BEHAVIOR, 'Copywriting lifecycle not pending behavioral revalidation')","req(ce['availability_state'] == RELEASED, 'Copywriting lifecycle not released after behavioral revalidation')",'v73 release state')
 s=one(s,"req(ce['current_foundation_compatibility_state'] == 'STATIC_COMPATIBILITY_VALIDATED_BEHAVIORAL_REVALIDATION_PENDING', 'Copywriting SET_008 state mismatch')","req(ce['current_foundation_compatibility_state'] == 'STATIC_AND_REPLAYABLE_BEHAVIORAL_VALIDATED' and ce.get('behavioral_revalidation_state') == BEHAVIOR_PASS, 'Copywriting SET_008 behavioral state mismatch')",'v73 behavior state')
 old="req(cwm['package_validation_state'].get('behavioral_revalidation') == 'PENDING_REPLAYABLE_MODEL_HOST_EVIDENCE', 'Copywriting behavioral state overclaimed')"
 new="req(cwm['package_validation_state'].get('behavioral_revalidation') == BEHAVIOR_PASS, 'Copywriting behavioral evidence not promoted')\n    evp = ROOT / '"+EVID_REL+"'\n    req(evp.is_file() and sha(evp) == '"+EVID_SHA+"', 'Copywriting behavioral evidence file/hash mismatch')\n    ev = load(evp); er = cwm.get('behavioral_evidence_receipt', {})\n    req(ev.get('evidence_id') == '"+EVID_ID+"' and ev.get('summary', {}).get('pass_count') == 6 and ev.get('summary', {}).get('scenario_count') == 6, 'Copywriting behavioral evidence result mismatch')\n    req(er.get('sha256') == '"+EVID_SHA+"' and er.get('result') == BEHAVIOR_PASS and er.get('cross_host_equivalence_claimed') is False, 'Copywriting behavioral evidence receipt mismatch')"
 s=one(s,old,new,'v73 manifest evidence')
 v73p.write_text(s,encoding='utf-8')

 v73mp=ROOT/'tools/test_air_v073_release_seal_mutations.py'; s=v73mp.read_text(encoding='utf-8')
 s=one(s,"add('V073-N10-INDEX-VERSION-ROLLBACK', idxmut(lambda o: o.__setitem__('INDEX_VERSION', '1.3.3')))","add('V073-N10-INDEX-VERSION-ROLLBACK', idxmut(lambda o: o.__setitem__('INDEX_VERSION', '1.3.4')))",'v73 mutation version')
 add="    add('V073-N11-COPYWRITING-BEHAVIORAL-ROLLBACK', idxmut(lambda o: next(e for e in o['entries'] if e['package_identity'] == 'AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_V2').__setitem__('availability_state', 'RELEASE_CATALOG_ENTRY_CANDIDATE_PENDING_BEHAVIORAL_REVALIDATION')))\n\n    def evidence_receipt_stale(d: Path):\n        p = d / 'profiles/public surface copywriting specialist/AIR_PUBLIC_SURFACE_COPYWRITING_SPECIALIST_PACKAGE_MANIFEST.json'; o = load(p); o['behavioral_evidence_receipt']['sha256'] = '0' * 64; dump(p, o)\n    add('V073-N12-COPYWRITING-EVIDENCE-RECEIPT-STALE', evidence_receipt_stale)\n\n    def evidence_passcount_stale(d: Path):\n        p = d / 'tests/AIR_PUBLIC_SURFACE_COPYWRITING_SET008_BEHAVIORAL_EVIDENCE_V1.json'; o = load(p); o['summary']['pass_count'] = 5; dump(p, o)\n    add('V073-N13-COPYWRITING-EVIDENCE-PASSCOUNT-STALE', evidence_passcount_stale)\n\n"
 s=one(s,"    killed = 0\n",add+"    killed = 0\n",'v73 mutation append')
 v73mp.write_text(s,encoding='utf-8')

 # Validate the candidate with the complete canonical suite before any permanent commit.
 sh(sys.executable,'tools/validate_air_suite.py')

 # Restore the temporary carrier and clean validation-generated bytecode.
 sh('git','checkout','origin/main','--','tools/apply_r1_remediation.py')
 clean_ephemeral()
 changed=set(filter(None,sh('git','diff','--name-only','origin/main',capture=True).splitlines()))
 untracked=set(filter(None,sh('git','ls-files','--others','--exclude-standard',capture=True).splitlines()))
 final=changed|untracked
 if final!=PERM: raise SystemExit(f'final path scope mismatch: {sorted(final)}')
 sh('git','add','-A')
 sh('git','config','user.name','github-actions[bot]'); sh('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
 sh('git','commit','-m','specialists: promote Public-Surface Copywriting after SET_008 behavioral revalidation [r1-applied]')
 sh('git','push','origin','HEAD:audit-remediation-r1-939801a9')
 print('Copywriting SET_008 behavioral promotion carrier: PASS')

if __name__=='__main__': main()
