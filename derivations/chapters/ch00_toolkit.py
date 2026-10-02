"""Appendix, Mathematical toolkit: src/appendices/mathematical-toolkit.typ.

Coverage (Typst line -> test):
  K_s, U_s, P_s, q_s, W_s = K_s + U_s     l.74-79            -> test_energy_moments
  total-energy equation                   l.91, 121-186      -> test_lorentz_work_by_parts
  energy-flux decomposition               l.192-207          -> test_energy_flux_decomposition
  bulk kinetic-energy equation            l.232-238          -> test_bulk_energy_equation
  div(P.u) identity, isotropic limit      l.254-261, 216-222 -> test_pressure_work
  internal-energy equation                l.216, 247         -> test_internal_energy_equation
  scale factors                           l.349-353          -> test_scale_factors
  general orthogonal operators            l.363-369, 396-427 -> test_general_operators
  Cartesian specialization                l.437-442          -> test_general_operators
  cylindrical specialization              l.453-456          -> test_specializations
  spherical specialization                l.468-474          -> test_specializations
  identity checks                         l.484-490          -> test_identities
  cylindrical flux check                  l.497-519          -> test_cylindrical_flux
  Rechenbeispiel Gamma_r = C/r            l.525-534          -> test_example_cylindrical_flux

Run `python derivations/ch00_toolkit.py` or `pytest derivations`.
"""

import itertools

import sympy as sp
from sympy.physics import units as su

from si import Derivation, check

m, n = sp.symbols("m_s n_s", positive=True)
q = sp.Symbol("q_s", real=True)
U3 = sp.symbols("u_x u_y u_z", real=True)
C3 = sp.symbols("c_x c_y c_z", real=True)
P = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"P_{min(i, j) + 1}{max(i, j) + 1}"))  # symmetric
T3 = {}  # third central moments int c_i c_j c_k f


def moment(poly):
    """Velocity integral of poly(c) f, using only the moment definitions."""
    poly = sp.Poly(sp.expand(poly), *C3)
    out = 0
    for powers, coeff in poly.terms():
        k = sum(powers)
        if k == 0:
            val = n  # int f = n_s
        elif k == 1:
            val = 0  # int c f = 0 by definition of u_s
        elif k == 2:
            i, j = [ix for ix, p in enumerate(powers) for _ in range(p)]
            val = P[i, j] / m  # P_s = m int c c f
        elif k == 3:
            key = tuple(sorted(ix for ix, p in enumerate(powers) for _ in range(p)))
            val = T3.setdefault(key, sp.Symbol("T_" + "".join(map(str, key))))
        else:
            raise ValueError(powers)
        out += coeff * val
    return sp.expand(out)


def test_energy_moments():
    d = Derivation("Energy moments", "src/appendices/mathematical-toolkit.typ:79")
    u, c = sp.Matrix(U3), sp.Matrix(C3)
    v = u + c
    W = d.eq("second moment", sp.Symbol("W_s"), moment(m * v.dot(v) / 2))
    K = m * n * u.dot(u) / 2
    U = P.trace() / 2
    check(W, sp.expand(K + U))  # :74-79
    # Isotropic pressure: U = 3 p / 2.  # :219
    p = sp.Symbol("p")
    check((p * sp.eye(3)).trace() / 2, sp.Rational(3, 2) * p)
    rho, uu = sp.symbols("rho u", positive=True)
    check(rho * uu**2 / 2, rho * uu**2 / 2, unit=su.joule / su.meter**3,
          units={rho: su.kilogram / su.meter**3, uu: su.meter / su.second})


def test_energy_flux_decomposition():
    d = Derivation("Energy-flux decomposition", "src/appendices/mathematical-toolkit.typ:202")
    u, c = sp.Matrix(U3), sp.Matrix(C3)
    v = u + c
    flux = [moment(m * v.dot(v) * v[k] / 2) for k in range(3)]
    d.eq("expand v = u + c", sp.Symbol(r"\frac{m_{s}}{2}\int |v|^{2} v f\, d^{3}v"),
         sp.Symbol(r"K_{s} u + U_{s} u + P_{s}\cdot u + q_{s}"))
    K = m * n * u.dot(u) / 2
    U = P.trace() / 2
    heat = [moment(m * c.dot(c) * c[k] / 2) for k in range(3)]  # q_s definition
    Pu = P * u
    for k in range(3):
        stated = K * u[k] + U * u[k] + Pu[k] + heat[k]  # :202
        check(flux[k], sp.expand(stated))
        check(flux[k], sp.expand((K + U) * u[k] + Pu[k] + heat[k]))  # :207


def test_lorentz_work_by_parts():
    d = Derivation("Lorentz work by parts", "src/appendices/mathematical-toolkit.typ:171")
    V = sp.symbols("v_x v_y v_z", real=True)
    E, B = sp.symbols("E_x E_y E_z", real=True), sp.symbols("B_x B_y B_z", real=True)
    v, Ev, Bv = sp.Matrix(V), sp.Matrix(E), sp.Matrix(B)
    f = sp.Function("f")(*V)
    a = q / m * (Ev + v.cross(Bv))
    eps = m * v.dot(v) / 2
    divv = lambda F: sum(sp.diff(F[i], V[i]) for i in range(3))
    grad_f = sp.Matrix([f.diff(x) for x in V])
    grad_eps = sp.Matrix([eps.diff(x) for x in V])
    # Product rule: eps a.df/dv = div_v(eps f a) - f a.d(eps)/dv - eps f div_v a.  # :153
    lhs = eps * a.dot(grad_f)
    rhs = divv(eps * f * a) - f * a.dot(grad_eps) - eps * f * divv(a)
    check(sp.expand(lhs - rhs), 0)
    check(d.eq("zero trace", sp.Symbol(r"\nabla_{v}\cdot a"), sp.expand(divv(a))), 0)
    # Remaining term -m f a.v: the magnetic part vanishes pointwise.  # :171-176
    work = d.eq("magnetic part drops", sp.Symbol(r"-m f a \cdot v"), sp.expand(-m * f * a.dot(v)))
    check(work, sp.expand(-q * f * Ev.dot(v)))
    # Concrete check with a shifted Maxwellian: int eps a.df/dv = -q n E.u.
    T, kB = sp.symbols("T k_B", positive=True)
    uu = sp.symbols("u_x u_y u_z", real=True)
    fM = n * (m / (2 * sp.pi * kB * T)) ** sp.Rational(3, 2) * sp.exp(
        -m * sum((x - y) ** 2 for x, y in zip(V, uu)) / (2 * kB * T))
    integrand = (eps * a.dot(sp.Matrix([fM.diff(x) for x in V])))
    W = sp.symbols("w_x w_y w_z", real=True)
    integrand = integrand.subs({x: w + y for x, w, y in zip(V, W, uu)})
    for w in W:
        integrand = sp.integrate(sp.expand(integrand), (w, -sp.oo, sp.oo))
    val = d.eq("Maxwellian", sp.Symbol("I_a"), sp.simplify(integrand))
    check(val, -q * n * Ev.dot(sp.Matrix(uu)))  # :176


# --- Fluid energy balances on generic fields ---------------------------------

t, x, y, z = sp.symbols("t x y z", real=True)
X3 = (t, x, y, z)
R3 = (x, y, z)
F = lambda name: sp.Function(name)(*X3)
rho = F("rho")
uf = sp.Matrix([F(f"u_{c}") for c in "xyz"])
Pf = sp.Matrix(3, 3, lambda i, j: F(f"P_{min(i, j) + 1}{max(i, j) + 1}"))
qf = sp.Matrix([F(f"q_{c}") for c in "xyz"])
Ef = sp.Matrix([F(f"E_{c}") for c in "xyz"])
Bf = sp.Matrix([F(f"B_{c}") for c in "xyz"])
Rf = sp.Matrix([F(f"R_{c}") for c in "xyz"])
Qf = F("Q")


def div(vec):
    return sum(sp.diff(vec[i], R3[i]) for i in range(3))


def div_tensor(T):
    """(div T)_i = sum_j d_j T_ji."""
    return sp.Matrix([sum(sp.diff(T[j, i], R3[j]) for j in range(3)) for i in range(3)])


def test_bulk_energy_equation():
    d = Derivation("Bulk kinetic-energy equation", "src/appendices/mathematical-toolkit.typ:238")
    K = rho * uf.dot(uf) / 2
    # Momentum balance and continuity (residuals vanish on solutions).  # :232
    mom = (sp.diff(rho * uf, t) + div_tensor(rho * uf * uf.T + Pf)
           - (q * F("n") * (Ef + uf.cross(Bf)) + Rf))
    cont = sp.diff(rho, t) + div(rho * uf)
    d.step("momentum", sp.Symbol(r"\partial_{t}(\rho u) + \nabla\cdot(\rho u u + P) = q n (E + u \times B) + R"))
    # u . momentum - (|u|^2/2) continuity reproduces the stated K equation.
    lhs = sp.diff(K, t) + div(K * uf)
    rhs = q * F("n") * Ef.dot(uf) - uf.dot(div_tensor(Pf)) + uf.dot(Rf)  # :238
    combo = uf.dot(mom) - uf.dot(uf) / 2 * cont
    d.eq("dot with u", sp.Symbol(r"\partial_{t} K + \nabla\cdot(K u)"),
         sp.Symbol(r"q n E\cdot u - u\cdot\nabla\cdot P + u\cdot R"))
    check(sp.expand(combo - (lhs - rhs)), 0)


def test_pressure_work():
    d = Derivation("Pressure-work identity", "src/appendices/mathematical-toolkit.typ:254")
    Pu = Pf * uf
    graduu = sum(Pf[i, j] * sp.diff(uf[i], R3[j]) for i in range(3) for j in range(3))
    d.eq("product rule", sp.Symbol(r"\nabla\cdot(P\cdot u)"),
         sp.Symbol(r"u\cdot\nabla\cdot P + P:\nabla u"))
    check(sp.expand(div(Pu) - (uf.dot(div_tensor(Pf)) + graduu)), 0)  # :254
    # Isotropic limit P = p I.  # :221, :261
    p = F("p")
    Pi = p * sp.eye(3)
    iso = sum(Pi[i, j] * sp.diff(uf[i], R3[j]) for i in range(3) for j in range(3))
    check(iso, p * div(uf))
    d.eq("P = p I", sp.Symbol(r"P:\nabla u"), sp.Symbol(r"p \nabla\cdot u"))


def test_internal_energy_equation():
    d = Derivation("Internal-energy equation", "src/appendices/mathematical-toolkit.typ:216")
    U = F("U")
    K = rho * uf.dot(uf) / 2
    W = K + U
    nE = q * F("n") * Ef.dot(uf)
    # Residual form of each balance (zero on solutions).
    total = sp.diff(W, t) + div(W * uf + Pf * uf + qf) - nE - Qf  # :91
    bulk = sp.diff(K, t) + div(K * uf) - (nE - uf.dot(div_tensor(Pf)) + uf.dot(Rf))  # :238
    graduu = sum(Pf[i, j] * sp.diff(uf[i], R3[j]) for i in range(3) for j in range(3))
    internal = (sp.diff(U, t) + div(U * uf + qf)
                - (-graduu + Qf - uf.dot(Rf)))  # :216
    d.eq("total minus bulk", sp.Symbol(r"\partial_{t} U + \nabla\cdot(U u + q)"),
         sp.Symbol(r"-P:\nabla u + Q - u\cdot R"))
    check(sp.expand(total - bulk - internal), 0)
    su_ = {sp.Symbol("Pu"): su.pascal * su.meter / su.second}
    check(sp.Symbol("Pu"), sp.Symbol("Pu"), unit=su.watt / su.meter**2, units=su_)


# --- Orthogonal curvilinear coordinates -------------------------------------

r, th, ph, zc = sp.symbols("r theta phi z", positive=True)
xc, yc = sp.symbols("x y", real=True)
SYSTEMS = {
    "cartesian": ((xc, yc, zc), sp.Matrix([xc, yc, zc]), (1, 1, 1)),
    "cylindrical": ((r, ph, zc), sp.Matrix([r * sp.cos(ph), r * sp.sin(ph), zc]), (1, r, 1)),
    "spherical": ((r, th, ph), sp.Matrix([r * sp.sin(th) * sp.cos(ph), r * sp.sin(th) * sp.sin(ph),
                                          r * sp.cos(th)]), (1, r, r * sp.sin(th))),
}  # stated scale factors, mathematical-toolkit.typ:349-353
# Cartesian test fields for the independent oracle.
X, Y, Z = sp.symbols("X Y Z", real=True)
PSI = X**2 * Y + Y * Z**3 + X * Z
AVEC = sp.Matrix([X * Y, Y * Z**2, X**2 * Z])


def basis(pos, qs):
    """Unit vectors e_i = (dr/dq_i)/h_i and scale factors h_i = |dr/dq_i|."""
    cols = [pos.diff(qq) for qq in qs]
    h = [sp.simplify(sp.sqrt(sp.trigsimp(sp.expand(c.dot(c))))) for c in cols]
    h = [hh.replace(sp.Abs, lambda a: a) for hh in h]  # sin(theta) >= 0 for 0 <= theta <= pi
    return [sp.simplify(c / hh) for c, hh in zip(cols, h)], h


def cyc(i):
    return (i + 1) % 3, (i + 2) % 3


def grad_g(psi, qs, h):
    return [sp.diff(psi, qs[i]) / h[i] for i in range(3)]  # :363


def div_g(A, qs, h):
    H = h[0] * h[1] * h[2]
    return sum(sp.diff(h[cyc(i)[0]] * h[cyc(i)[1]] * A[i], qs[i]) for i in range(3)) / H  # :364


def curl_g(A, qs, h):
    out = []
    for i in range(3):
        j, k = cyc(i)
        out.append((sp.diff(h[k] * A[k], qs[j]) - sp.diff(h[j] * A[j], qs[k])) / (h[j] * h[k]))  # :366
    return out


def lap_g(psi, qs, h):
    H = h[0] * h[1] * h[2]
    return sum(sp.diff(h[cyc(i)[0]] * h[cyc(i)[1]] / h[i] * sp.diff(psi, qs[i]), qs[i])
               for i in range(3)) / H  # :369


def _zero(ex):
    return sp.simplify(sp.expand_trig(sp.simplify(ex))) == 0


def test_scale_factors():
    d = Derivation("Scale factors", "src/appendices/mathematical-toolkit.typ:349")
    for name, (qs, pos, h_stated) in SYSTEMS.items():
        _, h = basis(pos, qs)
        d.eq(name, sp.Symbol(r"(h_{1}, h_{2}, h_{3})"), sp.Tuple(*h))
        for a, b in zip(h, h_stated):
            check(a, b)
        # Orthogonality of the coordinate directions.
        cols = [pos.diff(qq) for qq in qs]
        for i, j in itertools.combinations(range(3), 2):
            assert sp.simplify(cols[i].dot(cols[j])) == 0


def test_general_operators():
    d = Derivation("Orthogonal-coordinate operators", "src/appendices/mathematical-toolkit.typ:363")
    # Oracle: Cartesian operators of the test fields, projected on the local basis.
    cart = [X, Y, Z]
    grad_c = sp.Matrix([PSI.diff(v) for v in cart])
    div_c = sum(AVEC[i].diff(cart[i]) for i in range(3))
    curl_c = sp.Matrix([AVEC[2].diff(Y) - AVEC[1].diff(Z), AVEC[0].diff(Z) - AVEC[2].diff(X),
                        AVEC[1].diff(X) - AVEC[0].diff(Y)])  # Cartesian curl, :442
    lap_c = sum(PSI.diff(v, 2) for v in cart)  # :440
    for name, (qs, pos, h) in SYSTEMS.items():
        e, _ = basis(pos, qs)
        sub = dict(zip(cart, pos))
        psi = PSI.subs(sub)
        A = [AVEC.subs(sub).dot(ei) for ei in e]  # physical components A_i
        g = grad_g(psi, qs, h)
        cu = curl_g(A, qs, h)
        for i in range(3):
            assert _zero(g[i] - grad_c.subs(sub).dot(e[i])), (name, "grad", i)
            assert _zero(cu[i] - curl_c.subs(sub).dot(e[i])), (name, "curl", i)
        assert _zero(div_g(A, qs, h) - div_c.subs(sub)), (name, "div")
        assert _zero(lap_g(psi, qs, h) - lap_c.subs(sub)), (name, "lap")
        d.step(name, sp.Symbol(r"\nabla\psi,\ \nabla\cdot A,\ \nabla\times A,\ \nabla^{2}\psi\ \mathrm{match\ Cartesian}"))


def test_specializations():
    d = Derivation("Cylindrical and spherical forms", "src/appendices/mathematical-toolkit.typ:454")
    psi = sp.Function("psi")
    A = [sp.Function(f"A_{i}") for i in (1, 2, 3)]
    # Cylindrical (r, phi, z), as printed at :453-456.
    qs, _, h = SYSTEMS["cylindrical"]
    s, Ac = psi(*qs), [a(*qs) for a in A]
    check(div_g(Ac, qs, h), sp.diff(r * Ac[0], r) / r + sp.diff(Ac[1], ph) / r + sp.diff(Ac[2], zc))
    check(lap_g(s, qs, h), sp.diff(r * sp.diff(s, r), r) / r + sp.diff(s, ph, 2) / r**2 + sp.diff(s, zc, 2))
    gs = grad_g(s, qs, h)
    check(gs[1], sp.diff(s, ph) / r)
    d.eq("cylindrical", sp.Symbol(r"\nabla^{2}\psi"), sp.expand(lap_g(s, qs, h)))
    # Spherical (r, theta, phi), as printed at :468-474.
    qs, _, h = SYSTEMS["spherical"]
    s, As = psi(*qs), [a(*qs) for a in A]
    check(div_g(As, qs, h), sp.diff(r**2 * As[0], r) / r**2
          + sp.diff(sp.sin(th) * As[1], th) / (r * sp.sin(th)) + sp.diff(As[2], ph) / (r * sp.sin(th)))
    check(lap_g(s, qs, h), sp.diff(r**2 * sp.diff(s, r), r) / r**2
          + sp.diff(sp.sin(th) * sp.diff(s, th), th) / (r**2 * sp.sin(th))
          + sp.diff(s, ph, 2) / (r**2 * sp.sin(th) ** 2))
    gs = grad_g(s, qs, h)
    check(gs[1], sp.diff(s, th) / r)
    check(gs[2], sp.diff(s, ph) / (r * sp.sin(th)))
    d.eq("spherical", sp.Symbol(r"\nabla^{2}\psi"), sp.expand(lap_g(s, qs, h)))


def test_identities():
    d = Derivation("Identity checks", "src/appendices/mathematical-toolkit.typ:484")
    qs, _, h = SYSTEMS["spherical"]
    psi = sp.Function("psi")(*qs)
    A = [sp.Function(f"A_{i}")(*qs) for i in (1, 2, 3)]
    check(d.eq("div curl", sp.Symbol(r"\nabla\cdot\nabla\times A"),
               sp.simplify(div_g(curl_g(A, qs, h), qs, h))), 0)
    cg = curl_g(grad_g(psi, qs, h), qs, h)
    for comp in cg:
        check(sp.simplify(comp), 0)
    Cc = sp.Symbol("C")
    check(d.eq("inverse square", sp.Symbol(r"\nabla\cdot A"), div_g([Cc / r**2, 0, 0], qs, h)), 0)


def test_cylindrical_flux():
    d = Derivation("Cylindrical flux check", "src/appendices/mathematical-toolkit.typ:519")
    L = sp.Symbol("L", positive=True)
    Ar = sp.Function("A_r")
    Phi = d.eq("surface flux", sp.Symbol("Phi"), 2 * sp.pi * r * L * Ar(r))  # :506
    dV = d.eq("shell volume", sp.Symbol("dV/dr"), 2 * sp.pi * r * L)  # :514
    ratio = d.eq("flux per volume", sp.Symbol("dPhi/dV"), sp.simplify(sp.diff(Phi, r) / dV))
    qs, _, h = SYSTEMS["cylindrical"]
    check(ratio, div_g([Ar(r), 0, 0], qs, h))  # :519
    check(ratio, sp.diff(r * Ar(r), r) / r)  # :502


def test_example_cylindrical_flux():
    d = Derivation("Example: radial flux C/r", "src/appendices/mathematical-toolkit.typ:533")
    C = sp.Rational(2, 1) * 10**12
    G = C / r
    g1 = d.eq("r = 0.1 m", sp.Symbol("Gamma_1"), G.subs(r, sp.Rational(1, 10)))
    g2 = d.eq("r = 0.2 m", sp.Symbol("Gamma_2"), G.subs(r, sp.Rational(2, 10)))
    check(g1, sp.Rational(2) * 10**13)  # :533
    check(g2, sp.Rational(1) * 10**13)
    check(d.eq("divergence", sp.Symbol(r"\nabla\cdot\Gamma"), sp.diff(r * G, r) / r), 0)


if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
