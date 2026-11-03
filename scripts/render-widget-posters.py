#!/usr/bin/env python3
"""Screenshot each rendered slide widget (notebooks/slide-<name>.qmd) at its
initial slider values as the PDF poster media/posters/slide-<name>.png.

Usage: uv run python scripts/render-widget-posters.py [<rendered-notebooks-dir>]
       (default public/notebooks; render first with scripts/build-notebooks.sh)
The frame has the aspect of the deck's widget area, 257 mm x 150 mm.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 970, round(970 * 150 / 257)


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rendered", type=Path, nargs="?", default=ROOT / "public/notebooks")
    parser.add_argument("--chrome", default=None, help="Chromium executable")
    args = parser.parse_args()
    # Observable JS does not start from file:// URLs.
    handler = partial(Quiet, directory=str(args.rendered.resolve()))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    names = sorted(p.stem for p in (ROOT / "notebooks").glob("slide-*.qmd"))
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=args.chrome, headless=True)
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=3)
        for name in names:
            page.goto(f"http://127.0.0.1:{server.server_port}/{name}.html")
            page.wait_for_selector("svg[class^=plot], canvas", timeout=60000)
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready")
            # Simulations run on: give their running averages time to settle.
            page.wait_for_timeout(20000)
            out = ROOT / "media/posters" / f"{name}.png"
            page.screenshot(path=str(out))
            print(f"Poster written: {out.relative_to(ROOT)}")
        browser.close()
    server.shutdown()


if __name__ == "__main__":
    main()
