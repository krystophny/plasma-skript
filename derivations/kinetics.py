"""Plain helpers shared by the chapter scripts ch00-ch05 (no display).

Chapter scripts must not import each other (importing runs a chapter), so the
few functions they share live here.
"""

import sympy as sp


def maxwellian(n, m, kT, velocity, drift):
    """Shifted Maxwellian n (m / 2 pi kT)^(3/2) exp(-m |v - u|^2 / 2 kT).

    The prefactor is kept unevaluated, so the expression prints in this form.
    """
    w2 = sum((v - w) ** 2 for v, w in zip(velocity, drift))
    prefactor = sp.Pow(m / (2 * sp.pi * kT), sp.Rational(3, 2), evaluate=False)
    return sp.Mul(n, prefactor, sp.exp(-m * w2 / (2 * kT)), evaluate=False)


def velocity_integral(expr, velocity, drift):
    """Integral of expr over all of velocity space.

    Shifts v = u + w (the integral over R^3 is shift invariant) and integrates
    one Cartesian component of w at a time.
    """
    ws = sp.symbols("w_x w_y w_z", real=True)
    expr = expr.subs({v: w + u for v, w, u in zip(velocity, ws, drift)})
    for w in ws:
        expr = sp.integrate(sp.expand(expr), (w, -sp.oo, sp.oo))
    return sp.simplify(expr)


def rounding_rtol(printed):
    """Relative tolerance of a number printed as the string `printed`.

    Half a unit in the last printed digit, e.g. "6.9e-6" -> 0.05e-6 / 6.9e-6.
    """
    mantissa, _, exponent = printed.lower().partition("e")
    decimals = len(mantissa.partition(".")[2])
    half_unit = 0.5 * 10.0 ** (int(exponent or 0) - decimals)
    return half_unit / abs(float(printed))
