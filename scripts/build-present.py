#!/usr/bin/env python3
"""Export the paged Typst sources as hashed, same-origin presenter decks.

Only stdlib and the Typst CLI are required. MP4 downloads must match the
registered checksum; missing posters, metadata or PDF pages abort the build.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def source_digest():
    """Content identity survives committing a verified working-tree build."""
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).split(b"\0")
    digest = hashlib.sha256()
    for name in sorted(p for p in paths if p):
        path = ROOT / os.fsdecode(name)
        digest.update(name + b"\0")
        digest.update(path.read_bytes() if path.is_file() else b"<deleted>")
    return digest.hexdigest()


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def version(path):
    return path.name + "?v=" + sha(path)[:8]


def pdf_pages(path):
    # Typst emits an uncompressed page-tree root. Fail rather than guessing
    # if a future PDF writer changes that representation.
    counts = re.findall(rb"/Type\s*/Pages\b\s*/Count\s+(\d+)", path.read_bytes())
    if not counts:
        raise ValueError(f"Cannot read Typst PDF page tree: {path}")
    return max(map(int, counts))


class VideoAlternatives(HTMLParser):
    def __init__(self):
        super().__init__()
        self.alts = {}

    def handle_starttag(self, tag, attrs):
        if tag == "video":
            attrs = dict(attrs)
            self.alts[urlsplit(attrs.get("src", "")).path] = attrs.get("aria-label", "")


def copy_video(record, slug, dest, site):
    filename = Path(urlsplit(record["stream_url"]).path).name
    expected = record["mp4_sha256"]
    cache = ROOT / ".cache/present-media"
    candidates = [site / "media" / (slug + ".mp4"),
                  site / "present/media" / filename,
                  Path(os.environ.get("PRESENT_MEDIA_DIR", ROOT / ".cache/animations")) / (slug + ".mp4"),
                  Path(os.environ.get("MEDIA_DIR", ROOT / ".cache/animations")) / (slug + ".mp4"),
                  ROOT / ".cache/animations" / (slug + ".mp4"),
                  cache / (expected + ".mp4")]
    if os.environ.get("EXPORT_MEDIA_SOURCE"):
        candidates.append(Path(os.environ["EXPORT_MEDIA_SOURCE"]) / filename)
    for path in candidates:
        if path.is_file() and sha(path) == expected:
            if path.resolve() != (dest / filename).resolve():
                shutil.copyfile(path, dest / filename)
            return dest / filename
    cache.mkdir(parents=True, exist_ok=True)
    temp = cache / (expected + ".part")
    try:
        print(f"Downloading registered presenter video: {slug}", flush=True)
        with urlopen(record["stream_url"], timeout=120) as source, temp.open("wb") as target:
            shutil.copyfileobj(source, target)
        if sha(temp) != expected:
            raise ValueError(f"Checksum mismatch for presenter video: {slug}")
        saved = cache / (expected + ".mp4")
        temp.replace(saved)
        shutil.copyfile(saved, dest / filename)
        return dest / filename
    finally:
        temp.unlink(missing_ok=True)


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def build(site):
    target = site / "present"
    target.mkdir(parents=True, exist_ok=True)
    for path in (ROOT / "src/present").iterdir():
        if path.is_file() and path.name != "deck.html":
            shutil.copyfile(path, target / path.name)
    media = target / "media"
    media.mkdir(exist_ok=True)
    records = json.loads((ROOT / "media/animations.json").read_text())["animations"]
    outline = json.loads((ROOT / "slides/build/script-outline.json").read_text())
    chapters = {c["number"]: c["title"] for c in outline["chapters"]}
    parser = VideoAlternatives()
    for path in (site / "animations").glob("*.html"):
        parser.feed(path.read_text())
    typst = ["typst", "--root", str(ROOT), "--font-path", str(ROOT / "fonts"),
             "--ignore-system-fonts"]
    decks = []
    for source in sorted((ROOT / "slides").glob("[0-9]*.typ")):
        stem = source.stem
        folder = target / stem
        folder.mkdir(exist_ok=True)
        for old in folder.glob("p*.svg"):
            old.unlink()
        subprocess.run([typst[0], "compile", *typst[1:], "--format", "svg",
                        str(source), str(folder / "p{0p}.svg")], check=True)
        raw = subprocess.check_output([typst[0], "query", *typst[1:], str(source),
                                       "<present-page>", "--field", "value"])
        metadata = json.loads(raw)
        count = pdf_pages(site / "slides" / (stem + ".pdf"))
        svgs = sorted(folder.glob("p*.svg"))
        if len(metadata) != count or len(svgs) != count:
            raise ValueError(f"{stem}: PDF={count}, SVG={len(svgs)}, metadata={len(metadata)}")
        if [p["page"] for p in metadata] != list(range(1, count + 1)):
            raise ValueError(f"{stem}: expected exactly one metadata entry on each page")
        chapter = int(stem.split("-", 1)[0])
        pages = []
        for number, (svg, spec) in enumerate(zip(svgs, metadata), 1):
            # The template's padding depends on page count; the public contract
            # always uses at least two digits.
            canonical = folder / f"p{number:02}.svg"
            if svg != canonical:
                svg.rename(canonical)
            if spec["kind"] not in ("static", "animation") or spec["chapter"] != chapter:
                raise ValueError(f"Invalid presenter metadata: {stem} page {number}")
            page = {"src": version(canonical), "kind": spec["kind"],
                    "background": spec["background"], "alt": spec["alt"]}
            if spec["kind"] == "animation":
                slug = spec["slug"]
                record = records[slug]
                if spec["video"] != record["stream_url"]:
                    raise ValueError(f"Video metadata differs from registry: {slug}")
                video = copy_video(record, slug, media, site)
                poster = ROOT / record["poster"]
                if not poster.is_file():
                    raise FileNotFoundError(f"Missing presenter poster: {poster}")
                shutil.copyfile(poster, media / (slug + ".png"))
                alt = parser.alts.get(urlsplit(record["stream_url"]).path)
                if not alt:
                    raise ValueError(f"Missing existing animation alternative: {slug}")
                page.update(video="../media/" + version(video),
                            poster="../media/" + version(media / (slug + ".png")),
                            loop=spec["loop"], alt=alt)
            if not page["alt"]:
                raise ValueError(f"Empty page alternative: {stem} page {number}")
            pages.append(page)
        manifest = dict(stem=stem, chapter=chapter, title=chapters[chapter],
                        course="Plasma Physics", author="Christopher Albert",
                        aspect=297 / 210, pdf=f"../../slides/{stem}.pdf", pages=pages)
        write_json(folder / "manifest.json", manifest)
        shutil.copyfile(ROOT / "src/present/deck.html", folder / "index.html")
        decks.append(dict(stem=stem, chapter=chapter, title=chapters[chapter],
                          pages=count, cover=stem + "/" + pages[0]["src"]))
        print(f"Presenter: {stem}: {count} pages", flush=True)
    if not decks:
        raise ValueError("No lecture decks found")
    write_json(target / "decks.json", {"decks": decks})
    if (ROOT / ".git").exists():
        write_json(target / "build-revision.json", {"source_sha256": source_digest()})


if __name__ == "__main__":
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("site", type=Path, nargs="?", default=ROOT / "public")
    build(args.parse_args().site.resolve())
