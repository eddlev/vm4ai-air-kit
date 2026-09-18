from __future__ import annotations
import shutil, tempfile
from pathlib import Path
from validate_air_full_surface_integrity import validate, ValidationError

def expect_kill(root,mutate):
    with tempfile.TemporaryDirectory() as td:
        dst=Path(td)/"repo"; shutil.copytree(root,dst); mutate(dst)
        try: validate(dst)
        except (ValidationError,KeyError,ValueError): return
        raise AssertionError("mutation survived")

def main():
    root=Path(".").resolve(); killed=0
    muts=[
        lambda r:(r/"profiles/_mutation_unmanifested.json").write_text("{}",encoding="utf-8"),
        lambda r:(r/"prompts/AIR_CORE_RUNTIME.md").write_text((r/"prompts/AIR_CORE_RUNTIME.md").read_text().replace("Patch marker: AIR_DURABILITY_NEGOTIATION_ROUTE_V1","REMOVED"),encoding="utf-8"),
        lambda r:(r/"prompts/AIR_CONTROL_SURFACE.md").write_text((r/"prompts/AIR_CONTROL_SURFACE.md").read_text().replace("E. Recover or continue an existing AIR project without a valid Handoff","REMOVED"),encoding="utf-8"),
        lambda r:(r/"catalog/AIR_RUNTIME_ROUTE_MAP.json").write_text((r/"catalog/AIR_RUNTIME_ROUTE_MAP.json").read_text().replace('"RT.DURABILITY_NEGOTIATE"','"RT.ACTIVATE"',1),encoding="utf-8"),
        lambda r:(r/"profiles/grounding specialist/AIR_GROUNDING_EXECUTOR.json").write_text((r/"profiles/grounding specialist/AIR_GROUNDING_EXECUTOR.json").read_text().replace("V2_5_0_OBJECT_CONTRACT_SET_008_STATIC_VALIDATED_AVAILABLE_UNBOUND","DRAFT",1),encoding="utf-8")
    ]
    for m in muts: expect_kill(root,m); killed+=1
    print(f"AIR full-surface mutation tests: PASS ({killed}/{len(muts)} killed)")
if __name__=="__main__": main()
