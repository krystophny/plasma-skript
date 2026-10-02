"""Run every chapter script top to bottom; a failed `agrees`/`close_to` fails the test."""

import runpy
from pathlib import Path

import pytest

import notebook

CHAPTERS = sorted((Path(__file__).parent / "chapters").glob("ch*.py"))


@pytest.mark.parametrize("path", CHAPTERS, ids=[p.stem for p in CHAPTERS])
def test_chapter(path):
    notebook.reset(echo=False)
    namespace = runpy.run_path(str(path), run_name="chapter")
    for name, fn in namespace.items():
        if name.startswith("test_") and callable(fn):
            fn()
