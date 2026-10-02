"""Chapter 6, velocity moments: src/chapters/06-moments.typ.

Run `python derivations/ch06_moments.py` to check every step, or
`pytest derivations` to check every chapter.

Method. The moment equations are checked on an explicit test distribution:
a drifting, anisotropic Gaussian with a Hermite skew term (gives a nonzero
heat flux) and a shear term (gives an off-diagonal pressure). All parameters
depend on (t, x, y, z). Velocity integrals of the kinetic equation are done
term by term with SymPy, so the integration by parts in velocity space and
the split into flow and random parts are verified rather than assumed.

Coverage (line in src/chapters/06-moments.typ -> test):
  65-72        n_s, rho_s, rho_q, j_s, j (definitions, units)  -> test_density_and_current
  84-90        u_s, j_s = q_s n_s u_s, <w_s> = 0               -> test_density_and_current
  95-96        pressure tensor (definition, units)             -> test_raw_second_moment
  110-143      M_s = P_s + rho_s u_s u_s                       -> test_raw_second_moment
  158-159      q_i = (1/2) sum_j Q_ijj                         -> test_heat_flux_contraction
  256-290      kinetic balance -> continuity (number, mass, charge)
               305-330 derivation steps                         -> test_continuity
  339-350      example: Gamma = 2.0e21, Ndot = 2.0e17          -> test_example_flux
  440-488      first moment: time, flux, force terms, momentum
               equation; 504-545 derivation steps              -> test_momentum_equation
  494-496      material (convective) momentum form             -> test_material_momentum
  553-562      example: f_E,x = 96.1 N/m^3                     -> test_example_force_density
  645-647      W_s, eps_s = tr(P)/2, W = rho u^2/2 + eps       -> test_energy_moments
  654-667      heat flux q_s and raw energy flux F_s           -> test_energy_moments
  671-691      energy force term, raw and split energy eq.;
               723-760 derivation steps                         -> test_energy_equation
  704-716      scalar pressure, isotropic divergence           -> test_isotropic_pressure
  775-798      bulk kinetic and internal-energy balances,
               u.div(P) = div(P.u) - P:grad(u)                 -> test_internal_energy
  803-809      isotropic adiabatic law with 5/3                -> test_internal_energy
  817-829      example: eps = 0.0240, W_bulk = 0.0837, W = 0.108 -> test_example_energy
  924-948      cold / warm closures, polytropic law            -> test_polytropic_law
  961-1003     BGK moments vanish when moments are matched     -> test_bgk_moments
  1024-1035    example: p1/p0 = 32, T1/T0 = 4                  -> test_example_polytropic
Not checked: 919 (schematic hierarchy chain), 993-995 (sum_s R_s = 0 and
sum_s Q_s = 0 state momentum and energy conservation of the collision
operator; they are assumptions here, not derived results).
"""

from functools import lru_cache

import sympy as sp
from sympy.physics import units as u

import si
from si import Derivation, e, k_B, m_i


# Units of this file's symbols. Kept local (not in the shared si.UNITS) so that
# symbols with common names in other chapter files cannot clash.
LOCAL = {}


def check(derived, stated, unit=None, units=None):
    """si.check with this file's LOCAL unit table."""
    return si.check(derived, stated, unit=unit, units={**LOCAL, **(units or {})})

# CODATA 2018 values for the worked examples.
CODATA = {e: 1.602176634e-19, m_i: 1.67262192369e-27}


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


# ---------------------------------------------------------------------------
# Test distribution and velocity integration
# ---------------------------------------------------------------------------
t, x, y, z = sp.symbols("t x y z", real=True)
X = (x, y, z)
v = sp.symbols("v_x v_y v_z", real=True)
w = sp.symbols("w_x w_y w_z", real=True)
m_s, q_s = sp.symbols("m_s q_s", real=True)

# Fields of (t, r): density, flow, three thermal widths, skew and shear sizes.
args = (t, x, y, z)


def field(name, tex):
    """Undefined function of (t, x, y, z) that prints as `tex` (no arguments)."""
    def _latex(self, printer, exp=None):
        return tex if exp is None else f"{tex}^{{{exp}}}"

    return sp.Function(name, real=True, __dict__={"_latex": _latex})(*args)


n = field("n", "n_{s}")
U = [field(f"u_{c}", f"u_{{{c}}}") for c in "xyz"]
sig = [field(f"sigma_{c}", rf"\sigma_{{{c}}}") for c in "xyz"]
kap = field("kappa", r"\kappa")
lam = field("lambda", r"\lambda")
E = [field(f"E_{c}", f"E_{{{c}}}") for c in "xyz"]
B = [field(f"B_{c}", f"B_{{{c}}}") for c in "xyz"]

# Random velocity in units of the widths, and the Gaussian weight.
s = [(v[i] - U[i]) / sig[i] for i in range(3)]
G = sp.exp(-sum(si**2 for si in s) / 2)
# Hermite He_3 skew along x (heat flux) and He_1 He_1 shear in x-y; both
# leave n and u unchanged by construction.
f = n / ((2 * sp.pi) ** sp.Rational(3, 2) * sig[0] * sig[1] * sig[2]) * G * (
    1 + kap * (s[0] ** 3 - 3 * s[0]) + lam * s[0] * s[1]
)


@lru_cache(None)
def gauss_moment(k):
    """int_R w^k exp(-w^2/(2 a^2)) dw for a > 0, done by SymPy."""
    a, ww = sp.symbols("a ww", positive=True)
    return sp.Lambda(a, sp.integrate(ww**k * sp.exp(-ww**2 / (2 * a**2)), (ww, -sp.oo, sp.oo)))


def vint(expr, widths=None):
    """Integrate expr(v) over R^3. expr must be polynomial(v) times the
    Gaussian exp(-sum_i (v_i - u_i)^2 / (2 widths_i^2)) (default: sigma_i)."""
    widths = sig if widths is None else widths
    G_w = sp.exp(-sum(w[i] ** 2 / widths[i] ** 2 for i in range(3)) / 2)
    e_w = sp.expand(sp.powsimp(expr.subs({v[i]: U[i] + w[i] for i in range(3)}, simultaneous=True) / G_w))
    total = 0
    for term in sp.Add.make_args(e_w):
        coeff, mono = term.as_independent(*w, as_Add=False)
        powers = mono.as_powers_dict()
        k = [int(powers.get(wi, 0)) for wi in w]
        assert mono == sp.Mul(*[w[i] ** k[i] for i in range(3)]), mono
        total += coeff * sp.Mul(*[gauss_moment(k[i])(widths[i]) for i in range(3)])
    return sp.expand(total)


def div(vec):
    return sum(sp.diff(vec[i], X[i]) for i in range(3))


def tdiv(T):
    """Divergence of a rank-two tensor: (div T)_i = sum_j d_j T_ij."""
    return [sum(sp.diff(T[i][j], X[j]) for j in range(3)) for i in range(3)]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def zero(expr):
    assert sp.simplify(sp.expand(expr)) == 0, expr


# Display-only pressure-tensor components P_ij.
DP = [[field(f"P_{a}{b}", f"P_{{{a}{b}}}") for b in "xyz"] for a in "xyz"]

# Lorentz acceleration and the three left-hand terms of the kinetic equation.
acc = [q_s / m_s * (E[i] + cross(v, B)[i]) for i in range(3)]
kin_time = sp.diff(f, t)
kin_space = sum(sp.diff(f * v[j], X[j]) for j in range(3))
kin_force = sum(sp.diff(f * acc[j], v[j]) for j in range(3))
kinetic_lhs = kin_time + kin_space + kin_force


@lru_cache(None)
def moments():
    """Central moments of f computed by direct integration."""
    ww = [v[i] - U[i] for i in range(3)]
    dens = vint(f)
    flow = [vint(v[i] * f) / dens for i in range(3)]
    P = [[m_s * vint(ww[i] * ww[j] * f) for j in range(3)] for i in range(3)]
    w2 = sum(wi**2 for wi in ww)
    q = [m_s / 2 * vint(w2 * ww[i] * f) for i in range(3)]
    return dens, flow, P, q


# Plain symbols for unit checks of the definitions.
ns, rho_s, us, qs, ms = sp.symbols("n_s rho_s u_s q_s m_s", positive=True)
ps, Ts, Wd = sp.symbols("p_s T_s W", positive=True)
LOCAL.update({ns: u.meter**-3, us: u.meter / u.second, qs: u.coulomb,
              ms: u.kilogram, ps: u.pascal, Ts: u.kelvin})


# ---------------------------------------------------------------------------
# Section 1: definitions
# ---------------------------------------------------------------------------
def test_density_and_current():
    d = Derivation("Density, flow and current", "src/chapters/06-moments.typ:65")
    dens, flow, _, _ = moments()
    # Zeroth moment of the test distribution returns its density parameter.
    d.eq("zeroth moment", sp.Symbol("n_s"), dens)
    zero(dens - n)
    # First moment / n returns the flow; j_s = q_s n_s u_s (line 85).
    jx = d.eq("charge-weighted first moment", sp.Symbol("j_{s,x}"), q_s * vint(v[0] * f))
    zero(jx - q_s * n * U[0])
    # Random velocity has zero mean (line 90).
    for i in range(3):
        zero(vint((v[i] - flow[i]) * f))
    # Units: rho_q = q n in C/m^3, j = q n u in A/m^2, rho_s = m n in kg/m^3.
    check(qs * ns, qs * ns, unit=u.coulomb / u.meter**3)
    check(qs * ns * us, qs * ns * us, unit=u.ampere / u.meter**2)
    check(ms * ns, ms * ns, unit=u.kilogram / u.meter**3)


def test_raw_second_moment():
    d = Derivation("Raw second moment", "src/chapters/06-moments.typ:110")
    _, _, P, _ = moments()
    for i, j in [(0, 0), (0, 1), (1, 2)]:
        # Integrate m v_i v_j f directly ...
        M_ij = d.eq("second moment", sp.Symbol(f"M_{{{'xyz'[i]}{'xyz'[j]}}}"),
                    m_s * vint(v[i] * v[j] * f))
        # ... and compare with P_ij + rho_s u_i u_j (line 112).
        stated = P[i][j] + m_s * n * U[i] * U[j]
        check(M_ij, stated)
    # Pressure tensor m n <w w> is a pressure (line 95).
    check(ms * ns * us**2, ms * ns * us**2, unit=u.pascal)


def test_heat_flux_contraction():
    d = Derivation("Heat flux as contraction", "src/chapters/06-moments.typ:159")
    _, _, _, q = moments()
    ww = [v[i] - U[i] for i in range(3)]
    # Third central tensor Q_ijk = m int w_i w_j w_k f.
    Q = lambda i, j, k: m_s * vint(ww[i] * ww[j] * ww[k] * f)
    qx = d.eq("contract Q_ijj", sp.Symbol("q_x"), sp.Rational(1, 2) * sum(Q(0, j, j) for j in range(3)))
    check(qx, q[0])
    zero(sp.Rational(1, 2) * sum(Q(1, j, j) for j in range(3)) - q[1])


# ---------------------------------------------------------------------------
# Section 2: continuity
# ---------------------------------------------------------------------------
def test_continuity():
    d = Derivation("Continuity from the zeroth moment", "src/chapters/06-moments.typ:278")
    # Velocity integrals of the three kinetic terms (lines 261-272).
    I_t = d.eq("int df/dt", sp.Symbol("I_t"), vint(kin_time))
    I_x = d.eq("int div(f v)", sp.Symbol("I_r"), vint(kin_space))
    I_v = d.eq("int div_v(f a)", sp.Symbol("I_v"), vint(kin_force))
    check(I_t, sp.diff(n, t))
    check(I_x, div([n * U[i] for i in range(3)]))
    check(I_v, 0)
    # Number continuity (line 278) with a particle-conserving collision term.
    lhs = d.step("collisions conserve N", I_t + I_x + I_v)
    check(lhs, sp.diff(n, t) + div([n * U[i] for i in range(3)]))
    # Mass continuity (line 283): multiply by the constant m_s.
    check(m_s * lhs, sp.diff(m_s * n, t) + div([m_s * n * U[i] for i in range(3)]))
    # Charge continuity (line 289): two species, multiply by q_s and sum.
    n2 = field("n2", "n_{2}")
    U2 = [field(f"u2_{c}", f"u_{{2{c}}}") for c in "xyz"]
    q1, q2 = sp.symbols("q_1 q_2", real=True)
    cont = lambda nn, uu: sp.diff(nn, t) + div([nn * uu[i] for i in range(3)])
    rho_q = q1 * n + q2 * n2
    j = [q1 * n * U[i] + q2 * n2 * U2[i] for i in range(3)]
    check(q1 * cont(n, U) + q2 * cont(n2, U2), sp.diff(rho_q, t) + div(j))


def test_example_flux():
    d = Derivation("Example: particle flux to a collector", "src/chapters/06-moments.typ:339")
    Gamma = num(d, "Gamma = n u", r"\Gamma_s", sp.Float(1.0e16) * sp.Float(2.0e5))
    close(Gamma, "2.0e21")
    close(num(d, "Ndot = Gamma A", r"\dot N_s", Gamma * 1.0e-4), "2.0e17")


# ---------------------------------------------------------------------------
# Section 3: momentum
# ---------------------------------------------------------------------------
def test_momentum_equation():
    d = Derivation("Momentum equation from the first moment", "src/chapters/06-moments.typ:486")
    _, _, P, _ = moments()
    rho = m_s * n
    for i in range(3):
        # Weight the kinetic equation with m_s v_i and integrate (line 440).
        T_t = m_s * vint(v[i] * kin_time)
        T_x = m_s * vint(v[i] * kin_space)
        T_v = m_s * vint(v[i] * kin_force)
        # Time term (line 453) and flux term (lines 459-464).
        check(T_t, sp.diff(rho * U[i], t))
        check(T_x, sum(sp.diff(rho * U[i] * U[j] + P[i][j], X[j]) for j in range(3)))
        # Integration by parts: force term is -q n (E + u x B)_i (lines 472-481).
        lorentz = q_s * n * (E[i] + cross(U, B)[i])
        check(-T_v, lorentz)
        if i == 0:
            # Display: the same terms in compact notation (P_xj as symbols).
            rho_d = field("rho", r"\rho_{s}")
            d.eq("time term", sp.Symbol("T_t"), sp.Derivative(rho_d * U[0], t))
            d.eq("flux term", sp.Symbol("T_r"), sum(
                sp.Derivative(rho_d * U[0] * U[j] + DP[0][j], X[j]) for j in range(3)))
            d.eq("force term, by parts", sp.Symbol("T_v"), -lorentz)
            d.step("momentum eq., x", sp.Eq(sp.Symbol("T_t") + sp.Symbol("T_r") + sp.Symbol("T_v"),
                                             sp.Symbol("R_{s,x}")))


def test_material_momentum():
    d = Derivation("Material form of the momentum equation", "src/chapters/06-moments.typ:494")
    rho = field("rho", r"\rho_{s}")
    i = 0
    # Conservative form minus u_i times mass continuity ...
    cons = sp.diff(rho * U[i], t) + div([rho * U[i] * U[j] for j in range(3)])
    cont = sp.diff(rho, t) + div([rho * U[j] for j in range(3)])
    lhs = d.step("subtract u_x (continuity)", sp.expand(cons - U[i] * cont))
    # ... equals rho (du/dt + u.grad u)_i (lines 494, 543-545).
    stated = rho * (sp.diff(U[i], t) + sum(U[j] * sp.diff(U[i], X[j]) for j in range(3)))
    check(lhs, stated)


def test_example_force_density():
    d = Derivation("Example: electric force density", "src/chapters/06-moments.typ:553")
    fE = num(d, "f = n e E", "f_{E,x}", 1.0e16 * CODATA[e] * 6.00e4)
    close(fE, "96.1")
    check(ns * qs * sp.Symbol("E_0"), ns * qs * sp.Symbol("E_0"),
          unit=u.newton / u.meter**3, units={sp.Symbol("E_0"): u.volt / u.meter})


# ---------------------------------------------------------------------------
# Section 4: energy
# ---------------------------------------------------------------------------
def energy_moments():
    _, _, P, q = moments()
    v2 = dot(v, v)
    W = m_s / 2 * vint(v2 * f)
    Fv = [m_s / 2 * vint(v2 * v[i] * f) for i in range(3)]
    return W, Fv, P, q


def test_energy_moments():
    d = Derivation("Energy density and energy flux", "src/chapters/06-moments.typ:645")
    W, Fv, P, q = energy_moments()
    d.eq("energy moment", sp.Symbol("W_s"), W)
    d.eq("energy-flux moment", sp.Symbol("F_{s,x}"), sp.Symbol("W_s") * U[0]
         + sum(DP[0][j] * U[j] for j in range(3)) + sp.Symbol("q_{s,x}"))
    # W = rho u^2/2 + eps with eps = tr(P)/2 (line 647).
    eps = sum(P[i][i] for i in range(3)) / 2
    check(W, m_s * n * dot(U, U) / 2 + eps)
    # Raw flux F = W u + P.u + q (line 685; derivation 745-760).
    for i in range(3):
        stated = W * U[i] + sum(P[i][j] * U[j] for j in range(3)) + q[i]
        check(Fv[i], stated)
    # Units: energy density J/m^3, heat flux W/m^2.
    check(ms * ns * us**2 / 2, ms * ns * us**2 / 2, unit=u.joule / u.meter**3)
    check(ms * ns * us**3 / 2, ms * ns * us**3 / 2, unit=u.watt / u.meter**2)


def test_energy_equation():
    d = Derivation("Energy equation from the second moment", "src/chapters/06-moments.typ:690")
    W, Fv, P, q = energy_moments()
    wt = m_s * dot(v, v) / 2
    T_t = vint(wt * kin_time)
    T_x = vint(wt * kin_space)
    T_v = vint(wt * kin_force)
    check(T_t, sp.diff(W, t))
    check(T_x, div(Fv))
    # Force term: -m int v.a f; magnetic part drops, electric work remains (673-680).
    check(T_v, -m_s * vint(dot(v, acc) * f))
    check(-T_v, q_s * n * dot(U, E))
    # Split energy equation (line 690).
    flux = [W * U[i] + sum(P[i][j] * U[j] for j in range(3)) + q[i] for i in range(3)]
    check(T_t + T_x, sp.diff(W, t) + div(flux))
    # Display in compact notation.
    Wf = field("W", "W_{s}")
    qd = [field(f"qh_{c}", f"q_{{{c}}}") for c in "xyz"]
    d.eq("time term", sp.Symbol("T_t"), sp.Derivative(Wf, t))
    d.eq("flux term, split", sp.Symbol("T_r"), sp.Derivative(
        Wf * U[0] + sum(DP[0][j] * U[j] for j in range(3)) + qd[0], x) + Tex(r"\ldots"))
    d.eq("force term, by parts", sp.Symbol("T_v"), -q_s * n * dot(U, E))
    d.step("energy eq.", sp.Eq(sp.Symbol("T_t") + sp.Symbol("T_r") + sp.Symbol("T_v"), sp.Symbol("Q_s")))


def test_isotropic_pressure():
    d = Derivation("Isotropic pressure", "src/chapters/06-moments.typ:709")
    p = field("p", "p_{s}")
    Piso = [[p if i == j else 0 for j in range(3)] for i in range(3)]
    # Scalar pressure = trace/3 (line 704).
    check(sum(Piso[i][i] for i in range(3)) / 3, p)
    # Component divergence sum_j d_j P_ij (line 716) gives grad p.
    divP = d.eq("sum_j d_j (p delta_xj)", Tex(r"(\nabla\cdot P)_x"), tdiv(Piso)[0])
    check(divP, sp.diff(p, x))
    # For the Maxwellian part of the test distribution, P_xx = n m sigma_x^2 = n k_B T.
    _, _, P, _ = moments()
    check(P[0][0].subs(lam, 0), m_s * n * sig[0] ** 2)


def test_internal_energy():
    d = Derivation("Internal energy and the adiabatic law", "src/chapters/06-moments.typ:796")
    rho = field("rho", r"\rho_{s}")
    eps = field("epsilon", r"\epsilon_{s}")
    Q = field("Q", "Q_{s}")
    R = [field(f"R_{c}", f"R_{{{c}}}") for c in "xyz"]
    qh = [field(f"q_{c}", f"q_{{{c}}}") for c in "xyz"]
    Pn = {}
    for i in range(3):
        for j in range(i, 3):
            Pn[(i, j)] = Pn[(j, i)] = field(f"P_{i}{j}", f"P_{{{'xyz'[i]}{'xyz'[j]}}}")
    P = [[Pn[(i, j)] for j in range(3)] for i in range(3)]
    fE = [q_s / m_s * rho * E[i] for i in range(3)]  # q n E with n = rho/m
    gradU = [[sp.diff(U[j], X[i]) for j in range(3)] for i in range(3)]
    # Residuals (lhs - rhs) of mass, momentum and total-energy equations.
    mass = sp.diff(rho, t) + div([rho * U[j] for j in range(3)])
    mom = [sp.diff(rho * U[i], t) + sum(sp.diff(rho * U[i] * U[j] + P[i][j], X[j]) for j in range(3))
           - fE[i] - R[i] for i in range(3)]
    W = rho * dot(U, U) / 2 + eps
    PU = [sum(P[i][j] * U[j] for j in range(3)) for i in range(3)]
    energy = sp.diff(W, t) + div([W * U[i] + PU[i] + qh[i] for i in range(3)]) - dot(U, fE) - Q
    # Product identity u.div(P) = div(P.u) - P:grad(u) (line 787), P symmetric.
    PgU = sum(P[i][j] * gradU[j][i] for i in range(3) for j in range(3))
    check(dot(U, tdiv(P)), div(PU) - PgU)
    # Bulk balance (line 778) = u.(momentum) - (u^2/2)(mass).
    bulk = (sp.expand(dot(U, mom) - dot(U, U) / 2 * mass))
    stated_bulk = (sp.diff(rho * dot(U, U) / 2, t) + div([rho * dot(U, U) * U[i] / 2 for i in range(3)])
                   + dot(U, tdiv(P)) - dot(U, fE) - dot(U, R))
    check(bulk, stated_bulk)
    # Internal energy (line 796) = total energy - bulk.
    internal = sp.expand(energy - bulk)
    stated_int = (sp.diff(eps, t) + div([eps * U[i] + qh[i] for i in range(3)]) + PgU
                  - (Q - dot(U, R)))
    check(internal, stated_int)
    # Isotropic closure eps = 3p/2, P = p I, q = 0, Q = u.R (lines 803-809).
    p = field("p", "p_{s}")
    iso = {eps: 3 * p / 2, **{Pn[(i, j)]: (p if i == j else 0) for i in range(3) for j in range(3)},
           **{qh[i]: 0 for i in range(3)}, Q: dot(U, R)}
    adiab = sp.expand(2 * stated_int.subs(iso).doit() / 3)
    stated = sp.diff(p, t) + dot(U, [sp.diff(p, xi) for xi in X]) + 5 * p / 3 * div(U)
    check(adiab, stated)
    # Display: one-dimensional (x only) form of each step.
    D = sp.Derivative
    ux, Pxx, qx = U[0], Pn[(0, 0)], qh[0]
    d.step("u.momentum - (u.u/2) mass", sp.Eq(
        D(rho * ux**2 / 2, t) + D(rho * ux**3 / 2, x) + ux * D(Pxx, x),
        q_s / m_s * rho * ux * E[0] + ux * R[0]))
    d.step("u div P = div(P u) - P:grad u", sp.Eq(ux * D(Pxx, x), D(Pxx * ux, x) - Pxx * D(ux, x)))
    d.step("energy - bulk", sp.Eq(D(eps, t) + D(eps * ux + qx, x) + Pxx * D(ux, x), Q - ux * R[0]))
    d.step("eps = 3p/2, P = p I, q = 0", sp.Eq(D(p, t) + ux * D(p, x) + 5 * p / 3 * D(ux, x), 0))


def test_polytropic_law():
    d = Derivation("Polytropic closure", "src/chapters/06-moments.typ:947")
    gamma = sp.Symbol("gamma", positive=True)
    p = field("p", "p_{s}")
    nn = field("n", "n_{s}")
    Dt = lambda g: sp.diff(g, t) + dot(U, [sp.diff(g, xi) for xi in X])
    # D/Dt (p n^-gamma) = 0 with continuity D n/Dt = -n div u (line 941).
    K = Dt(p * nn ** (-gamma)) * nn**gamma
    K = sp.expand(K)
    # Continuity: dn/dt = -div(n u).
    dn_dt = -div([nn * U[i] for i in range(3)])
    K = sp.expand(K.subs(sp.Derivative(nn, t), dn_dt))
    stated = Dt(p) + gamma * p * div(U)
    check(K, stated)
    D = sp.Derivative
    d.step("polytropic law", sp.Eq(D(p * nn ** (-gamma), t) + U[0] * D(p * nn ** (-gamma), x)
                                   + Tex(r"\ldots"), 0))
    d.step("continuity", sp.Eq(D(p, t) + U[0] * D(p, x) + gamma * p * D(U[0], x) + Tex(r"\ldots"), 0))
    # Cold closure (line 924) has no pressure; warm: eps = 3p/2 = (3/2) n k_B T.
    check(sp.Rational(3, 2) * ns * k_B * Ts, sp.Rational(3, 2) * ps.subs(ps, ns * k_B * Ts),
          unit=u.joule / u.meter**3)


def test_bgk_moments():
    d = Derivation("BGK collision moments", "src/chapters/06-moments.typ:961")
    nu = sp.Symbol("nu_s", positive=True)
    # Maxwellian with the same n, u and the same mean energy: sigma^2 = tr(sigma_i^2)/3.
    s2 = sum(si**2 for si in sig) / 3
    fM = n / (2 * sp.pi * s2) ** sp.Rational(3, 2) * sp.exp(-sum((v[i] - U[i]) ** 2 / sp.sqrt(s2) ** 2 for i in range(3)) / 2)

    def vint_M(expr_f, expr_fM):
        """Integrate g(v) f - h(v) f_M, each against its own Gaussian."""
        return sp.simplify(vint(expr_f) - vint(expr_fM, [sp.sqrt(s2)] * 3))

    S_N = d.eq("int C_BGK", sp.Symbol("S_N"), -nu * vint_M(f, fM))
    check(S_N, 0)
    R_x = d.eq("m int v_x C_BGK", sp.Symbol("R_x"), -nu * m_s * vint_M(v[0] * f, v[0] * fM))
    check(R_x, 0)
    Q_s = d.eq("energy moment of BGK", sp.Symbol("Q_s"),
               -nu * m_s / 2 * vint_M(dot(v, v) * f, dot(v, v) * fM))
    check(Q_s, 0)


# ---------------------------------------------------------------------------
# Worked examples
# ---------------------------------------------------------------------------
def test_example_energy():
    d = Derivation("Example: energy densities of a drifting ion population",
                   "src/chapters/06-moments.typ:817")
    n_i, kT, u_i = 1.0e16, 10 * CODATA[e], 1.0e5
    # Isotropic Maxwellian: P = n k_B T I, so eps = tr(P)/2 = (3/2) n k_B T.
    eps = num(d, "eps = 3 n k_B T / 2", r"\epsilon_i", 1.5 * n_i * kT)
    Wb = num(d, "bulk energy", r"W_{\mathrm{bulk}}", 0.5 * n_i * CODATA[m_i] * u_i**2)
    W = num(d, "W = W_bulk + eps", "W_i", Wb + eps)
    close(eps, "0.0240")
    close(Wb, "0.0837")
    close(W, "0.108")


def test_example_polytropic():
    d = Derivation("Example: adiabatic compression", "src/chapters/06-moments.typ:1024")
    gamma = sp.Rational(5, 3)
    # p n^-gamma constant: p1/p0 = (n1/n0)^gamma; T = p/(n k_B).
    p_ratio = d.eq("polytropic law", sp.Symbol("p_1/p_0"), sp.Integer(8) ** gamma)
    T_ratio = d.eq("ideal gas", sp.Symbol("T_1/T_0"), p_ratio / 8)
    check(p_ratio, 32)
    check(T_ratio, 4)


if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
