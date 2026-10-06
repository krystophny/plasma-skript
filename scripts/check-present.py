#!/usr/bin/env python3
"""Check the exported presenter contract without starting a browser."""
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, urlsplit


def check(site):
    root = site / "present"
    for name in ("index.html", "present.css", "present.js", "sw.js",
                 "manifest.webmanifest", "icon.svg", "icon-180.png", "icon-512.png"):
        assert (root / name).is_file(), f"Missing presenter asset: {name}"
    decks = json.loads((root / "decks.json").read_text())["decks"]
    assert decks, "No published lecture decks"

    def hashed(base, url):
        parts = urlsplit(url)
        assert not parts.scheme and not parts.netloc, f"Media must be same-origin: {url}"
        path = (base / parts.path).resolve()
        assert path.is_relative_to(site.resolve()), f"Path escapes public bundle: {url}"
        assert path.is_file(), f"Missing presenter media: {url}"
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()[:8]
        assert parse_qs(parts.query).get("v") == [digest], f"Missing or incorrect content hash: {url}"

    for deck in decks:
        folder = root / deck["stem"]
        assert (folder / "index.html").is_file()
        manifest = json.loads((folder / "manifest.json").read_text())
        assert manifest["stem"] == deck["stem"] and manifest["chapter"] == deck["chapter"]
        assert manifest["course"] == "Plasma Physics" and manifest["author"] == "Christopher Albert"
        assert abs(manifest["aspect"] - 297 / 210) < 1e-10
        pages = manifest["pages"]
        pdf = (folder / manifest["pdf"]).read_bytes()
        counts = re.findall(rb"/Type\s*/Pages\b\s*/Count\s+(\d+)", pdf)
        assert counts and max(map(int, counts)) == len(pages) == deck["pages"]
        hashed(root, deck["cover"])
        for number, page in enumerate(pages, 1):
            assert page["kind"] in ("static", "animation"), "Blank or unknown page kind"
            assert page["background"] in ("light", "dark") and page["alt"].strip()
            assert urlsplit(page["src"]).path == f"p{number:02}.svg"
            hashed(folder, page["src"])
            if page["kind"] == "animation":
                assert isinstance(page["loop"], bool)
                hashed(folder, page["video"])
                hashed(folder, page["poster"])
    print(f"Presenter contract passed: {len(decks)} decks, hashed pages and same-origin media")


if __name__ == "__main__":
    check(Path(sys.argv[1] if len(sys.argv) > 1 else "public"))
