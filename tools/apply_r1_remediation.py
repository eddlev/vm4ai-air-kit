from pathlib import Path
import subprocess, sys, tempfile

ROOT=(Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path('.').resolve())
SOURCE_COMMIT='ad06815adadfb3a2a8c0f88f2a2a2ffda1bd8f31'


def run(*args):
    print('+',' '.join(args),flush=True)
    subprocess.run(args,cwd=ROOT,check=True)

# The prior carrier source is retained by exact commit identity. Fetch it,
# patch only the final transport hygiene step, and execute the otherwise
# identical authorized Governance SET_008 remediation transaction.
if (ROOT/'.git/shallow').exists():
    run('git','fetch','--no-tags','--unshallow','origin')
run('git','fetch','--no-tags','origin',SOURCE_COMMIT)
source=subprocess.check_output(
    ['git','show',f'{SOURCE_COMMIT}:tools/apply_r1_remediation.py'],
    cwd=ROOT,text=True
)
anchor="run('git','add','-A')"
assert source.count(anchor)==1,source.count(anchor)
cleanup="""# Remove only generated untracked Python bytecode before final staging.\nfor cache_dir in sorted(ROOT.rglob('__pycache__'), reverse=True):\n    if not cache_dir.is_dir():\n        continue\n    for artifact in sorted(cache_dir.rglob('*'), reverse=True):\n        if not artifact.is_file():\n            continue\n        rel=artifact.relative_to(ROOT).as_posix()\n        status=out('git','status','--porcelain','--',rel)\n        assert status.startswith('?? '),(rel,status)\n        artifact.unlink()\n    try:\n        cache_dir.rmdir()\n    except OSError:\n        pass\nfor artifact in sorted(ROOT.rglob('*.pyc')):\n    if not artifact.is_file():\n        continue\n    rel=artifact.relative_to(ROOT).as_posix()\n    status=out('git','status','--porcelain','--',rel)\n    assert status.startswith('?? '),(rel,status)\n    artifact.unlink()\nrun('git','add','-A')"""
source=source.replace(anchor,cleanup,1)
with tempfile.NamedTemporaryFile('w',encoding='utf-8',suffix='.py',delete=False) as f:
    f.write(source)
    patched=Path(f.name)
try:
    run(sys.executable,str(patched),str(ROOT))
finally:
    patched.unlink(missing_ok=True)
