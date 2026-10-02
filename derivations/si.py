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

# SI unit of the constant symbols; chapter files pass their own units= tables.
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


# --- Plots -----------------------------------------------------------------
# Plots of derived results live next to their derivation. A chapter file
# defines plot_<name>() functions that lambdify the derived expressions and
# call save(fig, "<name>"), which writes build/fig/<name>.svg (script
# website) and build/fig/<name>.pdf (slides).
#
# One figure, one source: the script includes the SVG with
# `derived-plot("<name>", width: ...)` from src/figures.typ (a light card in
# dark mode), the lecture slides include the PDF unchanged. Text is drawn as
# paths in Computer Modern, so the SVG looks the same in every browser. The
# relative text size follows from the figure size: a 10 pt label on a
# 3.4 in wide figure stays readable when a slide scales it up to ~16 cm.
# Plot in SI units (or say so in the axis label when normalized), encode each
# curve by color *and* dash or marker, and label curves directly.

BLUE, ORANGE, GRAY = "#0072B2", "#D55E00", "#555555"

# CODATA 2018 SI values for numerical evaluation (lambdify) of the symbols above.
SI_VALUES = {
    e: 1.602176634e-19,
    m_e: 9.1093837015e-31,
    eps0: 8.8541878128e-12,
    mu0: 1.25663706212e-6,
    k_B: 1.380649e-23,
    c: 299792458.0,
}

# Typical (n_e [m^-3], k_B T_e [eV]) of five example plasmas, one point each,
# shared by the n-T map (ch02) and the plasma-frequency plot (ch03). Sources:
# lecture-1 plan, lv/plasma/tex/slides/01_basics.md, "Parameter sources".
# Order-of-magnitude (n_e [m^-3], k_B T_e [eV]); checked 2026-10-02 against
# NRL Plasma Formulary (2019), "Approximate magnitudes in some typical plasmas"
# (corona, gaseous nebula); Kelley (2009) and Schunk & Nagy (1978) (F-region
# peak); Goebel & Katz (2008) ch. 7 (SPT-100 channel); ITER Q=10 reference
# (<n_e> = 1.01e20 m^-3, <T_e> = 8.8 keV). Sources: lv/plasma/tex/slides/01_basics.md.
EXAMPLE_PLASMAS = {
    "ionosphere": (1e12, 1e-1),
    "H II region": (1e9, 1.0),
    "solar corona": (1e15, 1e2),
    "Hall thruster": (1e18, 2e1),
    "tokamak core": (1e20, 1e4),
}


# Figure text is 10 pt at the natural figure size. The script includes the
# plots at that size (labels a step below its 11 pt body); the slides scale
# them by SLIDE_SCALE = 18 pt / 10 pt, so the labels equal the 18 pt slide
# body. The slide grid (slides/theme.typ) has 15 mm columns and a 7 mm gutter;
# slide_width(n) is the natural width in inches of a plot spanning n columns.
SLIDE_SCALE = 1.8


def slide_width(columns):
    """Natural figure width [in] that fills `columns` slide-grid columns."""
    return (15 * columns + 7 * (columns - 1)) / SLIDE_SCALE / 25.4


def _register_fonts():
    """Register the repository's Libertinus fonts (SIL OFL, fonts/) with
    Matplotlib so that plots use the script's typeface without a system
    install. Without the directory (e.g. an exported copy), Matplotlib falls
    back to an installed Libertinus Serif or its default serif."""
    from pathlib import Path

    from matplotlib import font_manager

    fonts = Path(__file__).resolve().parent.parent / "fonts"
    for path in sorted(fonts.glob("LibertinusSerif-*.otf")):
        font_manager.fontManager.addfont(str(path))


def figure(width=4.2, height=2.8):
    """Minimal figure: no top/right spines, thin lines, mathtext labels."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _register_fonts()
    plt.rcParams.update({
        "font.size": 10, "axes.linewidth": 0.8, "lines.linewidth": 1.6,
        "axes.spines.top": False, "axes.spines.right": False,
        "xtick.direction": "out", "ytick.direction": "out",
        "legend.frameon": False, "figure.dpi": 150,
        # Glyphs as paths: identical rendering without installed fonts.
        "svg.fonttype": "path", "svg.hashsalt": "plasma-skript",
        # Libertinus Serif for text and math, matching the script and the
        # slides; glyphs missing from it (some relations) come from STIX.
        "font.family": "serif",
        "font.serif": ["Libertinus Serif", "STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "custom", "mathtext.fallback": "stix",
        "mathtext.rm": "Libertinus Serif",
        "mathtext.it": "Libertinus Serif:italic",
        "mathtext.bf": "Libertinus Serif:bold",
        "mathtext.sf": "Libertinus Serif",
        "mathtext.cal": "Libertinus Serif:italic",
        "mathtext.tt": "DejaVu Sans Mono",
        "axes.formatter.use_mathtext": True,
        "axes.unicode_minus": False,
        "axes.edgecolor": "#333333", "xtick.color": "#333333",
        "ytick.color": "#333333", "axes.labelcolor": "#1c1f23",
        "text.color": "#1c1f23",
    })
    fig, ax = plt.subplots(figsize=(width, height), layout="constrained")
    return fig, ax


def save(fig, name):
    """Write build/fig/<name>.svg and .pdf and close the figure."""
    from pathlib import Path

    import matplotlib.pyplot as plt

    out = Path(__file__).resolve().parent / "build" / "fig"
    out.mkdir(parents=True, exist_ok=True)
    # Transparent background: the page or slide supplies the paper; on the
    # website the .quantitative-plot card keeps dark text readable in dark mode.
    # No date metadata, so unchanged plots give byte-identical files.
    fig.savefig(out / f"{name}.svg", transparent=True, metadata={"Date": None})
    fig.savefig(out / f"{name}.pdf", transparent=True,
                metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


def label(ax, x, y, text, color, **kw):
    """Direct curve label in data coordinates, in the curve's color."""
    kw.setdefault("ha", "left")
    kw.setdefault("va", "bottom")
    return ax.text(x, y, text, color=color, **kw)


def log_ticks(axis, lo, hi, step=1):
    """Major ticks at 10^lo ... 10^hi in steps of `step` decades, no minor ticks."""
    from matplotlib.ticker import NullLocator

    axis.set_ticks([10.0**k for k in range(lo, hi + 1, step)])
    axis.set_minor_locator(NullLocator())
