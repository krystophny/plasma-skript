# Chapter 15 · Sheaths and probes (src/chapters/15-sheaths-probes.typ)
#
# Maxwellian wall fluxes, the Bohm sheath (Poisson equation, first integral,
# Bohm criterion), Child-Langmuir sheaths, the floating potential and the
# Langmuir probe characteristic. `python ch15_sheaths_probes.py` prints every step.

# %% Setup
import mpmath as mp
import numpy as np
import sympy as sp
from sympy.physics import units as u

import si
from notebook import PROTON_MASS, agrees, close_to, evaluate, note, report, section, show
from si import BLUE, GRAY, ORANGE, figure, label, save
from waves import number

e, m_e, m_i, eps0, k_B = sp.symbols("e m_e m_i epsilon_0 k_B", positive=True)
n_s, n0, T_s, T_e, m_s = sp.symbols("n_s n_0 T_s T_e m_s", positive=True)
vx, vy, vz, v = sp.symbols("v_x v_y v_z v", real=True)
eta, M, xi, lambda_D = sp.symbols("eta M xi lambda_D", positive=True)
V, s, d_w, C, Gamma_i, V_w = sp.symbols("V s d C Gamma_i V_w", positive=True)
phi, phi_w, phi_p, phi_pl = sp.symbols("phi phi_w phi_p phi_pl", real=True)
A, Gamma_e0 = sp.symbols("A Gamma_e0", positive=True)
Gamma_s0 = sp.Symbol("Gamma_s0")

# SI units of the local symbols, for si.check(..., unit=...).
UNITS = {n_s: u.meter**-3, n0: u.meter**-3, T_s: u.kelvin, T_e: u.kelvin, m_s: u.kilogram,
         V: u.volt, V_w: u.volt, d_w: u.meter, s: u.meter, Gamma_i: u.meter**-2 / u.second,
         Gamma_e0: u.meter**-2 / u.second, A: u.meter**2, phi: u.volt, phi_w: u.volt,
         phi_p: u.volt, phi_pl: u.volt, lambda_D: u.meter}
HYDROGEN = {m_i: PROTON_MASS}
milliampere = u.Quantity("milliampere", abbrev="mA")
milliampere.set_global_relative_scale_factor(sp.Rational(1, 1000), u.ampere)


def maxwellian(n, T, m):
    """Isotropic 3D Maxwellian of density n, temperature T, mass m."""
    return n * (m / (2 * sp.pi * k_B * T)) ** sp.Rational(3, 2) * sp.exp(
        -m * (vx**2 + vy**2 + vz**2) / (2 * k_B * T))


def half_space_flux(n, T, m, v_min=0):
    """Gamma = integral of v_z f over v_z > v_min (integrated, not quoted)."""
    return sp.integrate(vz * maxwellian(n, T, m),
                        (vx, -sp.oo, sp.oo), (vy, -sp.oo, sp.oo), (vz, v_min, sp.oo))


# %% Maxwellian half-space flux
section("Maxwellian half-space flux", "15-sheaths-probes.typ:94")
show(sp.Eq(sp.Symbol("f_s"), maxwellian(n_s, T_s, m_s)))
show(sp.Eq(Gamma_s0, sp.Integral(vz * sp.Symbol("f_s"), (vx, -sp.oo, sp.oo), (vy, -sp.oo, sp.oo),
                                 (vz, 0, sp.oo))))
note("Tangential directions: Gaussian integrals")
gauss = sp.integrate(sp.exp(-m_s * vx**2 / (2 * k_B * T_s)), (vx, -sp.oo, sp.oo))
agrees(gauss, sp.sqrt(2 * sp.pi * k_B * T_s / m_s), ":110",
       lhs=sp.Integral(sp.exp(-m_s * vx**2 / (2 * k_B * T_s)), (vx, -sp.oo, sp.oo)))
a_n = sp.Symbol("a", positive=True)
note("Normal direction, only", sp.Gt(vz, 0), ":")
agrees(sp.integrate(v * sp.exp(-a_n * v**2), (v, 0, sp.oo)), 1 / (2 * a_n), ":122",
       lhs=sp.Integral(v * sp.exp(-a_n * v**2), (v, 0, sp.oo)))
flux = half_space_flux(n_s, T_s, m_s)
agrees(flux, n_s * sp.sqrt(k_B * T_s / (2 * sp.pi * m_s)), ":127", lhs=Gamma_s0)
si.check(flux, n_s * sp.sqrt(k_B * T_s / (2 * sp.pi * m_s)), unit=u.meter**-2 / u.second, units=UNITS)
v_th = sp.Symbol("v_th")
note("With", sp.Eq(v_th, sp.sqrt(2 * k_B * T_s / m_s)), ":")
agrees(flux, (n_s * v_th / (2 * sp.sqrt(sp.pi))).subs(v_th, sp.sqrt(2 * k_B * T_s / m_s)), ":131",
       lhs=Gamma_s0)
show(sp.Eq(Gamma_s0, n_s * v_th / (2 * sp.sqrt(sp.pi))))

# %% Mean speed form of the flux
section("Mean speed form of the flux", "15-sheaths-probes.typ:135")
w = sp.Symbol("w", positive=True)
speed_pdf = 4 * sp.pi * w**2 * (m_s / (2 * sp.pi * k_B * T_s)) ** sp.Rational(3, 2) * sp.exp(
    -m_s * w**2 / (2 * k_B * T_s))
v_mean = sp.integrate(w * speed_pdf, (w, 0, sp.oo))
agrees(v_mean, sp.sqrt(8 * k_B * T_s / (sp.pi * m_s)), ":135", lhs=sp.Integral(w * speed_pdf, (w, 0, sp.oo)))
si.check(v_mean, sp.sqrt(8 * k_B * T_s / (sp.pi * m_s)), unit=u.meter / u.second, units=UNITS)
agrees(flux, n_s * v_mean / 4, ":139", lhs=Gamma_s0)
show(sp.Eq(Gamma_s0, n_s * sp.Symbol("v_mean") / 4))

# %% Electron to ion flux ratio
section("Electron to ion flux ratio", "15-sheaths-probes.typ:83")
note("Equal density and temperature:")
agrees(half_space_flux(n_s, T_s, m_e) / half_space_flux(n_s, T_s, m_i), sp.sqrt(m_i / m_e), ":83",
       lhs=sp.Symbol("Gamma_e0") / sp.Symbol("Gamma_i0"))
note("Hydrogen,", sp.Eq(m_i / m_e, 1836))
ratio = number(sp.sqrt(m_i / m_e).subs(m_i, 1836 * m_e))
show(sp.Eq(sp.Symbol("Gamma_e0") / sp.Symbol("Gamma_i0"), sp.Float(ratio, 3)))
close_to(ratio, 42.8, rtol=2e-3, source=":152")

# %% Boltzmann electrons
section("Boltzmann electrons", "15-sheaths-probes.typ:278")
n_e = sp.Function("n_e")
note("Isothermal electrons, pressure against the electric force:")
balance = show(sp.Eq(k_B * T_e * n_e(phi).diff(phi), e * n_e(phi)))
boltzmann = sp.dsolve(balance, n_e(phi), ics={n_e(0): n0}).rhs
agrees(boltzmann, n0 * sp.exp(e * phi / (k_B * T_e)), ":278", lhs=n_e(phi))
note("Normalized potential", sp.Eq(eta, -e * phi / (k_B * T_e)))
N_E = sp.exp(-eta)  # n_e/n_0
agrees(boltzmann.subs(phi, -k_B * T_e * eta / e), n0 * N_E, ":278", lhs=sp.Symbol("n_e"))

# %% Cold ion density in the sheath
section("Cold ion density in the sheath", "15-sheaths-probes.typ:305")
u_s, u_i = sp.symbols("u_s u_i", positive=True)
x = sp.Symbol("x")
u_x, phi_x = sp.Function("u_i")(x), sp.Function("phi")(x)
momentum = show(sp.Eq(m_i * u_x * u_x.diff(x) + e * phi_x.diff(x), 0))
assert sp.simplify(sp.diff(m_i * u_x**2 / 2 + e * phi_x, x) - momentum.lhs) == 0  # :292
note("is a total derivative: energy conservation from the edge, where", sp.Eq(phi, 0, evaluate=False))
energy = show(sp.Eq(m_i * u_i**2 / 2 + e * phi, m_i * u_s**2 / 2))
u_i_sq = sp.solve(energy.subs(phi, -k_B * T_e * eta / e), u_i**2)[0]
agrees(u_i_sq, u_s**2 + 2 * k_B * T_e * eta / m_i, ":300", lhs=u_i**2)
c_s = sp.sqrt(k_B * T_e / m_i)
note("Edge speed", sp.Eq(u_s, M * sp.Symbol("c_s")), "with", sp.Eq(sp.Symbol("c_s"), c_s))
agrees(u_i_sq.subs(u_s, M * c_s), c_s**2 * (M**2 + 2 * eta), ":301", lhs=u_i**2)
note("Flux conservation", sp.Eq(sp.Symbol("n_i") * u_i, sp.Symbol("n_s") * u_s))
N_I = M / sp.sqrt(M**2 + 2 * eta)  # n_i/n_s
ion_ratio = sp.simplify((u_s / sp.sqrt(u_i_sq)).subs(u_s, M * c_s))
agrees(ion_ratio, N_I, ":305", lhs=sp.Symbol("n_i") / sp.Symbol("n_s"))
agrees(ion_ratio.subs(M, sp.Rational(3, 2)), sp.Rational(3, 2) / sp.sqrt(sp.Rational(9, 4) + 2 * eta),
       ":756", lhs=sp.Symbol("n_i") / n0)

# %% Normalized sheath equation
section("Normalized sheath equation", "15-sheaths-probes.typ:323")
eta_xi = sp.Function("eta")(xi)
n_i_sym, n_e_sym = sp.symbols("n_i n_e", positive=True)
note("Poisson in", sp.Eq(xi, x / lambda_D), "with", sp.Eq(phi, -k_B * T_e * eta / e))
phi_xi = -(k_B * T_e / e) * eta_xi
laplacian = -sp.diff(phi_xi, xi, 2) / lambda_D**2  # -d^2 phi/dx^2
si.check(sp.simplify(-laplacian), -(k_B * T_e / (e * lambda_D**2)) * eta_xi.diff(xi, 2))  # :318
poisson = show(sp.Eq(laplacian, e * (n_i_sym - n_e_sym) / eps0))
note("Insert", sp.Eq(lambda_D**2, eps0 * k_B * T_e / (n0 * e**2)))
normalized = sp.expand(sp.solve(poisson.subs(lambda_D, sp.sqrt(eps0 * k_B * T_e / (n0 * e**2))),
                                eta_xi.diff(xi, 2))[0])
agrees(normalized, n_i_sym / n0 - n_e_sym / n0, ":323", lhs=eta_xi.diff(xi, 2))
note("Boltzmann electrons and flux-conserving cold ions,", sp.Eq(n0, sp.Symbol("n_s")), ":")
SHEATH_RHS = sp.simplify(normalized.subs({n_i_sym: n0 * ion_ratio, n_e_sym: n0 * N_E}))
agrees(SHEATH_RHS, N_I - N_E, ":324", lhs=eta_xi.diff(xi, 2))

# %% Sheath first integral
section("Sheath first integral (Sagdeev potential)", "15-sheaths-probes.typ:324")
note("Multiply by", eta_xi.diff(xi), "and integrate from the edge, where", sp.Eq(eta, 0, evaluate=False),
     "and", sp.Eq(eta_xi.diff(xi), 0))
h = sp.Symbol("h", positive=True)
sagdeev = sp.integrate(SHEATH_RHS.subs(eta, h), (h, 0, eta))
SAGDEEV = M * (sp.sqrt(M**2 + 2 * eta) - M) + sp.exp(-eta) - 1
agrees(sagdeev, SAGDEEV, ":324", lhs=eta_xi.diff(xi) ** 2 / 2)
assert sp.simplify(sp.diff(SAGDEEV, eta) - SHEATH_RHS) == 0 and SAGDEEV.subs(eta, 0) == 0
note("Near the edge; a real", eta_xi.diff(xi), "needs a non-negative coefficient:")
agrees(sp.series(SAGDEEV, eta, 0, 3).removeO(), (1 - M**-2) * eta**2 / 2, ":330",
       lhs=eta_xi.diff(xi) ** 2 / 2)
note("At", sp.Eq(M, 1, evaluate=False), "the leading term is cubic and positive:")
agrees(sp.series(SAGDEEV.subs(M, 1), eta, 0, 4).removeO(), eta**3 / 3, ":324",
       lhs=eta_xi.diff(xi) ** 2 / 2)

# %% Bohm criterion
section("Bohm criterion", "15-sheaths-probes.typ:337")
note("Expand the ion density for small", eta)
agrees(sp.series(N_I, eta, 0, 2).removeO(), 1 - eta / M**2, ":331", lhs=N_I)
linear = sp.factor(sp.series(SHEATH_RHS, eta, 0, 2).removeO())
agrees(linear, (1 - M**-2) * eta, ":337", lhs=eta_xi.diff(xi, 2))
note("A monotone potential needs", sp.Ge(1 - M**-2, 0), ":")
bohm = sp.solve_univariate_inequality(1 - M**-2 >= 0, M, relational=False)
assert bohm.intersect(sp.Interval(0, sp.oo)) == sp.Interval(1, sp.oo)  # :259
show(sp.Ge(M, 1))

# %% Child-Langmuir: ion density and Poisson
section("Child-Langmuir: ion density and Poisson", "15-sheaths-probes.typ:357")
note("Ions start at rest; potential drop", sp.Eq(V, -phi), ", no electrons")
speed = sp.solve(sp.Eq(m_i * u_i**2 / 2, e * V), u_i)[0]
agrees(speed, sp.sqrt(2 * e * V / m_i), ":357", lhs=u_i)
si.check(speed, sp.sqrt(2 * e * V / m_i), unit=u.meter / u.second, units=UNITS)
ion_density = Gamma_i / speed
agrees(ion_density, Gamma_i * sp.sqrt(m_i / (2 * e * V)), ":361", lhs=sp.Symbol("n_i"))
si.check(ion_density, Gamma_i * sp.sqrt(m_i / (2 * e * V)), unit=u.meter**-3, units=UNITS)
C_stated = Gamma_i / eps0 * sp.sqrt(e * m_i / 2)
V_x = sp.Function("V")(x)
show(sp.Eq(V_x.diff(x, 2), e * sp.Symbol("n_i") / eps0))
agrees(e * ion_density / eps0, C_stated * V ** sp.Rational(-1, 2), ":366", lhs=V_x.diff(x, 2))
si.check(e * ion_density / eps0, C_stated * V ** sp.Rational(-1, 2), unit=u.volt / u.meter**2,
         units=UNITS)
note("Write", sp.Eq(C, C_stated), "(:368)")

# %% Child-Langmuir profile
section("Child-Langmuir profile", "15-sheaths-probes.typ:372")
V_s = sp.Function("V")(s)
show(sp.Eq(V_s.diff(s, 2), C / sp.sqrt(V_s)))
note("Multiply by", V_s.diff(s), "; first integral with", sp.Eq(V_s.subs(s, 0), 0), "and zero field at the edge:")
first_integral = V_s.diff(s) ** 2 / 2 - 2 * C * sp.sqrt(V_s)
assert sp.simplify(sp.diff(first_integral, s).subs(V_s.diff(s, 2), C / sp.sqrt(V_s))) == 0
show(sp.Eq(first_integral, 0))
slope = sp.sqrt(4 * C * sp.sqrt(V))
agrees(slope / V ** sp.Rational(1, 4), 2 * sp.sqrt(C), ":383", lhs=V_s.diff(s) / V_s ** sp.Rational(1, 4))
W = sp.Symbol("W", positive=True)
separated = sp.integrate(W ** sp.Rational(-1, 4), (W, 0, V))
agrees(separated, sp.Rational(4, 3) * V ** sp.Rational(3, 4), ":387",
       lhs=sp.Integral(W ** sp.Rational(-1, 4), (W, 0, V)))
show(sp.Eq(separated, 2 * sp.sqrt(C) * s))
profile = sp.solve(sp.Eq(separated, 2 * sp.sqrt(C) * s), V)[0]
child = (9 * C / 4) ** sp.Rational(2, 3) * s ** sp.Rational(4, 3)
agrees(profile, sp.Mul(sp.Pow(9 * C / 4, sp.Rational(2, 3), evaluate=False), s ** sp.Rational(4, 3),
                       evaluate=False), ":391", lhs=V_s)
assert sp.simplify(sp.diff(child, s, 2) - C / sp.sqrt(child)) == 0  # solves the ODE
assert child.subs(s, 0) == 0 and sp.diff(child, s).subs(s, 0) == 0  # edge conditions
si.check(sp.diff(child, s) ** 2 / 2, 2 * C * sp.sqrt(child))  # :377

# %% Child-Langmuir current
section("Child-Langmuir current", "15-sheaths-probes.typ:396")
note("At the wall,", sp.Eq(s, d_w, evaluate=False), ",", sp.Eq(V, V_w, evaluate=False))
wall = sp.expand_power_base(profile.subs(s, d_w) ** sp.Rational(3, 2), force=True)
agrees(wall, 9 * C / 4 * d_w**2, ":396", lhs=V_w ** sp.Rational(3, 2))
J_i = sp.Symbol("J_i")
current = e * sp.solve(sp.Eq(V_w ** sp.Rational(3, 2), sp.Rational(9, 4) * C_stated * d_w**2), Gamma_i)[0]
child_langmuir = 4 * eps0 / 9 * sp.sqrt(2 * e / m_i) * V_w ** sp.Rational(3, 2) / d_w**2
agrees(current, child_langmuir, ":401", lhs=J_i)
si.check(current, child_langmuir, unit=u.ampere / u.meter**2, units=UNITS)

# %% Worked example: sheath edge at 10 eV
section("Worked example: sheath edge at 10 eV", "15-sheaths-probes.typ:409")
example = {n0: 1e16 / u.meter**3, T_e: 10 * u.electronvolt / u.boltzmann_constant, M: 1.5, **HYDROGEN}
note("Hydrogen,", sp.Eq(n0, example[n0], evaluate=False), ",",
     sp.Eq(k_B * T_e, 10 * u.electronvolt, evaluate=False), ",", sp.Eq(M, sp.Float(1.5, 2)))
lambda_D_sq = eps0 * k_B * T_e / (n0 * e**2)
close_to(evaluate(lambda_D, sp.sqrt(lambda_D_sq), example, u.meter), 2.35e-4, source=":421")
close_to(evaluate(sp.Symbol("c_s"), c_s, example, u.meter / u.second), 3.09e4, source=":422")
close_to(evaluate(u_s, M * c_s, example, u.meter / u.second), 4.64e4, source=":423")
close_to(evaluate(Gamma_i, n0 * M * c_s, example, 1 / (u.meter**2 * u.second)), 4.64e20, source=":424")
note("The same with the rounded constants of the script,", sp.Eq(e, sp.Float(1.602e-19, 4) * u.coulomb),
     ",", sp.Eq(m_i, sp.Float(1.673e-27, 4) * u.kilogram))
printed = {**example, e: 1.602e-19 * u.coulomb, m_i: 1.673e-27 * u.kilogram}
close_to(number(sp.sqrt(lambda_D_sq) / u.meter, printed), 2.35e-4, source=":421")
close_to(number(c_s * u.second / u.meter, printed), 3.09e4, source=":422")

# %% Boltzmann transmission
section("Boltzmann transmission", "15-sheaths-probes.typ:538")
V_b = sp.Symbol("V_b", positive=True)  # barrier height -phi_w
note("Only electrons with", sp.Gt(m_e * vz**2 / 2, e * V_b), "reach the wall:")
v_min = sp.sqrt(2 * e * V_b / m_e)
show(sp.Eq(sp.Symbol("v_min"), v_min))
transmitted = half_space_flux(n0, T_e, m_e, v_min)
unretarded = half_space_flux(n0, T_e, m_e)
agrees(transmitted, unretarded * sp.exp(-e * V_b / (k_B * T_e)), ":538", lhs=sp.Symbol("Gamma_e"))
agrees(sp.simplify(transmitted.subs(V_b, -phi_w) / unretarded), sp.exp(e * phi_w / (k_B * T_e)), ":539",
       lhs=sp.Symbol("Gamma_e") / Gamma_e0)

# %% Floating potential
section("Floating potential", "15-sheaths-probes.typ:547")
J = show(sp.Eq(sp.Symbol("J"), e * Gamma_i - e * Gamma_e0 * sp.exp(e * phi_w / (k_B * T_e)))).rhs
phi_f = sp.Symbol("phi_f")
floating = sp.expand_log(sp.solve(sp.Eq(J, 0), phi_w)[0], force=True)
agrees(floating, k_B * T_e / e * sp.log(Gamma_i / Gamma_e0), ":560", lhs=phi_f)
si.check(floating, k_B * T_e / e * sp.log(Gamma_i / Gamma_e0), unit=u.volt, units=UNITS)
note("Bohm ions and unretarded Maxwellian electrons at the edge:")
bohm_flux = n0 * sp.sqrt(k_B * T_e / m_i)  # :565
show(sp.Eq(Gamma_i, bohm_flux))
agrees(unretarded, n0 * sp.sqrt(k_B * T_e / (2 * sp.pi * m_e)), ":566", lhs=Gamma_e0)
FLUX_RATIO = sp.sqrt(2 * sp.pi * m_e / m_i)
agrees(sp.simplify(bohm_flux / unretarded), FLUX_RATIO, ":566", lhs=Gamma_i / Gamma_e0)
two_logs = sp.Mul(k_B * T_e / (2 * e), sp.log(sp.simplify((bohm_flux / unretarded) ** 2)), evaluate=False)
si.check(sp.expand_log(two_logs, force=True),
         sp.expand_log(floating.subs({Gamma_i: bohm_flux, Gamma_e0: unretarded}), force=True))
stated = k_B * T_e / (2 * e) * sp.log(2 * sp.pi * m_e / m_i)
agrees(sp.expand_log(two_logs, force=True), stated, ":570", lhs=phi_f)
si.check(sp.expand_log(two_logs, force=True), sp.expand_log(stated, force=True), unit=u.volt, units=UNITS)

# %% Hydrogen floating coefficient
section("Hydrogen floating coefficient", "15-sheaths-probes.typ:572")
mass_term = number(2 * sp.pi * m_e / m_i, HYDROGEN)
show(sp.Eq(2 * sp.pi * m_e / m_i, sp.Float(mass_term, 3)))
close_to(mass_term, 0.00342, rtol=1e-3, source=":572")
log_term = float(np.log(mass_term))
show(sp.Eq(sp.log(2 * sp.pi * m_e / m_i), sp.Float(log_term, 3)))
close_to(log_term, -5.68, rtol=1e-3, source=":573")
show(sp.Eq(e * phi_f / (k_B * T_e), sp.Float(log_term / 2, 3)))
close_to(log_term / 2, -2.84, rtol=1e-3, source=":574")

# %% Worked example: floating surface at 3 eV
section("Worked example: floating surface at 3 eV", "15-sheaths-probes.typ:577")
area = 1.0e-4 * u.meter**2
example = {n0: 1e16 / u.meter**3, T_e: 3 * u.electronvolt / u.boltzmann_constant, **HYDROGEN, A: area}
note("Hydrogen,", sp.Eq(n0, example[n0], evaluate=False), ",",
     sp.Eq(k_B * T_e, 3 * u.electronvolt, evaluate=False), ",", sp.Eq(A, area, evaluate=False))
close_to(evaluate(lambda_D, sp.sqrt(lambda_D_sq), example, u.meter), 1.29e-4, source=":589")
flux_unit = 1 / (u.meter**2 * u.second)
electron_flux = evaluate(Gamma_e0, unretarded, example, flux_unit)
close_to(electron_flux, 2.90e21, source=":590")
ion_flux = evaluate(Gamma_i, bohm_flux, example, flux_unit)
close_to(ion_flux, 1.70e20, source=":591")
u_f = float(np.log(ion_flux / electron_flux))
show(sp.Eq(e * phi_f / (k_B * T_e), sp.Float(u_f, 3)))
close_to(u_f, -2.84, source=":592")
close_to(evaluate(phi_f, k_B * T_e / e * u_f, example, u.volt), -8.52, source=":593")
close_to(evaluate(sp.Symbol("I_i"), e * A * bohm_flux, example, milliampere), 2.72, source=":594")

# %% Langmuir probe: semilog slope
section("Langmuir probe: semilog slope", "15-sheaths-probes.typ:674")
retarded = Gamma_e0 * sp.exp(e * (phi_p - phi_pl) / (k_B * T_e))  # :704
I_p = show(sp.Eq(sp.Symbol("I_p"), A * (e * Gamma_i - e * retarded))).rhs
I_e0 = e * A * Gamma_e0  # :687
note("Subtract the ion saturation current", sp.Eq(sp.Symbol("I_i"), e * A * Gamma_i))
electron_current = sp.expand(I_p - e * A * Gamma_i)
agrees(electron_current, -e * A * retarded, ":686", lhs=sp.Symbol("I_e"))
si.check(-electron_current, e * A * Gamma_e0 * sp.exp(e * (phi_p - phi_pl) / (k_B * T_e)), unit=u.ampere,
         units=UNITS)  # :709
u_b = sp.Symbol("u", real=True)  # u = e (phi_p - phi_pl)/(k_B T_e)
PROBE_RETARDING = Gamma_i / Gamma_e0 - sp.exp(u_b)  # I_p/(e A Gamma_e0) for u <= 0
si.check(I_p / I_e0, PROBE_RETARDING.subs(u_b, e * (phi_p - phi_pl) / (k_B * T_e)))  # :676
show(sp.Eq(sp.Symbol("I_p") / (e * A * Gamma_e0), PROBE_RETARDING))
note("with", sp.Eq(u_b, e * (phi_p - phi_pl) / (k_B * T_e)), "; logarithm of the electron current:")
semilog = sp.expand_log(sp.log(sp.simplify(-electron_current / I_e0)), force=True)
agrees(semilog, e * (phi_p - phi_pl) / (k_B * T_e), ":715",
       lhs=sp.log(sp.Abs(sp.Symbol("I_e")) / sp.Symbol("I_e0")))
slope = sp.diff(semilog, phi_p)
S = sp.Symbol("S", positive=True)
agrees(slope, e / (k_B * T_e), ":721", lhs=S)
si.check(slope, e / (k_B * T_e), unit=u.volt**-1, units=UNITS)
agrees(sp.solve(sp.Eq(S, slope), T_e)[0] * k_B, e / S, ":725", lhs=k_B * T_e)

# %% Langmuir probe: density
section("Langmuir probe: density", "15-sheaths-probes.typ:734")
I0 = sp.Symbol("I_e0", positive=True)
saturation = half_space_flux(n_s, T_e, m_e)
agrees(saturation, n_s * sp.sqrt(k_B * T_e / (2 * sp.pi * m_e)), ":738", lhs=Gamma_e0)
show(sp.Eq(I0, e * A * Gamma_e0))
density = sp.solve(sp.Eq(I0, e * A * saturation), n_s)[0]
probe_density = I0 / (e * A * sp.sqrt(k_B * T_e / (2 * sp.pi * m_e)))
agrees(density, probe_density, ":742", lhs=n_s)
si.check(density, probe_density, unit=u.meter**-3, units={**UNITS, I0: u.ampere})

# %% Probe animation: ion level
section("Probe animation: ion level", "15-sheaths-probes.typ:775")
level = number(FLUX_RATIO, HYDROGEN)
show(sp.Eq(Gamma_i / Gamma_e0, sp.Float(level, 3)))
close_to(level, 0.058, rtol=1e-2, source=":775")

# %% Worked example: probe inversion
section("Worked example: probe inversion", "15-sheaths-probes.typ:782")
probe = {S: 0.40 / u.volt, I0: 4.0e-3 * u.ampere, A: 1.0e-5 * u.meter**2}
note("Measured slope", sp.Eq(S, probe[S], evaluate=False), ",", sp.Eq(I0, probe[I0], evaluate=False), ",",
     sp.Eq(A, probe[A], evaluate=False))
T_volt = evaluate(k_B * T_e / e, 1 / S, probe, u.volt)
close_to(T_volt, 2.50, rtol=1e-3, source=":789")
close_to(evaluate(n_s, probe_density, {**probe, T_e: T_volt * u.volt * u.elementary_charge / u.boltzmann_constant},
                  u.meter**-3), 9.44e15, rtol=2e-3, source=":791")

# %% Plot: Bohm sheath (M = 1) from the wall at the hydrogen floating potential
# Wall at x = 0: x(eta) = integral from eta to eta_w of d eta'/sqrt(2 S(eta')).
PANEL = (2.6, 3.0)  # one panel of a side-by-side pair
eta_w = -np.log(level)  # 2.84
sagdeev_M1 = sp.lambdify(eta, SAGDEEV.subs(M, 1), "mpmath")
eta_grid = np.geomspace(eta_w, 0.02, 120)
x_grid = [float(mp.quad(lambda t: 1 / mp.sqrt(2 * sagdeev_M1(t)), [h, eta_w])) for h in eta_grid]
n_e_plot, n_i_plot = (sp.lambdify(eta, f.subs(M, 1), "numpy") for f in (N_E, N_I))

fig, ax = figure(*PANEL)
ax.plot(x_grid, eta_grid, color=BLUE)
ax.axhline(eta_w, color=GRAY, lw=0.8, ls=":")
label(ax, 11.8, eta_w - 0.08, f"wall $\\eta_w={eta_w:.2f}$", GRAY, ha="right", va="top")
ax.set(xlim=(0, 12), ylim=(0, 3), xticks=[0, 4, 8, 12], yticks=[0, 1, 2, 3], xlabel=r"$x/\lambda_D$ from the wall [1]",
       ylabel=r"$\eta=-e\phi/k_BT_e$ [1]")
save(fig, "sheath-potential")

fig, ax = figure(*PANEL)
ax.plot(x_grid, n_i_plot(eta_grid), color=ORANGE, ls="--")
ax.plot(x_grid, n_e_plot(eta_grid), color=BLUE)
label(ax, 0.3, 0.7, "ions", ORANGE)
label(ax, 2.0, 0.12, "electrons", BLUE)
ax.set(xlim=(0, 12), ylim=(0, 1.05), xticks=[0, 4, 8, 12], yticks=[0, 0.5, 1], xlabel=r"$x/\lambda_D$ from the wall [1]",
       ylabel=r"$n/n_0$ [1]")
save(fig, "sheath-densities")

# %% Plot: planar probe current, retarding branch and electron saturation
probe_current = sp.lambdify(u_b, PROBE_RETARDING.subs(Gamma_i, level * Gamma_e0), "numpy")
u_grid = np.linspace(-8, 2, 400)
current = np.where(u_grid <= 0, probe_current(np.minimum(u_grid, 0)), probe_current(0))
u_float = np.log(level)  # -2.84
fig, ax = figure(4.2, 2.8)
ax.axhline(0, color="#333333", lw=0.6)
ax.axvline(0, color=GRAY, lw=0.8, ls=":")
ax.plot(u_grid, current, color=BLUE)
ax.plot([u_float], [0], "o", color=ORANGE, ms=4, zorder=3)
label(ax, u_float + 0.15, 0.03, f"floating $u_f={u_float:.2f}$", ORANGE)
label(ax, -7.9, level + 0.03, "ion saturation", BLUE)
label(ax, 1.9, -0.88, "electron\nsaturation", BLUE, ha="right")
label(ax, 0.1, -0.45, "plasma\npotential", GRAY)
ax.set(xlim=(-8, 2), ylim=(-1.1, 0.25), yticks=[-1, -0.5, 0],
       xlabel=r"$u=e(\phi_p-\phi_{pl})/k_BT_e$ [1]", ylabel=r"$I/(eA\Gamma_{e0})$ [1]")
save(fig, "probe-iv-characteristic")

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 15 · Sheaths and probes")
