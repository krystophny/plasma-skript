# Chapter 9 · Collisions and conductivity (src/chapters/09-collisions-conductivity.typ)
#
# Mean free path, Rutherford scattering and the Coulomb logarithm, Spitzer
# resistivity, and the magnetized conductivity tensor, with two plots.

# %% Setup
import math

import numpy as np
import sympy as sp
from sympy.physics import units as u

import si
from fluids import Named, rounded
from notebook import agrees, close_to, evaluate, note, report, section, show
from si import BLUE, GRAY, ORANGE, figure, label, save

e, eps0, k_B, m_e = si.e, si.eps0, si.k_B, si.m_e
n, sigma, v, L, T = sp.symbols("n sigma v L T_e", positive=True)
ell, b, b90, lamD = sp.symbols("ell b b_90 lambda_D", positive=True)
nu = sp.Symbol("nu", positive=True)
Lambda = sp.Symbol("Lambda", positive=True)     # plasma parameter n lambda_D^3
lnL = sp.log(Lambda)                             # Coulomb logarithm
UNITS = {n: u.meter**-3, sigma: u.meter**2, v: u.meter / u.second, L: u.meter, T: u.kelvin,
         ell: u.meter, b: u.meter, b90: u.meter, lamD: u.meter, nu: u.second**-1,
         Lambda: sp.S.One}


def has_unit(expr, unit, extra=None):
    si.check(expr, expr, unit=unit, units={**UNITS, **(extra or {})})


def ratio(symbol, value):
    """Show a dimensionless number computed from evaluated quantities."""
    show(sp.Eq(symbol, sp.Float(value, 3)))
    return value


def agrees_with(derived, printed, values, lhs, eq=""):
    """agrees() for a statement written with named quantities: `values` are
    inserted for the comparison, the display keeps the names."""
    residual = derived - printed.subs(values).doit()    # must vanish
    return agrees(residual + printed, printed, lhs=lhs, eq=eq)


def given(values, *more):
    """Note listing the inputs of a worked example, separated by commas."""
    parts = ["Input"]
    for symbol, value in values.items():
        parts += [sp.Eq(symbol, rounded(value)), ","]
    note(*parts[:-1], *more)


# %% Mean free path
section("Survival probability and mean free path", script="collision-bookkeeping")
P0 = sp.Function("P_0")
note("Each length", ell, "removes the fraction", n * sigma, "per metre of the unscattered beam")
survival = show(sp.Eq(P0(ell).diff(ell), -n * sigma * P0(ell)))
solution = show(sp.dsolve(survival, P0(ell), ics={P0(0): 1}))
agrees(solution.rhs, sp.exp(-n * sigma * ell), lhs=P0(ell))
lam = sp.Symbol("lambda", positive=True)
mean_free_path = show(sp.Eq(lam, sp.Integral(solution.rhs, (ell, 0, sp.oo))))
agrees(mean_free_path.rhs.doit(), 1 / (n * sigma), lhs=lam)
has_unit(1 / (n * sigma), u.meter)
note("The path grows as", sp.Eq(ell, v * sp.Symbol("t")), ", so the encounter rate is")
agrees(v / mean_free_path.rhs.doit(), n * sigma * v, lhs=nu)
has_unit(n * sigma * v, u.second**-1)
has_unit(lam / L, u.meter / u.meter, {lam: u.meter})              # Knudsen number

# %% Example: collision times
section("Example: collision frequency and Knudsen number", script="collision-bookkeeping")
beam = {n: 1.0e19 / u.meter**3, sigma: 2.0e-19 * u.meter**2, v: 1.0e5 * u.meter / u.second,
        L: 10.0 * u.meter}
given(beam)
nu_ab, tau_ab, lam_ab = sp.symbols("nu_ab tau_ab lambda_ab")
rate = evaluate(nu_ab, n * sigma * v, beam, u.second**-1)
close_to(rate, 2.0e5)
close_to(evaluate(tau_ab, 1 / (n * sigma * v), beam, u.second), 5.0e-6)
path = evaluate(lam_ab, 1 / (n * sigma), beam, u.meter)
close_to(path, 0.50)
close_to(ratio(sp.Symbol("K_n"), path / 10.0), 0.050)

# %% Neutral drag
section("Drag on stationary neutrals", script="neutral-collisions")
u_a, R_an = sp.symbols("u_a R_an", real=True)
note("Momentum", m_e * u_a, "lost per encounter,", n * nu, "encounters per volume and time")
drag = show(sp.Eq(R_an, -m_e * n * nu * u_a)).rhs
has_unit(drag, u.newton / u.meter**3, {u_a: u.meter / u.second})

# %% Example: electron-neutral collisions
section("Example: electron-neutral collisions", script="neutral-collisions")
gas = {n: 2.0e20 / u.meter**3, sigma: 2.0e-19 * u.meter**2, v: 1.0e5 * u.meter / u.second}
given(gas)
nu_en, lam_en = sp.symbols("nu_en lambda_en")
close_to(evaluate(nu_en, n * sigma * v, gas, u.second**-1), 4.0e6)
close_to(evaluate(lam_en, 1 / (n * sigma), gas, u.meter), 2.5e-2)

# %% Rutherford deflection
section("Rutherford deflection and the 90-degree impact parameter", script="coulomb-collisions")
q_a, q_b, m_r = sp.symbols("q_a q_b m_r", positive=True)
w = sp.Symbol("w", positive=True)                 # inverse radius 1/r
theta0, chi, w_max = sp.symbols("theta_0 chi w_max", positive=True)
note("Strong-deflection impact parameter: Coulomb energy at", b90, "equals the kinetic energy scale")
b90_def = show(sp.Eq(b90, q_a * q_b / (4 * sp.pi * eps0 * m_r * v**2))).rhs
has_unit(b90_def, u.meter, {q_a: u.coulomb, q_b: u.coulomb, m_r: u.kilogram})
note("Attractive orbit from energy and angular momentum, with", sp.Eq(w, 1 / sp.Symbol("r")), ":")
integrand = b / sp.sqrt(1 + 2 * b90 * w - b**2 * w**2)
show(sp.Eq(theta0, sp.Integral(integrand, (w, 0, w_max))))
roots = sp.solve(sp.Eq(1 + 2 * b90 * w - b**2 * w**2, 0), w)
turning = [root for root in roots if root.is_positive is not False][-1]   # outer turning point
show(sp.Eq(w_max, turning))
antiderivative = sp.asin((b**2 * w - b90) / sp.sqrt(b**2 + b90**2))
note("Antiderivative (checked by differentiation)")
agrees(sp.diff(antiderivative, w), integrand, lhs=sp.Derivative(antiderivative, w))
orbit = sp.simplify(antiderivative.subs(w, turning) - antiderivative.subs(w, 0))
show(sp.Eq(theta0, orbit))
note("Deflection", sp.Eq(chi, 2 * theta0 - sp.pi), ":")
deflection = 2 * orbit - sp.pi
agrees(sp.simplify(sp.tan(deflection / 2)), b90 / b, lhs=sp.tan(chi / 2))
agrees(sp.simplify(deflection.subs(b, b90)), sp.pi / 2, lhs=sp.Function("chi")(b90))
small = sp.Symbol("epsilon", positive=True)
note("Weak deflection,", sp.Eq(b90, small * b), ", to first order in", small)
agrees(sp.series(deflection.subs(b90, small * b), small, 0, 2).removeO(), 2 * small, lhs=chi)
note("Impulse approximation along the straight line, Coulomb force", q_a * q_b / (4 * sp.pi * eps0))
time = sp.Symbol("t", real=True)
impulse = sp.Integral(q_a * q_b / (4 * sp.pi * eps0) * b / (b**2 + v**2 * time**2) ** sp.Rational(3, 2),
                      (time, -sp.oo, sp.oo))
dp = sp.Symbol("p_y")                             # transverse momentum kick
show(sp.Eq(dp, impulse))
agrees(sp.simplify(impulse.doit() / (m_r * v)), 2 * b90_def / b, lhs=dp / (m_r * v))
note("Electron on a heavy ion,", sp.Eq(q_a, e), ",", sp.Eq(q_b, e), ",", sp.Eq(m_r, m_e))
b90_e = b90_def.subs({q_a: e, q_b: e, m_r: m_e})
agrees(b90_e, e**2 / (4 * sp.pi * eps0 * m_e * v**2), lhs=b90)
has_unit(b90_e, u.meter)

# %% Large-angle collision rate
section("Large-angle collision rate", script="coulomb-collisions")
nu90 = sp.Symbol("nu_90")
note("Cross section", sp.Eq(sp.Symbol("sigma_90"), sp.pi * b90**2))
agrees(n * sp.pi * b90_e**2 * v, n * e**4 / (16 * sp.pi * eps0**2 * m_e**2 * v**3), lhs=nu90)
has_unit(n * sp.pi * b90_e**2 * v, u.second**-1)

# %% Momentum-transfer cross section
section("Momentum-transfer cross section for Coulomb scattering", script="neutral-collisions")
b_max, sigma_mt = sp.symbols("b_max sigma_mt", positive=True)
ONE_MINUS_COS = 2 * b90**2 / (b**2 + b90**2)       # also used by the plot below
note("With", sp.Eq(sp.tan(chi / 2), b90 / b), ":")
agrees(sp.simplify(2 * sp.sin(sp.atan(b90 / b)) ** 2), ONE_MINUS_COS, lhs=1 - sp.cos(chi))
transfer = show(sp.Eq(sigma_mt, sp.Integral(2 * sp.pi * b * ONE_MINUS_COS, (b, 0, b_max))))
agrees(transfer.rhs.doit(), 2 * sp.pi * b90**2 * sp.log(1 + b_max**2 / b90**2), lhs=sigma_mt)
note("Leading logarithm for", b_max, "much larger than", b90, ":")
agrees(sp.limit(transfer.rhs.doit() - 4 * sp.pi * b90**2 * sp.log(b_max / b90), b_max, sp.oo), 0, lhs=sp.Limit(sigma_mt - 4 * sp.pi * b90**2 * sp.log(b_max / b90), b_max, sp.oo))

# %% Coulomb logarithm
section("Coulomb logarithm and plasma parameter", script="coulomb-collisions")
speed = sp.Symbol("v_e", positive=True)
mean_v = sp.Symbol("vbar_e")
maxwellian = (2 * sp.pi * k_B * T / m_e) ** sp.Rational(-3, 2) * sp.exp(-m_e * speed**2 / (2 * k_B * T))
average = show(sp.Eq(mean_v, sp.Integral(4 * sp.pi * speed**3 * maxwellian, (speed, 0, sp.oo))))
v_mean = sp.simplify(average.rhs.doit())
agrees(v_mean, sp.sqrt(8 * k_B * T / (sp.pi * m_e)), lhs=mean_v)
has_unit(v_mean, u.meter / u.second)
lambda_D = sp.sqrt(eps0 * k_B * T / (n * e**2))
Lambda_cut = sp.Symbol("Lambda_cut")
note("Cut-off ratio at the mean speed, with", sp.Eq(lamD, lambda_D))
cutoff = sp.simplify(lambda_D / b90_e.subs(v, v_mean))
agrees(cutoff, 32 * n * lambda_D**3, lhs=Lambda_cut)
has_unit(n * lambda_D**3, u.meter / u.meter)
note("Plasma parameter", sp.Eq(Lambda, n * lamD**3), "and Debye-sphere count")
agrees(n * sp.Rational(4, 3) * sp.pi * lambda_D**3, sp.Rational(4, 3) * sp.pi * (n * lambda_D**3), lhs=sp.Symbol("N_D"))
spread = sp.Symbol("S")                          # growth rate of the mean square v_perp
note("Growth rate", spread, "of the mean square transverse velocity: small deflections",
     2 * b90 / b, "summed over annuli between", b90, "and", lamD)
annuli = show(sp.Eq(spread, sp.Integral(n * v * 2 * sp.pi * b * v**2 * (2 * b90 / b) ** 2, (b, b90, lamD))))
agrees(annuli.rhs.doit(), 8 * sp.pi * n * v**3 * b90**2 * sp.log(lamD / b90), lhs=spread)
note("Cited electron-ion rate (Inan and Golkowski 2011); unit and temperature scaling checked:")
omega_pe2 = n * e**2 / (eps0 * m_e)
NU_EI = sp.sqrt(2) * omega_pe2**2 / (64 * sp.pi * n) * (k_B * T / m_e) ** sp.Rational(-3, 2) * lnL
nu_ei = sp.Symbol("nu_ei")
show(sp.Eq(nu_ei, NU_EI))
has_unit(NU_EI, u.second**-1)
agrees(sp.simplify(T * sp.diff(NU_EI, T) / NU_EI), sp.Rational(-3, 2),
       lhs=T * sp.Derivative(sp.Function("nu_ei")(T), T) / sp.Function("nu_ei")(T))

# %% Example: Coulomb collisions at 10 eV
section("Example: Coulomb collisions at 10 eV", script="coulomb-collisions")
plasma = {n: 1.0e16 / u.meter**3, T: 1.602e-18 * u.joule / u.boltzmann_constant}
note("Input", sp.Eq(n, rounded(plasma[n])), "and", sp.Eq(k_B * T, 1.602e-18 * u.joule))
debye = evaluate(lamD, lambda_D, plasma, u.meter)
close_to(debye, 2.35e-4)
plasma_parameter = ratio(Lambda, 1.0e16 * debye**3)
close_to(plasma_parameter, 1.30e5)
log_Lambda = ratio(lnL, math.log(plasma_parameter))
close_to(log_Lambda, 11.8)
rate = evaluate(nu_ei, NU_EI, {**plasma, lnL: log_Lambda}, u.second**-1)
close_to(rate, 3.60e3)
mean_speed = evaluate(mean_v, v_mean, plasma, u.meter / u.second)
close_to(mean_speed, 2.12e6)
note("Mean free path from the printed", mean_v, "and", nu_ei)
lam_ei = sp.Symbol("lambda_ei")
close_to(evaluate(lam_ei, v / nu, {v: 2.12e6 * u.meter / u.second, nu: 3.60e3 / u.second}, u.meter),
         5.89e2)
close_to(mean_speed / rate, 5.89e2)

# %% Spitzer resistivity
section("Spitzer resistivity", script="specific-resistivity")
j, u_i, u_e = sp.symbols("j u_i u_e", real=True)
eta, eta_Sp = sp.symbols("eta eta_Sp")
note("Electron-ion drag per charge density, with", sp.Eq(u_i - u_e, j / (e * n)))
friction = show(sp.Eq(sp.Symbol("R_ei"), m_e * n * nu * (u_i - u_e))).rhs
resistivity = sp.simplify((friction / (e * n)).subs(u_i, u_e + j / (e * n)) / j)
agrees(resistivity, m_e * nu / (n * e**2), lhs=eta)
has_unit(resistivity, u.ohm * u.meter)
agrees(1 / resistivity, n * e**2 / (m_e * nu), lhs=1 / eta)
has_unit(1 / resistivity, u.siemens / u.meter)
note("Insert the cited", nu_ei)
spitzer = sp.simplify(resistivity.subs(nu, NU_EI))
SPITZER = (sp.pi / (2 * sp.sqrt(2)) * e**2 * sp.sqrt(m_e)
           / ((4 * sp.pi * eps0) ** 2 * (k_B * T) ** sp.Rational(3, 2)) * lnL)
agrees(spitzer, SPITZER, lhs=eta_Sp)
has_unit(SPITZER, u.ohm * u.meter)
note("Independent of density, and falling as the -3/2 power of temperature:")
agrees(sp.diff(SPITZER, n), 0, lhs=sp.Derivative(eta_Sp, n))
agrees(sp.simplify(T * sp.diff(SPITZER, T) / SPITZER), sp.Rational(-3, 2),
       lhs=T * sp.Derivative(sp.Function("eta_Sp")(T), T) / sp.Function("eta_Sp")(T))

# %% Example: Spitzer resistivity
section("Example: Spitzer resistivity", script="specific-resistivity")
spitzer_case = {n: 1.0e16 / u.meter**3, nu: 3.60e3 / u.second}
given(spitzer_case)
eta_value = evaluate(eta_Sp, resistivity, spitzer_case, u.ohm * u.meter)
close_to(eta_value, 1.28e-5)
close_to(evaluate(sp.Symbol("sigma_dc"), 1 / resistivity, spitzer_case, u.siemens / u.meter),
         7.83e4)

# %% Conductivity tensor
section("Conductivity tensor", script="plasma-conductivity")
OM_S, OMEGA = sp.symbols("Omega_s omega", real=True)
q_s, m_s = sp.Symbol("q_s", real=True), sp.Symbol("m_s", positive=True)
A_S = nu - sp.I * OMEGA                          # a_s = nu_s - i omega
SIGMA_PAR = n * q_s**2 / (m_s * A_S)             # results shared with the plots
SIGMA_PERP = n * q_s**2 * A_S / (m_s * (A_S**2 + OM_S**2))
SIGMA_HALL = n * q_s**2 * OM_S / (m_s * (A_S**2 + OM_S**2))
B_0 = sp.Symbol("B_0", positive=True)
E_x, E_y, E_z = sp.symbols("E_x E_y E_z")
u_x, u_y, u_z = sp.symbols("u_x u_y u_z")
j_x = sp.Symbol("j_x")
note("Harmonic momentum balance with friction,", sp.Eq(sp.Symbol("a_s"), A_S), ", field along z:")
balance = [sp.Eq(m_s * A_S * u_x, q_s * (E_x + u_y * B_0)),
           sp.Eq(m_s * A_S * u_y, q_s * (E_y - u_x * B_0)),
           sp.Eq(m_s * A_S * u_z, q_s * E_z)]
for eq in balance:
    show(eq)
velocity = sp.solve(balance, [u_x, u_y, u_z], dict=True)[0]
J = [sp.simplify(n * q_s * velocity[c]) for c in (u_x, u_y, u_z)]
Omega = q_s * B_0 / m_s
note("Current", sp.Eq(j_x, n * q_s * u_x), "and alike; gyrofrequency", sp.Eq(OM_S, Omega))
s_perp, s_hall, s_par = (S.subs(OM_S, Omega) for S in (SIGMA_PERP, SIGMA_HALL, SIGMA_PAR))
sig_perp, sig_hall, sig_par = (Named(name) for name in ("sigma_perp", "sigma_H", "sigma_parallel"))
entries = {sig_perp: SIGMA_PERP, sig_hall: SIGMA_HALL, sig_par: SIGMA_PAR}
j_x, j_y, j_z = sp.symbols("j_x j_y j_z")
show(sp.Eq(sig_perp, SIGMA_PERP))
show(sp.Eq(sig_hall, SIGMA_HALL))
show(sp.Eq(sig_par, SIGMA_PAR))
note("Then the solved current is the tensor product (x row shown; y and z rows asserted)")
gyro = {OM_S: Omega}
agrees_with(J[0], sig_perp * E_x + sig_hall * E_y, {k: val.subs(gyro) for k, val in entries.items()}, lhs=j_x)
assert sp.simplify(J[1] - (-s_hall * E_x + s_perp * E_y)) == 0
assert sp.simplify(J[2] - s_par * E_z) == 0
sigma0 = n * q_s**2 / (m_s * A_S)
note("Component form of the balance, with", sp.Eq(sp.Symbol("sigma_0"), sigma0), ":")
agrees_with(J[0], sp.Symbol("sigma_0") * E_x + OM_S / A_S * j_y,
            {sp.Symbol("sigma_0"): sigma0, OM_S: Omega, j_y: J[1]}, lhs=j_x)
assert sp.simplify(J[1] - (sigma0 * E_y - Omega / A_S * J[0])) == 0
note("DC limit", sp.Eq(OMEGA, 0), ":")
dc = n * q_s**2 / (m_s * nu)
agrees(SIGMA_PERP.subs(OMEGA, 0), dc * nu**2 / (nu**2 + OM_S**2), lhs=sig_perp)
agrees(SIGMA_HALL.subs(OMEGA, 0), dc * nu * OM_S / (nu**2 + OM_S**2), lhs=sig_hall)
agrees(SIGMA_PAR.subs(OMEGA, 0), dc, lhs=sig_par)
has_unit(dc, u.siemens / u.meter, {q_s: u.coulomb, m_s: u.kilogram})
omega_p = sp.Symbol("omega_p", positive=True)
plasma_freq = {omega_p: sp.sqrt(n * q_s**2 / (eps0 * m_s))}
note("Plasma-frequency form,", sp.Eq(omega_p**2, plasma_freq[omega_p] ** 2), ":")
for symbol, stated in [(sig_par, eps0 * omega_p**2 / A_S),
                       (sig_perp, eps0 * omega_p**2 * A_S / (A_S**2 + OM_S**2)),
                       (sig_hall, eps0 * omega_p**2 * OM_S / (A_S**2 + OM_S**2))]:
    agrees_with(entries[symbol], stated, plasma_freq, lhs=symbol)

# %% Example: magnetized DC conductivity
section("Example: magnetized DC conductivity", script="plasma-conductivity")
B_value = {B_0: 0.010 * u.tesla, n: 1.0e16 / u.meter**3, nu: 2.5e3 / u.second}
given(B_value)
electron = {q_s: -e, m_s: m_e}
# nu^2 + Omega^2 is a sum of quantities: insert e, m_e and B in base units so it adds up.
base = [u.kilogram, u.coulomb, u.second]
in_base = {e: u.convert_to(u.elementary_charge, base), m_e: u.convert_to(u.electron_rest_mass, base),
           B_0: u.convert_to(B_value[B_0], base)}
Omega_e = sp.Symbol("Omega_e")
gyro_value = evaluate(Omega_e, Omega.subs(electron), B_value, u.second**-1)
close_to(gyro_value, -1.76e9)
dc_entries = {k: val.subs(OMEGA, 0).subs(OM_S, Omega).subs(electron) for k, val in entries.items()}
inputs = {**B_value, **in_base}
close_to(evaluate(sig_par, dc_entries[sig_par], inputs, u.siemens / u.meter), 1.13e5)
close_to(evaluate(sig_perp, dc_entries[sig_perp], inputs, u.siemens / u.meter), 2.28e-7)
close_to(evaluate(sig_hall, dc_entries[sig_hall], inputs, u.siemens / u.meter), -0.160)

# %% Plot: Coulomb cut-off
# Momentum-transfer weight per logarithmic impact-parameter interval,
# d sigma_mt / d ln b = 2 pi b^2 (1 - cos chi), in units of 4 pi b_90^2.
beta = sp.Symbol("beta", positive=True)          # b / b_90
weight = sp.lambdify(beta, sp.simplify((2 * sp.pi * b**2 * ONE_MINUS_COS / (4 * sp.pi * b90**2))
                                       .subs(b, beta * b90)), "numpy")
cut = 32 * plasma_parameter                      # lambda_D / b_90 of the 10 eV example
area = 0.5 * math.log(1 + cut**2)                # integral of the weight over ln b
fig, ax = figure(4.2, 2.4)
bb = np.logspace(-2, math.log10(cut), 400)
ax.fill_between(bb, weight(bb), color=BLUE, alpha=0.15, lw=0)
ax.plot(bb, weight(bb), color=BLUE)
ax.plot([cut, cut], [weight(cut), 0], color=BLUE)
ax.plot([cut, 3e8], [0, 0], color=BLUE)
for xb, txt in [(1, r"$b_{90}$"), (cut, r"$\lambda_D$")]:
    ax.axvline(xb, color=GRAY, lw=0.8, ls=":")
    ax.text(xb, 1.12, txt, color=GRAY, ha="center", va="bottom")
label(ax, math.sqrt(cut), 0.45, rf"$\mathrm{{area}}=\ln\Lambda_{{\rm cut}}\approx{area:.1f}$",
      BLUE, ha="center", va="center")
ax.set_xscale("log")
ax.set_xlim(1e-2, 3e8)
ax.set_ylim(0, 1.25)
ax.set_xticks([1e-2, 1, 1e2, 1e4, 1e6, 1e8])
ax.minorticks_off()
ax.set_yticks([0, 0.5, 1])
ax.set_xlabel(r"impact parameter $b/b_{90}$")
ax.set_ylabel(r"$d\sigma_{\rm mt}/d\ln b$  [$4\pi b_{90}^2$]")
save(fig, "coulomb-cutoff")

# %% Plot: DC conductivity tensor, Pedersen and Hall side by side
X_mag = sp.Symbol("X", positive=True)            # |Omega_s| / nu_s
dc_ratio = {OMEGA: 0, OM_S: X_mag * nu}
panels = [("conductivity-pedersen", SIGMA_PERP, BLUE, "-", r"$\sigma_\perp/\sigma_\parallel$",
           (0.12, 0.72, "right"), r"Pedersen"),
          ("conductivity-hall", SIGMA_HALL, ORANGE, "--", r"$|\sigma_{\rm H}|/\sigma_\parallel$",
           (3.5, 0.33, "left"), r"Hall")]
xx = np.logspace(-2, 2, 300)
for name, entry, color, style, ylabel, (lx, ly, ha), title in panels:
    curve = sp.lambdify(X_mag, sp.simplify((entry / SIGMA_PAR).subs(dc_ratio)), "numpy")
    fig, ax = figure(2.8, 2.6)
    ax.axhline(1, color=GRAY, lw=1.0, ls=(0, (1, 2)))
    ax.plot(xx, curve(xx), color=color, ls=style)
    label(ax, 1.2e-2, 1.02, r"$\sigma_\parallel$", GRAY)
    label(ax, lx, ly, title, color, ha=ha)
    ax.plot([1], [curve(1.0)], "o", color="#333333", ms=3.5)
    ax.text(1.4, curve(1.0) + 0.06, r"$|\Omega_s|=\nu_s$", color="#333333", fontsize=9)
    ax.set_xscale("log")
    ax.set_xticks([1e-2, 1, 1e2])
    ax.minorticks_off()
    ax.set_ylim(0, 1.12)
    ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel(r"$|\Omega_s|/\nu_s$")
    ax.set_ylabel(ylabel + " (DC)")
    save(fig, name)

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 9 · Collisions and conductivity")
