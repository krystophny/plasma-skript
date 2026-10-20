#!/usr/bin/env python3
"""Write the launch frame of the coupling animation for the coupling slide.

The slide still (slides/coupling-still.json) and the coupling-test-particle
animation share frozen electrons, launch point, Debye radii and the inside
flags; scripts/check-physics.py fails when the file is stale.
"""
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "slides/coupling-still.json"


def still():
    model = runpy.run_path(str(ROOT / "scripts/check-physics.py"))["model"]
    return model("coupling_test_particle.py")["still_data"]()


if __name__ == "__main__":
    OUT.write_text(json.dumps(still(), separators=(",", ":")) + "\n")
    print("Wrote", OUT.relative_to(ROOT))
