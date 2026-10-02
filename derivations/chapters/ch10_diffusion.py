"""Chapter 10, diffusion: src/chapters/10-diffusion.typ.

Run `python derivations/ch10_diffusion.py` to check every step, or
`pytest derivations` to check every chapter.

Coverage (line in src/chapters/10-diffusion.typ -> test):
  64-72, 83-97    random walk: <x> = 0, <x^2> = 2 D t, D = dx^2/(2 dt) -> test_random_walk
  100-113         Fick flux from left/right movers, diffusion equation -> test_fick_and_diffusion
  116-121         Green function, <x^2> = 2 D t, <r^2> = 6 D t        -> test_green_function
  126-136, 148-153 normalized variables, D_* = 0.0578                -> test_normalized_variables
  163-169         example: D = 20 m^2/s, tau_D = 5.0e-4 s           -> test_example_random_walk
  254-304         drift-diffusion velocity, mobility, Einstein relation -> test_mobility_diffusion
  317-325         example: mu_e = 1.76e3, D_e = 3.52e3                -> test_example_mobility
  409-479         ambipolar field, D_a and its mu_e >> mu_i limit      -> test_ambipolar
  492-505         example: E_a = 0.897 V/m, D_a = 18.2, |Gamma_a|      -> test_example_ambipolar
  586-653         magnetized tensor: D_par, D_perp, D_H, inverse matrix,
                  strong-field limit, (nu/2) rho_th^2                 -> test_magnetized_diffusion
  657-659         Hall-like flux is divergence free                   -> test_magnetized_diffusion
  675-686         example: |Omega_e|, D_par, D_perp, ratio            -> test_example_magnetized
  781-789, 812-858 classical one-fluid D_perp^cl, tau_D               -> test_classical_cross_field
  795-797         Bohm estimate (units, B^-1 vs B^-2 scaling)         -> test_classical_cross_field
  873-885         example: D_cl, D_Bohm, ratio, tau_D                 -> test_example_classical
"""

import itertools

import sympy as sp
from sympy.physics import units as u

from ch07_multiple_fluids import Tex, close, num
import si
from si import Derivation, e, k_B, m_e, m_i


# Units of this file's symbols. Kept local (not in the shared si.UNITS) so that
# symbols with common names in other chapter files cannot clash.
LOCAL = {}


def check(derived, stated, unit=None, units=None):
    """si.check with this file's LOCAL unit table."""
    return si.check(derived, stated, unit=unit, units={**LOCAL, **(units or {})})

# CODATA 2018 values for the worked examples.
CODATA = {e: 1.602176634e-19, m_e: 9.1093837015e-31, m_i: 1.67262192369e-27}

x, t = sp.symbols("x t", real=True)
dx, dt, D, Lm, tm = sp.symbols("Delta_x Delta_t D L t_0", positive=True)
LOCAL.update({dx: u.meter, dt: u.second, D: u.meter**2 / u.second, Lm: u.meter, tm: u.second})

# Results shared by the tests and the plots: each test proves its derivation
# equals one of these expressions, and each plot_* lambdifies the same one.
N0, tp = sp.symbols("N_0 t", positive=True)
GREEN = N0 / sp.sqrt(4 * sp.pi * D * tp) * sp.exp(-x**2 / (4 * D * tp))  # line 118


# ---------------------------------------------------------------------------
# Random walk and Fick's law
# ---------------------------------------------------------------------------
def test_random_walk():
    d = Derivation("Random walk", "src/chapters/10-diffusion.typ:92")
    # One step: +dx or -dx with probability 1/2 (line 85).
    d.eq("one step", Tex(r"\langle\Delta x\rangle"), (dx + (-dx)) / 2)
    d.eq("one step", Tex(r"\langle(\Delta x)^2\rangle"), (dx**2 + (-dx) ** 2) / 2)
    # N independent steps: average x and x^2 over all 2^N equally likely paths.
    for N in range(1, 7):
        paths = list(itertools.product([1, -1], repeat=N))
        mean = sum(sum(p) for p in paths) * dx / len(paths)
        msq = sum(sum(p) ** 2 for p in paths) * dx**2 / len(paths)
        check(mean, 0)
        check(msq, N * dx**2)
    # With N = t/dt and D = dx^2/(2 dt): <x^2> = 2 D t (line 94).
    msq_t = d.eq("N = t / Delta t", Tex(r"\langle x^2\rangle"), (t / dt) * dx**2)
    check(msq_t, 2 * (dx**2 / (2 * dt)) * t)
    check(dx**2 / (2 * dt), dx**2 / (2 * dt), unit=u.meter**2 / u.second)
    check(Lm**2 / D, Lm**2 / D, unit=u.second)  # tau_D = L^2/D


def test_fick_and_diffusion():
    d = Derivation("Fick's law and the diffusion equation", "src/chapters/10-diffusion.typ:104")
    n = sp.Function("n")
    x0 = sp.Symbol("x_0", real=True)
    # Half of the particles in the cell left of x0 cross to the right in dt,
    # half of those in the cell right of x0 cross to the left.
    Gamma = (n(x0 - dx / 2) * dx / 2 - n(x0 + dx / 2) * dx / 2) / dt
    lead = sp.series(Gamma, dx, 0, 3).removeO().doit()
    G = d.eq("expand densities", Tex(r"\Gamma^D"), sp.simplify(lead))
    check(G, -(dx**2 / (2 * dt)) * sp.diff(n(x0), x0))
    # Conservation dn/dt + dGamma/dx = 0 with Gamma = -D dn/dx (lines 108-113).
    Dx = sp.Function("D")(x)
    nn = sp.Function("n")(x, t)
    dndt = d.eq("conservation", sp.Derivative(nn, t), -sp.diff(-Dx * sp.diff(nn, x), x))
    check(dndt, sp.diff(Dx * sp.diff(nn, x), x))


def test_green_function():
    d = Derivation("Green function of the diffusion equation", "src/chapters/10-diffusion.typ:118")
    G = GREEN
    # Solves dn/dt = D d2n/dx2 and conserves the column density N0.
    check(sp.diff(G, tp) - D * sp.diff(G, x, 2), 0)
    check(sp.integrate(G, (x, -sp.oo, sp.oo)), N0)
    # Point-like start: n -> 0 away from x = 0 as t -> 0+.
    check(sp.limit(G.subs(x, 1), tp, 0, "+"), 0)
    x2 = d.eq("second moment", Tex(r"\langle x^2\rangle"), sp.integrate(x**2 * G, (x, -sp.oo, sp.oo)) / N0)
    check(x2, 2 * D * tp)
    # Three independent directions: <r^2> = 3 <x^2> = 6 D t (line 121).
    yy, zz = sp.symbols("y z", real=True)
    G3 = G * G.subs(x, yy) * G.subs(x, zz) / N0**2
    r2 = sp.integrate((x**2 + yy**2 + zz**2) * G3, (x, -sp.oo, sp.oo), (yy, -sp.oo, sp.oo),
                      (zz, -sp.oo, sp.oo)) / N0
    check(d.eq("three directions", Tex(r"\langle r^2\rangle"), r2), 6 * D * tp)
    check(N0 / sp.sqrt(D * tm), N0 / sp.sqrt(D * tm), unit=u.meter**-3, units={N0: u.meter**-2})


def test_normalized_variables():
    d = Derivation("Normalized diffusion variables", "src/chapters/10-diffusion.typ:134")
    L0, tau0, n0, xi, tau = sp.symbols("L_0 tau_0 n_0 xi tau", positive=True)
    Dn = sp.Symbol("D_norm", positive=True)
    nf = sp.Function("N")
    # n(x, t) = n0 N(x/L0, t/tau0) with D = D_norm L0^2/tau0 (lines 126-134).
    n = n0 * nf(x / L0, t / tau0)
    resid = sp.diff(n, t) - Dn * L0**2 / tau0 * sp.diff(n, x, 2)
    resid = sp.simplify(resid.subs({x: xi * L0, t: tau * tau0}) * tau0 / n0)
    stated = (sp.Derivative(nf(xi, tau), tau) - Dn * sp.Derivative(nf(xi, tau), xi, 2))
    check(resid.doit(), stated.doit())
    # tau_D / tau0 = L_norm^2 / D_norm (line 136).
    Ln = sp.Symbol("L_norm", positive=True)
    check((Ln * L0) ** 2 / (Dn * L0**2 / tau0) / tau0, Ln**2 / Dn)
    # Animation: steps of 0.34 in xi every unit of tau give D_* = 0.34^2/2 (line 150).
    Dstar = num(d, "Delta xi squared / 2", "D_*", 0.34**2 / 2)
    close(Dstar, "0.0578")


def test_example_random_walk():
    d = Derivation("Example: random-walk diffusion", "src/chapters/10-diffusion.typ:163")
    D_ = num(d, "dx2 / (2 dt)", "D", (2.0e-3) ** 2 / (2 * 1.0e-7))
    close(D_, "2.0e1")
    close(num(d, "L2 / D", r"\tau_D", (1.0e-1) ** 2 / D_), "5.0e-4")


# ---------------------------------------------------------------------------
# Mobility, Einstein relation, ambipolar diffusion
# ---------------------------------------------------------------------------
q, nu, m, T = sp.symbols("q_s nu_s m_s T_s", positive=True)  # q > 0 here; sign handled below
LOCAL.update({q: u.coulomb, nu: u.second**-1, m: u.kilogram, T: u.kelvin})
OM = sp.Symbol("Omega_s", real=True)
D_S = k_B * T / (m * nu)                       # unmagnetized D_s (line 304)
D_PERP = D_S / (1 + (OM / nu) ** 2)            # line 626
D_HALL = D_S * (OM / nu) / (1 + (OM / nu) ** 2)


def test_mobility_diffusion():
    d = Derivation("Mobility and diffusion", "src/chapters/10-diffusion.typ:291")
    n = sp.Symbol("n_s", positive=True)
    E, gn, us = sp.symbols("E g u_s", real=True)  # g = dn/dx
    qs = sp.Symbol("q", real=True)  # signed charge
    # Inertialess momentum balance: m n nu u = q n E - k_B T grad n (line 286).
    u_sol = sp.solve(sp.Eq(m * n * nu * us, qs * n * E - k_B * T * gn), us)[0]
    d.eq("drop inertia", Tex("u_s"), u_sol)
    mu_q, D_s = qs / (m * nu), k_B * T / (m * nu)
    check(u_sol, mu_q * E - D_s * gn / n)
    # Flux Gamma = n u (line 267) and Einstein relation D/|mu| = k_B T/|q| (line 304).
    check(n * u_sol, n * mu_q * E - D_s * gn)
    einstein = d.eq("Einstein relation", Tex(r"D_s/|\mu_s|"), D_s / (q / (m * nu)))
    check(einstein, k_B * T / q)
    check(q / (m * nu), q / (m * nu), unit=u.meter**2 / u.volt / u.second)
    check(D_s, D_s, unit=u.meter**2 / u.second)


def test_example_mobility():
    d = Derivation("Example: electron mobility and diffusion", "src/chapters/10-diffusion.typ:317")
    me, nu_ = CODATA[m_e], 1.0e8
    close(num(d, "e / (m_e nu_e)", r"\mu_e", CODATA[e] / (me * nu_)), "1.76e3")
    close(num(d, "k_B T_e / (m_e nu_e)", "D_e", 3.204e-19 / (me * nu_)), "3.52e3")


mui, mue, Di, De, n_a = sp.symbols("mu_i mu_e D_i D_e n", positive=True)
E_x, g_n = sp.symbols("E g", real=True)  # field and density gradient along x
GAMMA_I = mui * n_a * E_x - Di * g_n     # ion flux: drift + diffusion (line 449)
GAMMA_E = -mue * n_a * E_x - De * g_n    # electron flux
E_AMB = (Di - De) / (mui + mue) * g_n / n_a   # line 457
D_AMB = (mui * De + mue * Di) / (mui + mue)   # line 470


def test_ambipolar():
    d = Derivation("Ambipolar diffusion", "src/chapters/10-diffusion.typ:457")
    n, E, gn, Gi, Ge = n_a, E_x, g_n, GAMMA_I, GAMMA_E
    # Zero current j = e (Gamma_i - Gamma_e) = 0 fixes E (lines 449-457).
    Ea = sp.solve(sp.Eq(Gi, Ge), E)[0]
    d.eq("j = 0", Tex("E_a"), Ea)
    check(Ea, E_AMB)
    # Insert into Gamma_i: Gamma_a = -D_a grad n (lines 462-473).
    Ga = sp.simplify(Gi.subs(E, Ea))
    Da = D_AMB
    d.eq("insert E_a", Tex(r"\Gamma_a"), -Da * gn)
    check(Ga, -Da * gn)
    check(Ge.subs(E, Ea), -Da * gn)
    # mu_e >> mu_i: first order in eps = mu_i/mu_e gives D_i + eps (D_e - D_i) (line 479).
    eps = sp.Symbol("epsilon", positive=True)
    Da_eps = sp.series(Da.subs(mui, eps * mue), eps, 0, 2).removeO()
    check(Da_eps, Di + eps * (De - Di))
    # The stated D_i + eps D_e differs by eps D_i, negligible against D_i.
    check(sp.limit((Da_eps - (Di + eps * De)) / Di, eps, 0), 0)


def test_example_ambipolar():
    d = Derivation("Example: ambipolar field and flux", "src/chapters/10-diffusion.typ:492")
    kT, nu_i, nu_e, n, gn_n = 1.602e-19, 1.0e7, 1.0e9, 1.0e16, -1.0
    mui = CODATA[e] / (CODATA[m_i] * nu_i)
    mue = CODATA[e] / (CODATA[m_e] * nu_e)
    Di, De = kT / (CODATA[m_i] * nu_i), kT / (CODATA[m_e] * nu_e)
    Ea = num(d, "(D_i - D_e)/(mu_i + mu_e) grad n / n", "E_a", (Di - De) / (mui + mue) * gn_n)
    Da = num(d, "ambipolar coefficient", "D_a", (mui * De + mue * Di) / (mui + mue))
    G = num(d, "D_a times grad n", r"|\Gamma_a|", Da * n * abs(gn_n))
    close(Ea, "0.897")
    close(Da, "1.82e1")
    close(G, "1.82e17")


# ---------------------------------------------------------------------------
# Magnetized and classical cross-field diffusion
# ---------------------------------------------------------------------------
def test_magnetized_diffusion():
    d = Derivation("Diffusion across a magnetic field", "src/chapters/10-diffusion.typ:604")
    qs, Om = sp.symbols("q Omega_s", real=True)
    n = sp.Symbol("n_s", positive=True)
    ux, uy, Ex, Ey, gx, gy = sp.symbols("u_x u_y E_x E_y g_x g_y", real=True)
    B = sp.Symbol("B", positive=True)
    # Steady perpendicular balance m nu u = q (E + u x B z) - (k_B T/n) grad n.
    eqs = [m * nu * ux - qs * (Ex + uy * B) + k_B * T * gx / n,
           m * nu * uy - qs * (Ey - ux * B) + k_B * T * gy / n]
    # Matrix form (line 604) with Omega_s = q B / m.
    M = sp.Matrix([[nu, -Om], [Om, nu]])
    rhs = sp.Matrix([qs / m * Ex - k_B * T / (m * n) * gx, qs / m * Ey - k_B * T / (m * n) * gy])
    lin = (M * sp.Matrix([ux, uy]) - rhs).subs(Om, qs * B / m)
    check(sp.expand(lin[0] - eqs[0] / m), 0)
    check(sp.expand(lin[1] - eqs[1] / m), 0)
    # Inverse (line 612).
    Minv = d.eq("invert", Tex(r"M^{-1}"), sp.simplify(M.inv()))
    for i in range(2):
        for j in range(2):
            check(Minv[i, j], sp.Matrix([[nu, Om], [-Om, nu]])[i, j] / (nu**2 + Om**2))
    # Density-gradient part of the flux n u (lines 618-626).
    flux = sp.simplify(n * Minv * sp.Matrix([-k_B * T / (m * n) * gx, -k_B * T / (m * n) * gy]))
    Ds, Dperp, DH = D_S, D_PERP, D_HALL
    # Gamma_perp = -D_perp grad n + D_H b x grad n with b x grad n = (-g_y, g_x).
    check(flux[0], -Dperp * gx - DH * gy)
    check(flux[1], -Dperp * gy + DH * gx)
    d.eq("gradient flux", Tex(r"\Gamma_\perp"), Tex(r"-D_\perp\nabla_\perp n_s + D_H\,\hat b\times\nabla_\perp n_s"))
    d.eq("coefficient", Tex(r"D_\perp"), Dperp)
    d.eq("coefficient", Tex(r"D_H"), DH)
    check(k_B * T * nu / (m * (nu**2 + Om**2)), Ds * nu**2 / (nu**2 + Om**2))
    # Strong field |Omega| >> nu: D_perp ~ D_s (nu/Omega)^2 (line 635).
    eps = sp.Symbol("epsilon", positive=True)  # nu / Omega
    lead = sp.series(Dperp.subs(Om, nu / eps) / Ds, eps, 0, 3).removeO()
    check(lead, eps**2)
    # Thermal gyroradius form (lines 644-650).
    rho2 = (sp.sqrt(2 * k_B * T / m) / Om) ** 2
    check(Ds * (nu / Om) ** 2, nu / 2 * rho2)
    # Hall flux D_H b x grad n has zero divergence for constant D_H and b (line 657).
    X, Y = sp.symbols("X Y", real=True)
    nf = sp.Function("n")(X, Y)
    hall = [-DH * sp.diff(nf, Y), DH * sp.diff(nf, X)]
    check(sp.diff(hall[0], X) + sp.diff(hall[1], Y), 0)


def test_example_magnetized():
    d = Derivation("Example: magnetized electron diffusion", "src/chapters/10-diffusion.typ:675")
    kT, B, nu_ = 1.602e-19, 1.0e-2, 1.0e7
    Om = num(d, "e B / m_e", r"|\Omega_e|", CODATA[e] * B / CODATA[m_e])
    Dpar = num(d, "k_B T / (m_e nu)", r"D_\parallel", kT / (CODATA[m_e] * nu_))
    Dperp = num(d, "D / (1 + (Omega/nu) squared)", r"D_\perp", Dpar / (1 + (Om / nu_) ** 2))
    close(Om, "1.76e9")
    close(Dpar, "1.76e4")
    close(Dperp, "0.569")
    close(num(d, "ratio", r"D_\perp/D_\parallel", Dperp / Dpar), "3.23e-5")


sig, B_f, n_f = sp.symbols("sigma B n", positive=True)
Te, Ti = sp.symbols("T_e T_i", positive=True)
D_CL = n_f * k_B * (Te + Ti) / (sig * B_f**2)   # classical, line 849
D_BOHM = k_B * Te / (16 * e * B_f)              # empirical Bohm, line 796


def test_classical_cross_field():
    d = Derivation("Classical cross-field diffusion", "src/chapters/10-diffusion.typ:831")
    B, n = B_f, n_f
    Ex, Ey, ux, uy, gx, gy = sp.symbols("E_x E_y u_x u_y g_x g_y", real=True)  # g = grad_perp p
    # j = sigma (E + u x B z) and 0 = -grad p + j x B z (lines 812-816).
    j = [sig * (Ex + uy * B), sig * (Ey - ux * B)]
    jxB = [j[1] * B, -j[0] * B]
    sol = sp.solve([-gx + jxB[0], -gy + jxB[1]], [ux, uy], dict=True)[0]
    # Stated (line 831): u_perp = E x B / B^2 - grad_perp p / (sigma B^2); (E x B)_x = E_y B.
    check(sol[ux], Ey * B / B**2 - gx / (sig * B**2))
    check(sol[uy], -Ex * B / B**2 - gy / (sig * B**2))
    d.eq("solve force balance + Ohm", Tex(r"u_\perp"), Tex(r"\frac{E\times B}{B^2} - \frac{\nabla_\perp p}{\sigma B^2}"))
    # p = n k_B (T_e + T_i) with uniform temperatures: diffusive flux n u (lines 839-849).
    gn = sp.Symbol("g_n", real=True)
    Gdiff = n * (-(k_B * (Te + Ti) * gn) / (sig * B**2))
    Dcl = d.eq("p = n k_B (T_e + T_i)", Tex(r"D_\perp^{cl}"), sp.simplify(-Gdiff / gn))
    LOCAL.update({sig: u.siemens / u.meter, B: u.tesla, n: u.meter**-3, Te: u.kelvin, Ti: u.kelvin})
    check(Dcl, D_CL, unit=u.meter**2 / u.second)
    eta = sp.Symbol("eta", positive=True)
    check(Dcl.subs(sig, 1 / eta), eta * n * k_B * (Te + Ti) / B**2)
    # Scalings: classical B^-2, Bohm k_B T_e/(16 e B) as B^-1 (line 796).
    DB = D_BOHM
    check(DB, DB, unit=u.meter**2 / u.second)
    check(sp.simplify(B * sp.diff(Dcl, B) / Dcl), -2)
    check(sp.simplify(B * sp.diff(DB, B) / DB), -1)


def test_example_classical():
    d = Derivation("Example: classical and Bohm diffusion", "src/chapters/10-diffusion.typ:873")
    n, kT, sig, B, L = 1.0e16, 1.602e-18, 1.0e5, 1.0e-2, 1.0
    Dcl = num(d, "n k_B (T_e + T_i) / (sigma B2)", r"D_\perp^{cl}", n * 2 * kT / (sig * B**2))
    DB = num(d, "k_B T_e / (16 e B)", r"D_\perp^{B}", kT / (16 * CODATA[e] * B))
    close(Dcl, "3.20e-3")
    close(DB, "6.25e1")
    close(num(d, "ratio", r"D^B/D^{cl}", DB / Dcl), "1.95e4")
    close(num(d, "L2 / D", r"\tau_D", L**2 / Dcl), "3.12e2")


# ---------------------------------------------------------------------------
# Plots of derived results (written to build/fig by run_as_script)
# ---------------------------------------------------------------------------
def plot_random_walk_diffusion():
    """Green function at t = tau_D and 4 tau_D: rms width doubles, peak halves."""
    import numpy as np

    from si import BLUE, ORANGE, figure, label, save

    xi, tau, L0, tauD, n0 = sp.symbols("xi tau L_0 tau_D n_0", positive=True)
    # x = xi L0, t = tau tau_D with tau_D = L0^2/D, column N0 = sqrt(4 pi) L0 n0.
    norm = GREEN.subs({x: xi * L0, tp: tau * tauD, N0: sp.sqrt(4 * sp.pi) * L0 * n0}) / n0
    norm = sp.simplify(norm.subs(D, L0**2 / tauD))
    f = sp.lambdify((xi, tau), norm, "numpy")
    rms = sp.lambdify(tau, sp.sqrt(sp.integrate(xi**2 * norm, (xi, -sp.oo, sp.oo))
                                   / sp.integrate(norm, (xi, -sp.oo, sp.oo))), "numpy")

    fig, ax = figure(4.2, 2.4)
    xx = np.linspace(-9, 9, 400)
    for T_, color, ls, txt, at in [(1, BLUE, "-", r"$t=\tau_D$", (0.5, 0.97)),
                                   (4, ORANGE, "--", r"$t=4\tau_D$", (4.2, 0.36))]:
        ax.plot(xx, f(xx, T_), color=color, ls=ls)
        s_ = rms(T_)  # rms width sqrt(2 t / tau_D)
        h = f(s_, T_)
        ax.annotate("", xy=(-s_, h), xytext=(s_, h),
                    arrowprops=dict(arrowstyle="<->", color=color, lw=0.9, shrinkA=0, shrinkB=0))
        label(ax, *at, txt, color)
    ax.text(0, 0.03, r"arrows: $\pm\langle x^2\rangle^{1/2}$", ha="center", fontsize=9, color="#333333")
    ax.set_xlim(-9, 9)
    ax.set_ylim(0, 1.08)
    ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel(r"$x/L_0$")
    ax.set_ylabel(r"$n/n_0$")
    save(fig, "random-walk-diffusion")


def plot_cross_field_diffusion():
    """Perpendicular diffusion versus magnetization, with the strong-field limit."""
    import numpy as np

    from si import BLUE, GRAY, figure, label, log_ticks, save

    X = sp.Symbol("X", positive=True)  # |Omega_s| / nu_s
    ratio = sp.lambdify(X, sp.simplify((D_PERP / D_S).subs(OM, X * nu)), "numpy")
    # Worked example (line 675): electrons, B = 10 mT, nu_e = 1e7 s^-1.
    X_ex = CODATA[e] * 1.0e-2 / CODATA[m_e] / 1.0e7

    fig, ax = figure(4.2, 2.6)
    xx = np.logspace(-2, 3, 300)
    ax.plot(xx, ratio(xx), color=BLUE)
    ax.plot([X_ex], [ratio(X_ex)], "o", color=BLUE, ms=4)
    label(ax, X_ex * 0.8, ratio(X_ex), "worked example", BLUE, ha="right", va="center", fontsize=9)
    label(ax, 12, 12**-2.0 * 3, r"$\simeq(\nu_s/\Omega_s)^2$", GRAY)
    label(ax, 0.012, 0.25, r"$D_{s,\perp}$", BLUE, va="center")
    ax.set_xscale("log")
    ax.set_yscale("log")
    log_ticks(ax.xaxis, -2, 3)
    log_ticks(ax.yaxis, -6, 0, 2)
    ax.set_ylim(1e-6, 3)
    ax.set_xlabel(r"magnetization $|\Omega_s|/\nu_s$")
    ax.set_ylabel(r"$D_{s,\perp}/D_s$")
    save(fig, "cross-field-diffusion")


def _mantissa_exponent(value):
    import math

    k = math.floor(math.log10(value))
    return value / 10**k, k


def plot_diffusion_scalings():
    """Classical and Bohm cross-field diffusion for the worked-example plasma."""
    import numpy as np

    from si import BLUE, GRAY, ORANGE, SI_VALUES, figure, label, log_ticks, save

    # Worked example (line 873): n = 1e16 m^-3, k_B T_e = k_B T_i = 10 eV, sigma = 1e5 S/m.
    kT = 1.602e-18
    vals = {n_f: 1.0e16, sig: 1.0e5, Te: kT / SI_VALUES[k_B], Ti: kT / SI_VALUES[k_B],
            k_B: SI_VALUES[k_B], e: SI_VALUES[e]}
    dcl = sp.lambdify(B_f, D_CL.subs(vals), "numpy")
    dbohm = sp.lambdify(B_f, D_BOHM.subs(vals), "numpy")

    fig, ax = figure(4.2, 2.6)
    BB = np.logspace(-3, 0, 100)
    ax.plot(BB, dbohm(BB), color=ORANGE, ls="--")
    ax.plot(BB, dcl(BB), color=BLUE)
    B_ex = 1.0e-2
    ax.annotate("", xy=(B_ex, dbohm(B_ex)), xytext=(B_ex, dcl(B_ex)),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=0.9, shrinkA=2, shrinkB=2))
    label(ax, B_ex * 1.15, (dbohm(B_ex) * dcl(B_ex)) ** 0.5,
          r"$\times\,%.2f\cdot10^{%d}$" % _mantissa_exponent(dbohm(B_ex) / dcl(B_ex)),
          GRAY, va="center", fontsize=9)
    label(ax, 1.3e-3, dbohm(1.3e-3) * 1.5, r"Bohm $\propto B^{-1}$", ORANGE)
    label(ax, 0.1, dcl(0.1) * 20, r"classical $\propto B^{-2}$", BLUE)
    ax.set_xscale("log")
    ax.set_yscale("log")
    log_ticks(ax.xaxis, -3, 0)
    log_ticks(ax.yaxis, -6, 4, 2)
    ax.set_xlabel(r"$B$ (T)")
    ax.set_ylabel(r"$D_\perp$ (m$^2$/s)")
    save(fig, "diffusion-scalings")


def plot_ambipolar_balance():
    """Diffusion and field-drift parts of both species fluxes in the worked example."""
    from si import BLUE, GRAY, ORANGE, figure, label, save

    # Worked example (line 492): k_B T = 1 eV, nu_i = 1e7, nu_e = 1e9 s^-1,
    # n = 1e16 m^-3, (dn/dx)/n = -1 m^-1, hydrogen.
    kT, nu_i, nu_e, n0, gn_n = 1.602e-19, 1.0e7, 1.0e9, 1.0e16, -1.0
    vals = {mui: CODATA[e] / (CODATA[m_i] * nu_i), mue: CODATA[e] / (CODATA[m_e] * nu_e),
            Di: kT / (CODATA[m_i] * nu_i), De: kT / (CODATA[m_e] * nu_e),
            n_a: n0, g_n: gn_n * n0}
    Ea = float(E_AMB.subs(vals))
    unit = 1e17  # m^-2 s^-1
    rows = []
    for G in (GAMMA_E, GAMMA_I):
        diff = float(G.subs(vals).subs(E_x, 0)) / unit
        total = float(G.subs(vals).subs(E_x, Ea)) / unit
        rows.append((diff, total))
    Ga = float((-D_AMB * g_n).subs(vals)) / unit

    fig, ax = figure(4.2, 2.0)
    ax.axvline(Ga, color=GRAY, lw=0.9, ls=":")
    ax.text(Ga, 1.55, r"$\Gamma_a$", color=GRAY, ha="center", va="bottom")
    for y, (diff, total), name in [(1, rows[0], "electrons"), (0, rows[1], "ions")]:
        ax.annotate("", xy=(diff, y + 0.12), xytext=(0, y + 0.12),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6, shrinkA=0, shrinkB=0))
        ax.annotate("", xy=(total, y - 0.12), xytext=(diff, y - 0.12),
                    arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6, ls="--",
                                    shrinkA=0, shrinkB=0))
        ax.text(-0.4, y, name, ha="right", va="center")
    label(ax, rows[0][0] / 2, 1.2, r"diffusion $-D_e\,\partial_x n$", BLUE, ha="center")
    label(ax, rows[0][0] / 2, 0.8, r"field drift $-\mu_e n E_a$", ORANGE, ha="center", va="top")
    label(ax, rows[1][1] + 0.4, 0, r"ions: diffusion + drift $\mu_i n E_a$", "#333333",
          va="center", fontsize=9)
    ax.set_xlim(-0.2, max(r[0] for r in rows) * 1.05)
    ax.set_ylim(-0.5, 1.75)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel(r"particle flux $\Gamma_x$ ($10^{17}$ m$^{-2}$ s$^{-1}$)")
    save(fig, "ambipolar-balance")

if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
