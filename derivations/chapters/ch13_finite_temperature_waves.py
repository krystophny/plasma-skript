# Chapter 13 · Finite-temperature waves (src/chapters/13-finite-temperature-waves.typ)
#
# Collisions as a complex mass, ion dynamics in the cold tensor (Alfvén, whistler,
# ion cyclotron), warm-fluid pressure (Langmuir, ion acoustic, upper hybrid) and
# the MHD waves. `python ch13_finite_temperature_waves.py` prints every step.

# %% Setup
import numpy as np
import sympy as sp
from sympy.physics import units as u

import si
from notebook import PROTON_MASS, agrees, close_to, evaluate, note, report, section, show
from si import BLUE, GRAY, ORANGE, figure, label, log_ticks, save
from waves import matmul, number, plane_wave_matrix

e, m_e, m_i, eps0, mu0, k_B, c = sp.symbols("e m_e m_i epsilon_0 mu_0 k_B c", positive=True)
I = sp.I
w, nu, k, k_par = sp.symbols(r"omega nu k k_\parallel", positive=True)
n0, B0, T_e, T_i = sp.symbols("n_0 B_0 T_e T_i", positive=True)
gamma_e, gamma_i, gamma = sp.symbols("gamma_e gamma_i gamma", positive=True)  # adiabatic indices
wpe, wpi, wce, wci = sp.symbols("omega_pe omega_pi omega_ce omega_ci", positive=True)
c_se, c_si, v_s, v_A, rho0, p0 = sp.symbols("c_se c_si v_s v_A rho_0 p_0", positive=True)
z = sp.Symbol("z", real=True)
Ex, Ey, Ez = sp.symbols("E_x E_y E_z")
E = sp.Matrix([Ex, Ey, Ez])
S, D = sp.symbols(r"\epsilon_\perp \epsilon_\times")

# SI units of the local symbols, for si.check(..., unit=...).
UNITS = {w: u.second**-1, nu: u.second**-1, k: u.meter**-1, k_par: u.meter**-1,
         n0: u.meter**-3, B0: u.tesla, T_e: u.kelvin, T_i: u.kelvin,
         gamma_e: 1, gamma_i: 1, gamma: 1, wpe: u.second**-1, wpi: u.second**-1,
         wce: u.second**-1, wci: u.second**-1, c_se: u.meter / u.second,
         c_si: u.meter / u.second, v_s: u.meter / u.second, v_A: u.meter / u.second,
         rho0: u.kilogram / u.meter**3, p0: u.pascal}


def cold_velocity(q, m, Om, drag=0):
    """Solve -i w m u = q (E + u x B0 e_z) - m nu u; Om = q B0/m is signed."""
    vel = sp.Matrix(sp.symbols("u_x u_y u_z"))
    eqs = -I * w * vel - (q / m) * E - Om * vel.cross(sp.Matrix([0, 0, 1])) + drag * vel
    sol = sp.solve(list(eqs), list(vel), dict=True)[0]
    return vel.subs(sol)


def dielectric(species):
    """Cold tensor eps = 1 + i j/(eps0 w) for species (q, n, m, Om, drag)."""
    j = sum((q * n * cold_velocity(q, m, Om, drag) for q, n, m, Om, drag in species),
            sp.zeros(3, 1))
    return (E + I / (eps0 * w) * j).jacobian(E)


def electron(drag=0):
    """Electron species with omega_pe, omega_ce; Omega_e = -omega_ce."""
    return (-e, wpe**2 * eps0 * m_e / e**2, m_e, -wce, drag)


def ion():
    """Singly charged ion species with omega_pi, omega_ci."""
    return (e, wpi**2 * eps0 * m_i / e**2, m_i, wci, 0)


# Equal densities, Z = 1: ion frequencies follow from the electron ones.
ION = {wpi: wpe * sp.sqrt(m_e / m_i), wci: wce * m_e / m_i}
# Circular two-fluid indices without the O(m_e/m_i) numerator term (:279, :281).
N2_RH = 1 - wpe**2 / ((w + wci) * (w - wce))
N2_LH = 1 - wpe**2 / ((w - wci) * (w + wce))

# %% Complex effective mass
section("Complex effective mass", "13-finite-temperature-waves.typ:99")
m, m_eff = sp.Symbol("m", positive=True), sp.Symbol("m_eff")
note("Drag", -m * nu * sp.Symbol("u"), "moved to the left of the momentum equation")
law = show(sp.Eq(-I * w * m + m * nu, -I * w * m_eff))
agrees(sp.solve(law, m_eff)[0], m * (1 + I * nu / w), ":115", lhs=m_eff)
Om = sp.Symbol("Omega", real=True)
effective = m * (1 + I * nu / w)
assert sp.simplify(cold_velocity(-e, m, Om, drag=nu)
                   - cold_velocity(-e, effective, Om * m / effective)) == sp.zeros(3, 1)
note("Same velocity response as a collisionless species of mass", m_eff)

# %% Collisional RH branch
section("Collisional RH branch", "13-finite-temperature-waves.typ:82")
eps = dielectric([electron(drag=nu)])
note("Cold electron tensor with drag; right-hand circular combination",
     sp.Eq(sp.Symbol("N_RH") ** 2, sp.Symbol("epsilon_xx") + I * sp.Symbol("epsilon_xy")))
R = sp.simplify(eps[0, 0] + I * eps[0, 1])
stated = 1 - wpe**2 / (w * (w - wce + I * nu))
agrees(R, stated, ":82", lhs=sp.Symbol("N_RH") ** 2)
si.check(R, stated, unit=1, units=UNITS)
note("Effective parameters: divide", wpe**2, "and", wce, "by", 1 + I * nu / w)
effective_form = (wpe**2 / (1 + I * nu / w)) / (w * (w - wce / (1 + I * nu / w)))
agrees(effective_form, wpe**2 / (w * (w - wce + I * nu)), ":126",
       lhs=sp.UnevaluatedExpr(effective_form))

# %% Weak-collision susceptibility
section("Weak-collision susceptibility", "13-finite-temperature-waves.typ:135")
chi_e = sp.Symbol("chi_e")
chi = show(sp.Eq(chi_e, wpe**2 / (w * (w + I * nu)))).rhs
note("First order in", nu / w)
first_order = sp.series(chi, nu, 0, 2).removeO()
agrees(first_order, wpe**2 / w**2 * (1 - I * nu / w), ":136", lhs=chi_e)
si.check(first_order, wpe**2 / w**2 * (1 - I * nu / w), unit=1, units=UNITS)
assert sp.im(sp.expand(1 - first_order)).subs({nu: 1, w: 2, wpe: 1}) > 0
note("so", sp.Eq(sp.Symbol("N") ** 2, 1 - chi_e), "has a positive imaginary part")

# %% Spatial attenuation
section("Spatial attenuation", "13-finite-temperature-waves.typ:143")
k_r, k_i, t = sp.symbols("k_r k_i t", positive=True)
field = sp.exp(I * (k_r + I * k_i) * z - I * w * t)
note("Complex wave number", sp.Eq(k, k_r + I * k_i, evaluate=False))
agrees(sp.powsimp(sp.expand(field)), sp.powsimp(sp.exp(I * k_r * z - I * w * t) * sp.exp(-k_i * z)),
       ":143", lhs=sp.UnevaluatedExpr(field))
intensity = show(sp.Eq(sp.Symbol("I") / sp.Symbol("I_0"), sp.exp(-k_i * z) ** 2)).rhs
L_I = sp.solve(sp.Eq(sp.log(intensity), -1), z)[0]
agrees(L_I, 1 / (2 * k_i), ":147", lhs=sp.Symbol("L_I"))
si.check(L_I, 1 / (2 * k_i), unit=u.meter, units={k_i: u.meter**-1})

# %% Worked example: collisional attenuation
section("Worked example: collisional attenuation", "13-finite-temperature-waves.typ:166")
drive = {wpe: 5.64e9 / u.second, w: 2.00e10 / u.second, nu: 1.00e9 / u.second}
note("Frequencies in 1/s:", sp.Eq(wpe, sp.Float(5.64e9, 3)), ",", sp.Eq(w, sp.Float(2.0e10, 3)),
     ",", sp.Eq(nu, sp.Float(1.0e9, 3)))
mass_ratio = number(1 + I * nu / w, drive)
show(sp.Eq(m_eff / m, sp.Float(mass_ratio.real, 3) + I * sp.Float(mass_ratio.imag, 3)))
close_to(mass_ratio.real, 1.00, source=":175")
close_to(mass_ratio.imag, 0.05, source=":175")
weak = 1 - wpe**2 / w**2 * (1 - I * nu / w)
index = number(sp.sqrt(weak), drive)
show(sp.Eq(sp.Symbol("N"), sp.Float(index.real, 3) + I * sp.Float(index.imag, 3)))
close_to(index.real, 0.959, source=":176")
close_to(index.imag, 2.07e-3, source=":176")
wave_number = number(sp.sqrt(weak) * w / c * u.meter, drive)
show(sp.Eq(sp.Symbol("k"), (sp.Float(wave_number.real, 3) + I * sp.Float(wave_number.imag, 3))
           / u.meter, evaluate=False))
close_to(wave_number.real, 64.0, source=":177")
close_to(wave_number.imag, 1.38e-1, source=":178")
L_value = evaluate(sp.Symbol("L"), 1 / sp.Symbol("k_i"), {sp.Symbol("k_i"): wave_number.imag / u.meter},
                   u.meter)
close_to(L_value, 7.23, source=":179")

# %% Two-species cold tensor
section("Two-species cold tensor", "13-finite-temperature-waves.typ:257")
note("Electrons", sp.Eq(sp.Symbol("Omega_e"), -wce), "and ions", sp.Eq(sp.Symbol("Omega_i"), wci))
eps = dielectric([electron(), ion()])
eps_perp = 1 - (wpe**2 / (w**2 - wce**2) + wpi**2 / (w**2 - wci**2))
eps_times = -(wce * wpe**2) / (w * (w**2 - wce**2)) + (wci * wpi**2) / (w * (w**2 - wci**2))
eps_par = 1 - (wpe**2 + wpi**2) / w**2
for derived, stated, symbol, line in [(eps[0, 0], eps_perp, S, ":257"),
                                      (I * eps[0, 1], eps_times, D, ":260"),
                                      (eps[2, 2], eps_par, sp.Symbol(r"\epsilon_\parallel"), ":263")]:
    agrees(sp.simplify(derived), stated, line, lhs=symbol)
    si.check(sp.simplify(derived.subs(ION)), stated.subs(ION), unit=1, units=UNITS)

# %% Mass-ratio identities
section("Mass-ratio identities", "13-finite-temperature-waves.typ:324")
note("Equal densities, singly charged ions")
plasma_sq = lambda mass: n0 * e**2 / (eps0 * mass)  # noqa: E731
cyclotron = lambda mass: e * B0 / mass  # noqa: E731
agrees(plasma_sq(m_i) / plasma_sq(m_e), m_e / m_i, ":264", lhs=wpi**2 / wpe**2)
agrees(cyclotron(m_i) / cyclotron(m_e), m_e / m_i, ":983", lhs=wci / wce)
si.check(plasma_sq(m_i) / plasma_sq(m_e), cyclotron(m_i) / cyclotron(m_e))  # :324

# %% Parallel-propagation determinant
section("Parallel-propagation determinant", "13-finite-temperature-waves.typ:313")
N_sq = sp.Symbol("N^2")
M_transverse = sp.Matrix([[S, -I * D], [I * D, S]]) - N_sq * sp.eye(2)
note("Transverse block of the wave matrix for k along", B0)
show(sp.Eq(matmul(M_transverse, [Ex, Ey]), sp.ImmutableMatrix([0, 0]), evaluate=False))
show(sp.Eq(sp.factor(M_transverse.det()), 0))
roots = set(sp.solve(M_transverse.det(), N_sq))
assert roots == {S + D, S - D}  # :313
for root in sorted(roots, key=str):
    show(sp.Eq(N_sq, root))

# %% Circular branches with ions
section("Circular branches with ions", "13-finite-temperature-waves.typ:319")
R = sp.simplify(eps[0, 0] + I * eps[0, 1])
L = sp.simplify(eps[0, 0] - I * eps[0, 1])
rh_sum = 1 - wpe**2 / (w * (w - wce)) - wpi**2 / (w * (w + wci))
agrees(R, rh_sum, ":319", lhs=sp.Symbol("N_RH") ** 2)
si.check(R.subs(ION), rh_sum.subs(ION), unit=1, units=UNITS)
note("Common denominator; with", sp.Eq(wpi**2 * wce, wpe**2 * wci), "the numerator is")
numerator = sp.simplify(((1 - rh_sum) * (w + wci) * (w - wce)).subs(ION))
agrees(numerator, (wpe**2 * (1 + wci / wce)).subs(ION), ":329",
       lhs=(1 - sp.Symbol("N_RH") ** 2) * (w + wci) * (w - wce))
note("Drop the", wci / wce, "correction in the numerator, keep the ion denominators:")
show(sp.Eq(sp.Symbol("N_RH") ** 2, N2_RH))
show(sp.Eq(sp.Symbol("N_LH") ** 2, N2_LH))
M_ratio = sp.Symbol("M", positive=True)  # m_e/m_i
small = {wci: wce * M_ratio, wpi: wpe * sp.sqrt(M_ratio)}
for exact, approx in ((R, N2_RH), (L, N2_LH)):
    error = sp.simplify(exact.subs(ION).subs(m_i, m_e / M_ratio) - approx.subs(small))
    assert sp.simplify(sp.limit(error, M_ratio, 0)) == 0
    assert sp.simplify(sp.diff(error, M_ratio).subs(M_ratio, 0)) != 0  # first order in M
note("The dropped terms are first order in", sp.Eq(M_ratio, m_e / m_i))

# %% Low-frequency Alfvén limit
section("Low-frequency Alfvén limit", "13-finite-temperature-waves.typ:343")
alfven_index = 1 + wpe**2 / (wce * wci)
for N2, name in ((N2_RH, "N_RH"), (N2_LH, "N_LH")):
    show(sp.Eq(sp.Limit(sp.Symbol(name) ** 2, w, 0), sp.limit(N2, w, 0)))
    si.check(sp.limit(N2, w, 0), alfven_index, unit=1, units=UNITS)  # :286, :343
definitions = {wce: e * B0 / m_e, wci: e * B0 / m_i, wpe: sp.sqrt(n0 * e**2 / (eps0 * m_e))}
note("Insert the SI definitions and", sp.Eq(eps0, 1 / (mu0 * c**2)))
ratio = (wce * wci / wpe**2).subs(definitions)
agrees(ratio, eps0 * B0**2 / (n0 * m_i), ":348", lhs=wce * wci / wpe**2)
si.check(ratio, eps0 * B0**2 / (n0 * m_i), unit=1, units=UNITS)
agrees(ratio.subs(eps0, 1 / (mu0 * c**2)), B0**2 / (mu0 * n0 * m_i * c**2), ":349",
       lhs=wce * wci / wpe**2)
alfven = B0 / sp.sqrt(mu0 * n0 * m_i)
lead = (wpe**2 / (wce * wci)).subs(definitions).subs(eps0, 1 / (mu0 * c**2))
note("For", sp.Gt(wpe**2, wce * wci), "the 1 is negligible, with", sp.Eq(v_A, alfven))
to_v_A = {B0: v_A * sp.sqrt(mu0 * n0 * m_i)}
agrees(lead.subs(to_v_A), c**2 / v_A**2, ":353", lhs=sp.Symbol("N") ** 2)
si.check(lead, c**2 / alfven**2, unit=1, units=UNITS)
v_A_frequencies = c * sp.sqrt(wce * wci) / wpe
si.check(v_A_frequencies.subs(definitions).subs(eps0, 1 / (mu0 * c**2)), alfven,
         unit=u.meter / u.second, units=UNITS)  # :289
show(sp.Eq(v_A, v_A_frequencies))
phase = sp.solve(sp.Eq((k * c / w) ** 2, c**2 / alfven**2), w)[0] / k
agrees(phase.subs(to_v_A), v_A, ":356", lhs=w / k)
si.check(phase, alfven, unit=u.meter / u.second, units=UNITS)

# %% Normalized ion-cyclotron and whistler branches
section("Normalized ion-cyclotron and whistler branches", "13-finite-temperature-waves.typ:367")
K, W = sp.symbols("K W", positive=True)  # K = k v_A/omega_ci, W = omega/omega_ci
note("For", sp.Lt(w, wce), "and", sp.Lt(v_A, c), ": keep the leading term in", 1 / wce,
     "; normalize", sp.Eq(K, k * v_A / wci), ",", sp.Eq(W, w / wci))
W_branch = {}
for N2, name in ((N2_RH, "RH"), (N2_LH, "LH")):
    lead = sp.limit((N2 - 1) * wce, wce, sp.oo) / wce
    dispersion = sp.Eq((k * c / w) ** 2, lead)
    normalized = dispersion.subs({k: K * wci / v_A_frequencies, w: W * wci})
    scale = wce * wci / wpe**2
    show(sp.Eq(sp.simplify(normalized.lhs * scale), sp.simplify(normalized.rhs * scale)))
    roots = [r for r in sp.solve(normalized, W) if r.subs(K, 1).is_positive]
    assert len(roots) == 1
    W_branch[name] = show(sp.Eq(sp.Symbol(f"W_{name}"), roots[0])).rhs
assert sp.simplify(W_branch["RH"] - (K**2 + sp.sqrt(K**4 + 4 * K**2)) / 2) == 0
assert sp.simplify(W_branch["LH"] - (sp.sqrt(K**4 + 4 * K**2) - K**2) / 2) == 0
for root in W_branch.values():
    assert sp.limit(root / K, K, 0) == 1  # both start on the Alfvén line W = K
assert sp.limit(W_branch["LH"], K, sp.oo) == 1  # LH approaches the ion cyclotron resonance
note("Both start on the Alfvén line", sp.Eq(W, K), "; LH approaches",
     sp.Eq(sp.Limit(sp.Symbol("W_LH"), K, sp.oo), 1))

# %% Warm species response
section("Warm species response", "13-finite-temperature-waves.typ:498")
q, m_s, n_s, E1, T_s = sp.symbols("q m n E_1 T_s", positive=True)
u1, n1 = sp.symbols("u_1 n_1")


def warm_response(q, m, n, c_s2):
    """1D warm fluid: continuity and momentum with p1 = m c_s^2 n1; returns (u1, n1)."""
    continuity = sp.Eq(-I * w * n1 + I * n * k * u1, 0)
    momentum = sp.Eq(-I * w * m * u1, q * E1 - I * k * m * c_s2 * n1 / n)
    sol = sp.solve([continuity, momentum], [u1, n1], dict=True)[0]
    return continuity, momentum, sol[u1], sol[n1]


note("Adiabatic pressure", sp.Eq(gamma * k_B * T_s * n1 / n_s, m_s * c_se**2 * n1 / n_s), "with",
     sp.Eq(c_se**2, gamma * k_B * T_s / m_s))
si.check(m_s * (gamma * k_B * T_s / m_s), gamma * k_B * T_s)  # :510, :518
continuity, momentum, u1_warm, n1_warm = warm_response(q, m_s, n_s, c_se**2)
show(continuity)
show(momentum)
si.check(n1_warm / n_s, k * u1_warm / w)  # :506
agrees(u1_warm, I * q * w * E1 / (m_s * (w**2 - k**2 * c_se**2)), ":529", lhs=u1)

# %% Warm longitudinal susceptibility
section("Warm longitudinal susceptibility", "13-finite-temperature-waves.typ:535")
note("Current", sp.Eq(sp.Symbol("j"), q * n_s * u1), "in", sp.Eq(sp.Symbol("epsilon") * E1,
                                                                    E1 + I * sp.Symbol("j") / (eps0 * w)))
chi_s = sp.simplify(I / (eps0 * w) * q * n_s * u1_warm / E1)
agrees(chi_s, -(n_s * q**2 / (eps0 * m_s)) / (w**2 - k**2 * c_se**2), ":539", lhs=sp.Symbol("chi_s"))

# %% Warm Langmuir branch
section("Warm Langmuir branch", "13-finite-temperature-waves.typ:547")
w_sq = sp.Symbol("omega^2")
note("Fixed ions")
langmuir = show(sp.Eq(1 - wpe**2 / (w_sq - k**2 * c_se**2), 0))
bohm_gross = sp.solve(langmuir, w_sq)[0]
agrees(bohm_gross, wpe**2 + k**2 * c_se**2, ":551", lhs=w**2)
si.check(bohm_gross, wpe**2 + k**2 * c_se**2, unit=u.second**-2, units=UNITS)
lambda_D_sq = eps0 * k_B * T_e / (n0 * e**2)
c_se_sq = gamma_e * k_B * T_e / m_e
wpe_sq = n0 * e**2 / (eps0 * m_e)
note("With", sp.Eq(c_se**2, c_se_sq), "and", sp.Eq(sp.Symbol("lambda_De") ** 2, lambda_D_sq))
agrees(sp.simplify(c_se_sq / wpe_sq), gamma_e * lambda_D_sq, ":560", lhs=c_se**2 / wpe**2)
si.check(c_se_sq / wpe_sq, gamma_e * lambda_D_sq, unit=u.meter**2, units=UNITS)
lambda_De = sp.Symbol("lambda_De", positive=True)
si.check(bohm_gross.subs({wpe: sp.sqrt(wpe_sq), c_se: sp.sqrt(c_se_sq)}),
         wpe_sq * (1 + gamma_e * k**2 * lambda_D_sq))  # :468 in SI symbols
agrees(bohm_gross.subs(c_se, sp.sqrt(gamma_e) * wpe * lambda_De),
       wpe**2 * (1 + gamma_e * k**2 * lambda_De**2), ":468", lhs=w**2)

# %% Ion-acoustic root
section("Ion-acoustic root", "13-finite-temperature-waves.typ:566")
X = sp.Symbol("X", positive=True)  # X = omega^2
two_species = 1 - wpe**2 / (X - k**2 * c_se**2) - wpi**2 / (X - k**2 * c_si**2)
note("Electrons and ions, with", sp.Eq(X, w**2))
show(sp.Eq(two_species, 0))
note("Multiply by both denominators: a quadratic in", X)
quadratic = sp.expand(sp.numer(sp.together(two_species)))
POLY_LONG = ((X - k**2 * c_se**2) * (X - k**2 * c_si**2)
             - wpe**2 * (X - k**2 * c_si**2) - wpi**2 * (X - k**2 * c_se**2))
agrees(quadratic, POLY_LONG, ":566", lhs=sp.S.Zero)
roots = sp.solve(quadratic, X)
low = min(roots, key=lambda r: r.subs({k: sp.Rational(1, 100), c_se: 1, c_si: 1,
                                       wpe: 3, wpi: 1}).evalf())
note("Small root to order", k**2, ":")
low_k2 = sp.series(low, k, 0, 3).removeO().replace(
    lambda x: x.is_Pow and x.exp == sp.S.Half, lambda x: sp.sqrt(sp.factor(x.base)))
ion_acoustic = k**2 * (wpe**2 * c_si**2 + wpi**2 * c_se**2) / (wpe**2 + wpi**2)
agrees(sp.simplify(low_k2), ion_acoustic, ":485", lhs=sp.Symbol("omega_-") ** 2)
si.check(sp.simplify(low_k2), ion_acoustic, unit=u.second**-2, units=UNITS)
truncated = -(wpe**2 + wpi**2) * X + k**2 * (wpe**2 * c_si**2 + wpi**2 * c_se**2)
si.check(sp.solve(truncated, X)[0], ion_acoustic)  # linear truncation, :574
note("Leading order in", sp.Eq(M_ratio, m_e / m_i), "with", sp.Eq(wpi, wpe * sp.sqrt(M_ratio)))
c_ia_sq = (ion_acoustic / k**2).subs(wpi, wpe * sp.sqrt(M_ratio))
series_M = sp.series(c_ia_sq, M_ratio, 0, 2).removeO()
show(sp.Eq(sp.Symbol("c_ia") ** 2, series_M))
note("Drop", -M_ratio * c_si**2, "; keep", M_ratio * c_se**2, "since", sp.Eq(c_se**2 / c_si**2, 1 / M_ratio),
     "in order of magnitude")
si.check(series_M + M_ratio * c_si**2, c_si**2 + M_ratio * c_se**2)
lead = c_si**2 + M_ratio * c_se**2
speeds = {c_si: sp.sqrt(gamma_i * k_B * T_i / m_i), c_se: sp.sqrt(gamma_e * k_B * T_e / m_e),
          M_ratio: m_e / m_i}
c_ia_stated = gamma_i * k_B * T_i / m_i + gamma_e * k_B * T_e / m_i
agrees(lead.subs(speeds), c_ia_stated, ":585", lhs=sp.Symbol("c_ia") ** 2)
si.check(lead.subs(speeds), c_ia_stated, unit=(u.meter / u.second) ** 2, units=UNITS)
same_gamma = k**2 * c_ia_stated.subs({gamma_i: gamma, gamma_e: gamma})
agrees(same_gamma, k**2 * gamma * k_B * (T_e + T_i) / m_i, ":489", lhs=w**2)
si.check(same_gamma, k**2 * gamma * k_B * (T_e + T_i) / m_i, unit=u.second**-2, units=UNITS)

# %% Worked example: warm Langmuir
section("Worked example: warm Langmuir", "13-finite-temperature-waves.typ:594")
example = {n0: 1e16 / u.meter**3, T_e: 10 * u.electronvolt / u.boltzmann_constant}
note("Input", sp.Eq(n0, example[n0], evaluate=False), ",",
     sp.Eq(k_B * T_e, 10 * u.electronvolt, evaluate=False), ", isothermal", sp.Eq(gamma_e, 1),
     ",", sp.Eq(k * lambda_De, sp.Float(0.8, 2)))
debye = evaluate(lambda_De, sp.sqrt(lambda_D_sq), example, u.meter)
close_to(debye, 2.35e-4, source=":607")
close_to(evaluate(k, 0.8 / lambda_De, {lambda_De: debye * u.meter}, 1 / u.meter),
         3.40e3, source=":608")
ratio = number(sp.sqrt(1 + gamma_e * (k * lambda_De) ** 2), {gamma_e: 1, k: 0.8, lambda_De: 1})
show(sp.Eq(w / wpe, sp.Float(ratio, 3)))
close_to(ratio, 1.28, source=":609")

# %% Warm upper hybrid
section("Warm upper hybrid", "13-finite-temperature-waves.typ:723")
Om_e, q_e = sp.symbols("Omega_e q_e", real=True)
n1, ux, uy = sp.symbols("n_1 u_x u_y")
note("Fixed ions;", sp.Eq(sp.Symbol("k"), k * sp.Symbol("e_x")), ",",
     sp.Eq(sp.Symbol("E"), Ex * sp.Symbol("e_x")), ",", sp.Eq(sp.Symbol("B"), B0 * sp.Symbol("e_z")))
continuity = show(sp.Eq(-I * w * n1 + I * k * n0 * ux, 0))
mom_x = show(sp.Eq(-I * w * ux, (q_e / m_e) * Ex + Om_e * uy - I * k * c_se**2 * n1 / n0))
mom_y = show(sp.Eq(-I * w * uy, -Om_e * ux))
lorentz = Om_e * sp.Matrix([ux, uy, 0]).cross(sp.Matrix([0, 0, 1]))
assert sp.expand(mom_x.rhs - ((q_e / m_e) * Ex + lorentz[0] - I * k * c_se**2 * n1 / n0)) == 0
assert sp.expand(mom_y.rhs - lorentz[1]) == 0
sol = sp.solve([continuity, mom_x, mom_y], [n1, ux, uy], dict=True)[0]
agrees(sp.simplify(sol[uy] / sol[ux]), -I * Om_e / w, ":741", lhs=uy / ux)
denominator = m_e * (w**2 - Om_e**2 - k**2 * c_se**2)
agrees(sol[ux], I * q_e * w * Ex / denominator, ":751", lhs=ux)
agrees(sol[n1], I * n0 * q_e * k * Ex / denominator, ":756", lhs=n1)
poisson = show(sp.Eq(I * k * Ex, q_e * n1 / eps0))
response = sp.simplify(q_e * sol[n1] / (eps0 * I * k * Ex))
wpe_sq = n0 * q_e**2 / (eps0 * m_e)
agrees(response, wpe_sq / (w**2 - Om_e**2 - k**2 * c_se**2), ":767", lhs=sp.S.One)
note("All four equations as one system:")
fields = [n1, ux, uy, Ex]
M_uh = plane_wave_matrix([continuity, mom_x, mom_y, poisson], fields)
show(sp.Eq(matmul(M_uh, fields), sp.ImmutableMatrix(sp.zeros(4, 1)), evaluate=False))
determinant = sp.factor(M_uh.det())
show(sp.Eq(determinant, 0))
upper_hybrid = sp.solve(sp.Eq(response.subs(w, sp.sqrt(w_sq)), 1), w_sq)[0]
assert sp.simplify(determinant.subs(w, sp.sqrt(upper_hybrid))) == 0
agrees(upper_hybrid, wpe_sq + Om_e**2 + k**2 * c_se**2, ":773", lhs=w**2)


def mhd_matrix(kx, kz):
    """Linear ideal MHD for u with p1 = v_s^2 rho1, B0 = B0 e_z, B0^2 = v_A^2 mu0 rho0."""
    vel = sp.Matrix(sp.symbols("u_x u_y u_z"))
    k_vec, B_vec = sp.Matrix([kx, 0, kz]), sp.Matrix([0, 0, B0])
    rho1 = rho0 * k_vec.dot(vel) / w  # continuity
    B1 = -k_vec.cross(vel.cross(B_vec)) / w  # -i w B1 = i k x (u x B0)
    force = -I * k_vec * v_s**2 * rho1 + (I * k_vec.cross(B1)).cross(B_vec) / mu0
    eqs = (-I * w * rho0 * vel - force).subs(B0, sp.sqrt(v_A**2 * mu0 * rho0))
    return sp.ImmutableMatrix(eqs.jacobian(vel)), rho1, B1, vel


# %% Perpendicular magnetosonic wave
section("Perpendicular magnetosonic wave", "13-finite-temperature-waves.typ:794")
note("Ideal MHD,", sp.Eq(sp.Symbol("p_1"), v_s**2 * sp.Symbol("rho_1")), ",",
     sp.Eq(v_A, B0 / sp.sqrt(mu0 * rho0)), "; k across", B0)
A, rho1, B1, vel = mhd_matrix(k, 0)
ux = vel[0]
agrees(rho1, rho0 * k * ux / w, ":795", lhs=sp.Symbol("rho_1"))
agrees(B1[2], B0 * k * ux / w, ":800", lhs=sp.Symbol("B_1z"))
show(sp.Eq(matmul(A, vel), sp.ImmutableMatrix(sp.zeros(3, 1)), evaluate=False))
row = (-I * w * rho0 * ux + I * k * v_s**2 * (rho0 * k * ux / w)
       + I * k * B0 * (B0 * k * ux / w) / mu0)
si.check(A[0, 0] * ux, row.subs(B0, sp.sqrt(v_A**2 * mu0 * rho0)))  # :804
note("Only the x row couples to compression:", sp.Eq(A[0, 0], 0))
magnetosonic = sp.solve(A[0, 0].subs(w, sp.sqrt(w_sq)), w_sq)[0]
alfven = B0 / sp.sqrt(mu0 * rho0)
stated = k**2 * (v_s**2 + B0**2 / (mu0 * rho0))
agrees(magnetosonic, k**2 * (v_s**2 + v_A**2), ":810", lhs=w**2)
si.check(magnetosonic.subs(v_A, alfven), stated, unit=u.second**-2, units=UNITS)  # :809
si.check(stated, k**2 * (v_s**2 + alfven**2))
v_m = sp.sqrt(magnetosonic.subs(v_A, alfven)) / k
si.check(v_m, sp.sqrt(alfven**2 + v_s**2), unit=u.meter / u.second, units=UNITS)  # :814
show(sp.Eq(sp.Symbol("v_m"), sp.sqrt(magnetosonic) / k))
rho = sp.Symbol("rho", positive=True)
note("Sound speed from", sp.Eq(sp.Symbol("p"), p0 * (rho / rho0) ** gamma))
sound_sq = sp.diff(p0 * (rho / rho0) ** gamma, rho).subs(rho, rho0)
agrees(sound_sq, gamma * p0 / rho0, ":696", lhs=v_s**2)
si.check(sound_sq, gamma * p0 / rho0, unit=(u.meter / u.second) ** 2, units=UNITS)

# %% Shear Alfvén wave
section("Shear Alfvén wave", "13-finite-temperature-waves.typ:822")
A, rho1, _, vel = mhd_matrix(0, k_par)
note("k along", B0)
show(sp.Eq(matmul(A, vel), sp.ImmutableMatrix(sp.zeros(3, 1)), evaluate=False))
assert sp.simplify(sp.diff(rho1, vel[1])) == 0
note("Transverse", vel[1], "compresses nothing; only magnetic tension restores it")
shear = sp.solve(A[1, 1].subs(w, sp.sqrt(w_sq)), w_sq)[0]
agrees(shear, k_par**2 * v_A**2, ":826", lhs=w**2)
f = sp.exp(I * (k_par * z - w * t))
u_y = sp.Function("u_y")(z, t)
show(sp.Eq(sp.Derivative(u_y, t, 2), v_A**2 * sp.Derivative(u_y, z, 2)))
wave = sp.simplify((sp.diff(f, t, 2) - v_A**2 * sp.diff(f, z, 2)) / f)
si.check(sp.solve(wave.subs(w, sp.sqrt(w_sq)), w_sq)[0], shear)  # :822, same relation

# %% Animation speeds
section("Animation speeds", "13-finite-temperature-waves.typ:842")
note("Units", sp.Symbol("L_0") / sp.Symbol("t_0"), ":", sp.Eq(v_s, sp.Rational(6, 10)), ",",
     sp.Eq(v_A, 1, evaluate=False))
agrees((v_A**2 + v_s**2).subs({v_s: sp.Rational(6, 10), v_A: 1}), sp.Rational(136, 100), ":843",
       lhs=sp.Symbol("v_m") ** 2)

# %% Worked example: MHD speeds
section("Worked example: MHD speeds", "13-finite-temperature-waves.typ:853")
n_val = 1e16 / u.meter**3
example = {rho0: n_val * PROTON_MASS, B0: 1e-2 * u.tesla, gamma: 1,
           p0: 2 * n_val * 10 * u.electronvolt}
note("Hydrogen,", sp.Eq(n0, n_val, evaluate=False), ",", sp.Eq(B0, example[B0], evaluate=False),
     ", isothermal, ", sp.Eq(p0, n0 * k_B * (T_e + T_i)), "with 10 eV each")
v_A_value = evaluate(v_A, alfven, example, u.meter / u.second)
close_to(v_A_value, 2.18e6, source=":862")
v_s_value = evaluate(v_s, sp.sqrt(gamma * p0 / rho0), example, u.meter / u.second)
close_to(v_s_value, 4.38e4, source=":863")
v_m_value = evaluate(sp.Symbol("v_m"), sp.sqrt(alfven**2 + gamma * p0 / rho0), example,
                     u.meter / u.second)
close_to(v_m_value, 2.18e6, source=":864")
note("At", sp.Eq(k, 1e-3 / u.meter), ":")
close_to(evaluate(w, k * v_A, {k: 1e-3 / u.meter, v_A: v_A_value * u.meter / u.second},
                  1 / u.second), 2.18e3, source=":866")
close_to(evaluate(w, k * sp.Symbol("v_m"), {k: 1e-3 / u.meter,
                                            sp.Symbol("v_m"): v_m_value * u.meter / u.second},
                  1 / u.second), 2.18e3, source=":867")

# %% Cold limits
section("Cold limits", "13-finite-temperature-waves.typ:971")
agrees(sp.limit(m * (1 + I * nu / w), nu, 0), m, ":971", lhs=sp.Limit(m_eff, nu, 0))
T_s = sp.Symbol("T_s", positive=True)
agrees(sp.limit(w**2 - k**2 * gamma * k_B * T_s / m, T_s, 0), w**2, ":996",
       lhs=sp.Limit(w**2 - k**2 * gamma * k_B * T_s / m, T_s, 0))
note("Infinitely heavy ions recover the electron tensor:")
eps = dielectric([electron(), ion()]).subs(ION)
fixed_ions = dielectric([electron()])
for a, b in ((0, 0), (0, 1), (2, 2)):
    si.check(sp.limit(eps[a, b], m_i, sp.oo), fixed_ions[a, b])  # :986
show(sp.Eq(sp.Limit(S, m_i, sp.oo), sp.simplify(sp.limit(eps[0, 0], m_i, sp.oo))))

# %% Worked example: mass ratio
section("Worked example: mass ratio", "13-finite-temperature-waves.typ:1038")
mass_ratio = number(m_e / m_i, {m_i: PROTON_MASS})
show(sp.Eq(M_ratio, sp.Float(mass_ratio, 3)))
close_to(mass_ratio, 5.45e-4, source=":1038")

# %% Plot: normalized RH (whistler) and LH (ion cyclotron) branches
K_grid = np.linspace(0, 2.4, 300)
rh, lh = (sp.lambdify(K, W_branch[name], "numpy") for name in ("RH", "LH"))
fig, ax = figure(4.2, 2.8)
ax.plot(K_grid, K_grid, color=GRAY, ls=":", lw=1.2)
ax.axhline(1, color=GRAY, lw=0.8, ls="-.")
ax.plot(K_grid, rh(K_grid), color=BLUE)
ax.plot(K_grid, lh(K_grid), color=ORANGE, ls="--")
label(ax, 1.0, rh(1.0), "RH (whistler)", BLUE, ha="right")
label(ax, 2.38, lh(2.38) - 0.25, "LH (ion cyclotron)", ORANGE, ha="right", va="top")
label(ax, 1.95, 1.65, r"$\mathrm{Alfv\acute{e}n}$ $W=K$", GRAY, va="top")
label(ax, 2.38, 1.03, "resonance $\\omega=\\omega_{ci}$", GRAY, ha="right")
ax.set(xlim=(0, 2.4), ylim=(0, 3), xticks=[0, 1, 2], yticks=[0, 1, 2, 3],
       xlabel=r"$K=kv_A/\omega_{ci}$ [1]", ylabel=r"$W=\omega/\omega_{ci}$ [1]")
save(fig, "ion-wave-branches")

# %% Plot: both roots of the two-species quadratic, one panel each
# Isothermal electrons (c_se = omega_pe lambda_De), cold ions (c_si = 0),
# m_i/m_e = 1836; K = k lambda_De. Left: Langmuir root in omega_pe; right:
# ion-acoustic root in omega_pi = omega_pe sqrt(m_e/m_i).
PANEL = (2.6, 3.0)  # one panel of a side-by-side pair
mass = sp.Rational(1, 1836)
long_quadratic = sp.expand(POLY_LONG.subs({c_si: 0, c_se: wpe, wpi: wpe * sp.sqrt(mass)})
                           .subs({k: K, X: W**2 * wpe**2}) / wpe**4)  # lambda_De = 1
roots_W2 = [sp.lambdify(K, r, "numpy") for r in sp.solve(long_quadratic, W**2)]
langmuir_W2, acoustic_W2 = sorted(roots_W2, key=lambda f: -f(1.0))
langmuir = lambda K: np.sqrt(langmuir_W2(K))  # noqa: E731
acoustic = lambda K: np.sqrt(np.clip(acoustic_W2(K), 0, None))  # noqa: E731  (rounding at K = 0)
K_grid = np.linspace(0, 3, 300)

fig, ax = figure(*PANEL)
ax.plot(K_grid, K_grid, color=GRAY, ls=":", lw=1.2)
ax.plot(K_grid, langmuir(K_grid), color=BLUE)
label(ax, 0.1, 2.75, "Langmuir\n(Bohm-Gross)", BLUE, va="top")
label(ax, 1.6, 1.1, "$\\omega=kc_{se}$", GRAY, va="top")
ax.set(xlim=(0, 3), ylim=(0, 3.5), xticks=[0, 1, 2, 3], yticks=[0, 1, 2, 3],
       xlabel=r"$K=k\lambda_{De}$ [1]", ylabel=r"$\omega/\omega_{pe}$ [1]")
save(fig, "warm-langmuir-branch")

fig, ax = figure(*PANEL)
ax.plot(K_grid, K_grid, color=GRAY, ls=":", lw=1.2)
ax.axhline(1, color=GRAY, lw=0.8, ls="-.")
ax.plot(K_grid, acoustic(K_grid) / float(sp.sqrt(mass)), color=ORANGE, ls="--")
label(ax, 2.95, 0.8, "ion acoustic", ORANGE, ha="right", va="top")
label(ax, 2.95, 1.04, "$\\omega=\\omega_{pi}$", GRAY, ha="right")
label(ax, 1.35, 1.6, "$\\omega=kc_s$", GRAY, ha="right")
ax.set(xlim=(0, 3), ylim=(0, 1.75), xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1, 1.5],
       xlabel=r"$K=k\lambda_{De}$ [1]", ylabel=r"$\omega/\omega_{pi}$ [1]")
save(fig, "ion-acoustic-branch")

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 13 · Finite-temperature waves")
