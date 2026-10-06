#!/usr/bin/env python3
"""Export exactly the registered animation revisions, never stale renders."""
import json
from pathlib import Path
import runpy
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def export(site, destination):
    copy_video = runpy.run_path(str(ROOT / "scripts/build-present.py"))["copy_video"]
    records = json.loads((ROOT / "media/animations.json").read_text())["animations"]
    for slug, record in records.items():
        video = copy_video(record, slug, destination, site)
        poster = ROOT / record["poster"]
        if not poster.is_file():
            raise FileNotFoundError(f"Missing registered poster: {poster}")
        shutil.copyfile(poster, destination / (video.stem + ".png"))
    print(f"Exported {len(records)} checksum-verified animation revisions")


if __name__ == "__main__":
    export(Path(sys.argv[1]), Path(sys.argv[2]))
