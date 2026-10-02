# Chapter 2 · Debye shielding (src/chapters/02-debye-shielding.typ)
#
# Charge-separation scale, Debye length, screened point charge, finite
# spherical source (bare and screened), Debye number and the n-T regime map.

# %% Setup
import sympy as sp
from sympy.physics import units as u

from notebook import agrees, note, report, section, show
from si import check, e, eps0, k_B

n0, T_e, Q, r, R, N, kappa, s = sp.symbols("n_0 T_e Q r R N kappa s", positive=True)
lambda_D, a, L = sp.symbols("lambda_D a L", positive=True)
phi_0 = sp.Symbol("phi", positive=True)  # local potential value, for the Boltzmann factor
phi = sp.Function("phi")(r)
n_e, n_i, rho_q, rho_Q, E, W = sp.symbols("n_e n_i rho_q rho_Q E W")
E_in_sym, E_out_sym, phi_inner, phi_outer = sp.symbols("E_in E_out phi_in phi_out")
SI_UNITS = {n0: u.meter**-3, T_e: u.kelvin, Q: u.coulomb, r: u.meter, R: u.meter,
            N: u.meter**-3, kappa: u.meter**-1, lambda_D: u.meter, a: u.meter,
            L: u.meter, phi_0: u.volt, rho_q: u.coulomb / u.meter**3}


def laplacian(f):
    """Radial part of the spherical Laplacian, unevaluated: f'' + 2 f'/r."""
    return sp.Derivative(f, (r, 2)) + 2 * sp.Derivative(f, r) / r


# %% Charge-separation scale
section("Charge-separation scale", script="intro-debye-shielding")
note("Electrons removed from a sphere leave the charge density", N * e)
enclosed = show(sp.Eq(sp.Function("Q")(r), sp.Integral(4 * sp.pi * s**2 * N * e, (s, 0, r))))
Q_r = agrees(enclosed.rhs.doit(), sp.Rational(4, 3) * sp.pi * N * e * r**3, lhs=enclosed.lhs)
note("Gauss's law")
gauss = show(sp.Eq(4 * sp.pi * r**2 * eps0 * E, Q_r))
E_r = sp.solve(gauss, E)[0]
agrees(E_r, N * e * r / (3 * eps0), lhs=E)
check(E_r, N * e * r / (3 * eps0), unit=u.volt / u.meter, units=SI_UNITS)
note("Boundary potential against infinity; outside, the field is Coulomb")
boundary = show(sp.Eq(sp.Function("phi")(R),
                      sp.Integral(Q_r.subs(r, R) / (4 * sp.pi * eps0 * s**2), (s, R, sp.oo))))
phi_R = agrees(boundary.rhs.doit(), N * e * R**2 / (3 * eps0), lhs=boundary.lhs)
check(phi_R, phi_R, unit=u.volt, units=SI_UNITS)
note("Separation stops where the potential energy reaches the thermal energy")
balance = show(sp.Eq(e * phi_R, k_B * T_e))
R_scale = agrees(sp.solve(balance, R)[0], sp.sqrt(3 * eps0 * k_B * T_e / (N * e**2)), lhs=R, eq="debye-charge-separation-scale")
check(R_scale, R_scale, unit=u.meter, units=SI_UNITS)
note("With", sp.Eq(N, n0), "and", sp.Eq(lambda_D, sp.sqrt(eps0 * k_B * T_e / (n0 * e**2))))
agrees(R_scale.subs(N, n0) / sp.sqrt(eps0 * k_B * T_e / (n0 * e**2)), sp.sqrt(3),
       lhs=R / lambda_D)

# %% Debye length
section("Debye length", script="intro-debye-shielding")
note("Boltzmann factor", sp.exp(-W / (k_B * T_e)), "with the electron energy", sp.Eq(W, -e * phi_0))
boltzmann = agrees((n0 * sp.exp(-W / (k_B * T_e))).subs(W, -e * phi_0),
                   n0 * sp.exp(e * phi_0 / (k_B * T_e)), lhs=n_e, eq="debye-boltzmann-response")
note("Linearize for", sp.Lt(e * phi_0, k_B * T_e))
linear = sp.series(boltzmann, phi_0, 0, 2).removeO()
agrees(linear, n0 * (1 + e * phi_0 / (k_B * T_e)), lhs=n_e)
check(linear, linear, unit=u.meter**-3, units=SI_UNITS)
note("Immobile ions,", sp.Eq(n_i, n0))
charge = show(sp.Eq(rho_q, e * n_i - e * n_e))
charge_lin = agrees(sp.expand(charge.rhs.subs({n_i: n0, n_e: linear})),
                    -(e**2 * n0) / (k_B * T_e) * phi_0, lhs=rho_q)
check(charge_lin, charge_lin, unit=u.coulomb / u.meter**3, units=SI_UNITS)
note("Poisson equation in spherical symmetry")
poisson = show(sp.Eq(laplacian(phi), -rho_q / eps0))
check(poisson.rhs, poisson.rhs, unit=u.volt / u.meter**2, units=SI_UNITS)
screened_eq = show(poisson.subs(rho_q, charge_lin.subs(phi_0, phi)))
note("The coefficient of", phi, "defines the screening length")
lambda_D_sq = show(sp.Eq(lambda_D**2, sp.simplify(phi / screened_eq.rhs))).rhs
lambda_D_expr = agrees(sp.sqrt(lambda_D_sq), sp.sqrt(eps0 * k_B * T_e / (n0 * e**2)),
                       lhs=lambda_D, eq="debye-screened-equation")
check(lambda_D_expr, lambda_D_expr, unit=u.meter, units=SI_UNITS)

# %% Screened point charge
section("Screened point charge", script="intro-debye-shielding")
screening = show(sp.Eq(laplacian(phi), phi / lambda_D**2))
w = sp.Function("w")(r)
note("Substitute", sp.Eq(phi, w / r))
reduced = show(sp.Eq(sp.simplify(r * screening.lhs.subs(phi, w / r).doit()), w / lambda_D**2))
general = show(sp.dsolve(reduced, w))
note("Decay at infinity drops the growing branch; near the charge", sp.Eq(phi, Q / (4 * sp.pi * eps0 * r)))
C1 = sp.Symbol("C1")
decaying = general.rhs.coeff(sp.exp(-r / lambda_D)) * sp.exp(-r / lambda_D)
constant = sp.solve(sp.Eq(decaying.subs(r, 0), Q / (4 * sp.pi * eps0)), C1, dict=True)[0]
screened = agrees((decaying / r).subs(constant), Q / (4 * sp.pi * eps0 * r) * sp.exp(-r / lambda_D), lhs=phi)
assert sp.simplify(laplacian(screened).doit() - screened / lambda_D**2) == 0
bare = sp.limit(screened * r, r, 0) / r  # r << lambda_D
check(bare, Q / (4 * sp.pi * eps0 * r), unit=u.volt, units=SI_UNITS)

# %% Bare potential of a uniform sphere
section("Bare potential of a uniform sphere", script="debye-finite-source")
note("Total charge", Q, "spread uniformly over a sphere of radius", R)
rho_Q_expr = agrees(Q / (sp.Rational(4, 3) * sp.pi * R**3), 3 * Q / (4 * sp.pi * R**3),
                    lhs=rho_Q)
check(rho_Q_expr, rho_Q_expr, unit=u.coulomb / u.meter**3, units=SI_UNITS)
inner = show(sp.Eq(sp.Function("Q")(r), sp.Integral(4 * sp.pi * s**2 * rho_Q_expr, (s, 0, r))))
Q_in = agrees(inner.rhs.doit(), Q * r**3 / R**3, lhs=inner.lhs)
note("Gauss's law inside and outside")
E_in = agrees(Q_in / (4 * sp.pi * eps0 * r**2), Q * r / (4 * sp.pi * eps0 * R**3), lhs=E_in_sym)
E_out = show(sp.Eq(E_out_sym, Q / (4 * sp.pi * eps0 * r**2))).rhs
outside = show(sp.Eq(phi_outer, sp.Integral(E_out.subs(r, s), (s, r, sp.oo))))
phi_out = agrees(outside.rhs.doit(), Q / (4 * sp.pi * eps0 * r), lhs=phi_outer)
check(phi_out, phi_out, unit=u.volt, units=SI_UNITS)
inside = show(sp.Eq(phi_inner, phi_out.subs(r, R) + sp.Integral(E_in.subs(r, s), (s, r, R))))
phi_in = agrees(sp.factor(inside.rhs.doit()), Q / (8 * sp.pi * eps0 * R) * (3 - r**2 / R**2), lhs=phi_inner)
check(phi_in, phi_in, unit=u.volt, units=SI_UNITS)
note("Poisson inside:")
agrees(sp.simplify(laplacian(phi_in).doit()), -rho_Q_expr / eps0, lhs=laplacian(phi), eq="debye-poisson")
note("Potential and field are continuous at", sp.Eq(r, R))
assert sp.simplify(phi_in.subs(r, R) - phi_out.subs(r, R)) == 0
assert sp.simplify((phi_in.diff(r) - phi_out.diff(r)).subs(r, R)) == 0

# %% Small-source condition
section("Small-source condition", script="debye-finite-source")
note("The bare potential peaks at the centre")
phi_centre = show(sp.Eq(sp.Function("phi")(0), phi_in.subs(r, 0))).rhs
small_source = agrees(e * phi_centre / (k_B * T_e), 3 * e * Q / (8 * sp.pi * eps0 * R * k_B * T_e), lhs=e * sp.Function("phi")(0) / (k_B * T_e))
check(small_source, small_source, unit=u.meter / u.meter, units=SI_UNITS)

# %% Matched finite-source response
section("Matched finite-source Debye response", script="debye-finite-source")
A, B, phi_p = sp.symbols("A B phi_p")
x = sp.Symbol("x", positive=True)
note("Inside the source, with", sp.Eq(kappa, 1 / lambda_D))
screened_source = show(sp.Eq(laplacian(phi) - kappa**2 * phi, -rho_Q / eps0))
note("A constant particular solution")
phi_p_expr = sp.solve(screened_source.subs(phi, phi_p).doit().subs(rho_Q, rho_Q_expr), phi_p)[0]
agrees(phi_p_expr, 3 * Q / (4 * sp.pi * eps0 * kappa**2 * R**3), lhs=phi_p)
check(phi_p_expr, phi_p_expr, unit=u.volt, units=SI_UNITS)
note("Regular inside, decaying outside")
trial_in = show(sp.Eq(phi_inner, phi_p + A * sp.sinh(kappa * r) / r)).rhs
trial_out = show(sp.Eq(phi_outer, B * sp.exp(-kappa * r) / r)).rhs


def screened_operator(f):
    return laplacian(f).doit() - kappa**2 * f


assert sp.simplify(screened_operator(trial_in.subs(phi_p, phi_p_expr)) + rho_Q_expr / eps0) == 0
assert sp.simplify(screened_operator(trial_out)) == 0
note("Match potential and slope at", sp.Eq(r, R))
matching = [show(sp.Eq(trial_in.subs(r, R), trial_out.subs(r, R))),
            show(sp.Eq(trial_in.diff(r).subs(r, R), trial_out.diff(r).subs(r, R)))]
solution = sp.solve(matching, [A, B], dict=True)[0]
note("Solve and write", sp.Eq(x, kappa * R))


def in_x(expr):
    return sp.simplify(expr.rewrite(sp.exp).subs(kappa, x / R))


A_match = agrees(in_x(solution[A]), -(R * phi_p * (x + 1) * sp.exp(-x)) / x, lhs=A)
B_match = agrees(in_x(solution[B]),
                 (R * phi_p) / (2 * x) * (sp.exp(x) * (x - 1) + (x + 1) * sp.exp(-x)), lhs=B)
B_full = B_match.subs({phi_p: phi_p_expr, x: kappa * R})
check(B_full, B_full, unit=u.volt * u.meter, units=SI_UNITS)
note("Point-source limit", sp.Eq(R, 0, evaluate=False), "recovers the screened Coulomb coefficient")
agrees(sp.limit(B_full, R, 0), Q / (4 * sp.pi * eps0), lhs=B)

# %% Debye number and coupling
section("Debye number and coupling", script="debye-finite-source")
N_D, Gamma = sp.symbols("N_D Gamma", positive=True)
note("Electrons in a Debye sphere")
count = show(sp.Eq(N_D, sp.Integral(4 * sp.pi * s**2 * n0, (s, 0, lambda_D))))
N_D_expr = agrees(count.rhs.doit(), sp.Rational(4, 3) * sp.pi * n0 * lambda_D**3, lhs=N_D)
check(N_D_expr, N_D_expr, unit=u.meter / u.meter, units=SI_UNITS)
note("Mean spacing: one particle per sphere of radius", a)
spacing = show(sp.Eq(sp.Rational(4, 3) * sp.pi * a**3 * n0, 1))
a_expr = agrees(sp.solve(spacing, a)[0], (3 / (4 * sp.pi * n0)) ** sp.Rational(1, 3), lhs=a)
check(a_expr, a_expr, unit=u.meter, units=SI_UNITS)
note("Coupling: Coulomb energy at that spacing over thermal energy")
coupling = show(sp.Eq(Gamma, e**2 / (4 * sp.pi * eps0 * a * k_B * T_e))).rhs
check(coupling.subs(a, a_expr), coupling.subs(a, a_expr), unit=u.meter / u.meter, units=SI_UNITS)
note("Weak coupling and a large Debye number are one condition:")
link = show(sp.Eq(Gamma * N_D ** sp.Rational(2, 3),
                  sp.simplify((coupling.subs(a, a_expr)
                               * N_D_expr.subs(lambda_D, lambda_D_expr) ** sp.Rational(2, 3)))))
assert link.rhs.free_symbols == set(), link

# %% Regime lines in the n-T plane
section("Regime lines in the n-T plane", script="debye-finite-source")
T_eV = k_B * T_e / e


def temperature_in_volt(condition):
    """Solve condition = 0 for T_e and return k_B T_e / e (numerically k_B T_e in eV)."""
    return sp.simplify(k_B * sp.solve(condition, T_e)[0] / e)


note("System size equals the screening length,", sp.Eq(lambda_D, L))
T_line_L = agrees(temperature_in_volt(lambda_D_expr**2 - L**2), e * n0 * L**2 / eps0, lhs=T_eV)
check(T_line_L, T_line_L, unit=u.volt, units=SI_UNITS)
note("One electron per Debye sphere,", sp.Eq(N_D, 1))
T_line_1 = agrees(temperature_in_volt(N_D_expr.subs(lambda_D, lambda_D_expr) - 1),
                  e / eps0 * (3 / (4 * sp.pi)) ** sp.Rational(2, 3) * n0 ** sp.Rational(1, 3), lhs=T_eV)
check(T_line_1, T_line_1, unit=u.volt, units=SI_UNITS)

# %% Plots: shared setup
import numpy as np

from si import BLUE, EXAMPLE_PLASMAS, GRAY, ORANGE, SI_VALUES, figure, label, log_ticks, save, slide_width

# Widths fit the slide grid (si.slide_width): one panel of the pair or a
# summary plot spans 6 columns, the n-T map 10.
PANEL = (slide_width(6), 2.4)  # one panel of a side-by-side pair (debye_potential | debye_sphere_potential)
# r in units of lambda_D (kappa = 1), phi in units of Q/(4 pi eps0 lambda_D).
NORMALIZED = {Q: 1, eps0: 1 / (4 * sp.pi), lambda_D: 1, kappa: 1}


def potential_axes(ax):
    ax.set(xlim=(0, 4), ylim=(0, 3.2), xticks=[0, 1, 2, 3, 4],
           xlabel=r"$r/\lambda_D$", ylabel=r"$4\pi\varepsilon_0\lambda_D\,\varphi/Q$")


radius = np.linspace(1e-6, 4, 400)

# %% Plot: screened and bare point charge
bare_curve = sp.lambdify(r, bare.subs(NORMALIZED), "numpy")
screened_curve = sp.lambdify(r, screened.subs(NORMALIZED), "numpy")
fig, ax = figure(*PANEL)
ax.plot(radius, bare_curve(radius), color=ORANGE, ls="--")
ax.plot(radius, screened_curve(radius), color=BLUE)
label(ax, 1.3, bare_curve(1.3) + 0.08, "bare", ORANGE)
label(ax, 2.5, 0.05, "screened", BLUE)
potential_axes(ax)
save(fig, "debye_potential")

# %% Plot: uniform sphere of radius R = lambda_D/2, bare and screened
R_plot = sp.Rational(1, 2)
sphere = {**NORMALIZED, R: R_plot}
phi_p_plot = phi_p_expr.subs(sphere)
A_plot = A_match.subs({phi_p: phi_p_plot, x: R_plot, R: R_plot})
B_plot = B_match.subs({phi_p: phi_p_plot, x: R_plot, R: R_plot})
bare_sphere = sp.Piecewise((phi_in.subs(sphere), r <= R_plot), (phi_out.subs(sphere), True))
screened_sphere = sp.Piecewise((trial_in.subs({phi_p: phi_p_plot, A: A_plot, kappa: 1}), r <= R_plot),
                               (trial_out.subs({B: B_plot, kappa: 1}), True))
bare_sphere_curve = sp.lambdify(r, bare_sphere, "numpy")
screened_sphere_curve = sp.lambdify(r, screened_sphere, "numpy")
fig, ax = figure(*PANEL)
ax.plot(radius, bare_sphere_curve(radius), color=ORANGE, ls="--")
ax.plot(radius, screened_sphere_curve(radius), color=BLUE)
ax.axvline(float(R_plot), color="0.8", lw=0.6, zorder=0)
ax.text(float(R_plot) + 0.08, 3.15, r"$R$", ha="left", va="top", color="0.4")
label(ax, 1.3, bare_sphere_curve(1.3) + 0.08, "bare", ORANGE)
label(ax, 2.5, 0.05, "screened", BLUE)
potential_axes(ax)
save(fig, "debye_sphere_potential")

# %% Plots: n-T plane and regime map


def numeric(expr, *args):
    """lambdify expr in args with SI constants substituted."""
    return sp.lambdify(args, expr.subs(SI_VALUES), "numpy")


def nt_axes():
    fig, ax = figure(slide_width(10), 3.0)
    ax.set(xscale="log", yscale="log", xlim=(1e6, 1e32), ylim=(1e-2, 1e5),
           xlabel=r"$n_e\ [\mathrm{m^{-3}}]$", ylabel=r"$k_B T_e\ [\mathrm{eV}]$")
    log_ticks(ax.xaxis, 6, 32, 4)
    log_ticks(ax.yaxis, -2, 5)
    ax.grid(True, color="0.9", lw=0.5)
    return fig, ax


def label_along(ax, x0, text, f, color):
    """Label the curve T = f(n) at n = x0, rotated along it and just above it."""
    ax.figure.canvas.draw()
    p0 = ax.transData.transform((x0, f(x0)))
    p1 = ax.transData.transform((10 * x0, f(10 * x0)))
    angle = np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))
    offset = 5 * np.array([-np.sin(np.radians(angle)), np.cos(np.radians(angle))])
    ax.annotate(text, (x0, f(x0)), xytext=offset, textcoords="offset points",
                rotation=angle, rotation_mode="anchor", color=color, ha="center", va="bottom")


fig, _ = nt_axes()
save(fig, "nt_plane")

T_of_L = numeric(T_line_L, n0, L)
T_of_N1 = numeric(T_line_1, n0)
density = np.logspace(6, 32, 300)
fig, ax = nt_axes()
for size, text, at in [(1e-6, r"$\lambda_D = 1\,\mu\mathrm{m}$", 3e22),
                       (1e-2, r"$\lambda_D = 1\,\mathrm{cm}$", 3e14),
                       (1e2, r"$\lambda_D = 100\,\mathrm{m}$", 5e7)]:
    ax.plot(density, T_of_L(density, size), color=GRAY, ls="--", lw=0.9)
    label_along(ax, at, text, lambda n, size=size: T_of_L(n, size), GRAY)
ax.plot(density, T_of_N1(density), color=ORANGE)
ax.fill_between(density, 1e-3, T_of_N1(density), color=ORANGE, alpha=0.10, lw=0)
label_along(ax, 3e29, r"$N_D = 1$", T_of_N1, ORANGE)
ax.text(3e27, 2e-2, r"$N_D < 1$", color=ORANGE, va="bottom")
for name, (n_example, T_example) in EXAMPLE_PLASMAS.items():
    ax.plot(n_example, T_example, "o", ms=5, color=BLUE)
    ax.annotate(name, (n_example, T_example), xytext=(5, 0), textcoords="offset points",
                va="center", color="#1c1f23")
save(fig, "nt_map")

# %% Plot: Debye number against density at three temperatures
N_D_of = numeric(N_D_expr.subs(lambda_D, lambda_D_expr), n0, T_e)
kelvin_per_eV = float((e / k_B).subs(SI_VALUES))
fig, ax = figure(slide_width(6), 2.2)
for T_example, text, color, ls in [(1e4, r"$10\,\mathrm{keV}$", BLUE, "-"),
                                   (1e1, r"$10\,\mathrm{eV}$", ORANGE, "--"),
                                   (1e-1, r"$0.1\,\mathrm{eV}$", GRAY, ":")]:
    count_curve = N_D_of(density, T_example * kelvin_per_eV)
    ax.plot(density, count_curve, color=color, ls=ls)
    k = np.searchsorted(density, 1e8)
    # Labels above their curves; the lowest one in the free corner below it
    # (parallel lines leave no room for a level label between them).
    if T_example < 1:
        label(ax, 2e6, 10**2.2, text, color)
    else:
        label(ax, density[k], count_curve[k] * 60, text, color)
ax.axhline(1, color=ORANGE, lw=0.6)
ax.fill_between(density, 1e-6, 1, color=ORANGE, alpha=0.10, lw=0)
ax.set(xscale="log", yscale="log", xlim=(1e6, 1e32), ylim=(1e-4, 1e16),
       xlabel=r"$n_e\ [\mathrm{m^{-3}}]$", ylabel=r"$N_D$")
log_ticks(ax.xaxis, 6, 30, 8)
log_ticks(ax.yaxis, -4, 16, 4)
save(fig, "debye_number")

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 2 · Debye shielding")
