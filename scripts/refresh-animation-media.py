#!/usr/bin/env python3
"""Adopt rendered animation revisions and their posters into the shared register."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def refresh(media_dir, site_url):
    path = ROOT / 'media/animations.json'
    register = json.loads(path.read_text())
    register['preferred_host'] = 'native-nextcloud'
    for slug, record in register['animations'].items():
        video = media_dir / (slug + '.mp4')
        poster = media_dir / (slug + '.png')
        if not video.is_file() or not poster.is_file():
            raise ValueError('Missing rendered animation/poster: ' + slug)
        with video.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        record['player_url'] = site_url.rstrip('/') + '/animations/' + slug + '.html'
        record['stream_url'] = record['fallback_url'].split('?')[0] + '?v=' + digest[:16]
        record['mp4_sha256'] = digest
        record['appearance'] = 'dark'
    for slug in register['animations']:
        shutil.copyfile(media_dir / (slug + '.png'), ROOT / 'media/posters' / (slug + '.png'))
    path.write_text(json.dumps(register, indent=2, ensure_ascii=False) + '\n')
    print('Adopted', len(register['animations']), 'dark Nextcloud animation revisions.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--media-dir', type=Path, default=ROOT / '.cache/animations')
    parser.add_argument('--site-url', default='https://krystophny.github.io/plasma-skript')
    args = parser.parse_args()
    refresh(args.media_dir, args.site_url)
