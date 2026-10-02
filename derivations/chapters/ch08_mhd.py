"""Chapter 8, magnetohydrodynamics: src/chapters/08-mhd.typ.

Run `python derivations/ch08_mhd.py` to check every step, or
`pytest derivations` to check every chapter.

Coverage (line in src/chapters/08-mhd.typ -> test):
  70-74, 94-109   mass and charge continuity from species sums -> test_mass_charge_continuity
  78-81, 116-134  summed momentum, rho_q E + j x B              -> test_summed_momentum
                  (full species sum: ch07 test_one_fluid_momentum)
  144-159         example: rho, u_x, j_x                         -> test_example_one_fluid
  255-268         electron momentum -> generalized Ohm law;
                  303-352 derivation steps                       -> test_generalized_ohm
  282-289, 331-342 drag law, eta, sigma                          -> test_drag_resistivity
  363-374         example: eta = 9.01e-6, sigma = 1.11e5         -> test_example_resistivity
  481-497         ideal MHD system (stated model, units)         -> test_linearized_mhd
  508-519, 531-573 linearized equations and closure              -> test_linearized_mhd
  593-604         example: c_s, delta p                          -> test_example_sound
  702-710, 735-765 Faraday + Ohm + Ampere -> resistive induction -> test_resistive_induction
  715, 723, 786-792 R_m = U L / D_B = tau_D / tau_A              -> test_magnetic_reynolds
  771-780         flux through a material surface               -> test_flux_freezing
  802-816         example: D_B, tau_A, tau_D, R_m                -> test_example_reynolds
  908-917, 987-1007 static balance, pressure and tension         -> test_force_balance
  924-942, 1013-1044 B.grad p = j.grad p = 0, j_perp, j_par       -> test_equilibrium_geometry
  949             beta (units)                                   -> test_example_theta_pinch
  958-976, 1051-1080 theta- and z-pinch radial balance           -> test_pinches
  1091-1101       example: p_out = 8.25e5 Pa, beta_in = 2.51     -> test_example_theta_pinch
Not checked: 583-584 (animation parameters, not derived in the text).
"""

import sympy as sp
from sympy.physics import units as u

from ch07_multiple_fluids import (Tex, X, close, cross, curl, div, dot, field, grad, num,
                                  t, vcheck, vec, x, y, z)
import si
from si import Derivation, e, m_e, m_i, mu0


# Units of this file's symbols. Kept local (not in the shared si.UNITS) so that
# symbols with common names in other chapter files cannot clash.
LOCAL = {}


def check(derived, stated, unit=None, units=None):
    """si.check with this file's LOCAL unit table."""
    return si.check(derived, stated, unit=unit, units={**LOCAL, **(units or {})})

# CODATA 2018 values for the worked examples.
CODATA = {e: 1.602176634e-19, m_e: 9.1093837015e-31, m_i: 1.67262192369e-27,
          mu0: 1.25663706212e-6}

nn, eta, nu, Lm, Um = sp.symbols("n eta nu_ei L U", positive=True)
LOCAL.update({nn: u.meter**-3, eta: u.ohm * u.meter, nu: u.second**-1,
              Lm: u.meter, Um: u.meter / u.second})


def lap(g):
    return sum(sp.diff(g, xi, 2) for xi in X)


# ---------------------------------------------------------------------------
# One-fluid variables
# ---------------------------------------------------------------------------
def test_mass_charge_continuity():
    d = Derivation("Mass and charge continuity", "src/chapters/08-mhd.typ:70")
    S = ("e", "i")
    m = {"e": m_e, "i": m_i}
    q = {"e": -e, "i": e}
    n = {s: field(f"n_{s}", f"n_{s}") for s in S}
    U = {s: vec(f"u{s}", f"u_{{{s}}}") for s in S}
    cont = {s: sp.diff(n[s], t) + div([n[s] * U[s][i] for i in range(3)]) for s in S}
    rho = sum(m[s] * n[s] for s in S)
    rho_u = [sum(m[s] * n[s] * U[s][i] for s in S) for i in range(3)]
    # Multiply by m_s and sum (line 98): total mass continuity (line 70).
    check(sum(m[s] * cont[s] for s in S), sp.diff(rho, t) + div(rho_u))
    # Multiply by q_s and sum (line 108): charge continuity (line 74).
    rho_q = sum(q[s] * n[s] for s in S)
    j = [sum(q[s] * n[s] * U[s][i] for s in S) for i in range(3)]
    check(sum(q[s] * cont[s] for s in S), sp.diff(rho_q, t) + div(j))
    d.step("sum m_s (continuity)", sp.Eq(Tex(r"\partial_t\rho + \nabla\cdot(\rho u)"), 0))
    d.step("sum q_s (continuity)", sp.Eq(Tex(r"\partial_t\rho_q + \nabla\cdot j"), 0))


def test_summed_momentum():
    d = Derivation("Summed Lorentz force", "src/chapters/08-mhd.typ:132")
    E, B = vec("E", "E"), vec("B", "B")
    S = ("e", "i")
    q = {"e": -e, "i": e}
    n = {s: field(f"n_{s}", f"n_{s}") for s in S}
    U = {s: vec(f"u{s}", f"u_{{{s}}}") for s in S}
    lhs = [sum(q[s] * n[s] * (E[i] + cross(U[s], B)[i]) for s in S) for i in range(3)]
    rho_q = sum(q[s] * n[s] for s in S)
    j = [sum(q[s] * n[s] * U[s][i] for s in S) for i in range(3)]
    vcheck(lhs, [rho_q * E[i] + cross(j, B)[i] for i in range(3)])
    d.step("sum over species", sp.Eq(Tex(r"\sum_s q_s n_s(E + u_s\times B)"), Tex(r"\rho_q E + j\times B")))


def test_example_one_fluid():
    d = Derivation("Example: one-fluid density, velocity and current", "src/chapters/08-mhd.typ:144")
    n0, ui, ue = 1.0e16, 2.0e5, 1.5e5
    me, mi = CODATA[m_e], CODATA[m_i]
    rho = num(d, "sum_s m_s n_s", r"\rho", n0 * (me + mi))
    ux = num(d, "mass-weighted velocity", "u_x", n0 * (mi * ui + me * ue) / rho)
    jx = num(d, "e n (u_i - u_e)", "j_x", CODATA[e] * n0 * (ui - ue))
    close(rho, "1.674e-11")
    close(ux, "2.00e5")
    close(jx, "80.1")


# ---------------------------------------------------------------------------
# Generalized Ohm law and resistivity
# ---------------------------------------------------------------------------
def test_generalized_ohm():
    d = Derivation("Generalized Ohm law", "src/chapters/08-mhd.typ:264")
    mu = sp.Symbol("mu", positive=True)  # mass ratio m_e/m_i, taken to zero
    n = sp.Symbol("n", positive=True)    # uniform density
    U, J, B, Gp = vec("u", "u"), vec("j", "j"), vec("B", "B"), vec("g", r"(\nabla p_e)")
    # Exact species velocities from rho u = n (m_i u_i + m_e u_e) and j = e n (u_i - u_e).
    ui = [U[k] + mu / (1 + mu) * J[k] / (e * n) for k in range(3)]
    ue = [U[k] - 1 / (1 + mu) * J[k] / (e * n) for k in range(3)]
    me = m_e  # m_e kept in drag and inertia; mu only in the velocity split
    # Linear drag R_e = m_e n nu (u_i - u_e) (line 282).
    Re = [me * n * nu * (ui[k] - ue[k]) for k in range(3)]
    check(Re[0], me * nu * J[0] / e)  # exact for any mass ratio
    # Solve the electron momentum equation (line 255) for E.
    inertia = [sp.diff(ue[k], t) + dot(ue, grad(ue[k])) for k in range(3)]
    Ev = [-cross(ue, B)[k] - Gp[k] / (e * n) + Re[k] / (e * n) - me * inertia[k] / e for k in range(3)]
    eta_ = me * nu / (n * e**2)
    stated = [cross(J, B)[k] / (e * n) - Gp[k] / (e * n) + eta_ * J[k] + me / (e**2 * n) * sp.diff(J[k], t)
              for k in range(3)]
    for k in range(3):
        resid = sp.expand(Ev[k] + cross(U, B)[k] - stated[k])
        # Neglected: bulk acceleration and nonlinear electron inertia, and O(m_e/m_i) terms.
        neglected = -me / e * (sp.diff(U[k], t) + dot(ue, grad(ue[k])))
        check(sp.expand(resid - neglected).subs(mu, 0), 0)
    d.step("electron momentum", sp.Eq(Tex(r"E + u_e\times B"),
           Tex(r"-\frac{\nabla p_e}{e n} + \frac{R_e}{e n} - \frac{m_e}{e}\frac{d u_e}{dt}")))
    d.step("u_e = u - j/(e n)", sp.Eq(Tex(r"u_e\times B"), Tex(r"u\times B - \frac{j\times B}{e n}")))
    d.step("R_e = m_e nu_ei j / e", sp.Eq(Tex(r"\frac{R_e}{e n}"), Tex(r"\eta j")))
    d.step("result", sp.Eq(Tex(r"E + u\times B"), Tex(
        r"\frac{j\times B}{e n} - \frac{\nabla p_e}{e n} + \eta j + \frac{m_e}{e^2 n}\partial_t j")))
    # Unit of the inertia coefficient m_e/(e^2 n) times dj/dt is V/m.
    check(m_e / (e**2 * nn) / sp.Symbol("tau_0"), m_e / (e**2 * nn) / sp.Symbol("tau_0"),
          unit=u.ohm * u.meter, units={sp.Symbol("tau_0"): u.second})


def test_drag_resistivity():
    d = Derivation("Drag and resistivity", "src/chapters/08-mhd.typ:288")
    j = sp.Symbol("j", real=True)
    # Drag per charge density, R_e/(e n), is the field that balances it: E = eta j.
    Re = m_e * nu * j / e
    eta_d = d.eq("R_e/(e n j)", eta, sp.simplify(Re / (e * nn) / j))
    check(eta_d, m_e * nu / (nn * e**2), unit=u.ohm * u.meter)
    check(1 / eta_d, nn * e**2 / (m_e * nu), unit=u.siemens / u.meter)


def test_example_resistivity():
    d = Derivation("Example: resistivity from the collision rate", "src/chapters/08-mhd.typ:363")
    eta_v = num(d, "m_e nu / (n e2)", r"\eta", CODATA[m_e] * 2.54e3 / (1.0e16 * CODATA[e] ** 2))
    close(eta_v, "9.01e-6")
    close(num(d, "1/eta", r"\sigma", 1 / eta_v), "1.11e5")


# ---------------------------------------------------------------------------
# Ideal MHD and its linearization
# ---------------------------------------------------------------------------
def test_linearized_mhd():
    d = Derivation("Linearized ideal MHD", "src/chapters/08-mhd.typ:508")
    ep = sp.Symbol("varepsilon", positive=True)  # perturbation amplitude
    gamma, rho0, p0 = sp.symbols("gamma rho_0 p_0", positive=True)
    B0 = sp.symbols("B_0x B_0y B_0z", real=True)  # uniform equilibrium field
    r1, p1 = field("rho1", r"\delta\rho"), field("p1", r"\delta p")
    u1, b1 = vec("du", r"\delta u"), vec("dB", r"\delta B")
    rho = rho0 + ep * r1
    p = p0 + ep * p1
    U = [ep * c for c in u1]
    B = [B0[k] + ep * b1[k] for k in range(3)]
    first = lambda ex: sp.expand(sp.diff(ex, ep).subs(ep, 0))
    # Mass (line 481) -> line 508.
    mass = sp.diff(rho, t) + div([rho * c for c in U])
    check(first(mass), sp.diff(r1, t) + rho0 * div(u1))
    # Momentum with j = curl B / mu0 (lines 483, 497) -> line 510.
    for k in range(3):
        mom = (rho * (sp.diff(U[k], t) + dot(U, grad(U[k]))) + grad(p)[k]
               - cross(curl(B), B)[k] / mu0)
        stated = rho0 * sp.diff(u1[k], t) + grad(p1)[k] - cross(curl(b1), list(B0))[k] / mu0
        check(first(mom), stated)
        # Induction (line 487) -> line 514.
        ind = sp.diff(B[k], t) - curl(cross(U, B))[k]
        check(first(ind), sp.diff(b1[k], t) - curl(cross(u1, list(B0)))[k])
    check(first(div(B)), div(b1))
    # Adiabatic closure (line 490): first-order change of p rho^-gamma (line 566).
    K = p * rho ** (-gamma)
    dK = sp.simplify(first(K) / (p0 * rho0 ** (-gamma)))
    check(dK, p1 / p0 - gamma * r1 / rho0)
    # Isentropic perturbation dK = 0 gives delta p = c_s^2 delta rho (line 518).
    dp = sp.solve(sp.Eq(dK, 0), p1)[0]
    cs2 = gamma * p0 / rho0
    check(dp, cs2 * r1)
    LOCAL.update({rho0: u.kilogram / u.meter**3, p0: u.pascal})
    check(sp.sqrt(cs2), sp.sqrt(gamma * p0 / rho0), unit=u.meter / u.second, units={gamma: sp.S.One})
    d.step("mass, first order", sp.Eq(sp.Derivative(r1, t) + rho0 * Tex(r"\nabla\cdot\delta u"), 0))
    d.step("momentum, first order", sp.Eq(rho0 * Tex(r"\partial_t\delta u"),
                                          Tex(r"-\nabla\delta p + \frac{(\nabla\times\delta B)\times B_0}{\mu_0}")))
    d.step("induction, first order", sp.Eq(Tex(r"\partial_t\delta B"), Tex(r"\nabla\times(\delta u\times B_0)")))
    d.eq("first order", Tex(r"\frac{\delta(p\rho^{-\gamma})}{p_0\rho_0^{-\gamma}}"), dK)
    d.eq("isentropic", p1, dp)


def test_example_sound():
    d = Derivation("Example: sound speed and pressure perturbation", "src/chapters/08-mhd.typ:593")
    rho0, p0, gam = 1.0e-11, 0.10, 5 / 3
    cs = num(d, "sqrt(gamma p0 / rho0)", "c_s", (gam * p0 / rho0) ** 0.5)
    dp = num(d, "c_s2 delta rho", r"\delta p", cs**2 * 0.010 * rho0)
    close(cs, "1.29e5")
    close(dp, "1.67e-3")
    close(num(d, "delta p / p0", r"\delta p/p_0", dp / p0), "0.0167")


# ---------------------------------------------------------------------------
# Resistive induction and flux freezing
# ---------------------------------------------------------------------------
def test_resistive_induction():
    d = Derivation("Resistive induction equation", "src/chapters/08-mhd.typ:707")
    U, B = vec("u", "u"), vec("B", "B")
    J = [c / mu0 for c in curl(B)]                       # reduced Ampere
    E = [-cross(U, B)[k] + eta * J[k] for k in range(3)]  # Ohm: E + u x B = eta j
    dBdt = [-c for c in curl(E)]                           # Faraday
    for k in range(3):
        stated = curl(cross(U, B))[k] + eta / mu0 * lap(B[k])
        # The difference is -(eta/mu0) grad(div B), zero because div B = 0.
        check(dBdt[k] - stated, -eta / mu0 * grad(div(B))[k])
    d.step("Faraday + Ohm", sp.Eq(Tex(r"\partial_t B"), Tex(r"\nabla\times(u\times B) - \eta\nabla\times j")))
    d.step("Ampere", sp.Eq(Tex(r"-\eta\nabla\times j"), Tex(r"-\frac{\eta}{\mu_0}\nabla\times\nabla\times B")))
    d.step("div B = 0", sp.Eq(Tex(r"\partial_t B"), Tex(r"\nabla\times(u\times B) + \frac{\eta}{\mu_0}\nabla^2 B")))
    check(eta / mu0, eta / mu0, unit=u.meter**2 / u.second)


def test_magnetic_reynolds():
    d = Derivation("Magnetic Reynolds number", "src/chapters/08-mhd.typ:715")
    B_, D = sp.symbols("B D_B", positive=True)
    LOCAL.update({D: u.meter**2 / u.second})
    # Ratio of the scale estimates |curl(u x B)| ~ U B / L and |D_B lap B| ~ D_B B / L^2.
    Rm = d.eq("advection / diffusion", Tex("R_m"), sp.simplify((Um * B_ / Lm) / (D * B_ / Lm**2)))
    tau_A, tau_D = Lm / Um, Lm**2 / D
    check(Rm, Um * Lm / D)
    check(Rm, tau_D / tau_A)
    check(tau_D.subs(D, eta / mu0), mu0 * Lm**2 / eta, unit=u.second)
    check(Um * Lm * mu0 / eta, Um * Lm * mu0 / eta, unit=u.meter / u.meter)


def test_flux_freezing():
    d = Derivation("Flux through a material surface element", "src/chapters/08-mhd.typ:775")
    # Locally linear flow u = A r; the material area element evolves as
    # d(T1 x T2)/dt = (A T1) x T2 + T1 x (A T2) for tangent vectors T1, T2.
    A = sp.Matrix(3, 3, sp.symbols("a_:3:3", real=True))
    T1 = sp.Matrix(sp.symbols("s_:3", real=True))
    T2 = sp.Matrix(sp.symbols("r_:3", real=True))
    dS = T1.cross(T2)
    ddS = (A * T1).cross(T2) + T1.cross(A * T2)
    # Field and its first derivatives at the point (B is linear near r = 0).
    B0 = sp.Matrix(sp.symbols("b_:3", real=True))
    G = sp.Matrix(3, 3, sp.symbols("g_:3:3", real=True))  # G[i, j] = d_j B_i
    Bt = sp.Matrix(sp.symbols("bdot_:3", real=True))      # dB/dt at the point
    r0 = sp.Matrix(sp.symbols("x_:3", real=True))         # position of the element
    Bp, up = B0 + G * r0, A * r0
    # d/dt (B . dS) following the flow: (dB/dt + u.grad B) . dS + B . d(dS)/dt.
    lhs = (Bt + G * up).dot(dS) + Bp.dot(ddS)
    # Stated integrand: [dB/dt + u div B - curl(u x B)] . dS, with
    # curl(u x B) = u div B - B div u + (B.grad) u - (u.grad) B.
    divB, divu = G.trace(), A.trace()
    curl_uxB = up * divB - Bp * divu + A * Bp - G * up
    rhs = (Bt + up * divB - curl_uxB).dot(dS)
    check(sp.expand(lhs), sp.expand(rhs))
    d.step("transport theorem", sp.Eq(Tex(r"\frac{d\Psi_B}{dt}"),
           Tex(r"\int_{S(t)}[\partial_t B - \nabla\times(u\times B)]\cdot dS")))


def test_example_reynolds():
    d = Derivation("Example: magnetic Reynolds number", "src/chapters/08-mhd.typ:802")
    L, U_, eta_v, mu0_v = 10.0, 1.0e5, 9.0e-3, 1.257e-6
    D = num(d, "eta/mu0", "D_B", eta_v / mu0_v)
    tA = num(d, "L/U", r"\tau_A", L / U_)
    tD = num(d, "L2/D_B", r"\tau_D", L**2 / D)
    Rm = num(d, "tau_D / tau_A", "R_m", tD / tA)
    close(D, "7.16e3")
    close(tA, "1.00e-4")
    close(tD, "1.40e-2")
    close(Rm, "1.40e2")
    # mu0 printed as 1.257e-6 H/m agrees with CODATA to the printed digits.
    close(CODATA[mu0], "1.257e-6")


# ---------------------------------------------------------------------------
# Magnetostatic equilibrium
# ---------------------------------------------------------------------------
def test_force_balance():
    d = Derivation("Magnetic pressure and tension", "src/chapters/08-mhd.typ:916")
    B = vec("B", "B")
    B2 = dot(B, B)
    for k in range(3):
        # curl(B) x B = (B.grad) B - grad(B^2/2) (lines 912, 996-1003).
        check(cross(curl(B), B)[k], dot(B, grad(B[k])) - grad(B2 / 2)[k])
    d.step("vector identity", sp.Eq(Tex(r"(\nabla\times B)\times B"), Tex(r"(B\cdot\nabla)B - \nabla\frac{B^2}{2}")))
    d.step("grad p = j x B", sp.Eq(Tex(r"\nabla\left(p + \frac{B^2}{2\mu_0}\right)"), Tex(r"\frac{(B\cdot\nabla)B}{\mu_0}")))
    check(sp.Symbol("B_0") ** 2 / (2 * mu0), sp.Symbol("B_0") ** 2 / (2 * mu0), unit=u.pascal,
          units={sp.Symbol("B_0"): u.tesla})


def test_equilibrium_geometry():
    d = Derivation("Equilibrium geometry and currents", "src/chapters/08-mhd.typ:924")
    B, J = vec("B", "B"), vec("j", "j")
    jxB = cross(J, B)  # = grad p in equilibrium
    # B.grad p = 0 and j.grad p = 0 (line 924).
    check(dot(B, jxB), 0)
    check(dot(J, jxB), 0)
    # B x (j x B) = B^2 j - B (B.j) (line 1028), so j_perp = B x grad p / B^2 (line 931).
    B2 = dot(B, B)
    BxjxB = cross(B, jxB)
    vcheck(BxjxB, [B2 * J[k] - B[k] * dot(B, J) for k in range(3)])
    j_perp = [J[k] - B[k] * dot(B, J) / B2 for k in range(3)]
    vcheck([c / B2 for c in BxjxB], j_perp)
    # div j = 0 from reduced Ampere (div curl = 0).
    check(div(curl(B)), 0)
    # div(j_par B/B) = B.grad(j_par/B) + (j_par/B) div B (line 1044); div B = 0 removes the last term.
    fpar = field("f", r"\frac{j_\parallel}{B}")
    check(div([fpar * B[k] for k in range(3)]), dot(B, grad(fpar)) + fpar * div(B))
    d.step("cross with B", sp.Eq(Tex(r"B\times\nabla p"), Tex(r"B^2 j - B(B\cdot j)")))
    d.eq("solve", Tex(r"j_\perp"), Tex(r"\frac{B\times\nabla p}{B^2}"))
    d.step("div j = 0, div B = 0", sp.Eq(Tex(r"B\cdot\nabla\frac{j_\parallel}{B}"), Tex(r"-\nabla\cdot j_\perp")))


def test_pinches():
    d = Derivation("Theta- and z-pinch balance", "src/chapters/08-mhd.typ:972")
    r = sp.Symbol("r", positive=True)
    xx, yy = sp.symbols("x y", positive=True)
    Bz, Bth = sp.Function("B_z"), sp.Function("B_theta")
    rr = sp.sqrt(xx**2 + yy**2)
    er = [xx / rr, yy / rr, 0]
    eth = [-yy / rr, xx / rr, 0]
    to_r = lambda ex: sp.simplify(ex.subs({xx: r, yy: 0}).doit())

    def curl2(a):  # curl for fields depending on (x, y) only
        return [sp.diff(a[2], yy), -sp.diff(a[2], xx), sp.diff(a[1], xx) - sp.diff(a[0], yy)]

    # theta-pinch: B = B_z(r) e_z; j = curl B / mu0 (line 1053).
    B = [0, 0, Bz(rr)]
    J = [c / mu0 for c in curl2(B)]
    j_th = to_r(dot(J, eth))
    check(j_th, -sp.diff(Bz(r), r) / mu0)
    # Radial balance dp/dr = (j x B) . e_r (line 1057) gives line 972.
    f_r = to_r(dot(cross(J, B), er))
    d.eq("theta-pinch, (j x B)_r", Tex(r"\frac{dp}{dr}"), f_r)
    check(f_r, -sp.diff(Bz(r) ** 2 / (2 * mu0), r))
    # z-pinch: B = B_theta(r) e_theta; j_z = (1/(mu0 r)) d(r B_theta)/dr (line 1072).
    B = [Bth(rr) * c for c in eth]
    J = [c / mu0 for c in curl2(B)]
    check(to_r(J[2]), sp.diff(r * Bth(r), r) / (mu0 * r))
    f_r = to_r(dot(cross(J, B), er))
    check(f_r, -Bth(r) / (mu0 * r) * sp.diff(r * Bth(r), r))  # line 1076
    d.eq("z-pinch, (j x B)_r", Tex(r"\frac{dp}{dr}"), f_r)
    # Stated (line 976): d/dr(p + B_th^2/(2 mu0)) + B_th^2/(mu0 r) = 0 with dp/dr = f_r.
    check(f_r + sp.diff(Bth(r) ** 2 / (2 * mu0), r) + Bth(r) ** 2 / (mu0 * r), 0)



def test_example_theta_pinch():
    d = Derivation("Example: theta-pinch pressure balance", "src/chapters/08-mhd.typ:1091")
    p_in, B_in, B_out = 1.00e6, 1.00, 1.20
    # p + B^2/(2 mu0) is constant across the theta-pinch.
    p_out = num(d, "p + B2/(2 mu0) constant", r"p_{\mathrm{out}}",
                p_in + (B_in**2 - B_out**2) / (2 * CODATA[mu0]))
    beta = num(d, "2 mu0 p / B2", r"\beta_{\mathrm{in}}", 2 * CODATA[mu0] * p_in / B_in**2)
    close(p_out, "8.25e5")
    close(beta, "2.51")
    pp, BB = sp.symbols("p_0 B_0", positive=True)
    check(2 * mu0 * pp / BB**2, 2 * mu0 * pp / BB**2, unit=u.meter / u.meter,
          units={pp: u.pascal, BB: u.tesla})


if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
