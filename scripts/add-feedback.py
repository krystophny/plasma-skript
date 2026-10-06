#!/usr/bin/env python3
"""Add a public, credential-free GitHub feedback link to each HTML page."""
import html
import os
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode, urljoin


class PageTitle(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.parts.append(data)


def add_feedback(site, repo_url, site_url):
    source = Path(__file__).resolve().parent.parent / "src"
    for name in ("feedback.js", "feedback.css"):
        shutil.copyfile(source / name, site / name)
    count = 0
    for page in sorted(site.rglob("*.html")):
        content = page.read_text()
        if 'data-script-feedback="true"' in content:
            continue
        title = PageTitle()
        title.feed(content)
        title = "".join(title.parts).strip() or "Plasma Physics"
        relative = page.relative_to(site).as_posix()
        page_url = urljoin(site_url.rstrip("/") + "/", relative)
        issue_url = repo_url.rstrip("/") + "/issues/new?" + urlencode({
            "title": "Script feedback: " + title,
            "body": "### Location\n" + title + "\n" + page_url
                    + "\n\n### Problem or suggestion\nPlease describe the issue here.\n",
        })
        asset_prefix = os.path.relpath(site, page.parent).replace(os.sep, "/")
        if asset_prefix == ".":
            asset_prefix = ""
        else:
            asset_prefix += "/"
        escape = lambda value: html.escape(value, quote=True)
        stylesheet = f'<link rel="stylesheet" href="{asset_prefix}feedback.css">\n'
        link = (f'<a class="script-feedback" data-script-feedback="true" '
                f'data-repo-url="{escape(repo_url)}" data-page-url="{escape(page_url)}" '
                f'href="{escape(issue_url)}" target="_blank" rel="noopener noreferrer" '
                'title="Open a GitHub issue for this section (GitHub sign-in required)">'
                'Report a problem<span class="feedback-sr-only"> '
                '(opens GitHub in a new tab)</span></a>\n'
                f'<script defer src="{asset_prefix}feedback.js"></script>\n')
        if "</head>" not in content or "</body>" not in content:
            raise ValueError(f"Expected a complete HTML page: {relative}")
        content = content.replace("</head>", stylesheet + "</head>", 1)
        content = content.replace("</body>", link + "</body>", 1)
        page.write_text(content)
        count += 1
    print(f"GitHub feedback added to {count} HTML pages")


if __name__ == "__main__":
    add_feedback(Path(sys.argv[1]), "https://github.com/krystophny/plasma-skript",
                 os.environ.get("PUBLIC_SITE_URL", "https://krystophny.github.io/plasma-skript/"))
