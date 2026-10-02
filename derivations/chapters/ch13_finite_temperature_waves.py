"""Chapter 13, finite-temperature waves: src/chapters/13-finite-temperature-waves.typ.

Run `python derivations/ch13_finite_temperature_waves.py` to run every check,
or `pytest derivations` to check every chapter.

Coverage (Typst line -> test):
  65-71, 99-115 effective mass from drag            -> test_effective_mass
  82-83, 124-127 collisional RH circular response    -> test_collisional_rh_response
  135-137 weak-collision susceptibility             -> test_weak_collision_expansion
  87-89, 143-147 spatial attenuation, 1/(2 k_i)      -> test_spatial_attenuation
  166-179 collisional worked example                -> test_example_collisional
  257-264 two-species eps_perp, eps_times, eps_par   -> test_two_species_tensor
  264, 324, 580, 983 mass-ratio identities          -> test_mass_ratio_identities
  313-314 parallel determinant factors              -> test_parallel_determinant
  277-283, 319-335 RH/LH circular branches          -> test_circular_branches
  284-293, 343-356 low-frequency Alfven limit       -> test_alfven_limit
  498-529 warm species velocity response            -> test_warm_species_response
  463-465, 535-539 warm longitudinal susceptibility  -> test_warm_susceptibility
  466-472, 547-560 warm Langmuir branch             -> test_warm_langmuir
  478-490, 566-585 two-species roots, ion acoustic  -> test_ion_acoustic
  594-610 warm Langmuir worked example              -> test_example_warm_langmuir
  707, 723-774 warm upper-hybrid branch             -> test_warm_upper_hybrid
  694-697, 712, 786-814 perpendicular magnetosonic  -> test_magnetosonic
  710, 822-826 shear Alfven                         -> test_shear_alfven
  838-846 animation speed ratio sqrt(1.36)          -> test_animation_speeds
  853-867 MHD worked example                        -> test_example_mhd
  971-998 cold limits (nu -> 0, T_s -> 0)           -> test_cold_limits
  figure ion-wave-branches: normalized RH/LH roots  -> test_normalized_ion_branches
  1035-1042 ordering example, M = m_e/m_p           -> test_ordering_example
Not covered: 1021-1023 and 943-961 are ordering inequalities, not formulas.
"""

import sympy as sp
from sympy.physics import units as u

from si import (BLUE, GRAY, ORANGE, UNITS, Derivation, c, check, e, eps0, figure,
                k_B, label, log_ticks, m_e, m_i, mu0, save)

I = sp.I
w, nu, k, kpar = sp.symbols("omega nu k k_\\parallel", positive=True)
n0, B0, T_e, T_i, gam_e, gam_i, gam = sp.symbols(
    "n_0 B_0 T_e T_i gamma_e gamma_i gamma", positive=True
)
wpe, wpi, wce, wci = sp.symbols(
    "omega_pe omega_pi omega_ce omega_ci", positive=True
)
cse, csi, vs, rho0, p0 = sp.symbols("c_se c_si v_s rho_0 p_0", positive=True)
z = sp.symbols("z", real=True)
UNITS.update({
    w: u.second**-1, nu: u.second**-1, k: u.meter**-1, kpar: u.meter**-1,
    n0: u.meter**-3, B0: u.tesla, T_e: u.kelvin, T_i: u.kelvin,
    gam_e: 1, gam_i: 1, gam: 1,
    wpe: u.second**-1, wpi: u.second**-1, wce: u.second**-1, wci: u.second**-1,
    cse: u.meter / u.second, csi: u.meter / u.second, vs: u.meter / u.second,
    rho0: u.kilogram / u.meter**3, p0: u.pascal,
})

# CODATA 2018 values for the worked examples.
CODATA = {
    e: 1.602176634e-19, m_e: 9.1093837015e-31, m_i: 1.67262192369e-27,
    eps0: 8.8541878128e-12, mu0: 1.25663706212e-6, c: 299792458.0,
    k_B: 1.380649e-23,
}


def close(value, printed, rel=5e-3):
    """Numerical value agrees with the printed (rounded) number."""
    value = complex(value)
    assert abs(value - printed) <= rel * abs(printed), f"{value} vs {printed}"


def cold_velocity(q, m, Omega, E, drag=0):
    """Solve -i w m u = q (E + u x B0 e_z) - m nu u for the vector u.

    Omega = q B0 / m is the signed gyrofrequency.
    """
    ux, uy, uz = sp.symbols("u_x u_y u_z")
    U = sp.Matrix([ux, uy, uz])
    lorentz = sp.Matrix([uy, -ux, 0]) * Omega  # (q/m) u x B0 e_z
    eqs = -I * w * U - (q / m) * sp.Matrix(E) - lorentz + drag * U
    sol = sp.solve(list(eqs), [ux, uy, uz], dict=True)[0]
    return sp.Matrix([sol[ux], sol[uy], sol[uz]])


def dielectric(species):
    """Cold dielectric tensor eps = 1 + i j/(eps0 w) from (q, n, m, Omega, drag)."""
    Ex, Ey, Ez = sp.symbols("E_x E_y E_z")
    j = sp.zeros(3, 1)
    for q, n, m, Om, drag in species:
        j += q * n * cold_velocity(q, m, Om, [Ex, Ey, Ez], drag)
    D = sp.Matrix([Ex, Ey, Ez]) + I / (eps0 * w) * j
    return D.jacobian([Ex, Ey, Ez])


# Electron parameters expressed through omega_pe and omega_ce.
ELECTRON = {n0: wpe**2 * eps0 * m_e / e**2, B0: wce * m_e / e}


def electron(drag=0):
    return (-e, n0, m_e, -e * B0 / m_e, drag)


def test_effective_mass():
    # src/...typ:99-115: (-i w m + m nu) u = -i w m_eff u defines m_eff.
    d = Derivation("Complex effective mass", "src/chapters/13-finite-temperature-waves.typ:99")
    m = sp.symbols("m", positive=True)
    Ms = sp.Symbol("m_eff")
    law = d.step("drag moved left", sp.Eq(-I * w * m + m * nu, -I * w * Ms))
    m_eff = d.eq("solve", Ms, sp.solve(law, Ms)[0])
    stated = m * (1 + (I * nu) / w)  # src/chapters/13-finite-temperature-waves.typ:115
    check(m_eff, stated)
    # Same velocity response from the drag equation and from the effective mass.
    E = sp.symbols("E_x E_y E_z")
    Om = sp.symbols("Omega", real=True)
    drag = cold_velocity(-e, m, Om, E, drag=nu)
    eff = cold_velocity(-e, stated, Om * m / stated, E)
    d.eq("same velocity", sp.Symbol("u_x^{drag}"), sp.simplify(drag[0]))
    assert sp.simplify(drag - eff) == sp.zeros(3, 1)


def test_collisional_rh_response():
    # Cold electron tensor with drag; RH circular coefficient R = eps_xx + i eps_xy.
    d = Derivation("Collisional RH branch", "src/chapters/13-finite-temperature-waves.typ:82")
    eps = dielectric([electron(drag=nu)]).subs(ELECTRON)
    d.eq("cold tensor with drag", sp.Symbol(r"\epsilon_{xx}"), sp.apart(sp.simplify(eps[0, 0]), wce))
    d.eq("", sp.Symbol(r"\epsilon_{xy}"), sp.simplify(eps[0, 1]))
    R = sp.simplify(eps[0, 0] + I * eps[0, 1])
    d.eq("R = S + D", sp.Symbol("1 - N_{RH}^2"), sp.factor(1 - R))
    stated = 1 - wpe**2 / (w * (w - wce + I * nu))  # src/...typ:82-83
    check(R, stated, unit=1)
    # Effective-parameter form of the substitution (src/...typ:124-127).
    lhs = (wpe**2 / (1 + I * nu / w)) / (w * (w - wce / (1 + I * nu / w)))
    d.eq("effective parameters", sp.UnevaluatedExpr(lhs), sp.simplify(lhs))
    check(lhs, wpe**2 / (w * (w - wce + I * nu)))  # src/...typ:126-127


def test_weak_collision_expansion():
    # Unmagnetized limit (wce = 0) of the electron susceptibility magnitude.
    d = Derivation("Weak-collision susceptibility", "src/chapters/13-finite-temperature-waves.typ:135")
    chi = d.eq("unmagnetized", sp.Symbol(r"\chi_e"), wpe**2 / (w * (w + I * nu)))
    first = d.eq("series in nu", sp.Symbol(r"\chi_e"), sp.series(chi, nu, 0, 2).removeO())
    stated = wpe**2 / w**2 * (1 - (I * nu) / w)  # src/...typ:136-137
    check(first, stated, unit=1)
    # N^2 = 1 - chi then has a positive imaginary part.
    assert sp.im(sp.expand(1 - stated)).subs({nu: 1, w: 2, wpe: 1}) > 0


def test_spatial_attenuation():
    d = Derivation("Spatial attenuation", "src/chapters/13-finite-temperature-waves.typ:143")
    kr, ki, t = sp.symbols("k_r k_i t", positive=True)
    field = sp.exp(I * (kr + I * ki) * z - I * w * t)
    d.eq("complex k", sp.UnevaluatedExpr(field), sp.powsimp(sp.expand(field)))
    stated = sp.exp(I * kr * z - I * w * t) * sp.exp(-ki * z)  # src/...typ:143-144
    check(sp.powsimp(sp.expand(field)), sp.powsimp(stated))
    # Intensity ~ |amplitude|^2 = exp(-2 k_i z): e-folds after 1/(2 k_i).
    intensity = sp.exp(-ki * z) ** 2
    d.eq("intensity", sp.Symbol("I/I_0"), intensity)
    L = d.eq("e-folding", sp.Symbol("L_I"), sp.solve(sp.Eq(sp.log(intensity), -1), z)[0])
    check(L, 1 / (2 * ki), unit=u.meter, units={ki: u.meter**-1})


def test_example_collisional():
    # src/...typ:166-179; high-frequency weak-collision approximation.
    d = Derivation("Example: collisional attenuation", "src/chapters/13-finite-temperature-waves.typ:166")
    vals = {wpe: 5.64e9, w: 2.00e10, nu: 1.00e9}
    meff = (1 + I * nu / w).subs(vals)
    close(meff, 1.00 + 0.05j)  # src/...typ:175
    N2 = (1 - wpe**2 / w**2 * (1 - I * nu / w)).subs(vals)
    d.eq("weak collision", sp.Symbol("N^2"), sp.N(N2, 4))
    N = complex(sp.sqrt(N2).evalf())
    d.eq("square root", sp.Symbol("N"), sp.N(sp.sqrt(N2), 4))
    close(N.real, 0.959)  # src/...typ:176
    close(N.imag, 2.07e-3)
    kc = N * vals[w] / CODATA[c]
    close(kc.real, 64.0)  # src/...typ:177
    close(kc.imag, 1.38e-1)  # src/...typ:178
    close(1 / kc.imag, 7.23)  # src/...typ:179
    d.eq("k = w N / c, 1/m", sp.Symbol("k"), sp.N(sp.sympify(kc), 4))
    d.eq("attenuation length, m", sp.Symbol("L"), sp.Float(1 / kc.imag, 4))


SRC = "src/chapters/13-finite-temperature-waves.typ:"


# Singly charged ions with n_i = n_e: ion frequencies follow from the electron ones.
ION = {wpi: wpe * sp.sqrt(m_e / m_i), wci: wce * m_e / m_i}

# Results shared by the tests and the plots: each test proves its derivation
# equals one of these expressions, and each plot_* lambdifies the same one.
# Circular two-fluid indices without the O(m_e/m_i) numerator term (279, 281-283).
N2_RH = 1 - wpe**2 / ((w + wci) * (w - wce))
N2_LH = 1 - wpe**2 / ((w - wci) * (w + wce))
Kn, Wn = sp.symbols("K W", positive=True)  # K = k v_A/omega_ci, W = omega/omega_ci
W_RH = (Kn**2 + sp.sqrt(Kn**4 + 4 * Kn**2)) / 2  # figure ion-wave-branches
W_LH = (sp.sqrt(Kn**4 + 4 * Kn**2) - Kn**2) / 2
# Two-species warm longitudinal condition times both denominators (566-568),
# a quadratic in X = omega^2.
X2 = sp.symbols("X", positive=True)
POLY_LONG = ((X2 - k**2 * cse**2) * (X2 - k**2 * csi**2)
             - wpe**2 * (X2 - k**2 * csi**2) - wpi**2 * (X2 - k**2 * cse**2))


def two_species():
    ion = (e, n0, m_i, e * B0 / m_i, 0)
    return dielectric([electron(), ion]).subs(ELECTRON)


def test_two_species_tensor():
    d = Derivation("Two-species cold tensor", SRC + "257")
    eps = two_species()
    # Cold tensor convention: eps_xx = eps_perp, eps_xy = -i eps_times.
    show = lambda x: sp.apart(sp.simplify(x.subs(m_i, m_e * wce / wci)), w)
    eps_perp = d.eq("eps_xx", sp.Symbol(r"\epsilon_\perp"), sp.simplify(eps[0, 0]))
    d.eq("partial fractions", sp.Symbol(r"\epsilon_\perp"), show(eps_perp))
    eps_times = d.eq("i eps_xy", sp.Symbol(r"\epsilon_\times"), sp.simplify(I * eps[0, 1]))
    d.eq("partial fractions", sp.Symbol(r"\epsilon_\times"), show(eps_times))
    eps_par = d.eq("eps_zz", sp.Symbol(r"\epsilon_\parallel"), sp.simplify(eps[2, 2]))
    d.step("ion frequencies", sp.Eq(wpi**2, ION[wpi] ** 2))
    d.step("", sp.Eq(wci, ION[wci]))
    # src/chapters/13-finite-temperature-waves.typ:257-259
    s_perp = 1 - (wpe**2 / (w**2 - wce**2) + wpi**2 / (w**2 - wci**2))
    # src/...typ:260-261
    s_times = (-(wce * wpe**2) / (w * (w**2 - wce**2))
               + (wci * wpi**2) / (w * (w**2 - wci**2)))
    # src/...typ:263-264
    s_par = 1 - (wpe**2 + wpi**2) / w**2
    check(eps_perp, s_perp.subs(ION), unit=1)
    check(eps_times, s_times.subs(ION), unit=1)
    check(eps_par, s_par.subs(ION), unit=1)


def test_mass_ratio_identities():
    # Plasma and cyclotron frequencies from their definitions, n_i = n_e, Z = 1.
    wp2 = lambda m: n0 * e**2 / (eps0 * m)
    wc = lambda m: e * B0 / m
    d = Derivation("Mass-ratio identities", SRC + "324")
    d.eq("plasma frequencies", wpi**2 / wpe**2, wp2(m_i) / wp2(m_e))
    d.eq("cyclotron frequencies", wci / wce, wc(m_i) / wc(m_e))
    check(wp2(m_i) / wp2(m_e), m_e / m_i)  # src/...typ:264, 580, 984
    check(wc(m_i) / wc(m_e), m_e / m_i)  # src/...typ:983
    check(wp2(m_i) / wp2(m_e), wc(m_i) / wc(m_e))  # src/...typ:324-325


def test_parallel_determinant():
    # Wave equation N x (N x E) + eps E = 0 with N along z, transverse block.
    d = Derivation("Parallel-propagation determinant", SRC + "313")
    S, D, N2 = sp.symbols("S D N^2")
    eps = sp.Matrix([[S, -I * D], [I * D, S]])
    M = eps - N2 * sp.eye(2)
    d.eq("determinant", sp.Symbol(r"\det"), sp.factor(M.det()))
    roots = set(sp.solve(M.det(), N2))
    d.step("roots", sp.Tuple(*sorted(roots, key=str)))
    assert roots == {S + D, S - D}  # src/...typ:313-314


def test_circular_branches():
    eps = two_species()
    R = sp.simplify(eps[0, 0] + I * eps[0, 1])
    L = sp.simplify(eps[0, 0] - I * eps[0, 1])
    d = Derivation("Circular branches with ions", SRC + "319")
    d.eq("R = S + D", sp.Symbol("N_{RH}^2"), sp.apart(sp.simplify(R.subs(m_i, m_e * wce / wci)), w))
    # Exact species sum for the RH factor, src/...typ:319-320.
    rh_sum = (1 - wpe**2 / (w * (w - wce)) - wpi**2 / (w * (w + wci))).subs(ION)
    check(R, rh_sum, unit=1)
    # Common denominator: numerator wpe^2 (1 + wci/wce), src/...typ:329.
    # Common denominator (w + wci)(w - wce) after the factor w cancels.
    num = d.eq("numerator", sp.Symbol("(1-R)(\\omega+\\omega_{ci})(\\omega-\\omega_{ce})"),
               sp.simplify((1 - rh_sum) * ((w + wci) * (w - wce)).subs(ION)))
    check(num, (wpe**2 * (1 + wci / wce)).subs(ION))
    # Drop the O(m_e/m_i) numerator correction, keep ion denominators.
    rh = N2_RH  # src/...typ:279, 334-335
    lh = N2_LH  # src/...typ:281-283
    M = sp.symbols("M", positive=True)
    small = {wci: wce * M, wpi: wpe * sp.sqrt(M)}
    for exact, approx in ((R, rh), (L, lh)):
        exact = exact.subs(ION).subs(m_i, m_e / M)
        diff = sp.simplify(exact - approx.subs(small))
        d.eq("exact minus approx", sp.Symbol(r"\Delta N^2"), sp.factor(diff))
        assert sp.simplify(sp.limit(diff, M, 0)) == 0
        # The correction is first order in M.
        assert sp.simplify(sp.diff(diff, M).subs(M, 0)) != 0


def test_alfven_limit():
    rh, lh = N2_RH, N2_LH
    d = Derivation("Low-frequency Alfven limit", SRC + "343")
    stated = 1 + wpe**2 / (wce * wci)  # src/...typ:286, 343
    d.eq("limit w to 0", sp.Symbol("N^2"), sp.limit(rh, w, 0))
    for N2 in (rh, lh):
        check(sp.limit(N2, w, 0), stated, unit=1)
    # Frequency product in SI, src/...typ:347-349, with c^2 = 1/(mu0 eps0).
    defs = {wce: e * B0 / m_e, wci: e * B0 / m_i, wpe: sp.sqrt(n0 * e**2 / (eps0 * m_e))}
    ratio = d.eq("SI definitions", wce * wci / wpe**2, (wce * wci / wpe**2).subs(defs))
    d.eq("Maxwell c", wce * wci / wpe**2, ratio.subs(eps0, 1 / (mu0 * c**2)))
    check(ratio, eps0 * B0**2 / (n0 * m_i), unit=1)  # src/...typ:348
    check(ratio.subs(eps0, 1 / (mu0 * c**2)), B0**2 / (mu0 * n0 * m_i * c**2))
    # Large wpe^2/(wce wci): N^2 -> c^2 / v_A^2, src/...typ:353.
    vA = B0 / sp.sqrt(mu0 * n0 * m_i)
    lead = (wpe**2 / (wce * wci)).subs(defs).subs(eps0, 1 / (mu0 * c**2))
    check(lead, c**2 / vA**2, unit=1)  # src/...typ:353
    # v_A two ways, src/...typ:289-290.
    stated_vA = c * sp.sqrt(wce * wci) / wpe
    check(stated_vA.subs(defs).subs(eps0, 1 / (mu0 * c**2)), vA, unit=u.meter / u.second)
    # N = k c / w -> w / k = v_A, src/...typ:356.
    N2 = (k * c / w) ** 2
    wk = d.eq("N = k c / w", w / k, sp.solve(sp.Eq(N2, c**2 / vA**2), w)[0] / k)
    check(wk, vA, unit=u.meter / u.second)


def test_normalized_ion_branches():
    # omega << omega_ce and N^2 >> 1 (v_A << c): keep the leading term of
    # N^2 - 1 in 1/omega_ce, then normalize K = k v_A/omega_ci, W = omega/omega_ci.
    d = Derivation("Normalized ion-cyclotron and whistler branches", SRC + "367")
    vA = c * sp.sqrt(wce * wci) / wpe  # tested in test_alfven_limit
    for N2, stated in ((N2_RH, W_RH), (N2_LH, W_LH)):
        lead = sp.limit((N2 - 1) * wce, wce, sp.oo) / wce
        disp = sp.Eq((k * c / w) ** 2, lead)
        disp = disp.subs({k: Kn * wci / vA, w: Wn * wci})
        roots = [r for r in sp.solve(disp, Wn) if r.subs(Kn, 1).is_positive]
        d.eq("positive root", Wn, roots[0])
        assert len(roots) == 1 and sp.simplify(roots[0] - stated) == 0
    # Both start along the Alfven line W = K; LH approaches the ion cyclotron W = 1.
    for root in (W_RH, W_LH):
        assert sp.limit(root / Kn, Kn, 0) == 1
    assert sp.limit(W_LH, Kn, sp.oo) == 1


def warm_velocity(q, m, n, cs2, E1):
    """1D warm fluid: continuity, p1 = m cs^2 n1, momentum; returns (u1, n1)."""
    u1, n1 = sp.symbols("u_1 n_1")
    continuity = -I * w * n1 + I * n * k * u1
    momentum = -I * w * m * u1 - q * E1 + I * k * m * cs2 * n1 / n
    sol = sp.solve([continuity, momentum], [u1, n1], dict=True)[0]
    return sol[u1], sol[n1]


def test_warm_species_response():
    d = Derivation("Warm species response", SRC + "498")
    q, m, n, E1, Ts = sp.symbols("q m n E_1 T_s", positive=True)
    u1s, n1s = sp.symbols("u_1 n_1")
    d.step("continuity", sp.Eq(-I * w * n1s + I * n * k * u1s, 0))
    d.step("momentum", sp.Eq(-I * w * m * u1s, q * E1 - I * k * m * cse**2 * n1s / n))
    u1, n1 = warm_velocity(q, m, n, cse**2, E1)
    d.eq("solve", u1s, u1)
    d.eq("", n1s, n1)
    check(n1 / n, k * u1 / w)  # src/...typ:506
    # gamma k_B T_s n1 / n0 = m c_s^2 n1 / n0 with c_s^2 = gamma k_B T_s / m.
    check(m * (gam * k_B * Ts / m), gam * k_B * Ts)  # src/...typ:510, 518
    stated = (I * q * w * E1) / (m * (w**2 - k**2 * cse**2))  # src/...typ:529
    check(u1, stated)


def test_warm_susceptibility():
    q, m, n, E1 = sp.symbols("q m n E_1", positive=True)
    u1, _ = warm_velocity(q, m, n, cse**2, E1)
    # eps E = E + (i/(eps0 w)) j with j = q n u1 (src/...typ:535).
    d = Derivation("Warm longitudinal susceptibility", SRC + "535")
    chi = d.eq("j = q n u", sp.Symbol(r"\chi_s"), sp.simplify(I / (eps0 * w) * q * n * u1 / E1))
    wps2 = n * q**2 / (eps0 * m)
    stated = -wps2 / (w**2 - k**2 * cse**2)  # src/...typ:539
    check(chi, stated)


def test_warm_langmuir():
    # Fixed ions: 1 - wpe^2/(w^2 - k^2 cse^2) = 0, src/...typ:547-551.
    d = Derivation("Warm Langmuir branch", SRC + "547")
    Ws = sp.Symbol("W")
    disp = d.step("fixed ions", sp.Eq(1 - wpe**2 / (Ws - k**2 * cse**2), 0))
    w2 = d.eq("solve", w**2, sp.solve(disp, Ws)[0])
    check(w2, wpe**2 + k**2 * cse**2, unit=u.second**-2)  # src/...typ:551
    # c_se^2 / wpe^2 = gamma_e lambda_D^2, src/...typ:555-560.
    lam2 = eps0 * k_B * T_e / (n0 * e**2)  # src/...typ:555
    cse2 = gam_e * k_B * T_e / m_e  # src/...typ:556
    wpe2 = n0 * e**2 / (eps0 * m_e)
    d.eq("ratio", cse**2 / wpe**2, sp.simplify(cse2 / wpe2))
    check(cse2 / wpe2, gam_e * lam2, unit=u.meter**2)  # src/...typ:560
    d.eq("Debye length", w**2, sp.factor(w2.subs({wpe: sp.sqrt(wpe2), cse: sp.sqrt(cse2)})))
    # src/...typ:468-469
    check(w2.subs({wpe: sp.sqrt(wpe2), cse: sp.sqrt(cse2)}),
          wpe2 * (1 + gam_e * k**2 * lam2))


def test_ion_acoustic():
    d = Derivation("Ion acoustic root", SRC + "566")
    W = sp.symbols("W", positive=True)  # W = omega^2
    disp = d.eq("two species", sp.Symbol(r"\epsilon_\parallel"),
                1 - wpe**2 / (W - k**2 * cse**2) - wpi**2 / (W - k**2 * csi**2))
    poly = sp.expand(sp.numer(sp.together(disp)))
    # Product form, src/...typ:566-568.
    stated_poly = POLY_LONG.subs(X2, W)
    check(poly, stated_poly)
    # Low root: expand the smaller root in k to order k^2.
    roots = sp.solve(poly, W)
    low = min(roots, key=lambda r: r.subs({k: sp.Rational(1, 100), cse: 1, csi: 1,
                                          wpe: 3, wpi: 1}).evalf())
    low2 = sp.series(low, k, 0, 3).removeO()
    # sqrt((wpe^2 + wpi^2)^2) = wpe^2 + wpi^2 for positive frequencies.
    low2 = low2.replace(lambda x: x.is_Pow and x.exp == sp.S.Half,
                        lambda x: sp.sqrt(sp.factor(x.base)))
    stated = (k**2 * (wpe**2 * csi**2 + wpi**2 * cse**2)) / (wpe**2 + wpi**2)  # :485-487
    d.eq("series in k", sp.Symbol("W_-"), sp.simplify(low2))
    check(sp.simplify(low2), stated, unit=u.second**-2, units={gam: 1})
    # Linear truncation, src/...typ:574-576.
    trunc = -(wpe**2 + wpi**2) * W + k**2 * (wpe**2 * csi**2 + wpi**2 * cse**2)
    check(sp.solve(trunc, W)[0], stated)
    # Mass-ratio reduction, src/...typ:584-585 (leading order in m_e/m_i).
    M = sp.symbols("M", positive=True)
    cia2 = (stated / k**2).subs(wpi, wpe * sp.sqrt(M))
    lead = d.eq("series in M", sp.Symbol("c_{ia}^2"), sp.series(cia2, M, 0, 2).removeO())
    # The remainder -M csi^2 is an O(m_e/m_i) correction to csi^2 and is dropped;
    # M cse^2 is kept because cse^2 / csi^2 ~ m_i/m_e makes it order csi^2.
    check(lead + M * csi**2, csi**2 + M * cse**2)
    lead = csi**2 + M * cse**2
    speeds = {csi: sp.sqrt(gam_i * k_B * T_i / m_i), cse: sp.sqrt(gam_e * k_B * T_e / m_e),
              M: m_e / m_i}
    stated_cia2 = (gam_i * k_B * T_i) / m_i + (gam_e * k_B * T_e) / m_i  # :585
    d.eq("species speeds", sp.Symbol("c_{ia}^2"), sp.expand(lead.subs(speeds)))
    check(lead.subs(speeds), stated_cia2, unit=(u.meter / u.second) ** 2, units={gam: 1})
    # Same gamma for both species, src/...typ:489.
    check(k**2 * stated_cia2.subs({gam_i: gam, gam_e: gam}),
          (k**2 * gam * k_B * (T_e + T_i)) / m_i, unit=u.second**-2, units={gam: 1})


def test_example_warm_langmuir():
    # src/...typ:594-610, isothermal gamma_e = 1, k lambda_D = 0.80.
    d = Derivation("Example: warm Langmuir", SRC + "594")
    vals = {eps0: CODATA[eps0], n0: 1.0e16, e: 1.602e-19}
    lam = sp.sqrt(eps0 * k_B * T_e / (n0 * e**2))
    lam_num = float(lam.subs(T_e, 1.602e-18 / k_B).subs(vals))
    close(lam_num, 2.35e-4)  # src/...typ:607
    d.eq("Debye length, m", sp.Symbol(r"\lambda_{De}"), sp.Float(lam_num, 4))
    d.eq("k lambda = 0.8, 1/m", sp.Symbol("k"), sp.Float(0.80 / lam_num, 4))
    d.eq("Bohm-Gross", w / wpe, sp.Float((1 + 0.64) ** 0.5, 4))
    close(0.80 / lam_num, 3.40e3)  # src/...typ:608
    ratio = sp.sqrt(1 + gam_e * (k * sp.Symbol("lam")) ** 2)
    close(ratio.subs({gam_e: 1, k * sp.Symbol("lam"): 0.80}).evalf(), 1.28)  # :609


def test_warm_upper_hybrid():
    # Fixed ions, k = k e_x, E1 = E e_x, B0 = B0 e_z; signed Omega_e.
    Om = sp.symbols("Omega_e", real=True)
    qe = sp.symbols("q_e", real=True)
    n1, ux, uy, Ex = sp.symbols("n_1 u_x u_y E_x")
    continuity = -I * w * n1 + I * k * n0 * ux  # src/...typ:723
    mom_x = -I * w * ux - Om * uy - (qe / m_e) * Ex + I * k * cse**2 * n1 / n0  # :732-733
    mom_y = Om * ux - I * w * uy  # src/...typ:737
    # Check the momentum components against (q/m)(E + u x B0) - grad p / (m n0).
    lorentz = sp.Matrix([uy, -ux, 0]).T * Om
    assert sp.expand(mom_x - (-I * w * ux - (qe / m_e) * Ex - lorentz[0]
                              + I * k * cse**2 * n1 / n0)) == 0
    assert sp.expand(mom_y - (-I * w * uy - lorentz[1])) == 0
    d = Derivation("Warm upper hybrid", SRC + "723")
    d.step("continuity", sp.Eq(continuity, 0))
    d.step("x momentum", sp.Eq(mom_x, 0))
    d.step("y momentum", sp.Eq(mom_y, 0))
    sol = sp.solve([continuity, mom_x, mom_y], [n1, ux, uy], dict=True)[0]
    d.eq("solve", ux, sp.factor(sol[ux]))
    check(sol[uy], -I * (Om / w) * sol[ux])  # src/...typ:741
    wce2 = Om**2
    stated_u = (I * qe * w) / (m_e * (w**2 - wce2 - k**2 * cse**2)) * Ex  # :751-752
    check(sol[ux], stated_u)
    stated_n = (I * n0 * qe * k) / (m_e * (w**2 - wce2 - k**2 * cse**2)) * Ex  # :756-757
    check(sol[n1], stated_n)
    # Poisson i k E = q_e n1 / eps0, src/...typ:762, divided by i k E.
    ratio = sp.simplify(qe * sol[n1] / (eps0 * I * k * Ex))
    wpe2 = n0 * qe**2 / (eps0 * m_e)
    check(ratio, wpe2 / (w**2 - wce2 - k**2 * cse**2))  # src/...typ:767-769
    W = sp.symbols("W", positive=True)
    d.eq("Poisson", sp.Integer(1), ratio)
    w2 = d.eq("solve", w**2, sp.solve(sp.Eq(ratio.subs(w, sp.sqrt(W)), 1), W)[0])
    check(w2, wpe2 + Om**2 + k**2 * cse**2)  # src/...typ:773-774, 707


def mhd_matrix(kx, kz, vA2):
    """Linear ideal MHD for u, with p1 = vs^2 rho1 and B0 = B0 e_z."""
    ux, uy, uz = sp.symbols("u_x u_y u_z")
    U = sp.Matrix([ux, uy, uz])
    kv = sp.Matrix([kx, 0, kz])
    Bz = sp.Matrix([0, 0, B0])
    rho1 = rho0 * kv.dot(U) / w  # continuity
    B1 = -kv.cross(U.cross(Bz)) / w  # -i w B1 = i k x (u x B0)
    # -i w rho0 u = -i k p1 + (i k x B1) x B0 / mu0
    rhs = -I * kv * vs**2 * rho1 + (I * kv.cross(B1)).cross(Bz) / mu0
    eqs = (-I * w * rho0 * U - rhs).subs(B0, sp.sqrt(vA2 * mu0 * rho0))
    return eqs.jacobian(U), rho1, B1


def test_magnetosonic():
    vA = B0 / sp.sqrt(mu0 * rho0)  # src/...typ:695
    vA2 = sp.symbols("v_A^2", positive=True)
    d = Derivation("Perpendicular magnetosonic wave", SRC + "794")
    A, rho1, B1 = mhd_matrix(k, 0, vA2)
    d.eq("continuity", sp.Symbol(r"\rho_1"), rho1)
    d.eq("induction", sp.Symbol("B_{1z}"), B1[2])
    d.eq("MHD matrix", sp.Symbol("A"), A)
    check(rho1.subs(sp.Symbol("u_x"), 1), rho0 * k / w)  # src/...typ:795
    check(B1[2].subs(sp.Symbol("u_x"), 1), B0 * k / w)  # src/...typ:800
    # x momentum row, src/...typ:804, after p1 = vs^2 rho1.
    ux = sp.Symbol("u_x")
    row = -I * w * rho0 * ux + I * k * vs**2 * (rho0 * k * ux / w) \
        + I * k * B0 * (B0 * k * ux / w) / mu0
    check(A[0, 0] * ux, row.subs(B0, sp.sqrt(vA2 * mu0 * rho0)))
    W = sp.symbols("W", positive=True)
    w2 = d.eq("A_xx = 0", w**2, sp.solve(A[0, 0].subs(w, sp.sqrt(W)), W)[0])
    stated = k**2 * (vs**2 + B0**2 / (mu0 * rho0))  # src/...typ:809
    check(w2.subs(vA2, vA**2), stated, unit=u.second**-2, units={gam: 1})
    check(stated, k**2 * (vs**2 + vA**2))  # src/...typ:810, 712
    vm = sp.sqrt(w2.subs(vA2, vA**2)) / k
    check(vm, sp.sqrt(vA**2 + vs**2), unit=u.meter / u.second, units={gam: 1})  # src/...typ:814, 697
    # v_s^2 = gamma p0 / rho0 from p1 = (dp/drho) rho1 with p ~ rho^gamma.
    rho = sp.symbols("rho", positive=True)
    p_of_rho = p0 * (rho / rho0) ** gam
    check(sp.diff(p_of_rho, rho).subs(rho, rho0), gam * p0 / rho0,
          unit=(u.meter / u.second) ** 2, units={gam: 1})  # src/...typ:689, 696


def test_shear_alfven():
    vA2 = sp.symbols("v_A^2", positive=True)
    d = Derivation("Shear Alfven wave", SRC + "822")
    A, rho1, _ = mhd_matrix(0, kpar, vA2)
    d.eq("MHD matrix, k along z", sp.Symbol("A"), A)
    # Transverse u_y: no density perturbation, only magnetic tension.
    assert sp.simplify(sp.diff(rho1, sp.Symbol("u_y"))) == 0
    W = sp.symbols("W", positive=True)
    w2 = d.eq("A_yy = 0", w**2, sp.solve(A[1, 1].subs(w, sp.sqrt(W)), W)[0])
    check(w2, kpar**2 * vA2)  # src/...typ:826, 710
    # Plane wave in u_tt = vA^2 u_zz (src/...typ:822) gives the same relation.
    t = sp.symbols("t", real=True)
    f = sp.exp(I * (kpar * z - w * t))
    wave = sp.simplify((sp.diff(f, t, 2) - vA2 * sp.diff(f, z, 2)) / f)
    check(sp.solve(wave.subs(w, sp.sqrt(W)), W)[0], w2)


def test_animation_speeds():
    # src/...typ:842-843: vs = 0.6, vA = 1 in units L0/t0.
    d = Derivation("Animation speeds", SRC + "842")
    vm2 = d.eq("units L0/t0", sp.Symbol("v_m^2"), sp.Rational(6, 10) ** 2 + 1)
    check(vm2, sp.Rational(136, 100))


def test_example_mhd():
    # src/...typ:853-867: hydrogen, isothermal, total pressure p0 = n0 (Te + Ti).
    n, B, mi, kT = 1.0e16, 1.0e-2, 1.673e-27, 1.602e-18
    rho = n * mi
    vA = B / (CODATA[mu0] * rho) ** 0.5
    vs_num = (1 * 2 * n * kT / rho) ** 0.5  # gamma p0 / rho0
    vm = (vA**2 + vs_num**2) ** 0.5
    d = Derivation("Example: MHD speeds", SRC + "853")
    d.eq("Alfven, m/s", sp.Symbol("v_A"), sp.Float(vA, 4))
    d.eq("sound, m/s", sp.Symbol("v_s"), sp.Float(vs_num, 4))
    d.eq("magnetosonic, m/s", sp.Symbol("v_m"), sp.Float(vm, 4))
    close(vA, 2.18e6)  # src/...typ:862
    close(vs_num, 4.38e4)  # src/...typ:863
    close(vm, 2.18e6)  # src/...typ:864
    kk = 1.0e-3
    close(kk * vA, 2.18e3)  # src/...typ:866
    close(kk * vm, 2.18e3)  # src/...typ:867


def test_cold_limits():
    d = Derivation("Cold limits", SRC + "971")
    m = sp.symbols("m", positive=True)
    d.eq("limit nu to 0", sp.Symbol("m_{eff}"), sp.limit(m * (1 + I * nu / w), nu, 0))
    # nu -> 0 returns the physical mass, src/...typ:971-973.
    check(sp.limit(m * (1 + I * nu / w), nu, 0), m)
    # T_s -> 0 sends c_s -> 0 and the warm denominator to w^2, src/...typ:996-998.
    Ts = sp.symbols("T_s", positive=True)
    cs2 = gam * k_B * Ts / m
    check(sp.limit(w**2 - k**2 * cs2, Ts, 0), w**2)
    # m_i -> infinity removes the ion terms from the cold tensor (src/...typ:986-989).
    eps = two_species()
    fixed = dielectric([electron()]).subs(ELECTRON)
    d.eq("limit m_i to infinity", sp.Symbol(r"\epsilon_\perp"), sp.limit(eps[0, 0], m_i, sp.oo))
    for a, b in ((0, 0), (0, 1), (2, 2)):
        check(sp.limit(eps[a, b], m_i, sp.oo), fixed[a, b])


def test_ordering_example():
    # src/...typ:1038: M = m_e / m_p for hydrogen.
    d = Derivation("Example: mass ratio", SRC + "1038")
    d.eq("CODATA", sp.Symbol("M"), sp.Float(CODATA[m_e] / CODATA[m_i], 4))
    close(CODATA[m_e] / CODATA[m_i], 5.45e-4)


def plot_ion_wave_branches():
    """Normalized RH (whistler) and LH (ion cyclotron) roots and the Alfven line."""
    import numpy as np

    K = np.linspace(0, 2.4, 300)
    rh, lh = (sp.lambdify(Kn, r, "numpy") for r in (W_RH, W_LH))
    fig, ax = figure(4.2, 2.8)
    ax.plot(K, K, color=GRAY, ls=":", lw=1.2)
    ax.axhline(1, color=GRAY, lw=0.8, ls="-.")
    ax.plot(K, rh(K), color=BLUE)
    ax.plot(K, lh(K), color=ORANGE, ls="--")
    label(ax, 1.0, rh(1.0), "RH (whistler)", BLUE, ha="right")
    label(ax, 2.38, lh(2.38) - 0.25, "LH (ion cyclotron)", ORANGE, ha="right", va="top")
    label(ax, 1.95, 1.65, r"$\mathrm{Alfv\acute{e}n}$ $W=K$", GRAY, va="top")
    label(ax, 0.05, 1.03, "resonance $\\omega=\\omega_{ci}$", GRAY)
    ax.set(xlim=(0, 2.4), ylim=(0, 3), xticks=[0, 1, 2], yticks=[0, 1, 2, 3],
           xlabel=r"$K=kv_A/\omega_{ci}$ [1]", ylabel=r"$W=\omega/\omega_{ci}$ [1]")
    save(fig, "ion-wave-branches")


def plot_warm_longitudinal_modes():
    """Both roots of the tested two-species quadratic: Langmuir and ion acoustic.

    Isothermal electrons (gamma_e = 1, c_se^2 = omega_pe^2 lambda_De^2), cold
    ions (c_si = 0), m_i/m_e = 1836; K = k lambda_De, W = omega/omega_pe.
    """
    import numpy as np

    mass = sp.Rational(1, 1836)
    poly = POLY_LONG.subs({csi: 0, cse: wpe, wpi: wpe * sp.sqrt(mass)})
    poly = sp.expand(poly.subs({k: Kn, X2: Wn**2 * wpe**2}) / wpe**4)  # lambda_De = 1
    roots = [sp.lambdify(Kn, sp.sqrt(r), "numpy") for r in sp.solve(poly, Wn**2)]
    K = np.geomspace(1e-2, 3, 300)
    hi, lo = sorted(roots, key=lambda f: -f(1.0))
    w_pi = float(sp.sqrt(mass))
    fig, ax = figure(4.2, 2.8)
    ax.axhline(w_pi, color=GRAY, lw=0.8, ls="-.")
    ax.plot(K, hi(K), color=BLUE)
    ax.plot(K, lo(K), color=ORANGE, ls="--")
    label(ax, 0.012, hi(0.012) * 1.25, "electron plasma wave", BLUE)
    label(ax, 0.06, lo(0.06) * 1.3, "ion acoustic", ORANGE, ha="right")
    label(ax, 2.9, w_pi * 1.25, "$\\omega_{pi}/\\omega_{pe}$", GRAY, ha="right")
    ax.set(xscale="log", yscale="log", xlim=(1e-2, 3), ylim=(1e-4, 10),
           xlabel=r"$K=k\lambda_{De}$ [1]", ylabel=r"$W=\omega/\omega_{pe}$ [1]")
    log_ticks(ax.xaxis, -2, 0)
    log_ticks(ax.yaxis, -4, 1)
    save(fig, "warm-longitudinal-modes")


if __name__ == "__main__":
    from si import run_as_script
    run_as_script(globals())
