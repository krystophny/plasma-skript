"""Chapter 11, introduction to waves: src/chapters/11-introduction-waves.typ.

Run `python derivations/ch11_introduction_waves.py` to run every check, or
`pytest derivations` to check every chapter.

Coverage (Typst line -> test):
  88-91, 140-144 plane-wave replacement         -> test_plane_wave_replacement
  95-104, 126-153 linearized Fourier system      -> test_linearized_fourier_system
  166-187 example: epsilon, lambda_D, k lambda_D -> test_example_linearization
  268, 314, 351 omega_pe^2                       -> test_plasma_frequency
  287-309 electron response, Poisson loop        -> test_plasma_frequency
  275-276, 321 multi-species omega_p^2           -> test_multispecies_plasma_frequency
  328-341 example: omega_pe, f_p                 -> test_example_plasma_frequency
  428-438, 497 eps_r, k^2c^2 = omega^2 eps_r      -> test_em_branch_determinant
  453-493 current response, transverse wave eq.  -> test_em_branch_determinant
  433-438 v_phi, v_g;  559 v_phi v_g = c^2       -> test_phase_group_velocity
  531-544 example: kc/omega_pe, v_phi, v_g, k    -> test_example_em_branch
  610-612 lambda_D definition                    -> test_example_ion_acoustic
  654-662, 666-701 warm-fluid response/dispersion -> test_warm_fluid_dispersion
  705, 886 warm Langmuir branch                  -> test_warm_fluid_dispersion
  662, 711 ion-acoustic limit                    -> test_ion_acoustic_limit
  725-733 kinetic chi_s with Z(zeta)             -> test_kinetic_susceptibility_limits
  748-764 example: c_s, omega, lambda_D          -> test_example_ion_acoustic
  826-831, 846-862 W^2 = 1+K^2 and its limits    -> test_normalized_branch_limits
  871-875 evanescent k = i alpha                 -> test_evanescent_branch
  890-905 example: drive classification          -> test_example_drive_classification
Not checked: 95-104 (governing equations themselves, inputs), 638-642
(Z(zeta) definition; its asymptotics are used in test_kinetic_...), the
animation ansatz at 512 (prescribed illustration, not a result).
"""

import sympy as sp
from sympy.physics import units as u

from si import UNITS, Derivation, c, check, e, eps0, k_B, m_e, m_i, mu0

# Wave and plasma symbols.
omega, k, n0, T_e, T_i = sp.symbols("omega k n_0 T_e T_i", positive=True)
x, t, gamma_e, gamma_i = sp.symbols("x t gamma_e gamma_i", positive=True)
UNITS.update({omega: 1 / u.second, k: 1 / u.meter, n0: u.meter**-3,
              T_e: u.kelvin, T_i: u.kelvin, gamma_e: 1, gamma_i: 1})
I = sp.I

# CODATA 2018 values (SI) for the worked examples.
CODATA = {e: 1.602176634e-19, m_e: 9.1093837015e-31, eps0: 8.8541878128e-12,
          c: 299792458.0, m_i: 1.67262192369e-27, k_B: 1.380649e-23}
eV = 1.602176634e-19


def close(value, printed, rtol=5e-3):
    """Numerical agreement with a printed 3-4 digit result."""
    value = float(value)
    assert abs(value - printed) <= rtol * abs(printed), f"{value} != {printed}"


def omega_pe_sq(n=n0):
    return n * e**2 / (eps0 * m_e)


SRC = "src/chapters/11-introduction-waves.typ:"
wpe_s = sp.Symbol("omega_pe", positive=True)  # omega_pe as one symbol


def test_plane_wave_replacement():
    d = Derivation("Plane-wave replacement", SRC + "140")
    f = d.step("plane wave", sp.exp(I * (k * x - omega * t)))
    # Acting on the plane wave: d/dt -> -i omega, d/dx -> i k.
    dt = d.eq("time derivative", sp.Derivative(f, t) / f, sp.simplify(sp.diff(f, t) / f))
    dx = d.eq("gradient", sp.Derivative(f, x) / f, sp.simplify(sp.diff(f, x) / f))
    check(dt, -I * omega)  # src/chapters/11-introduction-waves.typ:141
    check(dx, I * k)  # src/chapters/11-introduction-waves.typ:142


def test_linearized_fourier_system():
    d = Derivation("Linearized continuity", SRC + "147")
    eps, n1, u1 = sp.symbols("epsilon n_1 u_1")
    f = sp.exp(I * (k * x - omega * t))
    # n = n0 + eps n1 e^{i(kx-wt)}, u = eps u1 e^{i(kx-wt)}.
    n_tot, u_tot = n0 + eps * n1 * f, eps * u1 * f
    cont = d.eq("continuity", sp.Symbol("0"), sp.diff(n_tot, t) + sp.diff(n_tot * u_tot, x))
    # Keep O(eps); the O(eps^2) term is the dropped nonlinear flux.
    first = d.eq("first order", sp.Symbol("0"),
                 sp.expand(sp.diff(cont, eps).subs(eps, 0) / f))
    assert sp.diff(cont, eps, 2).subs(eps, 0) != 0
    stated = -I * omega * n1 + I * n0 * k * u1  # src/chapters/11-introduction-waves.typ:147
    check(first, stated)


def test_plasma_frequency():
    d = Derivation("Electron plasma frequency", SRC + "314")
    E1, u1 = sp.symbols("E_1 u_1")
    # Cold electron momentum: -i omega m_e u1 = -e E1.
    mom = d.step("momentum", sp.Eq(-I * omega * m_e * u1, -e * E1))
    u_sol = d.eq("solve", u1, sp.solve(mom, u1)[0])
    check(u_sol, (-I * e * E1) / (m_e * omega))  # src/chapters/11-introduction-waves.typ:305
    # Continuity n1 = n0 k u1/omega, Poisson i k E1 = -e n1/eps0.
    n_sol = d.eq("continuity", sp.Symbol("n_1"), n0 * k * u_sol / omega)
    pois = d.step("Poisson", sp.Eq(I * k * E1, -e * n_sol / eps0))
    w2 = d.eq("cancel field", omega**2, sp.solve(pois, omega)[0] ** 2)
    stated = (n0 * e**2) / (eps0 * m_e)  # src/chapters/11-introduction-waves.typ:314
    check(w2, stated, unit=u.second**-2)


def test_multispecies_plasma_frequency():
    d = Derivation("Multi-species plasma frequency", SRC + "321")
    q1, q2, n1, n2, m1, m2, E1 = sp.symbols("q_1 q_2 n_1 n_2 m_1 m_2 E_1", positive=True)
    # Each cold species: n_s1 = n_s k u_s1/omega with u_s1 = i q_s E1/(m_s omega).
    rho1 = d.eq("species sum", sp.Symbol(r"\rho_1"),
                sum(q * (n * k / omega) * (I * q * E1 / (m * omega))
                    for q, n, m in [(q1, n1, m1), (q2, n2, m2)]))
    w2 = d.eq("Poisson", omega**2, sp.solve(sp.Eq(I * k * E1, rho1 / eps0), omega)[0] ** 2)
    stated = (n1 * q1**2) / (eps0 * m1) + (n2 * q2**2) / (eps0 * m2)  # src/chapters/11-introduction-waves.typ:321
    check(w2, stated)
    # Hydrogen: ion term / electron term = m_e/m_i.
    ratio = d.eq("hydrogen ratio", sp.Symbol("omega_pi") ** 2 / wpe_s**2,
                 sp.simplify((n0 * e**2 / (eps0 * m_i)) / omega_pe_sq()))
    check(ratio, m_e / m_i)


def test_example_linearization():
    d = Derivation("Example: linearization scales", SRC + "166")
    n, Te = 1.0e16, 1.0 * eV
    lamD = d.eq("Debye length [m]", sp.Symbol("lambda_D"), sp.sqrt(eps0 * Te / (n * e**2)).subs(CODATA).evalf(4))
    kk = 2 * sp.pi / 0.10
    klam = d.eq("product", sp.Symbol(r"k \lambda_D"), (kk * lamD).evalf(3))
    wpe = d.eq("plasma frequency [1/s]", wpe_s, sp.sqrt(omega_pe_sq(n)).subs(CODATA).evalf(4))
    close(lamD, 7.43e-5)  # src/chapters/11-introduction-waves.typ:182
    close(klam, 4.67e-3)  # src/chapters/11-introduction-waves.typ:183
    close(wpe, 5.64e9)  # src/chapters/11-introduction-waves.typ:184
    close(1.0e10 / wpe, 1.77)  # src/chapters/11-introduction-waves.typ:185


def test_example_plasma_frequency():
    d = Derivation("Example: plasma frequency", SRC + "339")
    wpe = d.eq("plasma frequency [1/s]", wpe_s, sp.sqrt(omega_pe_sq(1.0e16)).subs(CODATA).evalf(4))
    fp = d.eq("divide by 2 pi [1/s]", sp.Symbol("f_p"), (wpe / (2 * sp.pi)).evalf(4))
    close(wpe, 5.64e9)  # src/chapters/11-introduction-waves.typ:339
    close(fp, 8.98e8)  # src/chapters/11-introduction-waves.typ:340


def test_em_branch_determinant():
    d = Derivation("Cold electromagnetic branch", SRC + "493")
    Ev = sp.Matrix(sp.symbols("E_x E_y E_z"))
    # Cold electron velocity and current j = -e n0 u.
    uvec = -I * e * Ev / (m_e * omega)  # src/chapters/11-introduction-waves.typ:457
    j = -e * n0 * uvec
    check(j[0], (I * n0 * e**2 * Ev[0]) / (m_e * omega))  # src/chapters/11-introduction-waves.typ:461-462
    # Faraday k x E = omega B, Ampere k x B = -omega E/c^2 - i mu0 j:
    # k x (k x E) + omega^2 E/c^2 + i omega mu0 j = 0.
    kv = sp.Matrix([0, 0, k])
    wave = kv.cross(kv.cross(Ev)) + omega**2 / c**2 * Ev + I * omega * mu0 * j
    M = d.step("wave matrix", wave.jacobian(Ev).subs(mu0, 1 / (eps0 * c**2)))
    det = d.eq("determinant", sp.Symbol("D"), sp.factor(M.det()))
    w2_set = {sp.simplify(r**2) for r in sp.solve(det, omega)}
    stated = omega_pe_sq() + c**2 * k**2  # src/chapters/11-introduction-waves.typ:493
    assert any(sp.simplify(w - stated) == 0 for w in w2_set)  # transverse
    assert any(sp.simplify(w - omega_pe_sq()) == 0 for w in w2_set)  # longitudinal
    d.eq("transverse root", omega**2, stated)
    # Divide by omega^2: k^2 c^2/omega^2 = 1 - omega_pe^2/omega^2.
    k2 = sp.solve(sp.Eq(omega**2, stated), k)[0] ** 2
    eps_r = d.eq("divide by omega squared", c**2 * k**2 / omega**2, sp.expand(c**2 * k2 / omega**2))
    check(eps_r, 1 - omega_pe_sq() / omega**2)  # src/chapters/11-introduction-waves.typ:497, 433


def test_phase_group_velocity():
    d = Derivation("Phase and group velocity", SRC + "437")
    UNITS[wpe_s] = 1 / u.second
    w = d.eq("branch", omega, sp.sqrt(wpe_s**2 + c**2 * k**2))
    v_phi = d.eq("omega/k", sp.Symbol(r"v_\phi"), w / k)
    v_g = d.eq("d omega/dk", sp.Symbol("v_g"), sp.diff(w, k))
    check(v_phi, c * sp.sqrt(1 + wpe_s**2 / (c**2 * k**2)), unit=u.meter / u.second)  # src/chapters/11-introduction-waves.typ:437
    check(v_g, (c**2 * k) / w, unit=u.meter / u.second)  # src/chapters/11-introduction-waves.typ:438
    prod = d.eq("product", sp.Symbol(r"v_\phi v_g"), sp.simplify(v_phi * v_g))
    check(prod, c**2)  # src/chapters/11-introduction-waves.typ:559


def test_example_em_branch():
    d = Derivation("Example: electromagnetic branch", SRC + "540")
    W, wpe = 2, 5.64e9
    K = d.eq("normalized branch", sp.Symbol("K"), sp.sqrt(W**2 - 1))
    close(K, 1.732)  # src/chapters/11-introduction-waves.typ:540
    close(d.eq("W/K", sp.Symbol(r"v_\phi") / c, (W / K).evalf(4)), 1.155)  # src/chapters/11-introduction-waves.typ:541
    close(d.eq("K/W", sp.Symbol("v_g") / c, (K / W).evalf(4)), 0.866)  # src/chapters/11-introduction-waves.typ:542
    kk = d.eq("wave number [1/m]", k, (K * wpe / CODATA[c]).evalf(4))
    close(kk, 32.6)  # src/chapters/11-introduction-waves.typ:543
    close(d.eq("2 pi/k [m]", sp.Symbol("lambda"), (2 * sp.pi / kk).evalf(3)), 0.193)  # src/chapters/11-introduction-waves.typ:544


def test_warm_fluid_dispersion():
    d = Derivation("Warm-fluid dispersion", SRC + "697")
    q, ns, ms, gs, Ts = sp.symbols("q_s n_s m_s gamma_s T_s", positive=True)
    n1, u1, E1 = sp.symbols("n_1 u_1 E_1")
    cs2 = gs * k_B * Ts / ms
    # Continuity and momentum with p1 = gamma_s k_B T_s n1, plane wave.
    cont = d.step("continuity", sp.Eq(-I * omega * n1 + I * k * ns * u1, 0))  # src/chapters/11-introduction-waves.typ:668
    mom = d.step("momentum", sp.Eq(-I * omega * ms * u1, q * E1 - I * k * gs * k_B * Ts * n1 / ns))  # src/chapters/11-introduction-waves.typ:676-677
    sol = sp.solve([cont, mom], [n1, u1], dict=True)[0]
    uu = d.eq("solve", u1, sp.factor(sol[u1]))
    nn = d.eq("solve", n1, sp.factor(sol[n1]))
    check(uu, (I * q * omega * E1) / (ms * (omega**2 - k**2 * cs2)))  # src/chapters/11-introduction-waves.typ:682-683
    check(nn, (I * ns * q * k * E1) / (ms * (omega**2 - k**2 * cs2)))  # src/chapters/11-introduction-waves.typ:687-688
    # Poisson i k E1 = q n1/eps0; cancel i k E1.
    disp = d.eq("Poisson", sp.Integer(1), sp.simplify(q * nn / (eps0 * I * k * E1)))
    check(disp, (ns * q**2) / (eps0 * ms * (omega**2 - k**2 * cs2)))  # src/chapters/11-introduction-waves.typ:697-698
    # Electron branch with fixed ions (only the electron term).
    ce2 = gamma_e * k_B * T_e / m_e
    w2 = d.eq("fixed ions", omega**2,
              sp.solve(sp.Eq(1, omega_pe_sq() / (omega**2 - k**2 * ce2)), omega)[0] ** 2)
    check(w2, omega_pe_sq() + k**2 * ce2, unit=u.second**-2)  # src/chapters/11-introduction-waves.typ:705, 886


def test_ion_acoustic_limit():
    d = Derivation("Ion-acoustic limit", SRC + "711")
    delta = sp.symbols("delta", positive=True)  # marks the vacuum term "1"
    ce2 = gamma_e * k_B * T_e / m_e
    ci2 = gamma_i * k_B * T_i / m_i
    wpi2 = n0 * e**2 / (eps0 * m_i)
    # Two species; electron inertia dropped (omega^2 << k^2 c_e^2).
    disp = d.eq("two species", sp.Integer(0),
                delta - omega_pe_sq() / (-k**2 * ce2) - wpi2 / (omega**2 - k**2 * ci2))
    # k lambda_D << 1: the vacuum term delta = 1 is negligible.
    w2 = d.eq("long wavelength", omega**2, sp.solve(disp.subs(delta, 0), omega)[0] ** 2)
    stated = (k**2 * (gamma_e * k_B * T_e + gamma_i * k_B * T_i)) / m_i  # src/chapters/11-introduction-waves.typ:711
    check(w2, stated, unit=u.second**-2)


def test_kinetic_susceptibility_limits():
    d = Derivation("Kinetic susceptibility limits", SRC + "729")
    z, xx = sp.symbols("zeta x", positive=True)
    # |zeta| >> 1: expand 1/(x - zeta) and integrate against exp(-x^2)/sqrt(pi).
    mom = [sp.integrate(xx**(2 * j) * sp.exp(-xx**2), (xx, -sp.oo, sp.oo)) / sp.sqrt(sp.pi)
           for j in range(3)]
    Z = d.eq("series", sp.Function("Z")(z), -sum(mom[j] / z**(2 * j + 1) for j in range(3)))
    vth2 = 2 * k_B * T_e / m_e
    chi = 2 * omega_pe_sq() / (k**2 * vth2) * (1 + z * Z)
    chi = sp.expand(chi.subs(z, omega / (k * sp.sqrt(vth2))))
    d.eq("insert zeta", sp.Symbol(r"\chi_e"), chi)
    lead = d.eq("cold limit", sp.Symbol(r"\chi_e") * omega**2, sp.limit(chi * omega**2, omega, sp.oo))
    check(lead, -omega_pe_sq())  # cold result 1 - omega_pe^2/omega^2
    # Next order gives Bohm-Gross with gamma_e = 3.
    nxt = sp.limit((chi * omega**2 + omega_pe_sq()) * omega**2, omega, sp.oo)
    bg = d.eq("next order", k**2 * sp.Symbol("c_e") ** 2, sp.simplify(-nxt / omega_pe_sq()))
    check(bg, 3 * k**2 * k_B * T_e / m_e)
    # Static limit zeta -> 0: 1 + zeta Z -> 1, chi -> 1/(k lambda_D)^2.
    lamD2 = eps0 * k_B * T_e / (n0 * e**2)
    st = d.eq("static limit", sp.Symbol(r"\chi_e"), sp.simplify(2 * omega_pe_sq() / (k**2 * vth2)))
    check(st, 1 / (k**2 * lamD2))


def test_example_ion_acoustic():
    d = Derivation("Example: ion-acoustic wave", SRC + "760")
    Te, n = 10 * eV, 1.0e16
    cs = d.eq("sound speed [m/s]", sp.Symbol("c_s"), sp.sqrt(Te / CODATA[m_i]).evalf(4))
    close(cs, 3.09e4)  # src/chapters/11-introduction-waves.typ:760
    close(d.eq("times k [1/s]", omega, cs * 1.0), 3.09e4)  # src/chapters/11-introduction-waves.typ:761
    lamD = d.eq("Debye length [m]", sp.Symbol("lambda_D"), sp.sqrt(eps0 * Te / (n * e**2)).subs(CODATA).evalf(4))
    close(lamD, 2.35e-4)  # src/chapters/11-introduction-waves.typ:762
    close(1.0 * lamD, 2.35e-4)  # k lambda_D with k = 1/m, src/chapters/11-introduction-waves.typ:763


def test_normalized_branch_limits():
    d = Derivation("Normalized branch and limits", SRC + "846")
    K = sp.symbols("K", positive=True)
    W2 = d.eq("normalize", sp.Symbol("W") ** 2,
              sp.expand(((wpe_s**2 + c**2 * k**2) / wpe_s**2).subs(k, K * wpe_s / c)))
    check(W2, 1 + K**2)  # src/chapters/11-introduction-waves.typ:846
    W = sp.sqrt(W2)
    vg = d.eq("dW/dK", sp.Symbol("v_g") / c, sp.diff(W, K))
    check(vg, K / W)  # src/chapters/11-introduction-waves.typ:835
    assert sp.limit(W, K, 0) == 1 and sp.limit(vg, K, 0) == 0  # src/chapters/11-introduction-waves.typ:850
    lim = d.eq("large K", sp.Symbol(r"v_\phi") / c, sp.limit(W / K, K, sp.oo))
    assert lim == 1 and sp.limit(K / W, K, sp.oo) == 1  # src/chapters/11-introduction-waves.typ:858-862


def test_evanescent_branch():
    d = Derivation("Evanescent branch", SRC + "875")
    k2 = d.eq("below cutoff", k**2, (omega**2 - wpe_s**2) / c**2)  # src/chapters/11-introduction-waves.typ:871
    alpha = d.eq("k = i alpha", sp.Symbol("alpha"), sp.sqrt(sp.factor(-k2)))
    check((I * alpha) ** 2, k2)
    check(alpha**2, (sp.sqrt(wpe_s**2 - omega**2) / c) ** 2)  # src/chapters/11-introduction-waves.typ:875


def test_example_drive_classification():
    d = Derivation("Example: drive classification", SRC + "901")
    wpe = d.eq("plasma frequency [1/s]", wpe_s, sp.sqrt(omega_pe_sq(1.0e16)).subs(CODATA).evalf(4))
    close(wpe, 5.64e9)  # src/chapters/11-introduction-waves.typ:901
    alpha = d.eq("lower drive: alpha [1/m]", sp.Symbol("alpha"), (sp.sqrt(wpe**2 - 4.0e9**2) / CODATA[c]).evalf(3))
    close(alpha, 13.3)  # src/chapters/11-introduction-waves.typ:902
    w = 1.13e10
    kk = d.eq("upper drive: k [1/m]", k, (sp.sqrt(w**2 - wpe**2) / CODATA[c]).evalf(3))
    close(kk, 32.7)  # src/chapters/11-introduction-waves.typ:903
    close(w / (kk * CODATA[c]), 1.15)  # src/chapters/11-introduction-waves.typ:904
    close(kk * CODATA[c] / w, 0.866)  # src/chapters/11-introduction-waves.typ:905


if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
