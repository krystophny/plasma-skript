"""Notebook-style helpers for the derivation scripts.

A chapter script is plain Python split into `# %%` cells (VS Code, PyCharm and
Spyder run them one by one). Every displayed line is a SymPy object that the
script actually computes with, so the printed derivation cannot drift from
the code:

    section("Debye length", script="intro-debye-shielding")
    poisson = show(sp.Eq(laplacian, -rho / eps0))      # equation to solve
    ...
    agrees(lambda_D, printed, eq="debye-screened-equation")  # compare with the script

Running a script prints every step in the terminal; `make tex` / `make pdf`
collects the same steps into build/tex/<chapter>.tex and build/pdf/.

References to the script are broad and stable, never line numbers: a section
names the Typst label of a script section or chapter (`script=`), shown as
"§2.1 Debye shielding" from the outline that scripts/script-outline.sh
queries from the script; a check may name the Typst label of a displayed
equation (`eq=`). Both are verified against src/ when the script runs.
"""

import json
import re
import subprocess
from pathlib import Path

import sympy as sp
from sympy.physics import units as u
from sympy.physics.units import convert_to

BUILD = Path(__file__).resolve().parent / "build"  # derivations/build
REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "src"
# In the repository the outline is generated from src/; a standalone copy of
# derivations/ (scripts/export-course-folder.sh) ships it next to this file.
OUTLINE = (REPO / "slides" / "build" / "script-outline.json" if SRC.is_dir()
           else Path(__file__).resolve().parent / "script-outline.json")
_SECTIONS = []  # [title, reference, [(kind, payload), ...]]
_ECHO = True  # print steps while running


def _display(obj):
    """Display form: recombine sqrt(a) sqrt(b) / sqrt(c) into one root."""
    if isinstance(obj, sp.Equality):
        return sp.Eq(_display(obj.lhs), _display(obj.rhs), evaluate=False)
    if isinstance(obj, sp.Mul):
        powers = obj.as_powers_dict()
        half = {b: x for b, x in powers.items() if getattr(x, "q", 1) == 2}
        if len(half) > 1:
            inner = sp.Mul(*[b ** (2 * x) for b, x in half.items()])
            rest = sp.Mul(*[b**x for b, x in powers.items() if b not in half])
            root = sp.Pow(inner, sp.S.Half, evaluate=False)
            return root if rest == 1 else sp.Mul(rest, root, evaluate=False)
    return obj


def _join(pieces):
    """Join note pieces with spaces, but none before punctuation."""
    out = ""
    for piece in pieces:
        glue = "" if not out or piece[:1] in ",.;:)" else " "
        out += glue + piece
    return out


def _latex(obj):
    """LaTeX with scientific notation for very large or small floats."""
    return sp.latex(obj, min=-3, max=4)


def _inline(obj):
    """One-line terminal form of a SymPy object (for use inside a sentence)."""
    if isinstance(obj, sp.Equality):
        return f"{_inline(obj.lhs)} = {_inline(obj.rhs)}"
    pretty = sp.pretty(_display(obj), use_unicode=True)
    return pretty if "\n" not in pretty else sp.sstr(obj)


def _rounded(number, digits):
    """Display copy rounded to `digits` significant digits (94.1 stays 94.1)."""
    return sp.Float(f"{number:.{digits}g}", digits + 1)


def ensure_outline():
    """Regenerate the script outline if it is missing or older than src/."""
    if not SRC.is_dir():
        if not OUTLINE.exists():
            raise FileNotFoundError(f"no script sources and no {OUTLINE}")
        return OUTLINE
    newest = max(p.stat().st_mtime for p in SRC.rglob("*.typ"))
    if not OUTLINE.exists() or OUTLINE.stat().st_mtime < newest:
        subprocess.run(["bash", str(REPO / "scripts" / "script-outline.sh"), str(OUTLINE)],
                       check=True)
    return OUTLINE


_REFS = {}


def script_reference(label):
    """'§N.M Title' for a script section label, or the chapter title for a chapter label."""
    if not _REFS:
        outline = json.loads(ensure_outline().read_text())
        chapters = {c["label"]: c for c in outline["chapters"]}
        for c in chapters.values():
            _REFS[c["label"]] = (f"Chapter {c['number']} {c['title']}" if c["number"] is not None
                                 else c["title"])
        for s in outline["sections"]:
            parent = chapters.get(s.get("chapter"), {}).get("title", "")
            _REFS[s["label"]] = (f"§{s['number']} {s['title']}" if s["number"] is not None
                                 else f"{parent}, {s['title']}".lstrip(", "))
    if label not in _REFS:
        raise KeyError(f"no script section or chapter <{label}> in {OUTLINE}")
    return _REFS[label]


_EQ_LABELS = set()


def equation_labels():
    """Labels attached to displayed equations in src/ (`$ ... $ <label>`)."""
    if not _EQ_LABELS:
        for path in SRC.rglob("*.typ"):
            _EQ_LABELS.update(re.findall(r"\$\s*<([A-Za-z0-9:_.-]+)>", path.read_text()))
    return _EQ_LABELS


def _eq_tag(eq):
    if not eq:
        return ""
    if SRC.is_dir() and eq not in equation_labels():
        raise KeyError(f"no labelled equation <{eq}> in src/")
    return f"eq. <{eq}>"


def section(title, script=""):
    """Start a new derivation; script is the Typst label of the script section."""
    reference = script_reference(script) if script else ""
    _SECTIONS.append([title, reference, []])
    if _ECHO:
        print(f"\n== {title}" + (f"  [{reference}]" if reference else ""))


def _record(kind, payload, text):
    if not _SECTIONS:
        section("Derivation")
    _SECTIONS[-1][2].append((kind, payload))
    if _ECHO:
        print(text)


def note(*parts):
    """A short line of words; SymPy objects among the parts are typeset inline.

    note("Linearize for", sp.Lt(e * phi, k_B * T_e))
    """
    tex = _join([f"${_latex(_display(p))}$" if isinstance(p, sp.Basic) else _esc(p)
                  for p in parts])
    text = _join([_inline(p) if isinstance(p, sp.Basic) else p for p in parts])
    _record("note", tex, f"   {text}")


def show(obj, label=""):
    """Display a SymPy object (expression, Eq, Matrix) and return it unchanged."""
    d = _display(obj)
    _record("math", (_latex(d), label),
            sp.pretty(d, use_unicode=True) + (f"    [{label}]" if label else ""))
    return obj


def agrees(derived, printed, *, lhs=None, eq="", source=""):
    """Assert derived == printed formula of the script; display `lhs = printed`.

    eq: Typst label of the printed equation; source: another named, stable
    reference such as a figure. Never a line number.
    """
    diff = sp.simplify(sp.expand(sp.sympify(derived) - sp.sympify(printed)))
    assert diff == 0, f"derived {derived} != printed {printed}"
    tag = " ".join(t for t in ("script", _eq_tag(eq), source) if t)
    d = _display(sp.sympify(printed))
    if lhs is not None:
        d = sp.Eq(lhs, d, evaluate=False)
    _record("check", (_latex(d), "matches " + tag),
            sp.pretty(d, use_unicode=True) + f"    [matches {tag} ✓]")
    return printed


# CODATA values for the constant symbols used in the chapter scripts.
# SymPy has no proton mass; CODATA 2018: m_p = 1.67262192369e-27 kg.
PROTON_MASS = sp.Float("1.67262192369e-27") * u.kilogram
CONSTANTS = {
    "e": u.elementary_charge, "epsilon_0": u.electric_constant,
    "mu_0": u.magnetic_constant, "k_B": u.boltzmann_constant,
    "m_e": u.electron_rest_mass, "m_p": PROTON_MASS, "c": u.speed_of_light,
}


def evaluate(symbol, expr, inputs, unit, digits=3):
    """Evaluate expr for inputs {symbol: quantity with units}; show and return.

    Constants (e, epsilon_0, k_B, m_e, ...) are filled in from CODATA. Shows
    `symbol = number unit` and returns the float in `unit`.
    """
    subs = {s: CONSTANTS[s.name] for s in expr.free_symbols if s.name in CONSTANTS}
    subs.update(inputs)
    if unit == 1:
        number = complex(sp.N(expr.subs(subs)))
        number = number.real if number.imag == 0 else number
        shown = sp.Eq(symbol, _rounded(number, digits) if isinstance(number, float)
                      else sp.N(number, digits), evaluate=False)
    else:
        base = [u.kilogram, u.meter, u.second, u.ampere, u.kelvin]
        q = convert_to(sp.expand(convert_to(expr.subs(subs), base)), unit)
        number = float(sp.simplify(q / unit))
        shown = sp.Eq(symbol, sp.Mul(_rounded(number, digits), unit, evaluate=False),
                      evaluate=False)
    _record("math", (_latex(shown), ""), sp.pretty(shown, use_unicode=True))
    return number


def close_to(number, printed, rtol=5e-3, *, eq="", source=""):
    """Assert a computed (real or complex) number matches the printed one."""
    assert abs(number - printed) <= rtol * abs(printed), f"{number} vs printed {printed}"
    shown = _rounded(printed, 3) if isinstance(printed, (int, float)) else sp.N(printed, 3)
    tag = " ".join(t for t in (_eq_tag(eq), source) if t)
    _record("check", (_latex(shown), f"matches script {tag}".strip()),
            f"   matches printed {printed}" + (f"  [{tag}]" if tag else "") + " \u2713")


def _esc(text):
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("$", r"\$"), ("^", r"\^{}"),
                 ("<", r"\textless{}"), (">", r"\textgreater{}"), ("§", r"\S{}")]:
        text = text.replace(a, b)
    return text


def report(path, title=None):
    """Write all recorded sections as a standalone LaTeX document."""
    name = Path(path).stem
    title = title or name
    out = [r"\documentclass[11pt]{article}",
           r"\usepackage[a4paper,margin=2cm]{geometry}",
           r"\usepackage{amsmath,amssymb,xcolor}",
           r"\allowdisplaybreaks", r"\setlength{\parindent}{0pt}",
           rf"\title{{{_esc(title)}}}", r"\date{}", r"\begin{document}", r"\maketitle"]
    for title, reference, items in _SECTIONS:
        out.append(rf"\section*{{{_esc(title)}}}")
        if reference:
            out.append(rf"{{\small\color{{gray}}Script: {_esc(reference)}}}\par")
        for kind, payload in items:
            if kind == "note":
                out.append(rf"\medskip {payload}\par")
            else:
                tex, label = payload
                tag = r"\quad\checkmark" if kind == "check" else ""
                lab = rf"\tag*{{\small {_esc(label)}}}" if label else ""
                out.append(rf"\begin{{equation*}} {tex}{tag} {lab}\end{{equation*}}")
    out.append(r"\end{document}")
    target = BUILD / "tex" / f"{name}.tex"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(out) + "\n")


def reset(echo=True):
    """Clear recorded sections (used by the test runner)."""
    global _ECHO
    _SECTIONS.clear()
    _ECHO = echo


__all__ = ["section", "note", "show", "agrees", "evaluate", "close_to", "report",
           "reset", "u", "sp"]
