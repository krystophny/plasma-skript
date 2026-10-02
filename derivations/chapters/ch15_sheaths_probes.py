"""Chapter 15, sheaths and probes: src/chapters/15-sheaths-probes.typ.

Run `python derivations/ch15_sheaths_probes.py` to check every step, or
`pytest derivations` to check every chapter.

Coverage (line in src/chapters/15-sheaths-probes.typ -> test):
  79-83, 94-131   Maxwellian half-space flux, three forms      -> test_half_space_flux
  108-110, 122    Gaussian and half-space integrals            -> test_half_space_flux
  135, 139        mean speed and Gamma = n v_mean / 4          -> test_mean_speed_form
  83, 147-152     Gamma_e0/Gamma_i0 = sqrt(m_i/m_e) ~ 42.8     -> test_flux_ratio
  272-278         Boltzmann electrons n_e = n0 exp(-eta)       -> test_boltzmann_electrons
  283-305         ion energy, u_i^2 = c_s^2 (M^2+2 eta), n_i/n_s -> test_cold_ion_density
  310-323         normalized sheath equation                   -> test_sheath_equation
  329-337, 258-259 small-eta expansion, Bohm M >= 1            -> test_bohm_criterion
  357-366         Child-Langmuir ion speed, density, C         -> test_child_langmuir_poisson
  372-391         first integral and V(s) ~ s^(4/3)            -> test_child_langmuir_profile
  396-402, 446    V_w^(3/2) relation and Child-Langmuir J_i    -> test_child_langmuir_current
  409-425         numerical example (10 eV, M = 1.5)           -> test_example_bohm_numbers
  509, 537-539    Boltzmann transmission of electrons          -> test_electron_transmission
  517-526, 547-570 zero-current floating potential            -> test_floating_potential
  526, 606-611    hydrogen coefficient -2.84                   -> test_floating_coefficient_hydrogen
  577-595         numerical example (3 eV hydrogen)            -> test_example_floating_numbers
  674-676         probe current I_p = A(e Gamma_i - e Gamma_e)  -> test_probe_semilog
  683-693, 704-725 semilog line, slope, inverse slope          -> test_probe_semilog
  697-698, 734-743 density from electron saturation            -> test_probe_density
  755-756         animation density profile n_i/n0 at M = 1.5  -> test_cold_ion_density
  775             animation ion-saturation level 0.058         -> test_probe_animation_level
  782-791         numerical example (0.40 V^-1, 4.0 mA)        -> test_example_probe_numbers
  figure sheath-profile: first integral of the sheath equation -> test_sheath_first_integral
"""

import sympy as sp
from sympy.physics import units as u

from si import (BLUE, GRAY, ORANGE, UNITS, Derivation, check, e, eps0, figure, k_B,
                label, m_e, m_i, save)

SRC = "src/chapters/15-sheaths-probes.typ"

n_s, n0, T_s, T_e, m_s = sp.symbols("n_s n_0 T_s T_e m_s", positive=True)
vx, vy, vz, v = sp.symbols("v_x v_y v_z v", real=True)
eta, M, xi, lam = sp.symbols("eta M xi lambda_D", positive=True)
V, s, d_w, C, Gam_i, Vw = sp.symbols("V s d C Gamma_i V_w", positive=True)
phi, phi_w, phi_p, phi_pl = sp.symbols("phi phi_w phi_p phi_pl", real=True)
A, Gam_e0 = sp.symbols("A Gamma_e0", positive=True)
UNITS.update({
    n_s: u.meter**-3, n0: u.meter**-3, T_s: u.kelvin, T_e: u.kelvin,
    m_s: u.kilogram, V: u.volt, Vw: u.volt, d_w: u.meter, s: u.meter,
    Gam_i: u.meter**-2 / u.second, Gam_e0: u.meter**-2 / u.second,
    A: u.meter**2, phi: u.volt, phi_w: u.volt, phi_p: u.volt, phi_pl: u.volt,
    lam: u.meter,
})

# Results shared by the tests and the plots: each test proves its derivation
# equals one of these expressions, and each plot_* lambdifies the same one.
N_E = sp.exp(-eta)  # n_e/n_0, line 278
N_I = M / sp.sqrt(M**2 + 2 * eta)  # n_i/n_s, line 305
SHEATH_RHS = N_I - N_E  # d^2 eta/d xi^2, line 324
# Sagdeev potential: (d eta/d xi)^2/2 = SAGDEEV with eta = eta' = 0 at the edge.
SAGDEEV = M * (sp.sqrt(M**2 + 2 * eta) - M) + sp.exp(-eta) - 1
FLUX_RATIO = sp.sqrt(2 * sp.pi * m_e / m_i)  # Gamma_i/Gamma_e0, lines 565-566
u_b = sp.Symbol("u", real=True)  # u = e (phi_p - phi_pl)/(k_B T_e)
PROBE_RETARDING = Gam_i / Gam_e0 - sp.exp(u_b)  # I_p/(e A Gamma_e0) for u <= 0, line 676

# CODATA 2018 values (SI, exact where defined).
E_CODATA = 1.602176634e-19
ME_CODATA = 9.1093837015e-31
MP_CODATA = 1.67262192369e-27
EPS0_CODATA = 8.8541878128e-12


class _Silent:
    """Stand-in for Derivation when a helper's steps were already recorded."""

    def step(self, label, expr):
        return expr

    def eq(self, label, lhs, rhs):
        return rhs


def num(d, label, lhs, val):
    """Record a numerical result rounded to four digits; return the full value."""
    d.eq(label, lhs, sp.Float(float(val), 4))
    return val


def close(x, y, rel):
    assert abs(float(x) / float(y) - 1) < rel, f"{float(x)} vs {float(y)}"


def maxwellian(n, T, m):
    return n * (m / (2 * sp.pi * k_B * T)) ** sp.Rational(3, 2) * sp.exp(
        -m * (vx**2 + vy**2 + vz**2) / (2 * k_B * T))


def half_space_flux(n, T, m, vmin=0):
    """Gamma = int_{vz>vmin} vz f d^3v for a 3D Maxwellian (integrated, not quoted)."""
    return sp.integrate(vz * maxwellian(n, T, m),
                        (vx, -sp.oo, sp.oo), (vy, -sp.oo, sp.oo), (vz, vmin, sp.oo))


def test_half_space_flux():
    d = Derivation("Maxwellian half-space flux", f"{SRC}:94-131")
    G = sp.Symbol("Gamma_s0")
    d.eq("Maxwellian", sp.Symbol("f_s"), sp.Mul(n_s, sp.Pow(m_s / (2 * sp.pi * k_B * T_s), sp.Rational(3, 2), evaluate=False),
          sp.exp(-m_s * sp.Symbol("v") ** 2 / (2 * k_B * T_s)), evaluate=False))
    # Tangential Gaussian integral and normal half-space integral.
    gauss = sp.integrate(sp.exp(-m_s * vx**2 / (2 * k_B * T_s)), (vx, -sp.oo, sp.oo))
    d.eq("tangential", sp.Integral(sp.exp(-m_s * vx**2 / (2 * k_B * T_s)), (vx, -sp.oo, sp.oo)), gauss)
    check(gauss, sp.sqrt(2 * sp.pi * k_B * T_s / m_s))  # src/chapters/15-sheaths-probes.typ:110
    a = sp.symbols("a", positive=True)
    half = d.eq("normal", sp.Integral(v * sp.exp(-a * v**2), (v, 0, sp.oo)),
                sp.integrate(v * sp.exp(-a * v**2), (v, 0, sp.oo)))
    check(half, 1 / (2 * a))  # :122
    Gamma = d.eq("integrate", G, half_space_flux(n_s, T_s, m_s))
    stated = n_s * sp.sqrt(k_B * T_s / (2 * sp.pi * m_s))  # :127
    check(Gamma, stated, unit=u.meter**-2 / u.second)
    v_th = sp.sqrt(2 * k_B * T_s / m_s)  # :82
    d.eq("thermal speed", G, n_s * sp.Symbol("v_th") / (2 * sp.sqrt(sp.pi)))
    check(Gamma, n_s * v_th / (2 * sp.sqrt(sp.pi)))  # :131


def test_mean_speed_form():
    d = Derivation("Mean speed form of the flux", f"{SRC}:135-139")
    w = sp.symbols("w", positive=True)
    fsp = 4 * sp.pi * w**2 * (m_s / (2 * sp.pi * k_B * T_s)) ** sp.Rational(3, 2) \
        * sp.exp(-m_s * w**2 / (2 * k_B * T_s))
    v_mean = d.eq("speed average", sp.Integral(w * fsp, (w, 0, sp.oo)),
                  sp.integrate(w * fsp, (w, 0, sp.oo)))
    check(v_mean, sp.sqrt(8 * k_B * T_s / (sp.pi * m_s)), unit=u.meter / u.second)  # :135
    d.eq("ratio", sp.Symbol("Gamma_s0") / sp.Symbol("v_mean"),
         sp.simplify(half_space_flux(n_s, T_s, m_s) / (n_s * v_mean)) * n_s)
    check(half_space_flux(n_s, T_s, m_s), n_s * v_mean / 4)  # :139


def test_flux_ratio():
    d = Derivation("Electron to ion flux ratio", f"{SRC}:83, 147-152")
    ratio = d.eq("equal n, T", sp.Symbol("Gamma_e0") / sp.Symbol("Gamma_i0"),
                 half_space_flux(n_s, T_s, m_e) / half_space_flux(n_s, T_s, m_i))
    check(ratio, sp.sqrt(m_i / m_e))  # :83
    d.eq("mass ratio 1836", sp.sqrt(sp.Integer(1836), evaluate=False), sp.N(sp.sqrt(1836), 4))
    close(sp.sqrt(1836), 42.8, 2e-3)  # :152


def test_boltzmann_electrons():
    d = Derivation("Boltzmann electrons", f"{SRC}:272-278")
    # Force balance for isothermal electrons: k_B T_e dn_e/dphi = e n_e.
    ne = sp.Function("n_e")
    ode = d.step("force balance", sp.Eq(k_B * T_e * ne(phi).diff(phi), e * ne(phi)))
    sol = d.eq("solve", ne(phi), sp.dsolve(ode, ne(phi), ics={ne(0): n0}).rhs)
    check(sol, n0 * sp.exp(e * phi / (k_B * T_e)))  # :278
    out = d.eq("eta", ne(phi), sol.subs(phi, -k_B * T_e * eta / e))
    check(out, n0 * N_E)  # :278


def ion_density_ratio(d=None):
    """Cold ions: energy conservation plus flux conservation n_i u_i = n_s u_s."""
    us, ui = sp.symbols("u_s u_i", positive=True)
    x = sp.symbols("x")
    uf, pf = sp.Function("u_i")(x), sp.Function("phi")(x)
    mom = m_i * uf * uf.diff(x) + e * pf.diff(x)  # :287
    assert sp.simplify(sp.diff(m_i * uf**2 / 2 + e * pf, x) - mom) == 0  # :292
    # Energy at edge (phi = 0) and inside, with e phi = -k_B T_e eta.
    ui2 = sp.solve(sp.Eq(m_i * ui**2 / 2 - k_B * T_e * eta, m_i * us**2 / 2), ui**2)[0]
    c_s = sp.sqrt(k_B * T_e / m_i)
    check(ui2, us**2 + 2 * k_B * T_e * eta / m_i)  # :300
    check(ui2.subs(us, M * c_s), c_s**2 * (M**2 + 2 * eta))  # :301
    if d is not None:
        d.step("momentum", sp.Eq(mom, 0))
        d.step("energy", sp.Eq(m_i * ui**2 / 2 + e * phi, m_i * us**2 / 2))
        d.eq("solve", ui**2, ui2)
        d.eq("continuity", sp.Symbol("n_i") / sp.Symbol("n_s"), us / ui)
    return (us / sp.sqrt(ui2)).subs(us, M * c_s)


def test_cold_ion_density():
    d = Derivation("Cold ion density in the sheath", f"{SRC}:283-305")
    ratio = d.eq("Mach number", sp.Symbol("n_i") / sp.Symbol("n_s"),
                 sp.simplify(ion_density_ratio(d)))
    check(ratio, N_I)  # :305
    anim = d.eq("M = 1.5", sp.Symbol("n_i") / n0, ratio.subs(M, sp.Rational(3, 2)))
    check(anim, sp.Rational(3, 2) / sp.sqrt(sp.Rational(9, 4) + 2 * eta))  # :756


def test_sheath_equation():
    d = Derivation("Normalized sheath equation", f"{SRC}:310-324")
    etaf = sp.Function("eta")(xi)
    ni, ne = sp.symbols("n_i n_e", positive=True)
    phi_of_x = -(k_B * T_e / e) * etaf
    lhs = -sp.diff(phi_of_x, xi, 2) / lam**2  # d^2/dx^2 = lambda^-2 d^2/dxi^2
    check(sp.simplify(-lhs), -(k_B * T_e / (e * lam**2)) * etaf.diff(xi, 2))  # :318
    eq = d.step("Poisson", sp.Eq(lhs, e * (ni - ne) / eps0))
    lam_D2 = eps0 * k_B * T_e / (n0 * e**2)
    eta2 = d.eq("Debye length", etaf.diff(xi, 2),
                sp.expand(sp.solve(eq.subs(lam, sp.sqrt(lam_D2)), etaf.diff(xi, 2))[0]))
    check(eta2, ni / n0 - ne / n0)  # :323
    rhs = d.eq("densities", etaf.diff(xi, 2),
               sp.simplify(eta2.subs({ni: n0 * ion_density_ratio(), ne: n0 * sp.exp(-eta)})))
    check(rhs, SHEATH_RHS)  # :324


def test_sheath_first_integral():
    # Multiply eta'' = SHEATH_RHS by eta' and integrate from the edge (eta = eta' = 0).
    d = Derivation("Sheath first integral (Sagdeev potential)", f"{SRC}:324")
    S = d.eq("integrate", sp.Symbol("S"), sp.integrate(SHEATH_RHS.subs(eta, xi), (xi, 0, eta)))
    check(S, SAGDEEV)
    assert sp.simplify(sp.diff(SAGDEEV, eta) - SHEATH_RHS) == 0 and SAGDEEV.subs(eta, 0) == 0
    # Near the edge S ~ (1 - 1/M^2) eta^2/2: real eta' requires the Bohm criterion.
    lead = d.eq("series", sp.Symbol("S"), sp.series(SAGDEEV, eta, 0, 3).removeO())
    check(lead, (1 - M**-2) * eta**2 / 2)
    # At M = 1 the leading term is cubic and positive.
    check(sp.series(SAGDEEV.subs(M, 1), eta, 0, 4).removeO(), eta**3 / 3)


def test_bohm_criterion():
    d = Derivation("Bohm criterion", f"{SRC}:259, 329-337")
    rhs = M / (M**2 + 2 * eta) ** sp.Rational(1, 2) - sp.exp(-eta)
    ion = d.eq("series", M / sp.sqrt(M**2 + 2 * eta),
               sp.series(M / (M**2 + 2 * eta) ** sp.Rational(1, 2), eta, 0, 2).removeO())
    check(ion, 1 - eta / M**2)  # :331
    lin = d.eq("series", sp.Derivative(sp.Function("eta")(xi), xi, 2),
               sp.factor(sp.series(rhs, eta, 0, 2).removeO()))
    check(lin, (1 - M**-2) * eta)  # :259, :337
    # Monotone barrier requires a non-negative curvature coefficient.
    sol = sp.solve_univariate_inequality(1 - M**-2 >= 0, M, relational=False)
    assert sol.intersect(sp.Interval(0, sp.oo)) == sp.Interval(1, sp.oo)
    d.step("Bohm", M >= 1)


def test_child_langmuir_poisson():
    d = Derivation("Child-Langmuir: ion density and Poisson", f"{SRC}:357-368")
    # Zero injection energy: m_i u^2/2 = e V; flux conservation n_i = Gamma_i/u_i.
    w = sp.Symbol("u_i", positive=True)
    ui = d.eq("energy", w, sp.solve(sp.Eq(m_i * w**2 / 2, e * V), w)[0])
    check(ui, sp.sqrt((2 * e * V) / m_i), unit=u.meter / u.second)  # :357
    n_i = d.eq("flux", sp.Symbol("n_i"), Gam_i / ui)
    check(n_i, Gam_i * sp.sqrt(m_i / (2 * e * V)), unit=u.meter**-3)  # :361
    # Poisson with phi = -V and no electrons: V'' = e n_i / eps0 = C V^(-1/2).
    C_stated = (Gam_i / eps0) * sp.sqrt((e * m_i) / 2)  # :368
    d.eq("Poisson", sp.Derivative(sp.Function("V")(sp.Symbol("x")), sp.Symbol("x"), 2),
         e * n_i / eps0)
    check(e * n_i / eps0, C_stated * V ** sp.Rational(-1, 2), unit=u.volt / u.meter**2)


def child_langmuir_profile(d):
    """Solve V'' = C V^(-1/2) with V(0) = V'(0) = 0 by quadrature."""
    Vs = sp.Function("V")(s)
    d.step("ODE", sp.Eq(Vs.diff(s, 2), C / sp.sqrt(Vs)))
    # First integral: d/ds[(V')^2/2 - 2 C V^(1/2)] = V' (V'' - C V^(-1/2)) = 0.
    E1 = Vs.diff(s) ** 2 / 2 - 2 * C * sp.sqrt(Vs)
    assert sp.simplify(sp.diff(E1, s).subs(Vs.diff(s, 2), C / sp.sqrt(Vs))) == 0
    d.step("first integral", sp.Eq(E1, 0))
    # Edge values V = 0, V' = 0 give C_1 = 0, positive branch.
    Vp = sp.sqrt(4 * C * sp.sqrt(V))
    check(Vp / V ** sp.Rational(1, 4), 2 * sp.sqrt(C))  # :383
    W = sp.symbols("W", positive=True)
    left = d.eq("separate", sp.Integral(W ** sp.Rational(-1, 4), (W, 0, V)),
                sp.integrate(W ** sp.Rational(-1, 4), (W, 0, V)))
    check(left, sp.Rational(4, 3) * V ** sp.Rational(3, 4))  # :387
    Vsol = sp.solve(sp.Eq(left, 2 * sp.sqrt(C) * s), V)[0]
    d.eq("solve", V ** sp.Rational(3, 2),
         sp.expand_power_base(Vsol ** sp.Rational(3, 2), force=True))
    return Vsol


def test_child_langmuir_profile():
    d = Derivation("Child-Langmuir profile", f"{SRC}:372-391")
    Vsol = child_langmuir_profile(d)
    stated = ((9 * C) / 4) ** sp.Rational(2, 3) * s ** sp.Rational(4, 3)  # :391
    check(Vsol, stated)
    # Independent check: the profile satisfies the ODE and both edge conditions.
    assert sp.simplify(sp.diff(stated, s, 2) - C / sp.sqrt(stated)) == 0
    assert stated.subs(s, 0) == 0 and sp.diff(stated, s).subs(s, 0) == 0
    check(sp.diff(stated, s) ** 2 / 2, 2 * C * sp.sqrt(stated))  # :377


def test_child_langmuir_current():
    d = Derivation("Child-Langmuir current", f"{SRC}:396-402")
    Vsol = child_langmuir_profile(_Silent())
    wall = d.eq("wall", Vw ** sp.Rational(3, 2),
                sp.expand_power_base(Vsol.subs(s, d_w) ** sp.Rational(3, 2), force=True))
    check(wall, ((9 * C) / 4) * d_w**2)  # :396
    C_expr = (Gam_i / eps0) * sp.sqrt(e * m_i / 2)
    G = sp.solve(sp.Eq(Vw ** sp.Rational(3, 2), sp.Rational(9, 4) * C_expr * d_w**2), Gam_i)[0]
    J = d.eq("solve", sp.Symbol("J_i"), e * G)
    stated = (4 * eps0) / 9 * sp.sqrt((2 * e) / m_i) * Vw ** sp.Rational(3, 2) / d_w**2  # :401
    check(J, stated, unit=u.ampere / u.meter**2)


def test_example_bohm_numbers():
    d = Derivation("Example: sheath edge at 10 eV", f"{SRC}:409-425")
    ev, n, mi, M_ = 1.602e-19, 1.0e16, 1.673e-27, 1.50  # inputs as printed
    kT = 10.0 * ev
    lamD = num(d, "m", lam, (EPS0_CODATA * kT / (n * ev**2)) ** 0.5)
    cs = num(d, "m/s", sp.Symbol("c_s"), (kT / mi) ** 0.5)
    num(d, "m/s", sp.Symbol("u_s"), M_ * cs)
    num(d, "flux", Gam_i, n * M_ * cs)
    close(lamD, 2.35e-4, 5e-3)  # :421
    close(cs, 3.09e4, 5e-3)  # :422
    close(M_ * cs, 4.64e4, 5e-3)  # :423
    close(n * M_ * cs, 4.64e20, 5e-3)  # :424
    # Same with CODATA e and proton mass.
    close((EPS0_CODATA * 10 / (n * E_CODATA)) ** 0.5, 2.35e-4, 5e-3)
    close((10 * E_CODATA / MP_CODATA) ** 0.5, 3.09e4, 5e-3)


def test_electron_transmission():
    d = Derivation("Boltzmann transmission", f"{SRC}:509, 537-539")
    Vb = sp.symbols("V_b", positive=True)  # barrier |phi_w|
    UNITS[Vb] = u.volt
    G0 = half_space_flux(n0, T_e, m_e)
    # Electrons with m_e vz^2/2 > e |phi_w| pass; the flux is conserved along orbits.
    vmin = d.eq("barrier", sp.Symbol("v_min"), sp.sqrt(2 * e * Vb / m_e))
    Gt = d.eq("integrate", sp.Symbol("Gamma_e"), half_space_flux(n0, T_e, m_e, vmin))
    check(Gt, G0 * sp.exp(-(e * Vb) / (k_B * T_e)))  # :538
    out = d.eq("negative wall", sp.Symbol("Gamma_e") / sp.Symbol("Gamma_e0"),
               sp.simplify(Gt.subs(Vb, -phi_w) / G0))
    check(out, sp.exp((e * phi_w) / (k_B * T_e)))  # :539, :509


def test_floating_potential():
    d = Derivation("Floating potential", f"{SRC}:547-570")
    J = d.eq("net current", sp.Symbol("J"),
             e * Gam_i - e * Gam_e0 * sp.exp(e * phi_w / (k_B * T_e)))  # :551
    phi_f = d.eq("zero current", sp.Symbol("phi_f"),
                 sp.expand_log(sp.solve(sp.Eq(J, 0), phi_w)[0], force=True))
    check(phi_f, ((k_B * T_e) / e) * sp.log(Gam_i / Gam_e0), unit=u.volt)  # :560
    # Ideal edge fluxes: Bohm ions and unretarded Maxwellian electrons.
    Gi = n0 * sp.sqrt((k_B * T_e) / m_i)  # :565
    Ge = d.eq("Maxwellian", Gam_e0, half_space_flux(n0, T_e, m_e))
    check(Ge, n0 * sp.sqrt((k_B * T_e) / (2 * sp.pi * m_e)))  # :566
    ratio = d.eq("flux ratio", Gam_i / Gam_e0, sp.simplify(Gi / Ge))
    check(ratio, FLUX_RATIO)
    # ln(ratio) = ln(ratio^2)/2 keeps the mass ratio inside one logarithm.
    val = d.eq("Bohm flux", sp.Symbol("phi_f"),
               sp.Mul(k_B * T_e / (2 * e), sp.log(sp.simplify(ratio**2)), evaluate=False))
    check(sp.expand_log(val, force=True),
          sp.expand_log(phi_f.subs({Gam_i: Gi, Gam_e0: Ge}), force=True))
    stated = ((k_B * T_e) / (2 * e)) * sp.log((2 * sp.pi * m_e) / m_i)  # :570
    check(sp.expand_log(val, force=True), sp.expand_log(stated, force=True), unit=u.volt)


def test_floating_coefficient_hydrogen():
    d = Derivation("Hydrogen floating coefficient", f"{SRC}:572-574")
    ratio = num(d, "CODATA", 2 * sp.pi * m_e / m_i, 2 * sp.pi * ME_CODATA / MP_CODATA)
    num(d, "log", e * sp.Symbol("phi_f") / (k_B * T_e), sp.log(ratio) / 2)
    close(ratio, 0.00342, 1e-3)  # :572
    close(sp.log(ratio), -5.68, 1e-3)  # :573
    close(sp.log(ratio) / 2, -2.84, 1e-3)  # :526, :574, :611


def test_example_floating_numbers():
    d = Derivation("Example: floating surface at 3 eV", f"{SRC}:577-595")
    ev, n, me, mi, A_ = 1.602e-19, 1.0e16, 9.109e-31, 1.673e-27, 1.0e-4
    kT = 3.00 * ev
    lamD = num(d, "m", lam, (EPS0_CODATA * kT / (n * ev**2)) ** 0.5)
    Ge = num(d, "flux", Gam_e0, n * (kT / (2 * sp.pi * me)) ** 0.5)
    Gi = num(d, "flux", Gam_i, n * (kT / mi) ** 0.5)
    u_f = num(d, "log ratio", e * sp.Symbol("phi_f") / (k_B * T_e), sp.log(Gi / Ge))
    num(d, "mA", sp.Symbol("I_i"), ev * Gi * A_ * 1e3)
    close(lamD, 1.29e-4, 5e-3)  # :589
    close(Ge, 2.90e21, 5e-3)  # :590
    close(Gi, 1.70e20, 5e-3)  # :591
    close(u_f, -2.84, 5e-3)  # :592
    close(3.00 * u_f, -8.52, 5e-3)  # :593
    close(ev * Gi * A_ * 1e3, 2.72, 5e-3)  # :594 (mA)


def test_probe_semilog():
    d = Derivation("Langmuir probe: semilog slope", f"{SRC}:674-725")
    Ge = Gam_e0 * sp.exp(e * (phi_p - phi_pl) / (k_B * T_e))  # :704
    I_p = d.eq("probe current", sp.Symbol("I_p"), A * (e * Gam_i - e * Ge))  # :676
    I_i = e * A * Gam_i  # :693
    I_e = d.eq("subtract ions", sp.Symbol("I_e"), sp.expand(I_p - I_i))
    check(I_e, -e * A * Ge)  # :686
    abs_Ie = -I_e
    check(abs_Ie, e * A * Gam_e0 * sp.exp((e * (phi_p - phi_pl)) / (k_B * T_e)),
          unit=u.ampere)  # :709
    I_e0 = e * A * Gam_e0  # :687
    check(I_p / I_e0, PROBE_RETARDING.subs(u_b, e * (phi_p - phi_pl) / (k_B * T_e)))
    line = d.eq("log", sp.log(sp.Abs(sp.Symbol("I_e")) / sp.Symbol("I_e0")),
                sp.expand_log(sp.log(sp.simplify(abs_Ie / I_e0)), force=True))
    check(line, (e * (phi_p - phi_pl)) / (k_B * T_e))  # :715
    slope = d.eq("slope", sp.Symbol("S"), sp.diff(line, phi_p))
    check(slope, e / (k_B * T_e), unit=u.volt**-1)  # :721
    S = sp.symbols("S", positive=True)
    kT = d.eq("invert", k_B * T_e, sp.solve(sp.Eq(S, slope), T_e)[0] * k_B)
    check(kT, e * S ** (-1))  # :725


def test_probe_density():
    d = Derivation("Langmuir probe: density", f"{SRC}:734-743")
    I0 = sp.symbols("I_e0", positive=True)
    UNITS[I0] = u.ampere
    Ge = d.eq("Maxwellian", Gam_e0, half_space_flux(n_s, T_e, m_e))
    check(Ge, n_s * sp.sqrt((k_B * T_e) / (2 * sp.pi * m_e)))  # :738
    n_sol = d.eq("solve", n_s, sp.solve(sp.Eq(I0, e * A * Ge), n_s)[0])  # :734
    stated = I0 / (e * A * sp.sqrt((k_B * T_e) / (2 * sp.pi * m_e)))  # :742
    check(n_sol, stated, unit=u.meter**-3)


def test_probe_animation_level():
    d = Derivation("Probe animation: ion level", f"{SRC}:775")
    # Ion saturation over electron saturation, in units of e Gamma_e0 A (hydrogen).
    lvl = num(d, "Bohm / Maxwellian", sp.sqrt(2 * sp.pi * m_e / m_i),
               (2 * sp.pi * ME_CODATA / MP_CODATA) ** 0.5)
    close(lvl, 0.058, 1e-2)  # :775


def test_example_probe_numbers():
    d = Derivation("Example: probe inversion", f"{SRC}:782-791")
    slope, I0, A_ = 0.40, 4.0e-3, 1.0e-5
    Te_V = num(d, "inverse slope, V", k_B * T_e / e, 1 / slope)
    close(Te_V, 2.50, 1e-3)  # :789
    kT = Te_V * E_CODATA
    n = num(d, "density", sp.Symbol("n_e"),
             I0 / (E_CODATA * A_ * (kT / (2 * sp.pi * ME_CODATA)) ** 0.5))
    close(n, 9.44e15, 2e-3)  # :791


def plot_sheath_profile():
    """Poisson solution of the Bohm sheath (M = 1) from the wall at hydrogen floating potential."""
    import mpmath as mp
    import numpy as np

    Mv = 1  # ions enter at the Bohm speed
    eta_w = float(-sp.log(FLUX_RATIO.subs({m_e: ME_CODATA, m_i: MP_CODATA})))  # 2.84
    S = sp.lambdify(eta, SAGDEEV.subs(M, Mv), "mpmath")
    # Wall at x = 0: x(eta) = int_eta^eta_w d eta'/sqrt(2 S(eta')).
    etas = np.geomspace(eta_w, 0.02, 120)
    xs = [float(mp.quad(lambda t: 1 / mp.sqrt(2 * S(t)), [h, eta_w])) for h in etas]
    ne, ni = (sp.lambdify(eta, f.subs(M, Mv), "numpy") for f in (N_E, N_I))
    fig, ax = figure(4.2, 2.8)
    ax.plot(xs, etas, color=GRAY, ls=":")
    ax.plot(xs, ni(etas), color=ORANGE, ls="--")
    ax.plot(xs, ne(etas), color=BLUE)
    at = lambda x: np.interp(x, xs, etas)  # eta at distance x
    label(ax, 1.0, at(1.0) + 0.1, "potential $\\eta=-e\\phi/k_BT_e$", GRAY)
    label(ax, 0.3, 0.68, "ions $n_i/n_0$", ORANGE)
    label(ax, 8.0, 0.62, "electrons $n_e/n_0$", BLUE, va="top")
    ax.set(xlim=(0, 12), ylim=(0, 3), yticks=[0, 1, 2, 3],
           xlabel=r"$x/\lambda_D$ from the wall [1]", ylabel="$n/n_0$, $\\eta$ [1]")
    save(fig, "sheath-profile")


def plot_probe_iv_characteristic():
    """Planar probe current I/(e A Gamma_e0): retarding branch, flat electron saturation."""
    import numpy as np

    ratio = float(FLUX_RATIO.subs({m_e: ME_CODATA, m_i: MP_CODATA}))  # hydrogen, 0.0585
    f = sp.lambdify(u_b, PROBE_RETARDING.subs(Gam_i, ratio * Gam_e0) / 1, "numpy")
    U = np.linspace(-8, 2, 400)
    I = np.where(U <= 0, f(np.minimum(U, 0)), f(0))  # electron saturation for u > 0
    u_f = np.log(ratio)  # tested in test_floating_potential: -2.84
    fig, ax = figure(4.2, 2.8)
    ax.axhline(0, color="#333333", lw=0.6)
    ax.axvline(0, color=GRAY, lw=0.8, ls=":")
    ax.plot(U, I, color=BLUE)
    ax.plot([u_f], [0], "o", color=ORANGE, ms=4, zorder=3)
    label(ax, u_f + 0.15, 0.03, f"floating $u_f={u_f:.2f}$", ORANGE)
    label(ax, -7.9, ratio + 0.03, "ion saturation", BLUE)
    label(ax, 1.9, -0.88, "electron\nsaturation", BLUE, ha="right")
    label(ax, 0.1, -0.45, "plasma\npotential", GRAY)
    ax.set(xlim=(-8, 2), ylim=(-1.1, 0.25), yticks=[-1, -0.5, 0],
           xlabel=r"$u=e(\phi_p-\phi_{pl})/k_BT_e$ [1]", ylabel=r"$I/(eA\Gamma_{e0})$ [1]")
    save(fig, "probe-iv-characteristic")


if __name__ == "__main__":
    from si import run_as_script
    run_as_script(globals())
