from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

DIMS=["PHYSICAL_PARSE","IDENTITY_LIFECYCLE","CLOSED_WORLD_SCHEMA","SEMANTIC_OWNERSHIP","PRODUCER_CONSUMER","CROSS_FILE_REFERENCE","AUTHORITY_BOUNDARY","VISIBILITY_EMISSION","ROUTE_STATE_MACHINE","FAILURE_MODE","BEHAVIORAL_CONTRACT","MUTATION_TEST","MIGRATION_BACKWARD_COMPAT","SECURITY_PRIVACY_DATA_BOUNDARY","RELEASE_REPRODUCIBILITY"]
class ValidationError(Exception): pass
def req(c,m):
    if not c: raise ValidationError(m)
def reject_dupes(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValidationError("duplicate JSON key: "+k)
        out[k]=v
    return out
def loadj(p):
    return json.loads(p.read_text(encoding="utf-8"),object_pairs_hook=reject_dupes)
def discover(root):
    return sorted(str(p.relative_to(root)).replace("\\","/") for base in ("prompts","catalog","profiles") for p in (root/base).rglob("*") if p.is_file())

def validate(root):
    cov=loadj(root/"tests/air_full_surface_coverage_manifest.json")
    found=discover(root); listed=sorted(x["canonical_path"] for x in cov["files"])
    req(found==listed,f"coverage parity mismatch discovered-only={sorted(set(found)-set(listed))} manifest-only={sorted(set(listed)-set(found))}")
    for rec in cov["files"]:
        p=root/rec["canonical_path"]; raw=p.read_bytes()
        req(not raw.startswith(b"\xef\xbb\xbf"),"BOM prohibited: "+str(p))
        raw.decode("utf-8")
        if p.suffix==".json": loadj(p)
        req(set(rec["applicable_audit_dimensions"])==set(DIMS),"audit dimensions incomplete: "+str(p))
        req(rec["current_result"] in ("PASS","NOT_APPLICABLE_WITH_EVIDENCE"),"blocking result: "+str(p))
    core=(root/"prompts/AIR_CORE_RUNTIME.md").read_text(encoding="utf-8")
    control=(root/"prompts/AIR_CONTROL_SURFACE.md").read_text(encoding="utf-8")
    for marker in ("AIR_DURABILITY_NEGOTIATION_ROUTE_V1","AIR_FULL_SURFACE_INTEGRITY_AUDIT_V1","AIR_MANDATORY_VISIBLE_ALIGNMENT_VALIDATION_V1","AIR_NEW_TASK_ARTIFACT_VISIBLE_V1","AIR_EXECUTOR_INTEGRAL_PACKAGE_COMPONENT_V1"):
        req(("Patch marker: "+marker) in core,"missing Core marker "+marker)
    req("E. Recover or continue an existing AIR project without a valid Handoff" in control,"Q1-E missing")
    routes={x["route_id"]:x for x in loadj(root/"catalog/AIR_RUNTIME_ROUTE_MAP.json")["routes"]}
    req(routes["RT.ONBOARD"]["allowed_next_routes"]==["RT.DURABILITY_NEGOTIATE"],"ONBOARD bypasses durability negotiation")
    req(routes["RT.HANDOFF_RESTORE"]["allowed_next_routes"]==["RT.DURABILITY_NEGOTIATE"],"restore bypasses durability negotiation")
    req("DEP.DURABILITY_NEGOTIATION_RESOLVED" in routes["RT.ACTIVATE"]["requires"],"ACTIVATE missing durability dependency")
    pc=loadj(root/"prompts/AIR_HANDOFF_CARD_TEMPLATE.json")["AIR_HANDOFF_CARD"]["surfaced_object_ledger_state"]["provenance_capture"]
    for k in ("canonicalization_contract","provider_identity","provider_generation","provider_instance_id","project_namespace_id","project_namespace_fingerprint","storage_location_class","authorization_state_at_capture","retention_policy","deletion_policy","credentials_serialized"):
        req(k in pc,"Handoff provenance missing "+k)
    req(pc["credentials_serialized"] is False,"credential serialization must be false")
    for mp in (root/"profiles").rglob("*PACKAGE_MANIFEST.json"):
        m=loadj(mp)
        for comp in m.get("components",[]):
            target=mp.parent/comp["filename"]; req(target.exists(),"missing component "+str(target)); raw=target.read_bytes()
            if "sha256" in comp: req(hashlib.sha256(raw).hexdigest()==comp["sha256"],"component hash mismatch "+str(target))
            if "size_bytes" in comp: req(len(raw)==comp["size_bytes"],"component size mismatch "+str(target))
            if "EXECUTOR" in comp["filename"]:
                req(comp.get("status")!="DRAFT","Executor remains DRAFT")
                req(comp.get("availability_state")!="AVAILABLE_UNVALIDATED","Executor remains AVAILABLE_UNVALIDATED")
                ej=loadj(target); req(ej.get("STATUS")!="DRAFT","Executor file remains DRAFT")
                ec=ej.get("executor_validation_contract",{})
                req(ec.get("integral_package_component") is True,"Executor integral component contract missing")
                req(ec.get("independent_execution_authority") is False,"Executor authority boundary weakened")
    matrix=loadj(root/"tests/air_full_surface_scenario_matrix.json")
    req(matrix["scenario_count"]>=20 and len(matrix["scenarios"])>=20,"public-user scenario coverage incomplete")
    return {"files":len(found),"dimensions":len(DIMS),"scenarios":len(matrix["scenarios"])}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("root",nargs="?",default="."); args=ap.parse_args()
    try:
        r=validate(Path(args.root).resolve())
        print(f"AIR full-surface integrity validation: PASS ({r['files']} files, {r['dimensions']} dimensions, {r['scenarios']} scenarios)")
    except ValidationError as e:
        raise SystemExit("AIR full-surface integrity validation FAILED: "+str(e))
if __name__=="__main__": main()
