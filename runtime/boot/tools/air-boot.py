#!/usr/bin/env python3
"""Compatibility adapter from the v0.3.0 air-boot command to installed ``air boot`` services."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vm4ai_air.cli import main as air_main  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="air-boot")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--manifest", default="runtime/boot/AIR BOOT MODULE MANIFEST.json")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate-manifest")
    validate_module = sub.add_parser("validate-module")
    validate_module.add_argument("module_id")
    plan = sub.add_parser("plan")
    plan.add_argument("--trigger", action="append", default=[])
    bundle = sub.add_parser("bundle")
    bundle.add_argument("--trigger", action="append", default=[])
    bundle.add_argument("--output", required=True)
    bundle.add_argument("--overwrite", action="store_true")
    receipt = sub.add_parser("receipt")
    receipt.add_argument("--trigger", action="append", default=[])
    receipt.add_argument("--output", required=True)
    receipt.add_argument("--overwrite", action="store_true")
    compare = sub.add_parser("compare")
    compare.add_argument("--triggers", nargs="*", default=[])
    sub.add_parser("status")
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve()
    expected_manifest = (root / args.manifest).resolve()
    canonical_manifest = (root / "runtime/boot/AIR BOOT MODULE MANIFEST.json").resolve()
    if expected_manifest != canonical_manifest:
        parser.error("Stage 3 compatibility mode accepts only the canonical boot manifest")
    os.environ["AIR_RESOURCE_ROOT"] = str(root)

    command = ["--json", "boot"]
    if args.command == "validate-manifest":
        command += ["validate"]
    elif args.command == "validate-module":
        command += ["validate", "--module", args.module_id]
    elif args.command == "plan":
        command += ["plan"]
        for trigger in args.trigger:
            command += ["--trigger", trigger]
    elif args.command == "bundle":
        command += ["compile", "--output", args.output]
        for trigger in args.trigger:
            command += ["--trigger", trigger]
        if args.overwrite:
            command.append("--overwrite")
    elif args.command == "receipt":
        command += ["receipt", "--output", args.output]
        for trigger in args.trigger:
            command += ["--trigger", trigger]
        if args.overwrite:
            command.append("--overwrite")
    elif args.command == "compare":
        command += ["compare"]
        for trigger in args.triggers:
            command += ["--trigger", trigger]
    else:
        command += ["status"]
    return air_main(command)


if __name__ == "__main__":
    raise SystemExit(main())
