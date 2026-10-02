"""Chapter 2, Debye shielding: src/chapters/02-debye-shielding.typ.

Run `python derivations/ch02_debye_shielding.py` to print the steps, or
`pytest derivations` to check every chapter.
"""

import sympy as sp
from sympy.physics import units as u

from si import UNITS, check, e, eps0, k_B

n0, T_e, Q, r, phi = sp.symbols("n_0 T_e Q r phi", positive=True)
UNITS.update({n0: u.meter**-3, T_e: u.kelvin, Q: u.coulomb, r: u.meter})


def test_debye_length():
    # Boltzmann electrons, immobile ions: rho = e n0 (1 - exp(e phi / k_B T_e)).
    rho = e * n0 * (1 - sp.exp(e * phi / (k_B * T_e)))
    # Linearize for e phi << k_B T_e.
    rho_lin = sp.series(rho, phi, 0, 2).removeO()
    # Poisson: laplacian(phi) = -rho/eps0 = phi / lambda_D^2.
    inv_lambda_sq = sp.simplify(-rho_lin / eps0 / phi)
    lambda_D = sp.sqrt(1 / inv_lambda_sq)
    stated = sp.sqrt(eps0 * k_B * T_e / (n0 * e**2))
    check(lambda_D, stated, unit=u.meter)


def test_screened_potential():
    # Spherical Debye-Hueckel equation: (1/r^2) d/dr(r^2 dphi/dr) = phi/lambda^2.
    lam = sp.symbols("lambda_D", positive=True)
    UNITS[lam] = u.meter
    stated = Q / (4 * sp.pi * eps0 * r) * sp.exp(-r / lam)
    lhs = sp.diff(r**2 * sp.diff(stated, r), r) / r**2
    assert sp.simplify(lhs - stated / lam**2) == 0
    # Bare Coulomb potential for r << lambda_D.
    check(sp.limit(stated * r, r, 0) / r, Q / (4 * sp.pi * eps0 * r), unit=u.volt)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
