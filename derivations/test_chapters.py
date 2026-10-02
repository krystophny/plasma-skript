"""Run every chapter script top to bottom; a failed `agrees`/`close_to` fails the test.

The chapter scripts reference the Typst script only by section label
(`section(..., script="<label>")`) and equation label (`eq="<label>"`), never
by line number; the tests below keep it that way.
"""

import json
import re
import runpy
from pathlib import Path

import pytest

import notebook

CHAPTERS = sorted((Path(__file__).parent / "chapters").glob("ch*.py"))
LINE_REFERENCE = re.compile(r'\.typ:\d|"\d*:\d+(?:-\d+)?"')


@pytest.mark.parametrize("path", CHAPTERS, ids=[p.stem for p in CHAPTERS])
def test_chapter(path):
    notebook.reset(echo=False)
    namespace = runpy.run_path(str(path), run_name="chapter")
    for name, fn in namespace.items():
        if name.startswith("test_") and callable(fn):
            fn()


@pytest.mark.parametrize("path", CHAPTERS, ids=[p.stem for p in CHAPTERS])
def test_no_line_references(path):
    hits = [f"{path.name}:{i}: {line.strip()}"
            for i, line in enumerate(path.read_text().splitlines(), 1)
            if LINE_REFERENCE.search(line)]
    assert not hits, "line-number references to the script:\n" + "\n".join(hits)


def _used(keyword):
    pattern = re.compile(rf'\b{keyword}="([^"]+)"')
    return {label for p in CHAPTERS for label in pattern.findall(p.read_text())}


def test_section_labels_exist():
    outline = json.loads(notebook.ensure_outline().read_text())
    known = {e["label"] for e in outline["chapters"] + outline["sections"]}
    assert _used("script") <= known, sorted(_used("script") - known)


@pytest.mark.skipif(not notebook.SRC.is_dir(), reason="no script sources (exported copy)")
def test_equation_labels_exist():
    defined = set()
    for path in notebook.SRC.rglob("*.typ"):
        defined.update(re.findall(r"<([A-Za-z0-9:_.-]+)>", path.read_text()))
    used = _used("eq")
    assert used, "no equation labels used"
    assert used <= defined, sorted(used - defined)
