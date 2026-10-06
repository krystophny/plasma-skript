#!/usr/bin/env python3
"""Build stable native animation pages and theme-aware SVG appearances."""
import base64
from collections import Counter
import html
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
# Change only paint; paths, scales, line dashes, labels and marker shapes remain
# byte-for-byte unchanged. Dark hues come from Okabe-Ito's brighter members.
PALETTE = {
    '#000000': '#e4e6e9', '#17202a': '#e4e6e9', '#1c1f23': '#e4e6e9',
    '#333333': '#bac2cc', '#404040': '#bac2cc', '#484848': '#bac2cc',
    '#4a5058': '#bac2cc', '#555555': '#bac2cc', '#666666': '#a6afbb',
    '#8c8c8c': '#8f9aa8', '#999999': '#8f9aa8', '#cccccc': '#536175',
    '#d9d9d9': '#536175', '#e6e6e6': '#2a2f36', '#e8e8e8': '#2a2f36',
    '#ebebeb': '#2a2f36', '#eeeeee': '#2a2f36', '#f2f2f2': '#181c21',
    '#ffffff': '#111418', '#f7f9fc': '#181c21', '#d8f0f0': '#23383c',
    '#0072b2': '#56b4e9', '#006197': '#56b4e9', '#356aa0': '#56b4e9',
    '#d55e00': '#e69f00', '#b55000': '#e69f00', '#b86418': '#e69f00',
    '#126e82': '#6cc4c9', '#526175': '#bac2cc',
}


def dark_svg(svg):
    # Match hex colors, never SVG IDs or URL references.
    def color(match):
        original = match.group(0).lower()
        return PALETTE.get(original, original)
    return re.sub(r'#[0-9a-fA-F]{6}\b', color, svg)


def theme_graphics(content):
    counts = Counter()
    def embedded(match):
        tag, encoded = match.group(0), match.group(1)
        svg = base64.b64decode(encoded).decode()
        dark = base64.b64encode(dark_svg(svg).encode()).decode()
        counts['images'] += 1
        return '<picture class="themed-plot"><source media="(prefers-color-scheme: dark)" srcset="data:image/svg+xml;base64,' + dark + '">' + tag + '</picture>'
    content = re.sub(r'<img\b[^>]*src="data:image/svg\+xml;base64,([A-Za-z0-9+/=]+)"[^>]*>', embedded, content)
    def inline(match):
        svg = match.group(0)
        colors = set(re.findall(r'#[0-9a-fA-F]{6}\b', svg))
        rules = []
        for color in sorted(colors):
            dark = PALETTE.get(color.lower())
            if dark:
                for paint in ('fill', 'stroke'):
                    rules.append(f'[{paint}="{color}"] {{{paint}: {dark};}}')
        style = '<style>@media (prefers-color-scheme: dark) {svg {color: #e4e6e9;} ' + ' '.join(rules) + '}</style>'
        counts['inline'] += 1
        return svg.replace('>', '>' + style, 1)
    return re.sub(r'<svg\b.*?</svg>', inline, content, flags=re.S), counts


def player_markup(figure):
    start = figure.index('<div class="animation-player">')
    depth = 0
    for tag in re.finditer(r'</?div\b[^>]*>', figure[start:]):
        depth += -1 if tag.group(0).startswith('</') else 1
        if depth == 0:
            return figure[start:start + tag.end()]
    raise ValueError('Unclosed animation player')


def prepare(site):
    records = json.loads((site / 'media/animations.json').read_text())['animations']
    players = site / 'animations'
    players.mkdir(exist_ok=True)
    for name in ('animation-player.js', 'animation-player.css'):
        shutil.copyfile(ROOT / 'src' / name, site / name)
    by_source = {urlsplit(r['stream_url']).path: slug for slug, r in records.items()}
    found, counts = {}, Counter()
    for page in sorted(site.rglob('*.html')):
        if page.parent == players:
            continue
        content, changed = theme_graphics(page.read_text())
        counts.update(changed)
        for figure in re.findall(r'<figure\b[^>]*class="animation-figure"[^>]*>.*?</figure>', content, re.S):
            source = re.search(r'<video\b[^>]*src="([^"]+)"', figure)
            if source:
                slug = by_source[urlsplit(html.unescape(source.group(1))).path]
                found[slug] = (figure, page.relative_to(site).as_posix())
        prefix = '../' * (len(page.relative_to(site).parts) - 1)
        content = content.replace('</head>', f'<link rel="stylesheet" href="{prefix}animation-player.css">\n</head>', 1)
        content = content.replace('</body>', f'<script defer src="{prefix}animation-player.js"></script>\n</body>', 1)
        page.write_text(content)
    missing = set(records) - set(found)
    for slug in missing:
        record = records[slug]
        if not record.get('supplementary_description') or not record.get('supplementary_chapter'):
            raise ValueError('No captioned script animation or supplementary description for: ' + slug)
        description = html.escape(record['supplementary_description'])
        source = html.escape(record['stream_url'], quote=True)
        figure = f'''<figure class="animation-figure"><div class="animation-player">
<video controls loop muted playsinline preload="metadata" aria-label="{description}" src="{source}" poster="../media/{slug}.png">{description}</video>
<div class="animation-controls" hidden><input type="range" class="animation-seek" min="0" max="100" step="0.1" value="0" aria-label="Animation position"><button type="button" class="animation-fullscreen" aria-label="Full screen"></button></div>
<p class="animation-status" role="status"></p></div>
<figcaption>Supplementary demonstration. {description}</figcaption></figure>'''
        found[slug] = (figure, record['supplementary_chapter'])
    for slug, record in records.items():
        figure, chapter = found[slug]
        # The dedicated page puts all text below the full-window video.
        video = player_markup(figure)
        caption = re.search(r'<figcaption\b[^>]*>.*?</figcaption>', figure, re.S).group(0)
        title = slug.replace('-', ' ').capitalize()
        (players / (slug + '.html')).write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — Plasma Physics animation</title>
<link rel="stylesheet" href="../animation-player.css"></head>
<body class="animation-presentation"><main><figure style="margin:0">
{video}<div class="animation-information"><h1>{html.escape(title)}</h1>{caption}
<p><a href="../{chapter}">Return to the script chapter</a> · Original animation: Christopher Albert, CC BY 4.0.</p></div>
</figure></main><script defer src="../animation-player.js"></script></body></html>''')
    (site / 'media/graphic-theme-audit.json').write_text(json.dumps(dict(counts), indent=2) + '\n')
    print('Native animation pages:', len(found), '; themed SVGs:', dict(counts))


if __name__ == '__main__':
    prepare(Path(sys.argv[1]))
