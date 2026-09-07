#!/usr/bin/env python3
"""Build an offline PDF snapshot of the official Lilaq documentation."""

from concurrent.futures import ThreadPoolExecutor
from datetime import date
from html import escape, unescape
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "resources/typst/lilaq-documentation.pdf"
BASE_URL = "https://lilaq.org/"
SITEMAP_URL = urllib.parse.urljoin(BASE_URL, "sitemap.xml")
USER_AGENT = "plasma-physics-script-lilaq-pdf/1.0"


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def documentation_urls() -> list[str]:
    sitemap = fetch(SITEMAP_URL)
    urls = re.findall(r"<loc>(https://lilaq\.org/docs[^<]*)</loc>", sitemap)
    unique_urls = list(dict.fromkeys(urls))

    def sort_key(url: str) -> tuple[int, str]:
        path = urllib.parse.urlsplit(url).path
        if path == "/docs/quickstart":
            return (0, path)
        if path == "/docs/plot-types":
            return (1, path)
        if path == "/docs/category/tutorials":
            return (2, path)
        if path.startswith("/docs/tutorials/"):
            return (3, path)
        if path == "/docs/examples":
            return (4, path)
        if path.startswith("/docs/examples/"):
            return (5, path)
        if path == "/docs/category/reference":
            return (6, path)
        if path.startswith("/docs/category/"):
            return (7, path)
        if path.startswith("/docs/reference/"):
            return (8, path)
        return (9, path)

    return sorted(unique_urls, key=sort_key)


def extract_page(document: str) -> tuple[str, str]:
    article_match = re.search(r"<article\b[^>]*>(.*?)</article>", document, re.S)
    if article_match is not None:
        article = article_match.group(1)
        markdown_start = article.find('<div class="theme-doc-markdown markdown">')
        if markdown_start >= 0:
            content = article[markdown_start:]
        else:
            content = ""
    else:
        content = ""

    if not content:
        index_start = document.find('<div class="generatedIndexPage_')
        main_end = document.find("</main>", index_start)
        if index_start < 0 or main_end < 0:
            raise RuntimeError("Could not find the documentation content")
        content = document[index_start:main_end]

    title_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", content, re.S)
    if title_match is None:
        raise RuntimeError("Could not find the documentation title")

    title = unescape(re.sub(r"<[^>]+>", "", title_match.group(1)))
    title = re.sub(r"\s+", " ", title).strip()
    content = content.replace('loading="lazy"', 'loading="eager"')
    return title, content


def stylesheet_urls(document: str) -> list[str]:
    hrefs = re.findall(
        r'<link\b[^>]*rel="stylesheet"[^>]*href="([^"]+)"', document
    )
    return [urllib.parse.urljoin(BASE_URL, href) for href in hrefs]


def make_book(pages: list[tuple[str, str, str]]) -> str:
    first_stylesheets = stylesheet_urls(pages[0][1])
    links = "\n".join(
        f'    <link rel="stylesheet" href="{escape(url, quote=True)}">'
        for url in first_stylesheets
    )

    contents = []
    sections = []
    for index, (url, document, content) in enumerate(pages, start=1):
        title, content = extract_page(document)
        anchor = f"page-{index:03d}"
        contents.append(
            f'<li><a href="#{anchor}">{escape(title)}</a></li>'
        )
        sections.append(
            f'''<section id="{anchor}" class="offline-page">
  <p class="offline-source"><a href="{escape(url, quote=True)}">Source page</a></p>
  {content}
</section>'''
        )

    generated = date.today().isoformat()
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <base href="{BASE_URL}">
  <title>Lilaq documentation (offline snapshot)</title>
{links}
  <style>
    @page {{ size: A4; margin: 18mm 17mm 20mm; }}
    body {{
      color: #1c1e21;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.55;
    }}
    .offline-cover {{
      min-height: 245mm;
      display: flex;
      flex-direction: column;
      justify-content: center;
      break-after: page;
    }}
    .offline-cover h1 {{ font-size: 36pt; margin-bottom: 0.2em; }}
    .offline-cover h2 {{ font-size: 20pt; font-weight: 400; }}
    .offline-cover p {{ color: #606770; }}
    .offline-toc {{ break-after: page; }}
    .offline-toc ol {{ columns: 2; column-gap: 2.5em; }}
    .offline-toc li {{ break-inside: avoid; margin-bottom: 0.25em; }}
    .offline-page {{ break-before: page; }}
    .offline-source {{
      color: #606770;
      font-size: 8pt;
      margin-bottom: 1.5em;
    }}
    .offline-source a {{ color: inherit; }}
    .theme-doc-markdown {{ max-width: none !important; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; }}
    table, figure, pre, img, svg {{ break-inside: avoid; }}
    img, svg {{ max-width: 100%; }}
    a {{ color: #3578e5; }}
    @media print {{
      .offline-source a {{ text-decoration: none; }}
      h1, h2, h3, h4, h5, h6 {{ break-after: avoid; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="offline-cover">
      <h1>Lilaq documentation</h1>
      <h2>Offline snapshot</h2>
      <p>Rendered from the official Lilaq documentation at<br>
        <a href="https://lilaq.org/docs">https://lilaq.org/docs</a>
      </p>
      <p>Generated {generated}</p>
    </section>
    <nav class="offline-toc" aria-label="Contents">
      <h1>Contents</h1>
      <ol>
        {''.join(contents)}
      </ol>
    </nav>
    {''.join(sections)}
  </main>
</body>
</html>
'''


def find_chrome() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/chromium",
        shutil.which("chromium"),
        shutil.which("google-chrome"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise RuntimeError("Could not find a Chromium or Chrome executable")


def render_pdf(book: str, output: Path) -> None:
    chrome = find_chrome()
    with tempfile.TemporaryDirectory(prefix="lilaq-pdf-", dir="/private/tmp") as tmp:
        temporary = Path(tmp)
        html_path = temporary / "lilaq-documentation.html"
        html_path.write_text(book, encoding="utf-8")
        output.parent.mkdir(parents=True, exist_ok=True)
        command = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            "--disable-sync",
            "--disable-background-networking",
            "--allow-file-access-from-files",
            "--no-pdf-header-footer",
            f"--user-data-dir={temporary / 'profile'}",
            f"--print-to-pdf={output}",
            html_path.as_uri(),
        ]
        process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            process.wait(timeout=60)
        except subprocess.TimeoutExpired:
            if not output.exists() or output.stat().st_size < 1_000:
                process.kill()
                process.wait()
                raise RuntimeError("Chrome did not produce a PDF") from None
            process.kill()
            process.wait()

    if not output.exists() or output.stat().st_size < 1_000:
        raise RuntimeError("The generated PDF is missing or empty")


def main() -> int:
    output = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT
    urls = documentation_urls()
    print(f"Fetching {len(urls)} Lilaq documentation pages")
    with ThreadPoolExecutor(max_workers=8) as executor:
        documents = list(executor.map(fetch, urls))

    pages = []
    for url, document in zip(urls, documents):
        _, content = extract_page(document)
        pages.append((url, document, content))

    print("Assembling printable offline document")
    render_pdf(make_book(pages), output)
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
