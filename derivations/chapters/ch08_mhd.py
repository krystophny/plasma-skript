# Chapter 8 · Magnetohydrodynamics (src/chapters/08-mhd.typ)
#
# One-fluid sums, the generalized Ohm law, linearized ideal MHD, resistive
# induction and flux freezing, and magnetostatic equilibria (pressure balance).

# %% Setup
import sympy as sp
from sympy.physics import units as u

import si
from fluids import Partial, X, cross, curl, div, dot, field, first_order, grad, lap, rounded, t, vec, x
from notebook import agrees, close_to, evaluate, note, report, section, show

e, m_e, m_i, mu0 = si.e, si.m_e, si.m_i, si.mu0
eta, nu = sp.symbols("eta nu_ei", positive=True)


def same(a, b):
    """a == b, with derivatives evaluated (used for the asserted components)."""
    return sp.simplify(sp.expand((a - b).doit())) == 0


def agrees_with(derived, printed, values, lhs, eq=""):
    """agrees() for a statement written with named quantities: `values` are
    inserted for the comparison, the display keeps the names."""
    residual = derived - printed.subs(values).doit()    # must vanish
    return agrees(residual + printed, printed, lhs=lhs, eq=eq)


def ratio(symbol, value):
    """Show a dimensionless number computed from evaluated quantities."""
    show(sp.Eq(symbol, sp.Float(value, 3)))
    return value


# Silent unit checks with plain symbols.
nn, Lm, Um, tau0, B0_, p0_ = sp.symbols("n L U tau_0 B_0 p_0", positive=True)
UNITS = {nn: u.meter**-3, eta: u.ohm * u.meter, nu: u.second**-1, Lm: u.meter,
         Um: u.meter / u.second, tau0: u.second, B0_: u.tesla, p0_: u.pascal}


def has_unit(expr, unit, extra=None):
    si.check(expr, expr, unit=unit, units={**UNITS, **(extra or {})})


species = ("e", "i")
mass = {"e": m_e, "i": m_i}
charge = {"e": -e, "i": e}
n_s = {s: field(f"n_{s}") for s in species}
u_s = {s: [field(f"u_{s}{c}") for c in "xyz"] for s in species}


def given(values, *more):
    """Note listing the inputs of a worked example, separated by commas."""
    parts = ["Input"]
    for symbol, value in values.items():
        parts += [sp.Eq(symbol, rounded(value)), ","]
    note(*parts[:-1], *more)

# %% Mass and charge continuity
section("Mass and charge continuity", script="mhd-definitions")
C = {s: sp.Symbol(f"C_{s}") for s in species}
continuity = {s: Partial(n_s[s], t) + sum(Partial(n_s[s] * u_s[s][j], X[j]) for j in range(3))
              for s in species}
show(sp.Eq(C["e"], continuity["e"]))
note("and likewise", C["i"], "; one-fluid density and velocity")
rho, U = field("rho"), vec("u")
one_fluid = {rho: sum(mass[s] * n_s[s] for s in species),
             **{U[j]: sum(mass[s] * n_s[s] * u_s[s][j] for s in species)
                / sum(mass[s] * n_s[s] for s in species) for j in range(3)}}
show(sp.Eq(rho, one_fluid[rho]))
show(sp.Eq(U[0], one_fluid[U[0]]))
agrees_with(sum(mass[s] * continuity[s] for s in species),
            Partial(rho, t) + sum(Partial(rho * U[j], X[j]) for j in range(3)), one_fluid, lhs=sum(mass[s] * C[s] for s in species))
rho_q, J = field("rho_q"), vec("j")
charges = {rho_q: sum(charge[s] * n_s[s] for s in species),
           **{J[j]: sum(charge[s] * n_s[s] * u_s[s][j] for s in species) for j in range(3)}}
note("Charge density", sp.Eq(rho_q, charges[rho_q]), "and current", sp.Eq(J[0], charges[J[0]]))
agrees_with(sum(charge[s] * continuity[s] for s in species),
            Partial(rho_q, t) + sum(Partial(J[j], X[j]) for j in range(3)), charges, lhs=sum(charge[s] * C[s] for s in species))

# %% Summed Lorentz force
section("Summed Lorentz force", script="mhd-definitions")
E, B = vec("E"), vec("B")
lorentz = [sum(charge[s] * n_s[s] * (E[i] + cross(u_s[s], B)[i]) for s in species)
           for i in range(3)]
stated = [rho_q * E[i] + cross(J, B)[i] for i in range(3)]
assert all(same(lorentz[i], stated[i].subs(charges)) for i in (1, 2))
note("x component (y, z asserted)")
agrees_with(lorentz[0], stated[0], charges, lhs=lorentz[0])

# %% Example: one-fluid variables
section("Example: one-fluid density, velocity and current", script="mhd-definitions")
n_0, u_i0, u_e0, m_p = sp.symbols("n_0 u_i u_e m_p", positive=True)
rho_0, u_x, j_x = sp.symbols("rho u_x j_x")
beam = {n_0: 1.0e16 / u.meter**3, u_i0: 2.0e5 * u.meter / u.second,
        u_e0: 1.5e5 * u.meter / u.second}
given(beam, "; hydrogen with", sp.Eq(n_s["e"], n_0), "and", sp.Eq(n_s["i"], n_0))
equal = {n_s["e"]: n_0, n_s["i"]: n_0, m_i: m_p}
density = one_fluid[rho].subs(equal)
velocity = sp.simplify(((m_p * u_i0 + m_e * u_e0) * n_0 / density))
close_to(evaluate(rho_0, density, beam, u.kilogram / u.meter**3), 1.674e-11)
electron_kg = {m_e: u.convert_to(u.electron_rest_mass, u.kilogram)}   # sums need kg
close_to(evaluate(u_x, velocity, {**beam, **electron_kg}, u.meter / u.second), 2.00e5)
close_to(evaluate(j_x, e * n_0 * (u_i0 - u_e0), beam, u.ampere / u.meter**2), 80.1)

# %% Generalized Ohm law
section("Generalized Ohm law", script="mhd-ohms-law")
mu = sp.Symbol("mu", positive=True)              # mass ratio m_e/m_i, taken to zero
n = sp.Symbol("n", positive=True)                # uniform density
g = vec("g")                                     # grad p_e
u_e, R_e = [field(f"u_e{c}") for c in "xyz"], [field(f"R_e{c}") for c in "xyz"]
note("Electron momentum balance, x component (y, z alike);", g[0], "is the electron pressure"
     " gradient")
electron = [sp.Eq(m_e * n * (Partial(u_e[k], t) + sum(u_e[j] * Partial(u_e[k], X[j]) for j in range(3))),
                  -e * n * (E[k] + cross(u_e, B)[k]) - g[k] + R_e[k]) for k in range(3)]
show(electron[0])
note("Species velocities from", sp.Tuple(U[0], J[0]), "with", sp.Eq(mu, m_e / m_i),
     "and the linear drag")
velocities = {u_e[k]: U[k] - 1 / (1 + mu) * J[k] / (e * n) for k in range(3)}
u_i = [U[k] + mu / (1 + mu) * J[k] / (e * n) for k in range(3)]
drag = {R_e[k]: m_e * n * nu * (u_i[k] - velocities[u_e[k]]) for k in range(3)}
show(sp.Eq(u_e[0], velocities[u_e[0]]))
show(sp.Eq(R_e[0], drag[R_e[0]]))
agrees(drag[R_e[0]], m_e * nu * J[0] / e, lhs=R_e[0])
E_solved = [sp.solve(electron[k], E[k])[0].subs(drag).subs(velocities).doit() for k in range(3)]
eta_ = m_e * nu / (n * e**2)
ohm = [cross(J, B)[k] / (e * n) - g[k] / (e * n) + eta_ * J[k] + m_e / (e**2 * n) * Partial(J[k], t)
       for k in range(3)]
inertia = [-m_e / e * (Partial(U[k], t) + sum(u_e[j] * Partial(u_e[k], X[j]) for j in range(3)))
           for k in range(3)]                    # bulk acceleration + nonlinear inertia
neglected = [c.subs(velocities).doit() for c in inertia]
for k in (1, 2):
    assert same(sp.expand(E_solved[k] + cross(U, B)[k] - ohm[k] - neglected[k]).subs(mu, 0), 0)
note("Drop the bulk acceleration, the nonlinear electron inertia and terms of order", mu)
N_x = sp.Symbol("N_x")
show(sp.Eq(N_x, inertia[0]))
agrees(sp.expand(E_solved[0] + cross(U, B)[0] - neglected[0]).subs(mu, 0), ohm[0],
       lhs=E[0] + cross(U, B)[0] - N_x)
has_unit(m_e / (e**2 * nn) / tau0, u.ohm * u.meter)

# %% Drag and resistivity
section("Drag and resistivity", script="mhd-ohms-law")
j_ = sp.Symbol("j", real=True)
note("The drag per charge density balances a field", sp.Eq(E[0], eta * j_))
eta_drag = sp.simplify(m_e * nu * j_ / e / (e * nn) / j_)
agrees(eta_drag, m_e * nu / (nn * e**2), lhs=eta)
has_unit(eta_drag, u.ohm * u.meter)
agrees(1 / eta_drag, nn * e**2 / (m_e * nu), lhs=1 / eta)
has_unit(1 / eta_drag, u.siemens / u.meter)

# %% Example: resistivity
section("Example: resistivity from the collision rate", script="mhd-ohms-law")
eta_s, sigma_s = sp.symbols("eta sigma")
collisions = {nn: 1.0e16 / u.meter**3, nu: 2.54e3 / u.second}
given(collisions)
close_to(evaluate(eta_s, eta_drag, collisions, u.ohm * u.meter), 9.01e-6)
close_to(evaluate(sigma_s, 1 / eta_drag, collisions, u.siemens / u.meter), 1.11e5)

# %% Linearized ideal MHD
section("Linearized ideal MHD", script="mhd-linearized")
epsilon = sp.Symbol("epsilon", positive=True)    # perturbation amplitude
gamma, rho0, p0 = sp.symbols("gamma rho_0 p_0", positive=True)
B0 = sp.symbols("B_0x B_0y B_0z", real=True)    # uniform equilibrium field
rho1, p1, u1, B1 = field("rho_1"), field("p_1"), vec("u_1"), vec("B_1")
p_f = field("p")
note("Ideal MHD with the reduced Ampere current (x components shown, y and z asserted)")
show(sp.Eq(J[0], curl(B)[0] / mu0))
mhd_mass = Partial(rho, t) + sum(Partial(rho * U[j], X[j]) for j in range(3))
mhd_momentum = [rho * (Partial(U[k], t) + sum(U[j] * Partial(U[k], X[j]) for j in range(3)))
                + Partial(p_f, X[k]) - cross(curl(B), B)[k] / mu0 for k in range(3)]
mhd_induction = [Partial(B[k], t) - curl(cross(U, B))[k] for k in range(3)]
C_, M_, I_ = sp.symbols("C M_x I_x")              # the three balances, each = 0
show(sp.Eq(C_, mhd_mass))
show(sp.Eq(M_, mhd_momentum[0]))
show(sp.Eq(I_, mhd_induction[0]))
note("Perturb a uniform state at rest; keep the first order in", epsilon)
state = {rho: rho0 + epsilon * rho1, p_f: p0 + epsilon * p1,
         **{U[k]: epsilon * u1[k] for k in range(3)}, **{B[k]: B0[k] + epsilon * B1[k] for k in range(3)}}
show(sp.Eq(rho, state[rho]))
show(sp.Eq(B[0], state[B[0]]))
linear = lambda expr: first_order(expr.subs(state).doit(), epsilon)
C1, M1, I1 = sp.symbols("C_1 M_1x I_1x")            # their first-order parts
agrees(linear(mhd_mass), Partial(rho1, t) + rho0 * sum(Partial(u1[j], X[j]) for j in range(3)), lhs=C1)
for k in range(3):
    momentum1 = rho0 * Partial(u1[k], t) + Partial(p1, X[k]) - cross(curl(B1), list(B0))[k] / mu0
    induction1 = Partial(B1[k], t) - curl(cross(u1, list(B0)))[k]
    if k == 0:
        agrees(linear(mhd_momentum[0]), momentum1, lhs=M1)
        agrees(linear(mhd_induction[0]), induction1, lhs=I1)
    else:
        assert same(linear(mhd_momentum[k]), momentum1)
        assert same(linear(mhd_induction[k]), induction1)
agrees(linear(div(B)), sum(Partial(B1[j], X[j]) for j in range(3)), lhs=div(B))
note("Adiabatic closure: first-order change of", p_f * rho**-gamma)
entropy = sp.simplify(first_order((p_f * rho**-gamma).subs(state), epsilon) / (p0 * rho0**-gamma))
K1 = sp.Symbol("K_1")
agrees(entropy, p1 / p0 - gamma * rho1 / rho0, lhs=K1)
note("Isentropic,", sp.Eq(K1, 0), ":")
pressure1 = sp.solve(sp.Eq(entropy, 0), p1)[0]
c_s = sp.Symbol("c_s", positive=True)
agrees(pressure1, gamma * p0 / rho0 * rho1, lhs=p1)
show(sp.Eq(c_s**2, pressure1 / rho1))
has_unit(sp.sqrt(gamma * p0_ / (nn * m_i)), u.meter / u.second, {gamma: sp.S.One})

# %% Example: sound wave
section("Example: sound speed and pressure perturbation", script="mhd-linearized")
c_sound, dp = sp.symbols("c_s p_1")
gas = {rho0: 1.0e-11 * u.kilogram / u.meter**3, p0: 0.10 * u.pascal,
       gamma: sp.Rational(5, 3), rho1: 1.0e-13 * u.kilogram / u.meter**3}
given(gas)
sound = evaluate(c_sound, sp.sqrt(pressure1 / rho1), gas, u.meter / u.second)
close_to(sound, 1.29e5)
pressure = evaluate(dp, pressure1, gas, u.pascal)
close_to(pressure, 1.67e-3)
close_to(ratio(dp / p0, pressure / 0.10), 0.0167)

# %% Resistive induction
section("Resistive induction equation", script="mhd-flux")
note("Reduced Ampere, resistive Ohm and Faraday (x components; y, z asserted)")
ampere = [curl(B)[k] / mu0 for k in range(3)]
ohm_E = [-cross(U, B)[k] + eta * J[k] for k in range(3)]
show(sp.Eq(J[0], ampere[0]))
show(sp.Eq(E[0], ohm_E[0]))
faraday = [-curl(E)[k] for k in range(3)]
show(sp.Eq(Partial(B[0], t), faraday[0]))
inserted = [c.subs({E[k]: ohm_E[k] for k in range(3)}).doit().subs({J[k]: ampere[k] for k in range(3)})
            .doit() for c in faraday]
stated = [curl(cross(U, B), Partial)[k] + eta / mu0 * lap(B[k], Partial) for k in range(3)]
divB = sum(Partial(B[j], X[j]) for j in range(3))
for k in (1, 2):
    assert same(inserted[k] - stated[k], -eta / mu0 * sp.diff(divB.doit(), X[k]))
note("Stated form: advection by the flow plus resistive diffusion")
S_x, Delta = sp.symbols("S_x Delta_x")
show(sp.Eq(S_x, stated[0]))
note("Faraday minus the stated form is a gradient of the divergence of B, which vanishes:")
agrees(inserted[0] - stated[0], -eta / mu0 * Partial(divB, x),
       lhs=Partial(B[0], t) - S_x)
has_unit(eta / mu0, u.meter**2 / u.second, {mu0: u.henry / u.meter})

# %% Magnetic Reynolds number
section("Magnetic Reynolds number", script="mhd-flux")
B_s, D_B, R_m, tau_A, tau_D = sp.symbols("B D_B R_m tau_A tau_D", positive=True)
note("Scale estimates of advection and diffusion,", sp.Eq(D_B, eta / mu0))
estimate = show(sp.Eq(R_m, (Um * B_s / Lm) / (D_B * B_s / Lm**2)))
agrees(estimate.rhs, Um * Lm / D_B, lhs=R_m)
times = {tau_A: Lm / Um, tau_D: Lm**2 / D_B}
note("Transit time", sp.Eq(tau_A, times[tau_A]), "and diffusion time",
     sp.Eq(tau_D, times[tau_D]))
agrees_with(estimate.rhs, tau_D / tau_A, times, lhs=R_m)
has_unit(times[tau_D].subs(D_B, eta / mu0), u.second, {mu0: u.henry / u.meter})
has_unit(Um * Lm * mu0 / eta, u.meter / u.meter, {mu0: u.henry / u.meter})

# %% Flux freezing
section("Flux through a material surface element", script="mhd-flux")
note("Locally linear flow u = A r and field B = b + G r near the element; the element is spanned"
     " by tangent vectors s, r that move with the flow")
A_m = sp.Matrix(3, 3, sp.symbols("a_:3:3", real=True))
T1, T2 = sp.Matrix(sp.symbols("s_:3", real=True)), sp.Matrix(sp.symbols("r_:3", real=True))
b_0, G = sp.Matrix(sp.symbols("b_:3", real=True)), sp.Matrix(3, 3, sp.symbols("g_:3:3", real=True))
Bdot, r0 = sp.Matrix(sp.symbols("bdot_:3", real=True)), sp.Matrix(sp.symbols("x_:3", real=True))
dS = T1.cross(T2)
show(sp.Eq(sp.Symbol("dS"), dS, evaluate=False))
dS_dt = (A_m * T1).cross(T2) + T1.cross(A_m * T2)
B_at, u_at = b_0 + G * r0, A_m * r0
rate = (Bdot + G * u_at).dot(dS) + B_at.dot(dS_dt)          # d(B . dS)/dt along the flow
curl_uxB = u_at * G.trace() - B_at * A_m.trace() + A_m * B_at - G * u_at
integrand = (Bdot + u_at * G.trace() - curl_uxB).dot(dS)   # [dB/dt + u div B - curl(u x B)] . dS
Psi_dot, I_s = sp.symbols("Psidot I")
note("Material derivative of the flux", Psi_dot, "versus the stated integrand", I_s,
     "with curl(u x B) expanded; all 3 x 3 entries symbolic")
agrees(sp.expand(rate - integrand), 0, lhs=Psi_dot - I_s)

# %% Example: magnetic Reynolds number
section("Example: magnetic Reynolds number", script="mhd-flux")
flow = {Lm: 10.0 * u.meter, Um: 1.0e5 * u.meter / u.second, eta: 9.0e-3 * u.ohm * u.meter}
given(flow)
mu0_value = evaluate(mu0, mu0, {}, u.henry / u.meter, digits=4)
close_to(mu0_value, 1.257e-6)
D_value = evaluate(D_B, eta / mu0, flow, u.meter**2 / u.second)
close_to(D_value, 7.16e3)
tA = evaluate(tau_A, times[tau_A], flow, u.second)
close_to(tA, 1.00e-4)
tD = evaluate(tau_D, times[tau_D].subs(D_B, eta / mu0), flow, u.second)
close_to(tD, 1.40e-2)
close_to(ratio(R_m, tD / tA), 1.40e2)

# %% Magnetic pressure and tension
section("Magnetic pressure and tension", script="mhd-equilibrium")
B2 = dot(B, B)
note("Vector identity for the Lorentz force (x shown; y, z asserted)")
for k in (1, 2):
    assert same(cross(curl(B), B)[k], dot(B, grad(B[k])) - Partial(B2 / 2, X[k]))
K_x = sp.Symbol("K_x")                           # x component of (curl B) x B
show(sp.Eq(K_x, cross(curl(B), B)[0]))
agrees(cross(curl(B), B)[0], sum(B[j] * Partial(B[0], X[j]) for j in range(3)) - Partial(B2 / 2, x), lhs=K_x)
note("The force balance with the reduced Ampere current becomes")
show(sp.Eq(Partial(p_f + B2 / (2 * mu0), x), sum(B[j] * Partial(B[0], X[j]) for j in range(3)) / mu0))
has_unit(B0_**2 / (2 * mu0), u.pascal, {mu0: u.henry / u.meter})

# %% Equilibrium geometry
section("Equilibrium geometry and currents", script="mhd-equilibrium")
jxB = cross(J, B)                                # = grad p in equilibrium
note("Force balance: pressure is constant along field lines and current lines")
show(sp.Eq(Partial(p_f, x), jxB[0]))
agrees(sp.expand(dot(B, jxB)), 0, lhs=dot(B, jxB))
agrees(sp.expand(dot(J, jxB)), 0, lhs=dot(J, jxB))
note("Cross with B (x shown; y, z asserted)")
BxjxB = cross(B, jxB)
for k in (1, 2):
    assert same(BxjxB[k], B2 * J[k] - B[k] * dot(B, J))
agrees(BxjxB[0], B2 * J[0] - B[0] * dot(B, J), lhs=BxjxB[0])
j_perp = [J[k] - B[k] * dot(B, J) / B2 for k in range(3)]
assert all(same(BxjxB[k] / B2, j_perp[k]) for k in range(3))
pressure_gradient = {sp.Derivative(p_f, X[k]): jxB[k] for k in range(3)}
note("Divided by", sp.Symbol("B")**2, "this is the perpendicular current; insert the force balance:")
agrees_with(j_perp[0], cross(B, grad(p_f))[0] / B2, pressure_gradient,
            lhs=field("j_perp_x"))
note("Charge conservation: the divergence of the reduced Ampere current vanishes")
agrees(div(curl(B)), 0, lhs=sum(Partial(curl(B)[k], X[k]) for k in range(3)))
f_par, B_mag = field("f"), sp.Symbol("B", positive=True)
note("Parallel current", sp.Eq(field("j_parallel"), f_par * B_mag), "along B:")
agrees(div([f_par * B[k] for k in range(3)]),
       sum(B[k] * Partial(f_par, X[k]) for k in range(3)) + f_par * divB,
       lhs=sum(Partial(f_par * B[k], X[k]) for k in range(3)))

# %% Theta- and z-pinch
section("Theta- and z-pinch balance", script="mhd-equilibrium")
r = sp.Symbol("r", positive=True)
xx, yy = sp.symbols("x y", positive=True)
B_z, B_th, p_r = (lambda a: field("B_z", a)), (lambda a: field("B_theta", a)), field("p", r)
radius = sp.sqrt(xx**2 + yy**2)
e_r, e_th = [xx / radius, yy / radius, 0], [-yy / radius, xx / radius, 0]
on_axis = lambda expr: sp.simplify(expr.subs({xx: r, yy: 0}).doit())   # evaluate at (r, 0)
curl_xy = lambda a: [sp.diff(a[2], yy), -sp.diff(a[2], xx), sp.diff(a[1], xx) - sp.diff(a[0], yy)]
j_th, j_z = sp.symbols("j_theta j_z")
note("Theta-pinch: axial field", B_z(r), "; current from reduced Ampere in Cartesian components")
B_theta_pinch = [0, 0, B_z(radius)]
J_theta_pinch = [c / mu0 for c in curl_xy(B_theta_pinch)]
agrees(on_axis(dot(J_theta_pinch, e_th)), -Partial(B_z(r), r) / mu0, lhs=j_th)
note("Radial force balance: the pressure gradient equals the radial Lorentz force")
balance = on_axis(dot(cross(J_theta_pinch, B_theta_pinch), e_r))
agrees(balance, -Partial(B_z(r) ** 2 / (2 * mu0), r), lhs=Partial(p_r, r))
note("Z-pinch: azimuthal field", B_th(r))
B_z_pinch = [B_th(radius) * c for c in e_th]
J_z_pinch = [c / mu0 for c in curl_xy(B_z_pinch)]
agrees(on_axis(J_z_pinch[2]), Partial(r * B_th(r), r) / (mu0 * r), lhs=j_z)
pinch = on_axis(dot(cross(J_z_pinch, B_z_pinch), e_r))
agrees(pinch, -B_th(r) / (mu0 * r) * Partial(r * B_th(r), r), lhs=Partial(p_r, r))
note("Magnetic pressure plus tension (hoop force):")
agrees(pinch + Partial(B_th(r) ** 2 / (2 * mu0), r) + B_th(r) ** 2 / (mu0 * r), 0,
       lhs=Partial(p_r, r) + Partial(B_th(r) ** 2 / (2 * mu0), r) + B_th(r) ** 2 / (mu0 * r))

# %% Example: theta-pinch pressure balance
section("Example: theta-pinch pressure balance", script="mhd-equilibrium")
p_in, p_out, B_in, B_out, p_B = sp.symbols("p_in p_out B_in B_out p_B", positive=True)
pinch_values = {p_in: 1.00e6 * u.pascal, B_in: 1.00 * u.tesla, B_out: 1.20 * u.tesla}
mu0_SI = {mu0: u.convert_to(u.magnetic_constant, u.henry / u.meter)}   # sums need SI
given(pinch_values, "; total pressure",
     p_f + B_s**2 / (2 * mu0), "is constant")
outside = sp.expand(sp.solve(sp.Eq(p_out + B_out**2 / (2 * mu0), p_in + B_in**2 / (2 * mu0)), p_out)[0])
show(sp.Eq(p_out, outside))
close_to(evaluate(p_out, outside, {**pinch_values, **mu0_SI}, u.pascal), 8.25e5)
magnetic = evaluate(p_B, B_in**2 / (2 * mu0), pinch_values, u.pascal)
close_to(ratio(sp.Symbol("beta_in"), 1.00e6 / magnetic), 2.51)
has_unit(2 * mu0 * p0_ / B0_**2, u.meter / u.meter, {mu0: u.henry / u.meter})

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 8 · Magnetohydrodynamics")
