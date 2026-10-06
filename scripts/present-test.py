#!/usr/bin/env python3
"""Exercise real touch, H.264 playback and offline decks against exported PDFs.

Usage: uv run python scripts/present-test.py public
       uv run python scripts/present-test.py https://.../present/
Chrome with H.264 is required; no mocked videos or service worker routes.
"""
import argparse
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
import re
import runpy
import subprocess
import tempfile
from threading import Thread
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright


def pdf_count(data):
    with tempfile.TemporaryDirectory() as directory:
        pdf = Path(directory) / "deck.pdf"
        pdf.write_bytes(data)
        info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    return int(re.search(r"^Pages:\s+(\d+)", info, re.M)[1])


def swipe(page):
    # Chrome's input protocol sends genuine touch events through hit testing.
    session = page.context.new_cdp_session(page)
    for kind, x in [("touchStart", 850), ("touchMove", 700), ("touchMove", 500),
                    ("touchEnd", None)]:
        points = [] if x is None else [{"x": x, "y": 410}]
        session.send("Input.dispatchTouchEvent", {"type": kind, "touchPoints": points})
    session.detach()


def ready(page, count):
    page.wait_for_function("n => document.querySelectorAll('.page').length === n", arg=count)
    page.wait_for_function("navigator.serviceWorker.controller !== null")
    page.wait_for_function("document.querySelector('.page.current img')?.naturalWidth > 0")


def check(browser, base, artifacts):
    response = browser.new_context()
    decks = response.request.get(urljoin(base, "decks.json")).json()["decks"]
    response.close()
    for deck in decks:
        context = browser.new_context(viewport={"width": 1180, "height": 820}, has_touch=True)
        context.add_init_script("""
          window.cacheResult = null;
          navigator.serviceWorker.addEventListener('message', e => {
            if (e.data?.type === 'cached') window.cacheResult = e.data;
          });
        """)
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
        url = urljoin(base, deck["stem"] + "/")
        manifest = context.request.get(urljoin(url, "manifest.json")).json()
        pdf = context.request.get(urljoin(url, manifest["pdf"]))
        assert pdf.ok, f"PDF missing: {deck['stem']}"
        count = pdf_count(pdf.body())
        assert len(manifest["pages"]) == deck["pages"] == count
        page.goto(url)
        ready(page, count)
        page.touchscreen.tap(1050, 410)
        page.wait_for_url("**/#2")
        swipe(page)
        page.wait_for_url("**/#3")
        page.touchscreen.tap(130, 410)
        page.wait_for_url("**/#2")
        page.keyboard.press("End")
        page.wait_for_url(f"**/#{count}")
        page.keyboard.press("Home")
        page.wait_for_url("**/#1")
        # Every page must display real content; inspect all images, rather
        # than treating metadata or nonzero SVG bytes as a visual oracle.
        animations = []
        for number, spec in enumerate(manifest["pages"], 1):
            page.evaluate("n => location.hash = '#' + n", number)
            page.wait_for_function("n => document.querySelector('.where b')?.textContent === String(n)", arg=number)
            image = page.locator(".page.current img")
            page.wait_for_function("document.querySelector('.page.current img')?.naturalWidth > 0")
            assert image.get_attribute("alt"), f"Missing alt: {deck['stem']} #{number}"
            if spec["kind"] == "animation":
                animations.append(number)
                stream = context.request.get(urljoin(url, spec["video"]), headers={"Range": "bytes=0-99"})
                assert stream.status == 206 and len(stream.body()) == 100
                page.touchscreen.tap(590, 410)
                page.wait_for_function("document.querySelector('.page.current video')?.currentTime > 0.3")
                assert page.locator(".page.current video").evaluate("v => !v.paused && v.playsInline")
                assert not page.evaluate("Boolean(document.fullscreenElement)")
        page.wait_for_function("window.cacheResult !== null", timeout=180000)
        assert page.evaluate("window.cacheResult.failed") == 0
        page.keyboard.press("Home")
        context.set_offline(True)
        page.reload()
        ready(page, count)
        assert page.evaluate("getComputedStyle(document.querySelector('.frame')).position") == "relative"
        # Check every SVG offline as well as one animation in each deck.
        for number in range(1, count + 1):
            page.evaluate("n => location.hash = '#' + n", number)
            page.wait_for_function("n => document.querySelector('.where b')?.textContent === String(n)", arg=number)
            page.wait_for_function("document.querySelector('.page.current img')?.naturalWidth > 0")
        if animations:
            page.evaluate("n => location.hash = '#' + n", animations[0])
            page.wait_for_function("document.querySelector('.page.current video') !== null")
            page.touchscreen.tap(590, 410)
            page.wait_for_function("document.querySelector('.page.current video')?.currentTime > 0.3")
        # Exercise the actual web-manifest icon graph offline, including the
        # installation icon that desktop page rendering does not request.
        assert page.evaluate("""async () => {
          const base = new URL('../', location.href);
          const manifest = await (await fetch(new URL('manifest.webmanifest', base))).json();
          for (const icon of manifest.icons) {
            const response = await fetch(new URL(icon.src, base));
            if (!response.ok || (await response.blob()).size === 0) return false;
          }
          return true;
        }"""), 'PWA icons must remain available offline'
        if artifacts:
            artifacts.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(artifacts / (deck["stem"] + "-offline.png")))
        assert not errors, f"{deck['stem']}: {errors}"
        print(f"PASS {deck['stem']}: {count} PDF/SVG pages, touch, keys, {len(animations)} animations, offline", flush=True)
        context.close()


def main():
    import os
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", nargs="?", default="public")
    parser.add_argument("--artifacts", type=Path)
    parser.add_argument("--chrome", default=os.environ.get("CHROMIUM_EXECUTABLE_PATH", "/usr/bin/google-chrome-stable"))
    args = parser.parse_args()
    server = None
    if args.site.startswith(("http://", "https://")):
        base = args.site.rstrip("/") + "/"
    else:
        handler = runpy.run_path(str(Path(__file__).with_name("serve-site.py")))["SiteHandler"]
        class QuietHandler(handler):
            def log_message(self, *_):
                pass
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(Path(args.site).resolve())))
        Thread(target=server.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{server.server_port}/present/"
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=args.chrome, headless=True, args=["--no-sandbox"])
            check(browser, base, args.artifacts)
            browser.close()
    finally:
        if server:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    main()
