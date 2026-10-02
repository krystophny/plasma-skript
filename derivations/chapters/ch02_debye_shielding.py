"""Chapter 2, Debye shielding: src/chapters/02-debye-shielding.typ.

Coverage (Typst label or line -> test):
  <debye-charge-separation-scale> l.43-45, 59-79 -> test_charge_separation_scale
  <debye-boltzmann-response>      l.96, 137-141  -> test_boltzmann_response
  <debye-charge-response>         l.106, 145     -> test_boltzmann_response
  <debye-poisson>                 l.115          -> test_poisson_unit
  <debye-screened-equation>       l.124, 150-154 -> test_debye_length
  phi ~ exp(-r/lambda_D)/r        l.158          -> test_screened_potential
  rho_Q                           l.170, 223     -> test_sphere_bare_potential
  <debye-sphere-potential-inside>/-outside l.182-186, 227-238
                                                 -> test_sphere_bare_potential
  finite-source Debye-Hueckel     l.203-205, 253-275 -> test_matched_finite_source
  small-source condition          l.213          -> test_small_source_condition
  <intro-debye-number>            l.356          -> test_debye_number_and_coupling
  Gamma_s, a_s                    l.367-368      -> test_debye_number_and_coupling
  lambda_D = L and N_D = 1 lines  (figure)       -> test_regime_lines, plot_nt_map

Run `python derivations/ch02_debye_shielding.py` to print the steps, or
`pytest derivations` to check every chapter.
"""

import sympy as sp
from sympy.physics import units as u

from si import UNITS, Derivation, check, e, eps0, k_B

R, N, kap, s_ = sp.symbols("R N kappa s", positive=True)
LOCAL = {R: u.meter, N: u.meter**-3, kap: u.meter**-1}

n0, T_e, Q, r, phi = sp.symbols("n_0 T_e Q r phi", positive=True)
UNITS.update({n0: u.meter**-3, T_e: u.kelvin, Q: u.coulomb, r: u.meter})
rho_s, lam_s = sp.symbols("rho_q lambda_D", positive=True)
UNITS[lam_s] = u.meter
Phi = sp.Function("phi")

# Results as printed in the script. The tests derive and check them; the
# plot_* functions below evaluate exactly these expressions.
LAMBDA_D = sp.sqrt(eps0 * k_B * T_e / (n0 * e**2))  # :124, :150
N_DEBYE = sp.Rational(4, 3) * sp.pi * n0 * lam_s**3  # :356, with lambda_D symbolic
PHI_BARE_IN = Q / (8 * sp.pi * eps0 * R) * (3 - r**2 / R**2)  # :182, :238
PHI_BARE_OUT = Q / (4 * sp.pi * eps0 * r)  # :186
xs, pp = sp.Symbol("x", positive=True), sp.Symbol("phi_p")
PHI_P = 3 * Q / (4 * sp.pi * eps0 * kap**2 * R**3)  # :255
A_MATCH = -(R * pp * (xs + 1) * sp.exp(-xs)) / xs  # :271
B_MATCH = (R * pp) / (2 * xs) * (sp.exp(xs) * (xs - 1) + (xs + 1) * sp.exp(-xs))  # :275


def test_debye_length():
    d = Derivation("Debye length", "src/chapters/02-debye-shielding.typ:124")
    # Boltzmann electrons, immobile ions: rho = e n0 (1 - exp(e phi / k_B T_e)).
    rho = d.eq("Boltzmann", rho_s, e * n0 * (1 - sp.exp(e * phi / (k_B * T_e))))
    # Linearize for e phi << k_B T_e.
    rho_lin = d.eq("linearize", rho_s, sp.series(rho, phi, 0, 2).removeO())
    # Poisson: laplacian(phi) = -rho/eps0 = phi / lambda_D^2.
    inv_lambda_sq = d.eq("Poisson", lam_s**-2, sp.simplify(-rho_lin / eps0 / phi))
    lambda_D = d.eq("solve", lam_s, sp.sqrt(1 / inv_lambda_sq))
    check(lambda_D, LAMBDA_D, unit=u.meter)


def test_screened_potential():
    d = Derivation("Screened point-charge potential", "src/chapters/02-debye-shielding.typ:158")
    # Spherical Debye-Hueckel equation: (1/r^2) d/dr(r^2 dphi/dr) = phi/lambda^2.
    stated = Q / (4 * sp.pi * eps0 * r) * sp.exp(-r / lam_s)
    d.step("Debye-Hueckel", sp.Eq(sp.diff(r**2 * Phi(r).diff(r), r) / r**2, Phi(r) / lam_s**2))
    d.eq("trial", Phi(r), stated)
    lhs = d.eq("insert", sp.Symbol("LHS"), sp.simplify(sp.diff(r**2 * sp.diff(stated, r), r) / r**2))
    assert sp.simplify(lhs - stated / lam_s**2) == 0
    # Bare Coulomb potential for r << lambda_D.
    near = d.eq("near source", Phi(r), sp.limit(stated * r, r, 0) / r)
    check(near, Q / (4 * sp.pi * eps0 * r), unit=u.volt)


def test_charge_separation_scale():
    d = Derivation("Charge-separation scale", "src/chapters/02-debye-shielding.typ:43")
    # Enclosed charge of a uniformly charged sphere.
    Q_enc = d.eq("enclosed charge", sp.Symbol("Q(r)"), sp.integrate(4 * sp.pi * s_**2 * N * e, (s_, 0, r)))
    check(Q_enc, sp.Rational(4, 3) * sp.pi * N * e * r**3)  # :59
    # Gauss: E 4 pi r^2 = Q(r)/eps0.
    E = d.eq("Gauss", sp.Symbol("E(r)"), Q_enc / (eps0 * 4 * sp.pi * r**2))
    check(E, N * e * r / (3 * eps0), unit=u.volt / u.meter, units=LOCAL)  # :67
    # Boundary potential relative to infinity (exterior is Coulomb).
    phi_R = d.eq("integrate E", Phi(R),
                 sp.integrate(Q_enc.subs(r, R) / (4 * sp.pi * eps0 * s_**2), (s_, R, sp.oo)))
    stated_phi = N * e * R**2 / (3 * eps0)  # :43, :73
    check(phi_R, stated_phi, unit=u.volt, units=LOCAL)
    # Balance e phi(R) = k_B T_e and solve for R.
    R_sol = d.eq("potential = thermal energy", R, sp.solve(sp.Eq(e * stated_phi, k_B * T_e), R)[0])
    stated_R = sp.sqrt(3 * eps0 * k_B * T_e / (N * e**2))  # :45
    check(R_sol, stated_R, unit=u.meter, units=LOCAL)
    # With N = n0 the scale is sqrt(3) lambda_D.
    lam = sp.sqrt(eps0 * k_B * T_e / (n0 * e**2))
    ratio = d.eq("N equals n0", R / lam_s, sp.simplify(stated_R.subs(N, n0) / lam))
    check(ratio, sp.sqrt(3))  # :79


def test_boltzmann_response():
    d = Derivation("Boltzmann response", "src/chapters/02-debye-shielding.typ:96")
    n_e = sp.Symbol("n_e")
    # Electron energy -e phi in the Boltzmann factor exp(-W/k_B T_e).
    ne = d.eq("Boltzmann", n_e, n0 * sp.exp(-(-e * phi) / (k_B * T_e)))
    check(ne, n0 * sp.exp(e * phi / (k_B * T_e)))  # :96, :137
    lin = d.eq("linearize", n_e, sp.series(ne, phi, 0, 2).removeO())
    check(lin, n0 * (1 + e * phi / (k_B * T_e)), unit=u.meter**-3, units={phi: u.volt})  # :141
    # Immobile ions n_i = n0: rho = e n_i - e n_e.
    rho = d.eq("ions minus electrons", rho_s, sp.expand(e * n0 - e * lin))
    check(rho, -(e**2 * n0) / (k_B * T_e) * phi,  # :106, :145
          unit=u.coulomb / u.meter**3, units={phi: u.volt})


def test_poisson_unit():
    d = Derivation("Poisson equation units", "src/chapters/02-debye-shielding.typ:115")
    rhs = d.eq("Poisson", sp.Symbol(r"\nabla^{2}\phi"), -rho_s / eps0)
    check(rhs, rhs, unit=u.volt / u.meter**2, units={rho_s: u.coulomb / u.meter**3})


def _sphere_charge(Q):
    # Uniform source density of total charge Q in radius R.
    return Q / (sp.Rational(4, 3) * sp.pi * R**3)


def test_sphere_bare_potential():
    d = Derivation("Bare potential of a uniform sphere", "src/chapters/02-debye-shielding.typ:182")
    rhoQ = d.eq("charge density", sp.Symbol("rho_Q"), _sphere_charge(Q))
    check(rhoQ, 3 * Q / (4 * sp.pi * R**3), unit=u.coulomb / u.meter**3, units=LOCAL)  # :170
    Q_in = d.eq("enclosed charge", sp.Symbol("Q_enc"), sp.integrate(4 * sp.pi * s_**2 * rhoQ, (s_, 0, r)))
    check(Q_in, Q * r**3 / R**3)  # :223
    E_in = d.eq("Gauss inside", sp.Symbol("E_C"), Q_in / (4 * sp.pi * eps0 * r**2))
    check(E_in, Q * r / (4 * sp.pi * eps0 * R**3))  # :227
    E_out = d.eq("Gauss outside", sp.Symbol("E_C"), Q / (4 * sp.pi * eps0 * r**2))  # :232
    # phi(r) = integral_r^oo E dr', split at R.
    phi_out = d.eq("integrate outside", Phi(r), sp.integrate(E_out.subs(r, s_), (s_, r, sp.oo)))
    phi_in = d.eq("integrate inside", Phi(r),
                  sp.factor(phi_out.subs(r, R) + sp.integrate(E_in.subs(r, s_), (s_, r, R))))
    stated_in, stated_out = PHI_BARE_IN, PHI_BARE_OUT
    check(phi_in, stated_in, unit=u.volt, units=LOCAL)
    check(phi_out, stated_out, unit=u.volt)
    # Poisson inside: (1/r^2)(r^2 phi')' = -rho_Q/eps0.
    lap = d.eq("Poisson check", sp.Symbol(r"\nabla^{2}\phi"),
               sp.simplify(sp.diff(r**2 * sp.diff(stated_in, r), r) / r**2))
    check(lap, -rhoQ / eps0)
    # Continuity of potential and field at r = R.
    check(stated_in.subs(r, R), stated_out.subs(r, R))
    check(sp.diff(stated_in, r).subs(r, R), sp.diff(stated_out, r).subs(r, R))


def test_matched_finite_source():
    d = Derivation("Matched finite-source Debye response", "src/chapters/02-debye-shielding.typ:253")
    rhoQ = _sphere_charge(Q)
    A, B = sp.symbols("A B")
    x = kap * R
    # Particular solution: -phi_p kappa^2 = -rho_Q/eps0.
    phi_p = d.eq("particular", sp.Symbol("phi_p"), rhoQ / (eps0 * kap**2))
    check(phi_p, PHI_P, unit=u.volt, units=LOCAL)  # :255
    phi_in = d.eq("regular inside", sp.Symbol("phi_in"), pp + A * sp.sinh(kap * r) / r)  # :253
    phi_out = d.eq("decaying outside", sp.Symbol("phi_out"), B * sp.exp(-kap * r) / r)  # :258
    # Both satisfy the screened Poisson equation in their region.  # :203-205
    L = lambda f: sp.diff(r**2 * sp.diff(f, r), r) / r**2 - kap**2 * f
    check(L(phi_in.subs(pp, phi_p)), -rhoQ / eps0)
    check(L(phi_out), 0)
    # Match potential and slope at r = R.  # :263-267
    sol = sp.solve([(phi_in - phi_out).subs(r, R),
                    sp.diff(phi_in - phi_out, r).subs(r, R)], [A, B], dict=True)[0]
    nice = lambda ex: sp.simplify(ex.rewrite(sp.exp).subs(kap, xs / R))
    sA = d.eq("match", A, nice(sol[A]))
    sB = d.eq("match", B, nice(sol[B]))
    stated_A, stated_B = A_MATCH, B_MATCH
    check(sA, stated_A)
    check(sB, stated_B)
    sB_full = stated_B.subs({pp: phi_p, xs: x})
    check(sB_full, sB_full, unit=u.volt * u.meter, units=LOCAL)
    # Point-source limit R -> 0 gives B -> Q/(4 pi eps0): the screened Coulomb law.
    lim = d.eq("point-source limit", B, sp.limit(sB_full, R, 0))
    check(lim, Q / (4 * sp.pi * eps0))


def test_small_source_condition():
    d = Derivation("Small-source condition", "src/chapters/02-debye-shielding.typ:213")
    # Maximum bare potential at the centre, phi_C(0) = 3Q/(8 pi eps0 R).
    phi_max = d.eq("centre", Phi(0), (Q / (8 * sp.pi * eps0 * R) * (3 - r**2 / R**2)).subs(r, 0))
    ratio = d.eq("over k_B T_e", e * sp.Symbol("phi_max") / (k_B * T_e), e * phi_max / (k_B * T_e))
    stated = 3 * e * Q / (8 * sp.pi * eps0 * R * k_B * T_e)  # :213
    check(ratio, stated, unit=u.meter / u.meter, units=LOCAL)


def test_debye_number_and_coupling():
    d = Derivation("Debye number and coupling", "src/chapters/02-debye-shielding.typ:356")
    lam = LAMBDA_D
    # Number of electrons in a Debye sphere.
    N_D = d.eq("count in Debye sphere", sp.Symbol("N_D"),
               sp.integrate(4 * sp.pi * s_**2 * n0, (s_, 0, lam_s)))
    check(N_D, N_DEBYE, unit=u.meter / u.meter)  # :356
    # Mean spacing: one particle per sphere of radius a_s, (4 pi/3) a^3 n = 1.
    a = sp.symbols("a", positive=True)
    a_sol = d.eq("one particle per sphere", a,
                 sp.solve(sp.Eq(sp.Rational(4, 3) * sp.pi * a**3 * n0, 1), a)[0])
    check(a_sol, (3 / (4 * sp.pi * n0)) ** sp.Rational(1, 3), unit=u.meter)  # :368
    # Coupling: Coulomb energy at spacing a over thermal energy.
    Gamma = d.eq("Coulomb over thermal", sp.Symbol("Gamma"),
                 e**2 / (4 * sp.pi * eps0 * a_sol * k_B * T_e))  # :367
    check(Gamma, Gamma, unit=u.meter / u.meter)
    # Weak coupling and a large Debye number are linked: Gamma * N_D^(2/3) is a pure number.
    ratio = d.eq("link", sp.Symbol("Gamma") * sp.Symbol("N_D") ** sp.Rational(2, 3),
                 sp.simplify(Gamma * N_D.subs(lam_s, lam) ** sp.Rational(2, 3)))
    assert ratio.free_symbols == set(), ratio



# --- n-T regime lines -------------------------------------------------------
L_sys, T_eV = sp.symbols("L T_eV", positive=True)


def _temperature_ev(condition):
    """Solve condition(T_e) = 0 for T_e and express k_B T_e in eV."""
    T_sol = sp.solve(condition, T_e)[0]
    return sp.simplify(k_B * T_sol / e)


def test_regime_lines():
    d = Derivation("Regime lines in the n-T plane", "src/chapters/02-debye-shielding.typ:356")
    # lambda_D = L: the system size equals the screening length.
    T_L = d.eq(r"\lambda_D = L", T_eV, _temperature_ev(LAMBDA_D**2 - L_sys**2))
    check(T_L, e * n0 * L_sys**2 / eps0, unit=u.volt, units={L_sys: u.meter})
    # N_D = 1: one electron per Debye sphere, the edge of the collective regime.
    T_1 = d.eq("N_D = 1", T_eV, _temperature_ev(N_DEBYE.subs(lam_s, LAMBDA_D) - 1))
    check(T_1, e / eps0 * (3 / (4 * sp.pi)) ** sp.Rational(2, 3) * n0 ** sp.Rational(1, 3),
          unit=u.volt)


# --- Plots ------------------------------------------------------------------


def _numeric(expr, *args):
    """lambdify expr in args with SI constants substituted."""
    from si import SI_VALUES

    return sp.lambdify(args, expr.subs(SI_VALUES), "numpy")


def plot_debye_potential():
    """Bare and Debye-screened potential of the uniform sphere, R = lambda_D/2."""
    import numpy as np

    from si import BLUE, ORANGE, figure, label, save

    # Units: r in lambda_D (kappa = 1), phi in Q/(4 pi eps0 lambda_D).
    norm = {Q: 1, eps0: 1 / (4 * sp.pi), kap: 1}
    a = sp.Rational(1, 2)
    phi_p = PHI_P.subs(norm).subs(R, a)
    A = A_MATCH.subs({pp: phi_p, xs: a, R: a})
    B = B_MATCH.subs({pp: phi_p, xs: a, R: a})
    bare = sp.Piecewise((PHI_BARE_IN.subs(norm).subs(R, a), r <= a),
                        (PHI_BARE_OUT.subs(norm), True))
    screened = sp.Piecewise((phi_p + A * sp.sinh(r) / r, r <= a),
                            (B * sp.exp(-r) / r, True))
    x = np.linspace(1e-6, 4, 400)
    f_bare, f_scr = (sp.lambdify(r, ex, "numpy") for ex in (bare, screened))
    fig, ax = figure(3.4, 2.8)
    ax.plot(x, f_bare(x), color=ORANGE, ls="--")
    ax.plot(x, f_scr(x), color=BLUE)
    ax.axvline(float(a), color="0.8", lw=0.6, zorder=0)
    ax.text(float(a), 3.2, r"$R$", ha="center", va="bottom", color="0.4")
    label(ax, 2.8, f_bare(2.8) + 0.08, "bare", ORANGE)
    label(ax, 1.6, f_scr(1.6) + 0.08, "screened", BLUE)
    ax.set(xlim=(0, 4), ylim=(0, 3.2),
           xlabel=r"$r/\lambda_D$", ylabel=r"$4\pi\varepsilon_0\lambda_D\,\phi/Q$")
    save(fig, "debye_potential")


def _nt_axes():
    from si import figure, log_ticks

    fig, ax = figure(5.0, 3.0)
    ax.set(xscale="log", yscale="log", xlim=(1e6, 1e32), ylim=(1e-2, 1e5),
           xlabel=r"$n_e\ [\mathrm{m^{-3}}]$", ylabel=r"$k_B T_e\ [\mathrm{eV}]$")
    log_ticks(ax.xaxis, 6, 32, 4)
    log_ticks(ax.yaxis, -2, 5)
    ax.grid(True, color="0.9", lw=0.5)
    return fig, ax


def _along(ax, x, slope, text, f, color):
    """Label a power law T = f(n) of log-slope `slope` along the line, just above it."""
    import numpy as np

    fig = ax.figure
    fig.canvas.draw()
    p0 = ax.transData.transform((x, f(x)))
    p1 = ax.transData.transform((10 * x, f(10 * x)))
    ang = np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))
    off = 5 * np.array([-np.sin(np.radians(ang)), np.cos(np.radians(ang))])
    ax.annotate(text, (x, f(x)), xytext=off, textcoords="offset points",
                rotation=ang, rotation_mode="anchor", color=color, ha="center",
                va="bottom")


def plot_nt_plane():
    """Empty n-T plane, the canvas of the lecture-1 regime map."""
    from si import save

    fig, _ = _nt_axes()
    save(fig, "nt_plane")


def plot_nt_map():
    """Debye-length lines, the N_D = 1 boundary and five example plasmas."""
    import numpy as np

    from si import BLUE, EXAMPLE_PLASMAS, GRAY, ORANGE, save

    T_L = _numeric(_temperature_ev(LAMBDA_D**2 - L_sys**2), n0, L_sys)
    T_1 = _numeric(_temperature_ev(N_DEBYE.subs(lam_s, LAMBDA_D) - 1), n0)
    fig, ax = _nt_axes()
    n = np.logspace(6, 32, 300)
    for L, text, at in [(1e-6, r"$\lambda_D = 1\,\mu\mathrm{m}$", 3e22),
                        (1e-2, r"$\lambda_D = 1\,\mathrm{cm}$", 3e14),
                        (1e2, r"$\lambda_D = 100\,\mathrm{m}$", 5e7)]:
        ax.plot(n, T_L(n, L), color=GRAY, ls="--", lw=0.9)
        _along(ax, at, 1, text, lambda x, L=L: T_L(x, L), GRAY)
    ax.plot(n, T_1(n), color=ORANGE)
    ax.fill_between(n, 1e-3, T_1(n), color=ORANGE, alpha=0.10, lw=0)
    _along(ax, 3e29, 1 / 3, r"$N_D = 1$", T_1, ORANGE)
    ax.text(3e27, 2e-2, r"$N_D < 1$", color=ORANGE, va="bottom")
    for name, (ne, T) in EXAMPLE_PLASMAS.items():
        ax.plot(ne, T, "o", ms=5, color=BLUE)
        ax.annotate(name, (ne, T), xytext=(5, 0), textcoords="offset points",
                    va="center", color="#1c1f23")
    save(fig, "nt_map")


def plot_debye_number():
    """N_D(n_e) at three temperatures; N_D >> 1 holds except at high n and low T."""
    import numpy as np

    from si import BLUE, GRAY, ORANGE, figure, label, log_ticks, save

    N_of = _numeric(N_DEBYE.subs(lam_s, LAMBDA_D), n0, T_e)
    kelvin = _kelvin_per_ev()
    n = np.logspace(6, 32, 300)
    fig, ax = figure(3.4, 2.8)
    for T, text, color, ls in [(1e4, r"$10\,\mathrm{keV}$", BLUE, "-"),
                               (1e1, r"$10\,\mathrm{eV}$", ORANGE, "--"),
                               (1e-1, r"$0.1\,\mathrm{eV}$", GRAY, ":")]:
        N = N_of(n, T * kelvin)
        ax.plot(n, N, color=color, ls=ls)
        k = np.searchsorted(n, 1e8)
        label(ax, n[k], N[k] * 4, text, color)
    ax.axhline(1, color=ORANGE, lw=0.6)
    ax.fill_between(n, 1e-6, 1, color=ORANGE, alpha=0.10, lw=0)
    ax.set(xscale="log", yscale="log", xlim=(1e6, 1e32), ylim=(1e-4, 1e16),
           xlabel=r"$n_e\ [\mathrm{m^{-3}}]$", ylabel=r"$N_D$")
    log_ticks(ax.xaxis, 6, 30, 8)
    log_ticks(ax.yaxis, -4, 16, 4)
    save(fig, "debye_number")


def _kelvin_per_ev():
    """Kelvin per electron-volt of k_B T, from the SI values."""
    from si import SI_VALUES

    return float((e / k_B).subs(SI_VALUES))

if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
