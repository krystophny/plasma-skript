# Chapter 10 · Diffusion (src/chapters/10-diffusion.typ)
#
# Random walk and Fick's law, the Green function, mobility and the Einstein
# relation, ambipolar and magnetized diffusion, classical versus Bohm, with plots.

# %% Setup
import itertools
import math

import numpy as np
import sympy as sp
from sympy.physics import units as u

import si
from fluids import Named, Partial, field, rounded
from notebook import agrees, close_to, evaluate, note, report, section, show
from si import BLUE, GRAY, ORANGE, SI_VALUES, figure, label, log_ticks, save

e, k_B, m_e, m_i = si.e, si.k_B, si.m_e, si.m_i
x, t = sp.symbols("x t", real=True)
dx, dt, D, L, t0 = sp.symbols("Delta_x Delta_t D L t_0", positive=True)
UNITS = {dx: u.meter, dt: u.second, D: u.meter**2 / u.second, L: u.meter, t0: u.second}


def has_unit(expr, unit, extra=None):
    si.check(expr, expr, unit=unit, units={**UNITS, **(extra or {})})


def agrees_with(derived, printed, values, source, lhs):
    """agrees() for a statement written with named quantities: `values` are
    inserted for the comparison, the display keeps the names."""
    residual = derived - printed.subs(values).doit()    # must vanish
    return agrees(residual + printed, printed, source, lhs=lhs)


def ratio(symbol, value):
    """Show a dimensionless number computed from evaluated quantities."""
    show(sp.Eq(symbol, sp.Float(value, 3)))
    return value


def given(values, *more):
    """Note listing the inputs of a worked example, separated by commas."""
    parts = ["Input"]
    for symbol, value in values.items():
        parts += [sp.Eq(symbol, rounded(value)), ","]
    note(*parts[:-1], *more)


# %% Random walk
section("Random walk", "10-diffusion.typ:92")
M1, x_rms, N = sp.symbols("xbar x_rms N")
M2 = x_rms**2
note("Steps of", sp.Tuple(dx, -dx), "with probability 1/2 each; average position", M1,
     "and mean square", M2, "over all equally likely paths of", N, "steps")
for steps in range(1, 7):
    paths = list(itertools.product([1, -1], repeat=steps))
    mean = sum(sum(p) for p in paths) * dx / len(paths)
    mean_square = sum(sum(p) ** 2 for p in paths) * dx**2 / len(paths)
    if steps == 6:
        note("For", sp.Eq(N, steps), "(N = 1 ... 5 asserted):")
        agrees(mean, 0, ":85", lhs=M1)
        agrees(mean_square, steps * dx**2, ":88", lhs=M2)
    else:
        assert mean == 0 and sp.simplify(mean_square - steps * dx**2) == 0
note("After a time", t, "with the diffusion coefficient", D, ":")
show(sp.Eq(N, t / dt))
show(sp.Eq(D, dx**2 / (2 * dt)))
agrees_with((N * dx**2).subs(N, t / dt), 2 * D * t, {D: dx**2 / (2 * dt)}, ":94", lhs=M2)
has_unit(dx**2 / (2 * dt), u.meter**2 / u.second)
has_unit(L**2 / D, u.second)                    # tau_D = L^2/D

# %% Fick's law and the diffusion equation
section("Fick's law and the diffusion equation", "10-diffusion.typ:104")
n_x = sp.Function("n")
x0 = sp.Symbol("x_0", real=True)
Gamma = sp.Symbol("Gamma")
note("Half of each neighbouring cell crosses", x0, "in", dt, ":")
crossing = show(sp.Eq(Gamma, (n_x(x0 - dx / 2) * dx / 2 - n_x(x0 + dx / 2) * dx / 2) / dt)).rhs
note("Expand the densities to second order in", dx)
leading = sp.simplify(sp.series(crossing, dx, 0, 3).removeO().doit())
agrees(leading, -(dx**2 / (2 * dt)) * sp.Derivative(n_x(x0), x0), ":104", lhs=Gamma)
D_x, n_xt = field("D", x), field("n", x, t)
note("Conservation with the flux", sp.Eq(Gamma, -D_x * Partial(n_xt, x)), ":")
agrees(-Partial(-D_x * Partial(n_xt, x), x).doit(), Partial(D_x * Partial(n_xt, x), x), ":113",
       lhs=Partial(n_xt, t))

# %% Green function
section("Green function of the diffusion equation", "10-diffusion.typ:118")
N0, tp = sp.symbols("N_0 t", positive=True)
GREEN = N0 / sp.sqrt(4 * sp.pi * D * tp) * sp.exp(-x**2 / (4 * D * tp))   # also plotted below
n_G = sp.Symbol("n_G")
show(sp.Eq(n_G, GREEN))
note("It solves the diffusion equation, conserves the column", N0, "and starts point-like:")
agrees(sp.diff(GREEN, tp) - D * sp.diff(GREEN, x, 2), 0, ":118",
       lhs=sp.Derivative(n_G, tp) - D * sp.Derivative(n_G, (x, 2)))
column = sp.Integral(GREEN, (x, -sp.oo, sp.oo))
agrees(column.doit(), N0, ":118", lhs=sp.Integral(n_G, (x, -sp.oo, sp.oo)))
agrees(sp.limit(GREEN.subs(x, 1), tp, 0, "+"), 0, ":118",
       lhs=sp.Limit(sp.Function("n_G")(1, tp), tp, 0, "+"))
spread = sp.Integral(x**2 * GREEN, (x, -sp.oo, sp.oo)) / N0
agrees(spread.doit(), 2 * D * tp, ":120", lhs=M2)
y, z = sp.symbols("y z", real=True)
G3 = GREEN * GREEN.subs(x, y) * GREEN.subs(x, z) / N0**2
r_rms = sp.Symbol("r_rms")
note("Three independent directions:")
agrees(sp.integrate((x**2 + y**2 + z**2) * G3, (x, -sp.oo, sp.oo), (y, -sp.oo, sp.oo),
                    (z, -sp.oo, sp.oo)) / N0, 6 * D * tp, ":121", lhs=r_rms**2)
has_unit(N0 / sp.sqrt(D * t0), u.meter**-3, {N0: u.meter**-2})

# %% Normalized variables
section("Normalized diffusion variables", "10-diffusion.typ:134")
L0, tau0, n0, xi, tau = sp.symbols("L_0 tau_0 n_0 xi tau", positive=True)
D_norm, L_norm = sp.symbols("D_norm L_norm", positive=True)
Nf = sp.Function("N")
note("Write", sp.Eq(field("n", x, t), n0 * Nf(x / L0, t / tau0)), "with", sp.Eq(D, D_norm * L0**2 / tau0))
density = n0 * Nf(x / L0, t / tau0)
residual = sp.diff(density, t) - D_norm * L0**2 / tau0 * sp.diff(density, x, 2)
residual = sp.simplify(residual.subs({x: xi * L0, t: tau * tau0}) * tau0 / n0)
agrees(residual.doit(), sp.Derivative(Nf(xi, tau), tau) - D_norm * sp.Derivative(Nf(xi, tau), (xi, 2)),
       ":134", lhs=tau0 / n0 * (sp.Derivative(field("n", x, t), t) - D * sp.Derivative(field("n", x, t), (x, 2))))
tau_D = sp.Symbol("tau_D")
agrees((L_norm * L0) ** 2 / (D_norm * L0**2 / tau0) / tau0, L_norm**2 / D_norm, ":136", lhs=tau_D / tau0)
note("Animation: steps of 0.34 in", xi, "per unit of", tau)
D_star = sp.Symbol("D_*")
close_to(ratio(D_star, 0.34**2 / 2), 0.0578, source=":150")

# %% Example: random-walk diffusion
section("Example: random-walk diffusion", "10-diffusion.typ:163")
walk = {dx: 2.0e-3 * u.meter, dt: 1.0e-7 * u.second, L: 0.1 * u.meter}
given(walk)
D_walk = evaluate(D, dx**2 / (2 * dt), walk, u.meter**2 / u.second)
close_to(D_walk, 2.0e1, source=":166")
close_to(evaluate(tau_D, L**2 / (dx**2 / (2 * dt)), walk, u.second), 5.0e-4, source=":168")

# %% Mobility and diffusion
section("Mobility and diffusion", "10-diffusion.typ:291")
q, nu, m, T = sp.symbols("q_s nu_s m_s T_s", positive=True)   # q > 0 here; sign handled below
UNITS.update({q: u.coulomb, nu: u.second**-1, m: u.kilogram, T: u.kelvin})
n_s = sp.Symbol("n_s", positive=True)
E, g_s, u_s = sp.symbols("E g u_s", real=True)                # g = dn/dx
q_signed = sp.Symbol("q", real=True)
mu_s, D_s = sp.symbols("mu_s D_s")
note("Inertialess momentum balance with friction and pressure,", sp.Eq(g_s, sp.Derivative(sp.Function("n_s")(x), x)))
friction = show(sp.Eq(m * n_s * nu * u_s, q_signed * n_s * E - k_B * T * g_s))
drift = sp.solve(friction, u_s)[0]
mobility = {mu_s: q_signed / (m * nu), D_s: k_B * T / (m * nu)}
note("Mobility", sp.Eq(mu_s, mobility[mu_s]), "and diffusion coefficient", sp.Eq(D_s, mobility[D_s]))
agrees_with(drift, mu_s * E - D_s * g_s / n_s, mobility, ":286", lhs=u_s)
Gamma_s = sp.Symbol("Gamma_s")
agrees_with(n_s * drift, n_s * mu_s * E - D_s * g_s, mobility, ":267", lhs=Gamma_s)
note("Einstein relation, with", sp.Eq(sp.Abs(mu_s), q / (m * nu)), ":")
agrees((k_B * T / (m * nu)) / (q / (m * nu)), k_B * T / q, ":304", lhs=D_s / sp.Abs(mu_s))
has_unit(q / (m * nu), u.meter**2 / u.volt / u.second)
has_unit(k_B * T / (m * nu), u.meter**2 / u.second)

# %% Example: electron mobility
section("Example: electron mobility and diffusion", "10-diffusion.typ:317")
electron = {nu: 1.0e8 / u.second, T: 2.0 * u.electronvolt / u.boltzmann_constant}
note("Electrons,", sp.Eq(nu, rounded(electron[nu])), ",", sp.Eq(k_B * T, 2.0 * u.electronvolt))
mu_e, D_e = sp.symbols("mu_e D_e")
close_to(evaluate(mu_e, e / (m_e * nu), electron, u.meter**2 / (u.volt * u.second)), 1.76e3,
         source=":320")
close_to(evaluate(D_e, k_B * T / (m_e * nu), electron, u.meter**2 / u.second), 3.52e3, source=":323")

# %% Ambipolar diffusion
section("Ambipolar diffusion", "10-diffusion.typ:457")
mui, mue, Di, De, n_a = sp.symbols("mu_i mu_e D_i D_e n", positive=True)
E_x, g_n = sp.symbols("E g", real=True)          # field and density gradient along x
GAMMA_I = mui * n_a * E_x - Di * g_n             # shared with the plot below
GAMMA_E = -mue * n_a * E_x - De * g_n
E_AMB = (Di - De) / (mui + mue) * g_n / n_a
D_AMB = (mui * De + mue * Di) / (mui + mue)
Gamma_i, Gamma_e, E_a, D_a, Gamma_a = sp.symbols("Gamma_i Gamma_e E_a D_a Gamma_a")
note("Drift plus diffusion for ions and electrons, with", sp.Eq(g_n, sp.Derivative(sp.Function("n")(x), x)))
show(sp.Eq(Gamma_i, GAMMA_I))
show(sp.Eq(Gamma_e, GAMMA_E))
note("Zero current,", sp.Eq(Gamma_i, Gamma_e), ", fixes the field:")
field_a = sp.solve(sp.Eq(GAMMA_I, GAMMA_E), E_x)[0]
agrees(field_a, E_AMB, ":457", lhs=E_a)
note("Insert into either flux:")
show(sp.Eq(D_a, D_AMB))
agrees_with(sp.simplify(GAMMA_I.subs(E_x, field_a)), -D_a * g_n, {D_a: D_AMB}, ":470", lhs=Gamma_i)
agrees_with(sp.simplify(GAMMA_E.subs(E_x, field_a)), -D_a * g_n, {D_a: D_AMB}, ":470", lhs=Gamma_e)
eps = sp.Symbol("epsilon", positive=True)
note("Light electrons,", sp.Eq(mui, eps * mue), ", to first order in", eps, ":")
expansion = sp.series(D_AMB.subs(mui, eps * mue), eps, 0, 2).removeO()
agrees(expansion, Di + eps * (De - Di), ":479", lhs=D_a)
note("The stated", Di + eps * De, "differs by", eps * Di, ", negligible against", Di, ":")
agrees(sp.limit((expansion - (Di + eps * De)) / Di, eps, 0), 0, ":479",
       lhs=sp.Limit((D_a - (Di + eps * De)) / Di, eps, 0))

# %% Example: ambipolar field and flux
section("Example: ambipolar field and flux", "10-diffusion.typ:492")
nu_i, nu_e, m_p = sp.symbols("nu_i nu_e m_p", positive=True)
T_a, gradient = sp.symbols("T g_n", positive=True)
hydrogen = {mui: e / (m_p * nu_i), mue: e / (m_e * nu_e), Di: k_B * T_a / (m_p * nu_i),
            De: k_B * T_a / (m_e * nu_e)}
discharge = {T_a: 1.0 * u.electronvolt / u.boltzmann_constant, nu_i: 1.0e7 / u.second,
             nu_e: 1.0e9 / u.second, n_a: 1.0e16 / u.meter**3, g_n: -1.0e16 / u.meter**4}
note("Hydrogen,", sp.Eq(k_B * T_a, 1.0 * u.electronvolt), ",", sp.Eq(nu_i, rounded(discharge[nu_i])), ",",
     sp.Eq(nu_e, rounded(discharge[nu_e])), ",", sp.Eq(n_a, rounded(discharge[n_a])), ",",
     sp.Eq(g_n / n_a, -1 / u.meter))
in_kg = {m_e: u.convert_to(u.electron_rest_mass, u.kilogram)}        # sums need kg
close_to(evaluate(E_a, E_AMB.subs(hydrogen), {**discharge, **in_kg}, u.volt / u.meter), 0.897,
         source=":497")
D_a_value = evaluate(D_a, D_AMB.subs(hydrogen), {**discharge, **in_kg}, u.meter**2 / u.second)
close_to(D_a_value, 1.82e1, source=":501")
close_to(evaluate(sp.Abs(Gamma_a), -D_AMB.subs(hydrogen) * g_n, {**discharge, **in_kg},
                  1 / (u.meter**2 * u.second)), 1.82e17, source=":504")

# %% Magnetized diffusion
section("Diffusion across a magnetic field", "10-diffusion.typ:604")
OM = sp.Symbol("Omega_s", real=True)
D_S = k_B * T / (m * nu)                         # unmagnetized D_s (line 304), shared with plots
D_PERP = D_S / (1 + (OM / nu) ** 2)              # line 626
D_HALL = D_S * (OM / nu) / (1 + (OM / nu) ** 2)
q_m, B_m = sp.Symbol("q", real=True), sp.Symbol("B", positive=True)
u_x, u_y, E_1, E_2, g_x, g_y = sp.symbols("u_x u_y E_x E_y g_x g_y", real=True)
note("Steady perpendicular balance with friction, B along z, density gradient", sp.Tuple(g_x, g_y))
balance = [sp.Eq(m * nu * u_x, q_m * (E_1 + u_y * B_m) - k_B * T * g_x / n_s),
           sp.Eq(m * nu * u_y, q_m * (E_2 - u_x * B_m) - k_B * T * g_y / n_s)]
for eq in balance:
    show(eq)
M = sp.Matrix([[nu, -OM], [OM, nu]])
force = sp.Matrix([q_m / m * E_1 - k_B * T / (m * n_s) * g_x, q_m / m * E_2 - k_B * T / (m * n_s) * g_y])
note("Matrix form with", sp.Eq(OM, q_m * B_m / m), "(both rows asserted):")
show(sp.Eq(sp.MatMul(M, sp.Matrix([u_x, u_y])), force, evaluate=False))
linear = (M * sp.Matrix([u_x, u_y]) - force).subs(OM, q_m * B_m / m)
assert all(sp.expand(linear[k] - (balance[k].lhs - balance[k].rhs) / m) == 0 for k in range(2))
M_inv = sp.simplify(M.inv())
expected_inv = sp.Matrix([[nu, OM], [-OM, nu]]) / (nu**2 + OM**2)
assert all(sp.simplify(M_inv[i, j] - expected_inv[i, j]) == 0 for i in range(2) for j in range(2))
show(sp.Eq(sp.Symbol("M")**-1, M_inv, evaluate=False))
note("Gradient part of the flux", n_s * sp.Symbol("u"), ":")
flux = sp.simplify(n_s * M_inv * sp.Matrix([-k_B * T / (m * n_s) * g_x, -k_B * T / (m * n_s) * g_y]))
D_perp, D_H, Gamma_x = Named("D_perp"), sp.Symbol("D_H"), sp.Symbol("Gamma_x")
coefficients = {D_perp: D_PERP, D_H: D_HALL}
show(sp.Eq(D_perp, D_PERP))
show(sp.Eq(D_H, D_HALL))
agrees_with(flux[0], -D_perp * g_x - D_H * g_y, coefficients, ":618", lhs=Gamma_x)
assert sp.simplify(flux[1] - (-D_PERP * g_y + D_HALL * g_x)) == 0
agrees(k_B * T * nu / (m * (nu**2 + OM**2)), D_S * nu**2 / (nu**2 + OM**2), ":626", lhs=D_perp)
note("Strong field,", sp.Eq(nu, eps * OM), ", to leading order in", eps, ":")
lead = sp.series(D_PERP.subs(OM, nu / eps) / D_S, eps, 0, 3).removeO()
agrees(lead, eps**2, ":635", lhs=D_perp / D_s)
rho_th = sp.Symbol("rho_th")
note("Thermal gyroradius", sp.Eq(rho_th, sp.sqrt(2 * k_B * T / m) / OM), ":")
agrees_with(D_S * (nu / OM) ** 2, nu / 2 * rho_th**2, {rho_th: sp.sqrt(2 * k_B * T / m) / OM}, ":650",
            lhs=D_perp)
note("The Hall flux is divergence free for constant", D_H, ":")
X_, Y_ = sp.symbols("X Y", real=True)
n_XY = sp.Function("n")(X_, Y_)
hall = [-D_HALL * sp.diff(n_XY, Y_), D_HALL * sp.diff(n_XY, X_)]
agrees(sp.diff(hall[0], X_) + sp.diff(hall[1], Y_), 0, ":657",
       lhs=sp.Derivative(-D_H * sp.Derivative(n_XY, Y_), X_) + sp.Derivative(D_H * sp.Derivative(n_XY, X_), Y_))

# %% Example: magnetized electron diffusion
section("Example: magnetized electron diffusion", "10-diffusion.typ:675")
magnetized = {B_m: 1.0e-2 * u.tesla, nu: 1.0e7 / u.second, T: 1.0 * u.electronvolt / u.boltzmann_constant}
note("Electrons,", sp.Eq(B_m, rounded(magnetized[B_m])), ",", sp.Eq(nu, rounded(magnetized[nu])), ",",
     sp.Eq(k_B * T, 1.0 * u.electronvolt))
base = [u.kilogram, u.coulomb, u.second]          # 1 + (Omega/nu)^2 is a sum of quantities
in_base = {e: u.convert_to(u.elementary_charge, base), m_e: u.convert_to(u.electron_rest_mass, base),
           B_m: u.convert_to(magnetized[B_m], base)}
gyro = sp.Abs(e * B_m / m_e)
Omega_e, D_par = sp.Symbol("Omega_e"), Named("D_parallel")
gyro_value = evaluate(sp.Abs(Omega_e), gyro, magnetized, u.second**-1)
close_to(gyro_value, 1.76e9, source=":678")
electrons = {m: m_e, OM: e * B_m / m_e}
D_par_value = evaluate(D_par, D_S.subs(electrons), magnetized, u.meter**2 / u.second)
close_to(D_par_value, 1.76e4, source=":680")
D_perp_value = evaluate(D_perp, D_PERP.subs(electrons), {**magnetized, **in_base},
                        u.meter**2 / u.second)
close_to(D_perp_value, 0.569, source=":683")
close_to(ratio(D_perp / D_par, D_perp_value / D_par_value), 3.23e-5, source=":686")

# %% Classical cross-field diffusion
section("Classical cross-field diffusion", "10-diffusion.typ:831")
sig, B_f, n_f = sp.symbols("sigma B n", positive=True)
Te, Ti = sp.symbols("T_e T_i", positive=True)
D_CL = n_f * k_B * (Te + Ti) / (sig * B_f**2)    # classical, line 849 (shared with plots)
D_BOHM = k_B * Te / (16 * e * B_f)               # empirical Bohm, line 796
UNITS.update({sig: u.siemens / u.meter, B_f: u.tesla, n_f: u.meter**-3, Te: u.kelvin, Ti: u.kelvin})
p_x, p_y = sp.symbols("g_x g_y", real=True)       # components of grad_perp p
j_x, j_y = sp.symbols("j_x j_y")
note("One-fluid Ohm law and force balance, B along z, pressure gradient", sp.Tuple(p_x, p_y))
ohm = [sp.Eq(j_x, sig * (E_1 + u_y * B_f)), sp.Eq(j_y, sig * (E_2 - u_x * B_f))]
force_balance = [sp.Eq(p_x, j_y * B_f), sp.Eq(p_y, -j_x * B_f)]
for eq in ohm + force_balance:
    show(eq)
solved = sp.solve([fb.subs({j_x: ohm[0].rhs, j_y: ohm[1].rhs}) for fb in force_balance], [u_x, u_y],
                  dict=True)[0]
agrees(solved[u_x], E_2 * B_f / B_f**2 - p_x / (sig * B_f**2), ":831", lhs=u_x)
agrees(solved[u_y], -E_1 * B_f / B_f**2 - p_y / (sig * B_f**2), ":831", lhs=u_y)
note("The second term with", sp.Eq(sp.Symbol("p"), n_f * k_B * (Te + Ti)), "at uniform temperatures,",
     sp.Eq(p_x, k_B * (Te + Ti) * sp.Symbol("g_n")), ":")
g_n2 = sp.Symbol("g_n", real=True)
diffusive = n_f * (-(k_B * (Te + Ti) * g_n2) / (sig * B_f**2))
D_cl = Named("D_perp,cl")
agrees(sp.simplify(-diffusive / g_n2), D_CL, ":849", lhs=D_cl)
has_unit(D_CL, u.meter**2 / u.second)
eta = sp.Symbol("eta", positive=True)
agrees(D_CL.subs(sig, 1 / eta), eta * n_f * k_B * (Te + Ti) / B_f**2, ":852", lhs=D_cl)
D_B = Named("D_perp,B")
note("Empirical Bohm estimate")
show(sp.Eq(D_B, D_BOHM))
has_unit(D_BOHM, u.meter**2 / u.second)
note("Scalings with B: classical as the -2 power, Bohm as the -1 power")
agrees(sp.simplify(B_f * sp.diff(D_CL, B_f) / D_CL), -2, ":858",
       lhs=B_f * sp.Derivative(D_cl, B_f) / D_cl)
agrees(sp.simplify(B_f * sp.diff(D_BOHM, B_f) / D_BOHM), -1, ":797",
       lhs=B_f * sp.Derivative(D_B, B_f) / D_B)

# %% Example: classical and Bohm diffusion
section("Example: classical and Bohm diffusion", "10-diffusion.typ:873")
worked = {n_f: 1.0e16 / u.meter**3, Te: 10 * u.electronvolt / u.boltzmann_constant,
          Ti: 10 * u.electronvolt / u.boltzmann_constant, sig: 1.0e5 * u.siemens / u.meter,
          B_f: 1.0e-2 * u.tesla, L: 1.0 * u.meter}
note("Input", sp.Eq(n_f, rounded(worked[n_f])), ",", sp.Eq(k_B * Te, 10 * u.electronvolt), ",",
     sp.Eq(k_B * Ti, 10 * u.electronvolt), ",", sp.Eq(sig, rounded(worked[sig])), ",",
     sp.Eq(B_f, rounded(worked[B_f])), ",", sp.Eq(L, worked[L]))
classical = evaluate(D_cl, D_CL, worked, u.meter**2 / u.second)
close_to(classical, 3.20e-3, source=":876")
bohm = evaluate(D_B, D_BOHM, worked, u.meter**2 / u.second)
close_to(bohm, 6.25e1, source=":879")
close_to(ratio(D_B / D_cl, bohm / classical), 1.95e4, source=":882")
close_to(evaluate(sp.Symbol("tau_D"), L**2 / D_CL, worked, u.second), 3.12e2, source=":885")

# %% Plot: random-walk diffusion
# Green function at t = tau_D and 4 tau_D: the rms width doubles, the peak halves.
tau_D_s = sp.Symbol("tau_D", positive=True)
# x = xi L0, t = tau tau_D with tau_D = L0^2/D, column N0 = sqrt(4 pi) L0 n0.
normalized = GREEN.subs({x: xi * L0, tp: tau * tau_D_s, N0: sp.sqrt(4 * sp.pi) * L0 * n0}) / n0
normalized = sp.simplify(normalized.subs(D, L0**2 / tau_D_s))
profile = sp.lambdify((xi, tau), normalized, "numpy")
rms = sp.lambdify(tau, sp.sqrt(sp.integrate(xi**2 * normalized, (xi, -sp.oo, sp.oo))
                               / sp.integrate(normalized, (xi, -sp.oo, sp.oo))), "numpy")
fig, ax = figure(4.2, 2.4)
xx = np.linspace(-9, 9, 400)
for time, color, style, text, at in [(1, BLUE, "-", r"$t=\tau_D$", (0.5, 0.97)),
                                     (4, ORANGE, "--", r"$t=4\tau_D$", (4.2, 0.36))]:
    ax.plot(xx, profile(xx, time), color=color, ls=style)
    width = rms(time)                            # sqrt(2 t / tau_D)
    height = profile(width, time)
    ax.annotate("", xy=(-width, height), xytext=(width, height),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.9, shrinkA=0, shrinkB=0))
    label(ax, *at, text, color)
ax.text(0, 0.03, r"arrows: $\pm\langle x^2\rangle^{1/2}$", ha="center", fontsize=9, color="#333333")
ax.set_xlim(-9, 9)
ax.set_ylim(0, 1.08)
ax.set_yticks([0, 0.5, 1])
ax.set_xlabel(r"$x/L_0$")
ax.set_ylabel(r"$n/n_0$")
save(fig, "random-walk-diffusion")

# %% Plot: cross-field diffusion versus magnetization
X_mag = sp.Symbol("X", positive=True)            # |Omega_s| / nu_s
suppression = sp.lambdify(X_mag, sp.simplify((D_PERP / D_S).subs(OM, X_mag * nu)), "numpy")
X_example = gyro_value / 1.0e7                   # electrons of the worked example
fig, ax = figure(4.2, 2.6)
xx = np.logspace(-2, 3, 300)
ax.plot(xx, suppression(xx), color=BLUE)
ax.plot([X_example], [suppression(X_example)], "o", color=BLUE, ms=4)
label(ax, X_example * 0.8, suppression(X_example), "worked example", BLUE, ha="right", va="center",
      fontsize=9)
label(ax, 12, 12**-2.0 * 3, r"$\simeq(\nu_s/\Omega_s)^2$", GRAY)
label(ax, 0.012, 0.25, r"$D_{s,\perp}$", BLUE, va="center")
ax.set_xscale("log")
ax.set_yscale("log")
log_ticks(ax.xaxis, -2, 3)
log_ticks(ax.yaxis, -6, 0, 2)
ax.set_ylim(1e-6, 3)
ax.set_xlabel(r"magnetization $|\Omega_s|/\nu_s$")
ax.set_ylabel(r"$D_{s,\perp}/D_s$")
save(fig, "cross-field-diffusion")

# %% Plot: classical and Bohm diffusion side by side
# Worked example: n = 1e16 m^-3, k_B T_e = k_B T_i = 10 eV, sigma = 1e5 S/m.
kT = 10 * 1.602176634e-19
values = {n_f: 1.0e16, sig: 1.0e5, Te: kT / SI_VALUES[k_B], Ti: kT / SI_VALUES[k_B],
          k_B: SI_VALUES[k_B], e: SI_VALUES[e]}
BB = np.logspace(-3, 0, 100)
B_example = 1.0e-2
for name, D_expr, color, style, title, scaling in [
        ("diffusion-classical", D_CL, BLUE, "-", "classical", r"$\propto B^{-2}$"),
        ("diffusion-bohm", D_BOHM, ORANGE, "--", "Bohm", r"$\propto B^{-1}$")]:
    curve = sp.lambdify(B_f, D_expr.subs(values), "numpy")
    fig, ax = figure(2.8, 2.6)
    ax.plot(BB, curve(BB), color=color, ls=style)
    ax.plot([B_example], [curve(B_example)], "o", color=color, ms=4)
    exponent = math.floor(math.log10(curve(B_example)))     # value label at 10 mT
    label(ax, B_example * 1.4, curve(B_example) * 1.5,
          r"$%.2f\cdot10^{%d}$" % (curve(B_example) / 10**exponent, exponent), color, fontsize=9)
    label(ax, 1.3e-3, 3e-6, f"{title} {scaling}", color)
    ax.set_xscale("log")
    ax.set_yscale("log")
    log_ticks(ax.xaxis, -3, 0)
    log_ticks(ax.yaxis, -6, 4, 2)
    ax.set_ylim(1e-6, 1e4)
    ax.set_xlabel(r"$B$ (T)")
    ax.set_ylabel(r"$D_\perp$ (m$^2$/s)")
    save(fig, name)

# %% Plot: ambipolar balance
# Diffusion and field-drift parts of both species fluxes in the worked example.
numbers = {T_a: 1.602e-19 / SI_VALUES[k_B], nu_i: 1.0e7, nu_e: 1.0e9, m_p: 1.67262192369e-27,
           m_e: SI_VALUES[m_e], e: SI_VALUES[e], k_B: SI_VALUES[k_B]}
flux_values = {k: float(val.subs(numbers)) for k, val in hydrogen.items()}
flux_values.update({n_a: 1.0e16, g_n: -1.0e16})
field_value = float(E_AMB.subs(flux_values))
unit = 1e17                                       # m^-2 s^-1
rows = [(float(G.subs(flux_values).subs(E_x, 0)) / unit, float(G.subs(flux_values).subs(E_x, field_value)) / unit)
        for G in (GAMMA_E, GAMMA_I)]
common = float((-D_AMB * g_n).subs(flux_values)) / unit
fig, ax = figure(4.2, 2.0)
ax.axvline(common, color=GRAY, lw=0.9, ls=":")
ax.text(common, 1.55, r"$\Gamma_a$", color=GRAY, ha="center", va="bottom")
for row, (diffusion, total), name in [(1, rows[0], "electrons"), (0, rows[1], "ions")]:
    ax.annotate("", xy=(diffusion, row + 0.12), xytext=(0, row + 0.12),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(total, row - 0.12), xytext=(diffusion, row - 0.12),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6, ls="--", shrinkA=0, shrinkB=0))
    ax.text(-0.4, row, name, ha="right", va="center")
label(ax, rows[0][0] / 2, 1.2, r"diffusion $-D_e\,\partial_x n$", BLUE, ha="center")
label(ax, rows[0][0] / 2, 0.8, r"field drift $-\mu_e n E_a$", ORANGE, ha="center", va="top")
label(ax, rows[1][1] + 0.4, 0, r"ions: diffusion + drift $\mu_i n E_a$", "#333333", va="center",
      fontsize=9)
ax.set_xlim(-0.2, max(r[0] for r in rows) * 1.05)
ax.set_ylim(-0.5, 1.75)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_xlabel(r"particle flux $\Gamma_x$ ($10^{17}$ m$^{-2}$ s$^{-1}$)")
save(fig, "ambipolar-balance")

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 10 · Diffusion")
