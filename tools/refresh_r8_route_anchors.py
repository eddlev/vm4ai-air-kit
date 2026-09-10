from __future__ import annotations
import json
from pathlib import Path

core=Path('prompts/AIR_CORE_RUNTIME.md').read_text(encoding='utf-8')
p=Path('catalog/AIR_RUNTIME_ROUTE_MAP.json')
o=json.loads(p.read_text(encoding='utf-8'))
line_by={ln.split('=',1)[1]:i for i,ln in enumerate(core.splitlines(),1) if ln.startswith('id=RT.')}
route_ids={r['route_id'] for r in o['routes']}
if set(line_by)!=route_ids:
    raise SystemExit('R8 route anchor refresh FAILED: Core/Route Map route-id set mismatch')
for r in o['routes']:
    r['source_anchor']['line']=line_by[r['route_id']]
p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(f'R8 Route Map source anchors refreshed: {len(o["routes"])}')
