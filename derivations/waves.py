"""Plain helpers shared by the wave chapters ch11-ch15 (no display, no checks)."""

import sympy as sp
from sympy.physics import units as u
from sympy.physics.units import convert_to

from notebook import CONSTANTS

_BASE = [u.kilogram, u.meter, u.second, u.ampere, u.kelvin]


def number(expr, inputs=None):
    """Float of a dimensionless expr; CODATA constants and `inputs` substituted.

    `inputs` maps symbols to numbers or to quantities with units; the units
    must cancel.
    """
    subs = {s: CONSTANTS[s.name] for s in expr.free_symbols if s.name in CONSTANTS}
    subs.update(inputs or {})
    value = complex(convert_to(sp.sympify(expr).subs(subs), _BASE).evalf())
    return value.real if abs(value.imag) <= 1e-12 * abs(value) else value


def plane_wave_matrix(equations, unknowns):
    """Coefficient matrix of a homogeneous linear system (rows: equations)."""
    exprs = [eq.lhs - eq.rhs if isinstance(eq, sp.Equality) else eq for eq in equations]
    return sp.ImmutableMatrix(sp.linear_eq_to_matrix(exprs, unknowns)[0])


def matmul(matrix, vector):
    """Unevaluated product matrix * vector for display of a linear system."""
    return sp.MatMul(sp.ImmutableMatrix(matrix), sp.ImmutableMatrix(vector),
                     evaluate=False)


def rounded(expr, digits=3):
    """Copy of expr with each Float shown to `digits` significant digits.

    Only for showing input values; compute with the full-precision original.
    """
    return expr.xreplace({f: sp.Float(f, digits) for f in expr.atoms(sp.Float)})
