# Chapter 7 · Multiple-fluid theory (src/chapters/07-multiple-fluids.typ)
#
# Species moments and their sums, the perpendicular drifts, the parallel
# balance with the Boltzmann relation, and the one-fluid momentum equation.

# %% Setup
import sympy as sp
from sympy.physics import units as u

import si
from fluids import (F_W, KINETIC, P, U, W, W_DEF, X, Partial, VelocityIntegral, cross, curl,
                    div, dot, eps, field, integrate, m_s, moment_values, n, q, q_s, t,
                    rounded, v, vec, x)
from notebook import agrees, close_to, evaluate, note, report, section, show

e, k_B, eps0, mu0 = si.e, si.k_B, si.eps0, si.mu0


def same(a, b):
    """a == b, with derivatives evaluated (used for the asserted components)."""
    return sp.simplify(sp.expand((a - b).doit())) == 0


def agrees_with(derived, printed, values, source, lhs):
    """agrees() for a statement written with named quantities: `values` are
    inserted for the comparison, the display keeps the names."""
    residual = derived - printed.subs(values).doit()    # must vanish
    return agrees(residual + printed, printed, source, lhs=lhs)


# Silent unit checks with plain symbols.
ns, us, qs, ms, ps, Ts = sp.symbols("n_s u_s q_s m_s p_s T_s", positive=True)
Bm, Em, Ls = sp.symbols("B E L", positive=True)
UNITS = {ns: u.meter**-3, us: u.meter / u.second, qs: u.coulomb, ms: u.kilogram,
         ps: u.pascal, Ts: u.kelvin, Bm: u.tesla, Em: u.volt / u.meter, Ls: u.meter}


def has_unit(expr, unit):
    si.check(expr, expr, unit=unit, units=UNITS)



def given(values, *more):
    """Note listing the inputs of a worked example, separated by commas."""
    parts = ["Input"]
    for symbol, value in values.items():
        parts += [sp.Eq(symbol, rounded(value)), ","]
    note(*parts[:-1], *more)

# %% Species moments
section("Species-resolved charge and current", "07-multiple-fluids.typ:107")
n_e, n_i = sp.symbols("n_e n_i", positive=True)
q_e, q_i = sp.symbols("q_e q_i", real=True)
u_e, u_i = sp.symbols("u_e u_i", real=True)
rho_q, j = sp.symbols("rho_q j")
charges = {q_e: -e, q_i: e}
note("Electrons and ions,", sp.Eq(q_e, -e), "and", sp.Eq(q_i, e))
charge = show(sp.Eq(rho_q, q_e * n_e + q_i * n_i))
current = show(sp.Eq(j, q_e * n_e * u_e + q_i * n_i * u_i))
agrees(charge.rhs.subs(charges), e * (n_i - n_e), ":107", lhs=rho_q)
agrees(current.rhs.subs(charges), e * n_i * u_i - e * n_e * u_e, ":108", lhs=j)
has_unit(qs * ns, u.coulomb / u.meter**3)
has_unit(qs * ns * us, u.ampere / u.meter**2)
has_unit(ms * ns, u.kilogram / u.meter**3)

# %% Momentum forms
section("Conservative and material momentum forms", "07-multiple-fluids.typ:202")
rho = field("rho_s")
E, B, R = vec("E"), vec("B"), vec("R")
C_mass, M_x = sp.symbols("C M_x")


def momentum_forms(U, P, R, E, B):
    """Conservative and material residuals of the momentum equation, continuity."""
    force = [q_s * n * (E[i] + cross(U, B)[i]) for i in range(3)]
    mass = Partial(rho, t) + sum(Partial(rho * U[j], X[j]) for j in range(3))
    conservative = [Partial(rho * U[i], t) + sum(Partial(rho * U[i] * U[j] + P[i][j], X[j])
                                                 for j in range(3)) - force[i] - R[i]
                    for i in range(3)]
    material = [rho * (Partial(U[i], t) + sum(U[j] * Partial(U[i], X[j]) for j in range(3)))
                - force[i] + sum(Partial(P[i][j], X[j]) for j in range(3)) - R[i]
                for i in range(3)]
    return mass, conservative, material


mass, conservative, material = momentum_forms(U, P, R, E, B)
for i in range(3):
    assert same(conservative[i] - U[i] * mass, material[i])
note("Checked for all components in 3D; shown in 1D, only", sp.Tuple(U[0], P[0][0], R[0], E[0]),
     "nonzero")
U1 = [U[0], 0, 0]
P1 = [[P[0][0] if i == j == 0 else 0 for j in range(3)] for i in range(3)]
mass, conservative, material = momentum_forms(U1, P1, [R[0], 0, 0], [E[0], 0, 0], [0, 0, 0])
show(sp.Eq(C_mass, mass))
show(sp.Eq(M_x, conservative[0]))
note("Subtract", U[0], "times continuity")
agrees((conservative[0] - U[0] * mass).doit(), material[0], ":210", lhs=M_x - U[0] * C_mass)
has_unit(ms * ns * us**2 / Ls, u.newton / u.meter**3)

# %% Energy balance
section("Species energy balance", "07-multiple-fluids.typ:239")
MOMENTS = moment_values()
T_W, K, C = sp.symbols("T_W K C")             # energy moment, kinetic operator, collisions
note("On the test distribution of Chapter 6, the energy density")
show(sp.Eq(W, W_DEF))
agrees_with(integrate(W_DEF), m_s * n * dot(U, U) / 2 + eps, MOMENTS, ":226", lhs=W)
note("Weight the kinetic equation", sp.Eq(K, C), "with", m_s * dot(v, v) / 2, "and integrate")
show(sp.Eq(K, KINETIC))
show(sp.Eq(T_W, VelocityIntegral(m_s * dot(v, v) / 2 * K)))
energy = VelocityIntegral(m_s * dot(v, v) / 2 * KINETIC)
E_t = vec("E")
agrees_with(integrate(energy),
            Partial(W, t) + sum(Partial(F_W[j], X[j]) for j in range(3)) - q_s * n * dot(U, E_t),
            MOMENTS, ":239", lhs=T_W)
note("Raw energy flux split into convection, pressure work and heat flux (asserted)")
split = [W * U[i] + sum(P[i][j] * U[j] for j in range(3)) + q[i] for i in range(3)]
show(sp.Eq(F_W[0], split[0]))
assert same(integrate(energy), (Partial(W, t) + sum(Partial(split[j], X[j]) for j in range(3))
                                - q_s * n * dot(U, E_t)).subs(MOMENTS))
has_unit(ms * ns * us**3, u.watt / u.meter**2)

# %% Maxwell equations and charge continuity
section("Maxwell equations and charge continuity", "07-multiple-fluids.typ:246")
rho_qf, J = field("rho_q"), vec("j")
gauss = show(sp.Eq(rho_qf, eps0 * sum(Partial(E[k], X[k]) for k in range(3))))
note("Ampere with displacement current, x component (y, z alike)")
ampere = [sp.Eq(J[k], curl(B)[k] / mu0 - eps0 * Partial(E[k], t)) for k in range(3)]
show(ampere[0])
charge_continuity = Partial(rho_qf, t) + sum(Partial(J[k], X[k]) for k in range(3))
inserted = charge_continuity.subs({rho_qf: gauss.rhs, **{J[k]: ampere[k].rhs for k in range(3)}})
agrees(sp.expand(inserted.doit()), 0, ":246", lhs=charge_continuity)
note("Faraday keeps the divergence of B constant:")
agrees(div(curl(E)), 0, ":251", lhs=sum(Partial(-curl(E)[k], X[k]) for k in range(3)))

# %% Example: current
section("Example: current with equal densities", "07-multiple-fluids.typ:321")
n_0, j_x, rho_qx = sp.symbols("n_0 j_x rho_q")
plasma = {n_0: 1.0e16 / u.meter**3, u_i: 2.0e5 * u.meter / u.second,
          u_e: 1.5e5 * u.meter / u.second}
given(plasma, "; equal densities", sp.Eq(n_e, n_0), "and", sp.Eq(n_i, n_0))
equal = {n_e: n_0, n_i: n_0}
assert sp.simplify(charge.rhs.subs(charges).subs(equal)) == 0
show(sp.Eq(rho_q, charge.rhs.subs(charges).subs(equal)))
close_to(evaluate(j_x, current.rhs.subs(charges).subs(equal), plasma, u.ampere / u.meter**2),
         80.1, source=":330")

# %% Perpendicular drift
section("Perpendicular drift balance", "07-multiple-fluids.typ:427")
q_, n_ = sp.symbols("q_s n_s", nonzero=True)
Bv, Ev = sp.symbols("B_x B_y B_z", real=True), sp.symbols("E_x E_y E_z", real=True)
Gp = sp.symbols("g_x g_y g_z", real=True)          # components of grad p_s
B2 = dot(Bv, Bv)
perp = lambda a: [a[i] - Bv[i] * dot(Bv, a) / B2 for i in range(3)]
a_ = sp.symbols("a_1 a_2 a_3", real=True)
assert all(same(l, r) for l, r in zip(cross(cross(a_, Bv), Bv), [-B2 * c for c in perp(a_)]))
c1, c2 = sp.symbols("c_1 c_2")
e1 = cross(Bv, [1, 0, 0])
e2 = cross(Bv, e1)
u_perp = [c1 * e1[i] + c2 * e2[i] for i in range(3)]
balance = [q_ * n_ * (perp(Ev)[i] + cross(u_perp, Bv)[i]) - perp(Gp)[i] for i in range(3)]
general = sp.solve([dot(balance, e1), dot(balance, e2)], [c1, c2], dict=True)[0]
drift_ExB = [c / B2 for c in cross(Ev, Bv)]
drift_dia = [c / (q_ * n_ * B2) for c in cross(Bv, Gp)]
assert all(same(sp.simplify(u_perp[i].subs(general)), drift_ExB[i] + drift_dia[i]) for i in range(3))
note("Solved for a general B and asserted; shown for", sp.Eq(sp.Symbol("B"), Bv[2]),
     "along z, unknowns", sp.Tuple(*sp.symbols("u_x u_y")))
ux, uy, Bz = sp.symbols("u_x u_y B_z")
along_z = {Bv[0]: 0, Bv[1]: 0}
balance_z = [sp.Eq(q_ * n_ * (Ev[0] + uy * Bz), Gp[0]), sp.Eq(q_ * n_ * (Ev[1] - ux * Bz), Gp[1])]
for eq in balance_z:
    show(eq)
solution = sp.solve(balance_z, [ux, uy], dict=True)[0]
for k, sym in enumerate((ux, uy)):
    expected = (drift_ExB[k] + drift_dia[k]).subs(along_z).subs(Bv[2], Bz)
    agrees(solution[sym], expected, ":440", lhs=sym)
note("The first term is the E x B drift, the second the diamagnetic drift")
has_unit(Em / Bm, u.meter / u.second)
has_unit(ps / (Ls * qs * ns * Bm), u.meter / u.second)

# %% Example: drifts
section("Example: E x B and diamagnetic drifts", "07-multiple-fluids.typ:492")
E_0, B_0, g_0, n0_ = sp.symbols("E_0 B_0 g_0 n_0", positive=True)
E_vec, B_vec, g_vec = [E_0, 0, 0], [0, 0, B_0], [g_0, 0, 0]
slab = {E_0: 30.0 * u.volt / u.meter, B_0: 0.0100 * u.tesla,
        g_0: 1.602e-5 * u.pascal / u.meter, n0_: 1.0e14 / u.meter**3}
given(slab, "; E and grad p along x, B along z")
ExB, Bxg = cross(E_vec, B_vec), cross(B_vec, g_vec)
assert ExB[0] == ExB[2] == 0 and Bxg[0] == Bxg[2] == 0
speed = u.meter / u.second
u_E, u_si, u_se = (sp.Symbol(s) for s in ("u_ExB,y", "u_*i,y", "u_*e,y"))
close_to(evaluate(u_E, ExB[1] / B_0**2, slab, speed), -3.00e3, source=":496")
close_to(evaluate(u_si, Bxg[1] / (e * n0_ * B_0**2), slab, speed), 1.00e2, source=":500")
close_to(evaluate(u_se, Bxg[1] / (-e * n0_ * B_0**2), slab, speed), -1.00e2, source=":503")

# %% Diamagnetic current
section("Diamagnetic current", "07-multiple-fluids.typ:589")
qe, qi, ne_, ni_ = sp.symbols("q_e q_i n_e n_i", nonzero=True)
ge, gi = sp.symbols("g_ex g_ey g_ez", real=True), sp.symbols("g_ix g_iy g_iz", real=True)
drift = lambda qq, nn, g: [drift_ExB[i] + cross(Bv, g)[i] / (qq * nn * B2) for i in range(3)]
J_perp = [qe * ne_ * drift(qe, ne_, ge)[i] + qi * ni_ * drift(qi, ni_, gi)[i] for i in range(3)]
charge_s = qe * ne_ + qi * ni_
stated = [charge_s * drift_ExB[i] + (cross(Bv, ge)[i] + cross(Bv, gi)[i]) / B2 for i in range(3)]
assert all(same(J_perp[i], stated[i]) for i in range(3))
neutral = {qi: -qe * ne_ / ni_}
g_sum = [ge[k] + gi[k] for k in range(3)]
assert all(same(J_perp[i].subs(neutral), cross(Bv, g_sum)[i] / B2) for i in range(3))
note("Sum of", sp.Mul(q_, n_), "times the drift over e and i; general B asserted, shown for B along z")
jx = sp.Symbol("j_x")
show(sp.Eq(jx, J_perp[0].subs(along_z).subs(Bv[2], Bz)))
agrees(J_perp[0].subs(along_z).subs(Bv[2], Bz),
       stated[0].subs(along_z).subs(Bv[2], Bz), ":592", lhs=jx)
note("Quasi-neutral,", sp.Eq(charge_s, 0), ": only the diamagnetic current remains")
agrees(sp.simplify(J_perp[0].subs(neutral).subs(along_z).subs(Bv[2], Bz)),
       cross([0, 0, Bz], g_sum)[0] / Bz**2, ":596", lhs=jx)
note("Ideal-gas pressures with equal densities", sp.Eq(sp.Symbol("p_s"), sp.Symbol("n") * k_B * sp.Symbol("T_s")))
nf, Te, Ti = field("n"), field("T_e"), field("T_i")
pressure = Partial(nf * k_B * Te + nf * k_B * Ti, x)
agrees(pressure.doit(), k_B * ((Te + Ti) * Partial(nf, x) + nf * Partial(Te + Ti, x)), ":602",
       lhs=pressure)
has_unit(ps / (Ls * Bm), u.ampere / u.meter**2)

# %% Example: diamagnetic current
section("Example: diamagnetic current density", "07-multiple-fluids.typ:661")
j_star = sp.Symbol("j_*,y")
gradient = {g_0: 3.204e-5 * u.pascal / u.meter, B_0: 0.0100 * u.tesla}
given(gradient)
close_to(evaluate(j_star, Bxg[1] / B_0**2, gradient, u.ampere / u.meter**2), 3.20e-3,
         source=":668")

# %% Parallel momentum equation
section("Parallel momentum equation", "07-multiple-fluids.typ:773")
p = field("p_s")
b = sp.symbols("b_x b_y b_z", real=True)          # constant unit vector along B
B_mag = sp.Symbol("B", positive=True)
B_field = [B_mag * c for c in b]
L, Fv = sp.symbols("L_x L_y L_z"), sp.symbols("F_x F_y F_z")
note("Material momentum balance", sp.Eq(L[0], Fv[0]), "with scalar pressure (x component)")
lhs = [rho * (Partial(U[i], t) + sum(U[j] * Partial(U[i], X[j]) for j in range(3)))
       for i in range(3)]
rhs = [q_s * n * (E[i] + cross(U, B_field)[i]) - Partial(p, X[i]) + R[i] for i in range(3)]
show(sp.Eq(L[0], lhs[0]))
show(sp.Eq(Fv[0], rhs[0]))
note("The magnetic force has no component along b:")
agrees(sp.expand(dot(b, cross(U, B_field))), 0, ":775", lhs=dot(b, cross(U, B_field)))
u_par, E_par, R_par = field("u_parallel"), field("E_parallel"), field("R_parallel")
parallel = {u_par: dot(b, U), E_par: dot(b, E), R_par: dot(b, R)}
note("Project both sides on b, with", sp.Eq(u_par, dot(b, U)), "and likewise", E_par, "and", R_par)
agrees_with(sp.expand(dot(b, lhs)),
            rho * (Partial(u_par, t) + sum(U[j] * Partial(u_par, X[j]) for j in range(3))),
            parallel, ":777", lhs=dot(b, L))
agrees_with(sp.expand(dot(b, rhs)),
            -sum(b[j] * Partial(p, X[j]) for j in range(3)) + q_s * n * E_par + R_par,
            parallel, ":777", lhs=dot(b, Fv))

# %% Boltzmann relation
section("Electron Boltzmann relation", "07-multiple-fluids.typ:793")
s_ = sp.Symbol("s", real=True)                     # arc length along b
T_e = sp.Symbol("T_e", positive=True)
n_s = sp.Function("n_e", positive=True)(s_)
phi = sp.Function("phi", real=True)(s_)
E_s = field("E_parallel", s_)
note("Inertialess, collisionless electrons along the field line")
electron = show(sp.Eq(0, -Partial(n_s * k_B * T_e, s_) - e * n_s * E_s))
E_solved = sp.solve(electron.doit(), E_s)[0]
show(sp.Eq(E_s, E_solved))
agrees(E_solved, -(k_B * T_e / e) * Partial(sp.log(n_s), s_), ":787", lhs=E_s)
note("Insert the potential and integrate along the field line")
show(sp.Eq(E_s, -Partial(phi, s_)))
ode = show(sp.Eq(sp.Derivative(n_s, s_), sp.solve(sp.Eq(-sp.Derivative(phi, s_), E_solved),
                                                  sp.Derivative(n_s, s_))[0]))
phi0, n_e0 = sp.symbols("phi_0 n_e0", real=True)
solution = show(sp.dsolve(ode, n_s))
constant = sp.solve(sp.Eq(solution.rhs.subs(phi, phi0), n_e0), sp.Symbol("C1"), dict=True)[0]
profile = solution.rhs.subs(constant)
agrees(profile, n_e0 * sp.exp(e * (phi - phi0) / (k_B * T_e)), ":793", lhs=n_s)
assert sp.simplify(profile.subs(phi, phi0) - n_e0) == 0
has_unit(k_B * Ts / (e * Ls), u.volt / u.meter)

# %% One-fluid momentum
section("One-fluid momentum equation", "07-multiple-fluids.typ:815")
species = ("e", "i")
mass_s = {s: sp.Symbol(f"m_{s}", positive=True) for s in species}
charge_q = {s: sp.Symbol(f"q_{s}", real=True) for s in species}


def one_fluid(*args):
    """Species fields of `args`; summed species momentum residuals and the
    stated one-fluid form, both per component, with the one-fluid variables."""
    f_ = lambda name: field(name, *args)
    v_ = lambda name: [f_(f"{name}{c}") for c in "xyz"]
    dens = {s: f_(f"n_{s}") for s in species}
    vel = {s: v_(f"u_{s}") for s in species}
    Ps = {s: [[f_(f"P_{s}{a}{b}") for b in "xyz"] for a in "xyz"] for s in species}
    Rs = {s: v_(f"R_{s}") for s in species}
    Ef, Bf = v_("E_"), v_("B_")
    rho_ = sum(mass_s[s] * dens[s] for s in species)
    u_cm = [sum(mass_s[s] * dens[s] * vel[s][i] for s in species) / rho_ for i in range(3)]
    V = {s: [vel[s][i] - u_cm[i] for i in range(3)] for s in species}
    charge_ = sum(charge_q[s] * dens[s] for s in species)
    jv = [sum(charge_q[s] * dens[s] * vel[s][i] for s in species) for i in range(3)]
    P1 = [[sum(Ps[s][i][j] + mass_s[s] * dens[s] * V[s][i] * V[s][j] for s in species)
           for j in range(3)] for i in range(3)]
    total = [sum(Partial(mass_s[s] * dens[s] * vel[s][i], t)
                 + sum(Partial(mass_s[s] * dens[s] * vel[s][i] * vel[s][j] + Ps[s][i][j], X[j])
                       for j in range(3))
                 - charge_q[s] * dens[s] * (Ef[i] + cross(vel[s], Bf)[i]) - Rs[s][i]
                 for s in species) for i in range(3)]
    return dict(dens=dens, vel=vel, rho=rho_, u=u_cm, V=V, charge=charge_, j=jv, P1=P1,
                total=total, E=Ef, B=Bf, R=Rs)


# Full 3D check of all identities and components.
full = one_fluid(t, *X)
rho_V = [sum(mass_s[s] * full["dens"][s] * full["V"][s][i] for s in species) for i in range(3)]
assert all(sp.simplify(c) == 0 for c in rho_V)
for i, j_ in [(0, 0), (0, 1)]:
    assert same(sum(mass_s[s] * full["dens"][s] * full["vel"][s][i] * full["vel"][s][j_]
                    for s in species),
                full["rho"] * full["u"][i] * full["u"][j_]
                + sum(mass_s[s] * full["dens"][s] * full["V"][s][i] * full["V"][s][j_]
                      for s in species))
stated_full = [Partial(full["rho"] * full["u"][i], t)
               + sum(Partial(full["rho"] * full["u"][i] * full["u"][j_] + full["P1"][i][j_], X[j_])
                     for j_ in range(3))
               - full["charge"] * full["E"][i] - cross(full["j"], full["B"])[i]
               - sum(full["R"][s][i] for s in species) for i in range(3)]
assert all(same(full["total"][i], stated_full[i]) for i in range(3))

# Display: x component, fields depending on (t, x) only, named one-fluid variables.
note("Checked in 3D; shown for the x component with fields of", sp.Tuple(t, x), "only")
d1 = one_fluid(t, x)
rho1, ux1, rhoq1 = field("rho", t, x), [field(f"u_{c}", t, x) for c in "xyz"], field("rho_q", t, x)
j1 = [field(f"j_{c}", t, x) for c in "xyz"]
V1 = {s: [field(f"V_{s}{c}", t, x) for c in "xyz"] for s in species}
P11 = field("P_1xx", t, x)
names = {rho1: d1["rho"], rhoq1: d1["charge"], P11: d1["P1"][0][0],
         **{ux1[i]: d1["u"][i] for i in range(3)}, **{j1[i]: d1["j"][i] for i in range(3)},
         **{V1[s][i]: d1["V"][s][i] for s in species for i in range(3)}}
show(sp.Eq(rho1, d1["rho"]))
show(sp.Eq(ux1[0], d1["u"][0]))
show(sp.Eq(V1["e"][0], d1["vel"]["e"][0] - ux1[0]))
note("Relative velocities carry no net momentum")
agrees(sp.simplify(sum(mass_s[s] * d1["dens"][s] * d1["V"][s][0] for s in species)), 0, ":868",
       lhs=sum(mass_s[s] * d1["dens"][s] * V1[s][0] for s in species))
note("so the momentum flux splits into bulk and relative parts")
agrees_with(sum(mass_s[s] * d1["dens"][s] * d1["vel"][s][0] ** 2 for s in species),
            rho1 * ux1[0] ** 2 + sum(mass_s[s] * d1["dens"][s] * V1[s][0] ** 2 for s in species),
            names, ":863", lhs=sum(mass_s[s] * d1["dens"][s] * d1["vel"][s][0] ** 2
                                   for s in species))
show(sp.Eq(P11, sum(field(f"P_{s}xx", t, x) + mass_s[s] * d1["dens"][s] * V1[s][0] ** 2
                    for s in species)))
M_e, M_i = sp.symbols("M_ex M_ix")
note("Sum of the species momentum equations", sp.Eq(M_e + M_i, 0), ":")
agrees_with(d1["total"][0],
            Partial(rho1 * ux1[0], t) + Partial(rho1 * ux1[0] ** 2 + P11, x)
            - rhoq1 * d1["E"][0] - cross(j1, d1["B"])[0] - sum(d1["R"][s][0] for s in species),
            names, ":815", lhs=M_e + M_i)

# %% Example: Boltzmann density
section("Example: Boltzmann density ratio", "07-multiple-fluids.typ:883")
phi1, n_e = sp.symbols("phi_1 n_e")
probe = {phi1: 3.00 * u.volt, phi0: 0 * u.volt, T_e: 3.00 * u.elementary_charge * u.volt / u.boltzmann_constant,
         n_e0: 1.0e16 / u.meter**3}
note("Input", sp.Eq(phi1 - phi0, 3.00 * u.volt), ",", sp.Eq(k_B * T_e, 3.00 * u.electronvolt),
     ",", sp.Eq(n_e0, rounded(probe[n_e0])))
rise = show(sp.Eq(n_e, sp.powsimp(profile.subs(phi, phi1))))
density = evaluate(n_e, rise.rhs, probe, u.meter**-3)
close_to(density, 2.72e16, source=":893")
ratio = sp.Symbol("n_e/n_e0")
show(sp.Eq(ratio, sp.Float(density / 1.0e16, 3)))
close_to(density / 1.0e16, 2.72, source=":889")

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 7 · Multiple-fluid theory")
