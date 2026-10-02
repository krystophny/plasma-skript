"""Appendix, Gaussian CGS translation: src/appendices/cgs-translation.typ.

Run `python derivations/ch99_cgs_translation.py` to check every row, or
`pytest derivations` to check every chapter.

Mapping (one consistent symbol substitution, SI -> Gaussian):
    eps0 -> 1/(4 pi),   mu0 -> 4 pi / c^2,   B -> B / c,
with every other symbol (q, rho_q, j, I, E, phi, n, p, T, m, lengths) kept.
The map preserves eps0 mu0 c^2 = 1. It turns each SI equation into the
Gaussian equation up to an overall factor, which `same_equation` divides out.

Coverage (line in src/appendices/cgs-translation.typ -> test):
  21-23  Coulomb force                -> test_coulomb_force
  24-26  Poisson equation             -> test_poisson
  27-29  Lorentz force                -> test_lorentz_force
  30-32  Gauss's law                  -> test_gauss_law
  33-35  Ampere-Maxwell law           -> test_ampere_maxwell
  36-38  Faraday's law                -> test_faraday
  39-41  no magnetic monopoles        -> test_no_monopoles
  42-44  Debye length                 -> test_debye_length
  45-47  electron plasma frequency    -> test_plasma_frequency
  48-50  signed gyrofrequency         -> test_gyrofrequency
  51-53  magnetic pressure            -> test_magnetic_pressure
  54-56  plasma beta                  -> test_plasma_beta
  57-59  E x B drift                  -> test_exb_drift
  60-62  magnetic moment              -> test_magnetic_moment (energy -mu.B invariant)
  63-65  MHD force density            -> test_mhd_force
  66-68  1 T = 1e4 G                  -> test_unit_tesla
  69-71  1 J = 1e7 erg                -> test_unit_energy
  72-74  1 m^-3 = 1e-6 cm^-3          -> test_unit_density
  75-77  1 C ~ 2.998e9 statC          -> test_unit_charge
  78-80  1 V ~ 1/299.8 statV          -> test_unit_potential
  83-84  Debye number N_D invariant   -> test_debye_number
  86-87  1 eV in J and erg            -> test_unit_ev
"""

import sympy as sp
from sympy.physics import units as u

from si import UNITS, Derivation, c, check, e, eps0, k_B, m_e, mu0, same_unit, si_unit

q, q1, q2, r, rho, n, T_e, m, p, I, S = sp.symbols(
    "q q_1 q_2 r rho_q n T_e m p I S", positive=True)
B = sp.symbols("B", positive=True)
# Vector components (E, B, v, j) and abstract derivative symbols.
Ex, Ey, Ez, Bx, By, Bz, vx, vy, vz, jx, jy, jz = sp.symbols(
    "E_x E_y E_z B_x B_y B_z v_x v_y v_z j_x j_y j_z", real=True)
lap_phi, divE, divB, curlB, curlE, dEdt, dBdt = sp.symbols(
    r"{\nabla^2\phi} {\nabla\cdot\mathbf{E}} {\nabla\cdot\mathbf{B}}"
    r" {(\nabla\times\mathbf{B})_x} {(\nabla\times\mathbf{E})_x}"
    r" {\partial_t{E_x}} {\partial_t{B_x}}", real=True)
UNITS.update({q: u.coulomb, r: u.meter, n: u.meter**-3, T_e: u.kelvin})

Evec = sp.Matrix([Ex, Ey, Ez])
Bvec = sp.Matrix([Bx, By, Bz])
vvec = sp.Matrix([vx, vy, vz])
jvec = sp.Matrix([jx, jy, jz])

# SI -> Gaussian substitution. Every quantity derived from B (components,
# magnitude, curl, divergence, time derivative) scales like B.
TO_CGS = {eps0: 1 / (4 * sp.pi), mu0: 4 * sp.pi / c**2,
          B: B / c, Bx: Bx / c, By: By / c, Bz: Bz / c,
          curlB: curlB / c, divB: divB / c, dBdt: dBdt / c}


def cgs(expr):
    """Apply the SI -> Gaussian substitution simultaneously."""
    return sp.sympify(expr).subs(TO_CGS, simultaneous=True)


SRC = "src/appendices/cgs-translation.typ"


def same_equation(d, si_residual, cgs_residual):
    """SI residual (lhs - rhs) maps onto the printed Gaussian one up to a constant."""
    d.eq("SI", si_residual, 0)
    d.eq("substitute", sp.expand(cgs(si_residual)), 0)
    ratio = sp.simplify(cgs(si_residual) / cgs_residual)
    assert ratio != 0 and not (ratio.free_symbols - {c}), ratio
    d.eq("Gaussian", sp.expand(cgs(si_residual) / ratio), 0)


def scalar_row(title, line, si, lhs):
    """Record SI expression and its Gaussian image; return the image."""
    d = Derivation(title, f"{SRC}:{line}")
    d.eq("SI", lhs, si)
    return d.eq("substitute", lhs, cgs(si))


def vector_row(title, line, si):
    d = Derivation(title, f"{SRC}:{line}")
    # Display the x component; all three are checked.
    d.step("SI, x component", si[0])
    out = sp.simplify(cgs(si))
    d.step("substitute", sp.expand(out[0]))
    return out


def test_coulomb_force():
    si = q1 * q2 / (4 * sp.pi * eps0 * r**2)  # :22
    UNITS.update({q1: u.coulomb, q2: u.coulomb})
    assert same_unit(si_unit(si), u.newton)
    check(scalar_row("Coulomb force", 21, si, sp.Symbol("F")), q1 * q2 / r**2)  # :23


def test_poisson():
    same_equation(Derivation("Poisson equation", f"{SRC}:24"),
                  lap_phi - (-rho / eps0),  # :25
                  lap_phi - (-4 * sp.pi * rho))  # :26


def test_lorentz_force():
    si = q * (Evec + vvec.cross(Bvec))  # :28
    stated = q * (Evec + vvec.cross(Bvec) / c)  # :29
    for a, b in zip(vector_row("Lorentz force", 27, si), stated):
        check(a, b)


def test_gauss_law():
    same_equation(Derivation("Gauss's law", f"{SRC}:30"),
                  divE - rho / eps0, divE - 4 * sp.pi * rho)  # :31, :32


def test_ampere_maxwell():
    # One Cartesian component; curlB and dEdt stand for that component.
    same_equation(Derivation("Ampere-Maxwell law", f"{SRC}:33"),
                  curlB - (mu0 * jx + mu0 * eps0 * dEdt),  # :34
                  curlB - ((4 * sp.pi) / c * jx + 1 / c * dEdt))  # :35


def test_faraday():
    same_equation(Derivation("Faraday's law", f"{SRC}:36"),
                  curlE - (-dBdt),  # :37
                  curlE - (-1 / c * dBdt))  # :38


def test_no_monopoles():
    d = Derivation("No magnetic monopoles", f"{SRC}:39")
    # divB = 0 maps to divB / c = 0: the same statement.
    d.eq("substitute", cgs(divB), 0)
    assert sp.solve(cgs(divB), divB) == [0]  # :40, :41


def test_debye_length():
    si = sp.sqrt((eps0 * k_B * T_e) / (n * e**2))  # :43
    assert same_unit(si_unit(si), u.meter)
    check(scalar_row("Debye length", 42, si, sp.Symbol("lambda_D")),
          sp.sqrt((k_B * T_e) / (4 * sp.pi * n * e**2)))  # :44


def test_plasma_frequency():
    si = sp.sqrt((n * e**2) / (eps0 * m_e))  # :46
    assert same_unit(si_unit(si), u.second**-1)
    check(scalar_row("Electron plasma frequency", 45, si, sp.Symbol("omega_pe")),
          sp.sqrt((4 * sp.pi * n * e**2) / m_e))  # :47


def test_gyrofrequency():
    # Circular orbit in m dv/dt = q v x B: m Omega^2 r = q Omega r B, Omega = q B / m.
    Om = sp.symbols("Omega", positive=True)
    si = sp.solve(sp.Eq(m * Om**2 * r, q * Om * r * B), Om)[0]
    check(si, q * B / m)  # :49
    check(scalar_row("Signed gyrofrequency", 48, si, sp.Symbol("Omega")), (q * B) / (m * c))  # :50


def test_magnetic_pressure():
    check(scalar_row("Magnetic pressure", 51, B**2 / (2 * mu0), sp.Symbol("p_B")), B**2 / (8 * sp.pi))  # :52, :53


def test_plasma_beta():
    check(scalar_row("Plasma beta", 54, (2 * mu0 * p) / B**2, sp.Symbol("beta")), (8 * sp.pi * p) / B**2)  # :55, :56


def test_exb_drift():
    si = Evec.cross(Bvec) / (Bx**2 + By**2 + Bz**2)  # :58
    stated = c * Evec.cross(Bvec) / (Bx**2 + By**2 + Bz**2)  # :59
    for a, b in zip(vector_row("E x B drift", 57, si), stated):
        check(a, b)


def test_magnetic_moment():
    d = Derivation("Magnetic moment of a current loop", f"{SRC}:60")
    # The moment is defined through the energy U = -mu B, the same number in
    # both systems. SI: mu_SI = I S (:61). Require mu_G B_G = mu_SI B_SI.
    mu_G = sp.symbols("mu_G")
    d.step("energy", sp.Eq(mu_G * B, cgs(I * S * B)))
    mu_sol = d.eq("solve", mu_G, sp.solve(sp.Eq(mu_G * B, cgs(I * S * B)), mu_G)[0])
    check(mu_sol, (I * S) / c)  # :62


def test_mhd_force():
    si = jvec.cross(Bvec)  # :64
    stated = jvec.cross(Bvec) / c  # :65
    for a, b in zip(vector_row("MHD force density", 63, si), stated):
        check(a, b)


# Unit conversion factors. Exact SI: c = 299792458 m/s, e = 1.602176634e-19 C.
# mu0 = 4 pi 1e-7 H/m is used for the Gaussian link; the CODATA 2018 value
# differs from it by 5.5e-10 relative, far below the printed precision.
C_SI = sp.Integer(299792458)
MU0_SI = 4 * sp.pi * sp.Rational(1, 10**7)
EPS0_SI = 1 / (MU0_SI * C_SI**2)
E_SI = sp.Rational(1602176634, 10**28)
GRAM, CM = sp.Rational(1, 1000), sp.Rational(1, 100)  # in kg and m
ERG = GRAM * CM**2  # in J
DYN = GRAM * CM  # in N


def test_unit_energy():
    d = Derivation("Energy unit", f"{SRC}:69")
    d.eq("1 J in erg", sp.Symbol("J") / sp.Symbol("erg"), 1 / ERG)
    check(1 / ERG, sp.Integer(10)**7)  # :70, :71
    # Same factor from sympy's unit system.
    assert sp.physics.units.convert_to(u.joule, [u.gram, u.centimeter, u.second]) \
        == 10**7 * u.gram * u.centimeter**2 / u.second**2


def test_unit_density():
    d = Derivation("Number density unit", f"{SRC}:72")
    d.eq("cm3 per m3", sp.Symbol("m") ** -3 / sp.Symbol("cm") ** -3, CM**3)
    check(CM**3, sp.Integer(10)**-6)  # :73, :74  (1 m^-3 = 1e-6 cm^-3)


def test_unit_charge():
    # Equal Coulomb force: 1 C and 1 C at 1 m <-> q_G and q_G at 100 cm.
    F_dyn = 1 / (4 * sp.pi * EPS0_SI) / DYN
    qG = sp.sqrt(F_dyn * (1 / CM) ** 2)
    d = Derivation("Charge unit", f"{SRC}:75")
    d.eq("Coulomb force, dyn", sp.Symbol("F"), sp.Float(float(F_dyn), 8))
    d.eq("equal force at 100 cm", sp.Symbol("q_G"), qG)
    check(qG, 10 * C_SI)
    assert abs(float(qG) / 2.998e9 - 1) < 1e-4  # :76
    # Elementary charge in statC.
    assert abs(float(E_SI * qG) / 4.8032e-10 - 1) < 1e-4


def test_unit_potential():
    # Equal energy q phi: 1 C x 1 V = 1 J = 1e7 erg = (10 c statC) x phi_G.
    phiG = (1 / ERG) / (10 * C_SI)
    d = Derivation("Potential unit", f"{SRC}:78")
    d.eq("equal energy", sp.Symbol("phi_G"), phiG)
    assert abs(float(phiG) * 299.8 - 1) < 1e-4  # :79


def test_unit_tesla():
    # Equal magnetic energy density: B_SI^2/(2 mu0) J/m^3 = B_G^2/(8 pi) erg/cm^3.
    w = 1**2 / (2 * MU0_SI) * ERG ** -1 * CM**3  # erg/cm^3 for 1 T
    BG = sp.sqrt(8 * sp.pi * w)
    d = Derivation("Magnetic field unit", f"{SRC}:66")
    d.eq("energy density, erg/cm3", sp.Symbol("w"), sp.nsimplify(w))
    d.eq("equal energy density", sp.Symbol("B_G"), BG)
    check(BG, sp.Integer(10)**4)  # :67, :68


def test_debye_number():
    # N_D = (4 pi/3) n lambda_D^3: same number from SI and Gaussian inputs.
    n_si, T_eV = 10**19, 10
    kT_si = T_eV * E_SI
    lam_si = sp.sqrt(EPS0_SI * kT_si / (n_si * E_SI**2))
    ND_si = sp.Rational(4, 3) * sp.pi * n_si * lam_si**3  # :84
    n_g, kT_g, e_g = n_si * CM**3, kT_si / ERG, E_SI * 10 * C_SI
    lam_g = sp.sqrt(kT_g / (4 * sp.pi * n_g * e_g**2))  # Gaussian Debye length, cm
    ND_g = sp.Rational(4, 3) * sp.pi * n_g * lam_g**3
    assert abs(float(ND_si / ND_g) - 1) < 1e-12
    d = Derivation("Debye number", f"{SRC}:83-84")
    d.eq("SI input", sp.Symbol("N_D"), sp.Float(float(ND_si), 6))
    d.eq("Gaussian", sp.Symbol("N_D"), sp.Float(float(ND_g), 6))
    check(lam_g * CM, lam_si)


def test_unit_ev():
    d = Derivation("Electronvolt", f"{SRC}:86-87")
    d.eq("J", sp.Symbol("eV"), sp.Float(float(E_SI), 11))
    d.eq("erg", sp.Symbol("eV"), sp.Float(float(E_SI / ERG), 11))
    check(E_SI, sp.Rational(1602176634, 10**28))  # :87 (J)
    check(E_SI / ERG, sp.Rational(1602176634, 10**21))  # :87 (erg)


if __name__ == "__main__":
    from si import run_as_script
    run_as_script(globals())
