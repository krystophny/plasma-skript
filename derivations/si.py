"""Shared SI symbols and checks for the SymPy derivations.

Every derivation file in this folder starts from governing equations, derives
the result with SymPy, and compares it with the formula as printed in the
script (`stated`). `check` asserts that both agree symbolically and that the
result carries the expected SI unit.
"""

import sympy as sp
from sympy.physics import units as u
from sympy.physics.units import convert_to

# Physical constants as positive symbols.
e, m_e, m_i, eps0, mu0, k_B, c = sp.symbols(
    "e m_e m_i epsilon_0 mu_0 k_B c", positive=True
)

# SI unit of each symbol. Derivation files extend this with UNITS.update(...).
UNITS = {
    e: u.coulomb,
    m_e: u.kilogram,
    m_i: u.kilogram,
    eps0: u.farad / u.meter,
    mu0: u.henry / u.meter,
    k_B: u.joule / u.kelvin,
    c: u.meter / u.second,
}

_BASE = [u.kilogram, u.meter, u.second, u.ampere, u.kelvin]


def si_unit(expr, units=None):
    """Return expr with every symbol replaced by its SI unit, in base units."""
    table = UNITS if units is None else {**UNITS, **units}
    missing = expr.free_symbols - set(table)
    if missing:
        raise KeyError(f"no SI unit declared for {sorted(map(str, missing))}")
    q = expr.subs({s: table[s] for s in expr.free_symbols})
    return sp.simplify(convert_to(q, _BASE))


def same_unit(a, b):
    """True if two unit expressions agree up to a pure number."""
    ratio = sp.simplify(convert_to(a / b, _BASE))
    return not (ratio.free_symbols or ratio.atoms(u.Quantity))


def check(derived, stated, unit=None, units=None):
    """Assert derived == stated symbolically and, if given, that stated has `unit`."""
    diff = sp.simplify(sp.expand(derived - stated))
    assert diff == 0, f"derived {derived} != stated {stated}"
    if unit is not None:
        got = si_unit(stated, units)
        assert same_unit(got, unit), f"unit of {stated} is {got}, expected {unit}"


# --- LaTeX report -----------------------------------------------------------
# Each test records its steps in a Derivation. Running a chapter file as a
# script (see the Makefile) writes all recorded steps to build/tex/<file>.tex,
# which latexmk turns into build/pdf/<file>.pdf.

_RECORDED = []


def _tex(expr):
    """LaTeX for display; recombine sqrt(a) sqrt(b) into sqrt(a b)."""
    if isinstance(expr, sp.Equality):
        return f"{_tex(expr.lhs)} = {_tex(expr.rhs)}"
    if isinstance(expr, sp.Mul):
        powers = expr.as_powers_dict()
        half = {b: x for b, x in powers.items() if getattr(x, "q", 1) == 2}
        if len(half) > 1:
            inner = sp.Mul(*[b ** (2 * x) for b, x in half.items()])
            rest = sp.Mul(*[b**x for b, x in powers.items() if b not in half])
            num, den = sp.fraction(rest)
            top = (r"\sqrt{%s}" % sp.latex(inner)) if num == 1 else (
                r"%s \sqrt{%s}" % (sp.latex(num), sp.latex(inner)))
            return top if den == 1 else r"\frac{%s}{%s}" % (top, sp.latex(den))
    return sp.latex(expr)


class Derivation:
    """Ordered list of (label, formula) steps, rendered as one LaTeX section."""

    def __init__(self, title, source=""):
        self.title, self.source, self.steps = title, source, []
        _RECORDED.append(self)

    def step(self, label, expr):
        """Record expr (a SymPy expression or sp.Eq) and return it unchanged."""
        self.steps.append((label, _tex(expr)))
        return expr

    def eq(self, label, lhs, rhs):
        """Record lhs = rhs and return rhs."""
        self.steps.append((label, f"{_tex(lhs)} = {_tex(rhs)}"))
        return rhs


def _tex_escape(text):
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("$", r"\$")]:
        text = text.replace(a, b)
    return text


def write_report(title, path):
    """Write every Derivation recorded so far as a standalone LaTeX document."""
    lines = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[a4paper,margin=2cm]{geometry}",
        r"\usepackage{amsmath,amssymb}",
        r"\allowdisplaybreaks",
        rf"\title{{{_tex_escape(title)}}}",
        r"\date{}",
        r"\begin{document}",
        r"\maketitle",
    ]
    for d in _RECORDED:
        lines.append(rf"\section*{{{_tex_escape(d.title)}}}")
        if d.source:
            lines.append(rf"\noindent{{\small\texttt{{{_tex_escape(d.source)}}}}}")
        lines.append(r"\begin{align*}")
        body = [rf"&{tex} && \text{{{_tex_escape(label)}}}" for label, tex in d.steps]
        lines.append(" \\\\\n".join(body))
        lines.append(r"\end{align*}")
    lines.append(r"\end{document}")
    from pathlib import Path

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n")


def run_as_script(module_globals):
    """Run all test_* functions of a chapter file and write its LaTeX report."""
    from pathlib import Path

    name = Path(module_globals["__file__"]).stem
    for key, fn in list(module_globals.items()):
        if key.startswith("test_") and callable(fn):
            fn()
            print("ok", key)
    for key, fn in list(module_globals.items()):
        if key.startswith("plot_") and callable(fn):
            fn()
            print("plot", key)
    doc = (module_globals.get("__doc__") or name).strip().splitlines()[0]
    write_report(doc, Path("build/tex") / f"{name}.tex")


# --- Plots -----------------------------------------------------------------
# Plots of derived results live next to their derivation. A chapter file
# defines plot_<name>() functions that lambdify the derived expressions and
# call save(fig, "<name>"); run_as_script writes build/fig/<name>.svg (script
# website) and build/fig/<name>.pdf (slides).

BLUE, ORANGE, GRAY = "#0072B2", "#D55E00", "#555555"


def figure(width=4.2, height=2.8):
    """Minimal figure: no top/right spines, thin lines, mathtext labels."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "font.size": 10, "axes.linewidth": 0.8, "lines.linewidth": 1.6,
        "axes.spines.top": False, "axes.spines.right": False,
        "xtick.direction": "out", "ytick.direction": "out",
        "legend.frameon": False, "svg.fonttype": "none",
        "mathtext.fontset": "cm", "figure.dpi": 150,
    })
    fig, ax = plt.subplots(figsize=(width, height), layout="constrained")
    return fig, ax


def save(fig, name):
    """Write build/fig/<name>.svg and .pdf and close the figure."""
    from pathlib import Path

    import matplotlib.pyplot as plt

    out = Path("build/fig")
    out.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "pdf"):
        fig.savefig(out / f"{name}.{ext}", transparent=False, facecolor="white")
    plt.close(fig)
