"""Chapter 12, cold magnetized waves: src/chapters/12-cold-magnetized-waves.typ.

Run `python derivations/ch12_cold_magnetized_waves.py` to print the steps, or
`pytest derivations` to check every chapter.

Coverage (src/chapters/12-cold-magnetized-waves.typ line -> test):
  67-68   Omega_s, omega_(p,s) definitions        -> test_frequency_example
  121-150 resolved cold momentum equation          -> test_cold_velocity_response
  78-90   cold dielectric tensor, eps_perp/x/par   -> test_dielectric_tensor
  159-160 eps.E = E + i j/(omega eps0)             -> test_dielectric_tensor
  105-111,168-179 magnetized wave equation         -> test_wave_equation
  194-200 example omega_pe, omega_ce, ratio        -> test_frequency_example
  205-216 example eps_perp, eps_x, eps_par         -> test_dielectric_example
  290-293,344-349 circular modes N_s^2             -> test_circular_modes
  309-313,353 parallel branches and cutoffs        -> test_parallel_cutoffs
  323-337 parallel wave matrix and eigenvalues     -> test_parallel_matrix
  364-373 Faraday rotation angle                   -> test_faraday_rotation
  415-426 example N_+, N_-, theta_F                -> test_faraday_example
  500-510,530-552 O and X modes, polarization      -> test_perpendicular_matrix
  519,619 N_X^2 = eps_+ eps_- / eps_perp           -> test_perpendicular_matrix
  505-507,556-576 X mode, upper hybrid             -> test_extraordinary_upper_hybrid
  593-605 example O evanescent, X propagating      -> test_perpendicular_example
  679-684,713-728 oblique wave matrix              -> test_oblique_matrix
  735-750 determinant as quadratic A Z^2-B Z+C     -> test_oblique_matrix
  755-765 S, P, |D|, S^2-D^2 for one species       -> test_stix_single_species
  686-691 Appleton-Hartree roots                   -> test_appleton_hartree
  774-776 theta = 0 and pi/2 endpoints             -> test_oblique_endpoints
  700     X_w = 1/W^2, Y_w = Y/W                   -> test_oblique_example
  785-795 example N_+, N_- at theta = pi/4         -> test_oblique_example
  882-891 normalized landmarks                     -> test_normalized_landmarks
  897-913 Y -> 0 and high-frequency limits         -> test_normalized_landmarks
  944-962 example cutoffs and O/X classification   -> test_landmark_example
"""

import sympy as sp
from sympy.physics import units as u

from si import (BLUE, GRAY, ORANGE, UNITS, Derivation, c, check, e, eps0, figure,
                label, m_e, mu0, same_unit, save, si_unit)

SRC = "src/chapters/12-cold-magnetized-waves.typ"

# CODATA 2018 values for the worked examples.
CODATA = {
    e: 1.602176634e-19,
    m_e: 9.1093837015e-31,
    eps0: 8.8541878128e-12,
    c: 299792458.0,
}

I = sp.I
w, k, B0, n0 = sp.symbols("omega k B_0 n_0", positive=True)
wpe, wce = sp.symbols("omega_pe omega_ce", positive=True)
N, theta = sp.symbols("N theta", positive=True)
Ex, Ey, Ez = sp.symbols("E_x E_y E_z")
UNITS.update({w: u.second**-1, k: u.meter**-1, B0: u.tesla,
              n0: u.meter**-3, wpe: u.second**-1, wce: u.second**-1})

# Results shared by the tests and the plots: each test proves its derivation
# equals one of these expressions, and each plot_* lambdifies the same one.
s_ = sp.Symbol("s")  # circular label s = +1 or -1
EPS_CIRC = 1 - wpe**2 / (w * (w + s_ * wce))  # N_s^2, line 348
N_O2 = 1 - wpe**2 / w**2  # ordinary mode, line 539
N_X2 = 1 - (wpe**2 * (w**2 - wpe**2)) / (w**2 * (w**2 - wpe**2 - wce**2))  # line 570
W_, Y_ = sp.symbols("W Y", positive=True)  # W = omega/omega_pe, Y = omega_ce/omega_pe
NORM = {w: W_ * wpe, wce: Y_ * wpe}


def close(x, ref, rtol=5e-3):
    """Numerical agreement with a printed three-digit value."""
    x = complex(x)
    assert abs(x.imag) < 1e-12 * abs(x)
    assert abs(x.real - ref) <= rtol * abs(ref), f"{x.real} vs printed {ref}"
    return sp.Float(x.real, 4)


def eps_species(q, m, n):
    """Cold susceptibility of one species from its momentum equation."""
    ux, uy, uz = sp.symbols("u_x u_y u_z")
    # -i w m u = q (E + u x B0 e_z), components in the plane-wave convention.
    eqs = [-I * w * m * ux - q * (Ex + uy * B0),
           -I * w * m * uy - q * (Ey - ux * B0),
           -I * w * m * uz - q * Ez]
    sol = sp.solve(eqs, [ux, uy, uz], dict=True)[0]
    # Species current j = q n u, then chi = sigma / (-i w eps0).
    j = [q * n * sol[v] for v in (ux, uy, uz)]
    sigma = sp.Matrix(3, 3, lambda a, b: sp.diff(j[a], (Ex, Ey, Ez)[b]))
    return sol, q * B0 / m, sigma / (-I * w * eps0)


def eps_electron():
    """Electron tensor with Omega_e = -omega_ce and omega_pe^2 inserted."""
    _, _, chi = eps_species(-e, m_e, n0)
    chi = chi.subs(B0, wce * m_e / e).subs(n0, wpe**2 * eps0 * m_e / e**2)
    return (sp.eye(3) + chi).applyfunc(sp.simplify)


def wave_matrix(eps, th, sc=None):
    """Normalized wave matrix of k(k.E) - k^2 E + w^2/c^2 eps.E, divided by w^2/c^2.

    k = k (sin th e_x + cos th e_z); pass sc = (a, b) to use symbols for (sin, cos).
    """
    sn, cs = sc if sc else (sp.sin(th), sp.cos(th))
    nhat = sp.Matrix([sn, 0, cs])
    geo = N**2 * (nhat * nhat.T - sp.eye(3))
    return (geo + eps).applyfunc(sp.expand if sc else sp.simplify)


def test_cold_velocity_response():
    d = Derivation("Cold magnetized velocity response", f"{SRC}:142")
    q, m = sp.symbols("q_s m_s", real=True)
    ux, uy, uz = sp.symbols("u_x u_y u_z")
    Om = sp.Symbol("Omega_s")
    d.step("momentum x", sp.Eq(-I * w * ux - Om * uy, q / m * Ex))
    d.step("momentum y", sp.Eq(Om * ux - I * w * uy, q / m * Ey))
    sol, _, _ = eps_species(q, m, 1)
    sol = {v: sp.simplify(x.subs(B0, Om * m / q)) for v, x in sol.items()}
    dd = m * (w**2 - Om**2)
    # src/chapters/12-cold-magnetized-waves.typ:142
    stated_ux = (I * q * w) / dd * Ex - (q * Om) / dd * Ey
    # src/chapters/12-cold-magnetized-waves.typ:148
    stated_uy = (q * Om) / dd * Ex + (I * q * w) / dd * Ey
    # src/chapters/12-cold-magnetized-waves.typ:137 solved for u_z
    stated_uz = (q / m) * Ez / (-I * w)
    check(d.eq("solve", ux, sol[ux]), stated_ux)
    check(d.eq("solve", uy, sol[uy]), stated_uy)
    check(d.eq("parallel", uz, sol[uz]), stated_uz)


def test_dielectric_tensor():
    d = Derivation("Cold dielectric tensor", f"{SRC}:78")
    # Two arbitrary species; the tensor is identity plus the sum of chi_s.
    q1, q2 = sp.symbols("q_1 q_2", real=True)
    m1, m2, n1, n2 = sp.symbols("m_1 m_2 n_1 n_2", positive=True)
    _, O1, chi1 = eps_species(q1, m1, n1)
    _, O2, chi2 = eps_species(q2, m2, n2)
    eps = sp.eye(3) + chi1 + chi2
    wp1, wp2 = n1 * q1**2 / (eps0 * m1), n2 * q2**2 / (eps0 * m2)
    # src/chapters/12-cold-magnetized-waves.typ:84-88
    e_perp = 1 - wp1 / (w**2 - O1**2) - wp2 / (w**2 - O2**2)
    e_x = O1 * wp1 / (w * (w**2 - O1**2)) + O2 * wp2 / (w * (w**2 - O2**2))
    e_par = 1 - wp1 / w**2 - wp2 / w**2
    check(eps[0, 0], e_perp)
    check(eps[1, 0] / I, e_x)
    check(eps[0, 1], -I * e_x)
    check(eps[1, 1], e_perp)
    check(eps[2, 2], e_par)
    # Display one species' susceptibility in Omega_1 and omega_p1.
    Os, ws = sp.symbols("Omega_1 omega_p1", positive=True)
    show = {B0: Os * m1 / q1, n1: ws**2 * eps0 * m1 / q1**2}
    for lab, (a, b) in [("xx", (0, 0)), ("yx", (1, 0)), ("zz", (2, 2))]:
        d.eq(f"chi = sigma/(-i omega eps0), {lab}", sp.Symbol(rf"\chi_{{1,{lab}}}"),
             sp.factor(sp.simplify(chi1[a, b].subs(show))))
    for a, b in [(0, 2), (1, 2), (2, 0), (2, 1)]:
        check(eps[a, b], 0)
    # eps.E = E + i j/(w eps0) with j = sigma.E (line 159).
    sigma = (chi1 + chi2) * (-I * w * eps0)
    E = sp.Matrix([Ex, Ey, Ez])
    lhs = eps * E - (E + I / (w * eps0) * sigma * E)
    assert lhs.applyfunc(sp.simplify) == sp.zeros(3, 1)


def test_wave_equation():
    d = Derivation("Magnetized wave equation", f"{SRC}:105")
    # Faraday: k x E = w B; Ampere: k x B = -w E/c^2 - i mu0 j (lines 168-173).
    kv = sp.Matrix(sp.symbols("k_x k_y k_z"))
    E = sp.Matrix([Ex, Ey, Ez])
    j = sp.Matrix(sp.symbols("j_x j_y j_z"))
    B = kv.cross(E) / w
    kxB = -w * E / c**2 - I * mu0 * j
    # src/chapters/12-cold-magnetized-waves.typ:178
    stated_bac = kv * kv.dot(E) - kv.dot(kv) * E
    assert (kv.cross(kv.cross(E)) - stated_bac).applyfunc(sp.expand) == sp.zeros(3, 1)
    assert (kv.cross(w * B) - kv.cross(kv.cross(E))).applyfunc(sp.simplify) == sp.zeros(3, 1)
    # Faraday then Ampere: k x (k x E) = w (k x B).
    kxkxE = w * kxB
    d.eq("Faraday, Ampere", sp.Symbol(r"[\mathbf{k}\times(\mathbf{k}\times\mathbf{E})]_x"),
         kxkxE[0])
    # Eliminate j with eps.E = E + i j/(w eps0), and c^2 = 1/(mu0 eps0).
    epsE = E + I / (w * eps0) * j
    d.eq("eps.E", sp.Symbol(r"(\epsilon\cdot\mathbf{E})_x"), epsE[0])
    # src/chapters/12-cold-magnetized-waves.typ:107-108 (governing law)
    stated = kxkxE + w**2 / c**2 * epsE
    res = stated.subs(mu0, 1 / (eps0 * c**2)).applyfunc(sp.simplify)
    d.eq("mu0 eps0 c2 = 1", sp.Symbol(r"[\mathbf{k}\times(\mathbf{k}\times\mathbf{E})"
                                         r"+\omega^2 c^{-2}\epsilon\cdot\mathbf{E}]_x"), res[0])
    assert res == sp.zeros(3, 1)


def test_frequency_example():
    d = Derivation("Example: plasma and cyclotron frequency", f"{SRC}:194")
    # Plasma and cyclotron frequencies (lines 67-70), n0 = 1e16, B0 = 1e-2 T.
    wp = sp.sqrt(n0 * e**2 / (eps0 * m_e))
    wc = e * B0 / m_e
    assert same_unit(si_unit(wp), u.second**-1)
    assert same_unit(si_unit(wc), u.second**-1)
    vals = {**CODATA, n0: 1.0e16, B0: 1.0e-2}
    d.eq("CODATA", wpe, close(wp.subs(vals), 5.64e9))      # src/...typ:198
    d.eq("CODATA", wce, close(wc.subs(vals), 1.76e9))      # :199
    d.eq("ratio", wce / wpe, close((wc / wp).subs(vals), 0.312))  # :200


def test_dielectric_example():
    d = Derivation("Example: cold dielectric coefficients", f"{SRC}:205")
    eps = eps_electron()
    vals = {w: 1.00e10, wpe: 5.64e9, wce: 1.76e9}
    d.eq("xx", sp.Symbol(r"\epsilon_\perp"), close(eps[0, 0].subs(vals), 0.672))  # :214
    d.eq("yx/i", sp.Symbol(r"\epsilon_\times"),
         close((eps[1, 0] / I).subs(vals), -5.78e-2))                            # :215
    d.eq("zz", sp.Symbol(r"\epsilon_\parallel"), close(eps[2, 2].subs(vals), 0.682))  # :216


def test_parallel_matrix():
    d = Derivation("Parallel wave matrix", f"{SRC}:323")
    eps = eps_electron()
    M = wave_matrix(eps, 0)
    S, Dx, P = eps[0, 0], eps[1, 0] / I, eps[2, 2]
    Ss, Ds, Ps = sp.symbols(r"\epsilon_\perp \epsilon_\times \epsilon_\parallel")
    Mgen = wave_matrix(sp.Matrix([[Ss, -I * Ds, 0], [I * Ds, Ss, 0], [0, 0, Ps]]), 0)
    d.step("theta = 0", Mgen)
    # src/chapters/12-cold-magnetized-waves.typ:323-327
    stated = sp.Matrix([[S - N**2, -I * Dx, 0], [I * Dx, S - N**2, 0], [0, 0, P]])
    assert (M - stated).applyfunc(sp.simplify) == sp.zeros(3, 3)
    # Transverse block determinant, line 332.
    det = d.eq("determinant", sp.Symbol(r"\det_\perp"), sp.factor(Mgen[:2, :2].det()))
    check(det, (Ss - N**2)**2 - Ds**2)
    # Eigenvalues, line 336.
    roots = sp.solve(det, N**2)
    d.step("roots", sp.Eq(N**2, roots[0]))
    assert set(roots) == {Ss + Ds, Ss - Ds}


def test_circular_modes():
    d = Derivation("Circular eigenmodes", f"{SRC}:348")
    eps = eps_electron()
    s = sp.Symbol("s")
    M = wave_matrix(eps, 0)
    S, Dx = eps[0, 0], eps[1, 0] / I
    # src/chapters/12-cold-magnetized-waves.typ:348
    stated = EPS_CIRC.subs(s_, s)
    for sv in (1, -1):
        Ns2 = d.eq(f"s = {sv}", sp.Symbol(f"N_{{{sv:+d}}}^2"), sp.factor(S - sv * Dx))
        check(Ns2, stated.subs(s, sv))
        # Eigenvector E_y = -i s E_x (line 344) annihilates the block.
        vec = sp.Matrix([1, -I * sv])
        assert (M[:2, :2].subs(N**2, Ns2) * vec).applyfunc(sp.simplify) == sp.zeros(2, 1)
    # s = -1 resonance at w = w_ce (line 296).
    assert sp.solve(sp.denom(sp.together(stated.subs(s, -1))), w) == [wce]


def test_parallel_cutoffs():
    d = Derivation("Parallel cutoffs", f"{SRC}:313")
    eps = eps_electron()
    s = sp.Symbol("s")
    # Longitudinal branch eps_par = 0 -> w = w_pe (line 309).
    assert sp.solve(eps[2, 2], w) == [wpe]
    Ns2 = 1 - wpe**2 / (w * (w + s * wce))
    # Cutoff N_s = 0 -> numerator polynomial, line 353.
    poly = d.eq("N_s = 0", 0, sp.numer(sp.together(Ns2 * w * (w + s * wce))))
    check(poly, w**2 + s * wce * w - wpe**2)
    for sv in (1, -1):
        roots = sp.solve(Ns2.subs(s, sv), w)
        # src/chapters/12-cold-magnetized-waves.typ:313
        stated = (sp.sqrt(wce**2 + 4 * wpe**2) - sv * wce) / 2
        # The stated root is one of the two, and it is the positive one.
        root = [r for r in roots if sp.simplify(r - stated) == 0][0]
        d.eq(f"positive root, s = {sv}", sp.Symbol(f"omega_cut{sv:+d}"), root)
        assert all(sp.simplify(r * stated).is_negative for r in roots if r != root)
        assert same_unit(si_unit(stated), u.second**-1)


def test_faraday_rotation():
    d = Derivation("Faraday rotation", f"{SRC}:368")
    kp, km, t, E0, L = sp.symbols("k_+ k_- t E_0 L", positive=True)
    # Write the phases as mean phase Phi plus/minus half the difference Delta.
    Phi, Delta = sp.symbols("Phi Delta", real=True)
    ph_p, ph_m = Phi + Delta, Phi - Delta
    # Equal circular modes s = +1 (E_y = -i E_x) and s = -1 (E_y = +i E_x).
    Exr = sp.re(E0 / 2 * (sp.exp(I * ph_p) + sp.exp(I * ph_m)))
    Eyr = sp.re(E0 / 2 * (-I * sp.exp(I * ph_p) + I * sp.exp(I * ph_m)))
    d.eq("circular sum", sp.Symbol("E_x"), Exr)
    d.eq("circular sum", sp.Symbol("E_y"), Eyr)
    ratio = d.eq("ratio", sp.Symbol("E_y/E_x"), sp.simplify(sp.expand_trig(Eyr / Exr)))
    # The ratio depends on Delta only: tan(angle) = tan(Delta), fixed in time.
    assert sp.simplify(ratio - sp.tan(Delta)) == 0
    # Delta = ((k_+ L - w t) - (k_- L - w t))/2 at z = L.
    Delta_val = d.eq("half phase", Delta, sp.simplify(((kp * L - w * t) - (km * L - w * t)) / 2))
    # src/chapters/12-cold-magnetized-waves.typ:368
    check(Delta_val, ((kp - km) * L) / 2)
    # Slowly varying plasma, line 373: d theta_F/dz = (k_+ - k_-)/2 locally.
    z = sp.Symbol("z")
    kpz, kmz = sp.Function("k_+")(z), sp.Function("k_-")(z)
    check(sp.diff(sp.Integral(kpz - kmz, (z, 0, z)) / 2, z), (kpz - kmz) / 2)


def test_faraday_example():
    d = Derivation("Example: Faraday rotation", f"{SRC}:415")
    s = sp.Symbol("s")
    Ns2 = 1 - wpe**2 / (w * (w + s * wce))
    vals = {w: 2.00e10, wpe: 5.64e9, wce: 1.76e9}
    Np = d.eq("s = +1", sp.Symbol("N_+"), close(sp.sqrt(Ns2.subs(s, 1).subs(vals)), 0.963))
    Nm = d.eq("s = -1", sp.Symbol("N_-"), close(sp.sqrt(Ns2.subs(s, -1).subs(vals)), 0.955))
    Np, Nm = sp.sqrt(Ns2.subs(s, 1).subs(vals)), sp.sqrt(Ns2.subs(s, -1).subs(vals))
    thF = (Np - Nm) * vals[w] / CODATA[c] * 0.10 / 2
    d.eq("k = omega N/c", sp.Symbol(r"\theta_F"), close(thF, 2.45e-2))   # :426
    close(thF * 180 / sp.pi, 1.41)


def test_perpendicular_matrix():
    d = Derivation("Perpendicular O and X modes", f"{SRC}:530")
    eps = eps_electron()
    M = wave_matrix(eps, sp.pi / 2)
    S, Dx, P = eps[0, 0], eps[1, 0] / I, eps[2, 2]
    Ss, Ds, Ps = sp.symbols(r"\epsilon_\perp \epsilon_\times \epsilon_\parallel")
    Mgen = d.step("theta = pi/2", wave_matrix(
        sp.Matrix([[Ss, -I * Ds, 0], [I * Ds, Ss, 0], [0, 0, Ps]]), sp.pi / 2))
    # src/chapters/12-cold-magnetized-waves.typ:530-534
    stated = sp.Matrix([[S, -I * Dx, 0], [I * Dx, S - N**2, 0], [0, 0, P - N**2]])
    assert (M - stated).applyfunc(sp.simplify) == sp.zeros(3, 3)
    # Ordinary mode from the decoupled z row, lines 501 and 539.
    NO2 = d.eq("z row", sp.Symbol("N_O^2"), sp.solve(M[2, 2], N**2)[0])
    check(NO2, N_O2)
    # X-block determinant (line 548) and its root (lines 503, 552).
    det = d.eq("determinant", sp.Symbol(r"\det_{xy}"), sp.expand(Mgen[:2, :2].det()))
    check(det, Ss * (Ss - N**2) - Ds**2)
    NX2g = d.eq("solve", sp.Symbol("N_X^2"), sp.solve(det, N**2)[0])
    check(NX2g, (Ss**2 - Ds**2) / Ss)
    # Circular-factor form, lines 519 and 619: eps_s = S - s D.
    NX2 = NX2g.subs({Ss: S, Ds: Dx})
    sgn = sp.Symbol("s")
    eps_s = 1 - wpe**2 / (w * (w + sgn * wce))
    check(NX2, eps_s.subs(sgn, 1) * eps_s.subs(sgn, -1) / S)
    # Polarization from the first row (lines 583, 587).
    row = d.eq("first row", 0, (Mgen[0, :] * sp.Matrix([Ex, Ey, 0]))[0])
    ratio = d.eq("polarization", Ex / Ey, sp.solve(row, Ex)[0] / Ey)
    check(ratio, (I * Ds) / Ss)


def test_extraordinary_upper_hybrid():
    d = Derivation("Extraordinary mode and upper hybrid", f"{SRC}:570")
    eps = eps_electron()
    S, Dx = eps[0, 0], eps[1, 0] / I
    # src/chapters/12-cold-magnetized-waves.typ:556 and 560
    check(d.eq("one electron species", sp.Symbol(r"\epsilon_\perp"), S),
          1 - wpe**2 / (w**2 - wce**2))
    check(d.eq("Omega_e = -omega_ce", sp.Symbol(r"\epsilon_\times"), Dx),
          -(wce * wpe**2) / (w * (w**2 - wce**2)))
    NX2 = (S**2 - Dx**2) / S
    dd, p = w**2 - wce**2, wpe**2
    # src/chapters/12-cold-magnetized-waves.typ:566
    check(NX2, ((dd - p)**2 - (wce**2 * p**2) / w**2) / (dd * (dd - p)))
    # src/chapters/12-cold-magnetized-waves.typ:570 (and definition line 506)
    stated = N_X2
    d.eq("simplify", sp.Symbol("N_X^2"), sp.factor(NX2))
    check(NX2, stated)
    # Resonance where the denominator vanishes, line 576.
    pole = [r for r in sp.solve(sp.denom(sp.factor(NX2)), w) if r != 0]
    check(d.eq("pole", sp.Symbol(r"\omega_{UH}^2"), pole[0]**2), wpe**2 + wce**2,
          unit=u.second**-2)


def test_perpendicular_example():
    d = Derivation("Example: perpendicular branches", f"{SRC}:593")
    vals = {w: 5.50e9, wpe: 5.64e9, wce: 1.76e9}
    cc = CODATA[c]
    # O mode: N^2 = 1 - wpe^2/w^2 < 0, k = i alpha with alpha = sqrt(-N^2) w/c.
    NO2 = (1 - wpe**2 / w**2).subs(vals)
    assert NO2 < 0
    d.eq("evanescent O", sp.Symbol(r"\alpha_O"), close(sp.sqrt(-NO2) * vals[w] / cc, 4.17))  # :602
    NX2 = (1 - (wpe**2 * (w**2 - wpe**2)) / (w**2 * (w**2 - wpe**2 - wce**2))).subs(vals)
    assert NX2 > 0
    d.eq("propagating X", sp.Symbol("N_X"), close(sp.sqrt(NX2), 0.805))                    # :603
    d.eq("k = omega N/c", sp.Symbol("k_X"), close(sp.sqrt(NX2) * vals[w] / cc, 14.8))  # :604
    d.eq("2 pi/k", sp.Symbol(r"\lambda_X"),
         close(2 * sp.pi * cc / (sp.sqrt(NX2) * vals[w]), 0.425))                      # :605


def stix_single():
    """S, D, P of the electron tensor expressed in X_w, Y_w."""
    Xw, Yw = sp.symbols("X_omega Y_omega", positive=True)
    eps = eps_electron()
    to_XY = {wpe: sp.sqrt(Xw) * w, wce: Yw * w}
    S, D, P = (sp.simplify(x.subs(to_XY)) for x in (eps[0, 0], eps[1, 0] / I, eps[2, 2]))
    return Xw, Yw, S, D, P


def test_oblique_matrix():
    d = Derivation("Oblique wave matrix and quadratic", f"{SRC}:735")
    S, D, P, Z = sp.symbols("S D P Z")
    eps = sp.Matrix([[S, -I * D, 0], [I * D, S, 0], [0, 0, P]])
    M = wave_matrix(eps, theta)
    sn, cs = sp.sin(theta), sp.cos(theta)
    # src/chapters/12-cold-magnetized-waves.typ:679-684
    stated = sp.Matrix([[S - N**2 * cs**2, -I * D, N**2 * sn * cs],
                        [I * D, S - N**2, 0],
                        [N**2 * sn * cs, 0, P - N**2 * sn**2]])
    assert (M - stated).applyfunc(sp.simplify) == sp.zeros(3, 3)
    # Geometric contributions, lines 722 and 726.
    geo = M - eps
    check(geo[0, 0] * Ex + geo[0, 2] * Ez, -N**2 * cs**2 * Ex + N**2 * sn * cs * Ez)
    check(geo[2, 0] * Ex + geo[2, 2] * Ez, N**2 * sn * cs * Ex - N**2 * sn**2 * Ez)
    # Determinant with Z = N^2, a = sin, b = cos (line 735), on a^2 + b^2 = 1.
    a, b = sp.symbols("a b")
    Mab = wave_matrix(eps, theta, (a, b)).subs(a**2, 1 - b**2).applyfunc(sp.expand)
    d.step("k = k(a e_x + b e_z)", Mab)
    on_circle = {a: sp.sqrt(1 - b**2)}
    detM = d.eq("determinant", sp.Symbol(r"\det M"),
                sp.collect(sp.expand(Mab.det().subs(N, sp.sqrt(Z)).subs(on_circle)), Z))
    stated_det = (P - Z * a**2) * ((S - Z * b**2) * (S - Z) - D**2) - Z**2 * a**2 * b**2 * (S - Z)
    check(detM, stated_det.subs(on_circle))
    # Quadratic A Z^2 - B Z + C (lines 740-746): the Z^3 terms cancel.
    A = S * a**2 + P * b**2
    B = (S**2 - D**2) * a**2 + P * S * (1 + b**2)
    C = P * (S**2 - D**2)
    check(detM, sp.expand((A * Z**2 - B * Z + C).subs(on_circle)))
    # Roots, line 750.
    roots = sp.solve(A * Z**2 - B * Z + C, Z)
    for sg in (1, -1):
        stated_root = (B + sg * sp.sqrt(B**2 - 4 * A * C)) / (2 * A)
        assert any(sp.simplify(r - stated_root) == 0 for r in roots)


def test_stix_single_species():
    d = Derivation("S, D, P for one electron species", f"{SRC}:755")
    Xw, Yw, S, D, P = stix_single()
    # src/chapters/12-cold-magnetized-waves.typ:755-756
    check(d.eq("X, Y", sp.Symbol("S"), S), 1 - Xw / (1 - Yw**2))
    check(d.eq("X", sp.Symbol("P"), P), 1 - Xw)
    # src/chapters/12-cold-magnetized-waves.typ:760 (magnitude of D)
    check(d.eq("X, Y", sp.Symbol("D"), sp.factor(D))**2, ((Yw * Xw) / (1 - Yw**2))**2)
    # src/chapters/12-cold-magnetized-waves.typ:764
    check(d.eq("difference", sp.Symbol("S^2-D^2"), sp.factor(S**2 - D**2)),
          ((1 - Xw)**2 - Yw**2) / (1 - Yw**2))


def test_appleton_hartree():
    d = Derivation("Appleton-Hartree roots", f"{SRC}:686")
    Xw, Yw, S, D, P = stix_single()
    Z, a, b, Q = sp.symbols("Z a b Q")
    A = S * a**2 + P * b**2
    B = (S**2 - D**2) * a**2 + P * S * (1 + b**2)
    C = P * (S**2 - D**2)
    # src/chapters/12-cold-magnetized-waves.typ:687-691: N^2 = 1 - X/Q with
    # Q = 1 - T +/- R, T = Y^2 sin^2/(2(1-X)), R^2 = T^2 + Y^2 cos^2.
    T = Yw**2 * a**2 / (2 * (1 - Xw))
    R2 = T**2 + Yw**2 * b**2
    # Both signs of Q are the roots of (Q - 1 + T)^2 = R^2; insert Q = X/(1-Z).
    q_poly = d.eq("square the root", 0, (Q - 1 + T)**2 - R2)
    ah = sp.numer(sp.together(q_poly.subs(Q, Xw / (1 - Z)).subs(a**2, 1 - b**2)))
    stix = sp.numer(sp.together((A * Z**2 - B * Z + C).subs(a, sp.sqrt(1 - b**2))))
    # Same quadratic in Z up to a Z-independent factor => same pair of roots.
    ratio = d.eq("ratio of quadratics", sp.Symbol("q_{AH}/q_{Stix}"),
                 sp.factor(sp.cancel(sp.expand(ah) / sp.expand(stix))))
    assert Z not in ratio.free_symbols, ratio


def test_oblique_endpoints():
    d = Derivation("Oblique endpoints", f"{SRC}:774")
    S, D, P = sp.symbols("S D P")
    eps = sp.Matrix([[S, -I * D, 0], [I * D, S, 0], [0, 0, P]])
    # theta = 0: determinant factors into P (S+D-N^2)(S-D-N^2).
    check(d.eq("theta = 0", sp.Symbol(r"\det M"), sp.factor(wave_matrix(eps, 0).det())),
          P * (S + D - N**2) * (S - D - N**2))
    # theta = pi/2: (P - N^2) times the X-mode block.
    check(d.eq("theta = pi/2", sp.Symbol(r"\det M"),
               sp.factor(wave_matrix(eps, sp.pi / 2).det())),
          (P - N**2) * (S * (S - N**2) - D**2))


def test_oblique_example():
    d = Derivation("Example: oblique Appleton-Hartree roots", f"{SRC}:785")
    Xw, Yw, S, D, P = stix_single()
    W, Y = 1.50, 0.30
    Xv = d.eq("X = 1/W2", Xw, close(1 / W**2, 0.444))   # src/...typ:700, :792
    Yv = d.eq("Y/W", Yw, close(Y / W, 0.200))         # :793
    Xv, Yv = 1 / W**2, Y / W
    th = sp.pi / 4
    T = Yv**2 * sp.sin(th)**2 / (2 * (1 - Xv))
    R = sp.sqrt(T**2 + Yv**2 * sp.cos(th)**2)
    Np = sp.sqrt(1 - Xv / (1 - T + R)).evalf()
    Nm = sp.sqrt(1 - Xv / (1 - T - R)).evalf()
    d.eq("upper sign", sp.Symbol("N_+"), close(Np, 0.778))   # :794
    d.eq("lower sign", sp.Symbol("N_-"), close(Nm, 0.686))   # :795
    # Independent route: numerical roots of the full 3x3 determinant.
    eps = sp.Matrix([[S, -I * D, 0], [I * D, S, 0], [0, 0, P]]).subs({Xw: Xv, Yw: Yv})
    det = sp.expand(wave_matrix(eps, th).det())
    sols = [float(r) for r in sp.Poly(det, N).nroots() if r.is_real and r > 0]
    assert any(abs(x - float(Np)) < 1e-9 for x in sols)
    assert any(abs(x - float(Nm)) < 1e-9 for x in sols)


def test_normalized_landmarks():
    d = Derivation("Normalized landmarks and limits", f"{SRC}:882")
    W, Y, K = sp.symbols("W Y K", positive=True)
    sgn = sp.Symbol("s")
    # Normalize by omega_pe: w = W wpe, wce = Y wpe.
    norm = {w: W * wpe, wce: Y * wpe}
    eps_s = d.eq("normalize", sp.Symbol(r"\epsilon_s"),
                 sp.simplify((1 - wpe**2 / (w * (w + sgn * wce))).subs(norm)))
    for sv in (1, -1):
        roots = sp.solve(eps_s.subs(sgn, sv), W)
        # src/chapters/12-cold-magnetized-waves.typ:884
        stated = (sp.sqrt(Y**2 + 4) - sv * Y) / 2
        root = [r for r in roots if sp.simplify(r - stated) == 0][0]
        d.eq(f"cutoff, s = {sv}", sp.Symbol(f"W_cut{sv:+d}"), root)
    # Upper hybrid, line 886: omega_UH^2 = wpe^2 + wce^2 normalized.
    uh = [r for r in sp.solve((w**2 - wpe**2 - wce**2).subs(norm), W) if r.is_positive]
    check(d.eq("upper hybrid", sp.Symbol("W_UH"), uh[0]), sp.sqrt(1 + Y**2))
    # Ordinary cutoff W = 1 (line 886).
    assert sp.solve((1 - wpe**2 / w**2).subs(norm), W) == [1]
    # Y -> 0: both circular indices become 1 - 1/W^2 (line 899).
    for sv in (1, -1):
        check(eps_s.subs(sgn, sv).subs(Y, 0), 1 - 1 / W**2)
    d.eq("Y = 0", N**2, eps_s.subs(Y, 0))
    # With N = K/W: W^2 = 1 + K^2 (lines 888, 904).
    WW = sp.solve(sp.Eq((K / W)**2, 1 - 1 / W**2), W)
    check(d.eq("N = K/W", W**2, WW[0]**2), 1 + K**2)
    # High frequency: N^2 -> 1 for every branch (line 913).
    NX2 = (1 - (wpe**2 * (w**2 - wpe**2)) / (w**2 * (w**2 - wpe**2 - wce**2))).subs(norm)
    for branch in (eps_s.subs(sgn, 1), eps_s.subs(sgn, -1), NX2, 1 - 1 / W**2):
        assert sp.limit(branch, W, sp.oo) == 1
    d.eq("W -> oo", sp.Limit(N**2, W, sp.oo), 1)


def test_landmark_example():
    d = Derivation("Example: landmarks and classification", f"{SRC}:944")
    Y = 0.30
    d.eq("s = +1", sp.Symbol("W_cut+"), close((sp.sqrt(Y**2 + 4) - Y) / 2, 0.861))  # :953
    d.eq("s = -1", sp.Symbol("W_cut-"), close((sp.sqrt(Y**2 + 4) + Y) / 2, 1.161))  # :954
    d.eq("upper hybrid", sp.Symbol("W_UH"), close(sp.sqrt(1 + Y**2), 1.044))         # :955

    def NO2(W):
        return 1 - 1 / W**2

    def NX2(W):
        return 1 - (W**2 - 1) / (W**2 * (W**2 - 1 - Y**2))

    # W = 0.90: O evanescent, X propagating (lines 956-957).
    assert NO2(0.90) < 0 and NX2(0.90) > 0
    d.eq("W = 0.90", sp.Symbol("N_X"), close(sp.sqrt(NX2(0.90)), 0.403))
    # W = 1.10: O propagating, X evanescent (lines 958-960).
    assert NO2(1.10) > 0 and NX2(1.10) < 0
    d.eq("W = 1.10", sp.Symbol("N_O"), close(sp.sqrt(NO2(1.10)), 0.417))
    # W = 1.30: both propagate (lines 960-962).
    d.eq("W = 1.30", sp.Symbol("N_O"), close(sp.sqrt(NO2(1.30)), 0.639))
    d.eq("W = 1.30", sp.Symbol("N_X"), close(sp.sqrt(NX2(1.30)), 0.565))


Y_PLOT = 0.3  # omega_ce/omega_pe of the plots and the worked example (line 946)


def _normalized(expr, **subs):
    """Lambdify a dielectric expression in W at Y = Y_PLOT (omega_pe cancels)."""
    return sp.lambdify(W_, sp.simplify(expr.subs(NORM).subs(Y_, Y_PLOT).subs(subs)), "numpy")


def plot_magnetized_parallel_dispersion():
    """Parallel circular branches W(K) from N_s^2 = EPS_CIRC, with K = W N_s."""
    import numpy as np

    Y = Y_PLOT
    fig, ax = figure(4.2, 3.0)
    K = np.linspace(0, 3, 50)
    ax.plot(K, K, color=GRAY, ls=":", lw=1.2)
    ax.axhline(Y, color=GRAY, lw=0.8, ls="-.")
    t = np.linspace(0, 1, 400)
    branches = []
    for sv, color, ls in ((1, BLUE, "-"), (-1, ORANGE, "--")):
        N2 = _normalized(EPS_CIRC, s=sv)
        cut = (np.sqrt(Y**2 + 4) - sv * Y) / 2  # tested in test_normalized_landmarks
        W = cut + (3.2 - cut) * t**2  # quadratic sampling resolves the cutoff
        ax.plot(W * np.sqrt(np.clip(N2(W), 0, None)), W, color=color, ls=ls)
        ax.plot([0], [cut], "o", color=color, ms=4, clip_on=False, zorder=3)
        branches.append(cut)
    # s = -1 below the cyclotron resonance W = Y: the whistler branch.
    N2 = _normalized(EPS_CIRC, s=-1)
    W = Y * (1 - np.geomspace(1, 1e-4, 400))
    ax.plot(W * np.sqrt(N2(W)), W, color=ORANGE, ls="--")
    label(ax, 1.0, 1.75, "$s=-1$", ORANGE, ha="right")
    label(ax, 1.6, 1.35, "$s=+1$", BLUE, va="top")
    label(ax, 2.95, Y, "resonance $\\omega=\\omega_{ce}$", GRAY, ha="right")
    label(ax, 2.95, Y * 0.62, "whistler, $s=-1$", ORANGE, ha="right", va="top")
    label(ax, 2.55, 2.3, "vacuum", GRAY, va="top")
    # Cutoffs and the resonance are read off as labelled ticks on the W axis.
    ticks = [0, Y, *branches, 2, 3]
    ax.set(xlim=(0, 3), ylim=(0, 3), xticks=[0, 1, 2, 3], yticks=ticks,
           yticklabels=["0", f"{Y:.1f}", f"{branches[0]:.3f}", f"{branches[1]:.3f}", "2", "3"],
           xlabel=r"$K=kc/\omega_{pe}$ [1]", ylabel=r"$W=\omega/\omega_{pe}$ [1]")
    save(fig, "magnetized-parallel-dispersion")


def plot_magnetized_cutoff_map():
    """Perpendicular N_O^2 and N_X^2 against W: cutoffs, resonance, stop bands."""
    import numpy as np

    Y = Y_PLOT
    NO2, NX2 = _normalized(N_O2), _normalized(N_X2)
    w_uh = np.sqrt(1 + Y**2)  # tested in test_normalized_landmarks
    cuts = [(np.sqrt(Y**2 + 4) - sv * Y) / 2 for sv in (1, -1)]
    fig, ax = figure(4.2, 3.0)
    ax.axhspan(-4, 0, color="#eeeeee", lw=0, zorder=0)
    ax.axhline(0, color="#333333", lw=0.6)
    ax.axvline(w_uh, color=GRAY, lw=0.8, ls="-.")
    W = np.linspace(0.6, 1.8, 600)
    ax.plot(W, NO2(W), color=ORANGE, ls="--")
    for lo, hi in ((0.6, w_uh - 1e-4), (w_uh + 1e-4, 1.8)):
        Wb = np.linspace(lo, hi, 600)
        ax.plot(Wb, NX2(Wb), color=BLUE)
    ax.plot(cuts, [0, 0], "o", color=BLUE, ms=4, zorder=3)
    ax.plot([1], [0], "o", color=ORANGE, ms=4, zorder=3)
    label(ax, 1.79, NX2(1.79) + 0.1, "X", BLUE, ha="right")
    label(ax, 1.79, NO2(1.79) - 0.12, "O", ORANGE, ha="right", va="top")
    label(ax, w_uh + 0.015, 2.85, f"upper-hybrid\nresonance\n$W={w_uh:.3f}$", GRAY, va="top")
    label(ax, 0.62, 1.6, "propagating\n$N^2>0$", GRAY)
    label(ax, 0.62, -3.6, "evanescent, $N^2<0$", GRAY)
    ax.set(xlim=(0.6, 1.8), ylim=(-4, 3), yticks=[-4, -2, 0, 2],
           xticks=[0.6, cuts[0], 1, cuts[1], 1.4, 1.8],
           xticklabels=["0.6", f"{cuts[0]:.3f}", "1", f"{cuts[1]:.3f}", "1.4", "1.8"],
           xlabel=r"$W=\omega/\omega_{pe}$ [1]", ylabel=r"$N^2=(kc/\omega)^2$ [1]")
    save(fig, "magnetized-cutoff-map")


if __name__ == "__main__":
    from si import run_as_script
    run_as_script(globals())
