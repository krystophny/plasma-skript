# Chapter 5 · Kinetic theory (src/chapters/05-kinetic-theory.typ)
#
# Mean free path and Coulomb collisions, the Maxwellian and its moments, the
# kinetic (Vlasov) equation, Boltzmann equilibrium and the Fermi energy.
# Not checked: the particle-field model restates electrodynamics.

# %% Setup
import sympy as sp
from sympy.physics import units as u

from kinetics import maxwellian, velocity_integral
from notebook import agrees, close_to, evaluate, note, report, section, show
from si import check, eps0, k_B

n_b, sigma, ell, v_rel, m, T, b = sp.symbols("n_b sigma ell v_rel m T b", positive=True)
n_s = sp.Symbol("n_s", positive=True)
v_x, v_y, v_z, u_x, u_y, u_z = sp.symbols("v_x v_y v_z u_x u_y u_z", real=True)
V, U = [v_x, v_y, v_z], [u_x, u_y, u_z]
SI_UNITS = {n_b: u.meter**-3, sigma: u.meter**2, ell: u.meter, v_rel: u.meter / u.second,
            m: u.kilogram, T: u.kelvin, b: u.meter, n_s: u.meter**-3}
PHASE_SPACE_DENSITY = u.second**3 / u.meter**6  # unit of f_s
f_M = maxwellian(n_s, m, k_B * T, V, U)


def over_velocity(integrand):
    """Unevaluated triple velocity integral, for display."""
    return sp.Integral(integrand, *[(v, -sp.oo, sp.oo) for v in V])


def moment(weight):
    """Velocity integral of weight * f_M."""
    return velocity_integral(weight * f_M, V, U)


# %% Survival law and mean free path
section("Survival law and mean free path", script="kinetic-collisions")
S = sp.Function("S")(ell)
note("Fraction of test particles that travel a path", ell, "without a collision")
survival = show(sp.Eq(S.diff(ell), -n_b * sigma * S))
S_ell = agrees(sp.dsolve(survival, S, ics={S.subs(ell, 0): 1}).rhs, sp.exp(-n_b * sigma * ell), lhs=S)
p = sp.Function("p")(ell)
note("First-collision density", sp.Eq(p, -S.diff(ell)))
p_ell = agrees(-S_ell.diff(ell), n_b * sigma * sp.exp(-n_b * sigma * ell), lhs=p)
normalization = sp.Integral(p_ell, (ell, 0, sp.oo))
agrees(normalization.doit(), 1, lhs=normalization)
lambda_mfp = sp.Symbol("lambda_mfp")
mean_path = show(sp.Eq(lambda_mfp, sp.Integral(ell * p_ell, (ell, 0, sp.oo)))).rhs.doit()
agrees(mean_path, 1 / (n_b * sigma), lhs=lambda_mfp)
check(mean_path, 1 / (n_b * sigma), unit=u.meter, units=SI_UNITS)
nu = sp.Symbol("nu")
rate = agrees(v_rel / mean_path, n_b * sigma * v_rel, lhs=nu)
check(rate, rate, unit=1 / u.second, units=SI_UNITS)

# %% Ninety-degree impact parameter
section("Ninety-degree impact parameter", script="kinetic-collisions")
q_a, q_b, m_r, w_orbit, z = sp.symbols("q_a q_b m_r u z", positive=True)
b_0, chi, b_90 = sp.symbols("b_0 chi b_90", positive=True)
note("Repulsive Kepler orbit in", sp.Eq(w_orbit, 1 / sp.Symbol("r")), "with the Coulomb length",
     sp.Eq(b_0, q_a * q_b / (4 * sp.pi * eps0 * m_r * v_rel**2)))
radicand = 1 - b**2 * w_orbit**2 - 2 * b_0 * w_orbit
show(sp.Eq(chi, sp.pi - 2 * sp.Integral(b / sp.sqrt(radicand), (w_orbit, 0, sp.Symbol("u_0")))))
amplitude = sp.sqrt(1 + b_0**2 / b**2)
note("Complete the square with", sp.Eq(z, b * (w_orbit + b_0 / b**2) / amplitude))
assert sp.simplify(radicand - amplitude**2 * (1 - (b * (w_orbit + b_0 / b**2) / amplitude) ** 2)) == 0
orbit_integral = show(sp.Eq(sp.Symbol("I"), sp.Integral(1 / sp.sqrt(1 - z**2),
                                                        (z, b_0 / (b * amplitude), 1)))).rhs
chi_b = show(sp.Eq(chi, sp.simplify(sp.pi - 2 * orbit_integral.doit()))).rhs
note("Ninety degrees,", sp.Eq(chi, sp.pi / 2))
b_90_expr = sp.solve(sp.Eq(chi_b, sp.pi / 2), b)[0]
assert b_90_expr == b_0
b_90_full = agrees(b_90_expr.subs(b_0, q_a * q_b / (4 * sp.pi * eps0 * m_r * v_rel**2)),
                   sp.Abs(q_a * q_b) / (4 * sp.pi * eps0 * m_r * v_rel**2), lhs=b_90, eq="kinetic-b90")
check(b_90_full, b_90_full, unit=u.meter,
      units={**SI_UNITS, q_a: u.coulomb, q_b: u.coulomb, m_r: u.kilogram})
m_a, m_b = sp.symbols("m_a m_b", positive=True)
note("Reduced mass of the relative motion")
reduced = agrees(1 / (1 / m_a + 1 / m_b), m_a * m_b / (m_a + m_b), lhs=m_r)
check(reduced, reduced, unit=u.kilogram, units={m_a: u.kilogram, m_b: u.kilogram})

# %% Coulomb logarithm and deflection frequency
section("Coulomb logarithm and deflection frequency", script="kinetic-collisions")
b_max, b_min, Lambda, v_a = sp.symbols("b_max b_min Lambda v_a", positive=True)
ln_Lambda = sp.log(Lambda)
coulomb_log = show(sp.Eq(ln_Lambda, sp.log(b_max / b_min))).rhs
assert coulomb_log.args[0] == b_max / b_min
check(b_max / b_min, b_max / b_min, unit=u.meter / u.meter, units={b_max: u.meter, b_min: u.meter})
note("Light test particle,", sp.Eq(m_r, m_a), ", and the cumulative small-angle cross section")
b_90_light = q_a * q_b / (4 * sp.pi * eps0 * m_a * v_a**2)
nu_estimate = show(sp.Eq(nu, n_b * sp.pi * b_90**2 * ln_Lambda * v_a)).rhs.subs(b_90, b_90_light)
nu_printed = n_b * q_a**2 * q_b**2 * ln_Lambda / (eps0**2 * m_a**2 * v_a**3)
note("Same scaling as the printed rate, up to a pure number:")
prefactor = show(sp.Eq(nu / sp.Symbol("nu_printed"), sp.simplify(nu_estimate / nu_printed))).rhs
assert prefactor.free_symbols == set(), prefactor
check(nu_printed, nu_printed, unit=1 / u.second,
      units={n_b: u.meter**-3, q_a: u.coulomb, q_b: u.coulomb, m_a: u.kilogram,
             v_a: u.meter / u.second, Lambda: sp.E})  # Lambda is a pure number

# %% Worked example: neutral collisions
section("Worked example: neutral collisions", script="kinetic-collisions")
neutral = {n_b: 1e18 / u.meter**3, sigma: 1e-19 * u.meter**2, v_rel: 1e6 * u.meter / u.second}
note("Input", sp.Eq(n_b, neutral[n_b], evaluate=False), ",", sp.Eq(sigma, neutral[sigma], evaluate=False),
     ",", sp.Eq(v_rel, neutral[v_rel], evaluate=False))
close_to(evaluate(lambda_mfp, mean_path, neutral, u.meter), 10, rtol=1e-9)
close_to(evaluate(nu, rate, neutral, 1 / u.second), 1e5, rtol=1e-9)
L, tau = sp.symbols("L tau", positive=True)
check(ell / L, ell / L, unit=u.meter / u.meter, units={**SI_UNITS, L: u.meter})
nu_s = sp.Symbol("nu", positive=True)
check(nu_s * tau, nu_s * tau, unit=u.second / u.second, units={tau: u.second, nu_s: 1 / u.second})

# %% Maxwellian: units and moments
section("Maxwellian: units and moments", script="kinetic-distribution")
f_M_sym = sp.Function("f_M")(*V)


def average(weight):
    """<weight> = (1/n_s) times the velocity integral of weight * f_M, unevaluated for display."""
    return over_velocity(weight * f_M_sym) / n_s


show(sp.Eq(f_M_sym, f_M))
at_rest = {**{v: 0 for v in V}, **{c: 0 for c in U}}
peak = n_s * (m / (2 * sp.pi * k_B * T)) ** sp.Rational(3, 2)
note("A count per volume of phase space, in", PHASE_SPACE_DENSITY, "; each velocity direction contributes",
     "a Gaussian factor")
check(f_M.subs(at_rest), peak, unit=PHASE_SPACE_DENSITY, units=SI_UNITS)
check(f_M.subs(at_rest) / n_s, peak / n_s, unit=u.second**3 / u.meter**3, units=SI_UNITS)
a, c = sp.Symbol("a", positive=True), sp.Symbol("c", real=True)
gaussian = sp.Integral(sp.exp(-a * c**2), (c, -sp.oo, sp.oo))
G = agrees(gaussian.doit(), sp.sqrt(sp.pi / a), lhs=gaussian)
assert sp.simplify(G**3 - sp.sqrt(sp.pi / a) ** 3) == 0
agrees(moment(1) / n_s, 1, lhs=average(1))
agrees(moment(1), n_s, lhs=over_velocity(f_M_sym))
for v, drift in zip(V, U):
    agrees(moment(v) / n_s, drift, lhs=average(v))
w_x, w_y, w_z = [v - drift for v, drift in zip(V, U)]
note("Pressure tensor from the velocities relative to the drift")
P_xx = agrees(moment(m * w_x**2), n_s * k_B * T, lhs=n_s * average(m * w_x**2))
check(P_xx, P_xx, unit=u.pascal, units=SI_UNITS)
agrees(moment(m * w_x * w_y), 0, lhs=n_s * average(m * w_x * w_y))
variance = agrees(moment(w_z**2) / n_s, k_B * T / m, lhs=average(w_z**2))
note("so the Gaussian width parameter is", sp.Eq(a, m / (2 * k_B * T)))
assert sp.simplify(1 / (2 * a) - variance.subs(T, m / (2 * a * k_B))) == 0

# %% Mean random kinetic energy
section("Mean random kinetic energy", script="kinetic-distribution")
w_sq = w_x**2 + w_y**2 + w_z**2
mean_energy = agrees(moment(m * w_sq / 2) / n_s, sp.Rational(3, 2) * k_B * T,
                     lhs=average(m * w_sq / 2))
check(mean_energy, mean_energy, unit=u.joule, units=SI_UNITS)
note("Kinetic temperature")
agrees(m * moment(w_sq) / n_s, 3 * k_B * T, lhs=m * average(w_sq))
w = sp.Symbol("w", positive=True)  # speed relative to the drift
note("The thermal speed is a width, not the mean speed; over spherical shells of radius", w)
shell = 4 * sp.pi * w**2 * maxwellian(1, m, k_B * T, [w, 0, 0], [0, 0, 0])
mean_speed = show(sp.Eq(sp.Symbol("<w>"), sp.Integral(w * shell, (w, 0, sp.oo)))).rhs.doit()
v_th = sp.sqrt(2 * k_B * T / m)
agrees(sp.simplify(mean_speed / v_th), 2 / sp.sqrt(sp.pi), lhs=sp.Symbol("<w>") / sp.Symbol("v_th"))

# %% Same n, u, T but different f
section("Same n, u, T; different f", script="kinetic-distribution")
s, alpha = sp.symbols("s alpha", real=True)
w_b = sp.Symbol("w", positive=True)
note("One velocity component,", sp.Eq(s, (sp.Symbol("v") - sp.Symbol("u")) / sp.Symbol("v_th")),
     ", f in units of", sp.Symbol("n") / sp.Symbol("v_th"), ": a Maxwellian and two half-density beams at",
     sp.Eq(s, alpha), "and", sp.Eq(s, -alpha))
f_1, f_2 = sp.Function("f_M")(s), sp.Function("f_B")(s)
f_maxwell = show(sp.Eq(f_1, sp.exp(-s**2) / sp.sqrt(sp.pi))).rhs
f_beams = show(sp.Eq(f_2, sum(sp.exp(-((s - sign * alpha) / w_b) ** 2) for sign in (1, -1))
                     / (2 * sp.sqrt(sp.pi) * w_b))).rhs
note("The beam width keeps the variance:", sp.Eq(w_b**2, 1 - 2 * alpha**2))
beam_width = sp.sqrt(1 - 2 * alpha**2)


def s_moment(f, k):
    """k-th moment of a normalized 1D distribution, beam width inserted."""
    m_k = sp.integrate(sp.expand(s**k * f), (s, -sp.oo, sp.oo))
    return sp.simplify(sp.expand(m_k.subs(w_b, beam_width)))


for k, value in [(0, 1), (1, 0), (2, sp.Rational(1, 2))]:  # same n, u and k_B T/m = v_th^2/2
    for f, f_sym in [(f_maxwell, f_1), (f_beams, f_2)]:
        agrees(s_moment(f, k), value, lhs=sp.Integral(s**k * f_sym, (s, -sp.oo, sp.oo)))
note("The fourth moments differ for every", sp.Ne(alpha, 0))
show(sp.Eq(sp.Integral(s**4 * f_1, (s, -sp.oo, sp.oo)), s_moment(f_maxwell, 4)))
agrees(s_moment(f_beams, 4), sp.Rational(3, 4) - 2 * alpha**4,
       lhs=sp.Integral(s**4 * f_2, (s, -sp.oo, sp.oo)))
ALPHA_PLOT = sp.Rational(3, 5)
assert 0 < ALPHA_PLOT < 1 / sp.sqrt(2)

# %% Plot: Maxwellian and two beams with identical n, u and T
import numpy as np

from si import BLUE, ORANGE, figure, label, save

speed = np.linspace(-3, 3, 400)
maxwell_curve = sp.lambdify(s, f_maxwell, "numpy")
beams_curve = sp.lambdify(s, f_beams.subs(w_b, beam_width).subs(alpha, ALPHA_PLOT), "numpy")
fig, ax = figure(3.4, 2.4)
ax.plot(speed, maxwell_curve(speed), color=BLUE)
ax.plot(speed, beams_curve(speed), color=ORANGE, ls="--")
label(ax, 1.35, maxwell_curve(1.35) + 0.04, "Maxwellian", BLUE)
label(ax, -0.95, beams_curve(-0.95) + 0.06, "two beams", ORANGE, ha="right")
ax.set(xlim=(-3, 3), ylim=(0, 0.8), yticks=[0, 0.25, 0.5, 0.75],
       xlabel=r"$(v-u)/v_{\mathrm{th}}$", ylabel=r"$f\,v_{\mathrm{th}}/n$")
save(fig, "moment_ambiguity")

# %% Convective derivative
section("Convective derivative", script="kinetic-derivatives")
t = sp.Symbol("t")
x_t, v_t = sp.Function("x")(t), sp.Function("v")(t)
g, accel = sp.Function("g"), sp.Function("a")
note("Along a characteristic", sp.Eq(x_t.diff(t), v_t), "and", sp.Eq(v_t.diff(t), accel(t, x_t, v_t)))
x, v = sp.symbols("x v")
chain = g(t, x_t, v_t).diff(t).subs({x_t.diff(t): v_t, v_t.diff(t): accel(t, x_t, v_t)})
agrees(chain.subs({x_t: x, v_t: v}).doit(),
       g(t, x, v).diff(t) + v * g(t, x, v).diff(x) + accel(t, x, v) * g(t, x, v).diff(v),
       lhs=sp.Derivative(g(t, x_t, v_t), t))

# %% Normalized free streaming
section("Normalized free streaming", script="kinetic-derivatives")
t_p, x_p, v_p, L_0, v_0 = sp.symbols("t x v L_0 v_0", positive=True)
tau, xi, eta = sp.symbols("tau xi eta")
F = sp.Function("F")
note("Rescale with", sp.Eq(tau, v_0 * t_p / L_0), ",", sp.Eq(xi, x_p / L_0), ",", sp.Eq(eta, v_p / v_0))
f_scaled = F(v_0 * t_p / L_0, x_p / L_0, v_p / v_0)
streaming = sp.simplify((f_scaled.diff(t_p) + v_p * f_scaled.diff(x_p)) * L_0 / v_0)
normalized = show(sp.Eq(F(tau, xi, eta).diff(tau) + eta * F(tau, xi, eta).diff(xi), 0))
assert sp.simplify(streaming - normalized.lhs.subs({tau: v_0 * t_p / L_0, xi: x_p / L_0,
                                                    eta: v_p / v_0}).doit()) == 0
G_free = sp.Function("G")(xi - eta * tau)
note("Every", G_free, "streams freely:")
agrees(sp.simplify(G_free.diff(tau) + eta * G_free.diff(xi)), 0,
       lhs=sp.Derivative(G_free, tau) + eta * sp.Derivative(G_free, xi))

# %% Conservative and convective kinetic equation
section("Conservative and convective kinetic equation", script="kinetic-boltzmann")
y, z_r = sp.symbols("y z", real=True)
x_r = sp.Symbol("x", real=True)
R = [x_r, y, z_r]
q_s = sp.Symbol("q_s", real=True)
f = sp.Function("f")(t, *R, *V)
E_field = sp.Matrix([sp.Function(f"E_{c}")(t, *R) for c in "xyz"])
B_field = sp.Matrix([sp.Function(f"B_{c}")(t, *R) for c in "xyz"])
velocity = sp.Matrix(V)
lorentz = q_s / m * (E_field + velocity.cross(B_field))
vec_E = sp.Matrix(sp.symbols("E_x E_y E_z", real=True))
vec_B = sp.Matrix(sp.symbols("B_x B_y B_z", real=True))
note("Lorentz acceleration", sp.Symbol("a"), "; phase-space flow", sp.Tuple(sp.Symbol("v"), sp.Symbol("a")),
     "has zero divergence:")
div_r = sp.Add(*[sp.Derivative(velocity[i], R[i]) for i in range(3)], evaluate=False)
agrees(div_r.doit(), 0, lhs=div_r, eq="kinetic-convective")
local_lorentz = q_s / m * (vec_E + velocity.cross(vec_B))  # fields at one point in space
div_v = sp.Add(*[sp.Derivative(local_lorentz[i], V[i]) for i in range(3)], evaluate=False)
agrees(sp.expand(div_v.doit()), 0, lhs=div_v, eq="kinetic-convective")
assert sp.expand(sum(lorentz[i].diff(V[i]) for i in range(3))) == 0
conservative = f.diff(t) + sum(sp.diff(f * velocity[i], R[i]) + sp.diff(f * lorentz[i], V[i]) for i in range(3))
convective = (f.diff(t) + sum(velocity[i] * f.diff(R[i]) + lorentz[i] * f.diff(V[i]) for i in range(3)))
note("By the product rule the conservative and the convective (Vlasov) form differ by f times",
     "these divergences, so they agree.")
assert sp.expand(conservative - convective) == 0
gamma = sp.Symbol("gamma", positive=True)
note("A velocity-dependent drag", sp.Eq(sp.Symbol("a"), -gamma * sp.Symbol("v")), "compresses phase space:")
drag = -gamma * velocity
compression = sp.Add(*[sp.Derivative(f * drag[i], V[i]) for i in range(3)], evaluate=False) \
    - sum(drag[i] * f.diff(V[i]) for i in range(3))
agrees(sp.expand(compression.doit()), -3 * gamma * f,
       lhs=f * sp.Add(*[sp.Derivative(drag[i], V[i]) for i in range(3)], evaluate=False))
E_0 = sp.Symbol("E_0", positive=True)
check(q_s / m * E_0, q_s / m * E_0, unit=u.meter / u.second**2,
      units={q_s: u.coulomb, m: u.kilogram, E_0: u.volt / u.meter})

# %% Particle-number conservation
section("Particle-number conservation", script="kinetic-boltzmann")
E_x0, B_z0 = sp.symbols("E_x B_z", real=True)
acceleration = sp.Matrix([q_s / m * E_x0, 0, 0]) + q_s / m * velocity.cross(sp.Matrix([0, 0, B_z0]))
note("Maxwellian in uniform fields", E_x0, "and", B_z0)
velocity_flux = over_velocity(sp.Add(*[sp.Derivative(f_M_sym * acceleration[i], V[i])
                                       for i in range(3) if acceleration[i] != 0], evaluate=False))
flux_divergence = sum(sp.diff(f_M * acceleration[i], V[i]) for i in range(3))
agrees(velocity_integral(flux_divergence, V, U), 0, lhs=velocity_flux)
agrees(moment(1), n_s, lhs=over_velocity(f_M_sym))
agrees(moment(v_x), n_s * u_x, lhs=over_velocity(v_x * f_M_sym))
note("One dimension with", sp.Function("n")(t, x), "and", sp.Function("u")(t, x), ", integrating over",
     sp.Eq(w, sp.Symbol("v") - sp.Function("u")(t, x)))
density, drift = sp.Function("n")(t, x), sp.Function("u")(t, x)
w_1d = sp.Symbol("w", real=True)
f_1d = density * sp.sqrt(m / (2 * sp.pi * k_B * T)) * sp.exp(-m * w_1d**2 / (2 * k_B * T))
f_sym = sp.Function("f")(t, x, w_1d)
kinetic_moment = sp.Integral(sp.Derivative(f_sym, t) + sp.Derivative((drift + w_1d) * f_sym, x),
                             (w_1d, -sp.oo, sp.oo))
agrees(sp.simplify(kinetic_moment.subs(f_sym, f_1d).doit()),
       density.diff(t) + (density * drift).diff(x), lhs=kinetic_moment)

# %% Boltzmann equilibrium in a potential
section("Boltzmann equilibrium in a potential", script="kinetic-equilibrium")
n_0s = sp.Symbol("n_0s", positive=True)
x_1 = sp.Symbol("x", real=True)
Phi = sp.Function("Phi")(x_1)
H = sp.Symbol("H")
energy = show(sp.Eq(H, m * (v_x**2 + v_y**2 + v_z**2) / 2 + q_s * Phi)).rhs
f_eq_sym = sp.Function("f_eq")(x_1, v_x)
equilibrium = show(sp.Eq(sp.Function("f_eq")(H), sp.Mul(
    n_0s, sp.Pow(m / (2 * sp.pi * k_B * T), sp.Rational(3, 2), evaluate=False), sp.exp(-H / (k_B * T)),
    evaluate=False))).rhs
f_eq = equilibrium.subs(H, energy)
note("Stationary Vlasov equation in one dimension")
agrees(sp.simplify(v_x * f_eq.diff(x_1) - q_s / m * Phi.diff(x_1) * f_eq.diff(v_x)), 0,
       lhs=v_x * sp.Derivative(f_eq_sym, x_1) - q_s / m * sp.Derivative(Phi, x_1) * sp.Derivative(f_eq_sym, v_x))
agrees(sp.simplify(velocity_integral(f_eq, V, [0, 0, 0])), n_0s * sp.exp(-q_s * Phi / (k_B * T)),
       lhs=over_velocity(f_eq_sym))
Phi_0 = sp.Symbol("Phi_0", positive=True)
check(q_s * Phi_0 / (k_B * T), q_s * Phi_0 / (k_B * T), unit=u.joule / u.joule,
      units={q_s: u.coulomb, Phi_0: u.volt, T: u.kelvin})

# %% Fermi energy
section("Fermi energy", script="kinetic-equilibrium")
hbar, k_F, n_e, m_e = sp.symbols("hbar k_F n_e m_e", positive=True)
note("Two spin states per k-space cell", (2 * sp.pi) ** 3, "fill a sphere of radius", k_F)
states = show(sp.Eq(n_e, 2 * sp.Rational(4, 3) * sp.pi * k_F**3 / (2 * sp.pi) ** 3))
k_F_expr = show(sp.Eq(k_F, sp.solve(states, k_F)[0])).rhs
E_F = agrees(sp.simplify(hbar**2 * k_F_expr**2 / (2 * m_e)),
             hbar**2 / (2 * m_e) * (3 * sp.pi**2 * n_e) ** sp.Rational(2, 3), lhs=sp.Symbol("E_F"))
quantum_units = {hbar: u.joule * u.second, n_e: u.meter**-3, m_e: u.kilogram, T: u.kelvin}
check(E_F, E_F, unit=u.joule, units=quantum_units)
check(k_B * T / E_F, k_B * T / E_F, unit=u.joule / u.joule, units=quantum_units)  # theta_e

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 5 · Kinetic theory")
