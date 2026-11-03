#!/usr/bin/env python3
"""Nonlinear Poisson-Boltzmann screening of a test charge vs Debye-Hueckel.

Model (electrons Boltzmann, ions a fixed uniform background, mean field):

    phi = e Phi/(k_B T_e),  rho = r/lambda_D,  n_e/n_0 = exp(phi),
    (1/rho^2) d/drho (rho^2 dphi/drho) = exp(phi) - 1,

lambda_D^2 = eps_0 k_B T_e/(n_0 e^2).  Near a test charge q = s e (s = -1 or
+1) the potential is Coulomb, phi = s Lambda/rho, with

    Lambda = e^2/(4 pi eps_0 lambda_D k_B T_e) = 1/(4 pi n_0 lambda_D^3).

The charge is a sphere of radius a; the boundary condition there is the
enclosed charge, rho^2 dphi/drho |_{rho=a} = -s Lambda, and phi -> 0 far away.

q = -e: electrons are expelled, 0 < n_e < n_0, and the result does not depend
on a (cutoff_sensitivity); the linearised density 1 + phi turns negative.

q = +e: n_0 exp(Lambda/rho) is not integrable at rho -> 0, so a classical point
charge has no Boltzmann solution and the ion size enters.  Here the ion has the
Bohr radius a_0, so a/lambda_D = Lambda k_B T_e/E_h and phi(a) ~ E_h/k_B T_e
(Hartree energy E_h = e^2/(4 pi eps_0 a_0) = 27.2 eV); shown for
k_B T_e = ATOM_TEMPERATURE_EV.  The electrons piled up within a few a_0 are
classically what quantum mechanically is a bound state.

Linear (Debye-Hueckel) point-charge solution: phi_DH = s Lambda exp(-rho)/rho.
Shown for n_0 lambda_D^3 = 10, 1, 0.1.

Writes build/fig/debye_nonlinear_{potential,density}.{svg,pdf,png}.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp
from scipy.optimize import brentq

CUTOFF = 0.1                       # q = -e: charge radius a/(Lambda lambda_D) [1]
HARTREE_EV = 27.211                # E_h = e^2/(4 pi eps_0 a_0) [eV]
ATOM_TEMPERATURE_EV = 2.0          # q = +e: k_B T_e [eV]
RHO_MAX = 14.0                     # outer boundary r/lambda_D [1]
DEBYE_NUMBERS = (10.0, 1.0, 0.1)   # n_0 lambda_D^3 [1]
STRENGTHS = tuple(1 / (4 * np.pi * nd) for nd in DEBYE_NUMBERS)   # Lambda [1]
RHO_PLOT = (1e-3, 6.0)             # plotted r/lambda_D range [1]


def radius(strength, sign=-1, temperature_ev=ATOM_TEMPERATURE_EV):
    """Charge radius a/lambda_D: arbitrary small for q < 0, Bohr radius for q > 0."""
    return CUTOFF * strength if sign < 0 else strength * temperature_ev / HARTREE_EV


def solve(strength, sign=-1, a=None, rho_max=RHO_MAX):
    """Solve for phi(rho), y = (phi, rho^2 phi'); returns the bvp solution."""
    a = radius(strength, sign) if a is None else a

    def rhs(rho, y):
        phi = np.clip(y[0], -60, 60)
        return np.vstack([y[1] / rho**2, rho**2 * np.expm1(phi)])

    def bc(ya, yb):
        # inner: enclosed charge; outer: decaying exponential, phi' = -(1+1/rho) phi
        return np.array([ya[1] + sign * strength, yb[1] + (rho_max + 1) * yb[0]])

    rho = np.geomspace(a, rho_max, 800)
    phi0 = sign * strength * np.exp(-(rho - a)) / (rho * (1 + a))
    guess = np.vstack([phi0, -rho**2 * phi0 * (1 + 1 / rho)])
    sol = solve_bvp(rhs, bc, rho, guess, tol=1e-8, max_nodes=400000)
    if not sol.success:
        raise RuntimeError(f"Poisson-Boltzmann BVP failed for Lambda={strength}, sign={sign}: {sol.message}")
    sol.a, sol.sign = a, sign
    return sol


def debye_hueckel(rho, strength, sign=-1):
    return sign * strength * np.exp(-rho) / rho


def coulomb(rho, strength, sign=-1):
    return sign * strength / rho


def unit_crossing(sol):
    """rho_1 where |e Phi| = k_B T_e."""
    return brentq(lambda r: abs(sol.sol(r)[0]) - 1.0, sol.a, RHO_MAX)


def far_field_ratio(sol, strength, rho=(1.0, 2.0, 3.0)):
    """phi/phi_DH at a few Debye lengths (point-charge Debye-Hueckel)."""
    rho = np.asarray(rho)
    return sol.sol(rho)[0] / debye_hueckel(rho, strength, sol.sign)


def cutoff_sensitivity(strength, sign=-1, factor=2.0, rho=2.0):
    """Relative change of phi(rho) when the charge radius a shrinks by `factor`."""
    base = solve(strength, sign)
    small = solve(strength, sign, a=base.a / factor)
    return small.sol(rho)[0] / base.sol(rho)[0] - 1


def screening_charge(sol, strength, outer):
    """Electron charge between a and `outer`, in units of e: N_D-weighted integral of n_e/n_0 - 1."""
    x = np.geomspace(sol.a, outer, 200001)
    return np.trapezoid(x**2 * np.expm1(sol.sol(x)[0]), x) / strength


def electrons_near(sol, strength, outer):
    """Mean electron number between a and `outer`: 4 pi n_0 lambda_D^3 int rho^2 n_e/n_0."""
    x = np.geomspace(sol.a, outer, 200001)
    return np.trapezoid(x**2 * np.exp(sol.sol(x)[0]), x) / strength


def solutions(sign, strengths=STRENGTHS):
    return {lam: solve(lam, sign) for lam in strengths}


SHADES = dict(zip(STRENGTHS, ("#6baed6", "#2171b5", "#08306b")))
MARKS = dict(zip(STRENGTHS, ("o", "s", "^")))


def _nd(lam):
    return f"{1 / (4 * np.pi * lam):.2g}"


def plot():
    from matplotlib.lines import Line2D
    import matplotlib.pyplot as plt
    from si import figure, slide_width, ORANGE, GRAY

    neg, pos = solutions(-1), solutions(+1)
    width, height = slide_width(12), 2.6
    titles = (r"$q=-e$", rf"$q=+e$, ion radius $a_0$, $k_BT_e={ATOM_TEMPERATURE_EV:g}$ eV")
    style = [Line2D([], [], color="#2171b5", lw=2.4, label="Poisson–Boltzmann"),
             Line2D([], [], color=ORANGE, ls=(0, (4, 3)), lw=1.3, label="Debye–Hückel"),
             Line2D([], [], color="k", marker="o", ms=4.5, ls="", label=r"$|e\Phi|=k_BT_e$")]

    # --- potential relative to the bare Coulomb potential ---
    fig, _ = figure(width, height)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(width, height), sharey=True, layout="constrained")
    for ax, sols, title in zip(axes, (neg, pos), titles):
        rho = np.geomspace(*RHO_PLOT, 600)
        ax.plot(rho, np.exp(-rho), color=ORANGE, ls=(0, (4, 3)), lw=1.3, zorder=4)
        ax.axhline(1.0, color=GRAY, ls=":", lw=1.0)
        for lam, sol in sols.items():
            rho = np.geomspace(max(sol.a, RHO_PLOT[0]), RHO_PLOT[1], 600)
            ax.plot(rho, sol.sol(rho)[0] / coulomb(rho, lam, sol.sign), color=SHADES[lam], lw=2.4,
                    solid_capstyle="butt")
            r1 = unit_crossing(sol)
            ax.plot([r1], [sol.sol(r1)[0] / coulomb(r1, lam, sol.sign)], MARKS[lam], color="k", ms=4.5, zorder=5)
        ax.set(xscale="log", xlim=RHO_PLOT, ylim=(0, 1.08), xlabel=r"$r/\lambda_D\ [1]$", title=title)
        ax.title.set_fontsize(10)
    axes[0].set_ylabel(r"$\Phi/\Phi_{\mathrm{Coulomb}}\ [1]$")
    axes[0].legend(handles=style, loc="lower left", fontsize=8.5)
    axes[1].legend(handles=[Line2D([], [], color=SHADES[lam], lw=2.4, label=rf"$n_0\lambda_D^3={_nd(lam)}$")
                            for lam in STRENGTHS], loc="lower left", fontsize=8.5)
    save_all(fig, "debye_nonlinear_potential")

    # --- electron density ---
    fig, axes = plt.subplots(1, 2, figsize=(width, height), layout="constrained")
    for ax, sols, title in zip(axes, (neg, pos), titles):
        for lam, sol in sols.items():
            rho = np.geomspace(max(sol.a, RHO_PLOT[0]), RHO_PLOT[1], 600)
            ax.plot(rho, np.exp(sol.sol(rho)[0]), color=SHADES[lam], lw=2.4, solid_capstyle="butt")
            ax.plot(rho, 1 + debye_hueckel(rho, lam, sol.sign), color=ORANGE, ls=(0, (4, 3)), lw=1.1)
            r1 = unit_crossing(sol)
            ax.plot([r1], [np.exp(sol.sign)], MARKS[lam], color="k", ms=4.5, zorder=5)
        ax.set(xscale="log", xlim=RHO_PLOT, xlabel=r"$r/\lambda_D\ [1]$", title=title)
        ax.title.set_fontsize(10)
    axes[0].axhline(0.0, color="0.6", lw=0.7, zorder=0)
    axes[0].set(ylim=(-1.5, 1.15), ylabel=r"$n_e/n_0\ [1]$")
    axes[1].set(yscale="log", ylim=(0.5, 1e8))
    axes[1].legend(handles=[Line2D([], [], color=SHADES[lam], lw=2.4, label=rf"$n_0\lambda_D^3={_nd(lam)}$")
                            for lam in STRENGTHS]
                   + [Line2D([], [], color=ORANGE, ls=(0, (4, 3)), lw=1.1, label="linearised"),
                      style[2]], loc="upper right", fontsize=8.5)
    save_all(fig, "debye_nonlinear_density")
    return neg, pos


def save_all(fig, name):
    from si import save
    out = Path(__file__).resolve().parent / "build" / "fig"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.png", dpi=200, facecolor="white")
    save(fig, name)


def report(neg, pos):
    for label, sols in (("q=-e", neg), (f"q=+e, a=a_0, k_BT_e={ATOM_TEMPERATURE_EV:g} eV", pos)):
        for lam, sol in sols.items():
            print(f"{label} n0 lD^3={_nd(lam)}: a={sol.a:.2e} phi(a)={sol.sol(sol.a)[0]:+.1f} "
                  f"rho_1={unit_crossing(sol):.3e} phi/phi_DH at rho=1,2,3: "
                  + ", ".join(f"{x:.3f}" for x in far_field_ratio(sol, lam))
                  + f"  screening charge {screening_charge(sol, lam, RHO_MAX):+.4f}"
                  + f"  electrons within 2a: {electrons_near(sol, lam, 2 * sol.a):.3g}")


if __name__ == "__main__":
    report(*plot())
