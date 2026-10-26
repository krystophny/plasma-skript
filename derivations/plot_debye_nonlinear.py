#!/usr/bin/env python3
"""Nonlinear Poisson-Boltzmann screening of a positive charge vs Debye-Hueckel.

Model (electrons Boltzmann, ions a fixed uniform background, mean field):

    phi = e Phi/(k_B T_e),  rho = r/lambda_D,  n_e/n_0 = exp(phi),
    (1/rho^2) d/drho (rho^2 dphi/drho) = exp(phi) - 1,

lambda_D^2 = eps_0 k_B T_e/(n_0 e^2).  Near a point charge q the potential is
Coulomb, phi = Lambda/rho, with

    Lambda = q e/(4 pi eps_0 lambda_D k_B T_e) = (q/e)/(4 pi n_0 lambda_D^3),

so ePhi = k_B T_e at rho_1 ~ Lambda: for q = e this is the Landau length
e^2/(4 pi eps_0 k_B T_e), far inside the Debye sphere when n_0 lambda_D^3 >> 1.
For q > 0 a strict point charge has no solution: n_e = n_0 exp(Lambda/rho) is
not integrable at rho -> 0 (classical collapse onto the charge).  The charge
is therefore a sphere of radius a = CUTOFF Lambda, where phi ~ 1/CUTOFF = 10;
the boundary condition there is the enclosed charge,

    rho^2 dphi/drho |_{rho=a} = -Lambda,     phi -> 0 far away.

Outside rho ~ a the result depends on a only at order Lambda^2
(cutoff_sensitivity).  Linear (Debye-Hueckel) solution of the same problem:
phi_DH = Lambda exp(-(rho - a))/(rho (1 + a)), for a << 1 Lambda exp(-rho)/rho.
Coulomb: phi_C = Lambda/rho.

Writes build/fig/debye_nonlinear_{potential,density}.{svg,pdf,png}.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp, quad
from scipy.optimize import brentq

CUTOFF = 0.1                       # charge radius a/(Lambda lambda_D) [1]
RHO_MAX = 14.0                     # outer boundary r/lambda_D [1]
STRENGTHS = (1e-4, 1e-3, 1e-2)     # Lambda [1]; q = e: N_D = n_0 lambda_D^3 = 800, 80, 8
RHO_PLOT = (1e-5, 8.0)             # plotted r/lambda_D range [1]


def radius(strength, cutoff=CUTOFF):
    return cutoff * strength


def solve(strength, a=None, rho_max=RHO_MAX):
    """Solve for phi(rho), y = (phi, rho^2 phi'); returns the bvp solution."""
    a = radius(strength) if a is None else a

    def rhs(rho, y):
        phi = np.clip(y[0], -60, 60)
        return np.vstack([y[1] / rho**2, rho**2 * np.expm1(phi)])

    def bc(ya, yb):
        # inner: enclosed charge; outer: decaying exponential, phi' = -(1+1/rho) phi
        return np.array([ya[1] + strength, yb[1] + (rho_max + 1) * yb[0]])

    rho = np.geomspace(a, rho_max, 800)
    phi0 = debye_hueckel(rho, strength, a)
    guess = np.vstack([phi0, -rho**2 * phi0 * (1 + 1 / rho)])
    sol = solve_bvp(rhs, bc, rho, guess, tol=1e-8, max_nodes=200000)
    if not sol.success:
        raise RuntimeError(f"Poisson-Boltzmann BVP failed for Lambda={strength}: {sol.message}")
    sol.a = a
    return sol


def debye_hueckel(rho, strength, a=0.0):
    return strength * np.exp(-(rho - a)) / (rho * (1 + a))


def coulomb(rho, strength):
    return strength / rho


def unit_crossing(sol):
    """rho_1 where the exact potential equals k_B T_e/e (phi = 1)."""
    return brentq(lambda r: sol.sol(r)[0] - 1.0, sol.a, RHO_MAX)


def far_field_ratio(sol, strength, rho=(1.0, 2.0, 3.0)):
    """phi/phi_DH at a few Debye lengths (point-charge Debye-Hueckel)."""
    rho = np.asarray(rho)
    return sol.sol(rho)[0] / debye_hueckel(rho, strength)


def cutoff_sensitivity(strength, factor=2.0, rho=2.0):
    """Relative change of phi(rho) when the charge radius a shrinks by `factor`."""
    base = solve(strength)
    small = solve(strength, a=radius(strength) / factor)
    return small.sol(rho)[0] / base.sol(rho)[0] - 1


def electrons_inside(sol, strength, rho_1, n_debye=None):
    """Mean electron number inside rho_1 for q = e: 4 pi N_D int rho^2 e^phi.

    For q = e, Lambda = 1/(4 pi N_D) with N_D = n_0 lambda_D^3.
    """
    n_debye = 1 / (4 * np.pi * strength) if n_debye is None else n_debye
    integral = quad(lambda r: r**2 * np.exp(sol.sol(r)[0]), sol.a, rho_1, limit=200)[0]
    return 4 * np.pi * n_debye * integral


def solutions(strengths=STRENGTHS):
    return {lam: solve(lam) for lam in strengths}


SHADES = {1e-4: "#6baed6", 1e-3: "#2171b5", 1e-2: "#08306b"}
MARKS = {1e-4: "o", 1e-3: "s", 1e-2: "^"}


def _lam_tex(lam):
    return rf"$\Lambda=10^{{{int(round(np.log10(lam)))}}}$"


def plot():
    from matplotlib.lines import Line2D
    from si import figure, slide_width, ORANGE, GRAY

    sols = solutions()
    width, height = slide_width(8), 3.0

    # --- potential ---
    fig, ax = figure(width, height)
    for lam, sol in sols.items():
        rho = np.geomspace(sol.a, RHO_PLOT[1], 600)
        ax.plot(rho, coulomb(rho, lam), color=GRAY, ls=":", lw=1.2)
        ax.plot(rho, sol.sol(rho)[0], color=SHADES[lam], lw=2.4, solid_capstyle="butt")
        ax.plot(rho, debye_hueckel(rho, lam), color=ORANGE, ls=(0, (4, 3)), lw=1.1)
        r1 = unit_crossing(sol)
        ax.plot([r1], [1.0], MARKS[lam], color="k", ms=5, zorder=5)
        ax.text(1.15 * sol.a, 14, _lam_tex(lam), color=SHADES[lam], fontsize=9, ha="left", va="bottom")
    ax.axhline(1.0, color="0.6", lw=0.7, zorder=0)
    ax.text(7.5, 0.8, r"$e\Phi=k_BT_e$", color="0.35", fontsize=9, ha="right", va="top")
    ax.set(xscale="log", yscale="log", xlim=RHO_PLOT, ylim=(1e-7, 1e2),
           xlabel=r"$r/\lambda_D\ [1]$", ylabel=r"$e\Phi/k_BT_e\ [1]$")
    ax.legend(handles=[
        Line2D([], [], color="#4292c6", lw=2.4, label="Poisson–Boltzmann (exact)"),
        Line2D([], [], color=ORANGE, ls=(0, (4, 3)), lw=1.1, label="Debye–Hückel (linear)"),
        Line2D([], [], color=GRAY, ls=":", lw=1.0, label="bare Coulomb"),
        Line2D([], [], color="k", marker="o", ms=5, ls="", label=r"$e\Phi=k_BT_e$")],
        loc="lower left", fontsize=8.5, title=r"$q=e$: $n_0\lambda_D^3=1/(4\pi\Lambda)$", title_fontsize=8.5)
    save_all(fig, "debye_nonlinear_potential")

    # --- excess electron density ---
    fig, ax = figure(width, height)
    for lam, sol in sols.items():
        rho = np.geomspace(sol.a, RHO_PLOT[1], 600)
        phi = sol.sol(rho)[0]
        ax.plot(rho, np.expm1(phi), color=SHADES[lam], lw=2.4, solid_capstyle="butt")
        ax.plot(rho, debye_hueckel(rho, lam), color=ORANGE, ls=(0, (4, 3)), lw=1.1)
        r1 = unit_crossing(sol)
        ax.plot([r1], [np.e - 1], MARKS[lam], color="k", ms=5, zorder=5)
        ax.text(1.15 * sol.a, 3e4, _lam_tex(lam), color=SHADES[lam], fontsize=9, ha="left", va="bottom")
    ax.set(xscale="log", yscale="log", xlim=RHO_PLOT, ylim=(1e-5, 1e6),
           xlabel=r"$r/\lambda_D\ [1]$", ylabel=r"$n_e/n_0-1\ [1]$")
    ax.legend(handles=[
        Line2D([], [], color="#4292c6", lw=2.4, label=r"Boltzmann $e^{e\Phi/k_BT_e}-1$"),
        Line2D([], [], color=ORANGE, ls=(0, (4, 3)), lw=1.1, label=r"linearised $e\Phi_{DH}/k_BT_e$"),
        Line2D([], [], color="k", marker="o", ms=5, ls="", label=r"$e\Phi=k_BT_e$")],
        loc="upper right", fontsize=8.5, title=r"$q=e$: $n_0\lambda_D^3=1/(4\pi\Lambda)$", title_fontsize=8.5)
    save_all(fig, "debye_nonlinear_density")
    return sols


def save_all(fig, name):
    from si import save
    out = Path(__file__).resolve().parent / "build" / "fig"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.png", dpi=200, facecolor="white")
    save(fig, name)


def report(sols):
    for lam, sol in sols.items():
        r1 = unit_crossing(sol)
        ratio = far_field_ratio(sol, lam)
        print(f"Lambda={lam:g}: a={sol.a:.1e}  rho_1={r1:.3e}  phi/phi_DH at rho=1,2,3: "
              + ", ".join(f"{x:.5f}" for x in ratio)
              + f"  cutoff a/2 changes phi(2) by {cutoff_sensitivity(lam):+.1e}"
              + f"  electrons inside rho_1 (q=e): {electrons_inside(sol, lam, r1):.1e}")


if __name__ == "__main__":
    report(plot())
