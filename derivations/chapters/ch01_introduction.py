# Chapter 1 · Introduction (src/chapters/01-introduction.typ)
#
# Charge density and quasineutrality, thermal speed, and the electron-volt as a
# temperature; the screened net charge, Maxwellian speeds and the scale
# ordering of five example plasmas, with their plots.
# `python ch01_introduction.py` prints every step.

# %% Setup
import sympy as sp
from sympy.physics import units as u

from notebook import agrees, close_to, evaluate, note, report, section, show
from si import check, e, k_B

m_s, T_s, v, n_e, n_i, Z, q_s, n_s = sp.symbols("m_s T_s v n_e n_i Z q_s n_s", positive=True)
rho_q, eps_kin, eps_th = sp.symbols("rho_q epsilon_kin epsilon_th")
v_th = sp.Symbol("v_th", positive=True)
SI_UNITS = {m_s: u.kilogram, T_s: u.kelvin, v: u.meter / u.second, n_e: u.meter**-3,
            n_i: u.meter**-3, q_s: u.coulomb, n_s: u.meter**-3, Z: 1}

# %% Charge density and quasineutrality
section("Charge density and quasineutrality", script="intro-plasma-state")
q_e, q_i = sp.symbols("q_e q_i")
note("Sum of", q_s * n_s, "over electrons and ions")
check(q_s * n_s, q_s * n_s, unit=u.coulomb / u.meter**3, units=SI_UNITS)
species_sum = show(sp.Eq(rho_q, q_e * n_e + q_i * n_i))
note("Electrons carry", sp.Eq(q_e, -e), "and ions of charge state", Z, "carry", sp.Eq(q_i, Z * e))
charge = show(species_sum.subs({q_e: -e, q_i: Z * e}))
agrees(charge.rhs, e * (Z * n_i - n_e), lhs=rho_q, eq="intro-quasineutrality")
check(charge.rhs, e * (Z * n_i - n_e), unit=u.coulomb / u.meter**3, units=SI_UNITS)
note("Quasineutrality", sp.Eq(rho_q, 0), "fixes the electron density")
n_e_neutral = sp.solve(charge.rhs, n_e)[0]
agrees(n_e_neutral, Z * n_i, lhs=n_e, eq="intro-quasineutrality")
note("Hydrogen,", sp.Eq(Z, 1))
agrees(n_e_neutral.subs(Z, 1), n_i, lhs=n_e, eq="intro-quasineutrality")

# %% Thermal energy and thermal speed
section("Thermal speed", script="intro-speed-energy-temperature")
note("Kinetic and thermal energy, both in joule")
kinetic = show(sp.Eq(eps_kin, m_s * v**2 / 2))
thermal = show(sp.Eq(eps_th, k_B * T_s))
check(kinetic.rhs, kinetic.rhs, unit=u.joule, units=SI_UNITS)
check(thermal.rhs, thermal.rhs, unit=u.joule, units=SI_UNITS)
note("Convention: the kinetic energy at the thermal speed equals", thermal.rhs)
convention = show(sp.Eq(kinetic.rhs.subs(v, v_th), thermal.rhs))
v_th_solved = sp.solve(convention, v_th)[0]
agrees(v_th_solved, sp.sqrt(2 * k_B * T_s / m_s), lhs=v_th, eq="intro-thermal-speed")
check(v_th_solved, v_th_solved, unit=u.meter / u.second, units=SI_UNITS)
note("Four times the energy doubles the speed")
agrees(v_th_solved.subs(T_s, 4 * T_s) / v_th_solved, 2,
       lhs=sp.Function("v_th")(4 * T_s) / sp.Function("v_th")(T_s))

# %% Worked example: electron-volt as a temperature
section("Electron-volt in kelvin", script="intro-speed-energy-temperature")
energy = sp.Symbol("epsilon", positive=True)
note("Temperature with", sp.Eq(k_B * T_s, energy))
kelvin_per_eV = evaluate(T_s, energy / k_B, {energy: 1 * u.electronvolt}, u.kelvin, digits=5)
close_to(kelvin_per_eV, 1.1605e4, rtol=1e-4)
kelvin_10eV = evaluate(T_s, energy / k_B, {energy: 10 * u.electronvolt}, u.kelvin)
close_to(kelvin_10eV, 1.16e5)

# %% Net charge around a screened point charge
section("Net charge around a screened point charge", script="intro-plasma-state")
from si import eps0

Q, r, lam_D = sp.symbols("Q r lambda_D", positive=True)
Q_enc = sp.Symbol("Q_enc")
SCREEN_UNITS = {Q: u.coulomb, r: u.meter, lam_D: u.meter}
note("Debye-screened potential of a point charge", Q, "(derived in chapter 2)")
phi_D = show(sp.Eq(sp.Symbol("phi"), Q * sp.exp(-r / lam_D) / (4 * sp.pi * eps0 * r)))
note("Gauss's law gives the net charge inside radius", r)
enclosed = sp.simplify(-4 * sp.pi * eps0 * r**2 * sp.diff(phi_D.rhs, r))
enclosed_stated = Q * (1 + r / lam_D) * sp.exp(-r / lam_D)
agrees(enclosed, enclosed_stated, source="fig. enclosed_charge", lhs=Q_enc)
check(enclosed, enclosed_stated, unit=u.coulomb, units=SCREEN_UNITS)
note("The screening cloud cancels the charge far from it")
agrees(sp.limit(enclosed, r, sp.oo), 0, source="fig. enclosed_charge", lhs=sp.Limit(Q_enc, r, sp.oo))
close_to(float((enclosed / Q).subs(r, 3 * lam_D)), 4 * float(sp.exp(-3)), rtol=1e-12)

# %% One velocity component: heating versus acceleration
section("Heating versus acceleration", script="intro-speed-energy-temperature")
v_x, u_s = sp.symbols("v_x u_s", real=True)
f_x = sp.Function("f")(v_x)
note("One velocity component of a Maxwellian drifting with bulk velocity", u_s)
maxwell_1d = show(sp.Eq(f_x, n_s / (sp.sqrt(sp.pi) * v_th) * sp.exp(-(v_x - u_s) ** 2 / v_th**2))).rhs
agrees(sp.integrate(maxwell_1d, (v_x, -sp.oo, sp.oo)), n_s, source="fig. maxwellian_heating", lhs=sp.Symbol("n_s"))
mean_vx = sp.simplify(sp.integrate(v_x * maxwell_1d, (v_x, -sp.oo, sp.oo)) / n_s)
agrees(mean_vx, u_s, source="fig. maxwellian_drift", lhs=sp.Symbol(r"\langle v_x \rangle"))
variance = sp.simplify(sp.integrate((v_x - u_s) ** 2 * maxwell_1d, (v_x, -sp.oo, sp.oo)) / n_s)
note("Velocity variance with", sp.Eq(v_th, v_th_solved))
agrees(variance.subs(v_th, v_th_solved), k_B * T_s / m_s,
       lhs=sp.Symbol(r"\langle (v_x - u_s)^2 \rangle"))
note("Heating", sp.Eq(T_s, 4 * T_s), "doubles the width; the mean stays", u_s)
agrees(v_th_solved.subs(T_s, 4 * T_s) / v_th_solved, 2, source="fig. maxwellian_heating",
       lhs=sp.Function("v_th")(4 * T_s) / sp.Function("v_th")(T_s))

# %% Speed distribution: v_th is the most probable speed, not the mean
section("Speeds of a Maxwellian", script="intro-speed-energy-temperature")
w = sp.Symbol("v", positive=True)
F_w = sp.Function("F")(w)
note("Isotropic Maxwellian at rest, distribution of speeds (normalized to 1)")
speed_pdf = show(sp.Eq(F_w, 4 * sp.pi * w**2 / (sp.pi ** sp.Rational(3, 2) * v_th**3)
                      * sp.exp(-w**2 / v_th**2))).rhs
agrees(sp.integrate(speed_pdf, (w, 0, sp.oo)), 1, source="fig. maxwell_speed", lhs=sp.Integral(F_w, (w, 0, sp.oo)))
peak = [s for s in sp.solve(sp.diff(speed_pdf, w), w) if s.is_positive]
agrees(peak[0], v_th, source="fig. maxwell_speed", lhs=sp.Symbol("v_peak"))
v_mean = sp.simplify(sp.integrate(w * speed_pdf, (w, 0, sp.oo)))
agrees(v_mean, 2 * v_th / sp.sqrt(sp.pi), source="fig. maxwell_speed", lhs=sp.Symbol(r"\langle v \rangle"))
agrees(v_mean.subs(v_th, v_th_solved), sp.sqrt(8 * k_B * T_s / (sp.pi * m_s)),
       lhs=sp.Symbol(r"\langle v \rangle"))
v_rms = sp.sqrt(sp.simplify(sp.integrate(w**2 * speed_pdf, (w, 0, sp.oo))))
agrees(v_rms, sp.sqrt(sp.Rational(3, 2)) * v_th, source="fig. maxwell_speed", lhs=sp.Symbol("v_rms"))
note("Mean kinetic energy", m_s * v_rms**2 / 2, "is", sp.Rational(3, 2) * k_B * T_s)
agrees((m_s * v_rms**2 / 2).subs(v_th, v_th_solved), sp.Rational(3, 2) * k_B * T_s,
       lhs=sp.Symbol(r"\langle \epsilon_{kin} \rangle"))

# %% Thermal speeds of electrons and protons
section("Thermal speed against temperature", script="intro-speed-energy-temperature")
eV = sp.Symbol("epsilon", positive=True)
m_p_sym = sp.Symbol("m_p", positive=True)
v_th_eV = sp.sqrt(2 * eV / m_s)
agrees(v_th_solved.subs(T_s, eV / k_B), v_th_eV, lhs=v_th, eq="intro-thermal-speed")
v_e_1eV = evaluate(sp.Symbol("v_th,e"), v_th_eV.subs(m_s, sp.Symbol("m_e", positive=True)),
                   {eV: 1 * u.electronvolt}, u.meter / u.second)
close_to(v_e_1eV, 5.93e5, rtol=1e-3, source="fig. thermal_speed")
v_p_1eV = evaluate(sp.Symbol("v_th,p"), v_th_eV.subs(m_s, m_p_sym),
                   {eV: 1 * u.electronvolt}, u.meter / u.second)
close_to(v_e_1eV / v_p_1eV, 42.85, rtol=1e-3, source="fig. thermal_speed")

# %% Characteristic scales of five example plasmas
import numpy as np

section("Characteristic scales of five example plasmas", script="intro-scales")
from si import m_e

n0, T_e, B0 = sp.symbols("n_0 T_e B_0", positive=True)
lnL = sp.Symbol("ln_Lambda", positive=True)
SCALE_UNITS = {n0: u.meter**-3, T_e: u.kelvin, B0: u.tesla, lnL: 1}
lambda_D_expr = sp.sqrt(eps0 * k_B * T_e / (n0 * e**2))
omega_pe_expr = sp.sqrt(n0 * e**2 / (eps0 * m_e))
omega_ce_expr = e * B0 / m_e
v_th_e = v_th_solved.subs({T_s: T_e, m_s: m_e})
rho_e_expr = v_th_e / omega_ce_expr
v_mean_e = v_mean.subs(v_th, v_th_e)
note("Electron-ion collision rate (Inan and Golkowski 2011, as in chapter 9)")
nu_ei_expr = (sp.sqrt(2) * omega_pe_expr**4 / (64 * sp.pi * n0)
              * (k_B * T_e / m_e) ** sp.Rational(-3, 2) * lnL)
mfp_expr = v_mean_e / nu_ei_expr
for name, expr, unit in [("lambda_D", lambda_D_expr, u.meter), ("rho_e", rho_e_expr, u.meter),
                         ("lambda_mfp", mfp_expr, u.meter), ("omega_pe", omega_pe_expr, u.second**-1),
                         ("omega_ce", omega_ce_expr, u.second**-1), ("nu_ei", nu_ei_expr, u.second**-1)]:
    show(sp.Eq(sp.Symbol(name), expr))
    check(expr, expr, unit=unit, units=SCALE_UNITS)
note("Chapter 9 example", sp.Eq(n0, 1e16 / u.meter**3, evaluate=False), "at 10 eV,",
     sp.Eq(lnL, sp.log(n0 * lambda_D_expr**3)))
example = {n0: 1.0e16 / u.meter**3, T_e: 1.602e-18 * u.joule / u.boltzmann_constant}
debye_example = evaluate(sp.Symbol("lambda_D"), lambda_D_expr, example, u.meter)
log_L = float(np.log(1.0e16 * debye_example**3))
close_to(evaluate(sp.Symbol("nu_ei"), nu_ei_expr, {**example, lnL: log_L}, u.second**-1),
         3.60e3)
close_to(evaluate(sp.Symbol("lambda_mfp"), mfp_expr, {**example, lnL: log_L}, u.meter),
         5.89e2)

# %% Plots: shared setup
from si import BLUE, EXAMPLE_PLASMAS, GRAY, ORANGE, SI_VALUES, figure, label, log_ticks, save, slide_width

INK = "#1c1f23"
# Widths fit the slide grid (si.slide_width): one panel of a pair or a summary
# plot spans 6 columns, a full plot page 8, the scale-ordering summary 12.
PANEL = (slide_width(6), 2.4)  # one panel of the side-by-side pair maxwellian_heating | maxwellian_drift

# %% Plot: net charge inside radius r around a point charge
screened_fraction = sp.lambdify(r, (enclosed / Q).subs(lam_D, 1), "numpy")
radius = np.linspace(0, 5, 300)
fig, ax = figure(slide_width(6), 2.0)
ax.axhline(1, color=ORANGE, ls="--")
ax.plot(radius, screened_fraction(radius), color=BLUE)
label(ax, 3.3, 1.03, "bare", ORANGE)
label(ax, 1.9, screened_fraction(1.9) + 0.04, "screened", BLUE)
ax.set(xlim=(0, 5), ylim=(0, 1.2), xticks=range(6),
       xlabel=r"$r/\lambda_D\ [1]$", ylabel=r"$Q_\mathrm{enc}/Q\ [1]$")
save(fig, "enclosed_charge")

# %% Plots: heating and acceleration of one velocity component
# v_x in units of the initial v_th, f in units of n_s / v_th (initial).
maxwell_curve = sp.lambdify((v_x, u_s, v_th), maxwell_1d.subs(n_s, 1), "numpy")
velocity = np.linspace(-4, 5, 400)


def velocity_panel(curves, name):
    fig, ax = figure(*PANEL)
    for (drift, width, color, ls, text, at) in curves:
        ax.plot(velocity, maxwell_curve(velocity, drift, width), color=color, ls=ls)
        label(ax, *at, text, color)
    ax.set(xlim=(-4, 5), ylim=(0, 0.65), xticks=[-4, -2, 0, 2, 4],
           xlabel=r"$v_x/v_\mathrm{th}\ [1]$", ylabel=r"$v_\mathrm{th} f/n\ [1]$")
    save(fig, name)


velocity_panel([(0, 1, BLUE, "-", r"$T$", (0.55, 0.5)), (0, 2, ORANGE, "--", r"$4T$", (1.9, 0.18))],
               "maxwellian_heating")
velocity_panel([(0, 1, BLUE, "-", r"$u = 0$", (-3.2, 0.2)), (2, 1, ORANGE, "--", r"$u = 2 v_\mathrm{th}$", (2.9, 0.45))],
               "maxwellian_drift")

# %% Plot: speed distribution with the most probable, mean and rms speed
speed_curve = sp.lambdify(w, (v_th * speed_pdf).subs(v_th, 1), "numpy")
speed = np.linspace(0, 3, 300)
fig, ax = figure(slide_width(6), 2.0)
ax.plot(speed, speed_curve(speed), color=BLUE)
for value, text, ls, y_text in [(1.0, r"$v_\mathrm{th}$", "-", 0.98),
                                (float(v_mean.subs(v_th, 1)), r"$\langle v \rangle$", "--", 0.78),
                                (float(v_rms.subs(v_th, 1)), r"$v_\mathrm{rms}$", ":", 0.58)]:
    ax.plot([value, value], [0, speed_curve(value)], color=INK, ls=ls, lw=1.0)
    ax.annotate(text, (value, speed_curve(value) * 0.55 if ls != "-" else speed_curve(value)),
                xytext=(1.85, y_text), color=INK, va="center",
                arrowprops={"arrowstyle": "-", "color": "0.6", "lw": 0.6})
ax.set(xlim=(0, 3), ylim=(0, 1.05), xticks=[0, 1, 2, 3],
       xlabel=r"$v/v_\mathrm{th}\ [1]$", ylabel=r"$v_\mathrm{th} F\ [1]$")
save(fig, "maxwell_speed")

# %% Plot: thermal speed against temperature, electrons and protons
J_PER_EV = 1.602176634e-19
PROTON = 1.67262192369e-27
kelvin_per_eV_value = J_PER_EV / SI_VALUES[k_B]
thermal = sp.lambdify((eV, m_s), v_th_eV, "numpy")
energy_eV = np.logspace(-2, 4, 200)
fig, ax = figure(slide_width(8), 3.0)
ax.plot(energy_eV, thermal(energy_eV * J_PER_EV, SI_VALUES[m_e]), color=BLUE)
ax.plot(energy_eV, thermal(energy_eV * J_PER_EV, PROTON), color=ORANGE, ls="--")
label(ax, 0.03, 2.2 * thermal(0.03 * J_PER_EV, SI_VALUES[m_e]), r"$v_{\mathrm{th},e}$", BLUE)
label(ax, 0.03, 2.2 * thermal(0.03 * J_PER_EV, PROTON), r"$v_{\mathrm{th},p}$", ORANGE)
ax.set(xscale="log", yscale="log", xlim=(1e-2, 1e4), ylim=(1e3, 1e8),
       xlabel=r"$k_B T\ [\mathrm{eV}]$", ylabel=r"$v_\mathrm{th}\ [\mathrm{m/s}]$")
log_ticks(ax.xaxis, -2, 4, 2)
log_ticks(ax.yaxis, 3, 8)
top = ax.secondary_xaxis("top", functions=(lambda x: x * kelvin_per_eV_value,
                                           lambda t: t / kelvin_per_eV_value))
top.set_xlabel(r"$T\ [\mathrm{K}]$")
log_ticks(top.xaxis, 2, 8, 2)
save(fig, "thermal_speed")

# %% Plot: length and frequency scales of five example plasmas
# Order-of-magnitude magnetic field B [T] and system size L [m] beside the
# (n_e, k_B T_e) of si.EXAMPLE_PLASMAS; each value is within a factor of ~3
# of the cited typical range. Sources:
# H II region: Faraday rotation through five large H II regions gives
#   B_par = 2 to 6 uG = 2e-10 to 6e-10 T (Harvey-Smith, Madsen and Gaensler,
#   ApJ 736, 83, 2011); sizes 0.5 pc (Orion) to ~5 pc (M17), 1 pc = 3.1e16 m.
# Ionosphere: geomagnetic field 2.5e-5 to 6.5e-5 T at the surface, 3.5e-5 T
#   at the equator in the lower ionosphere (NRL Plasma Formulary 2019, p. 41);
#   F region from ~150 km to ~500 km altitude, a layer of order 100 km
#   (NOAA NGDC, Definition of the Ionospheric Regions).
# Solar corona: active-region loop fields 4 to 100 G = 4e-4 to 1e-2 T and loop
#   lengths 60 to 350 Mm (Nakariakov and Ofman 2001; Aschwanden et al. 2008).
# Hall thruster: typical radial field 150 G = 0.015 T (Goebel and Katz 2008,
#   Sec. 7.2); channel width ~1.5 cm (SPT-100).
# Tokamak core: ITER B_T = 5.3 T at R_0 = 6.2 m, minor radius a = 2.0 m
#   (ITER Physics Basis, Nucl. Fusion 39, 2137, 1999).
FIELD_AND_SIZE = {
    "H II region": (5e-10, 3e16),
    "ionosphere": (5e-5, 1e5),
    "solar corona": (1e-3, 1e8),
    "Hall thruster": (2e-2, 1e-2),
    "tokamak core": (5.0, 2.0),
}
args = (n0, T_e, B0)
lnL_of = sp.lambdify((n0, T_e), sp.log(n0 * lambda_D_expr**3).subs(SI_VALUES), "numpy")
scale_fns = {key: sp.lambdify(args + (lnL,), expr.subs(SI_VALUES), "numpy") for key, expr in [
    ("lambda_D", lambda_D_expr), ("rho_e", rho_e_expr), ("mfp", mfp_expr),
    ("omega_pe", omega_pe_expr), ("omega_ce", omega_ce_expr), ("nu_ei", nu_ei_expr)]}
LENGTHS = [("lambda_D", r"$\lambda_D$", BLUE, "o"), ("rho_e", r"$\rho_e$", ORANGE, "^"),
           ("mfp", r"$\lambda_\mathrm{mfp}$", GRAY, "s"), ("L", r"$L$", INK, "|")]
RATES = [("omega_pe", r"$\omega_{pe}$", BLUE, "o"), ("omega_ce", r"$\omega_{ce}$", ORANGE, "^"),
         ("nu_ei", r"$\nu_{ei}$", GRAY, "s")]
fig, _ = figure(slide_width(12), 2.0)
fig.clf()
ax_len, ax_rate = fig.subplots(1, 2, sharey=True)
for row, (name, (B_ex, L_ex)) in enumerate(FIELD_AND_SIZE.items()):
    n_ex, T_eV = EXAMPLE_PLASMAS[name]
    T_K = T_eV * kelvin_per_eV_value
    values = {key: fn(n_ex, T_K, B_ex, lnL_of(n_ex, T_K)) for key, fn in scale_fns.items()}
    values["L"] = L_ex
    for ax, items in [(ax_len, LENGTHS), (ax_rate, RATES)]:
        xs = [values[key] for key, *_ in items]
        ax.plot([min(xs), max(xs)], [row, row], color="0.85", lw=0.8, zorder=0)
        for (key, text, color, marker), x in zip(items, xs):
            ax.plot(x, row, marker, color=color, ms=9 if marker == "|" else 5,
                    mew=1.6 if marker == "|" else 1.0)
            if row == 0:
                # Marker names above the top row, clear of the rows below.
                ax.annotate(text, (x, row), xytext=(0, 7), textcoords="offset points",
                            ha="center", va="bottom", color=color)
ax_len.set(xscale="log", xlim=(1e-6, 1e18), xlabel=r"$\ell\ [\mathrm{m}]$",
           yticks=range(len(FIELD_AND_SIZE)), yticklabels=list(FIELD_AND_SIZE), ylim=(4.5, -1.4))
ax_rate.set(xscale="log", xlim=(1e-3, 1e13), xlabel=r"$\omega,\ \nu\ [\mathrm{s^{-1}}]$")
log_ticks(ax_len.xaxis, -6, 18, 6)
log_ticks(ax_rate.xaxis, -3, 13, 4)
for ax in (ax_len, ax_rate):
    ax.tick_params(axis="y", length=0)
    ax.grid(True, axis="x", color="0.92", lw=0.5)
ax_rate.tick_params(axis="y", left=False)
save(fig, "scale_ordering")

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 1 · Introduction")
