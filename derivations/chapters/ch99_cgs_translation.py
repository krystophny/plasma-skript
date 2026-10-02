# Appendix · Gaussian CGS translation (src/appendices/cgs-translation.typ)
#
# One substitution turns every SI row of the table into its Gaussian row:
# eps0 -> 1/(4 pi), mu0 -> 4 pi/c^2, B -> B/c; all other symbols stay.
# Then the unit factors (T, J, m^-3, C, V, eV) from exact SI values.

# %% Setup
import sympy as sp
from sympy.physics import units as u

import si
from notebook import agrees, note, report, section, show

e, eps0, mu0, k_B, m_e, c = sp.symbols("e epsilon_0 mu_0 k_B m_e c", positive=True)
q, q1, q2, r, rho, n, T_e, m, p, I, S = sp.symbols("q q_1 q_2 r rho_q n T_e m p I S", positive=True)
B = sp.Symbol("B", positive=True)
Ex, Ey, Ez, Bx, By, Bz, vx, vy, vz, jx, jy, jz = sp.symbols(
    "E_x E_y E_z B_x B_y B_z v_x v_y v_z j_x j_y j_z", real=True)
# Field derivatives as plain symbols; curl and time derivative stand for one component.
lap_phi, div_E, div_B, curl_B, curl_E, dE_dt, dB_dt = sp.symbols(
    r"{\nabla^2\phi} {\nabla\cdot\mathbf{E}} {\nabla\cdot\mathbf{B}}"
    r" {(\nabla\times\mathbf{B})_x} {(\nabla\times\mathbf{E})_x}"
    r" {\partial_t{E_x}} {\partial_t{B_x}}", real=True)
E_vec, B_vec, v_vec, j_vec = (sp.Matrix(t) for t in ([Ex, Ey, Ez], [Bx, By, Bz], [vx, vy, vz], [jx, jy, jz]))
B_sq = Bx**2 + By**2 + Bz**2
UNITS = {q: u.coulomb, q1: u.coulomb, q2: u.coulomb, r: u.meter, n: u.meter**-3, T_e: u.kelvin}

# %% The substitution
section("SI to Gaussian substitution", script="cgs-translation")
note("Every quantity built from B (components, curl, divergence, time derivative) scales like B")
TO_CGS = {eps0: 1 / (4 * sp.pi), mu0: 4 * sp.pi / c**2, B: B / c, Bx: Bx / c, By: By / c, Bz: Bz / c,
          curl_B: curl_B / c, div_B: div_B / c, dB_dt: dB_dt / c}
note("Replace the left by the right:")
show(sp.Eq(sp.Tuple(eps0, mu0, B), sp.Tuple(*(TO_CGS[s] for s in (eps0, mu0, B))), evaluate=False))
assert sp.simplify((eps0 * mu0 * c**2).subs(TO_CGS, simultaneous=True)) == 1
note("The map keeps", sp.Eq(eps0 * mu0 * c**2, 1))


def cgs(expr):
    """Apply the SI -> Gaussian substitution simultaneously."""
    return sp.sympify(expr).subs(TO_CGS, simultaneous=True)


def scalar_row(title, symbol, si_expr, gaussian):
    """Show the SI row, map it, and compare with the printed Gaussian row."""
    section(title, script="cgs-translation")
    show(sp.Eq(symbol, si_expr))
    return agrees(cgs(si_expr), gaussian, lhs=symbol)


def equation_row(title, si_lhs, si_rhs, gaussian_lhs, gaussian_rhs):
    """Map an SI equation; it equals the printed Gaussian one up to a constant factor."""
    section(title, script="cgs-translation")
    show(sp.Eq(si_lhs, si_rhs))
    residual = cgs(si_lhs - si_rhs)
    factor = sp.simplify(residual / (gaussian_lhs - gaussian_rhs))
    assert factor != 0 and not (factor.free_symbols - {c}), factor
    assert sp.simplify(cgs(si_lhs) / factor - gaussian_lhs) == 0
    if factor != 1:
        note("Substitute and divide by the constant", factor)
    agrees(sp.expand(cgs(si_rhs) / factor), gaussian_rhs, lhs=gaussian_lhs)


def vector_row(title, symbol, si_vec, gaussian_vec):
    """Map a vector row component by component; show the x component."""
    section(title, script="cgs-translation")
    show(sp.Eq(symbol, si_vec[0]))
    mapped = sp.simplify(cgs(si_vec))
    for derived, printed in zip(mapped, gaussian_vec):
        si.check(derived, printed)
    agrees(mapped[0], gaussian_vec[0], lhs=symbol)
    note("and likewise for the y and z components")


# %% Maxwell and force rows
coulomb = q1 * q2 / (4 * sp.pi * eps0 * r**2)
assert si.same_unit(si.si_unit(coulomb, UNITS), u.newton)
scalar_row("Coulomb force", sp.Symbol("F"), coulomb, q1 * q2 / r**2)
equation_row("Poisson equation", lap_phi, -rho / eps0, lap_phi, -4 * sp.pi * rho)
vector_row("Lorentz force", sp.Symbol("F_x"), q * (E_vec + v_vec.cross(B_vec)),
           q * (E_vec + v_vec.cross(B_vec) / c))
equation_row("Gauss's law", div_E, rho / eps0, div_E, 4 * sp.pi * rho)
equation_row("Ampère-Maxwell law", curl_B, mu0 * jx + mu0 * eps0 * dE_dt,
             curl_B, 4 * sp.pi / c * jx + dE_dt / c)
equation_row("Faraday's law", curl_E, -dB_dt, curl_E, -dB_dt / c)

section("No magnetic monopoles", script="cgs-translation")
show(sp.Eq(cgs(div_B), 0))
assert sp.solve(cgs(div_B), div_B) == [0]
note("the same statement,", sp.Eq(div_B, 0))

# %% Plasma parameters
debye = sp.sqrt(eps0 * k_B * T_e / (n * e**2))
assert si.same_unit(si.si_unit(debye, UNITS), u.meter)
scalar_row("Debye length", sp.Symbol("lambda_D"), debye, sp.sqrt(k_B * T_e / (4 * sp.pi * n * e**2)))
plasma = sp.sqrt(n * e**2 / (eps0 * m_e))
assert si.same_unit(si.si_unit(plasma, UNITS), u.second**-1)
scalar_row("Electron plasma frequency", sp.Symbol("omega_pe"), plasma, sp.sqrt(4 * sp.pi * n * e**2 / m_e))
section("Signed gyrofrequency", script="cgs-translation")
Om = sp.Symbol("Omega", positive=True)
note("Circular orbit,", sp.Eq(m * Om**2 * r, q * Om * r * B))
gyro = sp.solve(sp.Eq(m * Om**2 * r, q * Om * r * B), Om)[0]
agrees(gyro, q * B / m, lhs=Om)
agrees(cgs(gyro), q * B / (m * c), lhs=Om)
scalar_row("Magnetic pressure", sp.Symbol("p_B"), B**2 / (2 * mu0), B**2 / (8 * sp.pi))
scalar_row("Plasma beta", sp.Symbol("beta"), 2 * mu0 * p / B**2, 8 * sp.pi * p / B**2)
vector_row("E x B drift", sp.Symbol("v_E,x"), E_vec.cross(B_vec) / B_sq, c * E_vec.cross(B_vec) / B_sq)

section("Magnetic moment of a current loop", script="cgs-translation")
mu_G = sp.Symbol("mu_G")
note("The energy", -sp.Symbol("mu") * B, "is the same number in both systems; SI moment", I * S)
energy = show(sp.Eq(mu_G * B, cgs(I * S * B)))
agrees(sp.solve(energy, mu_G)[0], I * S / c, lhs=mu_G)

vector_row("MHD force density", sp.Symbol("f_x"), j_vec.cross(B_vec), j_vec.cross(B_vec) / c)

# %% Unit factors
# Exact SI: c = 299792458 m/s, e = 1.602176634e-19 C. mu0 = 4 pi 1e-7 H/m links
# the systems; CODATA 2018 differs by 5.5e-10 relative, far below the printed digits.
C_SI = sp.Integer(299792458)
MU0_SI = 4 * sp.pi * sp.Rational(1, 10**7)
EPS0_SI = 1 / (MU0_SI * C_SI**2)
E_SI = sp.Rational(1602176634, 10**28)
GRAM, CM = sp.Rational(1, 1000), sp.Rational(1, 100)  # in kg and m
erg, cm, gauss, dyn, statC, statV = sp.symbols("erg cm G dyn statC statV", positive=True)  # unit names
ERG, DYN = GRAM * CM**2, GRAM * CM  # in J and N

section("Magnetic field unit", script="cgs-translation")
note("Equal magnetic energy density,", sp.Eq(sp.Symbol("B_SI") ** 2 / (2 * mu0), sp.Symbol("B_G") ** 2 / (8 * sp.pi)))
w_density = 1 / (2 * MU0_SI) / ERG * CM**3  # erg/cm^3 for 1 T
show(sp.Eq(sp.Symbol("w") / (erg / cm**3), sp.nsimplify(w_density)))
agrees(sp.sqrt(8 * sp.pi * w_density), sp.Integer(10) ** 4, lhs=sp.Symbol("B_G") / gauss)

section("Energy unit", script="cgs-translation")
agrees(1 / ERG, sp.Integer(10) ** 7, lhs=sp.Symbol("J") / erg)
assert u.convert_to(u.joule, [u.gram, u.centimeter, u.second]) == 10**7 * u.gram * u.centimeter**2 / u.second**2

section("Number density unit", script="cgs-translation")
agrees(CM**3, sp.Integer(10) ** -6, lhs=cm**3 / sp.Symbol("m") ** 3)

section("Charge unit", script="cgs-translation")
note("Equal Coulomb force: 1 C and 1 C at 1 m against", sp.Symbol("q_G"), "and", sp.Symbol("q_G"), "at 100 cm")
force_dyn = 1 / (4 * sp.pi * EPS0_SI) / DYN
show(sp.Eq(sp.Symbol("F") / dyn, sp.Float(float(force_dyn), 8)))
q_G = sp.sqrt(force_dyn / CM**2)
agrees(q_G, 10 * C_SI, lhs=sp.Symbol("q_G") / statC)
assert abs(float(q_G) / 2.998e9 - 1) < 1e-4
assert abs(float(E_SI * q_G) / 4.8032e-10 - 1) < 1e-4  # elementary charge in statC
show(sp.Eq(e / statC, sp.Float(float(E_SI * q_G), 5)))

section("Potential unit", script="cgs-translation")
note("Equal energy: 1 C times 1 V is", sp.Integer(10) ** 7 * erg, ", the charge is", 10 * C_SI, "statC")
phi_G = (1 / ERG) / (10 * C_SI)
show(sp.Eq(sp.Symbol("phi_G") / statV, phi_G))
show(sp.Eq(sp.Symbol("phi_G") / statV, sp.Float(float(phi_G), 5)))
assert abs(float(phi_G) * 299.8 - 1) < 1e-4

section("Debye number", script="cgs-translation")
n_si, kT_si = 10**19, 10 * E_SI  # 1e19 m^-3, 10 eV in J
lambda_si = sp.sqrt(EPS0_SI * kT_si / (n_si * E_SI**2))
N_D_si = sp.Rational(4, 3) * sp.pi * n_si * lambda_si**3
n_g, kT_g, e_g = n_si * CM**3, kT_si / ERG, E_SI * 10 * C_SI
lambda_g = sp.sqrt(kT_g / (4 * sp.pi * n_g * e_g**2))  # Gaussian Debye length in cm
N_D_g = sp.Rational(4, 3) * sp.pi * n_g * lambda_g**3
note("Same plasma,", sp.Eq(n, sp.Float(1e19, 2) / u.meter**3, evaluate=False), ", 10 eV, in both systems:")
show(sp.Eq(sp.Symbol("N_D,SI"), sp.Float(float(N_D_si), 6)))
show(sp.Eq(sp.Symbol("N_D,G"), sp.Float(float(N_D_g), 6)))
assert abs(float(N_D_si / N_D_g) - 1) < 1e-12
si.check(lambda_g * CM, lambda_si)

section("Electronvolt", script="cgs-translation")
agrees(E_SI, sp.Rational(1602176634, 10**28), lhs=sp.Symbol("eV") / sp.Symbol("J"))
agrees(E_SI / ERG, sp.Rational(1602176634, 10**21), lhs=sp.Symbol("eV") / erg)
show(sp.Eq(sp.Symbol("eV") / erg, sp.Float(float(E_SI / ERG), 10)))

# %%
if __name__ == "__main__":
    report(__file__, "Appendix · Gaussian CGS translation")
