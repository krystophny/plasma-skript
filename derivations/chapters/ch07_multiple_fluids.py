"""Chapter 7, multiple-fluid theory: src/chapters/07-multiple-fluids.typ.

Run `python derivations/ch07_multiple_fluids.py` to check every step, or
`pytest derivations` to check every chapter.

Coverage (line in src/chapters/07-multiple-fluids.typ -> test):
  64-66, 94-108  species moments, rho_q, j, hydrogen j      -> test_species_moments
  197-214        continuity, conservative and material
                 momentum forms                             -> test_momentum_forms
  226-242        W_s, eps_s, q_h,s and the energy balance;
                 300-313 derivation steps                   -> test_energy_balance
  246-251        Maxwell equations imply charge continuity  -> test_maxwell_charge_continuity
  258-297        moment derivation (same as Chapter 6)      -> ch06_moments tests
  321-333        example: rho_q = 0, j_x = 80.1 A/m^2       -> test_example_current
  427-474        perpendicular balance, E x B and
                 diamagnetic drifts, (u x B) x B = -B^2 u_perp -> test_perpendicular_drift
  482            r_L/L_perp << 1 (ordering, not checked)
  492-507        example: u_ExB, u_*i, u_*e                 -> test_example_drifts
  589-603        current sum, j_*, grad(p_e + p_i)
                 626-646 derivation steps                   -> test_diamagnetic_current
  661-673        example: j_* = 3.20e-3 A/m^2               -> test_example_diamagnetic_current
  773-777        parallel momentum equation                 -> test_parallel_equation
  782-793        electron balance, E_par, Boltzmann relation;
                 827-854 derivation steps                   -> test_boltzmann_relation
  802-818        one-fluid definitions, summed momentum;
                 859-875 derivation steps                   -> test_one_fluid_momentum
  883-895        example: n_e/n_e0 = 2.72                   -> test_example_boltzmann
"""

import sympy as sp
from sympy.physics import units as u

import si
from si import Derivation, e, k_B


# Units of this file's symbols. Kept local (not in the shared si.UNITS) so that
# symbols with common names in other chapter files cannot clash.
LOCAL = {}


def check(derived, stated, unit=None, units=None):
    """si.check with this file's LOCAL unit table."""
    return si.check(derived, stated, unit=unit, units={**LOCAL, **(units or {})})

# CODATA 2018 values for the worked examples.
CODATA = {e: 1.602176634e-19}


class Tex(sp.Symbol):
    """Display-only symbol whose LaTeX is its name, verbatim."""

    def _latex(self, printer, exp=None):
        return self.name if exp is None else f"{{{self.name}}}^{{{exp}}}"


def num(d, label, name, value):
    """Record a numerical step with four significant digits; return the value."""
    d.eq(label, Tex(name), sp.Float(value, 4))
    return value


def close(value, printed, slack=5e-4):
    """Value agrees with the printed number to half a unit in its last digit."""
    mant = printed.lower().split("e")[0].lstrip("+-")
    digits = len(mant.replace(".", "").lstrip("0"))
    p = float(printed)
    tol = 0.5 * 10 ** (sp.floor(sp.log(abs(p), 10)) - digits + 1) + slack * abs(p)
    assert abs(float(value) - p) <= tol, f"{float(value):.6g} vs printed {printed}"


t, x, y, z = sp.symbols("t x y z", real=True)
X = (x, y, z)
args = (t, x, y, z)


def field(name, tex):
    """Undefined function of (t, x, y, z) that prints as `tex` (no arguments)."""
    def _latex(self, printer, exp=None):
        return tex if exp is None else f"{tex}^{{{exp}}}"

    return sp.Function(name, real=True, __dict__={"_latex": _latex})(*args)


def vec(name, tex):
    return [field(f"{name}_{c}", f"{tex}_{{{c}}}") for c in "xyz"]


def div(a):
    return sum(sp.diff(a[i], X[i]) for i in range(3))


def grad(g):
    return [sp.diff(g, xi) for xi in X]


def curl(a):
    return [sp.diff(a[2], y) - sp.diff(a[1], z), sp.diff(a[0], z) - sp.diff(a[2], x),
            sp.diff(a[1], x) - sp.diff(a[0], y)]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def vcheck(a, b):
    for ai, bi in zip(a, b):
        check(ai, bi)


ns, us, qs, ms, ps, Ts = sp.symbols("n_s u_s q_s m_s p_s T_s", positive=True)
Bm, Em, Ls = sp.symbols("B E L", positive=True)
LOCAL.update({ns: u.meter**-3, us: u.meter / u.second, qs: u.coulomb, ms: u.kilogram,
              ps: u.pascal, Ts: u.kelvin, Bm: u.tesla, Em: u.volt / u.meter, Ls: u.meter})


# ---------------------------------------------------------------------------
# Species variables and the two-fluid equations
# ---------------------------------------------------------------------------
def test_species_moments():
    d = Derivation("Species-resolved charge and current", "src/chapters/07-multiple-fluids.typ:107")
    n_e, n_i = sp.symbols("n_e n_i", positive=True)
    ue, ui = sp.symbols("u_e u_i", real=True)
    # Sum q_s n_s and q_s n_s u_s over s = e, i with q_e = -e, q_i = +e.
    species = [(-e, n_e, ue), (e, n_i, ui)]
    rho_q = d.eq("sum_s q_s n_s", Tex(r"\rho_q"), sum(q * nn for q, nn, _ in species))
    j = d.eq("sum_s q_s n_s u_s", sp.Symbol("j"), sum(q * nn * uu for q, nn, uu in species))
    check(rho_q, e * (n_i - n_e))
    check(j, e * n_i * ui - e * n_e * ue)
    check(qs * ns, qs * ns, unit=u.coulomb / u.meter**3)
    check(qs * ns * us, qs * ns * us, unit=u.ampere / u.meter**2)
    check(ms * ns, ms * ns, unit=u.kilogram / u.meter**3)


def test_momentum_forms():
    d = Derivation("Conservative and material momentum forms",
                   "src/chapters/07-multiple-fluids.typ:202")
    rho, n = field("rho", r"\rho_{s}"), field("n", "n_{s}")
    U, E, B, R = vec("u", "u"), vec("E", "E"), vec("B", "B"), vec("R", "R")
    P = [[field(f"P_{a}{b}", f"P_{{{a}{b}}}") for b in "xyz"] for a in "xyz"]
    q = sp.Symbol("q_s", real=True)
    force = [q * n * (E[i] + cross(U, B)[i]) for i in range(3)]
    cont = sp.diff(rho, t) + div([rho * U[j] for j in range(3)])
    for i in range(3):
        cons = (sp.diff(rho * U[i], t) + sum(sp.diff(rho * U[i] * U[j] + P[i][j], X[j]) for j in range(3))
                - force[i] - R[i])
        # Subtract u_i times continuity from the conservative residual ...
        mat = sp.expand(cons - U[i] * cont)
        # ... to obtain the material form (line 210).
        stated = (rho * (sp.diff(U[i], t) + dot(U, grad(U[i]))) - force[i]
                  + sum(sp.diff(P[i][j], X[j]) for j in range(3)) - R[i])
        check(mat, stated)
    d.step("conservative form", sp.Eq(Tex(r"\partial_t(\rho_s u_s) + \nabla\cdot(\rho_s u_s u_s + P_s)"),
                                      Tex(r"q_s n_s(E + u_s\times B) + R_s")))
    d.step("subtract u_s continuity", sp.Eq(Tex(r"\rho_s(\partial_t u_s + u_s\cdot\nabla u_s)"),
                                            Tex(r"q_s n_s(E + u_s\times B) - \nabla\cdot P_s + R_s")))
    check(ms * ns * us**2 / Ls, ms * ns * us**2 / Ls, unit=u.newton / u.meter**3)


def test_energy_balance():
    d = Derivation("Species energy balance", "src/chapters/07-multiple-fluids.typ:239")
    # Reuse the explicit test distribution of Chapter 6.
    import ch06_moments as c6
    W_mom = c6.m_s / 2 * c6.vint(c6.dot(c6.v, c6.v) * c6.f)
    ww = [c6.v[i] - c6.U[i] for i in range(3)]
    eps = c6.m_s / 2 * c6.vint(c6.dot(ww, ww) * c6.f)
    qh = [c6.m_s / 2 * c6.vint(c6.dot(ww, ww) * ww[i] * c6.f) for i in range(3)]
    _, _, P, _ = c6.moments()
    # W_s = rho u^2/2 + eps_s with eps_s = (m/2) int w^2 f (line 226).
    check(W_mom, c6.m_s * c6.n * c6.dot(c6.U, c6.U) / 2 + eps)
    # Weight the kinetic equation by m v^2/2 and integrate (line 239).
    wt = c6.m_s * c6.dot(c6.v, c6.v) / 2
    lhs = c6.vint(wt * c6.kinetic_lhs)
    flux = [W_mom * c6.U[i] + sum(P[i][j] * c6.U[j] for j in range(3)) + qh[i] for i in range(3)]
    stated = sp.diff(W_mom, t) + c6.div(flux) - c6.q_s * c6.n * c6.dot(c6.U, c6.E)
    check(lhs, stated)
    W, rho, n = field("W", "W_s"), field("rho", r"\rho_s"), field("n", "n_s")
    d.eq("energy moment", W, rho * sp.Symbol("u_s") ** 2 / 2 + Tex(r"\epsilon_s"))
    d.step("moment of kinetic eq.", sp.Eq(Tex(r"\partial_t W_s + \nabla\cdot(W_s u_s + P_s u_s + q_{h,s})"),
                                          Tex(r"q_s n_s u_s\cdot E + Q_s")))
    check(ms * ns * us**3, ms * ns * us**3, unit=u.watt / u.meter**2)


def test_maxwell_charge_continuity():
    d = Derivation("Maxwell equations and charge continuity", "src/chapters/07-multiple-fluids.typ:246")
    from si import eps0, mu0
    E, B = vec("E", "E"), vec("B", "B")
    rho_q = eps0 * div(E)  # Gauss
    # Ampere: j = curl(B)/mu0 - eps0 dE/dt; take its divergence.
    j_amp = [curl(B)[i] / mu0 - eps0 * sp.diff(E[i], t) for i in range(3)]
    res = d.eq("div Ampere + d/dt Gauss", Tex(r"\partial_t\rho_q + \nabla\cdot j"),
               sp.expand(sp.diff(rho_q, t) + div(j_amp)))
    check(res, 0)
    # div(curl E) = 0 keeps div B = 0 for all time under Faraday's law.
    check(div([-c for c in curl(E)]), 0)


def test_example_current():
    d = Derivation("Example: current with equal densities", "src/chapters/07-multiple-fluids.typ:321")
    n0, ui, ue = 1.0e16, 2.0e5, 1.5e5
    rho_q = num(d, "e (n_i - n_e)", r"\rho_q", CODATA[e] * (n0 - n0))
    jx = num(d, "e n (u_i - u_e)", "j_x", CODATA[e] * n0 * ui - CODATA[e] * n0 * ue)
    assert rho_q == 0
    close(jx, "80.1")


# ---------------------------------------------------------------------------
# Perpendicular drifts and diamagnetic current
# ---------------------------------------------------------------------------
Bv = sp.symbols("B_x B_y B_z", real=True)
Ev = sp.symbols("E_x E_y E_z", real=True)
Gp = sp.symbols("g_x g_y g_z", real=True)  # components of grad p_s
B2 = dot(Bv, Bv)


def perp(a):
    """a_perp = a - b (b . a)."""
    return [a[i] - Bv[i] * dot(Bv, a) / B2 for i in range(3)]


def test_perpendicular_drift():
    d = Derivation("Perpendicular drift balance", "src/chapters/07-multiple-fluids.typ:427")
    q, n_ = sp.symbols("q_s n_s", nonzero=True)
    a = sp.symbols("a_1 a_2 a_3", real=True)
    # Identity (u x B) x B = -B^2 u_perp for any u (line 461).
    vcheck(cross(cross(a, Bv), Bv), [-B2 * c for c in perp(a)])
    # Unknown perpendicular velocity: u_perp = c1 e1 + c2 e2 with e1, e2 perpendicular to B.
    c1, c2 = sp.symbols("c_1 c_2")
    e1 = cross(Bv, [1, 0, 0]) if Bv[1] != 0 or Bv[2] != 0 else [0, 1, 0]
    e2 = cross(Bv, e1)
    uperp = [c1 * e1[i] + c2 * e2[i] for i in range(3)]
    # Inertialess perpendicular balance: q n (E_perp + u_perp x B) - grad_perp p = 0 (line 427).
    bal = [q * n_ * (perp(Ev)[i] + cross(uperp, Bv)[i]) - perp(Gp)[i] for i in range(3)]
    sol = sp.solve([dot(bal, e1), dot(bal, e2)], [c1, c2], dict=True)[0]
    u_sol = [sp.simplify(c.subs(sol)) for c in uperp]
    # Stated: u_perp = E x B / B^2 + B x grad p / (q n B^2) (lines 434-440).
    u_ExB = [c / B2 for c in cross(Ev, Bv)]
    u_dia = [c / (q * n_ * B2) for c in cross(Bv, Gp)]
    vcheck(u_sol, [u_ExB[i] + u_dia[i] for i in range(3)])
    d.step("perpendicular balance", sp.Eq(Tex(r"q_s n_s(E_\perp + u_{s\perp}\times B)"),
                                          Tex(r"\nabla_\perp p_s")))
    d.step("cross with B", sp.Eq(Tex(r"q_s n_s E\times B - q_s n_s B^2 u_{s\perp}"),
                                 Tex(r"\nabla p_s\times B")))
    d.eq("solve", Tex(r"u_{s\perp}"), Tex(r"\frac{E\times B}{B^2} + \frac{B\times\nabla p_s}{q_s n_s B^2}"))
    # Units: E/B and grad p/(q n B) are speeds.
    check(Em / Bm, Em / Bm, unit=u.meter / u.second)
    check(ps / (Ls * qs * ns * Bm), ps / (Ls * qs * ns * Bm), unit=u.meter / u.second)


def test_example_drifts():
    d = Derivation("Example: E x B and diamagnetic drifts", "src/chapters/07-multiple-fluids.typ:492")
    E_ = [30.0, 0, 0]
    B_ = [0, 0, 0.0100]
    g = [1.602e-5, 0, 0]
    n_ = 1.0e14
    b2 = dot(B_, B_)
    uE = num(d, "E x B drift", r"u_{E\times B,y}", cross(E_, B_)[1] / b2)
    ui = num(d, "ion diamagnetic drift", r"u_{*i,y}", cross(B_, g)[1] / (CODATA[e] * n_ * b2))
    ue = num(d, "electron diamagnetic drift", r"u_{*e,y}", cross(B_, g)[1] / (-CODATA[e] * n_ * b2))
    close(uE, "-3.00e3")
    close(ui, "1.00e2")
    close(ue, "-1.00e2")
    for vv in (cross(E_, B_), cross(B_, g)):
        assert vv[0] == 0 and vv[2] == 0


def test_diamagnetic_current():
    d = Derivation("Diamagnetic current", "src/chapters/07-multiple-fluids.typ:589")
    qe, qi, ne_, ni_ = sp.symbols("q_e q_i n_e n_i", nonzero=True)
    ge, gi = sp.symbols("g_ex g_ey g_ez", real=True), sp.symbols("g_ix g_iy g_iz", real=True)
    drift = lambda q, nn, g: [cross(Ev, Bv)[i] / B2 + cross(Bv, g)[i] / (q * nn * B2) for i in range(3)]
    # j_perp = sum_s q_s n_s u_s,perp with the drift of each species.
    j = [qe * ne_ * drift(qe, ne_, ge)[i] + qi * ni_ * drift(qi, ni_, gi)[i] for i in range(3)]
    rho_q = qe * ne_ + qi * ni_
    stated = [rho_q * cross(Ev, Bv)[i] / B2 + (cross(Bv, ge)[i] + cross(Bv, gi)[i]) / B2 for i in range(3)]
    vcheck(j, stated)
    # Quasi-neutral limit rho_q = 0 leaves j_* = B x grad(p_e + p_i) / B^2 (line 596).
    j_star = [sp.simplify(c.subs(qi, -qe * ne_ / ni_)) for c in j]
    vcheck(j_star, [cross(Bv, [ge[k] + gi[k] for k in range(3)])[i] / B2 for i in range(3)])
    d.eq("sum_s q_s n_s u_s,perp", Tex(r"j_\perp"),
         Tex(r"\frac{\rho_q\, E\times B}{B^2} + \sum_s \frac{B\times\nabla p_s}{B^2}"))
    d.eq("rho_q = 0", Tex(r"j_*"), Tex(r"\frac{B\times\nabla(p_e+p_i)}{B^2}"))
    # Ideal-gas pressures with n_e = n_i = n (line 602).
    n, Te, Ti = field("n", "n"), field("T_e", "T_e"), field("T_i", "T_i")
    lhs = d.eq("p_s = n k_B T_s", Tex(r"\partial_x(p_e+p_i)"), sp.expand(sp.diff(n * k_B * Te + n * k_B * Ti, x)))
    check(lhs, k_B * ((Te + Ti) * sp.diff(n, x) + n * sp.diff(Te + Ti, x)))
    check(ps / (Ls * Bm), ps / (Ls * Bm), unit=u.ampere / u.meter**2)


def test_example_diamagnetic_current():
    d = Derivation("Example: diamagnetic current density", "src/chapters/07-multiple-fluids.typ:661")
    B_, g = [0, 0, 0.0100], [3.204e-5, 0, 0]
    jy = num(d, "diamagnetic current", "j_{*,y}", cross(B_, g)[1] / dot(B_, B_))
    close(jy, "3.20e-3")


# ---------------------------------------------------------------------------
# Parallel dynamics and one-fluid variables
# ---------------------------------------------------------------------------
def test_parallel_equation():
    d = Derivation("Parallel momentum equation", "src/chapters/07-multiple-fluids.typ:773")
    rho, n, p = field("rho", r"\rho_s"), field("n", "n_s"), field("p", "p_s")
    U, E, R = vec("u", "u"), vec("E", "E"), vec("R", "R")
    q = sp.Symbol("q_s", real=True)
    bx, by, bz = sp.symbols("b_x b_y b_z", real=True)
    b = [bx, by, bz]
    Bmag = sp.Symbol("B", positive=True)
    Bvec = [Bmag * c for c in b]
    # Material momentum equation with scalar pressure, dotted with constant b.
    lhs = [rho * (sp.diff(U[i], t) + dot(U, grad(U[i]))) for i in range(3)]
    rhs = [q * n * (E[i] + cross(U, Bvec)[i]) - grad(p)[i] + R[i] for i in range(3)]
    res = sp.expand(dot(b, lhs) - dot(b, rhs))
    upar = dot(b, U)
    stated = (rho * (sp.diff(upar, t) + dot(U, grad(upar))) + dot(b, grad(p))
              - q * n * dot(b, E) - dot(b, R))
    # The magnetic force drops out because b . (u x B) = 0.
    check(sp.expand(dot(b, cross(U, Bvec))), 0)
    check(res, stated)
    d.step("b . momentum", sp.Eq(Tex(r"\rho_s(\partial_t u_{\parallel s} + u_s\cdot\nabla u_{\parallel s})"),
                                 Tex(r"-b\cdot\nabla p_s + q_s n_s E_\parallel + R_{\parallel s}")))


def test_boltzmann_relation():
    d = Derivation("Electron Boltzmann relation", "src/chapters/07-multiple-fluids.typ:793")
    s_ = sp.Symbol("s", real=True)  # arc length along b
    T_e = sp.Symbol("T_e", positive=True)
    n = sp.Function("n_e", positive=True)(s_)
    phi = sp.Function("phi", real=True)(s_)
    # Inertialess, collisionless electrons: 0 = -dp_e/ds - e n_e E_par (line 782).
    E_par = sp.solve(sp.Eq(0, -sp.diff(n * k_B * T_e, s_) - e * n * sp.Symbol("E")), sp.Symbol("E"))[0]
    E_par = d.eq("electron balance", Tex(r"E_\parallel"), E_par)
    # Stated (line 787): E_par = -(k_B T_e / e) d ln n_e / ds.
    check(E_par, -(k_B * T_e / e) * sp.diff(sp.log(n), s_))
    # With E_par = -dphi/ds, integrate along the field line.
    ode = sp.Eq(-sp.diff(phi, s_), E_par)
    phi0 = sp.Symbol("phi_0", real=True)
    # d ln n / ds = (e/k_B T_e) dphi/ds  =>  n = n_0 exp(e (phi - phi_0)/(k_B T_e)).
    dlnn = sp.solve(ode, sp.diff(n, s_))[0] / n
    d.eq("E_par = -dphi/ds", Tex(r"\frac{d\ln n_e}{ds}"), sp.simplify(dlnn))
    n_e0 = sp.Symbol("n_e0", positive=True)
    stated = n_e0 * sp.exp(e * (phi - phi0) / (k_B * T_e))
    # The stated profile solves d ln n/ds = (e/k_B T_e) dphi/ds and equals n_e0 at phi = phi_0.
    check(sp.diff(sp.log(stated), s_), dlnn)
    check(stated.subs(phi, phi0), n_e0)
    d.step("integrate", sp.Eq(sp.Symbol("n_e"), stated))
    check(k_B * Ts / (e * Ls), k_B * Ts / (e * Ls), unit=u.volt / u.meter)


def test_one_fluid_momentum():
    d = Derivation("One-fluid momentum equation", "src/chapters/07-multiple-fluids.typ:815")
    S = ("e", "i")
    m = {s: sp.Symbol(f"m_{s}", positive=True) for s in S}
    q = {s: sp.Symbol(f"q_{s}", real=True) for s in S}
    n = {s: field(f"n_{s}", f"n_{s}") for s in S}
    U = {s: vec(f"u{s}", f"u_{{{s}}}") for s in S}
    P = {s: [[field(f"P{s}_{a}{b}", f"P_{{{s},{a}{b}}}") for b in "xyz"] for a in "xyz"] for s in S}
    R = {s: vec(f"R{s}", f"R_{{{s}}}") for s in S}
    E, B = vec("E", "E"), vec("B", "B")
    rho = sum(m[s] * n[s] for s in S)
    u_cm = [sum(m[s] * n[s] * U[s][i] for s in S) / rho for i in range(3)]
    V = {s: [U[s][i] - u_cm[i] for i in range(3)] for s in S}
    # sum_s rho_s V_s = 0 (line 868).
    vcheck([sum(m[s] * n[s] * V[s][i] for s in S) for i in range(3)], [0, 0, 0])
    # sum_s rho_s u_s u_s = rho u u + sum_s rho_s V_s V_s (line 863).
    for i, j in [(0, 0), (0, 1)]:
        check(sum(m[s] * n[s] * U[s][i] * U[s][j] for s in S),
              rho * u_cm[i] * u_cm[j] + sum(m[s] * n[s] * V[s][i] * V[s][j] for s in S))
    # Add the species momentum equations (residual form) ...
    rho_q = sum(q[s] * n[s] for s in S)
    jv = [sum(q[s] * n[s] * U[s][i] for s in S) for i in range(3)]
    P1 = [[sum(P[s][i][j] + m[s] * n[s] * V[s][i] * V[s][j] for s in S) for j in range(3)] for i in range(3)]
    for i in range(3):
        total = sum(sp.diff(m[s] * n[s] * U[s][i], t)
                    + sum(sp.diff(m[s] * n[s] * U[s][i] * U[s][j] + P[s][i][j], X[j]) for j in range(3))
                    - q[s] * n[s] * (E[i] + cross(U[s], B)[i]) - R[s][i] for s in S)
        # ... and compare with the one-fluid form (line 815).
        stated = (sp.diff(rho * u_cm[i], t) + sum(sp.diff(rho * u_cm[i] * u_cm[j] + P1[i][j], X[j]) for j in range(3))
                  - rho_q * E[i] - cross(jv, B)[i] - sum(R[s][i] for s in S))
        check(total, stated)
    d.step("relative velocity", sp.Eq(Tex(r"\sum_s \rho_s u_s u_s"),
                                      Tex(r"\rho u u + \sum_s \rho_s V_s V_s")))
    d.step("Lorentz force", sp.Eq(Tex(r"\sum_s q_s n_s(E + u_s\times B)"), Tex(r"\rho_q E + j\times B")))
    d.step("sum over species", sp.Eq(Tex(r"\partial_t(\rho u) + \nabla\cdot(\rho u u + P_1)"),
                                     Tex(r"\rho_q E + j\times B + \sum_s R_s")))


def test_example_boltzmann():
    d = Derivation("Example: Boltzmann density ratio", "src/chapters/07-multiple-fluids.typ:883")
    ratio = num(d, "exp(e dphi / k_B T_e)", "n_e/n_{e0}", sp.exp(3.00 / 3.00))
    close(ratio, "2.72")
    close(num(d, "n_e0 ratio", "n_e", 1.0e16 * ratio), "2.72e16")


if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
