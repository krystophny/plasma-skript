"""Chapter 9, collisions and conductivity: src/chapters/09-collisions-conductivity.typ.

Run `python derivations/ch09_collisions_conductivity.py` to check every step, or
`pytest derivations` to check every chapter.

Coverage (line in src/chapters/09-collisions-conductivity.typ -> test):
  52-60, 100-128  survival law, lambda = 1/(n sigma), nu = n sigma v, Kn -> test_mean_free_path
  138-153         example: nu, tau, lambda, Kn                     -> test_example_collision_times
  240             momentum-transfer cross section (Rutherford case) -> test_momentum_transfer_cross_section
  252-281         neutral drag R = -m n nu (u_a - u_n) (units)      -> test_neutral_drag
  296-307         example: nu_en = 4.0e6, lambda_en = 2.5e-2       -> test_example_neutral
  398-403, 550    b_90, sigma_90; Rutherford deflection tan(chi/2) = b_90/b
                  and chi ~ 2 b_90/b for b >> b_90 (418, 451)       -> test_rutherford_deflection
  410-411         nu_90 = n sigma_90 v                              -> test_nu90
  419-442, 449-488 Lambda_cut = 32 Lambda, N_D = (4 pi/3) Lambda,
                  annulus integral, <v_e>, scaling T^-3/2            -> test_coulomb_logarithm
  425-427         nu_ei estimate (cited, Inan and Golkowski 2011):
                  units and T_e scaling only                         -> test_coulomb_logarithm
  498-517         example: lambda_D, Lambda, ln Lambda, nu_ei, lambda_ei -> test_example_coulomb
  606-613, 634-653 drag -> eta, sigma_dc                             -> test_spitzer_resistivity
  618-626, 658-664 eta_Sp, density independence, T^-3/2              -> test_spitzer_resistivity
  674-686         example: eta_Sp, sigma_dc                          -> test_example_spitzer
  782-862         harmonic momentum balance, DC and AC tensor         -> test_conductivity_tensor
  868-881         multi-species tensor with omega_p^2, Omega_s         -> test_conductivity_tensor
  897-914         example: Omega_e, sigma_par, sigma_perp, sigma_H     -> test_example_tensor
"""

import sympy as sp
from sympy.physics import units as u

from ch07_multiple_fluids import Tex, close, num
import si
from si import Derivation, e, eps0, k_B, m_e


# Units of this file's symbols. Kept local (not in the shared si.UNITS) so that
# symbols with common names in other chapter files cannot clash.
LOCAL = {}


def check(derived, stated, unit=None, units=None):
    """si.check with this file's LOCAL unit table."""
    return si.check(derived, stated, unit=unit, units={**LOCAL, **(units or {})})

# CODATA 2018 values for the worked examples.
CODATA = {e: 1.602176634e-19, m_e: 9.1093837015e-31, eps0: 8.8541878128e-12}

n, sig, v, L, T = sp.symbols("n sigma v L T_e", positive=True)
ell, b, b90, lamD = sp.symbols("ell b b_90 lambda_D", positive=True)
nu = sp.Symbol("nu", positive=True)
LOCAL.update({n: u.meter**-3, sig: u.meter**2, v: u.meter / u.second, L: u.meter,
              T: u.kelvin, ell: u.meter, b: u.meter, b90: u.meter, lamD: u.meter,
              nu: u.second**-1})


# ---------------------------------------------------------------------------
# Neutral collisions
# ---------------------------------------------------------------------------
def test_mean_free_path():
    d = Derivation("Survival probability and mean free path",
                   "src/chapters/09-collisions-conductivity.typ:105")
    P0 = sp.Function("P_0")
    # dP0 = -n sigma P0 d ell with P0(0) = 1 (lines 105-109).
    sol = sp.dsolve(sp.Eq(P0(ell).diff(ell), -n * sig * P0(ell)), P0(ell), ics={P0(0): 1}).rhs
    d.eq("solve survival ODE", P0(ell), sol)
    check(sol, sp.exp(-n * sig * ell))
    # Mean free path = integral of the survival probability (line 114).
    lam = d.eq("integrate P_0", Tex(r"\lambda"), sp.integrate(sol, (ell, 0, sp.oo)))
    check(lam, 1 / (n * sig), unit=u.meter)
    # d ell = v dt: encounter rate nu = v / lambda (line 119).
    nu_ = d.eq("d ell = v dt", nu, v / lam)
    check(nu_, n * sig * v, unit=u.second**-1)
    check(lam / L, lam / L, unit=u.meter / u.meter)  # Knudsen number


def test_example_collision_times():
    d = Derivation("Example: collision frequency and Knudsen number",
                   "src/chapters/09-collisions-conductivity.typ:138")
    nb, s_, vr, L_ = 1.0e19, 2.0e-19, 1.0e5, 10.0
    nu_ = num(d, "n sigma v", r"\nu_{ab}", nb * s_ * vr)
    close(nu_, "2.0e5")
    close(num(d, "1/nu", r"\tau_{ab}", 1 / nu_), "5.0e-6")
    lam = num(d, "1/(n sigma)", r"\lambda_{ab}", 1 / (nb * s_))
    close(lam, "0.50")
    close(num(d, "lambda/L", r"K_n", lam / L_), "0.050")


def test_neutral_drag():
    d = Derivation("Drag on stationary neutrals", "src/chapters/09-collisions-conductivity.typ:281")
    ua = sp.Symbol("u_a", real=True)
    # Momentum lost per encounter ~ m u_a; encounters per volume and time ~ n nu.
    R = d.eq("m u per encounter, n nu encounters", Tex("R_{an}"), -m_e * n * nu * ua)
    check(R, -m_e * n * nu * ua, unit=u.newton / u.meter**3, units={ua: u.meter / u.second})


def test_example_neutral():
    d = Derivation("Example: electron-neutral collisions", "src/chapters/09-collisions-conductivity.typ:296")
    nn, s_, ve = 2.0e20, 2.0e-19, 1.0e5
    nu_ = num(d, "n sigma v", r"\nu_{en}", nn * s_ * ve)
    close(nu_, "4.0e6")
    close(num(d, "v / nu", r"\lambda_{en}", ve / nu_), "2.5e-2")


# ---------------------------------------------------------------------------
# Coulomb collisions
# ---------------------------------------------------------------------------
def test_rutherford_deflection():
    d = Derivation("Rutherford deflection and b_90", "src/chapters/09-collisions-conductivity.typ:400")
    qa, qb, mr = sp.symbols("q_a q_b m_r", positive=True)
    w = sp.Symbol("w", positive=True)  # inverse radius 1/r
    # Strong-deflection scale: Coulomb energy at b equals ... define b90 (line 400).
    b90_def = qa * qb / (4 * sp.pi * eps0 * mr * v**2)
    check(b90_def, b90_def, unit=u.meter, units={qa: u.coulomb, qb: u.coulomb, mr: u.kilogram})
    # Attractive orbit: energy and angular momentum give
    # dtheta/dw = b / sqrt(1 + 2 b90 w - b^2 w^2), w = 1/r.
    integrand = b / sp.sqrt(1 + 2 * b90 * w - b**2 * w**2)
    F = sp.asin((b**2 * w - b90) / sp.sqrt(b**2 + b90**2))
    check(sp.diff(F, w), integrand)  # antiderivative
    w_max = sp.solve(sp.Eq(1 + 2 * b90 * w - b**2 * w**2, 0), w)
    w_max = [s for s in w_max if s.is_positive is not False][-1]
    theta0 = sp.simplify(F.subs(w, w_max) - F.subs(w, 0))
    d.eq("orbit integral", Tex(r"\theta_0"), theta0)
    # Deflection angle chi = 2 theta0 - pi in magnitude: tan(chi/2) = b90/b.
    chi = 2 * theta0 - sp.pi
    check(sp.simplify(sp.tan(chi / 2)), b90 / b)
    d.eq("chi = 2 theta_0 - pi", Tex(r"\tan\frac{\chi}{2}"), b90 / b)
    check(sp.simplify(chi.subs(b, b90)), sp.pi / 2)  # ninety degrees at b = b90
    # Small-angle limit chi ~ 2 b90 / b (line 419).
    eps_ = sp.Symbol("epsilon", positive=True)
    check(sp.series(chi.subs(b90, eps_ * b), eps_, 0, 2).removeO(), 2 * eps_)
    # Impulse approximation: Delta p_perp = int F_perp dt along a straight line (line 451).
    tt = sp.Symbol("t", real=True)
    K = qa * qb / (4 * sp.pi * eps0)
    dp = sp.integrate(K * b / (b**2 + v**2 * tt**2) ** sp.Rational(3, 2), (tt, -sp.oo, sp.oo))
    chi_small = d.eq("impulse approximation", Tex(r"\chi"), sp.simplify(dp / (mr * v)))
    check(chi_small, 2 * b90_def / b)
    # Electron on a heavy ion: q_a = q_b = e, m_r = m_e (line 402).
    check(b90_def.subs({qa: e, qb: e, mr: m_e}), e**2 / (4 * sp.pi * eps0 * m_e * v**2), unit=u.meter)


def test_nu90():
    d = Derivation("Large-angle collision rate", "src/chapters/09-collisions-conductivity.typ:410")
    b90e = e**2 / (4 * sp.pi * eps0 * m_e * v**2)
    nu90 = d.eq("n sigma_90 v", Tex(r"\nu_{90}"), n * sp.pi * b90e**2 * v)
    check(nu90, n * e**4 / (16 * sp.pi * eps0**2 * m_e**2 * v**3), unit=u.second**-1)


def test_momentum_transfer_cross_section():
    d = Derivation("Momentum-transfer cross section for Coulomb scattering",
                   "src/chapters/09-collisions-conductivity.typ:240")
    bmax = sp.Symbol("b_max", positive=True)
    # 1 - cos chi = 2 sin^2(chi/2) with tan(chi/2) = b90/b.
    one_minus_cos = sp.simplify(2 * sp.sin(sp.atan(b90 / b)) ** 2)
    check(one_minus_cos, 2 * b90**2 / (b**2 + b90**2))
    # sigma_mt = int (1 - cos chi) dsigma, dsigma = 2 pi b db, screened at b_max.
    s_mt = d.eq("int (1 - cos chi) 2 pi b db", Tex(r"\sigma_{mt}"),
                sp.integrate(2 * sp.pi * b * one_minus_cos, (b, 0, bmax)))
    check(s_mt, 2 * sp.pi * b90**2 * sp.log(1 + bmax**2 / b90**2))
    # Leading log: 4 pi b90^2 ln(b_max / b90) for b_max >> b90.
    lead = sp.limit(s_mt - 4 * sp.pi * b90**2 * sp.log(bmax / b90), bmax, sp.oo)
    check(lead, 0)
    d.eq("b_max much larger than b_90", Tex(r"\sigma_{mt}"), 4 * sp.pi * b90**2 * sp.log(lamD / b90))


def test_coulomb_logarithm():
    d = Derivation("Coulomb logarithm and plasma parameter", "src/chapters/09-collisions-conductivity.typ:433")
    vx = sp.Symbol("v", positive=True)
    # Maxwellian mean speed (line 474): <v> = int v f d^3v / n.
    a2 = k_B * T / m_e
    fM = (2 * sp.pi * a2) ** sp.Rational(-3, 2) * sp.exp(-vx**2 / (2 * a2))
    vmean = d.eq("Maxwellian average", Tex(r"\langle v_e\rangle"),
                 sp.simplify(sp.integrate(4 * sp.pi * vx**3 * fM, (vx, 0, sp.oo))))
    check(vmean, sp.sqrt(8 * k_B * T / (sp.pi * m_e)), unit=u.meter / u.second)
    # Lambda_cut = lambda_D / b90(<v>) = 32 Lambda with Lambda = n lambda_D^3 (line 434).
    lam_D = sp.sqrt(eps0 * k_B * T / (n * e**2))
    b90v = e**2 / (4 * sp.pi * eps0 * m_e * vmean**2)
    Lcut = d.eq("lambda_D / b_90", Tex(r"\Lambda_{\mathrm{cut}}"), sp.simplify(lam_D / b90v))
    check(Lcut, 32 * n * lam_D**3)
    check(n * lam_D**3, n * lam_D**3, unit=u.meter / u.meter)
    # Debye-sphere count N_D = n (4 pi/3) lambda_D^3 = (4 pi/3) Lambda (line 442).
    check(n * sp.Rational(4, 3) * sp.pi * lam_D**3, sp.Rational(4, 3) * sp.pi * (n * lam_D**3))
    # Annulus sum (line 461): n v 2 pi b db (v chi)^2 with chi = 2 b90/b.
    rate = sp.integrate(n * v * 2 * sp.pi * b * v**2 * (2 * b90 / b) ** 2, (b, b90, lamD))
    d.eq("sum over annuli", Tex(r"\frac{d\langle\Delta v_\perp^2\rangle}{dt}"), rate)
    check(rate, 8 * sp.pi * n * v**3 * b90**2 * sp.log(lamD / b90))
    # Cited estimate (line 425): unit s^-1 and scaling T^-3/2 at fixed ln Lambda.
    lnL = Tex(r"\ln\Lambda", positive=True)
    wpe2 = n * e**2 / (eps0 * m_e)
    nu_ei = sp.sqrt(2) * wpe2**2 / (64 * sp.pi * n) * (k_B * T / m_e) ** sp.Rational(-3, 2) * lnL
    check(nu_ei, nu_ei, unit=u.second**-1, units={lnL: sp.S.One})
    check(sp.simplify(T * sp.diff(nu_ei, T) / nu_ei), sp.Rational(-3, 2))


def nu_ei_num(ne, kT, lnL):
    """Cited electron-ion rate (line 425) with CODATA constants."""
    wpe2 = ne * CODATA[e] ** 2 / (CODATA[eps0] * CODATA[m_e])
    return 2**0.5 * wpe2**2 / (64 * 3.141592653589793 * ne) * (kT / CODATA[m_e]) ** -1.5 * lnL


def test_example_coulomb():
    d = Derivation("Example: Coulomb collisions at 10 eV", "src/chapters/09-collisions-conductivity.typ:498")
    import math
    ne, kT = 1.0e16, 1.602e-18
    lam = num(d, "Debye length", r"\lambda_D", (CODATA[eps0] * kT / (ne * CODATA[e] ** 2)) ** 0.5)
    Lam = num(d, "n lambda_D cubed", r"\Lambda", ne * lam**3)
    lnL = num(d, "log", r"\ln\Lambda", math.log(Lam))
    nu_ = num(d, "cited rate", r"\nu_{ei}", nu_ei_num(ne, kT, lnL))
    vm = num(d, "mean speed", r"\langle v_e\rangle", (8 * kT / (math.pi * CODATA[m_e])) ** 0.5)
    close(lam, "2.35e-4")
    close(Lam, "1.30e5")
    close(lnL, "11.8")
    close(nu_, "3.60e3")
    close(vm, "2.12e6")
    # Mean free path from the printed <v_e> and nu_ei.
    close(num(d, "mean speed / nu_ei", r"\lambda_{ei}", 2.12e6 / 3.60e3), "5.89e2")
    close(vm / nu_, "5.89e2", slack=2e-3)


# ---------------------------------------------------------------------------
# Resistivity and the conductivity tensor
# ---------------------------------------------------------------------------
def test_spitzer_resistivity():
    d = Derivation("Spitzer resistivity", "src/chapters/09-collisions-conductivity.typ:662")
    j, ui, ue = sp.symbols("j u_i u_e", real=True)
    # R_ei / (e n) with u_i - u_e = j / (e n) (lines 634-644).
    R = m_e * n * nu * (ui - ue)
    eta = d.eq("R_ei / (e n j)", Tex(r"\eta"), sp.simplify((R / (e * n)).subs(ui, ue + j / (e * n)) / j))
    check(eta, m_e * nu / (n * e**2), unit=u.ohm * u.meter)
    check(1 / eta, n * e**2 / (m_e * nu), unit=u.siemens / u.meter)
    # Insert the cited nu_ei (line 618) to obtain eta_Sp (line 620).
    lnL = Tex(r"\ln\Lambda", positive=True)
    wpe2 = n * e**2 / (eps0 * m_e)
    nu_ei = sp.sqrt(2) * wpe2**2 / (64 * sp.pi * n) * (k_B * T / m_e) ** sp.Rational(-3, 2) * lnL
    eta_sp = d.eq("insert nu_ei", Tex(r"\eta_{Sp}"), sp.simplify(eta.subs(nu, nu_ei)))
    stated = (sp.pi / (2 * sp.sqrt(2)) * e**2 * sp.sqrt(m_e)
              / ((4 * sp.pi * eps0) ** 2 * (k_B * T) ** sp.Rational(3, 2)) * lnL)
    check(eta_sp, stated, unit=u.ohm * u.meter, units={lnL: sp.S.One})
    # Independent of density at fixed ln Lambda; scales as T^-3/2.
    check(sp.diff(stated, n), 0)
    check(sp.simplify(T * sp.diff(stated, T) / stated), sp.Rational(-3, 2))


def test_example_spitzer():
    d = Derivation("Example: Spitzer resistivity", "src/chapters/09-collisions-conductivity.typ:674")
    eta = num(d, "m_e nu / (n e2)", r"\eta_{Sp}", CODATA[m_e] * 3.60e3 / (1.0e16 * CODATA[e] ** 2))
    close(eta, "1.28e-5")
    close(num(d, "1 / eta", r"\sigma_{dc}", 1 / eta), "7.83e4")


def test_conductivity_tensor():
    d = Derivation("Conductivity tensor", "src/chapters/09-collisions-conductivity.typ:853")
    q, w = sp.symbols("q_s omega", real=True)
    m = sp.Symbol("m_s", positive=True)
    B0 = sp.Symbol("B_0", positive=True)
    Ex, Ey, Ez = sp.symbols("E_x E_y E_z")
    ux, uy, uz = sp.symbols("u_x u_y u_z")
    a = nu - sp.I * w
    # Harmonic momentum balance m a u = q (E + u x B0 z) (line 782).
    eqs = [m * a * ux - q * (Ex + uy * B0), m * a * uy - q * (Ey - ux * B0), m * a * uz - q * Ez]
    sol = sp.solve(eqs, [ux, uy, uz], dict=True)[0]
    J = [sp.simplify(n * q * sol[c]) for c in (ux, uy, uz)]
    Om = q * B0 / m
    s_perp = n * q**2 * a / (m * (a**2 + Om**2))
    s_H = n * q**2 * Om / (m * (a**2 + Om**2))
    s_par = n * q**2 / (m * a)
    # Tensor form (line 805) with the AC entries (lines 853-860).
    check(J[0], s_perp * Ex + s_H * Ey)
    check(J[1], -s_H * Ex + s_perp * Ey)
    check(J[2], s_par * Ez)
    d.eq("solve for j_x", Tex("J_x"), Tex(r"\sigma_\perp E_x + \sigma_H E_y"))
    d.eq("AC entry", Tex(r"\sigma_\perp"), s_perp)
    d.eq("AC entry", Tex(r"\sigma_H"), s_H)
    # Component equations (line 799/843): J_x = sigma0 E_x + (Omega/a) J_y, etc.
    sig0 = n * q**2 / (m * a)
    check(J[0], sig0 * Ex + Om / a * J[1])
    check(J[1], sig0 * Ey - Om / a * J[0])
    # DC limit omega = 0 (lines 812-815).
    sdc = n * q**2 / (m * nu)
    check(s_perp.subs(w, 0), sdc * nu**2 / (nu**2 + Om**2))
    check(s_H.subs(w, 0), sdc * nu * Om / (nu**2 + Om**2))
    check(s_par.subs(w, 0), sdc, unit=u.siemens / u.meter,
          units={q: u.coulomb, m: u.kilogram})
    # Plasma-frequency form (lines 868-881): eps0 omega_p^2 = n q^2 / m.
    wp2 = n * q**2 / (eps0 * m)
    check(eps0 * wp2 / a, s_par)
    check(eps0 * wp2 * a / (a**2 + Om**2), s_perp)
    check(eps0 * wp2 * Om / (a**2 + Om**2), s_H)


def test_example_tensor():
    d = Derivation("Example: magnetized DC conductivity", "src/chapters/09-collisions-conductivity.typ:897")
    ne, nu_, B0 = 1.0e16, 2.5e3, 0.010
    qe, me = -CODATA[e], CODATA[m_e]
    Om = num(d, "q_e B_0 / m_e", r"\Omega_e", qe * B0 / me)
    sdc = num(d, "n q2 / (m nu)", r"\sigma_\parallel", ne * qe**2 / (me * nu_))
    sp_ = num(d, "Pedersen", r"\sigma_\perp", sdc * nu_**2 / (nu_**2 + Om**2))
    sH = num(d, "Hall", r"\sigma_H", sdc * nu_ * Om / (nu_**2 + Om**2))
    close(Om, "-1.76e9")
    close(sdc, "1.13e5")
    close(sp_, "2.28e-7")
    close(sH, "-0.160")


if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
