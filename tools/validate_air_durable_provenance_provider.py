from __future__ import annotations
import json, tempfile
from pathlib import Path
from adapters.durable_provenance import FilesystemDurableProvenanceProvider, SQLiteDurableProvenanceProvider, canonical_sha256
from adapters.durable_provenance.contract import ProviderGenerationMismatch, ProviderIntegrityError, SnapshotKey

def exercise(cls, target):
    p=cls(target); d=p.describe_provider()
    assert d["positive_execution_authority"]=="NONE"
    assert p.probe_write_readback()["write_readback_state"]=="PASS"
    ns="project-"+canonical_sha256({"namespace":"isolated"})[:20]
    expected=[]
    for i in range(1,6):
        snap={"AIR_TEST_OBJECT":{"sequence":i,"array":[3,2,1],"unicode":"ÆØÅ"}}
        key=SnapshotKey(ns,i,f"LEDGER::{i}",canonical_sha256(snap))
        p.prepare_snapshot(key,snap)
        assert p.retrieve_committed_range(ns,i,i)==[]
        p.commit_visible(key)
        expected.append({"emission_sequence":i,"ledger_entry_ref":key.ledger_entry_ref,"canonical_object_sha256":key.canonical_object_sha256})
    assert p.verify_coverage(ns,expected)["coverage_state"]=="COMPLETE"
    missing=expected+[{"emission_sequence":6,"ledger_entry_ref":"LEDGER::6","canonical_object_sha256":"0"*64}]
    assert p.verify_coverage(ns,missing)["coverage_state"]=="INCOMPLETE"
    assert p.retrieve_committed_range("other-project",1,99)==[]
    return d["provider_generation"],ns,expected

def main():
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"fs"; gen,ns,expected=exercise(FilesystemDurableProvenanceProvider,path)
        p2=FilesystemDurableProvenanceProvider(path,expected_generation=gen)
        assert p2.verify_coverage(ns,expected)["coverage_state"]=="COMPLETE"
        try: FilesystemDurableProvenanceProvider(path,expected_generation="wrong")
        except ProviderGenerationMismatch: pass
        else: raise AssertionError("filesystem generation mismatch not rejected")
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"db.sqlite"; gen,ns,expected=exercise(SQLiteDurableProvenanceProvider,path)
        p2=SQLiteDurableProvenanceProvider(path,expected_generation=gen)
        assert p2.verify_coverage(ns,expected)["coverage_state"]=="COMPLETE"
        try: SQLiteDurableProvenanceProvider(path,expected_generation="wrong")
        except ProviderGenerationMismatch: pass
        else: raise AssertionError("sqlite generation mismatch not rejected")
    obj={"z":1,"a":[2,1],"u":"é"}
    assert canonical_sha256(obj)==canonical_sha256(json.loads(json.dumps(obj,ensure_ascii=False)))
    print("AIR durable provenance provider validation: PASS")

if __name__=="__main__": main()
