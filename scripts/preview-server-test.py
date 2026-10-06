#!/usr/bin/env python3
"""Check video byte-range transport against independently chosen bytes."""
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, build_opener, ProxyHandler

Handler = runpy.run_path(str(Path(__file__).with_name('serve-site.py')))['SiteHandler']
Handler.log_message = lambda *args: None
opener = build_opener(ProxyHandler({}))

with TemporaryDirectory() as directory:
    Path(directory, 'video.mp4').write_bytes(b'abcdefghij')
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=directory))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f'http://127.0.0.1:{server.server_port}/video.mp4'
    try:
        for span, expected, header in (
            ('bytes=0-2', b'abc', 'bytes 0-2/10'),
            ('bytes=7-', b'hij', 'bytes 7-9/10'),
            ('bytes=-3', b'hij', 'bytes 7-9/10'),
            ('bytes=8-99', b'ij', 'bytes 8-9/10'),
        ):
            with opener.open(Request(url, headers={'Range': span}), timeout=5) as response:
                assert response.status == 206
                assert response.headers['Content-Range'] == header
                assert response.headers['Accept-Ranges'] == 'bytes'
                assert response.read() == expected
        with opener.open(Request(url, method='HEAD', headers={'Range': 'bytes=0-2'}), timeout=5) as response:
            assert response.status == 206 and response.headers['Content-Length'] == '3'
            assert response.read() == b''
        with opener.open(url, timeout=5) as response:
            assert response.status == 200 and response.read() == b'abcdefghij'
        try:
            opener.open(Request(url, headers={'Range': 'bytes=20-30'}), timeout=5)
            raise AssertionError('Unsatisfiable range accepted')
        except HTTPError as error:
            assert error.code == 416 and error.headers['Content-Range'] == 'bytes */10'
            error.close()
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
print('Preview range transport: full, partial, suffix, clamped, HEAD and 416 passed.')
