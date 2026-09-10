from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any
ROOT=Path('.')
HASH_FIELDS={'sha256','observed_sha256'}
META_FIELDS=HASH_FIELDS|{'size_bytes','line_count'}
HISTORICAL_CONTAINER_KEYS={'source_baseline','mainline_release_binding','t7_change_record','historical_release_catalogs','source_candidate_manifest','change_history','release_history','historical_records'}
class ResealError(Exception): pass
def reject_dupes(pairs):
 out={}
 for k,v in pairs:
  if k in out: raise ResealError(f'duplicate JSON key: {k}')
  out[k]=v
 return out
def load_json_bytes(raw,path):
 try:return json.loads(raw.decode('utf-8'),object_pairs_hook=reject_dupes)
 except Exception as e: raise ResealError(f'{path}: strict JSON parse failed: {e}') from e
def operational_files(root): return sorted([*root.glob('prompts/*.md'),*root.glob('prompts/*.json'),*root.glob('catalog/*.json'),*root.glob('profiles/**/*.json')])
def historical_path(path): return any(p in HISTORICAL_CONTAINER_KEYS or p.startswith('historical_') for p in path)
def walk_dicts(obj,path=()):
 if historical_path(path): return
 if isinstance(obj,dict):
  yield obj,path
  for k,v in obj.items(): yield from walk_dicts(v,path+(k,))
 elif isinstance(obj,list):
  for i,v in enumerate(obj): yield from walk_dicts(v,path+(str(i),))
def ref_target(node,names):
 ref=node.get('filename') or node.get('canonical_filename'); fields=set(node)&META_FIELDS
 if isinstance(ref,str) and ref in names and fields:return ref,fields
 manifest=node.get('manifest_filename')
 if isinstance(manifest,str) and manifest in names and 'manifest_sha256' in node:return manifest,{'manifest_sha256'}
 return None,set()
def metadata(raw):
 text=raw.decode('utf-8');return {'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'line_count':len(text.splitlines())}
def build_graph(files,raw_by_path):
 by_name={}
 for p in files:
  if p.name in by_name: raise ResealError(f'duplicate operational basename: {p.name}')
  by_name[p.name]=p
 names=set(by_name); graph={p:set() for p in files if p.suffix=='.json'}
 for owner in graph:
  obj=load_json_bytes(raw_by_path[owner],owner)
  for node,path in walk_dicts(obj):
   target,_=ref_target(node,names)
   if target and target!=owner.name and by_name[target].suffix=='.json':graph[owner].add(by_name[target])
 return graph,by_name
def topo(graph):
 state={};out=[];stack=[]
 def visit(node):
  mark=state.get(node,0)
  if mark==2:return
  if mark==1:
   i=stack.index(node) if node in stack else 0; cyc=stack[i:]+[node];raise ResealError('content-hash dependency cycle: '+' -> '.join(str(p) for p in cyc))
  state[node]=1;stack.append(node)
  for dep in sorted(graph[node],key=str):visit(dep)
  stack.pop();state[node]=2;out.append(node)
 for node in sorted(graph,key=str):visit(node)
 return out
def virtual_reseal(root):
 files=operational_files(root);actual={p:p.read_bytes() for p in files};virtual=dict(actual);graph,by_name=build_graph(files,actual);names=set(by_name);updates=0
 for owner in topo(graph):
  obj=load_json_bytes(virtual[owner],owner);changed=False
  for node,path in walk_dicts(obj):
   target,fields=ref_target(node,names)
   if not target or target==owner.name:continue
   m=metadata(virtual[by_name[target]])
   for field in fields:
    new=m['sha256'] if field in {'manifest_sha256','observed_sha256'} else m[field]
    if node.get(field)!=new:node[field]=new;updates+=1;changed=True
  if changed:virtual[owner]=(json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode()
 return virtual,[p for p in files if virtual[p]!=actual[p]],updates
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--apply',action='store_true');g.add_argument('--check',action='store_true');a=ap.parse_args()
 virtual,changed,updates=virtual_reseal(ROOT)
 if a.check:
  if changed:raise SystemExit('AIR candidate reseal check FAILED: another reseal pass would change: '+', '.join(str(p) for p in changed[:20]))
  print('AIR candidate reseal idempotence: PASS (0 changes)');return
 for p in changed:p.write_bytes(virtual[p])
 print(f'AIR dependency-graph reseal applied: {len(changed)} files, {updates} metadata fields updated')
 _,second,_=virtual_reseal(ROOT)
 if second:raise SystemExit('AIR candidate reseal FAILED to converge: '+', '.join(str(p) for p in second[:20]))
 print('AIR dependency-graph reseal convergence: PASS')
if __name__=='__main__':
 try:main()
 except ResealError as e:raise SystemExit(f'AIR candidate reseal FAILED: {e}')
