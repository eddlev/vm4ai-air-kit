from __future__ import annotations
import json, tempfile
from pathlib import Path
from adapters.durable_provenance import FilesystemDurableProvenanceProvider, SQLiteDurableProvenanceProvider, canonical_sha256
from adapters.durable_provenance.contract import ProviderIntegrityError, SnapshotKey

def main():
    killed=0
    with tempfile.TemporaryDirectory() as td:
        p=FilesystemDurableProvenanceProvider(Path(td)/"fs"); snap={"ok":True}; k=SnapshotKey("n",1,"L1",canonical_sha256(snap)); p.prepare_snapshot(k,snap); p.commit_visible(k)
        f=next((Path(td)/"fs"/"namespaces"/"n"/"committed").glob("*.json")); r=json.loads(f.read_text()); r["canonical_object_snapshot"]={"ok":False}; f.write_text(json.dumps(r),encoding="utf-8")
        try: p.retrieve_committed_range("n",1,1)
        except ProviderIntegrityError: killed+=1
    with tempfile.TemporaryDirectory() as td:
        p=SQLiteDurableProvenanceProvider(Path(td)/"db.sqlite"); snap={"ok":True}; k=SnapshotKey("n",1,"L1",canonical_sha256(snap)); p.prepare_snapshot(k,snap); p.commit_visible(k)
        p.db.execute("update records set snapshot='{}'"); p.db.commit()
        try: p.retrieve_committed_range("n",1,1)
        except ProviderIntegrityError: killed+=1
    assert killed==2
    print("AIR durable provenance provider mutation tests: PASS (2/2 killed)")

if __name__=="__main__": main()
