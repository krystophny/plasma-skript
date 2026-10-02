"""Chapter 14, waves in hot plasmas: src/chapters/14-hot-plasma-waves.typ.

Run `python derivations/ch14_hot_plasma_waves.py` to print the steps, or
`pytest derivations` to check every chapter.

Coverage (src/chapters/14-hot-plasma-waves.typ line -> test):
  87-101 governing law eps_L, Maxwellian, v_te, lambda_D -> test_electrostatic_dielectric,
                                                          test_maxwellian_gives_Z
  123, 128   linear Vlasov response                    -> test_linear_vlasov_response
  135-149    Poisson closure, rho_1                    -> test_electrostatic_dielectric
  158, 166   Z(zeta) and Maxwellian eps_L              -> test_maxwellian_gives_Z
  171        cold limit eps_L = 1 - w_pe^2/w^2         -> test_cold_limit
  175        asymptotic Z(zeta)                        -> test_Z_asymptotic_series
  179, 499   kinetic Bohm-Gross root                   -> test_kinetic_bohm_gross
  189-203    numerical example (k lambda_D = 0.20)     -> test_example_isotropic
  282, 286   velocity marginal of Maxwellian           -> test_maxwellian_gives_Z
  292-294    v_phi = v_res = w_r/k                     -> test_example_resonance
  304, 483   weak-rate relation                        -> test_weak_rate_relation
  321, 328   first-derivative and integrated forms     -> test_integration_by_parts_forms
  341, 346   Plemelj boundary value, Im eps_L          -> test_plemelj_and_im_eps
  361-371    numerical example (k lambda_D = 0.30)     -> test_example_resonance
  461, 508   Landau damping rate                       -> test_landau_rate
  490        Im Z = sqrt(pi) exp(-zeta^2)              -> test_Z_imaginary_part
  494        Re Z asymptotic                           -> test_Z_asymptotic_series
  449-453, 525, 529  k_i = -gamma/v_g                  -> test_spatial_rate
  554-564    numerical example (gamma, v_g)            -> test_example_spatial_damping
  651        B_1 = k E_1x / w e_y                      -> test_transverse_vlasov
  660-678, 708, 734  transverse dispersion forms       -> test_transverse_ampere,
                                                          test_transverse_integration_by_parts
  687, 695   transverse Vlasov response                -> test_transverse_vlasov
  704        transverse current                        -> test_transverse_ampere
  717-726    integration-by-parts identities           -> test_transverse_integration_by_parts
  743-752    cold transverse branch                    -> test_transverse_cold_limit
  761-770, 784, 790  anisotropic quartic               -> test_anisotropic_quartic
  797, 807   roots Y_pm and growth rate                -> test_anisotropic_quartic
  818-832    numerical example (kc/w_p = 0.5)          -> test_example_anisotropic
  909        two-stream marginal                       -> test_two_stream_dispersion
  918-927, 938  two-stream D(w,k)                      -> test_two_stream_dispersion
  944-958    quartic, quadratic, roots                 -> test_two_stream_roots
  962-977    unstable band and gamma                   -> test_two_stream_roots
  982, 986   maximum growth                            -> test_two_stream_maximum
  1003-1005  animation growth exp(tau/(2 sqrt 2))      -> test_two_stream_maximum
  1012-1024  numerical example (k v0/w_p = 0.5)        -> test_example_two_stream
  1086, 1110 signed gyrofrequency                      -> test_example_magnetized
  1128-1131, 1186  Doppler-shifted resonance           -> test_harmonic_operator
  1147-1152  gyro-orbit characteristics                -> test_gyro_orbit
  1157       gyrotropic equilibrium                    -> test_gyro_orbit
  1166, 1173 harmonic operator and response            -> test_harmonic_operator
  1180-1181  circular forcing selects n = sigma        -> test_circular_forcing
  1190-1196  orbit x and Bessel (Jacobi-Anger) weights -> test_flr_bessel_weights
  1214-1232  numerical example (magnetized)            -> test_example_magnetized

Plots: plot_hot_isotropic_dispersion (exact root of EPS_L_MAXWELL against
W_BOHM_GROSS and GAMMA_LANDAU) and plot_two_stream_growth (G2_TWO_STREAM).
Not covered: the illustrative bump-on-tail figure in src/figures.typ and the
single test-particle animation ODE at lines 539-545, which is
an illustrative prescribed-wave orbit rather than a derived result.
"""

import mpmath as mp
import sympy as sp
from sympy.physics import units as u

from si import (BLUE, GRAY, ORANGE, UNITS, Derivation, c, check, e, eps0, figure,
                k_B, label, m_e, save)

I = sp.I
n0, T_e, k, v, omega, q, m, phi, E1 = sp.symbols(
    "n_0 T_e k v omega q m phi_1 E_1", positive=True
)
v_te, lam_D, w_pe, gamma, v_g, k_i = sp.symbols(
    "v_te lambda_D omega_pe gamma v_g k_i", positive=True
)
zeta, x, a = sp.symbols("zeta x a", positive=True)
Zs = sp.symbols("Z")  # value of the plasma dispersion function
UNITS.update({
    n0: u.meter**-3, T_e: u.kelvin, k: u.meter**-1, v: u.meter / u.second,
    omega: u.second**-1, q: u.coulomb, m: u.kilogram, v_te: u.meter / u.second,
    lam_D: u.meter, w_pe: u.second**-1, gamma: u.second**-1,
    v_g: u.meter / u.second, k_i: u.meter**-1,
})

# Results shared by the tests and the plots: each test proves its derivation
# equals one of these expressions, and each plot_* lambdifies the same one.
# Electron Maxwellian, a = k lambda_D, zeta = omega/(k v_te), Zs = Z(zeta).
EPS_L_MAXWELL = 1 + (1 + zeta * Zs) / a**2  # line 166
W_BOHM_GROSS = sp.sqrt(1 + 3 * a**2)  # omega_r/omega_pe, line 499
GAMMA_LANDAU = -sp.sqrt(sp.pi / 8) * a**(-3) * sp.exp(-1 / (2 * a**2) - sp.Rational(3, 2))  # 508

# CODATA 2018 values for the worked examples.
CODATA = {e: 1.602176634e-19, m_e: 9.1093837015e-31, eps0: 8.8541878128e-12,
          c: 299792458.0, k_B: 1.380649e-23}


def close(value, printed, rtol, d=None, name=None):
    """Relative agreement of a computed number with a printed one.

    With a Derivation `d`, record name = value (CODATA) in the report."""
    value = float(value)
    if d is not None:
        d.eq(f"printed {printed:.3g}", sp.Symbol(name), sp.Float(value, 4))
    assert abs(value - printed) <= rtol * abs(printed), f"{value} vs {printed}"


def plasma_freq(n):
    """Electron plasma frequency in s^-1 for density n in m^-3 (CODATA)."""
    return float(sp.sqrt(n * e**2 / (eps0 * m_e)).subs(CODATA))


def z_function(zeta_value):
    """Causal plasma dispersion function, Z = i sqrt(pi) w(zeta) (Faddeeva)."""
    z = mp.mpc(zeta_value)
    return 1j * mp.sqrt(mp.pi) * mp.exp(-z**2) * mp.erfc(-1j * z)


# ---------------------------------------------------------------------------
# Hot isotropic electrostatic dispersion
# ---------------------------------------------------------------------------
F = sp.Function("F")  # equilibrium marginal F_{s,0}(v) along k


def test_linear_vlasov_response():
    # Linearized Vlasov with d/dt -> -i w, grad -> i k, k = k e_z:
    #   -i w f1 + i k v f1 + (q/m) E1 dF/dv = 0.
    d = Derivation("Linear Vlasov response", "src/chapters/14-hot-plasma-waves.typ:128")
    f1 = sp.symbols("f1")
    vlasov = d.eq("plane wave", sp.Symbol("0"),
                  -I * omega * f1 + I * k * v * f1 + q / m * E1 * sp.diff(F(v), v))
    # src/chapters/14-hot-plasma-waves.typ:123
    stated_eq = I * (k * v - omega) * f1 + q / m * E1 * sp.diff(F(v), v)
    assert sp.simplify(vlasov - stated_eq) == 0
    derived = d.eq("solve", f1, sp.solve(vlasov, f1)[0])
    # src/chapters/14-hot-plasma-waves.typ:128
    stated = (-I * q) / m * (E1 * sp.diff(F(v), v)) / (omega - k * v)
    check(derived, stated)


def test_electrostatic_dielectric():
    # E1 = -grad(phi1) -> -i k phi1 (line 135).
    d = Derivation("Electrostatic dielectric function", "src/chapters/14-hot-plasma-waves.typ:87")
    E_es = d.eq("potential", E1, -I * k * phi)
    f1 = d.eq("response", sp.Symbol("f_1"), (-I * q) / m * (E_es * sp.diff(F(v), v)) / (omega - k * v))
    # rho1 = q * integral f1 dv; keep the integrand per unit velocity.
    rho_integrand = d.eq("charge", sp.Symbol(r"d\rho_1/dv"), q * f1)
    # src/chapters/14-hot-plasma-waves.typ:143 (integrand of rho_1)
    stated_rho = -(q**2 * phi) / m * (k * sp.diff(F(v), v)) / (omega - k * v)
    check(rho_integrand, stated_rho)
    # Poisson: div E1 = rho1/eps0 -> k^2 phi1 = rho1/eps0. Normal modes need
    # k^2 phi - rho1/eps0 = 0; dividing by k^2 phi defines eps_L.
    Ik = sp.symbols("I_k")  # integral of k F'/(w - k v)
    rho1 = -(q**2 * phi) / m * Ik
    eps_derived = d.eq("Poisson", sp.Symbol(r"\epsilon_L"),
                       sp.expand(sp.simplify((k**2 * phi - rho1 / eps0) / (k**2 * phi))))
    # src/chapters/14-hot-plasma-waves.typ:86
    stated = 1 + q**2 / (eps0 * m * k**2) * Ik
    check(eps_derived, stated)


def test_maxwellian_gives_Z():
    d = Derivation("Maxwellian dielectric and Z", "src/chapters/14-hot-plasma-waves.typ:166")
    vx, vy, vz = sp.symbols("v_x v_y v_z", real=True)
    # src/chapters/14-hot-plasma-waves.typ:96
    f0 = n0 / (sp.pi**sp.Rational(3, 2) * v_te**3) * sp.exp(-(vx**2 + vy**2 + vz**2) / v_te**2)
    # Integrate out perpendicular velocities to get the marginal.
    marg = d.eq("marginal", sp.Symbol("F_{e,0}"),
                sp.integrate(f0, (vx, -sp.oo, sp.oo), (vy, -sp.oo, sp.oo)))
    # src/chapters/14-hot-plasma-waves.typ:286
    stated_marg = (n0 / (sp.sqrt(sp.pi) * v_te)) * sp.exp(-vz**2 / v_te**2)
    check(marg, stated_marg)
    assert sp.simplify(sp.integrate(marg, (vz, -sp.oo, sp.oo)) - n0) == 0
    # Integrand k F'/(w - k v) with v = v_te x, w = k v_te zeta, dv = v_te dx.
    integrand = (k * sp.diff(marg, vz) / (omega - k * vz)).subs(
        {vz: v_te * x, omega: k * v_te * zeta}) * v_te
    # Split x/(x - zeta) = 1 + zeta/(x - zeta): the pole part defines Z.
    parts = sp.apart(sp.simplify(integrand * sp.exp(x**2)), x)
    d.step("partial fractions", sp.Eq(sp.Symbol(r"e^{x^2} k F'/(\omega-kv)\,dv/dx"), parts))
    regular = sum(t for t in sp.Add.make_args(parts) if not t.has(1 / (x - zeta)))
    pole_coeff = sp.simplify((parts - regular) * (x - zeta))
    integral = sp.integrate(regular * sp.exp(-x**2), (x, -sp.oo, sp.oo)) \
        + pole_coeff * sp.sqrt(sp.pi) * Zs  # Z = (1/sqrt pi) int e^{-x^2}/(x-zeta)
    # Electron Maxwellian: q = -e, m = m_e, v_te^2 = 2 k_B T_e/m_e.
    eps_L = 1 + e**2 / (eps0 * m_e * k**2) * integral
    eps_L = eps_L.subs(v_te, sp.sqrt(2 * k_B * T_e / m_e))
    d.eq("Maxwellian", sp.Symbol(r"\epsilon_L"), 1 + sp.factor(sp.simplify(
        (eps_L - 1).subs(T_e, lam_D**2 * n0 * e**2 / (eps0 * k_B)))))
    lamD2 = eps0 * k_B * T_e / (n0 * e**2)  # line 101
    # src/chapters/14-hot-plasma-waves.typ:166
    stated = 1 + 1 / (k**2 * lamD2) * (1 + zeta * Zs)
    check(eps_L, stated)
    check(stated.subs(k, a / sp.sqrt(lamD2)), EPS_L_MAXWELL)
    # The dimension of lambda_D^2 (line 101) is m^2.
    check(sp.sqrt(lamD2), sp.sqrt(eps0 * k_B * T_e / (n0 * e**2)), unit=u.meter)


def test_cold_limit():
    # Integrated form with a cold marginal F = n0 delta(v), electrons.
    w = sp.symbols("v", real=True)
    F_cold = n0 * sp.DiracDelta(w)
    d = Derivation("Cold limit", "src/chapters/14-hot-plasma-waves.typ:171")
    integral = d.eq("delta", sp.Integral(F(w) / (w - omega / k)**2, (w, -sp.oo, sp.oo)),
                    sp.integrate(F_cold / (w - omega / k)**2, (w, -sp.oo, sp.oo)))
    derived = d.eq("cold", sp.Symbol(r"\epsilon_L"), 1 - e**2 / (eps0 * m_e * k**2) * integral)
    w_p2 = n0 * e**2 / (eps0 * m_e)
    # src/chapters/14-hot-plasma-waves.typ:171
    stated = 1 - w_p2 / omega**2
    check(derived, stated)


def test_Z_imaginary_part():
    # Plemelj: int g/(x - zeta - i0) = PV + i pi g(zeta); g = e^{-x^2}/sqrt(pi).
    d = Derivation("Imaginary part of Z", "src/chapters/14-hot-plasma-waves.typ:490")
    g = sp.exp(-x**2) / sp.sqrt(sp.pi)
    derived = d.eq("Plemelj", sp.Symbol(r"\mathrm{Im}\,Z"), sp.pi * g.subs(x, zeta))
    # src/chapters/14-hot-plasma-waves.typ:490
    stated = sp.sqrt(sp.pi) * sp.exp(-zeta**2)
    check(derived, stated)
    # Independent check against the Faddeeva closed form of Z.
    for zr in (0.5, 1.7, 3.0):
        close(mp.im(z_function(zr)), float(stated.subs(zeta, zr)), 1e-12)


def test_Z_asymptotic_series():
    # For |zeta| >> 1 expand 1/(x - zeta) = -(1/zeta) sum (x/zeta)^n and use
    # the Gaussian moments (1/sqrt pi) int x^n e^{-x^2} dx.
    d = Derivation("Asymptotic Z", "src/chapters/14-hot-plasma-waves.typ:175")
    N = 6
    series = -sum(
        sp.integrate(x**n * sp.exp(-x**2), (x, -sp.oo, sp.oo)) / sp.sqrt(sp.pi)
        / zeta**(n + 1) for n in range(N))
    d.eq("moments", sp.Symbol("Z"), series)
    # src/chapters/14-hot-plasma-waves.typ:175 (and :494 to two terms)
    stated = -1 / zeta - 1 / (2 * zeta**3) - 3 / (4 * zeta**5)
    check(series, stated)
    # Numerical check against the exact Re Z at zeta = 8.
    close(mp.re(z_function(8.0)), float(stated.subs(zeta, 8)), 2e-5)


def test_kinetic_bohm_gross():
    # eps_L = 1 + (1 + zeta Z)/(k lambda_D)^2 = 0 with the asymptotic Z.
    Z_asym = -1 / zeta - 1 / (2 * zeta**3) - 3 / (4 * zeta**5)
    vte = sp.sqrt(2 * k_B * T_e / m_e)
    lamD2 = eps0 * k_B * T_e / (n0 * e**2)
    d = Derivation("Kinetic Bohm-Gross root", "src/chapters/14-hot-plasma-waves.typ:179")
    W, small = sp.symbols("W varepsilon", positive=True)  # W = omega^2
    eps_L = d.eq("asymptotic Z", sp.Symbol(r"\epsilon_L"), 1 + (1 + zeta * Z_asym) / (k**2 * lamD2))
    eps_L = sp.expand(eps_L.subs(zeta, sp.sqrt(W) / (k * vte)))
    # Keep terms up to O(k^2) relative to the leading one: drop zeta^-6 terms.
    eps_L = sum(t for t in sp.Add.make_args(eps_L) if sp.degree(t.as_numer_denom()[1], W) <= 2)
    # Clear denominators: quadratic in W; take the root continuous with w_pe.
    poly = d.eq("truncate", sp.Symbol("0"), sp.numer(sp.together(eps_L)))
    roots = sp.solve(poly, W)
    root = [r for r in roots if sp.limit(r.subs(k, 0), k, 0) != 0][0]
    derived = d.eq("series", omega**2,
                   sp.series(root.subs(k, small * k), small, 0, 3).removeO().subs(small, 1))
    w_p2 = n0 * e**2 / (eps0 * m_e)
    # src/chapters/14-hot-plasma-waves.typ:179
    stated = w_p2 + (3 * k**2 * k_B * T_e) / m_e
    check(derived, stated, unit=u.second**-2)
    # src/chapters/14-hot-plasma-waves.typ:499
    stated_499 = w_p2 * (1 + 3 * (k * sp.sqrt(lamD2))**2)
    check(derived, stated_499)
    check(stated_499.subs(k, a / sp.sqrt(lamD2)) / w_p2, W_BOHM_GROSS**2)


def test_integration_by_parts_forms():
    d = Derivation("First-derivative and integrated forms", "src/chapters/14-hot-plasma-waves.typ:328")
    a_ = sp.symbols("a")  # a = omega/k
    # k F'/(w - k v) = -F'/(v - w/k): the first-derivative form of line 87.
    lhs = d.eq("rewrite", k * sp.diff(F(v), v) / (omega - k * v),
               sp.factor(k * sp.diff(F(v), v) / (omega - k * v)))
    # src/chapters/14-hot-plasma-waves.typ:321 (integrand with the sign of eps_L)
    stated_321 = -sp.diff(F(v), v) / (v - omega / k)
    check(lhs, stated_321)
    # F'/(v-a) = d/dv[F/(v-a)] + F/(v-a)^2, and the boundary term vanishes.
    total = d.eq("by parts", sp.Derivative(F(v) / (v - a_), v), sp.diff(F(v) / (v - a_), v))
    assert sp.simplify(sp.diff(F(v), v) / (v - a_) - total - F(v) / (v - a_)**2) == 0
    # Numerical check with a Gaussian marginal and complex a (Im a > 0).
    a_num = mp.mpc(0.7, 0.4)
    Fg = lambda t: mp.exp(-t**2)
    dFg = lambda t: -2 * t * mp.exp(-t**2)
    left = mp.quad(lambda t: dFg(t) / (t - a_num), [-mp.inf, 0, mp.inf])
    # src/chapters/14-hot-plasma-waves.typ:328 (integral of F/(v - w/k)^2)
    right = mp.quad(lambda t: Fg(t) / (t - a_num)**2, [-mp.inf, 0, mp.inf])
    assert abs(left - right) < 1e-10


def test_plemelj_and_im_eps():
    # Boundary value: int g/(v - v_res - i eta) -> PV + i pi g(v_res), eta -> 0+.
    g = lambda t: mp.exp(-(t - 0.3)**2)
    vres, eta = 0.8, 1e-6
    val = mp.quad(lambda t: g(t) / (t - vres - 1j * eta), [-mp.inf, vres - 1, vres, vres + 1, mp.inf])
    # src/chapters/14-hot-plasma-waves.typ:341
    close(mp.im(val), float(mp.pi * g(vres)), 1e-4)
    # Im of the first-derivative form, one species, slope F'(v_res) = S.
    d = Derivation("Resonant imaginary part", "src/chapters/14-hot-plasma-waves.typ:346")
    S = sp.symbols("S", real=True)  # S = F'(v_res)
    C = q**2 / (eps0 * m * k**2)
    PV = sp.symbols("PV", real=True)
    eps_L = d.eq("Plemelj", sp.Symbol(r"\epsilon_L"), 1 - C * (PV + I * sp.pi * S))
    derived = d.eq("imaginary part", sp.Symbol(r"\mathrm{Im}\,\epsilon_L"), sp.im(eps_L))
    # src/chapters/14-hot-plasma-waves.typ:346
    stated = -(sp.pi * q**2) / (eps0 * m * k**2) * S
    check(derived, stated)


def test_weak_rate_relation():
    # eps(w_r + i gamma) ~ eps_r + i eps_i + i gamma d(eps_r)/dw; eps_i is small
    # so gamma d(eps_i)/dw is second order and dropped.
    er, ei = sp.symbols("epsilon_r epsilon_i", real=True)
    der = sp.Symbol(r"\partial_\omega \epsilon_r", real=True)
    d = Derivation("Weak-rate relation", "src/chapters/14-hot-plasma-waves.typ:483")
    g_ = sp.symbols("gamma", real=True)
    expansion = d.eq("Taylor", sp.Function(r"\epsilon_L")(sp.Symbol(r"\omega_r") + I * g_), er + I * ei + I * g_ * der)
    # src/chapters/14-hot-plasma-waves.typ:478
    assert sp.simplify(expansion - (er + I * ei + I * g_ * der)) == 0
    re_part, im_part = sp.re(expansion), sp.im(expansion)
    assert re_part == er  # real part: eps_r(w_r) = 0 (line 483)
    derived = d.eq("imaginary part", g_, sp.solve(im_part, g_)[0])
    # src/chapters/14-hot-plasma-waves.typ:483 (and governing law at :304)
    stated = -ei / der
    check(derived, stated)


def test_landau_rate():
    d = Derivation("Landau damping rate", "src/chapters/14-hot-plasma-waves.typ:508")
    # v_te = sqrt(2) w_pe lambda_D (line 367), so k v_te = sqrt(2) a w_pe.
    vte = sp.sqrt(2 * k_B * T_e / m_e)
    wpe = sp.sqrt(n0 * e**2 / (eps0 * m_e))
    lamD = sp.sqrt(eps0 * k_B * T_e / (n0 * e**2))
    check(sp.sqrt(2) * wpe * lamD, vte, unit=u.meter / u.second)
    w = sp.symbols("omega", positive=True)
    zeta_w = w / (sp.sqrt(2) * a * w_pe)
    # Real part with the asymptotic Re Z; imaginary part from Im Z.
    ReZ = -1 / zeta - 1 / (2 * zeta**3) - 3 / (4 * zeta**5)
    eps_r = 1 + (1 + zeta * ReZ) / a**2
    eps_i = zeta * sp.sqrt(sp.pi) * sp.exp(-zeta**2) / a**2
    # src/chapters/14-hot-plasma-waves.typ:506 (epsilon_i)
    check(eps_i, (sp.sqrt(sp.pi) * zeta * sp.exp(-zeta**2)) / a**2)
    # d eps_r / d w at w = w_pe, leading order as a -> 0.
    der = sp.diff(eps_r.subs(zeta, zeta_w), w).subs(w, w_pe)
    der0 = d.eq("leading order", sp.Derivative(sp.Symbol(r"\epsilon_r"), w), sp.limit(der, a, 0))
    check(der0, 2 / w_pe)  # line 503
    # Real root w_r^2 = w_pe^2 (1 + 3 a^2): exponent zeta^2 = 1/(2a^2) + 3/2.
    zeta2 = d.eq("root", zeta**2, sp.expand((w_pe**2 * (1 + 3 * a**2)) / (2 * a**2 * w_pe**2)))
    check(zeta2, 1 / (2 * a**2) + sp.Rational(3, 2))
    # Prefactor uses zeta ~ 1/(sqrt 2 a); weak-rate relation gamma = -eps_i/der.
    pref = (sp.sqrt(sp.pi) * zeta / a**2).subs(zeta, 1 / (sp.sqrt(2) * a))
    derived = d.eq("weak rate", gamma / w_pe, -pref * sp.exp(-zeta2) / der0 / w_pe)
    # src/chapters/14-hot-plasma-waves.typ:508
    stated = GAMMA_LANDAU
    check(derived, stated)
    # src/chapters/14-hot-plasma-waves.typ:462 (governing-law form)
    stated_462 = -sp.sqrt(sp.pi / 8) * w_pe * sp.exp(-sp.Rational(3, 2)) * a**(-3) \
        * sp.exp(-1 / (2 * a**2))
    check(derived * w_pe, stated_462)
    # Sanity: compare with the exact complex root at a = 0.2 (within ~25%).
    root = kinetic_root(0.2, mp.mpc(mp.sqrt(1 + 3 * 0.2**2), -0.001))
    close(mp.im(root), float(stated.subs(a, 0.2)), 0.25)


def kinetic_root(a_value, guess):
    """Complex root W = omega/omega_pe of EPS_L_MAXWELL = 0 at k lambda_D = a."""
    eps = sp.lambdify((zeta, Zs, a), EPS_L_MAXWELL, "mpmath")
    aa = mp.mpf(a_value)

    def f(W):
        z = W / (mp.sqrt(2) * aa)  # zeta = omega/(k v_te), v_te = sqrt(2) omega_pe lambda_D
        return eps(z, z_function(z), aa)

    return mp.findroot(f, guess)


def test_spatial_rate():
    # omega(k_r + i k_i) ~ omega_r + i gamma + i k_i v_g; demand real omega.
    g_, ki_ = sp.symbols("gamma k_i", real=True)
    w_r = sp.symbols("omega_r", positive=True)
    d = Derivation("Spatial damping rate", "src/chapters/14-hot-plasma-waves.typ:529")
    expansion = d.eq("Taylor", sp.Function(r"\omega")(sp.Symbol("k_r") + I * ki_), w_r + I * g_ + I * ki_ * v_g)
    derived = d.eq("real omega", ki_, sp.solve(sp.im(expansion), ki_)[0])
    # src/chapters/14-hot-plasma-waves.typ:529
    stated = -g_ / v_g
    check(derived, stated)
    # src/chapters/14-hot-plasma-waves.typ:529, unit m^-1
    check(derived.subs(g_, gamma), -gamma / v_g, unit=u.meter**-1,
          units={gamma: u.second**-1})  # gamma is shared with ch13's adiabatic index


# ---------------------------------------------------------------------------
# Worked numerical examples, unmagnetized electrostatic
# ---------------------------------------------------------------------------
def test_example_isotropic():
    d = Derivation("Example: warm Langmuir root", "src/chapters/14-hot-plasma-waves.typ:200")
    # n0 = 1e16 m^-3, k_B T_e = 10 eV; CODATA constants.
    kT = 10 * CODATA[e]
    lamD = float(sp.sqrt(eps0 * kT / (n0 * e**2)).subs({**CODATA, n0: 1e16}))
    close(lamD, 2.35e-4, 3e-3,
          d=d, name=r"\lambda_D")  # line 200
    close(0.20 / lamD, 851, 3e-3,
          d=d, name=r"k")  # line 201
    wpe = plasma_freq(1e16)
    ratio = (1 + 3 * 0.20**2) ** 0.5
    close(ratio, 1.06, 5e-3,
          d=d, name=r"\omega_r/\omega_{pe}")  # line 202
    close(ratio * wpe, 5.97e9, 3e-3,
          d=d, name=r"\omega_r")  # line 203


def test_example_resonance():
    d = Derivation("Example: resonant velocity", "src/chapters/14-hot-plasma-waves.typ:369")
    wpe = plasma_freq(1e16)
    close(wpe, 5.64e9, 1e-3,
          d=d, name=r"\omega_{pe}")  # line 364
    ratio = (1 + 3 * 0.30**2) ** 0.5
    close(ratio, 1.13, 5e-3,
          d=d, name=r"\omega_r/\omega_{pe}")  # line 370
    # v_res = v_phi = w_r/k and v_te = sqrt(2) w_pe lambda_D (lines 292, 367).
    close(ratio / (0.30 * 2**0.5), 2.66, 3e-3,
          d=d, name=r"v_{res}/v_{te}")  # line 371


def test_example_spatial_damping():
    d = Derivation("Example: spatial damping", "src/chapters/14-hot-plasma-waves.typ:562")
    g_, vg = -1.13e8, 1.00e6
    ki = -g_ / vg
    close(ki, 113, 1e-3,
          d=d, name=r"k_i")  # line 562
    close(1 / ki, 8.85e-3, 1e-3,
          d=d, name=r"L_{amp}")  # line 563
    close(1 / abs(g_), 8.85e-9, 1e-3,
          d=d, name=r"\tau_d")  # line 564


# ---------------------------------------------------------------------------
# Transverse kinetic waves
# ---------------------------------------------------------------------------
vx, vy, vz = sp.symbols("v_x v_y v_z", real=True)
class _F0(sp.Function):
    """Equilibrium f_0(v_x, v_y, v_z), printed without its arguments."""

    def _latex(self, printer, exp=None):
        return "f_0" if exp is None else "f_0^{%s}" % exp


f0 = _F0(vx, vy, vz)


class _Quiet:
    """Stand-in for Derivation when a helper is reused without recording."""

    def step(self, label, expr):
        return expr

    def eq(self, label, lhs, rhs):
        return rhs


def transverse_f1(record=True):
    """Linear Vlasov response to E = E1 e_x, k = k e_z (exp(i(kz - wt)))."""
    d = Derivation("Transverse Vlasov response", "src/chapters/14-hot-plasma-waves.typ:695") \
        if record else _Quiet()
    # Faraday: k x E1 = w B1.
    Evec = sp.Matrix([E1, 0, 0])
    kvec = sp.Matrix([0, 0, k])
    B1 = d.eq("Faraday", sp.Symbol(r"\mathbf{B}_1"), kvec.cross(Evec) / omega)
    vvec = sp.Matrix([vx, vy, vz])
    force = d.eq("Lorentz", sp.Symbol(r"\mathbf{F}/q_s"), Evec + vvec.cross(B1))
    grad_v = sp.Matrix([sp.diff(f0, s) for s in (vx, vy, vz)])
    f1 = sp.symbols("f_1")
    vlasov = d.eq("Vlasov", sp.Symbol("0"),
                  -I * (omega - k * vz) * f1 + q / m * force.dot(grad_v))
    sol = d.eq("solve", f1, sp.solve(vlasov, f1)[0])
    return B1, vlasov, sol, f1


def test_transverse_vlasov():
    B1, vlasov, sol, f1 = transverse_f1()
    # src/chapters/14-hot-plasma-waves.typ:651
    check(B1[1], k / omega * E1)
    assert B1[0] == 0 and B1[2] == 0
    # src/chapters/14-hot-plasma-waves.typ:687
    stated_eq = -I * (omega - k * vz) * f1 + (q / m) * E1 * (
        (1 - (k * vz) / omega) * sp.diff(f0, vx) + (k * vx) / omega * sp.diff(f0, vz))
    check(vlasov, stated_eq)
    # src/chapters/14-hot-plasma-waves.typ:695
    stated = (-I * q * E1) / (m * omega) * (
        (omega - k * vz) * sp.diff(f0, vx) + k * vx * sp.diff(f0, vz)) / (omega - k * vz)
    check(sol, stated)


def test_transverse_ampere():
    _, _, f1, _ = transverse_f1(record=False)
    d = Derivation("Transverse Ampere law", "src/chapters/14-hot-plasma-waves.typ:708")
    # Ampere + Faraday for E along x: (w^2 - k^2 c^2) E1 = -i w J1/eps0.
    J = sp.symbols("J_1")
    disp = d.eq("Ampere", k**2 * c**2, omega**2 + I * omega * J / (eps0 * E1))
    # J1 = q int v_x f1 d^3v (line 704); record the integrand per species.
    integrand = d.eq("current", k**2 * c**2 - omega**2, sp.simplify(
        (disp - omega**2).subs(J, q * vx * f1)))
    # src/chapters/14-hot-plasma-waves.typ:708 (integrand of the species sum)
    stated = q**2 / (eps0 * m) * (vx * sp.diff(f0, vx)
                                  + (k * vx**2) / (omega - k * vz) * sp.diff(f0, vz))
    check(integrand, stated)
    # Check the Ampere step from the curl equations with sympy vectors.
    Ev = sp.Matrix([E1, 0, 0])
    kv = sp.Matrix([0, 0, k])
    B = kv.cross(Ev) / omega
    Jv = sp.Matrix([J, 0, 0])
    # i k x B = mu0 J - i w E/c^2, with mu0 = 1/(eps0 c^2).
    resid = I * kv.cross(B) - (Jv / (eps0 * c**2) - I * omega * Ev / c**2)
    sol = sp.solve(resid[0], J)[0]
    check(sp.solve(sp.Eq(k**2 * c**2, disp), J)[0], sol)


def test_transverse_integration_by_parts():
    d = Derivation("Transverse integration by parts", "src/chapters/14-hot-plasma-waves.typ:734")
    # src/chapters/14-hot-plasma-waves.typ:717
    derived = d.eq("pole", sp.Derivative(1 / (omega - k * vz), vz), sp.diff(1 / (omega - k * vz), vz))
    check(derived, k / (omega - k * vz)**2)
    # Identity 1 (line 722), checked for an anisotropic Gaussian of density n.
    ax, ay, az = sp.symbols("a_x a_y a_z", positive=True)
    fg = n0 / (sp.pi**sp.Rational(3, 2) * ax * ay * az) * sp.exp(
        -vx**2 / ax**2 - vy**2 / ay**2 - vz**2 / az**2)
    lhs = sp.integrate(vx * sp.diff(fg, vx), (vx, -sp.oo, sp.oo), (vy, -sp.oo, sp.oo),
                       (vz, -sp.oo, sp.oo))
    check(d.eq("by parts", sp.Symbol(r"\int v_x \partial_{v_x} f_0"), lhs), -n0)
    # Identity 2 (line 726): the integrands differ by a total v_z derivative.
    left = k * vx**2 / (omega - k * vz) * sp.diff(f0, vz)
    right = -(k**2 * vx**2 * f0) / (omega - k * vz)**2
    total = sp.diff(k * vx**2 * f0 / (omega - k * vz), vz)
    assert sp.simplify(left - right - total) == 0
    # Assemble the integrated law (line 734) from line 708 with both identities.
    wps2 = n0 * q**2 / (eps0 * m)
    Ires = sp.symbols("I_res")  # integral of v_x^2 f0/(w - k v_z)^2
    derived = d.eq("assemble", k**2 * c**2,
                   omega**2 + q**2 / (eps0 * m) * (-n0 - k**2 * Ires))
    # src/chapters/14-hot-plasma-waves.typ:734
    stated = omega**2 - wps2 - (q**2 * k**2) / (eps0 * m) * Ires
    check(derived, stated)


def test_transverse_cold_limit():
    d = Derivation("Cold transverse branch", "src/chapters/14-hot-plasma-waves.typ:752")
    # src/chapters/14-hot-plasma-waves.typ:743
    fc = n0 * sp.DiracDelta(vx) * sp.DiracDelta(vy) * sp.DiracDelta(vz)
    Ires = sp.integrate(vx**2 * fc / (omega - k * vz)**2,
                        (vx, -sp.oo, sp.oo), (vy, -sp.oo, sp.oo), (vz, -sp.oo, sp.oo))
    d.eq("cold", sp.Symbol(r"I_{\rm res}"), Ires)
    w_p2 = sp.Symbol("omega_p", positive=True)**2
    k2c2 = d.eq("dispersion", k**2 * c**2,
                omega**2 - w_p2 - q**2 * k**2 / (eps0 * m) * Ires)
    # src/chapters/14-hot-plasma-waves.typ:748
    check(k2c2, omega**2 - w_p2)
    W = sp.solve(sp.Eq(k**2 * c**2, k2c2), omega**2)[0]
    # src/chapters/14-hot-plasma-waves.typ:752
    check(W, k**2 * c**2 + w_p2)


def test_anisotropic_quartic():
    d = Derivation("Anisotropic transverse instability", "src/chapters/14-hot-plasma-waves.typ:767")
    Fp = sp.Function("F")(vx, vy)
    vx2 = sp.symbols(r"\langle{v_x^2}\rangle", positive=True)
    UNITS[vx2] = u.meter**2 / u.second**2
    # Equilibrium delta(v_z) F(v_x, v_y): do the v_z integral first.
    inner = sp.integrate(vx**2 * sp.DiracDelta(vz) * Fp / (omega - k * vz)**2, (vz, -sp.oo, sp.oo))
    d.eq("delta", sp.Symbol(r"\int dv_z"), inner)
    # The remaining moment is n0 <v_x^2> by definition (line 764).
    Ires = sp.simplify(inner / (vx**2 * Fp)) * n0 * vx2
    # src/chapters/14-hot-plasma-waves.typ:784
    check(Ires, n0 * vx2 / omega**2)
    wp2 = n0 * e**2 / (eps0 * m_e)  # line 790
    rhs = omega**2 - wp2 - e**2 * k**2 / (eps0 * m_e) * Ires
    wp_ = sp.Symbol("omega_p", positive=True)
    to_wp = {n0: wp_**2 * eps0 * m_e / e**2}
    d.eq("dispersion", k**2 * c**2, sp.expand(rhs.subs(to_wp)))
    # src/chapters/14-hot-plasma-waves.typ:767
    check(rhs, omega**2 - wp2 * (1 + (k**2 * vx2) / omega**2))
    quartic = sp.expand((rhs - k**2 * c**2) * omega**2)
    d.eq("quartic", sp.Symbol("0"), sp.collect(sp.expand(quartic.subs(to_wp)), omega))
    # src/chapters/14-hot-plasma-waves.typ:769
    check(quartic, omega**4 - (k**2 * c**2 + wp2) * omega**2 - k**2 * wp2 * vx2)
    Y = sp.symbols("Y")
    roots = sp.solve(quartic.subs(omega, sp.sqrt(Y)), Y)
    root_sum = (k**2 * c**2 + wp2)
    root_disc = sp.sqrt((k**2 * c**2 + wp2)**2 + 4 * k**2 * wp2 * vx2)
    # src/chapters/14-hot-plasma-waves.typ:797
    stated = {(root_sum + root_disc) / 2, (root_sum - root_disc) / 2}
    for r in roots:
        assert any(sp.simplify(r - s) == 0 for s in stated)
    # Lower root negative: disc^2 - sum^2 = 4 k^2 w_p^2 <v_x^2> > 0.
    assert sp.simplify(root_disc**2 - root_sum**2 - 4 * k**2 * wp2 * vx2) == 0
    # omega = i gamma -> gamma^2 = -Y_-.
    g2 = -(root_sum - root_disc) / 2
    d.eq("growth", gamma**2, g2.subs(to_wp))
    # src/chapters/14-hot-plasma-waves.typ:807
    check(g2, (root_disc - (k**2 * c**2 + wp2)) / 2, unit=u.second**-2)


def test_example_anisotropic():
    d = Derivation("Example: anisotropic growth", "src/chapters/14-hot-plasma-waves.typ:828")
    wp = plasma_freq(1e16)
    close(wp, 5.64e9, 1e-3,
          d=d, name=r"\omega_p")  # line 828
    kk = 0.50 * wp / CODATA[c]
    close(kk, 9.41, 1e-3,
          d=d, name=r"k")  # line 829
    close(2 * float(sp.pi) / kk, 0.668, 2e-3,
          d=d, name=r"\lambda")  # line 830
    # Normalized quartic with k^2 c^2 = 0.25, <v_x^2> k^2/w_p^2 = 0.25*0.01.
    s, d4 = 0.25 + 1, 4 * 0.25 * 1.00e-2
    g = (((s**2 + d4) ** 0.5 - s) / 2) ** 0.5
    close(g, 4.47e-2, 1e-3,
          d=d, name=r"\gamma/\omega_p")  # line 831
    close(g * wp, 2.52e8, 2e-3,
          d=d, name=r"\gamma")  # line 832


# ---------------------------------------------------------------------------
# Two-stream instability
# ---------------------------------------------------------------------------
xx, yy = sp.symbols("x y", positive=True)
v0, w_p = sp.symbols("v_0 omega_p", positive=True)
UNITS.update({v0: u.meter / u.second, w_p: u.second**-1})
G2_TWO_STREAM = sp.sqrt(1 + 8 * xx) / 2 - xx - sp.Rational(1, 2)  # (gamma/w_p)^2, line 977


def test_two_stream_dispersion():
    d = Derivation("Two-stream dispersion", "src/chapters/14-hot-plasma-waves.typ:938")
    w = sp.symbols("v", real=True)
    # src/chapters/14-hot-plasma-waves.typ:909
    Fb = n0 / 2 * (sp.DiracDelta(w - v0) + sp.DiracDelta(w + v0))
    assert sp.simplify(sp.integrate(Fb, (w, -sp.oo, sp.oo)) - n0) == 0
    # Integrated form: eps = 1 - e^2/(eps0 m k^2) int F/(v - w/k)^2 dv.
    integral = sp.integrate(Fb / (w - omega / k)**2, (w, -sp.oo, sp.oo))
    D = (1 - e**2 / (eps0 * m_e * k**2) * integral).subs(n0, w_p**2 * eps0 * m_e / e**2)
    d.eq("integrated form", sp.Symbol("D"), sp.apart(sp.simplify(D), omega))
    # src/chapters/14-hot-plasma-waves.typ:938 (and :920)
    stated = 1 - w_p**2 / (2 * (omega - k * v0)**2) - w_p**2 / (2 * (omega + k * v0)**2)
    check(D, stated)


def test_two_stream_roots():
    d = Derivation("Two-stream roots", "src/chapters/14-hot-plasma-waves.typ:958")
    D = 1 - w_p**2 / (2 * (omega - k * v0)**2) - w_p**2 / (2 * (omega + k * v0)**2)
    quartic = d.step("clear", sp.expand(sp.simplify(D * (omega**2 - k**2 * v0**2)**2)))
    # src/chapters/14-hot-plasma-waves.typ:944
    stated = omega**4 - (2 * k**2 * v0**2 + w_p**2) * omega**2 \
        + k**2 * v0**2 * (k**2 * v0**2 - w_p**2)
    check(quartic, stated)
    # x = k^2 v0^2/w_p^2, y = w^2/w_p^2 (line 949).
    quad = d.step("normalize", sp.expand((quartic / w_p**4).subs(
        {omega: w_p * sp.sqrt(yy), v0: w_p * sp.sqrt(xx) / k})))
    # src/chapters/14-hot-plasma-waves.typ:954
    check(quad, yy**2 - (2 * xx + 1) * yy + xx * (xx - 1))
    roots = sp.solve(quad, yy)
    # src/chapters/14-hot-plasma-waves.typ:958 (and :923)
    stated_roots = {xx + sp.Rational(1, 2) + sp.sqrt(1 + 8 * xx) / 2,
                    xx + sp.Rational(1, 2) - sp.sqrt(1 + 8 * xx) / 2}
    for r in roots:
        assert any(sp.simplify(r - s) == 0 for s in stated_roots)
    y_minus = xx + sp.Rational(1, 2) - sp.sqrt(1 + 8 * xx) / 2
    # y_- < 0  <=>  sqrt(1+8x) > 1 + 2x  <=>  1+8x > (1+2x)^2 (lines 964, 968).
    check(sp.expand((1 + 2 * xx)**2), 1 + 4 * xx + 4 * xx**2)
    band = sp.solve_univariate_inequality(1 + 8 * xx > 1 + 4 * xx + 4 * xx**2, xx,
                                          relational=False)
    assert band == sp.Interval.open(0, 1)
    # omega = i gamma -> gamma^2/w_p^2 = -y_- (lines 972, 977, 925).
    g2 = d.eq("i gamma", gamma**2 / w_p**2, -y_minus)
    check(g2, G2_TWO_STREAM)


def test_two_stream_maximum():
    d = Derivation("Maximum two-stream growth", "src/chapters/14-hot-plasma-waves.typ:986")
    g2 = G2_TWO_STREAM
    xs = sp.solve(sp.diff(g2, xx), xx)
    d.eq("extremum", xx, xs[0])
    assert xs == [sp.Rational(3, 8)]  # line 979
    g2max = d.eq("max", gamma**2 / w_p**2, g2.subs(xx, xs[0]))
    # src/chapters/14-hot-plasma-waves.typ:982
    check(g2max, sp.Rational(1, 8))
    # src/chapters/14-hot-plasma-waves.typ:986 (animation at :1005 uses the same)
    check(sp.sqrt(g2max), 1 / (2 * sp.sqrt(2)))
    # Animation wave number K = sqrt(3/8) (line 1004) is sqrt(x_max).
    check(sp.sqrt(xs[0]), sp.sqrt(sp.Rational(3, 8)))


def test_example_two_stream():
    d = Derivation("Example: two-stream growth", "src/chapters/14-hot-plasma-waves.typ:1020")
    wp = plasma_freq(1e16)
    close(wp, 5.64e9, 1e-3,
          d=d, name=r"\omega_p")  # line 1020
    kk = 0.50 * wp / (0.10 * CODATA[c])
    close(kk, 94.1, 1e-3,
          d=d, name=r"k")  # line 1021
    close(2 * float(sp.pi) / kk, 6.68e-2, 2e-3,
          d=d, name=r"\lambda")  # line 1022
    g = (3 ** 0.5 / 2 - 0.25 - 0.5) ** 0.5           # x = 0.25
    close(g, 0.341, 2e-3,
          d=d, name=r"\gamma/\omega_p")  # line 1023
    close(g * wp, 1.92e9, 2e-3,
          d=d, name=r"\gamma")  # line 1024


# ---------------------------------------------------------------------------
# Hot magnetized waves
# ---------------------------------------------------------------------------
t, B0, vperp, vpar, Om, kpar = sp.symbols(
    r"t B_0 v_\perp v_\parallel Omega_s k_\parallel", real=True)
theta = sp.Function("theta")(t)


def test_gyro_orbit():
    d = Derivation("Gyro-orbit characteristics", "src/chapters/14-hot-plasma-waves.typ:1147")
    Omega = q * B0 / m  # signed gyrofrequency, line 1110
    check(Omega, q * B0 / m, unit=u.second**-1, units={B0: u.tesla})
    vvec = sp.Matrix([vperp * sp.cos(theta), -vperp * sp.sin(theta), vpar])
    # Characteristics with dtheta/dt = Omega_s (line 1149).
    dvdt = d.eq("orbit", sp.Symbol(r"\dot{\mathbf{v}}"),
                vvec.diff(t).subs(sp.Derivative(theta, t), Omega))
    lorentz = d.eq("Lorentz", sp.Symbol(r"\dot{\mathbf{v}}"),
                   q / m * vvec.cross(sp.Matrix([0, 0, B0])))
    assert sp.simplify(dvdt - lorentz) == sp.zeros(3, 1)
    # src/chapters/14-hot-plasma-waves.typ:1151-1152
    check(dvdt[0], Omega * vvec[1])
    check(dvdt[1], -Omega * vvec[0])
    # A function of v_parallel and |v_perp| is constant along the orbit (line 1157).
    g = sp.Function("g")
    f_gyro = g(vvec[2], sp.sqrt(vvec[0]**2 + vvec[1]**2))
    assert sp.simplify(sp.diff(f_gyro, t)) == 0


def test_harmonic_operator():
    d = Derivation("Gyroangle harmonic response", "src/chapters/14-hot-plasma-waves.typ:1173")
    z, th, n = sp.symbols("z theta n", real=True)
    harmonic = sp.exp(I * (kpar * z - omega * t + n * th))
    # Unperturbed streaming operator d/dt + v_par d/dz + Omega d/dtheta.
    op = d.eq("streaming", sp.Symbol("L"), sp.simplify(
        (sp.diff(harmonic, t) + vpar * sp.diff(harmonic, z) + Om * sp.diff(harmonic, th)) / harmonic))
    # src/chapters/14-hot-plasma-waves.typ:1166
    check(op, -I * (omega - kpar * vpar - n * Om))
    S, fn = sp.symbols("S_sn f_sn")
    resp = d.eq("solve", fn, sp.solve(sp.Eq(op * fn, S), fn)[0])
    # src/chapters/14-hot-plasma-waves.typ:1173
    check(resp, (I * S) / (omega - kpar * vpar - n * Om))
    # Resonance (line 1186) and resonant velocity (line 1131).
    w_r = sp.symbols("omega_r", real=True)
    vres = d.eq("resonance", sp.Symbol(r"v_{\parallel,res}"),
                sp.solve(w_r - kpar * vpar - n * Om, vpar)[0])
    check(vres, (w_r - n * Om) / kpar)


def test_circular_forcing():
    th = sp.symbols("theta", real=True)
    Ex = sp.symbols("E_x")
    vx_, vy_ = vperp * sp.cos(th), -vperp * sp.sin(th)
    for sigma in (1, -1):
        Ey = -I * sigma * Ex  # chapter 12 circular basis, line 1180
        dot = sp.expand((Ex * vx_ + Ey * vy_).rewrite(sp.exp))
        # src/chapters/14-hot-plasma-waves.typ:1181
        check(dot, sp.expand(Ex * vperp * sp.exp(I * sigma * th)))


def test_flr_bessel_weights():
    d = Derivation("Finite-Larmor-radius weights", "src/chapters/14-hot-plasma-waves.typ:1195")
    X, th0 = sp.symbols("X theta_0", real=True)
    Ompos = sp.symbols("Omega", positive=True)
    th_t = Ompos * t + th0
    # x = X + (v_perp/Omega) sin(theta) solves dx/dt = v_perp cos(theta).
    x_orbit = d.eq("orbit", sp.Symbol("x"), X + vperp / Ompos * sp.sin(th_t))
    check(sp.diff(x_orbit, t), vperp * sp.cos(th_t))
    # Jacobi-Anger: exp(i a sin th) = sum_n J_n(a) exp(i n th), checked as a
    # power series in a up to a^7.
    th, aa = sp.symbols("theta a", real=True)
    N = 8
    lhs = sp.series(sp.exp(I * aa * sp.sin(th)), aa, 0, N).removeO()
    rhs = sum(sp.series(sp.besselj(n, aa), aa, 0, N).removeO() * sp.exp(I * n * th)
              for n in range(-N, N + 1))
    diff = sp.expand((lhs - rhs).rewrite(sp.exp))
    assert sp.simplify(diff) == 0
    d.eq("Jacobi-Anger", sp.exp(I * aa * sp.sin(th)),
         sp.Sum(sp.besselj(sp.Symbol("n"), aa) * sp.exp(I * sp.Symbol("n") * th),
                (sp.Symbol("n"), -sp.oo, sp.oo)))


def test_example_magnetized():
    d = Derivation("Example: cyclotron resonances", "src/chapters/14-hot-plasma-waves.typ:1227")
    # Positive electron gyrofrequency magnitude at B0 = 1e-2 T.
    wce = CODATA[e] * 1.0e-2 / CODATA[m_e]
    close(wce, 1.76e9, 1e-3,
          d=d, name=r"\omega_{ce}")  # line 1218
    # v_te = sqrt(2 k_B T_e/m_e) for the chapter's 10 eV electrons.
    close((2 * 10 * CODATA[e] / CODATA[m_e]) ** 0.5, 1.88e6, 3e-3,
          d=d, name=r"v_{te}")  # line 1223
    w, kv = 0.80, 1.50   # omega/w_ce and k_par v_te/w_ce
    Om_e = -1.0          # Omega_e/w_ce
    vres = lambda n: (w - n * Om_e) / kv
    close(vres(0), 0.533, 1e-3,
          d=d, name=r"v_{res,0}/v_{te}")  # line 1228
    close(vres(-1), -0.133, 3e-3,
          d=d, name=r"v_{res,-1}/v_{te}")  # line 1230
    close(kv * 1.76e9 / 1.88e6, 1.40e3, 4e-3,
          d=d, name=r"k_\parallel")  # line 1231
    close(w * 1.76e9, 1.41e9, 2e-3,
          d=d, name=r"\omega")  # line 1232


def plot_hot_isotropic_dispersion():
    """Exact Maxwellian Langmuir root against its Bohm-Gross and Landau asymptotes."""
    import numpy as np

    mp.mp.dps = 30
    A = np.linspace(0.12, 0.6, 97)
    guess = mp.mpc(float(W_BOHM_GROSS.subs(a, A[0])), float(GAMMA_LANDAU.subs(a, A[0])))
    exact = []
    for av in A:  # continuation in k lambda_D from the weakly damped end
        guess = kinetic_root(av, guess)
        exact.append(complex(guess))
    mp.mp.dps = 15
    exact = np.array(exact)
    bg = sp.lambdify(a, W_BOHM_GROSS, "numpy")
    gl = sp.lambdify(a, GAMMA_LANDAU, "numpy")
    fig, top = figure(4.2, 4.0)
    top.remove()
    top, bot = fig.subplots(2, 1, sharex=True)
    for ax in (top, bot):
        ax.spines[["top", "right"]].set_visible(False)
    top.plot(A, exact.real, color=BLUE)
    top.plot(A, bg(A), color=ORANGE, ls="--")
    label(top, 0.45, exact.real[np.searchsorted(A, 0.45)] + 0.02, "exact root", BLUE, ha="right")
    label(top, 0.3, 1.08, "Bohm-Gross $\\sqrt{1+3a^2}$", ORANGE, va="top")
    top.set(ylabel=r"$\omega_r/\omega_{pe}$ [1]", ylim=(1, 1.6), yticks=[1, 1.2, 1.4, 1.6])
    bot.plot(A, -exact.imag, color=BLUE)
    bot.plot(A, -gl(A), color=ORANGE, ls="--")
    label(bot, 0.42, 0.18, "exact root", BLUE, ha="right")
    label(bot, 0.14, 0.12, "weak-damping\nasymptote", ORANGE)
    bot.set(ylabel=r"$-\gamma/\omega_{pe}$ [1]", ylim=(0, 0.3), yticks=[0, 0.1, 0.2, 0.3],
            xlabel=r"$a=k\lambda_{De}$ [1]", xlim=(0.12, 0.6))
    save(fig, "hot-isotropic-dispersion")


def plot_two_stream_growth():
    """Growth rate gamma/omega_p = sqrt(-y_-) over the unstable band 0 < K < 1."""
    import numpy as np

    g = sp.lambdify(xx, sp.sqrt(G2_TWO_STREAM), "numpy")
    K = np.linspace(0, 1, 300)
    kmax, gmax = np.sqrt(3 / 8), 1 / (2 * np.sqrt(2))  # tested in test_two_stream_maximum
    fig, ax = figure(4.2, 2.6)
    ax.plot(K, g(K**2), color=BLUE)
    ax.plot([kmax], [gmax], "o", color=ORANGE, ms=4, zorder=3)
    label(ax, kmax + 0.03, gmax + 0.005,
          "max $1/(2\\sqrt{2})$ at $K=\\sqrt{3/8}$", ORANGE)
    label(ax, 0.99, 0.02, "stable for $K>1$", GRAY, ha="right")
    ax.set(xlim=(0, 1.1), ylim=(0, 0.42), xticks=[0, 0.25, 0.5, 0.75, 1],
           xlabel=r"$K=|k v_0|/\omega_p$ [1]", ylabel=r"$\gamma/\omega_p$ [1]")
    save(fig, "two-stream-growth")


if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
