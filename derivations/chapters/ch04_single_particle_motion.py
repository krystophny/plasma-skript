"""Chapter 4, Single-particle motion: src/chapters/04-single-particle-motion.typ.

Coverage (Typst label or line -> test):
  <motion-lorentz-force>, <motion-energy>   l.39, 49     -> test_energy_theorem
  <motion-cyclotron-components>             l.59, 84     -> test_cyclotron_components
  gyroradius, omega_c                       l.73-77      -> test_gyroradius
  thermal gyroradius rho_s                  l.100-106    -> test_thermal_gyroradius_units
  Rechenbeispiel n=1e20, T=1e6 K, B=1 T     l.122-137    -> test_example_scales_1T
  Rechenbeispiel thermonuclear, B=5 T       l.141-162    -> test_example_thermonuclear
  <motion-electric-decomposition>           l.228-229    -> test_parallel_acceleration
  <motion-force-balance>, <motion-general-drift> l.251, 260, 281-291 -> test_force_drift
  <motion-exb-drift>                        l.269        -> test_exb_drift
  <motion-position-split>, <motion-velocity-split> l.378, 388 -> test_guiding_center_split
  <motion-magnetic-moment>                  l.402, 421-429 -> test_magnetic_moment
  mu adiabatic balance                      l.439-458    -> test_mu_balance
  Rechenbeispiel betatron (proton)          l.471-482    -> test_example_betatron
  <motion-mu-force>                         l.553, 598   -> test_mu_force_from_gyroaverage
  <motion-gradb-drift>                      l.563, 603-611 -> test_gradb_drift
  <motion-curvature-force>                  l.574        -> test_curvature_force
  <motion-curvature-drift>                  l.585        -> test_curvature_drift
  <motion-mirror-force>, <motion-mirror-energy> l.631, 642, 655-670 -> test_mirror_energy
  mirror point and loss cone                l.675-690    -> test_loss_cone
  Rechenbeispiel loss cone                  l.696-704    -> test_loss_cone
  <motion-polarization-split>/-exb          l.789, 793   -> test_polarization_drift
  <motion-polarization-drift>               l.803, 816-848 -> test_polarization_drift
  <motion-polarization-current>             l.858-860    -> test_polarization_current
  Rechenbeispiel polarization (electron)    l.868-880    -> test_example_polarization
  <motion-cyclotron-response>               l.973, 987-1016 -> test_cyclotron_response
  Rechenbeispiel resonance                  l.1029-1041  -> test_example_resonance

Run `python derivations/ch04_single_particle_motion.py` or `pytest derivations`.
"""

import sympy as sp
from sympy.physics import units as u

from si import Derivation, check, k_B

m, B, t, v_perp, T_s = sp.symbols("m B t v_perp T_s", positive=True)
q, Omega, delta = sp.symbols("q Omega delta", real=True)
mu = sp.symbols("mu", positive=True)
LOCAL = {m: u.kilogram, B: u.tesla, t: u.second, v_perp: u.meter / u.second,
         T_s: u.kelvin, q: u.coulomb, mu: u.joule / u.tesla}
V = u.meter / u.second


def vec(name, **kw):
    return sp.Matrix(sp.symbols(f"{name}_x {name}_y {name}_z", **kw))


def rounds_to(value, stated):
    """The computed value, rounded to the printed significant digits, equals the print."""
    digits = len(stated.split("e")[0].replace(".", "").lstrip("0"))
    assert float(f"{float(value):.{digits - 1}e}") == float(stated), f"{float(value):.4g} vs {stated}"


# Constants used in the worked examples (as printed in the script).
NUM = {"m_e": 9.109e-31, "m_i": 1.673e-27, "e": 1.602e-19,
       "eps0": 8.854e-12, "k_B": 1.381e-23}


def test_energy_theorem():
    d = Derivation("Magnetic force does no work", "src/chapters/04-single-particle-motion.typ:49")
    v, E, Bv = vec("v", real=True), vec("E", real=True), vec("B", real=True)
    # Lorentz force: m dv/dt = q (E + v x B).
    dvdt = q / m * (E + v.cross(Bv))
    d.eq("magnetic power", sp.Symbol(r"v \cdot (v \times B)"), sp.expand(v.dot(v.cross(Bv))))
    # d/dt (m v^2/2) = m v . dv/dt.
    power = d.eq("chain rule", sp.Symbol("dK/dt"), sp.expand((m * v.dot(dvdt))))
    check(power, q * E.dot(v))  # :49


def test_cyclotron_components():
    d = Derivation("Cyclotron components", "src/chapters/04-single-particle-motion.typ:59")
    vx, vy = sp.Function("v_x"), sp.Function("v_y")
    v = sp.Matrix([vx(t), vy(t), 0])
    F = q * v.cross(sp.Matrix([0, 0, B]))  # E = 0, B = B e_z
    d.eq("Lorentz x", vx(t).diff(t), F[0] / m)
    d.eq("Lorentz y", vy(t).diff(t), F[1] / m)
    W = q * B / m  # :59
    check(F[0] / m, W * vy(t))
    check(W, W, unit=1 / u.second, units=LOCAL)
    check(F[1] / m, -W * vx(t))
    # Solve the system; the stated orbit is the solution with phase delta.
    sx = v_perp * sp.cos(Omega * t + delta)
    sy = -v_perp * sp.sin(Omega * t + delta)  # :84
    d.eq("solution", vx(t), sx)
    d.eq("solution", vy(t), sy)
    assert sp.simplify(sx.diff(t) - Omega * sy) == 0
    assert sp.simplify(sy.diff(t) + Omega * sx) == 0
    sol = sp.dsolve([sp.Eq(vx(t).diff(t), Omega * vy(t)), sp.Eq(vy(t).diff(t), -Omega * vx(t))],
                    ics={vx(0): v_perp * sp.cos(delta), vy(0): -v_perp * sp.sin(delta)})
    check(sp.expand_trig(sol[0].rhs), sp.expand_trig(sx))
    check(sp.expand_trig(sol[1].rhs), sp.expand_trig(sy))
    # Speed is constant: the magnetic force only turns v.
    check(sp.simplify(sx**2 + sy**2), v_perp**2)


def test_gyroradius():
    d = Derivation("Gyroradius", "src/chapters/04-single-particle-motion.typ:77")
    rho = sp.Symbol("rho", positive=True)
    # Centripetal balance m v^2/rho = |q| v B.
    r_bal = d.eq("centripetal balance", rho,
                 sp.solve(sp.Eq(m * v_perp**2 / rho, sp.Abs(q) * v_perp * B), rho)[0])
    stated = m * v_perp / (sp.Abs(q) * B)  # :77
    check(r_bal, stated, unit=u.meter, units=LOCAL)
    # Integrate the velocity: the orbit is a circle of radius v_perp/|Omega|.
    s = sp.Symbol("s")
    x = sp.integrate(v_perp * sp.cos(Omega * s + delta), (s, 0, t), conds="none")
    y = sp.integrate(-v_perp * sp.sin(Omega * s + delta), (s, 0, t), conds="none")
    X, Y = sp.sin(delta) * v_perp / Omega, sp.cos(delta) * v_perp / Omega  # centre
    r2 = d.eq("integrate orbit", rho**2, sp.simplify((x + X) ** 2 + (y + Y) ** 2))
    W = q * B / m
    check(r2, v_perp**2 / Omega**2)
    check(sp.sqrt(r2.subs(Omega, W)), stated)


def test_thermal_gyroradius_units():
    d = Derivation("Thermal gyroradius", "src/chapters/04-single-particle-motion.typ:105")
    vth = sp.sqrt(2 * k_B * T_s / m)
    wc = sp.Abs(q) * B / m
    rho = d.eq("thermal estimate", sp.Symbol("rho_s"), vth / wc)
    check(wc, wc, unit=1 / u.second, units=LOCAL)
    check(rho, rho, unit=u.meter, units=LOCAL)


def _scales(n, Te, Ti, Bf):
    c = NUM
    lam = (c["eps0"] * c["k_B"] * Te / (n * c["e"] ** 2)) ** 0.5
    wpe = (n * c["e"] ** 2 / (c["eps0"] * c["m_e"])) ** 0.5
    wce, wci = c["e"] * Bf / c["m_e"], c["e"] * Bf / c["m_i"]
    rho_e = (2 * c["k_B"] * Te / c["m_e"]) ** 0.5 / wce
    rho_i = (2 * c["k_B"] * Ti / c["m_i"]) ** 0.5 / wci
    return dict(lam=lam, wpe=wpe, wce=wce, wci=wci, rho_e=rho_e, rho_i=rho_i,
                kTe_keV=c["k_B"] * Te / c["e"] / 1e3)


SHOW = {"lam": sp.Symbol("lambda_D"), "wpe": sp.Symbol("omega_pe"), "wce": sp.Symbol("omega_ce"),
        "wci": sp.Symbol("omega_ci"), "rho_e": sp.Symbol("rho_e"), "rho_i": sp.Symbol("rho_i"),
        "kTe_keV": sp.Symbol("k_B T_e/keV")}


def test_example_scales_1T():
    d = Derivation("Example: scales at 1e6 K, 1 T", "src/chapters/04-single-particle-motion.typ:135")
    s = _scales(1e20, 1e6, 1e6, 1.0)
    for k in ("lam", "wpe", "rho_e", "rho_i"):
        d.eq("SI value", SHOW[k], sp.Float(s[k], 3))
    # src/chapters/04-single-particle-motion.typ:135-137
    for k, stated in [("lam", "6.9e-6"), ("wpe", "5.6e11"), ("rho_e", "3.1e-5"), ("rho_i", "1.3e-3")]:
        rounds_to(s[k], stated)


def test_example_thermonuclear():
    d = Derivation("Example: thermonuclear scales", "src/chapters/04-single-particle-motion.typ:156")
    s = _scales(1e20, 1e8, 1e8, 5.0)
    for k in ("kTe_keV", "lam", "wpe", "wce", "wci", "rho_e", "rho_i"):
        d.eq("SI value", SHOW[k], sp.Float(s[k], 3))
    # src/chapters/04-single-particle-motion.typ:156-162
    rounds_to(s["kTe_keV"], "8.62")
    for k, stated in [("lam", "6.9e-5"), ("wpe", "5.6e11"), ("wce", "8.8e11"), ("wci", "4.8e8"),
                      ("rho_e", "6.3e-5"), ("rho_i", "2.7e-3")]:
        rounds_to(s[k], stated)


def test_parallel_acceleration():
    d = Derivation("Parallel acceleration", "src/chapters/04-single-particle-motion.typ:229")
    v, E = vec("v", real=True), vec("E", real=True)
    b = sp.Matrix([0, 0, 1])
    # Project the Lorentz force on b = B/B: (v x B) . b = 0.
    Fpar = d.eq("project on b", sp.Symbol("F_par"), (q * (E + v.cross(B * b))).dot(b))
    check(Fpar, q * E.dot(b), unit=u.newton, units={**LOCAL, E[2]: u.volt / u.meter})


def test_force_drift():
    d = Derivation("Homogeneous-force drift", "src/chapters/04-single-particle-motion.typ:260")
    vD, F, Bv = vec("vD"), vec("F", real=True), vec("B", real=True)
    B2 = Bv.dot(Bv)
    # Force balance F + q vD x B = 0 with vD perpendicular to B (and F . B = 0).
    eqs = list(F + q * vD.cross(Bv)) + [vD.dot(Bv)]
    d.step("force balance", sp.Eq(sp.Symbol("F") + q * sp.Symbol(r"v_D \times B"), 0))
    # Solvable only if F . B = 0; impose it by eliminating F_z (generic B_z != 0).
    Fz = sp.solve(F.dot(Bv), F[2])[0]
    sol = sp.solve([ex.subs(F[2], Fz) for ex in eqs], list(vD), dict=True)[0]
    derived = vD.subs(sol)
    stated = F.cross(Bv) / (q * B2)  # :260, :291
    for i in range(3):
        check(sp.simplify(derived[i] - stated[i].subs(F[2], Fz)), 0)
    d.eq("solve", sp.Symbol("v_D"), sp.Symbol(r"F \times B") / (q * sp.Symbol("B") ** 2))
    # Identity used in the text: (vD x B) x B = -vD B^2 for vD perpendicular to B.  # :286
    w = vec("w")
    wp = w - w.dot(Bv) / B2 * Bv
    check(sp.simplify((wp.cross(Bv).cross(Bv) + wp * B2)).norm(), 0)
    Fm, Bm = sp.symbols("F B_0", positive=True)
    check(Fm / (q * Bm), Fm / (q * Bm), unit=V,
          units={**LOCAL, Fm: u.newton, Bm: u.tesla})


def test_exb_drift():
    d = Derivation("E x B drift", "src/chapters/04-single-particle-motion.typ:269")
    E, Bv = vec("E", real=True), vec("B", real=True)
    vD = d.eq("F = qE", sp.Symbol("v_E"), q * E.cross(Bv) / (q * Bv.dot(Bv)))
    stated = E.cross(Bv) / Bv.dot(Bv)  # :269
    check(sp.simplify((vD - stated).norm()), 0)
    # Independent of q: check the full Lorentz force vanishes for E perpendicular to B.
    Bz = sp.Matrix([0, 0, B])
    Ep = sp.Matrix([sp.Symbol("E_x"), sp.Symbol("E_y"), 0])
    vE = Ep.cross(Bz) / B**2
    check(sp.simplify((q * (Ep + vE.cross(Bz))).norm()), 0)
    Em = sp.Symbol("E_0", positive=True)
    check(Em / B, Em / B, unit=V, units={**LOCAL, Em: u.volt / u.meter})


def test_guiding_center_split():
    d = Derivation("Guiding-centre split", "src/chapters/04-single-particle-motion.typ:388")
    Rg = sp.Matrix([sp.Function(f"R_{c}")(t) for c in "xyz"])
    rg = sp.Matrix([sp.Function(f"rho_{c}")(t) for c in "xyz"])
    d.eq("differentiate", sp.Symbol("v"), sp.Symbol("dR/dt") + sp.Symbol("drho/dt"))
    check(sp.simplify(((Rg + rg).diff(t) - Rg.diff(t) - rg.diff(t)).norm()), 0)


def test_magnetic_moment():
    d = Derivation("Magnetic moment of a gyro-orbit", "src/chapters/04-single-particle-motion.typ:429")
    wc = d.eq("gyrofrequency", sp.Symbol("omega_c"), sp.Abs(q) * B / m)
    rho = d.eq("gyroradius", sp.Symbol("rho"), v_perp / wc)
    I = d.eq("current", sp.Symbol("I"), sp.Abs(q) / (2 * sp.pi / wc))  # :425
    mu_d = d.eq("current x area", sp.Symbol("mu"), sp.simplify(I * sp.pi * rho**2))
    check(mu_d, sp.Abs(q) * wc * rho**2 / 2)  # :429
    stated = m * v_perp**2 / (2 * B)  # :402
    check(mu_d, stated, unit=u.joule / u.tesla, units=LOCAL)
    check(stated, stated, unit=u.ampere * u.meter**2, units=LOCAL)


def test_mu_balance():
    d = Derivation("Adiabatic balance for mu", "src/chapters/04-single-particle-motion.typ:458")
    s, vpar, Bf, muf = sp.Function("s"), sp.Function("v_par"), sp.Function("B"), sp.Function("mu")
    # Averaged mirror force and dB/dt = v_par dB/ds along the orbit.
    dvpar = -muf(t) * sp.Derivative(Bf(s(t)), s(t)) / m  # :439
    subs = {vpar(t).diff(t): dvpar, s(t).diff(t): vpar(t)}
    dKpar = d.eq("parallel energy", sp.Symbol("dK_par/dt"),
                 sp.diff(m * vpar(t) ** 2 / 2, t).subs(subs).doit())
    dmuB = d.eq("magnetic part", sp.Symbol("d(mu B)/dt"),
                sp.diff(muf(t) * Bf(s(t)), t).subs(subs).doit())
    total = d.eq("sum", sp.Symbol("d(K_par + mu B)/dt"), sp.simplify(dKpar + dmuB))
    check(total, Bf(s(t)) * muf(t).diff(t))  # :458
    # Static B: total kinetic energy m v_par^2/2 + m v_perp^2/2 = m v_par^2/2 + mu B is
    # conserved, so B dmu/dt = 0, i.e. mu is constant.


def test_example_betatron():
    d = Derivation("Example: adiabatic compression", "src/chapters/04-single-particle-motion.typ:481")
    B0, B1, v0 = sp.symbols("B_0 B_1 v_0", positive=True)
    v1 = sp.symbols("v_1", positive=True)
    # mu conserved: m v0^2/(2 B0) = m v1^2/(2 B1).
    v1s = d.eq("mu conserved", v1, sp.solve(sp.Eq(m * v0**2 / (2 * B0), m * v1**2 / (2 * B1)), v1)[0])
    vals = {B0: 0.01, B1: 0.04, v0: 1.0e5, m: 1.673e-27}
    rho = lambda v, Bf: m * v / (1.602e-19 * Bf)
    rounds_to(v1s.subs(vals), "2.00e5")  # :481
    rounds_to(rho(v0, B0).subs(vals), "0.104")  # :482
    rounds_to(rho(v1s, B1).subs(vals), "0.0522")


def test_mu_force_from_gyroaverage():
    d = Derivation("Mirror force from the gyro-average", "src/chapters/04-single-particle-motion.typ:553")
    B0, kap, X, th = sp.symbols("B_0 kappa X theta", real=True)
    # Weak gradient B = B0 (1 + kappa x) e_z. Unperturbed orbit, theta = Omega t,
    # Omega = q B0/m: v = v_perp (cos, -sin), x = X + (v_perp/Omega) sin.
    W = q * B0 / m
    v = sp.Matrix([v_perp * sp.cos(th), -v_perp * sp.sin(th), 0])
    x = X + v_perp / W * sp.sin(th)
    B1 = sp.Matrix([0, 0, B0 * kap * x])
    # Lorentz force of the gradient part, averaged over one gyration.
    F = q * v.cross(B1)
    Favg = d.eq("gyro-average", sp.Symbol("<F>"),
                sp.simplify(sp.integrate(F, (th, 0, 2 * sp.pi)) / (2 * sp.pi)))
    mu_ = m * v_perp**2 / (2 * B0)
    gradB = sp.Matrix([B0 * kap, 0, 0])
    stated = -mu_ * gradB  # :553
    check(sp.simplify((Favg - stated).norm()), 0)


def test_gradb_drift():
    d = Derivation("Grad-B drift", "src/chapters/04-single-particle-motion.typ:563")
    Bv, G = B * sp.Matrix([0, 0, 1]), vec("G", real=True)  # B = B e_z, G = grad B
    F = d.eq("mirror force", sp.Symbol("F_mu"), -mu * G)
    vD = d.eq("force drift", sp.Symbol("v_gradB"), F.cross(Bv) / (q * Bv.dot(Bv)))
    stated = mu * Bv.cross(G) / (q * Bv.dot(Bv))  # :563, :611
    check(sp.simplify((vD - stated).norm()), 0)
    g = sp.Symbol("g", positive=True)
    check(mu * B * g / (q * B**2), mu * g / (q * B), unit=V,
          units={**LOCAL, g: u.tesla / u.meter})


def test_curvature_force():
    d = Derivation("Centrifugal force on a curved field line",
                   "src/chapters/04-single-particle-motion.typ:574")
    Rc, vp = sp.symbols("R_c v_par", positive=True)
    # Guiding centre moving at v_par along a circle of radius R_c.
    p = Rc * sp.Matrix([sp.cos(vp * t / Rc), sp.sin(vp * t / Rc), 0])
    acc = d.eq("centripetal", sp.Symbol("a"), sp.simplify(p.diff(t, 2)))
    Rvec = -p  # points from the particle to the centre of curvature
    Fcf = d.eq("centrifugal", sp.Symbol("F_curv"), -m * acc)
    stated = -m * vp**2 * Rvec / Rc**2  # :574
    check(sp.simplify((Fcf - stated).norm()), 0)
    check(m * vp**2 / Rc, m * vp**2 / Rc, unit=u.newton,
          units={**LOCAL, Rc: u.meter, vp: V})


def test_curvature_drift():
    d = Derivation("Curvature drift", "src/chapters/04-single-particle-motion.typ:585")
    Rc, vp = sp.symbols("R_c v_par", positive=True)
    Rv = vec("R", real=True)
    Bv = B * sp.Matrix([0, 0, 1])
    Rv = sp.Matrix([Rv[0], Rv[1], 0])  # R_c perpendicular to b
    F = -m * vp**2 * Rv / Rc**2
    vD = d.eq("force drift", sp.Symbol("v_curv"), F.cross(Bv) / (q * B**2))
    kappa = Rv / Rc**2
    stated = m * vp**2 / (q * B) * sp.Matrix([0, 0, 1]).cross(kappa)  # :585
    check(sp.simplify((vD - stated).norm()), 0)
    check(m * vp**2 / (q * B * Rc), m * vp**2 / (q * B * Rc), unit=V,
          units={**LOCAL, Rc: u.meter, vp: V})


def test_mirror_energy():
    d = Derivation("Mirror energy", "src/chapters/04-single-particle-motion.typ:642")
    s, vpar, Bf = sp.Function("s"), sp.Function("v_par"), sp.Function("B")
    subs = {vpar(t).diff(t): -mu * sp.Derivative(Bf(s(t)), s(t)) / m,  # :631
            s(t).diff(t): vpar(t)}
    K = d.eq("energy", sp.Symbol("K"), m * vpar(t) ** 2 / 2 + mu * Bf(s(t)))
    dK = d.eq("time derivative", sp.Symbol("dK/dt"), sp.simplify(K.diff(t).subs(subs).doit()))
    check(dK, 0)  # :642, :670


def test_loss_cone():
    d = Derivation("Mirror point and loss cone", "src/chapters/04-single-particle-motion.typ:686")
    v0, B0, Bm, al = sp.symbols("v_0 B_0 B_m alpha_0", positive=True)
    mu0 = m * (v0 * sp.sin(al)) ** 2 / (2 * B0)  # :675-681
    # K conserved: at the mirror point v_par = 0, so mu B_m = m v0^2/2.
    Bms = d.eq("v_par = 0", Bm, sp.solve(sp.Eq(mu0 * Bm, m * v0**2 / 2), Bm)[0])
    check(Bms / B0, 1 / sp.sin(al) ** 2)  # :686
    # Critical angle: B_m = B_max.
    ac = d.eq("B_m = B_max", sp.Symbol("alpha_c"), sp.asin(sp.sqrt(sp.Rational(1, 100) / sp.Rational(5, 100))))
    rounds_to(ac * 180 / sp.pi, "26.6")  # :703


def test_polarization_drift():
    d = Derivation("Polarization drift", "src/chapters/04-single-particle-motion.typ:803")
    a = sp.Symbol("a", real=True)  # dE_x/dt for a linearly ramping field
    Bz = sp.Matrix([0, 0, B])
    E = sp.Matrix([a * t, 0, 0])
    # Ansatz: orbit-centre velocity linear in t, v = c0 + c1 t.
    c0, c1 = vec("c0"), vec("c1")
    v = c0 + c1 * t
    lorentz = m * v.diff(t) - q * (E + v.cross(Bz))
    eqs = [co for comp in lorentz for co in sp.Poly(comp, t).all_coeffs()]
    sol = sp.solve(eqs + [c0[2], c1[2]], list(c0) + list(c1), dict=True)[0]
    vsol = d.eq("Lorentz, ramp", sp.Symbol("v_perp"), sp.simplify(v.subs(sol)))
    vE = E.cross(Bz) / B**2  # :793
    vpol = m / (q * B**2) * E.diff(t)  # :803
    d.eq("split", sp.Symbol("v_perp"), sp.Symbol("v_E") + sp.Symbol("v_pol"))
    check(sp.simplify((vsol - vE - vpol).norm()), 0)  # :789 (no gyration for this IC)
    # Text steps: delta v = m/(q B^2) B x dv_E/dt and B x (A x B) = B^2 A.  # :837-848
    A = sp.Matrix([sp.Symbol("A_x"), sp.Symbol("A_y"), 0])
    check(sp.simplify((Bz.cross(A.cross(Bz)) - B**2 * A).norm()), 0)
    dv = m / (q * B**2) * Bz.cross(vE.diff(t))
    check(sp.simplify((dv - vpol).norm()), 0)
    Ed = sp.Symbol("Edot", positive=True)
    check(m * Ed / (q * B**2), m * Ed / (q * B**2), unit=V,
          units={**LOCAL, Ed: u.volt / u.meter / u.second})


def test_polarization_current():
    d = Derivation("Polarization current", "src/chapters/04-single-particle-motion.typ:858")
    n1, n2, m1, m2, q1, q2, Ed = sp.symbols("n_1 n_2 m_1 m_2 q_1 q_2 Edot", positive=True)
    j = d.eq("species sum", sp.Symbol("j_pol"),
             sum(n * qq * mm / (qq * B**2) * Ed for n, qq, mm in [(n1, q1, m1), (n2, -q2, m2)]))
    stated = (n1 * m1 + n2 * m2) / B**2 * Ed  # :858-860
    check(j, stated, unit=u.ampere / u.meter**2,
          units={B: u.tesla, n1: u.meter**-3, n2: u.meter**-3, m1: u.kilogram,
                 m2: u.kilogram, Ed: u.volt / u.meter / u.second})


def test_example_polarization():
    d = Derivation("Example: electron polarization drift",
                   "src/chapters/04-single-particle-motion.typ:879")
    me, ee, Bf, E0, wd = 9.109e-31, 1.602e-19, 0.01, 3.0e4, 1.0e5
    # |dE/dt| amplitude = omega_d E0.
    vpol = d.eq("amplitude", sp.Symbol("v_pol"), sp.Float(me * wd * E0 / (ee * Bf**2), 4))
    ratio = d.eq("ordering", sp.Symbol("omega_d") / sp.Symbol("Omega_e"),
                 sp.Float(wd / (ee * Bf / me), 4))
    rounds_to(vpol, "171")  # :879
    rounds_to(ratio, "5.69e-5")  # :880


def test_cyclotron_response():
    d = Derivation("Circular cyclotron response", "src/chapters/04-single-particle-motion.typ:973")
    vx, vy, Ex, Ey = [sp.Function(n)(t) for n in ("v_x", "v_y", "E_x", "E_y")]
    W = q * B / m
    # Lorentz with B = B e_z (:987).
    rx = q / m * Ex + W * vy
    ry = q / m * Ey - W * vx
    vcw, Ecw = vx + sp.I * vy, Ex + sp.I * Ey
    lhs = d.eq("combine x + i y", sp.Symbol("dv_cw/dt"), sp.expand(rx + sp.I * ry))
    check(lhs, sp.expand(q / m * Ecw - sp.I * W * vcw))  # :973, :993
    # Harmonic drive exp(-i w t).
    w, Et, vt = sp.symbols("omega E_t v_t")
    amp = d.eq("harmonic drive", vt, sp.solve(-sp.I * w * vt + sp.I * Omega * vt - q / m * Et, vt)[0])
    check(amp, q * Et / (sp.I * m * (Omega - w)))  # :1008
    # Free gyration for q B > 0: v_cw = v_perp exp(-i Omega t) (clockwise).
    free = (v_perp * sp.cos(Omega * t) - sp.I * v_perp * sp.sin(Omega * t))
    check(sp.simplify((free - v_perp * sp.exp(-sp.I * Omega * t)).rewrite(sp.exp)), 0)
    # Counter-rotating combination: denominator omega + Omega.  # :1016
    vccw, Eccw = vx - sp.I * vy, Ex - sp.I * Ey
    check(sp.expand(rx - sp.I * ry), sp.expand(q / m * Eccw + sp.I * W * vccw))
    amp2 = d.eq("counter-rotating", vt, sp.solve(-sp.I * w * vt - sp.I * Omega * vt - q / m * Et, vt)[0])
    check(sp.simplify(amp2 * (w + Omega)), sp.I * q * Et / m)


def test_example_resonance():
    d = Derivation("Example: cyclotron resonance", "src/chapters/04-single-particle-motion.typ:1039")
    ee, Bf = 1.602e-19, 0.01
    we = d.eq("electron", sp.Symbol("omega_res,e"), sp.Float(ee * Bf / 9.109e-31, 4))
    wi = d.eq("proton", sp.Symbol("omega_res,i"), sp.Float(ee * Bf / 1.673e-27, 4))
    rounds_to(we, "1.76e9")  # :1039
    rounds_to(wi, "9.58e5")


if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
