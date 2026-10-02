# Chapter 6 · Velocity moments (src/chapters/06-moments.typ)
#
# The moment equations are checked on an explicit test distribution (fluids.py):
# velocity integrals of the kinetic equation are done term by term, so the
# integration by parts in velocity space is verified, not assumed.

# %% Setup
import sympy as sp
from sympy.physics import units as u

import si
from fluids import (EPS_DEF, F_W, W_DEF, W_REL, A, B, E, F, KINETIC, P, SHAPE, SIGMA, S, U,
                    Partial, VelocityIntegral, W, X, cross, div, dot, eps, f, field,
                    gauss_moment, integrate, kappa, lam, m_s, moment, moment_values, moments,
                    n, q, q_s, rounded, t, tdiv, v, vec, vint, x)
from notebook import agrees, close_to, evaluate, note, report, section, show

k_B = si.k_B
w = W_REL                                    # random velocity v - u
v2, w2 = dot(v, v), dot(w, w)
C = sp.Symbol("C")                           # collision term
T_t, T_r, T_v = sp.symbols("T_t T_r T_v")    # time, flux and force terms
C_mass, M_x = sp.symbols("C M_x")             # mass and momentum balances


def same(a, b):
    """a == b, with derivatives evaluated (used for the asserted components)."""
    return sp.simplify(sp.expand((a - b).doit())) == 0


_, _, P_test, _ = moments()
MOMENTS = moment_values()                    # P_ij, q_i, eps, W, F_i on the test f


def agrees_in_moments(derived, printed, lhs, eq=""):
    """agrees() for a statement written with P, q, W, epsilon: the test values
    are inserted for the comparison, the display keeps the compact notation."""
    residual = derived - printed.subs(MOMENTS).doit()   # must vanish
    return agrees(residual + printed, printed, lhs=lhs, eq=eq)


# Silent unit checks with plain symbols.
ns, us, qs, ms, ps, Ts, E0 = sp.symbols("n_s u_s q_s m_s p_s T_s E_0", positive=True)
UNITS = {ns: u.meter**-3, us: u.meter / u.second, qs: u.coulomb, ms: u.kilogram,
         ps: u.pascal, Ts: u.kelvin, E0: u.volt / u.meter}


def has_unit(expr, unit):
    si.check(expr, expr, unit=unit, units=UNITS)



def given(values, *more):
    """Note listing the inputs of a worked example, separated by commas."""
    parts = ["Input"]
    for symbol, value in values.items():
        parts += [sp.Eq(symbol, rounded(value)), ","]
    note(*parts[:-1], *more)

# %% Test distribution
section("Test distribution")
note("Drifting anisotropic Gaussian with a skew", kappa, "(heat flux) and a shear",
     lam, "(off-diagonal pressure)")
show(sp.Eq(F, SHAPE))
note("with", sp.Eq(S[0], (v[0] - U[0]) / SIGMA[0]), "and likewise for y, z; all parameters"
     " depend on", sp.Tuple(t, *X), ". Velocity integrals reduce to Gaussian moments, e.g.")
a_w, w_w = sp.symbols("a w", positive=True)
show(sp.Eq(sp.Integral(w_w**2 * sp.exp(-w_w**2 / (2 * a_w**2)), (w_w, -sp.oo, sp.oo)),
           gauss_moment(2)(a_w)))

# %% Density, flow and current
section("Density, flow and current", script="moments-definitions")
density = moment(1)
agrees(integrate(density), n, lhs=density)
current = moment(q_s * v[0])
agrees(integrate(current), q_s * n * U[0], lhs=current)
note("The random velocity", sp.Eq(w[0], v[0] - U[0]), "has zero mean (x shown; y, z asserted)")
agrees(integrate(moment(w[0])), 0, lhs=moment(w[0]))
assert all(integrate(moment(w[i])) == 0 for i in (1, 2))
has_unit(qs * ns, u.coulomb / u.meter**3)
has_unit(qs * ns * us, u.ampere / u.meter**2)
has_unit(ms * ns, u.kilogram / u.meter**3)

# %% Raw second moment
section("Raw second moment", script="moments-definitions")
note("Raw minus central second moment (xy shown; xx and yz asserted)")
for i, j in [(0, 1), (0, 0), (1, 2)]:
    raw, central = moment(m_s * v[i] * v[j]), moment(m_s * w[i] * w[j])
    split = integrate(raw) - integrate(central)
    if (i, j) == (0, 1):
        agrees(split, m_s * n * U[i] * U[j], lhs=raw - central)
    else:
        assert same(split, m_s * n * U[i] * U[j])
has_unit(ms * ns * us**2, u.pascal)                  # P_s = m n <w w>

# %% Heat flux as contraction
section("Heat flux as contraction", script="moments-definitions")
heat = moment(m_s * w2 * w[0] / 2)
show(sp.Eq(heat, integrate(heat)))
tensor = [moment(m_s * w[0] * w[j] * w[j]) for j in range(3)]   # Q_xjj
agrees(sum(integrate(Q) for Q in tensor) / 2, integrate(heat), lhs=sum(tensor) / 2)
assert same(sum(integrate(moment(m_s * w[1] * w[j] ** 2)) for j in range(3)) / 2,
            integrate(moment(m_s * w2 * w[1] / 2)))

# %% Continuity
section("Continuity from the zeroth moment", script="moments-continuity")
note("Kinetic equation with the Lorentz acceleration (x component; y, z alike)")
show(sp.Eq(A[0], q_s / m_s * (E[0] + cross(v, B)[0])))
show(sp.Eq(KINETIC, C))
time = VelocityIntegral(Partial(F, t))
flux = VelocityIntegral(sum(Partial(v[j] * F, X[j]) for j in range(3)))
force = VelocityIntegral(sum(Partial(A[j] * F, v[j]) for j in range(3)))
agrees(integrate(time), Partial(n, t), lhs=time, eq="moments-continuity-terms")
agrees(integrate(flux), sum(Partial(n * U[j], X[j]) for j in range(3)), lhs=flux)
note("Integration by parts in velocity: the force term vanishes")
agrees(integrate(force), 0, lhs=force)
note("Collisions conserve particles,", sp.Eq(VelocityIntegral(C), 0), "; the sum is continuity")
number = integrate(VelocityIntegral(KINETIC))
agrees(number, Partial(n, t) + sum(Partial(n * U[j], X[j]) for j in range(3)),
       lhs=sp.S.Zero)
note("Times", m_s, "gives mass continuity; times", q_s, "summed over two species gives charge"
     " continuity (both asserted)")
assert same(m_s * number, sp.diff(m_s * n, t) + div([m_s * n * U[i] for i in range(3)]))
n2, U2 = field("n_2"), vec("u_2")
q1, q2 = sp.symbols("q_1 q_2", real=True)
cont = lambda nn, uu: sp.diff(nn, t) + div([nn * uu[i] for i in range(3)])
rho_q = q1 * n + q2 * n2
j_q = [q1 * n * U[i] + q2 * n2 * U2[i] for i in range(3)]
assert same(q1 * cont(n, U) + q2 * cont(n2, U2), sp.diff(rho_q, t) + div(j_q))

# %% Example: particle flux
section("Example: particle flux to a collector", script="moments-continuity")
n_0, u_0, area = sp.symbols("n_0 u_0 A", positive=True)
Gamma, Ndot = sp.symbols("Gamma_s Ndot_s")
collector = {n_0: 1.0e16 / u.meter**3, u_0: 2.0e5 * u.meter / u.second, area: 1.0e-4 * u.meter**2}
given(collector)
close_to(evaluate(Gamma, n_0 * u_0, collector, 1 / (u.meter**2 * u.second)), 2.0e21)
close_to(evaluate(Ndot, n_0 * u_0 * area, collector, 1 / u.second), 2.0e17)

# %% Momentum equation
section("Momentum equation from the first moment", script="moments-momentum")
note("Weight the kinetic equation with", m_s * v[0], "and integrate (x shown; y, z asserted)")
for i in range(3):
    time = VelocityIntegral(m_s * v[i] * Partial(F, t))
    flux = VelocityIntegral(m_s * v[i] * sum(Partial(v[j] * F, X[j]) for j in range(3)))
    force = VelocityIntegral(m_s * v[i] * sum(Partial(A[j] * F, v[j]) for j in range(3)))
    time_term = Partial(m_s * n * U[i], t)
    flux_term = sum(Partial(m_s * n * U[i] * U[j] + P[i][j], X[j]) for j in range(3))
    lorentz = q_s * n * (E[i] + cross(U, B)[i])
    if i == 0:
        show(sp.Eq(T_t, time))
        agrees(integrate(time), time_term, lhs=T_t)
        show(sp.Eq(T_r, flux))
        agrees_in_moments(integrate(flux), flux_term, lhs=T_r)
        note("By parts in velocity the force term becomes the Lorentz force density")
        show(sp.Eq(T_v, force))
        agrees(-integrate(force), lorentz, lhs=-T_v)
    else:
        assert same(integrate(time), time_term)
        assert same(integrate(flux), flux_term.subs(MOMENTS))
        assert same(-integrate(force), lorentz)
R_x = field("R_x")
note("Momentum equation, x component, with the collisional friction", R_x)
show(sp.Eq(T_t + T_r + T_v, R_x))

# %% Material momentum
section("Material form of the momentum equation", script="moments-momentum")
rho = field("rho_s")
note("Subtract", U[0], "times mass continuity from the conservative form (x shown)")
conservative = show(sp.Eq(M_x, Partial(rho * U[0], t)
                          + sum(Partial(rho * U[0] * U[j], X[j]) for j in range(3)))).rhs
continuity = show(sp.Eq(C_mass, Partial(rho, t)
                        + sum(Partial(rho * U[j], X[j]) for j in range(3)))).rhs
agrees((conservative - U[0] * continuity).doit(),
       rho * (Partial(U[0], t) + sum(U[j] * Partial(U[0], X[j]) for j in range(3))),
       lhs=M_x - U[0] * C_mass)

# %% Example: electric force density
section("Example: electric force density", script="moments-momentum")
f_E = sp.Symbol("f_E,x")
field_input = {n_0: 1.0e16 / u.meter**3, E0: 6.00e4 * u.volt / u.meter}
given(field_input)
close_to(evaluate(f_E, n_0 * si.e * E0, field_input,
                  u.newton / u.meter**3), 96.1)
has_unit(ns * qs * E0, u.newton / u.meter**3)

# %% Energy moments
section("Energy density and energy flux", script="moments-energy")
note("Internal energy is half the trace of the pressure tensor")
show(sp.Eq(eps, EPS_DEF))
agrees_in_moments(integrate(W_DEF), m_s * n * dot(U, U) / 2 + eps, lhs=W_DEF)
note("Raw energy flux = convected energy", W, "+ pressure work + heat flux (x shown; y, z asserted)")
for i in range(3):
    energy_flux = moment(m_s * dot(v, v) * v[i] / 2)
    stated = W * U[i] + sum(P[i][j] * U[j] for j in range(3)) + q[i]
    if i == 0:
        agrees_in_moments(integrate(energy_flux), stated, lhs=energy_flux)
    else:
        assert same(integrate(energy_flux), stated.subs(MOMENTS))
has_unit(ms * ns * us**2 / 2, u.joule / u.meter**3)
has_unit(ms * ns * us**3 / 2, u.watt / u.meter**2)

# %% Energy equation
section("Energy equation from the second moment", script="moments-energy")
note("Weight the kinetic equation with", m_s * v2 / 2, "and integrate")
time = VelocityIntegral(m_s * v2 / 2 * Partial(F, t))
flux = VelocityIntegral(m_s * v2 / 2 * sum(Partial(v[j] * F, X[j]) for j in range(3)))
force = VelocityIntegral(m_s * v2 / 2 * sum(Partial(A[j] * F, v[j]) for j in range(3)))
show(sp.Eq(T_t, time))
agrees_in_moments(integrate(time), Partial(W, t), lhs=T_t)
show(sp.Eq(T_r, flux))
agrees_in_moments(integrate(flux), sum(Partial(F_W[j], X[j]) for j in range(3)),
                  lhs=T_r)
note("By parts in velocity; the magnetic force does no work")
by_parts = moment(-m_s * dot(v, A))
assert same(integrate(force), integrate(by_parts))
show(sp.Eq(T_v, force))
show(sp.Eq(T_v, by_parts))
agrees(integrate(by_parts), -q_s * n * dot(U, E), lhs=T_v)
note("Energy equation; inserting the split flux", sp.Eq(F_W[0], W * U[0] + q[0]
     + sum(P[0][j] * U[j] for j in range(3))), "is asserted for all components")
split_flux = [W * U[i] + sum(P[i][j] * U[j] for j in range(3)) + q[i] for i in range(3)]
assert same(integrate(time) + integrate(flux),
            (Partial(W, t) + sum(Partial(split_flux[j], X[j]) for j in range(3))).subs(MOMENTS))
Q_s = field("Q_s")
show(sp.Eq(Partial(W, t) + sum(Partial(F_W[j], X[j]) for j in range(3)),
           q_s * n * dot(U, E) + Q_s))

# %% Isotropic pressure
section("Isotropic pressure", script="moments-energy")
p = field("p_s")
isotropic = {P[i][j]: (p if i == j else 0) for i in range(3) for j in range(3)}
note("Scalar pressure is a third of the trace; isotropic tensor")
show(sp.Eq(sp.Matrix(P), sp.Matrix(P).subs(isotropic), evaluate=False))
agrees((P[0][0] + P[1][1] + P[2][2]).subs(isotropic) / 3, p,
       lhs=(P[0][0] + P[1][1] + P[2][2]) / 3)
divergence = tdiv(P)[0]
agrees(divergence.subs(isotropic).doit(), Partial(p, x), lhs=divergence)
note("Maxwellian part of the test distribution,", sp.Eq(lam, 0))
agrees(P_test[0][0].subs(lam, 0), m_s * n * SIGMA[0] ** 2, lhs=P[0][0])

# %% Internal energy
section("Internal energy and the adiabatic law", script="moments-energy")
eps, Q_s = field("epsilon_s"), field("Q_s")
R = vec("R")
W_tot, W_int = sp.symbols("W_tot W_int")      # total and internal energy balances


def balances(U, P, q, R, E):
    """Residuals (lhs - rhs) of mass, momentum and total energy, and the
    stated bulk and internal balances; rho, eps, Q are fields."""
    force = [q_s / m_s * rho * E[i] for i in range(3)]      # q n E with n = rho/m
    mass = Partial(rho, t) + sum(Partial(rho * U[j], X[j]) for j in range(3))
    momentum = [Partial(rho * U[i], t) + sum(Partial(rho * U[i] * U[j] + P[i][j], X[j])
                                             for j in range(3)) - force[i] - R[i]
                for i in range(3)]
    Wt = rho * dot(U, U) / 2 + eps
    PU = [sum(P[i][j] * U[j] for j in range(3)) for i in range(3)]
    energy = (Partial(Wt, t) + sum(Partial(Wt * U[i] + PU[i] + q[i], X[i]) for i in range(3))
              - dot(U, force) - Q_s)
    PgU = sum(P[i][j] * Partial(U[i], X[j]) for i in range(3) for j in range(3))
    bulk = (Partial(rho * dot(U, U) / 2, t)
            + sum(Partial(rho * dot(U, U) * U[i] / 2, X[i]) for i in range(3))
            + dot(U, tdiv(P)) - dot(U, force) - dot(U, R))
    internal = (Partial(eps, t) + sum(Partial(eps * U[i] + q[i], X[i]) for i in range(3))
                + PgU - (Q_s - dot(U, R)))
    return mass, momentum, energy, PU, PgU, bulk, internal


note("Checked in 3D with a symmetric pressure tensor; shown in 1D, only",
     sp.Tuple(U[0], P[0][0], q[0], R[0]), "nonzero")
Psym = [[P[min(i, j)][max(i, j)] for j in range(3)] for i in range(3)]
mass, mom, energy, PU, PgU, bulk, internal = balances(U, Psym, q, R, E)
assert same(dot(U, tdiv(Psym)), div(PU) - PgU)
assert same(dot(U, mom) - dot(U, U) / 2 * mass, bulk)
assert same(energy - bulk, internal)

zero_yz = {c: 0 for c in (U[1], U[2], q[1], q[2], R[1], R[2])}
one_d = lambda expr: expr.subs(zero_yz)
P1 = [[P[0][0] if i == j == 0 else 0 for j in range(3)] for i in range(3)]
U1, q1, R1 = [U[0], 0, 0], [q[0], 0, 0], [R[0], 0, 0]
mass, mom, energy, PU, PgU, bulk, internal = balances(U1, P1, q1, R1, E)
show(sp.Eq(C_mass, mass))
show(sp.Eq(M_x, mom[0]))
show(sp.Eq(W_tot, energy))
note("Product rule for the pressure work")
agrees(dot(U1, tdiv(P1)), Partial(P[0][0] * U[0], x) - P[0][0] * Partial(U[0], x),
       lhs=U[0] * Partial(P[0][0], x))
note("Bulk kinetic energy from the momentum and mass balances")
agrees((U[0] * mom[0] - U[0]**2 / 2 * mass).doit(), bulk,
       lhs=U[0] * M_x - U[0]**2 / 2 * C_mass)
note("Internal energy: total minus bulk")
show(sp.Eq(W_int, W_tot - (U[0] * M_x - U[0]**2 / 2 * C_mass)))
agrees((energy - bulk).doit(), internal, lhs=W_int)
note("Isotropic closure", sp.Eq(eps, 3 * p / 2), ",", sp.Eq(P[0][0], p), ",", sp.Eq(q[0], 0), ",",
     sp.Eq(Q_s, dot(U1, R1)))
closure = {eps: 3 * p / 2, P[0][0]: p, q[0]: 0, Q_s: dot(U1, R1)}
agrees((2 * internal.subs(closure) / 3).doit(),
       Partial(p, t) + U[0] * Partial(p, x) + 5 * p / 3 * Partial(U[0], x),
       lhs=2 * W_int / 3)
iso3 = {eps: 3 * p / 2, Q_s: dot(U, R), **{q[i]: 0 for i in range(3)},
        **{P[i][j]: (p if i == j else 0) for i in range(3) for j in range(3)}}
_, _, _, _, _, _, internal3 = balances(U, Psym, q, R, E)
assert same(2 * internal3.subs(iso3) / 3,
            sp.diff(p, t) + dot(U, [sp.diff(p, xi) for xi in X]) + 5 * p / 3 * div(U))

# %% Polytropic closure
section("Polytropic closure", script="moments-closures")
gamma = sp.Symbol("gamma", positive=True)
material = lambda g: Partial(g, t) + sum(U[j] * Partial(g, X[j]) for j in range(3))
note("Polytropic law and continuity")
K = sp.Symbol("K")                            # material derivative of p n^-gamma
law = show(sp.Eq(K, material(p * n**-gamma)))
continuity = show(sp.Eq(Partial(n, t), -sum(Partial(n * U[j], X[j]) for j in range(3))))
note("Set", sp.Eq(K, 0), "and eliminate the time derivative of the density")
expanded = sp.expand((n**gamma * law.rhs).doit())
expanded = sp.expand(expanded.subs(sp.Derivative(n, t), continuity.rhs.doit()))
agrees(expanded, material(p) + gamma * p * sum(Partial(U[j], X[j]) for j in range(3)),
       lhs=n**gamma * K)
note("Warm closure", sp.Eq(eps, 3 * p / 2), "with", sp.Eq(p, ns * k_B * Ts), "is an energy density")
has_unit(sp.Rational(3, 2) * ns * k_B * Ts, u.joule / u.meter**3)

# %% BGK collision moments
section("BGK collision moments", script="moments-closures")
nu, sigma_M = sp.symbols("nu_s sigma_M", positive=True)
F_M = field("f_M", t, *X, *v)
maxwellian = n / (2 * sp.pi * sigma_M**2) ** sp.Rational(3, 2) * sp.exp(-dot(w, w) / (2 * sigma_M**2))
note("Maxwellian with the same", sp.Tuple(n, U[0]), "and energy:",
     sp.Eq(sigma_M**2, sum(s**2 for s in SIGMA) / 3))
show(sp.Eq(F_M, maxwellian))
bgk = -nu * (F - F_M)
show(sp.Eq(C, bgk))
matched = sp.sqrt(sum(s**2 for s in SIGMA) / 3)
f_M = maxwellian.subs({w[i]: v[i] - U[i] for i in range(3)}).subs(sigma_M, matched)


def bgk_moment(weight):
    """int weight C_BGK d^3v: f and f_M are integrated against their own Gaussians."""
    return sp.simplify(-nu * (vint(weight * f) - vint(weight * f_M, [matched] * 3)))


for label, weight in [("number", 1), ("momentum", m_s * v[0]),
                            ("energy", m_s * v2 / 2)]:
    agrees(bgk_moment(weight), 0, lhs=VelocityIntegral(weight * bgk))

# %% Example: energy densities
section("Example: energy densities of a drifting ion population", script="moments-energy")
n_i, T_i, u_i, m_p = sp.symbols("n_i T_i u_i m_p", positive=True)
eps_i, W_bulk, W_i = sp.symbols("epsilon_i W_bulk W_i")
ions = {n_i: 1.0e16 / u.meter**3, T_i: 10 * u.electronvolt / u.boltzmann_constant,
        u_i: 1.0e5 * u.meter / u.second}
note("Hydrogen ions,", sp.Eq(n_i, rounded(ions[n_i])), ",", sp.Eq(k_B * T_i, 10 * u.electronvolt), ",",
     sp.Eq(u_i, rounded(ions[u_i])))
internal_i = sp.Rational(3, 2) * n_i * k_B * T_i         # tr(P)/2 with P = n k_B T I
bulk_i = n_i * m_p * u_i**2 / 2
close_to(evaluate(eps_i, internal_i, ions, u.joule / u.meter**3), 0.0240)
close_to(evaluate(W_bulk, bulk_i, ions, u.joule / u.meter**3), 0.0836)
close_to(evaluate(W_i, internal_i + bulk_i, ions, u.joule / u.meter**3), 0.108)

# %% Example: adiabatic compression
section("Example: adiabatic compression", script="moments-closures")
p0, p1, n0_, n1_, T0, T1 = sp.symbols("p_0 p_1 n_0 n_1 T_0 T_1", positive=True)
note("Compress by", sp.Eq(n1_ / n0_, 8), "with", sp.Eq(gamma, sp.Rational(5, 3)))
adiabat = show(sp.Eq(p1 * n1_**-gamma, p0 * n0_**-gamma))
pressure_ratio = sp.solve(adiabat, p1)[0] / p0
compression = {n1_: 8 * n0_, gamma: sp.Rational(5, 3)}
agrees(pressure_ratio.subs(compression), 32, lhs=p1 / p0)
note("Ideal gas", sp.Eq(T1 / T0, (p1 / p0) / (n1_ / n0_)))
agrees((pressure_ratio / (n1_ / n0_)).subs(compression), 4, lhs=T1 / T0)

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 6 · Velocity moments")
