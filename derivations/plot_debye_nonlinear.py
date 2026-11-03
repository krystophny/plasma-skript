#!/usr/bin/env python3
"""Nonlinear Poisson-Boltzmann screening of a negative charge vs Debye-Hueckel.

Model (electrons Boltzmann, ions a fixed uniform background, mean field):

    phi = e Phi/(k_B T_e),  rho = r/lambda_D,  n_e/n_0 = exp(phi),
    (1/rho^2) d/drho (rho^2 dphi/drho) = exp(phi) - 1,

lambda_D^2 = eps_0 k_B T_e/(n_0 e^2).  Near a point charge q the potential is
Coulomb, phi = -Lambda/rho for q < 0, with

    Lambda = |q| e/(4 pi eps_0 lambda_D k_B T_e) = (|q|/e)/(4 pi n_0 lambda_D^3),

so e Phi = -k_B T_e at rho_1 ~ Lambda.  The test charge is negative: electrons
are expelled and n_e = n_0 exp(phi) stays between 0 and n_0, while the
linearised density n_0 (1 + phi) turns negative for phi < -1.  (For q > 0 a
point charge has no Boltzmann solution: n_0 exp(Lambda/rho) is not integrable
at rho -> 0, and the result depends on the charge radius.)  The charge is a
sphere of radius a = CUTOFF Lambda; the boundary condition there is the
enclosed charge,

    rho^2 dphi/drho |_{rho=a} = +Lambda,     phi -> 0 far away,

and the result does not depend on a (cutoff_sensitivity).  Linear
(Debye-Hueckel) point-charge solution: phi_DH = -Lambda exp(-rho)/rho.
For q = -e the strengths below correspond to n_0 lambda_D^3 = 0.1, 1, 10.

Writes build/fig/debye_nonlinear_{potential,density}.{svg,pdf,png}.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp, quad
from scipy.optimize import brentq

CUTOFF = 0.1                       # charge radius a/(Lambda lambda_D) [1]
RHO_MAX = 14.0                     # outer boundary r/lambda_D [1]
DEBYE_NUMBERS = (10.0, 1.0, 0.1)   # n_0 lambda_D^3 [1] for q = -e
STRENGTHS = tuple(1 / (4 * np.pi * nd) for nd in DEBYE_NUMBERS)   # Lambda [1]
RHO_PLOT = (1e-3, 6.0)             # plotted r/lambda_D range [1]


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
        return np.array([ya[1] - strength, yb[1] + (rho_max + 1) * yb[0]])

    rho = np.geomspace(a, rho_max, 800)
    phi0 = debye_hueckel(rho, strength, a)
    guess = np.vstack([phi0, -rho**2 * phi0 * (1 + 1 / rho)])
    sol = solve_bvp(rhs, bc, rho, guess, tol=1e-8, max_nodes=200000)
    if not sol.success:
        raise RuntimeError(f"Poisson-Boltzmann BVP failed for Lambda={strength}: {sol.message}")
    sol.a = a
    return sol


def debye_hueckel(rho, strength, a=0.0):
    return -strength * np.exp(-(rho - a)) / (rho * (1 + a))


def coulomb(rho, strength):
    return -strength / rho


def unit_crossing(sol):
    """rho_1 where the exact potential equals -k_B T_e/e (phi = -1)."""
    return brentq(lambda r: sol.sol(r)[0] + 1.0, sol.a, RHO_MAX)


def far_field_ratio(sol, strength, rho=(1.0, 2.0, 3.0)):
    """phi/phi_DH at a few Debye lengths (point-charge Debye-Hueckel)."""
    rho = np.asarray(rho)
    return sol.sol(rho)[0] / debye_hueckel(rho, strength)


def cutoff_sensitivity(strength, factor=2.0, rho=2.0):
    """Relative change of phi(rho) when the charge radius a shrinks by `factor`."""
    base = solve(strength)
    small = solve(strength, a=radius(strength) / factor)
    return small.sol(rho)[0] / base.sol(rho)[0] - 1


def solutions(strengths=STRENGTHS):
    return {lam: solve(lam) for lam in strengths}


SHADES = dict(zip(STRENGTHS, ("#6baed6", "#2171b5", "#08306b")))
MARKS = dict(zip(STRENGTHS, ("o", "s", "^")))


def _nd_tex(lam):
    return rf"$n_0\lambda_D^3={1 / (4 * np.pi * lam):.2g}$"


def plot():
    from matplotlib.lines import Line2D
    from si import figure, slide_width, ORANGE, GRAY

    sols = solutions()
    width, height = slide_width(10), 2.8

    # --- potential relative to the bare Coulomb potential ---
    fig, ax = figure(width, height)
    for lam, sol in sols.items():
        rho = np.geomspace(max(sol.a, RHO_PLOT[0]), RHO_PLOT[1], 600)
        ax.plot(rho, sol.sol(rho)[0] / coulomb(rho, lam), color=SHADES[lam], lw=2.4,
                solid_capstyle="butt", label=_nd_tex(lam))
        r1 = unit_crossing(sol)
        ax.plot([r1], [sol.sol(r1)[0] / coulomb(r1, lam)], MARKS[lam], color="k", ms=5, zorder=5)
    rho = np.geomspace(*RHO_PLOT, 600)
    ax.plot(rho, debye_hueckel(rho, 1.0) / coulomb(rho, 1.0), color=ORANGE, ls=(0, (4, 3)), lw=1.4,
            label="Debye–Hückel (linear)")
    ax.axhline(1.0, color=GRAY, ls=":", lw=1.2, label="bare Coulomb")
    ax.plot([], [], "o", color="k", ms=5, ls="", label=r"$e\Phi=-k_BT_e$")
    ax.set(xscale="log", xlim=RHO_PLOT, ylim=(0, 1.08),
           xlabel=r"$r/\lambda_D\ [1]$", ylabel=r"$\Phi/\Phi_{\mathrm{Coulomb}}\ [1]$")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8.5, title=r"exact, $q=-e$", title_fontsize=8.5)
    save_all(fig, "debye_nonlinear_potential")

    # --- electron density ---
    fig, ax = figure(width, height)
    for lam, sol in sols.items():
        rho = np.geomspace(max(sol.a, RHO_PLOT[0]), RHO_PLOT[1], 600)
        ax.plot(rho, np.exp(sol.sol(rho)[0]), color=SHADES[lam], lw=2.4, solid_capstyle="butt",
                label=_nd_tex(lam))
        ax.plot(rho, 1 + debye_hueckel(rho, lam), color=ORANGE, ls=(0, (4, 3)), lw=1.1)
        r1 = unit_crossing(sol)
        ax.plot([r1], [np.exp(-1)], MARKS[lam], color="k", ms=5, zorder=5)
    ax.axhline(0.0, color="0.6", lw=0.7, zorder=0)
    ax.plot([], [], color=ORANGE, ls=(0, (4, 3)), lw=1.1, label=r"linearised $1+e\Phi_{DH}/k_BT_e$")
    ax.plot([], [], "o", color="k", ms=5, ls="", label=r"$e\Phi=-k_BT_e$")
    ax.set(xscale="log", xlim=RHO_PLOT, ylim=(-1.5, 1.15),
           xlabel=r"$r/\lambda_D\ [1]$", ylabel=r"$n_e/n_0\ [1]$")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8.5, title=r"Boltzmann $e^{e\Phi/k_BT_e}$, $q=-e$",
              title_fontsize=8.5)
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
        print(f"n0 lD^3={1 / (4 * np.pi * lam):.2g} Lambda={lam:.3g}: rho_1={unit_crossing(sol):.3e}  "
              "phi/phi_DH at rho=1,2,3: " + ", ".join(f"{x:.4f}" for x in far_field_ratio(sol, lam))
              + f"  cutoff a/2 changes phi(2) by {cutoff_sensitivity(lam):+.1e}")


if __name__ == "__main__":
    report(plot())
