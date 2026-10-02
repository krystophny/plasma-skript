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
