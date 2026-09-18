from __future__ import annotations
import json, sqlite3, uuid
from pathlib import Path
from typing import Any
from .canonical_json import canonical_json_bytes, canonical_sha256
from .contract import ADAPTER_CONTRACT, CANONICALIZATION_CONTRACT, ProviderGenerationMismatch, ProviderIntegrityError, SnapshotKey

class SQLiteDurableProvenanceProvider:
    def __init__(self, path: str | Path, *, expected_generation: str | None = None):
        self.path=Path(path); self.path.parent.mkdir(parents=True, exist_ok=True); self.db=sqlite3.connect(self.path)
        self.db.execute("create table if not exists meta(k text primary key,v text not null)")
        self.db.execute("create table if not exists records(namespace_id text, emission_sequence integer, ledger_entry_ref text, sha256 text, snapshot text, state text, provider_generation text, primary key(namespace_id,ledger_entry_ref))")
        self.db.commit()
        row=self.db.execute("select v from meta where k='generation'").fetchone()
        if row: gen=row[0]
        else: gen=str(uuid.uuid4()); self.db.execute("insert into meta values('generation',?)",(gen,)); self.db.commit()
        if expected_generation and gen != expected_generation: raise ProviderGenerationMismatch("provider generation mismatch")
        self.generation=gen

    def describe_provider(self) -> dict[str, Any]:
        return {"adapter_contract":ADAPTER_CONTRACT,"provider_identity":"AIR_SQLITE_DURABLE_PROVENANCE_V1","provider_class":"SQLITE","provider_generation":self.generation,"provider_instance_id":str(self.path.resolve()),"canonicalization_contract":CANONICALIZATION_CONTRACT,"authorization_state":"LOCAL_PROVIDER_AUTHORIZED_BY_CALLER","storage_state":"AVAILABLE","positive_execution_authority":"NONE"}

    def probe_write_readback(self) -> dict[str, Any]:
        token=str(uuid.uuid4()); self.db.execute("create table if not exists probe(k text primary key,v text)")
        self.db.execute("insert into probe values(?,?)",(token,token)); self.db.commit()
        got=self.db.execute("select v from probe where k=?",(token,)).fetchone()
        self.db.execute("delete from probe where k=?",(token,)); self.db.commit()
        if not got or got[0] != token: raise ProviderIntegrityError("probe readback mismatch")
        return {"discovery_state":"PROVIDER_VERIFIED","write_readback_state":"PASS"}

    def open_project_namespace(self, namespace_id: str) -> dict[str, Any]:
        if not namespace_id or "/" in namespace_id or "\\" in namespace_id: raise ValueError("opaque namespace id required")
        return {"namespace_id":namespace_id,"namespace_fingerprint":canonical_sha256({"provider_generation":self.generation,"namespace_id":namespace_id})}

    def prepare_snapshot(self, key: SnapshotKey, snapshot: Any) -> dict[str, Any]:
        if canonical_sha256(snapshot) != key.canonical_object_sha256: raise ProviderIntegrityError("snapshot hash mismatch")
        self.open_project_namespace(key.namespace_id)
        raw=canonical_json_bytes(snapshot).decode("utf-8")
        self.db.execute("insert or replace into records values(?,?,?,?,?,?,?)",(key.namespace_id,key.emission_sequence,key.ledger_entry_ref,key.canonical_object_sha256,raw,"PREPARED",self.generation)); self.db.commit()
        return self.read_snapshot(key)

    def read_snapshot(self, key: SnapshotKey) -> dict[str, Any]:
        r=self.db.execute("select emission_sequence,ledger_entry_ref,sha256,snapshot,state,provider_generation from records where namespace_id=? and ledger_entry_ref=?",(key.namespace_id,key.ledger_entry_ref)).fetchone()
        if not r: raise KeyError(key.ledger_entry_ref)
        snap=json.loads(r[3])
        if r[5] != self.generation or canonical_sha256(snap) != r[2]: raise ProviderIntegrityError("stored record integrity failure")
        return {"provenance_store_id":"AIR_SQLITE_DURABLE_PROVENANCE_V1","emission_sequence":r[0],"ledger_entry_ref":r[1],"canonical_object_sha256":r[2],"canonical_object_snapshot":snap,"record_state":r[4],"provider_generation":r[5],"project_namespace_id":key.namespace_id,"positive_execution_authority":"NONE"}

    def commit_visible(self, key: SnapshotKey) -> dict[str, Any]:
        rec=self.read_snapshot(key)
        if rec["record_state"] != "PREPARED": raise ProviderIntegrityError("only PREPARED may commit")
        self.db.execute("update records set state='COMMITTED_VISIBLE' where namespace_id=? and ledger_entry_ref=?",(key.namespace_id,key.ledger_entry_ref)); self.db.commit()
        return self.read_snapshot(key)

    def mark_orphaned(self, key: SnapshotKey) -> dict[str, Any]:
        self.db.execute("update records set state='ORPHANED' where namespace_id=? and ledger_entry_ref=?",(key.namespace_id,key.ledger_entry_ref)); self.db.commit()
        return self.read_snapshot(key)

    def retrieve_committed_range(self, namespace_id: str, start: int, end: int) -> list[dict[str, Any]]:
        rows=self.db.execute("select emission_sequence,ledger_entry_ref,sha256,snapshot,state,provider_generation from records where namespace_id=? and state='COMMITTED_VISIBLE' and emission_sequence between ? and ? order by emission_sequence",(namespace_id,start,end)).fetchall()
        out=[]
        for r in rows:
            snap=json.loads(r[3])
            if r[5] != self.generation or canonical_sha256(snap) != r[2]: raise ProviderIntegrityError("tampered committed snapshot")
            out.append({"emission_sequence":r[0],"ledger_entry_ref":r[1],"canonical_object_sha256":r[2],"canonical_object_snapshot":snap,"record_state":r[4]})
        return out

    def verify_coverage(self, namespace_id: str, expected: list[dict[str, Any]]) -> dict[str, Any]:
        if not expected: return {"coverage_state":"COMPLETE","missing":[],"duplicates":[],"provider_only":[]}
        got=self.retrieve_committed_range(namespace_id,min(x["emission_sequence"] for x in expected),max(x["emission_sequence"] for x in expected))
        exp={(x["emission_sequence"],x["ledger_entry_ref"],x["canonical_object_sha256"]) for x in expected}
        obs=[(x["emission_sequence"],x["ledger_entry_ref"],x["canonical_object_sha256"]) for x in got]; obsset=set(obs); dups=sorted({x for x in obs if obs.count(x)>1})
        return {"coverage_state":"COMPLETE" if exp==obsset and not dups else "INCOMPLETE","missing":sorted(exp-obsset),"duplicates":dups,"provider_only":sorted(obsset-exp)}
