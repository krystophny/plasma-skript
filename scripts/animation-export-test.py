#!/usr/bin/env python3
"""A fresh publisher must beat stale local renders; corrupt streams must fail."""
import base64
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from threading import Thread
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ExportRevisionTest(unittest.TestCase):
    def test_registered_revision_and_corruption(self):
        publisher = {"body": b"independent registered video payload", "requests": 0}

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                publisher["requests"] += 1
                self.send_response(200)
                self.send_header("Content-Length", str(len(publisher["body"])))
                self.end_headers()
                self.wfile.write(publisher["body"])

            def log_message(self, *_):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        Thread(target=server.serve_forever, daemon=True).start()
        try:
            with tempfile.TemporaryDirectory() as directory:
                fixture = Path(directory)
                for name in ("scripts", "media/posters", ".cache/animations", "public/media", "export"):
                    (fixture / name).mkdir(parents=True, exist_ok=True)
                for name in ("build-present.py", "export-animation-media.py"):
                    shutil.copyfile(ROOT / "scripts" / name, fixture / "scripts" / name)
                (fixture / ".cache/animations/example.mp4").write_bytes(b"obsolete local render")
                (fixture / "public/media/example.mp4").write_bytes(b"another obsolete render")
                expected = publisher["body"]
                digest = hashlib.sha256(expected).hexdigest()
                poster = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a3ioAAAAASUVORK5CYII=")
                (fixture / "media/posters/example.png").write_bytes(poster)
                registry = {"animations": {"example": {
                    "stream_url": f"http://127.0.0.1:{server.server_port}/example_export.mp4?v={digest[:8]}",
                    "mp4_sha256": digest, "poster": "media/posters/example.png",
                }}}
                (fixture / "media/animations.json").write_text(json.dumps(registry))
                command = [sys.executable, str(fixture / "scripts/export-animation-media.py"),
                           str(fixture / "public"), str(fixture / "export")]
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((fixture / "export/example_export.mp4").read_bytes(), expected)
                self.assertEqual((fixture / "export/example_export.png").read_bytes(), poster)
                self.assertEqual(publisher["requests"], 1)

                # Rebuilding an existing presenter must reuse its verified
                # stream even when source and destination are the same file.
                present_media = fixture / "public/present/media"
                present_media.mkdir(parents=True)
                (present_media / "example_export.mp4").write_bytes(expected)
                rebuild = command[:-1] + [str(present_media)]
                result = subprocess.run(rebuild, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((present_media / "example_export.mp4").read_bytes(), expected)
                self.assertEqual(publisher["requests"], 1)

                # Remove the good revision and serve bytes that disagree with
                # the independent registry. Nothing corrupt may be exported.
                (fixture / "export/example_export.mp4").unlink()
                (present_media / "example_export.mp4").unlink()
                (fixture / ".cache/present-media" / (digest + ".mp4")).unlink()
                publisher["body"] = b"corrupt replacement"
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Checksum mismatch", result.stderr)
                self.assertFalse((fixture / "export/example_export.mp4").exists())
                self.assertFalse(list((fixture / ".cache/present-media").glob("*.part")))
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
