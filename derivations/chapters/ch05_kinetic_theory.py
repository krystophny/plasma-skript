"""Chapter 5, Kinetic theory: src/chapters/05-kinetic-theory.typ.

Coverage (Typst label or line -> test):
  <kinetic-survival>, <kinetic-mfp>   l.61, 71-73, 87-109 -> test_survival_and_mfp
  <kinetic-b90>                       l.138              -> test_b90_from_orbit
  <kinetic-coulomb-log>               l.151-153          -> test_coulomb_log_unit
  <kinetic-coulomb-frequency>         l.167-168          -> test_coulomb_frequency_scaling
  <kinetic-collisionality>            l.191              -> test_example_mfp
  Rechenbeispiel neutral collisions    l.198-205          -> test_example_mfp
  f_s units, <kinetic-local-average>, <kinetic-density> l.270, 289, 301 -> test_distribution_units
  <kinetic-moments-preview>           l.312-314          -> test_maxwellian_moments
  <kinetic-maxwellian>, l.344-373     normalization, moments -> test_maxwellian_moments
  mean energy 3 k_B T/2, l.386-397    -> test_maxwellian_energy
  convective derivative l.493, 540-551 -> test_convective_derivative
  <kinetic-characteristic>            l.500              -> test_convective_derivative
  <kinetic-phase-space-balance>, <kinetic-conservative>, <kinetic-product-rules>,
  <kinetic-liouville>, <kinetic-convective>, <kinetic-vlasov>
                                      l.512, 573, 723-765, 779-784 -> test_conservative_to_convective
  phase-space compression (drag)      l.639              -> test_conservative_to_convective
  <kinetic-normalized-streaming>      l.523              -> test_normalized_streaming
  <kinetic-acceleration>              l.712              -> test_conservative_to_convective
  particle-number conservation        l.810-820          -> test_continuity
  <kinetic-equilibrium-distribution>, <kinetic-boltzmann-response>
                                      l.914-951          -> test_boltzmann_equilibrium
  Fermi energy, theta_e               l.986-989          -> test_fermi_energy
  same n, u, T but different f (figure) -> test_moments_do_not_fix_f, plot_moment_ambiguity

Not checked: particle-field model l.688-699 (Maxwell equations and Klimontovich
sources are definitions restated from electrodynamics; no derived result).

Run `python derivations/ch05_kinetic_theory.py` or `pytest derivations`.
"""

import sympy as sp
from sympy.physics import units as u

from si import Derivation, check, eps0, k_B

n, sig, ell, v_rel, m, T, b = sp.symbols("n_b sigma ell v_rel m T b", positive=True)
LOCAL = {n: u.meter**-3, sig: u.meter**2, ell: u.meter, v_rel: u.meter / u.second,
         m: u.kilogram, T: u.kelvin, b: u.meter}
FUNIT = u.second**3 / u.meter**6  # unit of f_s


def close(a, b_, rtol):
    assert abs(float(a) / float(b_) - 1) < rtol, f"{float(a):.4g} vs {float(b_):.4g}"


def test_survival_and_mfp():
    d = Derivation("Survival law and mean free path", "src/chapters/05-kinetic-theory.typ:71")
    S = sp.Function("S")
    ode = d.step("survival", sp.Eq(S(ell).diff(ell), -n * sig * S(ell)))  # :61
    Sl = d.eq("dsolve", S(ell), sp.dsolve(ode, S(ell), ics={S(0): 1}).rhs)
    check(Sl, sp.exp(-n * sig * ell))  # :94
    p = d.eq("first-collision density", sp.Symbol("p"), -Sl.diff(ell))
    check(p, n * sig * sp.exp(-n * sig * ell))  # :99
    check(d.eq("normalization", sp.Symbol("P"), sp.integrate(p, (ell, 0, sp.oo))), 1)
    lam = d.eq("mean path", sp.Symbol("lambda_mfp"), sp.integrate(ell * p, (ell, 0, sp.oo)))
    check(lam, 1 / (n * sig), unit=u.meter, units=LOCAL)  # :71, :104
    nu = d.eq("rate", sp.Symbol("nu"), v_rel / lam)
    check(nu, n * sig * v_rel, unit=1 / u.second, units=LOCAL)  # :72, :109


def test_b90_from_orbit():
    d = Derivation("Ninety-degree impact parameter", "src/chapters/05-kinetic-theory.typ:138")
    qa, qb, mr, uu = sp.symbols("q_a q_b m_r u", positive=True)
    b0 = qa * qb / (4 * sp.pi * eps0 * mr * v_rel**2)  # Coulomb length scale
    B0 = sp.Symbol("b_0", positive=True)
    # Repulsive Kepler orbit, u = 1/r: chi = pi - 2 int_0^u0 b du / sqrt(1 - b^2 u^2 - 2 b0 u).
    rad = 1 - b**2 * uu**2 - 2 * B0 * uu
    A = sp.sqrt(1 + B0**2 / b**2)
    # Complete the square, w = b (u + b0/b^2): rad = A^2 - w^2.
    check(sp.expand(rad - (A**2 - (b * (uu + B0 / b**2)) ** 2)), 0)
    # With z = w/A the integrand is 1/sqrt(1 - z^2).
    z = sp.Symbol("z")
    F = sp.integrate(1 / sp.sqrt(1 - z**2), z)
    integral = d.eq("orbit integral", sp.Symbol("I"), F.subs(z, 1) - F.subs(z, B0 / (b * A)))
    chi = d.eq("deflection", sp.Symbol("chi"), sp.simplify(sp.pi - 2 * integral))
    # Set chi = pi/2 and solve for b.
    bsol = d.eq("ninety degrees", sp.Symbol("b_90"), sp.solve(sp.Eq(chi, sp.pi / 2), b)[0])
    check(bsol, B0)
    stated = sp.Abs(qa * qb) / (4 * sp.pi * eps0 * mr * v_rel**2)  # :138
    check(bsol.subs(B0, b0), stated, unit=u.meter,
          units={**LOCAL, qa: u.coulomb, qb: u.coulomb, mr: u.kilogram})
    # Reduced mass of the relative motion.
    ma, mb = sp.symbols("m_a m_b", positive=True)
    check(1 / (1 / ma + 1 / mb), ma * mb / (ma + mb), unit=u.kilogram,
          units={ma: u.kilogram, mb: u.kilogram})


def test_coulomb_log_unit():
    d = Derivation("Coulomb logarithm", "src/chapters/05-kinetic-theory.typ:153")
    bmax, bmin = sp.symbols("b_max b_min", positive=True)
    lnL = d.eq("cutoff ratio", sp.Symbol("ln Lambda"), sp.log(bmax / bmin))
    check(bmax / bmin, bmax / bmin, unit=u.meter / u.meter,
          units={bmax: u.meter, bmin: u.meter})
    assert lnL.args[0] == bmax / bmin


def test_coulomb_frequency_scaling():
    d = Derivation("Coulomb deflection frequency", "src/chapters/05-kinetic-theory.typ:167")
    qa, qb, ma, va, lnL = sp.symbols("q_a q_b m_a v_a lnLambda", positive=True)
    b90 = qa * qb / (4 * sp.pi * eps0 * ma * va**2)  # m_r ~ m_a for a light test particle
    # Cumulative small-angle cross section ~ pi b90^2 ln Lambda; nu = n sigma v.
    nu = d.eq("n sigma v", sp.Symbol("nu"), n * sp.pi * b90**2 * lnL * va)
    stated = n * qa**2 * qb**2 * lnL / (eps0**2 * ma**2 * va**3)  # :167-168
    ratio = sp.simplify(nu / stated)
    assert ratio.free_symbols == set(), ratio  # same scaling, pure-number prefactor
    check(stated, stated, unit=1 / u.second,
          units={n: u.meter**-3, qa: u.coulomb, qb: u.coulomb, ma: u.kilogram,
                 va: u.meter / u.second, lnL: 1})


def test_example_mfp():
    d = Derivation("Example: neutral collisions", "src/chapters/05-kinetic-theory.typ:204")
    vals = {n: 1e18, sig: 1e-19, v_rel: 1e6}
    lam = d.eq("mean free path", sp.Symbol("lambda_mfp"), (1 / (n * sig)).subs(vals))
    nu = d.eq("collision frequency", sp.Symbol("nu"), (v_rel / (1 / (n * sig))).subs(vals))
    close(lam, 10, 1e-9)  # :204
    close(nu, 1e5, 1e-9)  # :205
    L, tau = sp.symbols("L tau", positive=True)
    check(ell / L, ell / L, unit=u.meter / u.meter, units={**LOCAL, L: u.meter})  # :191
    nus = sp.Symbol("nu", positive=True)
    check(nus * tau, nus * tau, unit=u.second / u.second, units={tau: u.second, nus: 1 / u.second})


vx, vy, vz, ux, uy, uz = sp.symbols("v_x v_y v_z u_x u_y u_z", real=True)
V3, U3 = [vx, vy, vz], [ux, uy, uz]
ns = sp.Symbol("n_s", positive=True)


def maxwellian():
    return ns * (m / (2 * sp.pi * k_B * T)) ** sp.Rational(3, 2) * sp.exp(
        -m * sum((v - w) ** 2 for v, w in zip(V3, U3)) / (2 * k_B * T))


def vint(expr):
    """Integrate over all velocity space, one Cartesian component at a time."""
    # Shift v = u + w (integration over all of R^3 is shift invariant).
    ws = sp.symbols("w_x w_y w_z", real=True)
    expr = expr.subs({v: w + uu for v, w, uu in zip(V3, ws, U3)})
    for w in ws:
        expr = sp.integrate(sp.expand(expr), (w, -sp.oo, sp.oo))
    return sp.simplify(expr)


def test_distribution_units():
    d = Derivation("Phase-space density units", "src/chapters/05-kinetic-theory.typ:270")
    # dN = f d^3r d^3v is a count, so [f] = 1/(m^3 (m/s)^3).
    fM = maxwellian()
    wsym = sp.Symbol("w")
    d.eq("Maxwellian", sp.Symbol("f_M"),
         ns * (m / (2 * sp.pi * k_B * T)) ** sp.Rational(3, 2) * sp.exp(-m * wsym**2 / (2 * k_B * T)))
    check(fM.subs({vx: 0, vy: 0, vz: 0, ux: 0, uy: 0, uz: 0}), ns * (m / (2 * sp.pi * k_B * T)) ** sp.Rational(3, 2),
          unit=FUNIT, units={**LOCAL, ns: u.meter**-3})
    # Local average of g = 1 is one; f/n_s carries s^3 m^-3.  # :289-296
    avg1 = d.eq("average of 1", sp.Symbol(r"\langle 1 \rangle"), vint(fM) / ns)
    check(avg1, 1)
    check(fM.subs({vx: 0, vy: 0, vz: 0, ux: 0, uy: 0, uz: 0}) / ns,
          (m / (2 * sp.pi * k_B * T)) ** sp.Rational(3, 2), unit=u.second**3 / u.meter**3, units=LOCAL)


def test_maxwellian_moments():
    d = Derivation("Maxwellian moments", "src/chapters/05-kinetic-theory.typ:327")
    a = sp.Symbol("a", positive=True)
    c = sp.Symbol("c", real=True)
    # One-dimensional Gaussian factor, cubed.  # :349
    g1 = d.eq("1D Gaussian", sp.Symbol("G"), sp.integrate(sp.exp(-a * c**2), (c, -sp.oo, sp.oo)))
    check(g1**3, sp.sqrt(sp.pi / a) ** 3)
    f = maxwellian()
    n_d = d.eq("zeroth moment", sp.Symbol("n"), vint(f))
    check(n_d, ns)  # :301, :356
    flux = [d.eq("first moment", sp.Symbol(f"n u_{i}"), vint(v * f)) for i, v in zip("xyz", V3)]
    for fl, w in zip(flux, U3):
        check(fl / ns, w)  # :312, :364
    # Central second moment: P_ij = m int w_i w_j f.  # :314, :373
    W = [v - w for v, w in zip(V3, U3)]
    Pxx = d.eq("pressure xx", sp.Symbol("P_xx"), vint(m * W[0] ** 2 * f))
    Pxy = d.eq("pressure xy", sp.Symbol("P_xy"), vint(m * W[0] * W[1] * f))
    check(Pxx, ns * k_B * T, unit=u.pascal, units={**LOCAL, ns: u.meter**-3})
    check(Pxy, 0)
    # Variance of one component: 1/(2a) = k_B T/m.  # :327 note, :369
    var = vint(W[2] ** 2 * f) / ns
    check(var, k_B * T / m)
    check(1 / (2 * a), var.subs(T, m / (2 * a * k_B)))


def test_maxwellian_energy():
    d = Derivation("Mean random kinetic energy", "src/chapters/05-kinetic-theory.typ:390")
    f = maxwellian()
    W2 = sum((v - w) ** 2 for v, w in zip(V3, U3))
    eps = d.eq("average", sp.Symbol(r"\langle m w^{2}/2 \rangle"), vint(m * W2 / 2 * f) / ns)
    check(eps, sp.Rational(3, 2) * k_B * T, unit=u.joule, units=LOCAL)  # :390
    # Kinetic temperature: 3 k_B T = m <|v - u|^2>.  # :402
    check(m * vint(W2 * f) / ns, 3 * k_B * T)
    # v_th is a width, not the mean speed: <|w|> = (2/sqrt(pi)) v_th.  # :397
    s = sp.Symbol("s", positive=True)
    shell = 4 * sp.pi * s**2 * (m / (2 * sp.pi * k_B * T)) ** sp.Rational(3, 2) * sp.exp(-m * s**2 / (2 * k_B * T))
    mean_speed = d.eq("mean speed", sp.Symbol(r"\langle |w| \rangle"), sp.simplify(sp.integrate(s * shell, (s, 0, sp.oo))))
    vth = sp.sqrt(2 * k_B * T / m)
    check(mean_speed / vth, 2 / sp.sqrt(sp.pi))


def test_convective_derivative():
    d = Derivation("Convective derivative", "src/chapters/05-kinetic-theory.typ:551")
    t = sp.Symbol("t")
    X, Vv = sp.Function("x")(t), sp.Function("v")(t)
    g, a = sp.Function("g"), sp.Function("a")
    # Characteristic: dx/dt = v, dv/dt = a.  # :500
    total = g(t, X, Vv).diff(t).subs({X.diff(t): Vv, Vv.diff(t): a(t, X, Vv)})
    xs, vs = sp.symbols("x v")
    d.eq("chain rule", sp.Symbol("Dg/Dt"), total.subs({X: xs, Vv: vs}).doit())
    stated = (sp.diff(g(t, xs, vs), t) + vs * sp.diff(g(t, xs, vs), xs)
              + a(t, xs, vs) * sp.diff(g(t, xs, vs), vs))  # :493, :551
    check(total.subs({X: xs, Vv: vs}).doit(), stated)


def test_conservative_to_convective():
    d = Derivation("Conservative and convective kinetic equation",
                   "src/chapters/05-kinetic-theory.typ:758")
    t, x, y, z = sp.symbols("t x y z", real=True)
    q = sp.Symbol("q_s", real=True)
    R3 = [x, y, z]
    f = sp.Function("f")(t, x, y, z, vx, vy, vz)
    E = sp.Matrix([sp.Function(f"E_{c}")(t, x, y, z) for c in "xyz"])
    B = sp.Matrix([sp.Function(f"B_{c}")(t, x, y, z) for c in "xyz"])
    v = sp.Matrix(V3)
    a = q / m * (E + v.cross(B))  # :712
    divr = lambda F: sum(sp.diff(F[i], R3[i]) for i in range(3))
    divv = lambda F: sum(sp.diff(F[i], V3[i]) for i in range(3))
    # Phase-space incompressibility of Lorentz characteristics.  # :748
    check(d.eq("div_r v", sp.Symbol(r"\nabla_{r}\cdot v"), divr(v)), 0)
    check(d.eq("div_v a", sp.Symbol(r"\nabla_{v}\cdot a"), sp.expand(divv(a))), 0)
    # Conservative form minus convective form = f (div_r v + div_v a).  # :723-740, :784
    conservative = f.diff(t) + divr(f * v) + divv(f * a)
    convective = (f.diff(t) + sum(v[i] * f.diff(R3[i]) for i in range(3))
                  + sum(a[i] * f.diff(V3[i]) for i in range(3)))  # :758, :763 (Vlasov)
    check(sp.expand(conservative - convective), 0)
    # Velocity-dependent drag compresses phase space: Df/Dt = -f div_v a.  # :639
    gam = sp.Symbol("gamma", positive=True)
    drag = -gam * v
    resid = sp.expand(divv(f * drag) - sum(drag[i] * f.diff(V3[i]) for i in range(3)))
    check(d.eq("drag", sp.Symbol(r"f \nabla_{v}\cdot a"), resid), -3 * gam * f)
    E0 = sp.Symbol("E_0", positive=True)
    check(q / m * E0, q / m * E0, unit=u.meter / u.second**2,
          units={q: u.coulomb, m: u.kilogram, E0: u.volt / u.meter})


def test_normalized_streaming():
    d = Derivation("Normalized free streaming", "src/chapters/05-kinetic-theory.typ:523")
    t, x, vv, L0, v0 = sp.symbols("t x v L_0 v_0", positive=True)
    tau, xi, eta = sp.symbols("tau xi eta")
    F = sp.Function("F")
    f = F(t * v0 / L0, x / L0, vv / v0)
    lhs = sp.simplify((f.diff(t) + vv * f.diff(x)) * L0 / v0)
    rhs = (F(tau, xi, eta).diff(tau) + eta * F(tau, xi, eta).diff(xi))  # :523
    rhs = rhs.subs({tau: t * v0 / L0, xi: x / L0, eta: vv / v0})
    d.eq("rescale", sp.Symbol(r"\frac{L_0}{v_0}\left(\partial_{t} f + v \partial_{x} f\right)"),
         sp.Symbol(r"\partial_{\tau} F + \eta \partial_{\xi} F"))
    check(sp.simplify(lhs - rhs.doit()), 0)
    # Characteristics: any G(xi - eta tau) streams freely.
    G = sp.Function("G")
    sol = G(xi - eta * tau)
    check(sp.simplify(sol.diff(tau) + eta * sol.diff(xi)), 0)


def test_continuity():
    d = Derivation("Particle-number conservation", "src/chapters/05-kinetic-theory.typ:820")
    E, Bz = sp.symbols("E B_z", real=True)
    q = sp.Symbol("q_s", real=True)
    f = maxwellian()
    a = sp.Matrix([q / m * E, 0, 0]) + q / m * sp.Matrix(V3).cross(sp.Matrix([0, 0, Bz]))
    # Velocity-space divergence integrates to a vanishing surface term.  # :803-806
    divv = sum(sp.diff(f * a[i], V3[i]) for i in range(3))
    check(d.eq("velocity flux", sp.Symbol(r"\int \nabla_{v}\cdot (f a)\, d^3v"), vint(divv)), 0)
    # Moments that remain: n_s and n_s u_s.  # :815
    check(d.eq("density", sp.Symbol("n"), vint(f)), ns)
    check(d.eq("flux", sp.Symbol("n u_x"), vint(vx * f)), ns * ux)
    # Hence d n/dt + div(n u) = 0 (1D check with n(t,x), u(t,x)).  # :820
    t, x = sp.symbols("t x")
    nf, uf = sp.Function("n")(t, x), sp.Function("u")(t, x)
    w = sp.Symbol("w", real=True)
    f1 = nf * sp.sqrt(m / (2 * sp.pi * k_B * T)) * sp.exp(-m * w**2 / (2 * k_B * T))  # v = u + w
    N = sp.integrate(f1, (w, -sp.oo, sp.oo))
    Gam = sp.integrate((uf + w) * f1, (w, -sp.oo, sp.oo))
    cont = d.eq("integrate", sp.Symbol("0"), N.diff(t) + Gam.diff(x))
    check(sp.simplify(cont - (nf.diff(t) + (nf * uf).diff(x))), 0)


def test_boltzmann_equilibrium():
    d = Derivation("Boltzmann equilibrium in a potential", "src/chapters/05-kinetic-theory.typ:920")
    q = sp.Symbol("q_s", real=True)
    n0 = sp.Symbol("n_0s", positive=True)
    x = sp.Symbol("x", real=True)
    Phi = sp.Function("Phi")(x)
    H = m * (vx**2 + vy**2 + vz**2) / 2 + q * Phi  # :933
    Hs = sp.Symbol("H")
    d.eq("energy invariant", Hs, H)
    pref = n0 * (m / (2 * sp.pi * k_B * T)) ** sp.Rational(3, 2)
    d.eq("Maxwellian in H", sp.Symbol("f_eq"), pref * sp.exp(-Hs / (k_B * T)))
    feq = pref * sp.exp(-H / (k_B * T))  # :914
    # Stationary Vlasov solution: v_x df/dx - (q/m) Phi' df/dv_x = 0.
    vlasov = vx * feq.diff(x) - q / m * Phi.diff(x) * feq.diff(vx)
    check(d.eq("Vlasov", sp.Symbol("residual"), sp.simplify(vlasov)), 0)
    dens = d.eq("integrate over v", sp.Symbol("n_s"), sp.simplify(vint(feq)))
    stated = n0 * sp.exp(-q * Phi / (k_B * T))  # :920, :951
    check(dens, stated)
    P = sp.Symbol("Phi_0", positive=True)
    check(q * P / (k_B * T), q * P / (k_B * T), unit=u.joule / u.joule,
          units={q: u.coulomb, P: u.volt, T: u.kelvin})


def test_fermi_energy():
    d = Derivation("Fermi energy", "src/chapters/05-kinetic-theory.typ:989")
    hbar, kF, ne, me = sp.symbols("hbar k_F n_e m_e", positive=True)
    # Two spin states per k-space cell (2 pi)^3: n = 2 (4 pi/3) k_F^3 / (2 pi)^3.
    kFs = d.eq("count states", kF, sp.solve(sp.Eq(ne, 2 * sp.Rational(4, 3) * sp.pi * kF**3 / (2 * sp.pi) ** 3), kF)[0])
    EF = d.eq("free electron", sp.Symbol("E_F"), sp.simplify(hbar**2 * kFs**2 / (2 * me)))
    stated = hbar**2 / (2 * me) * (3 * sp.pi**2 * ne) ** sp.Rational(2, 3)  # :989
    U = {hbar: u.joule * u.second, ne: u.meter**-3, me: u.kilogram}
    check(EF, stated, unit=u.joule, units=U)
    check(k_B * T / stated, k_B * T / stated, unit=u.joule / u.joule, units={**U, T: u.kelvin})



# --- Same moments, different distributions (figure at l.413) ----------------
# One velocity component, s = (v - u)/v_th with v_th = sqrt(2 k_B T/m), and
# f normalized by n/v_th. A Maxwellian and two half-density beams at
# s = +-alpha whose width keeps the variance: w^2 = 1 - 2 alpha^2.
s1, alpha = sp.symbols("s alpha", real=True)
w_b = sp.Symbol("w", positive=True)
W_BEAM = sp.sqrt(1 - 2 * alpha**2)
F_MAXWELL_1D = sp.exp(-s1**2) / sp.sqrt(sp.pi)
F_BEAMS_1D = sum(sp.exp(-((s1 - sgn * alpha) / w_b) ** 2)
                 for sgn in (1, -1)) / (2 * sp.sqrt(sp.pi) * w_b)
ALPHA_PLOT = sp.Rational(3, 5)


def _moment(f, k):
    m_k = sp.integrate(sp.expand(s1**k * f), (s1, -sp.oo, sp.oo))
    return sp.simplify(sp.expand(m_k.subs(w_b, W_BEAM)))


def test_moments_do_not_fix_f():
    d = Derivation("Same n, u, T; different f", "src/chapters/05-kinetic-theory.typ:413")
    for f in (F_MAXWELL_1D, F_BEAMS_1D):
        check(_moment(f, 0), 1)  # same density n
        check(_moment(f, 1), 0)  # same bulk velocity u
        # <(v-u)^2> = v_th^2/2 = k_B T/m: same temperature.
        check(_moment(f, 2), sp.Rational(1, 2))
    d.eq("Maxwellian, 4th moment", sp.Symbol(r"\langle s^{4} \rangle_M"), _moment(F_MAXWELL_1D, 4))
    m4 = d.eq("beams, 4th moment", sp.Symbol(r"\langle s^{4} \rangle_B"), _moment(F_BEAMS_1D, 4))
    check(m4, sp.Rational(3, 4) - 2 * alpha**4)  # differs for every alpha != 0
    assert 0 < ALPHA_PLOT < 1 / sp.sqrt(2)


def plot_moment_ambiguity():
    """A Maxwellian and two beams with identical n, u and T."""
    import numpy as np

    from si import BLUE, ORANGE, figure, label, save

    x = np.linspace(-3, 3, 400)
    fM = sp.lambdify(s1, F_MAXWELL_1D, "numpy")
    fB = sp.lambdify(s1, F_BEAMS_1D.subs(w_b, W_BEAM).subs(alpha, ALPHA_PLOT), "numpy")
    fig, ax = figure(3.4, 2.4)
    ax.plot(x, fM(x), color=BLUE)
    ax.plot(x, fB(x), color=ORANGE, ls="--")
    label(ax, 1.35, fM(1.35) + 0.04, "Maxwellian", BLUE)
    label(ax, -0.95, fB(-0.95) + 0.06, "two beams", ORANGE, ha="right")
    ax.set(xlim=(-3, 3), ylim=(0, 0.8), yticks=[0, 0.25, 0.5, 0.75],
           xlabel=r"$(v-u)/v_{\mathrm{th}}$", ylabel=r"$f\,v_{\mathrm{th}}/n$")
    save(fig, "moment_ambiguity")

if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
