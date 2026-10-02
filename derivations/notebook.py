"""Notebook-style helpers for the derivation scripts.

A chapter script is plain Python split into `# %%` cells (VS Code, PyCharm and
Spyder run them one by one). Every displayed line is a SymPy object that the
script actually computes with, so the printed derivation cannot drift from
the code:

    section("Debye length", "02-debye-shielding.typ:124")
    poisson = show(sp.Eq(laplacian, -rho / eps0))      # equation to solve
    ...
    agrees(lambda_D, printed)                          # compare with the script

Running a script prints every step in the terminal; `make tex` / `make pdf`
collects the same steps into build/tex/<chapter>.tex and build/pdf/.
"""

from pathlib import Path

import sympy as sp
from sympy.physics import units as u
from sympy.physics.units import convert_to

BUILD = Path(__file__).resolve().parent / "build"  # derivations/build
_SECTIONS = []  # [title, source, [(kind, payload), ...]]
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


def section(title, source=""):
    """Start a new derivation; source is 'file.typ:line' in src/chapters."""
    _SECTIONS.append([title, source, []])
    if _ECHO:
        print(f"\n== {title}" + (f"  [{source}]" if source else ""))


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


def agrees(derived, printed, source="", lhs=None):
    """Assert derived == printed formula of the script; display `lhs = printed`."""
    diff = sp.simplify(sp.expand(sp.sympify(derived) - sp.sympify(printed)))
    assert diff == 0, f"derived {derived} != printed {printed}"
    tag = "script" + (f" {source}" if source else "")
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


def close_to(number, printed, rtol=5e-3, source=""):
    """Assert a computed (real or complex) number matches the printed one."""
    assert abs(number - printed) <= rtol * abs(printed), f"{number} vs printed {printed}"
    shown = _rounded(printed, 3) if isinstance(printed, (int, float)) else sp.N(printed, 3)
    _record("check", (_latex(shown), f"matches script {source}".strip()),
            f"   matches printed {printed}  [{source}] \u2713")


def _esc(text):
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("$", r"\$"), ("^", r"\^{}")]:
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
    for title, source, items in _SECTIONS:
        out.append(rf"\section*{{{_esc(title)}}}")
        if source:
            out.append(rf"{{\small\color{{gray}}\texttt{{{_esc(source)}}}}}\par")
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
