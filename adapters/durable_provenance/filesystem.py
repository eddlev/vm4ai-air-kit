from __future__ import annotations
import json, os, tempfile, uuid
from pathlib import Path
from typing import Any
from .canonical_json import canonical_json_bytes, canonical_sha256
from .contract import ADAPTER_CONTRACT, CANONICALIZATION_CONTRACT, ProviderGenerationMismatch, ProviderIntegrityError, SnapshotKey

class FilesystemDurableProvenanceProvider:
    def __init__(self, root: str | Path, *, expected_generation: str | None = None):
        self.root = Path(root); self.root.mkdir(parents=True, exist_ok=True)
        self.meta = self.root / ".air_provider.json"
        if self.meta.exists():
            info = json.loads(self.meta.read_text(encoding="utf-8"))
        else:
            info = {"provider_identity":"AIR_FILESYSTEM_DURABLE_PROVENANCE_V1","provider_class":"FILESYSTEM","provider_generation":str(uuid.uuid4()),"provider_instance_id":str(self.root.resolve())}
            self._atomic(self.meta, canonical_json_bytes(info))
        if expected_generation and info["provider_generation"] != expected_generation:
            raise ProviderGenerationMismatch("provider generation mismatch")
        self.info = info

    def _atomic(self, path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".air.")
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(data); f.flush(); os.fsync(f.fileno())
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)

    def describe_provider(self) -> dict[str, Any]:
        return {"adapter_contract":ADAPTER_CONTRACT, **self.info, "canonicalization_contract":CANONICALIZATION_CONTRACT, "authorization_state":"LOCAL_PROVIDER_AUTHORIZED_BY_CALLER", "storage_state":"AVAILABLE", "positive_execution_authority":"NONE"}

    def probe_write_readback(self) -> dict[str, Any]:
        p = self.root / ".probe" / (str(uuid.uuid4()) + ".bin"); data = os.urandom(32)
        self._atomic(p, data); got = p.read_bytes(); p.unlink()
        if got != data: raise ProviderIntegrityError("probe readback mismatch")
        return {"discovery_state":"PROVIDER_VERIFIED","write_readback_state":"PASS"}

    def open_project_namespace(self, namespace_id: str) -> dict[str, Any]:
        if not namespace_id or "/" in namespace_id or "\\" in namespace_id: raise ValueError("opaque namespace id required")
        (self.root / "namespaces" / namespace_id).mkdir(parents=True, exist_ok=True)
        return {"namespace_id":namespace_id,"namespace_fingerprint":canonical_sha256({"provider_generation":self.info["provider_generation"],"namespace_id":namespace_id})}

    def _path(self, key: SnapshotKey, state: str) -> Path:
        return self.root/"namespaces"/key.namespace_id/state/f"{key.emission_sequence:012d}-{canonical_sha256(key.ledger_entry_ref)[:16]}.json"

    def _record(self, key: SnapshotKey, snapshot: Any, state: str) -> dict[str, Any]:
        if canonical_sha256(snapshot) != key.canonical_object_sha256: raise ProviderIntegrityError("snapshot hash mismatch")
        return {"provenance_store_id":self.info["provider_identity"],"ledger_entry_ref":key.ledger_entry_ref,"emission_sequence":key.emission_sequence,"canonical_object_sha256":key.canonical_object_sha256,"canonical_object_snapshot":snapshot,"record_state":state,"provider_generation":self.info["provider_generation"],"project_namespace_id":key.namespace_id,"positive_execution_authority":"NONE"}

    def prepare_snapshot(self, key: SnapshotKey, snapshot: Any) -> dict[str, Any]:
        self.open_project_namespace(key.namespace_id); rec=self._record(key,snapshot,"PREPARED"); self._atomic(self._path(key,"prepared"),canonical_json_bytes(rec)); return rec

    def read_snapshot(self, key: SnapshotKey) -> dict[str, Any]:
        for state in ("committed","prepared","orphaned"):
            p=self._path(key,state)
            if p.exists():
                rec=json.loads(p.read_text(encoding="utf-8"))
                if rec["provider_generation"] != self.info["provider_generation"] or canonical_sha256(rec["canonical_object_snapshot"]) != rec["canonical_object_sha256"]:
                    raise ProviderIntegrityError("stored record integrity failure")
                return rec
        raise KeyError(key.ledger_entry_ref)

    def commit_visible(self, key: SnapshotKey) -> dict[str, Any]:
        rec=self.read_snapshot(key)
        if rec["record_state"] != "PREPARED": raise ProviderIntegrityError("only PREPARED may commit")
        rec["record_state"]="COMMITTED_VISIBLE"; src=self._path(key,"prepared"); dst=self._path(key,"committed"); self._atomic(dst,canonical_json_bytes(rec)); src.unlink(missing_ok=True); return rec

    def mark_orphaned(self, key: SnapshotKey) -> dict[str, Any]:
        rec=self.read_snapshot(key); rec["record_state"]="ORPHANED"; src=self._path(key,"prepared"); dst=self._path(key,"orphaned"); self._atomic(dst,canonical_json_bytes(rec)); src.unlink(missing_ok=True); return rec

    def retrieve_committed_range(self, namespace_id: str, start: int, end: int) -> list[dict[str, Any]]:
        p=self.root/"namespaces"/namespace_id/"committed"; out=[]
        for f in sorted(p.glob("*.json")) if p.exists() else []:
            rec=json.loads(f.read_text(encoding="utf-8"))
            if start <= rec["emission_sequence"] <= end:
                if canonical_sha256(rec["canonical_object_snapshot"]) != rec["canonical_object_sha256"]: raise ProviderIntegrityError("tampered committed snapshot")
                out.append(rec)
        return out

    def verify_coverage(self, namespace_id: str, expected: list[dict[str, Any]]) -> dict[str, Any]:
        if not expected: return {"coverage_state":"COMPLETE","missing":[],"duplicates":[],"provider_only":[]}
        got=self.retrieve_committed_range(namespace_id,min(x["emission_sequence"] for x in expected),max(x["emission_sequence"] for x in expected))
        exp={(x["emission_sequence"],x["ledger_entry_ref"],x["canonical_object_sha256"]) for x in expected}
        obs=[(x["emission_sequence"],x["ledger_entry_ref"],x["canonical_object_sha256"]) for x in got]
        dups=sorted({x for x in obs if obs.count(x)>1}); obsset=set(obs)
        return {"coverage_state":"COMPLETE" if exp==obsset and not dups else "INCOMPLETE","missing":sorted(exp-obsset),"duplicates":dups,"provider_only":sorted(obsset-exp)}
