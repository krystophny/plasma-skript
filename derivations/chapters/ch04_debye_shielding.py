# Chapter 4 · Debye shielding (src/chapters/04-debye-shielding.typ)
#
# Charge-separation scale, Debye length, screened point charge, Debye number
# and the n-T regime map.

# %% Setup
import sympy as sp
from sympy.physics import units as u

from notebook import agrees, note, report, section, show
from si import check, e, eps0, k_B, m_e

n0, T_e, Q, r, R, N, s = sp.symbols("n_0 T_e Q r R N s", positive=True)
lambda_D, a, L = sp.symbols("lambda_D a L", positive=True)
phi_0 = sp.Symbol("Phi", positive=True)  # local potential value, for the Boltzmann factor
phi = sp.Function("Phi")(r)
n_e, n_i, rho_q, E, W = sp.symbols("n_e n_i rho_q E W")
phi_inner = sp.Symbol("Phi_in")
SI_UNITS = {n0: u.meter**-3, T_e: u.kelvin, Q: u.coulomb, r: u.meter, R: u.meter,
            N: u.meter**-3, lambda_D: u.meter, a: u.meter,
            L: u.meter, phi_0: u.volt, rho_q: u.coulomb / u.meter**3}


def laplacian(f):
    """Radial part of the spherical Laplacian, unevaluated: f'' + 2 f'/r."""
    return sp.Derivative(f, (r, 2)) + 2 * sp.Derivative(f, r) / r


# %% Charge-separation scale
section("Charge-separation scale", script="debye-collective-validity")
note("Electrons removed from a sphere leave the charge density", N * e)
enclosed = show(sp.Eq(sp.Function("Q")(r), sp.Integral(4 * sp.pi * s**2 * N * e, (s, 0, r))))
Q_r = agrees(enclosed.rhs.doit(), sp.Rational(4, 3) * sp.pi * N * e * r**3, lhs=enclosed.lhs)
note("Gauss's law")
gauss = show(sp.Eq(4 * sp.pi * r**2 * eps0 * E, Q_r))
E_r = sp.solve(gauss, E)[0]
agrees(E_r, N * e * r / (3 * eps0), lhs=E)
check(E_r, N * e * r / (3 * eps0), unit=u.volt / u.meter, units=SI_UNITS)
note("Boundary potential against infinity; outside, the field is Coulomb")
boundary = show(sp.Eq(sp.Function("Phi")(R),
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
note("Inside the sphere, integrate the linear field inward from the boundary")
inside_sep = show(sp.Eq(phi_inner, phi_R + sp.Integral(E_r.subs(r, s), (s, r, R))))
phi_sep_in = agrees(sp.factor(inside_sep.rhs.doit()), N * e * (3 * R**2 - r**2) / (6 * eps0), lhs=phi_inner)
check(phi_sep_in, phi_sep_in, unit=u.volt, units=SI_UNITS)
phi_sep_out = Q_r.subs(r, R) / (4 * sp.pi * eps0 * r)
note("Neighbour energy at the mean spacing", sp.Eq(a, n0**sp.Rational(-1, 3)), "against the thermal energy")
coupling = (e**2 / (4 * sp.pi * eps0 * a) / (k_B * T_e)).subs(a, n0**sp.Rational(-1, 3))
agrees(sp.simplify(coupling - (a**2 / (4 * sp.pi * lambda_D**2)).subs(
    {a: n0**sp.Rational(-1, 3), lambda_D: sp.sqrt(eps0 * k_B * T_e / (n0 * e**2))})), 0,
    lhs=sp.Symbol("Gamma") - a**2 / (4 * sp.pi * lambda_D**2), eq="debye-coupling-estimate")

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

# %% Plasma frequency and Debye length
section("Plasma frequency and Debye length", script="intro-debye-shielding")
omega_pe, v_th = sp.symbols("omega_pe v_th", positive=True)
omega_pe_expr = sp.sqrt(n0 * e**2 / (eps0 * m_e))
definitions = {lambda_D: lambda_D_expr, omega_pe: omega_pe_expr, v_th: sp.sqrt(2 * k_B * T_e / m_e)}
for symbol, expr in definitions.items():
    show(sp.Eq(symbol, expr))
ratio = show(sp.Eq(v_th / (omega_pe * lambda_D),
                   sp.simplify((v_th / (omega_pe * lambda_D)).subs(definitions))))
assert ratio.rhs == sp.sqrt(2)
lambda_D_rel = sp.solve(ratio, lambda_D)[0]
agrees(lambda_D_rel, v_th / (sp.sqrt(2) * omega_pe), lhs=lambda_D, eq="debye-plasma-frequency-relation")
check(lambda_D_expr, lambda_D_rel.subs(definitions), unit=u.meter, units=SI_UNITS)
omega_pe_rel = sp.solve(ratio, omega_pe)[0]
agrees(omega_pe_rel, v_th / (sp.sqrt(2) * lambda_D), lhs=omega_pe)
check(omega_pe_expr, omega_pe_rel.subs(definitions), unit=1 / u.second, units=SI_UNITS)
v_th_alt = sp.sqrt(k_B * T_e / m_e)
note("With", sp.Eq(v_th, v_th_alt), "instead, the factor", sp.sqrt(2), "drops out")
ratio_alt = show(sp.Eq(ratio.lhs, sp.simplify(ratio.lhs.subs({**definitions, v_th: v_th_alt}))))
agrees(sp.solve(ratio_alt, lambda_D)[0], v_th / omega_pe, lhs=lambda_D)

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

# %% Dielectric function
section("Dielectric function", script="intro-debye-shielding")
kw = sp.Symbol("k", positive=True)
note("Fourier transform with the convention f(k) = integral of f(r) exp(-i k.r) over all space; for a radial f it reduces to the sine integral below")


def fourier_radial(f):
    return sp.simplify(sp.integrate(4 * sp.pi * r**2 * f * sp.sin(kw * r) / (kw * r), (r, 0, sp.oo), conds="none"))


phi_hat = agrees(fourier_radial(screened), Q / (eps0 * (kw**2 + 1 / lambda_D**2)), lhs=sp.Symbol(r"\hat{\Phi}"))
phi_hat_bare = Q / (eps0 * kw**2)
note("The bare Coulomb potential transforms to", phi_hat_bare)
epsilon_k = agrees(sp.simplify(phi_hat_bare / phi_hat), 1 + 1 / (kw**2 * lambda_D**2), lhs=sp.Symbol(r"\varepsilon(k)"))
surviving = agrees(sp.simplify(1 / epsilon_k), kw**2 / (kw**2 + 1 / lambda_D**2), lhs=1 / sp.Symbol(r"\varepsilon(k)"))
note("Induced charge from Poisson's equation in k-space,", sp.Eq(eps0 * kw**2 * sp.Symbol(r"\hat{\Phi}"), Q + sp.Symbol(r"\hat{\rho}_{\mathrm{ind}}")))
rho_ind_hat = agrees(sp.simplify(eps0 * kw**2 * phi_hat - Q), -Q / (1 + kw**2 * lambda_D**2), lhs=sp.Symbol(r"\hat{\rho}_{\mathrm{ind}}"))
agrees(sp.limit(rho_ind_hat, kw, 0), -Q, lhs=sp.Symbol(r"\hat{\rho}_{\mathrm{ind}}(0)"))
assert sp.limit(surviving, kw, 0) == 0 and sp.limit(surviving, kw, sp.oo) == 1
assert surviving.subs(kw, 1 / lambda_D) == sp.Rational(1, 2)

# %% Debye number and coupling
section("Debye number and coupling", script="debye-collective-validity")
N_D, Gamma = sp.symbols("N_D Gamma", positive=True)
note("Electrons in a Debye sphere")
count = show(sp.Eq(N_D, sp.Integral(4 * sp.pi * s**2 * n0, (s, 0, lambda_D))))
N_D_expr = agrees(count.rhs.doit(), sp.Rational(4, 3) * sp.pi * n0 * lambda_D**3, lhs=N_D)
check(N_D_expr, N_D_expr, unit=u.meter / u.meter, units=SI_UNITS)
note("Mean spacing: one particle per cube of edge", a)
spacing = show(sp.Eq(a**3 * n0, 1))
a_expr = agrees(sp.solve(spacing, a)[0], n0 ** sp.Rational(-1, 3), lhs=a)
check(a_expr, a_expr, unit=u.meter, units=SI_UNITS)
note("Coupling: Coulomb energy at that spacing over thermal energy")
coupling = show(sp.Eq(Gamma, e**2 / (4 * sp.pi * eps0 * a * k_B * T_e))).rhs
check(coupling.subs(a, a_expr), coupling.subs(a, a_expr), unit=u.meter / u.meter, units=SI_UNITS)
note("Weak coupling and a large Debye number are one condition:")
link = show(sp.Eq(Gamma * N_D ** sp.Rational(2, 3),
                  sp.simplify((coupling.subs(a, a_expr)
                               * N_D_expr.subs(lambda_D, lambda_D_expr) ** sp.Rational(2, 3)))))
assert link.rhs.free_symbols == set(), link
agrees(link.rhs, (36 * sp.pi) ** sp.Rational(-1, 3), lhs=Gamma * N_D ** sp.Rational(2, 3))

# %% Regime lines in the n-T plane
section("Regime lines in the n-T plane", script="debye-collective-validity")
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

# %% Degeneracy line in the n-T plane
section("Degeneracy line in the n-T plane", script="debye-collective-validity")
h_P, lambda_th = sp.symbols("h lambda_th", positive=True)
note("Thermal wavelength (chapter 2) and two spin states per electron state")
thermal_wavelength = show(sp.Eq(lambda_th, h_P / sp.sqrt(2 * sp.pi * m_e * k_B * T_e)))
degenerate = show(sp.Eq(n0 * thermal_wavelength.rhs**3, 2))
T_line_deg = agrees(sp.simplify(k_B * sp.solve(degenerate, T_e)[0] / e),
                    h_P**2 / (2 * sp.pi * m_e * e) * (n0 / 2) ** sp.Rational(2, 3), lhs=T_eV)
check(T_line_deg, T_line_deg, unit=u.volt, units={**SI_UNITS, h_P: u.joule * u.second})

# %% Plots: shared setup
import numpy as np

from si import BLUE, EXAMPLE_PLASMAS, GRAY, ORANGE, SI_VALUES, figure, label, log_ticks, save, slide_width

# Widths fit the slide grid (si.slide_width): one panel of the pair or a
# summary plot spans 6 columns, the n-T map 10.
PANEL = (slide_width(6), 2.4)  # one 6-column slide panel
# r in units of lambda_D, phi in units of Q/(4 pi eps0 lambda_D).
NORMALIZED = {Q: 1, eps0: 1 / (4 * sp.pi), lambda_D: 1}


def potential_axes(ax):
    ax.set(xlim=(0, 4), ylim=(0, 3.2), xticks=[0, 1, 2, 3, 4],
           xlabel=r"$r/\lambda_D$", ylabel=r"$4\pi\varepsilon_0\lambda_D\,\Phi/Q$")


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

# %% Plot: electron energy around a charge-separated sphere of radius sqrt(3) lambda_D
# Rigid model: electrons removed from r < R, no plasma response. eV units of k_B T_e.
SEPARATED = {N: n0, R: sp.sqrt(3) * lambda_D}
thermal = k_B * T_e
energy_in = sp.simplify((e * phi_sep_in / thermal).subs(SEPARATED).subs(lambda_D, lambda_D_expr).subs(r, r * lambda_D_expr))
energy_out = sp.simplify((e * phi_sep_out / thermal).subs(SEPARATED).subs(lambda_D, lambda_D_expr).subs(r, r * lambda_D_expr))
agrees(energy_in, (9 - r**2) / 6, lhs=e * phi_inner / thermal)
agrees(energy_out, sp.sqrt(3) / r, lhs=e * phi_inner / thermal)
R_sep = float(sp.sqrt(3))
separated = np.linspace(1e-6, 5, 500)
energy_curve = np.where(separated <= R_sep, sp.lambdify(r, energy_in, "numpy")(separated),
                        sp.lambdify(r, energy_out, "numpy")(separated))
fig, ax = figure(*PANEL)
ax.axhline(1, color=GRAY, lw=0.8, ls=":")
ax.axvline(R_sep, color="0.8", lw=0.6, zorder=0)
ax.plot(separated, energy_curve, color=BLUE)
ax.plot([R_sep], [1], "o", color=BLUE, ms=4)
ax.text(R_sep + 0.08, 1.62, r"$R=\sqrt{3}\,\lambda_D$", ha="left", va="top", color="0.4")
label(ax, 3.6, 1.04, r"$k_B T_e$", GRAY)
label(ax, 0.1, 0.78, r"$\propto 3R^2-r^2$", BLUE)
label(ax, 2.6, 0.72, r"$\propto 1/r$", BLUE)
ax.set(xlim=(0, 5), ylim=(0, 1.65), xticks=[0, 1, 2, 3, 4, 5],
       xlabel=r"$r/\lambda_D$", ylabel=r"$e\Phi/(k_B T_e)$")
save(fig, "charge_separation_energy")

# %% Plots: n-T plane and regime map


def numeric(expr, *args):
    """lambdify expr in args with SI constants substituted."""
    return sp.lambdify(args, expr.subs(SI_VALUES), "numpy")


def nt_axes():
    fig, ax = figure(slide_width(10), 2.7)
    ax.set(xscale="log", yscale="log", xlim=(1e6, 1e32), ylim=(1e-2, 1e5),
           xlabel=r"$n_e\ [\mathrm{m^{-3}}]$", ylabel=r"$k_B T_e\ [\mathrm{eV}]$")
    log_ticks(ax.xaxis, 6, 32, 4)
    log_ticks(ax.yaxis, -2, 5)
    ax.grid(True, color="0.9", lw=0.5)
    return fig, ax


def label_along(ax, x0, text, f, color, side=1):
    """Label the curve T = f(n) at n = x0, rotated along it and just above it."""
    ax.figure.canvas.draw()
    p0 = ax.transData.transform((x0, f(x0)))
    p1 = ax.transData.transform((10 * x0, f(10 * x0)))
    angle = np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))
    offset = side * 7 * np.array([-np.sin(np.radians(angle)), np.cos(np.radians(angle))])
    ax.annotate(text, (x0, f(x0)), xytext=offset, textcoords="offset points",
                rotation=angle, rotation_mode="anchor", color=color, ha="center",
                va="bottom" if side > 0 else "top")


fig, ax = nt_axes()
for name, (n_example, T_example) in EXAMPLE_PLASMAS.items():
    ax.plot(n_example, T_example, "o", ms=5, color=BLUE)
    ax.annotate(name, (n_example, T_example), xytext=(5, 0),
                textcoords="offset points", va="center")
save(fig, "nt_plane")

T_of_L = numeric(T_line_L, n0, L)
T_of_N1 = numeric(T_line_1, n0)
density = np.logspace(6, 32, 300)
fig, ax = nt_axes()
for size, text, at in [(1e-6, r"$\lambda_D = 1\,\mu\mathrm{m}$", 1e20),
                       (1e-2, r"$\lambda_D = 1\,\mathrm{cm}$", 3e14),
                       (1e2, r"$\lambda_D = 100\,\mathrm{m}$", 1.5e7)]:
    ax.plot(density, T_of_L(density, size), color=GRAY, ls="--", lw=0.9)
    label_along(ax, at, text, lambda n, size=size: T_of_L(n, size), GRAY,
                side=-1 if size > 1 else 1)
ax.plot(density, T_of_N1(density), color=ORANGE)
ax.fill_between(density, 1e-3, T_of_N1(density), color=ORANGE, alpha=0.10, lw=0)
label_along(ax, 1e28, r"$N_D = 1$", T_of_N1, ORANGE)
ax.text(2e20, 1.2e-2, r"$N_D < 1$", color=ORANGE, va="bottom")
T_of_deg = sp.lambdify(n0, T_line_deg.subs({**SI_VALUES, h_P: 6.62607015e-34}), "numpy")
ax.plot(density, T_of_deg(density), color="#1c1f23", ls="-.", lw=0.9)
label_along(ax, 3e26, r"$n_e \lambda_{\mathrm{th},e}^3 = 2$", T_of_deg, "#1c1f23")
ax.text(6e31, 1e-1, "quantum\ndegenerate", color="#1c1f23", va="bottom", ha="right")
# Dense examples (n_e [m^-3], k_B T_e [eV], label side): copper conduction
# electrons at room temperature (Kittel, Introduction to Solid State Physics,
# free-electron table); solar core from the standard solar model (central
# T = 15.7 MK, n_e ~ 6e31 m^-3); ICF hot spot at ignition (rho ~ 100 g/cm^3
# DT, T ~ 5 keV). Order of magnitude only.
DENSE_PLASMAS = {
    "metal electrons": (8.5e28, 2.5e-2, "above"),
    "solar core": (6e31, 1.35e3, "left"),
    "ICF hot spot": (2e31, 5e3, "left"),
}
# Label placement keeps every name clear of the lambda_D and regime lines.
MAP_LABELS = {  # name: (text, dx, dy, ha, va)
    "ionosphere": ("ionosphere", 5, 0, "left", "center"),
    "H II region": ("H II\nregion", -5, 0, "right", "center"),
    "solar corona": ("solar corona", 5, 0, "left", "center"),
    "Hall thruster": ("Hall\nthruster", -5, 0, "right", "top"),
    "tokamak core": ("tokamak core", 0, 5, "center", "bottom"),
    "metal electrons": ("metals", 5, 0, "left", "center"),
    "solar core": ("solar core", -5, 0, "right", "center"),
    "ICF hot spot": ("ICF hot spot", -5, 0, "right", "center"),
}
points = {**{k: v for k, v in EXAMPLE_PLASMAS.items()},
          **{k: v[:2] for k, v in DENSE_PLASMAS.items()}}
for name, (n_example, T_example) in points.items():
    text, dx, dy, ha, va = MAP_LABELS[name]
    ax.plot(n_example, T_example, "o", ms=5, color=BLUE)
    ax.annotate(text, (n_example, T_example), xytext=(dx, dy), textcoords="offset points",
                ha=ha, va=va, color="#1c1f23", linespacing=0.95)
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

# %% Plot: surviving fraction 1/epsilon(k) of a charge pattern
# k in units of 1/lambda_D.
wavenumber = np.geomspace(1e-2, 1e2, 400)
surviving_curve = sp.lambdify(kw, surviving.subs(lambda_D, 1), "numpy")
fig, ax = figure(*PANEL)
ax.plot(wavenumber, surviving_curve(wavenumber), color=BLUE)
ax.plot([1], [0.5], "o", color=BLUE, ms=4)
label(ax, 0.7, 0.52, r"half at $k\lambda_D = 1$", BLUE, ha="right")
label(ax, 1.3e-2, 0.08, "screened", GRAY)
label(ax, 90, 0.9, "unscreened", GRAY, ha="right", va="top")
ax.set(xscale="log", xlim=(1e-2, 1e2), ylim=(0, 1.05), yticks=[0, 0.5, 1],
       xlabel=r"$k\lambda_D$", ylabel=r"$1/\varepsilon(k)$")
log_ticks(ax.xaxis, -2, 2)
save(fig, "debye_surviving_fraction")

# %% Plot: bare and screened potential in k-space
# Phi_hat in units of Q lambda_D^2/eps0.
bare_k = sp.lambdify(kw, (phi_hat_bare * eps0 / (Q * lambda_D**2)).subs(lambda_D, 1), "numpy")
screened_k = sp.lambdify(kw, (phi_hat * eps0 / (Q * lambda_D**2)).subs(lambda_D, 1), "numpy")
fig, ax = figure(*PANEL)
ax.plot(wavenumber, bare_k(wavenumber), color=ORANGE, ls="--")
ax.plot(wavenumber, screened_k(wavenumber), color=BLUE)
label(ax, 0.25, 3e2, r"bare $\propto 1/k^2$", ORANGE)
label(ax, 1.3e-2, 1.6, "screened", BLUE)
ax.set(xscale="log", yscale="log", xlim=(1e-2, 1e2), ylim=(1e-4, 1e4),
       xlabel=r"$k\lambda_D$", ylabel=r"$\varepsilon_0\hat{\Phi}/(Q\lambda_D^2)$")
log_ticks(ax.xaxis, -2, 2)
log_ticks(ax.yaxis, -4, 4, 2)
save(fig, "debye_potential_k")

# %% Example plasmas: Debye length, plasma frequency, Debye number
import json
from pathlib import Path

lambda_D_of = numeric(lambda_D_expr, n0, T_e)
omega_pe_of = numeric(omega_pe_expr, n0)
scale_examples = []
for name in ["H II region", "ionosphere", "solar corona", "Hall thruster", "tokamak core"]:
    density_example, T_eV_example = EXAMPLE_PLASMAS[name]
    T_K = T_eV_example * kelvin_per_eV
    scale_examples.append(dict(name=name, n=density_example, T_eV=T_eV_example,
                               lambda_D=float(lambda_D_of(density_example, T_K)),
                               omega_pe=float(omega_pe_of(density_example)),
                               N_D=float(N_D_of(density_example, T_K))))
tokamak = scale_examples[-1]
assert abs(tokamak["lambda_D"] / 7.43e-5 - 1) < 0.01 and abs(tokamak["omega_pe"] / 5.64e11 - 1) < 0.01
Path("build").mkdir(exist_ok=True)
Path("build/debye-scales.json").write_text(json.dumps(scale_examples, indent=2))

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 3 · Debye shielding")
