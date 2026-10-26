#!/usr/bin/env python3
"""Spitzer resistivity against electron temperature, with copper for scale.

Formula (NRL Plasma Formulary, 2019 edition, "Fundamental plasma parameters"
and "Transport coefficients"): transverse Spitzer resistivity

    eta_perp = 1.03e-2 Z ln Lambda T_e^(-3/2) Ohm cm = 1.03e-4 Z ln Lambda T_e^(-3/2) Ohm m,

T_e in eV, and for Z = 1 the parallel resistivity eta_par = 0.51 eta_perp
(friction force R_u = (n e/sigma_0)(0.51 j_par + j_perp), Braginskii).  The
Coulomb logarithm is the formulary's electron-ion lambda_ei with n_e in cm^-3:

    ln Lambda = 23 - ln(n_e^(1/2) Z T_e^(-3/2))   for T_e < 10 Z^2 eV,
              = 24 - ln(n_e^(1/2) T_e^(-1))         above.

The coefficient 1.03e-4 is checked against m_e/(n e^2 tau_e) with the
formulary's electron collision time tau_e = 6 sqrt(2) pi^(3/2) eps_0^2
m_e^(1/2) (k_B T_e)^(3/2)/(ln Lambda e^4 n) in SI form (`coefficient`).

Copper: 1.68e-8 Ohm m at 293 K, interpolated in Matula, J. Phys. Chem. Ref.
Data 8, 1147 (1979), doi:10.1063/1.555614 (1.543e-8 at 273 K, 1.725e-8 at
300 K).  The example plasmas are the shared (n_e, k_B T_e) points of
si.EXAMPLE_PLASMAS, each with its own ln Lambda; Z = 1 throughout.

Writes build/fig/spitzer-resistivity.{svg,pdf}.
"""
from __future__ import annotations

import math

import numpy as np

NRL_PERP = 1.03e-4          # Ohm m eV^(3/2), NRL transverse coefficient
PARALLEL = 0.51             # eta_par/eta_perp for Z = 1 (NRL, Braginskii)
COPPER = 1.68e-8            # Ohm m at 293 K (Matula 1979)
CURVE_DENSITY = 1e20        # n_e [m^-3] of the drawn curves
SHOWN = ("H II region", "Hall thruster", "solar corona", "tokamak core")


def coulomb_log(n_e, t_e, z=1.0):
    """NRL electron-ion ln Lambda; n_e in m^-3, k_B T_e in eV."""
    n_cgs = np.asarray(n_e) * 1e-6
    t_e = np.asarray(t_e, dtype=float)
    low = 23.0 - np.log(np.sqrt(n_cgs) * z * t_e**-1.5)
    high = 24.0 - np.log(np.sqrt(n_cgs) / t_e)
    return np.where(t_e < 10.0 * z * z, low, high)


def eta_perp(n_e, t_e, z=1.0):
    """Transverse Spitzer resistivity [Ohm m]."""
    return NRL_PERP * z * coulomb_log(n_e, t_e, z) * np.asarray(t_e, dtype=float)**-1.5


def eta_par(n_e, t_e):
    return PARALLEL * eta_perp(n_e, t_e)


def coefficient():
    """eta_perp T_e^(3/2)/(Z ln Lambda) [Ohm m eV^(3/2)] from m_e/(n e^2 tau_e)."""
    e, m_e, eps0 = 1.602176634e-19, 9.1093837015e-31, 8.8541878128e-12
    t_joule = e                                        # k_B T_e = 1 eV
    # n tau_e ln Lambda, so that n and ln Lambda cancel in m_e/(n e^2 tau_e)
    n_tau_lnl = 6 * math.sqrt(2) * math.pi**1.5 * eps0**2 * math.sqrt(m_e) \
        * t_joule**1.5 / e**4
    return m_e / (e**2 * n_tau_lnl)


def plot():
    from si import BLUE, EXAMPLE_PLASMAS, GRAY, ORANGE, figure, label, log_ticks, save

    t = np.geomspace(0.5, 3e4, 300)
    fig, ax = figure(4.6, 3.1)
    ax.plot(t, eta_par(CURVE_DENSITY, t), color=BLUE)
    ax.plot(t, eta_perp(CURVE_DENSITY, t), color=BLUE, ls="--", lw=1.2)
    ax.axhline(COPPER, color=ORANGE, ls=":", lw=1.4)
    label(ax, 0.6, COPPER * 1.4, "copper, 293 K", ORANGE)
    label(ax, 1.3, eta_perp(CURVE_DENSITY, 1.3) * 1.15, r"$\eta_\perp$", BLUE)
    label(ax, 0.9, eta_par(CURVE_DENSITY, 0.9) * 0.35, r"$\eta_\parallel$", BLUE, va="top")
    offsets = {"H II region": (1.3, 1.6), "Hall thruster": (1.3, 1.6),
               "solar corona": (1.3, 1.6), "tokamak core": (0.12, 0.25)}
    for name in SHOWN:
        n_e, t_e = EXAMPLE_PLASMAS[name]
        value = eta_par(n_e, t_e)
        ax.plot([t_e], [value], "o", color="#1c1f23", ms=4)
        dx, dy = offsets[name]
        label(ax, t_e * dx, value * dy,
              f"{name}\n" + rf"$\ln\Lambda={float(coulomb_log(n_e, t_e)):.0f}$",
              "#1c1f23", fontsize=8, linespacing=1.0)
    label(ax, 0.6, 2e-10, "lines: " + r"$n_e=10^{20}\,$m$^{-3}$, $Z=1$" + "\ndots: " + r"$\eta_\parallel$"
          + r" at their own $n_e$", GRAY, fontsize=8, linespacing=1.1)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.5, 3e4)
    ax.set_ylim(1e-10, 1e-2)
    log_ticks(ax.xaxis, 0, 4)
    log_ticks(ax.yaxis, -10, -2, 2)
    ax.set_xlabel(r"$k_B T_e$ [eV]")
    ax.set_ylabel(r"$\eta$ [$\Omega\,$m]")
    save(fig, "spitzer-resistivity")


if __name__ == "__main__":
    plot()
    print(f"eta_perp coefficient: NRL {NRL_PERP:.3e}, m_e/(n e^2 tau_e) {coefficient():.4e} "
          f"Ohm m eV^1.5 ({NRL_PERP / coefficient() - 1:+.2%})")
    from si import EXAMPLE_PLASMAS
    for name in SHOWN:
        n_e, t_e = EXAMPLE_PLASMAS[name]
        print(f"{name:14s} n_e={n_e:.0e} T_e={t_e:g} eV  lnL={float(coulomb_log(n_e, t_e)):.1f}"
              f"  eta_par={float(eta_par(n_e, t_e)):.2e} Ohm m  /copper={float(eta_par(n_e, t_e)) / COPPER:.2g}")
