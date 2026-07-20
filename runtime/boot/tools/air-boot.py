#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, sys, tempfile
from pathlib import Path

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def load(path):
    def hook(pairs):
        d={}
        for k,v in pairs:
            if k in d: raise ValueError(f'duplicate JSON key: {k}')
            d[k]=v
        return d
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=hook)

def safe(root, rel):
    p=Path(rel)
    if p.is_absolute() or '..' in p.parts: raise ValueError(f'unsafe relative path: {rel}')
    root=root.resolve(); target=(root/p).resolve()
    if target!=root and root not in target.parents: raise ValueError(f'path escapes AIR root: {rel}')
    return target

def validate(root, manifest):
    errors=[]; warnings=[]
    if manifest.get('SYSTEM_DESIGNATION')!='AIR_BOOT_MODULE_MANIFEST_V1': errors.append('wrong manifest designation')
    mods=manifest.get('modules',[]); ids=[m.get('module_id') for m in mods]
    if len(ids)!=len(set(ids)): errors.append('duplicate module id')
    by={m.get('module_id'):m for m in mods}
    for m in mods:
        rel=m.get('relative_path','')
        if '://' in rel: errors.append(f'remote URL prohibited: {rel}'); continue
        try: p=safe(root,rel)
        except Exception as e: errors.append(str(e)); continue
        if not p.is_file(): errors.append(f'missing module: {rel}'); continue
        if p.is_symlink():
            try: safe(root,os.readlink(p))
            except Exception: errors.append(f'symlink escape: {rel}')
        expected=m.get('sha256')
        if expected and sha(p)!=expected: errors.append(f'digest mismatch: {rel}')
        if m.get('terminal_sentinel'):
            text=p.read_text(encoding='utf-8')
            if not text.rstrip().endswith(m['terminal_sentinel']): errors.append(f'sentinel mismatch: {rel}')
        for dep in m.get('dependencies',[]):
            if dep not in by: errors.append(f'unresolved dependency {dep} for {m.get("module_id")}')
    visiting=set(); done=set()
    def visit(mid):
        if mid in done: return
        if mid in visiting: errors.append(f'dependency cycle at {mid}'); return
        visiting.add(mid)
        for dep in by.get(mid,{}).get('dependencies',[]): visit(dep)
        visiting.remove(mid); done.add(mid)
    for mid in ids: visit(mid)
    return errors,warnings

def plan(manifest,triggers):
    by={m['module_id']:m for m in manifest['modules']}; selected=set()
    for m in manifest['modules']:
        if m.get('load_class')=='SESSION_ENTRY' or set(m.get('triggers',[])) & set(triggers): selected.add(m['module_id'])
    if any(t in {'MATERIAL_EXECUTION','STATE_TRANSITION','APPROVAL','MUTATION','HANDOFF','RESCOPE'} for t in triggers): selected.add('AIR_RUNTIME_CONTRACT_GATE_AND_EXECUTION_V1')
    def add(mid):
        if mid in selected:
            pass
        selected.add(mid)
        for dep in by.get(mid,{}).get('dependencies',[]): add(dep)
    for mid in list(selected): add(mid)
    order=[]; seen=set()
    def emit(mid):
        if mid in seen: return
        for dep in by.get(mid,{}).get('dependencies',[]): emit(dep)
        seen.add(mid); order.append(mid)
    for mid in sorted(selected): emit(mid)
    return order

def atomic_write(path,data,overwrite=False):
    if path.exists() and not overwrite: raise FileExistsError(f'output exists: {path}')
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=path.name+'.',dir=str(path.parent)); os.close(fd)
    Path(tmp).write_bytes(data); os.replace(tmp,path)

def receipt(root,manifest,manifest_path,triggers,planned,decision='VALID'):
    now=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    loaded=[]
    by={m['module_id']:m for m in manifest['modules']}
    for mid in planned:
        m=by[mid]; p=safe(root,m['relative_path']); loaded.append({'module_id':mid,'relative_path':m['relative_path'],'sha256':sha(p),'verification_state':'DIGEST_VERIFIED'})
    raw=(str(root.resolve())+'|'+manifest['version']+'|'+'|'.join(planned)+'|'+now).encode()
    return {'SYSTEM_DESIGNATION':'AIR_BOOT_MODULE_LOAD_RECEIPT_V1','receipt_id':'AIR-BOOT-'+hashlib.sha256(raw).hexdigest()[:20],'created_at_utc':now,'air_root':str(root.resolve()),'boot_mode':'LOCAL_BUNDLED','kernel':manifest['kernel'],'manifest':{'module_id':manifest['SYSTEM_DESIGNATION'],'version':manifest['version'],'sha256':sha(manifest_path)},'requested_triggers':triggers,'planned_modules':planned,'loaded_modules':loaded,'missing_or_failed_modules':[],'decision':decision,'authorization_decision':'NOT_EVALUATED','limitations':['Digest verification and module planning do not authorize tool execution.','Content remains subject to prompt-injection and direct-binding controls.']}

def main():
    ap=argparse.ArgumentParser(prog='air-boot')
    default_root=str(Path(__file__).resolve().parents[3])
    ap.add_argument('--root',default=default_root)
    ap.add_argument('--manifest',default='runtime/boot/AIR BOOT MODULE MANIFEST.json')
    sp=ap.add_subparsers(dest='cmd',required=True)
    sp.add_parser('validate-manifest')
    vm=sp.add_parser('validate-module'); vm.add_argument('module_id')
    pl=sp.add_parser('plan'); pl.add_argument('--trigger',action='append',default=[])
    bu=sp.add_parser('bundle'); bu.add_argument('--trigger',action='append',default=[]); bu.add_argument('--output',required=True); bu.add_argument('--overwrite',action='store_true')
    rc=sp.add_parser('receipt'); rc.add_argument('--trigger',action='append',default=[]); rc.add_argument('--output',required=True); rc.add_argument('--overwrite',action='store_true')
    co=sp.add_parser('compare'); co.add_argument('--triggers',nargs='*',default=[])
    sp.add_parser('status')
    a=ap.parse_args(); root=Path(a.root).resolve(); mp=safe(root,a.manifest); manifest=load(mp)
    errors,warnings=validate(root,manifest)
    if a.cmd=='validate-manifest':
        print(json.dumps({'decision':'PASS' if not errors else 'FAIL','errors':errors,'warnings':warnings},indent=2)); return 0 if not errors else 2
    if errors: print(json.dumps({'decision':'FAIL','errors':errors},indent=2)); return 2
    by={m['module_id']:m for m in manifest['modules']}
    if a.cmd=='validate-module':
        if a.module_id not in by: print(json.dumps({'decision':'FAIL','error':'unknown module'},indent=2)); return 2
        m=by[a.module_id]; p=safe(root,m['relative_path']); ok=sha(p)==m['sha256']; print(json.dumps({'decision':'PASS' if ok else 'FAIL','module_id':a.module_id,'sha256':sha(p)},indent=2)); return 0 if ok else 2
    triggers=getattr(a,'trigger',[]) or getattr(a,'triggers',[]) or []
    planned=plan(manifest,triggers)
    if a.cmd=='plan': print(json.dumps({'triggers':triggers,'planned_modules':planned,'authorization_decision':'NOT_EVALUATED'},indent=2)); return 0
    if a.cmd=='receipt':
        r=receipt(root,manifest,mp,triggers,planned); atomic_write(Path(a.output),json.dumps(r,indent=2).encode()+b'\n',a.overwrite); print(json.dumps({'decision':'PASS','output':a.output,'receipt_id':r['receipt_id']},indent=2)); return 0
    if a.cmd=='bundle':
        r=receipt(root,manifest,mp,triggers,planned); parts=['# AIR LOCAL MODULAR BOOT BUNDLE','', '```json',json.dumps(r,indent=2),'```','']
        for mid in planned:
            m=by[mid]; parts += [f'<!-- AIR_MODULE_BEGIN {mid} -->',safe(root,m['relative_path']).read_text(encoding='utf-8').rstrip(),f'<!-- AIR_MODULE_END {mid} -->','']
        atomic_write(Path(a.output),('\n'.join(parts)+'\n').encode(),a.overwrite); print(json.dumps({'decision':'PASS','output':a.output,'modules':planned},indent=2)); return 0
    if a.cmd=='compare':
        full=sum(x['size_bytes'] for x in manifest['canonical_monolith']); selected=manifest['kernel']['size_bytes']+manifest['boot_starter']['size_bytes']+mp.stat().st_size+sum(by[x]['size_bytes'] for x in planned)
        print(json.dumps({'full_framework_bytes':full,'selected_framework_bytes':selected,'ratio':selected/full if full else None,'planned_modules':planned},indent=2)); return 0
    if a.cmd=='status': print(json.dumps({'decision':'PASS','kernel':manifest['kernel'],'manifest_version':manifest['version'],'modules':len(manifest['modules']),'network_required':False,'package_install_required':False},indent=2)); return 0
    return 1
if __name__=='__main__': raise SystemExit(main())
