#!/usr/bin/env python3
"""Write the frozen frame of the coupling-regions animation for the coupling slide.

slides/coupling-regions.json holds the drawn electrons, temperatures, Gamma_e,
lambda_D/a and colour limits of both panels; slides/coupling-regions-<p>.png
the net charge density on the white slide background with the animation's
colour map and limits.  scripts/check-physics.py fails when they are stale.
"""
import json
from pathlib import Path
import runpy

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "slides/coupling-regions.json"


def image_path(p):
    return ROOT / f"slides/coupling-regions-{p}.png"


def still():
    model = runpy.run_path(str(ROOT / "scripts/check-physics.py"))["model"]
    return model("coupling_regions.py")["still_data"]()


if __name__ == "__main__":
    record, images = still()
    OUT.write_text(json.dumps(record, separators=(",", ":")) + "\n")
    for p, image in enumerate(images):
        Image.fromarray(np.ascontiguousarray(image)).save(image_path(p), optimize=True)
    print("Wrote", OUT.relative_to(ROOT), "and", len(images), "field images")
