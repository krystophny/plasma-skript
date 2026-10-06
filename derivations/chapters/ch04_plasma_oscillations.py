# Chapter 4 · Plasma oscillations (src/chapters/04-plasma-oscillations.typ)
#
# Charge-separation field of a displaced electron slab, the electron plasma
# oscillation, species plasma frequencies and the link to the Debye length.

# %% Setup
import sympy as sp
from sympy.physics import units as u

from notebook import agrees, note, report, section, show
from si import c, check, e, eps0, k_B, m_e

n0, xi0, x, t, T_e, L = sp.symbols("n_0 xi x t T_e L", positive=True)
n_s, q_s, m_s = sp.symbols("n_s q_s m_s", positive=True)
omega_pe, omega_ps, lambda_D, v_th = sp.symbols("omega_pe omega_ps lambda_D v_th", positive=True)
sigma, E, f_ps, d_s = sp.symbols("sigma E f_ps d_s")
xi = sp.Function("xi")(t)
SI_UNITS = {n0: u.meter**-3, xi0: u.meter, x: u.meter, t: u.second, T_e: u.kelvin,
            n_s: u.meter**-3, q_s: u.coulomb, m_s: u.kilogram}

# %% Charge-separation field
section("Charge-separation field", script="intro-plasma-oscillations")
note("Electrons shifted by", xi0, "leave an ion sheet at", sp.Eq(x, 0, evaluate=False),
     "and an electron sheet at", sp.Eq(x, L))
sheet = show(sp.Eq(sigma, e * n0 * xi0))
x_0 = sp.Symbol("x_0")
note("A sheet at", x_0, "has the field", sigma / (2 * eps0) * sp.sign(x - x_0))


def sheet_field(position, charge):
    return charge / (2 * eps0) * sp.sign(x - position)


two_sheets = show(sp.Eq(E, sheet_field(0, sigma) + sheet_field(L, -sigma)))
note("Between the sheets,", sp.Eq(x, L / 2))
inside = two_sheets.rhs.subs({x: L / 2, sigma: sheet.rhs})
agrees(inside, e * n0 * xi0 / eps0, lhs=E)
check(inside, e * n0 * xi0 / eps0, unit=u.volt / u.meter, units=SI_UNITS)
note("Outside the slab the sheet fields cancel:")
outside = show(sp.Eq(E, two_sheets.rhs.subs(x, 2 * L)))
assert outside.rhs == 0

# %% Electron plasma oscillation
section("Electron plasma oscillation", script="intro-plasma-oscillations")
note("Newton for an electron in the field", sp.Eq(E, e * n0 * xi / eps0))
newton = sp.Eq(m_e * sp.Derivative(xi, t, 2), -e * (e * n0 * xi / eps0))
agrees(newton.rhs, -(n0 * e**2) / eps0 * xi, lhs=newton.lhs)
note("Divide by", m_e * xi, "and compare with", sp.Eq(sp.Derivative(xi, t, 2) + omega_pe**2 * xi, 0))
omega_sq = show(sp.Eq(omega_pe**2, -newton.rhs / (m_e * xi))).rhs
omega_pe_expr = agrees(sp.sqrt(omega_sq), sp.sqrt(n0 * e**2 / (eps0 * m_e)), lhs=omega_pe)
check(sp.sqrt(omega_sq), omega_pe_expr, unit=1 / u.second, units=SI_UNITS)
oscillator = show(sp.Eq(newton.lhs / m_e, (newton.rhs / m_e).subs(omega_sq, omega_pe**2)))
assert oscillator.rhs == -omega_pe**2 * xi
general = show(sp.dsolve(oscillator, xi))
assert general.rhs.subs(omega_pe, omega_pe_expr).has(sp.sin(omega_pe_expr * t))
delta, amplitude = sp.symbols("delta xi_0")
trial = amplitude * sp.cos(omega_pe_expr * t + delta)  # amplitude-phase form
assert sp.simplify(m_e * trial.diff(t, 2) + e**2 * n0 / eps0 * trial) == 0

# %% Species plasma frequency
section("Species plasma frequency", script="intro-plasma-oscillations")
note("Same oscillator for species", sp.Symbol("s"), "with charge", q_s, ", density", n_s, ", mass", m_s)
species = show(newton.subs({e: q_s, n0: n_s, m_e: m_s}))
omega_ps_expr = sp.sqrt(-species.rhs / (m_s * xi))
agrees(omega_ps_expr, sp.sqrt(n_s * q_s**2 / (eps0 * m_s)), lhs=omega_ps)
check(omega_ps_expr.subs({n_s: n0, q_s: e, m_s: m_e}), omega_pe_expr,
      unit=1 / u.second, units=SI_UNITS)
frequency = show(sp.Eq(f_ps, omega_ps / (2 * sp.pi)))
check(frequency.rhs.subs(omega_ps, omega_ps_expr), frequency.rhs.subs(omega_ps, omega_ps_expr),
      unit=u.hertz, units=SI_UNITS)

# %% Plasma frequency and Debye length
section("Plasma frequency and Debye length", script="intro-plasma-oscillations")
definitions = {lambda_D: sp.sqrt(eps0 * k_B * T_e / (n0 * e**2)),
               omega_pe: omega_pe_expr, v_th: sp.sqrt(2 * k_B * T_e / m_e)}
for symbol, expr in definitions.items():
    show(sp.Eq(symbol, expr))
ratio = show(sp.Eq(v_th / (omega_pe * lambda_D),
                   sp.simplify((v_th / (omega_pe * lambda_D)).subs(definitions))))
assert ratio.rhs == sp.sqrt(2)
lambda_D_rel = sp.solve(ratio, lambda_D)[0]
agrees(lambda_D_rel, v_th / (sp.sqrt(2) * omega_pe), lhs=lambda_D)
check(definitions[lambda_D], lambda_D_rel.subs(definitions), unit=u.meter, units=SI_UNITS)
omega_pe_rel = sp.solve(ratio, omega_pe)[0]
agrees(omega_pe_rel, v_th / (sp.sqrt(2) * lambda_D), lhs=omega_pe)
check(omega_pe_expr, omega_pe_rel.subs(definitions), unit=1 / u.second, units=SI_UNITS)
v_th_alt = sp.sqrt(k_B * T_e / m_e)
note("With", sp.Eq(v_th, v_th_alt), "instead, the factor", sp.sqrt(2), "drops out")
ratio_alt = show(sp.Eq(ratio.lhs, sp.simplify(ratio.lhs.subs({**definitions, v_th: v_th_alt}))))
agrees(sp.solve(ratio_alt, lambda_D)[0], v_th / omega_pe, lhs=lambda_D)

# %% Inertial length
section("Inertial length", script="intro-plasma-oscillations")
inertial = show(sp.Eq(d_s, c / omega_ps))
check(inertial.rhs.subs(omega_ps, omega_ps_expr), inertial.rhs.subs(omega_ps, omega_ps_expr),
      unit=u.meter, units=SI_UNITS)

# %% Plot: plasma frequency against density
import numpy as np

from si import BLUE, EXAMPLE_PLASMAS, SI_VALUES, figure, log_ticks, save, slide_width

f_pe = sp.lambdify(n0, (omega_pe_expr / (2 * sp.pi)).subs(SI_VALUES), "numpy")
density = np.logspace(6, 32, 200)
# 6 slide-grid columns (si.slide_width): the summary plot of the deck.
fig, ax = figure(slide_width(6), 2.2)
for f, text in [(1e6, "MHz"), (1e9, "GHz"), (1e12, "THz")]:
    ax.axhline(f, color="0.85", lw=0.6, zorder=0)
    ax.text(1.5e6, f * 1.6, text, color="0.4", va="bottom")
ax.plot(density, f_pe(density), color=BLUE)
for name, (n_example, _) in EXAMPLE_PLASMAS.items():
    ax.plot(n_example, f_pe(n_example), "o", ms=4, color="#1c1f23")
    # The top point is labelled above the curve, clear of its neighbour.
    above = name == "tokamak core"
    ax.annotate(name, (n_example, f_pe(n_example)), textcoords="offset points",
                xytext=(-6, 3) if above else (5, -3), ha="right" if above else "left",
                va="bottom" if above else "top")
ax.plot(1e29, f_pe(1e29), "s", ms=4, color=BLUE)
ax.annotate("metal electrons", (1e29, f_pe(1e29)), xytext=(-5, 8),
            textcoords="offset points", ha="right", color=BLUE)
ax.set(xscale="log", yscale="log", xlim=(1e6, 1e32), ylim=(1e3, 1e17),
       xlabel=r"$n_e\ [\mathrm{m^{-3}}]$", ylabel=r"$f_{pe}\ [\mathrm{Hz}]$")
log_ticks(ax.xaxis, 6, 30, 8)
log_ticks(ax.yaxis, 3, 15, 3)
save(fig, "plasma_frequency")

# %% Independent numerical frequency/time estimates
import json
from pathlib import Path

omega_numeric = sp.lambdify(n0, omega_pe_expr.subs(SI_VALUES), "numpy")
frequency_examples = []
for name, density_example in [("metal", 1e29), ("fusion", 1e20)]:
    w = float(omega_numeric(density_example))
    frequency_examples.append(dict(name=name, n=density_example, omega=w,
                                   f=w/(2*np.pi), inverse=1/w, period=2*np.pi/w))
Path("build").mkdir(exist_ok=True)
Path("build/plasma-frequency.json").write_text(json.dumps(frequency_examples, indent=2))

# %% Cold unmagnetized transverse waves (reference wave chapter)
section("Electromagnetic cutoff", script="intro-plasma-oscillations")
k, omega = sp.symbols("k omega", positive=True)
dispersion = omega_pe**2 + c**2*k**2
assert sp.diff(dispersion, k) == 2*c**2*k
assert dispersion.subs(k, 0) == omega_pe**2


def plot_cold_em_dispersion():
    """Cutoff and vacuum line; both axes have explicitly normalized unit [1]."""
    q = np.linspace(0, 4, 300)
    fig, ax = figure(slide_width(6), 2.5)
    ax.plot(q, np.sqrt(1+q*q), color=BLUE, label="plasma")
    ax.plot(q, q, color="0.4", ls="--", label="vacuum")
    ax.axhline(1, color="0.65", ls=":")
    ax.set(xlabel=r"$ck/\omega_{pe}$ [1]", ylabel=r"$\omega/\omega_{pe}$ [1]",
           xlim=(0,4), ylim=(0,4.5))
    ax.legend(loc="upper left")
    save(fig, "cold_em_dispersion")


plot_cold_em_dispersion()

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 4 · Plasma oscillations")
