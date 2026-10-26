#!/usr/bin/env python3
"""Velocity moments as weighted areas of one distribution function.

Model: a one-dimensional velocity distribution of species alpha, a core
Maxwellian plus a warm beam,

    f(v) = sum_j n_j (2 pi)^(-1/2) / v_j * exp(-(v - u_j)^2 / (2 v_j^2)),

core (n_j, u_j, v_j) = (0.8, 0, 1) and beam (0.2, 2.5, 0.6), so the sum is
shifted (net flow), heated (wider than the core) and skewed (a beam on one
side).  Normalization: velocities in v_t = (k_B T_c / m_alpha)^(1/2) of the
core, densities in n_0 = the total density, f in n_0 / v_t [1].

The four panels show the integrands of the moments that define the fluid
variables, w = v - u being the random velocity relative to the flow u:

    integral f dv            = n
    integral v f dv          = n u
    integral w^2 f dv        = n k_B T / m_alpha      (1D temperature)
    integral w^3 f dv        = 2 q / m_alpha          (1D heat flux)

Each area is computed by quadrature on a grid and compared with the closed
form for a sum of Maxwellians (`analytic_moments`), the check printed below
and repeated in test_chapters.py.

Writes build/fig/moment-weights.{svg,pdf}.
"""
from __future__ import annotations

import numpy as np

COMPONENTS = [(0.8, 0.0, 1.0), (0.2, 2.5, 0.6)]   # (n_j/n_0, u_j/v_t, v_j/v_t) [1]
V = np.linspace(-7.0, 9.0, 4001)                     # v/v_t [1]


def distribution(v):
    """f v_t / n_0 [1]."""
    v = np.asarray(v, dtype=float)
    return sum(n / (np.sqrt(2 * np.pi) * s) * np.exp(-(v - u)**2 / (2 * s * s))
               for n, u, s in COMPONENTS)


def numerical_moments(v=V):
    """(n, u, k_B T/m, q/m) from trapezoidal quadrature of the integrands."""
    f = distribution(v)
    n = np.trapezoid(f, v)
    u = np.trapezoid(v * f, v) / n
    w = v - u
    temperature = np.trapezoid(w**2 * f, v) / n
    heat = 0.5 * np.trapezoid(w**3 * f, v)
    return n, u, temperature, heat


def analytic_moments():
    """Closed form for a sum of drifting Maxwellians: central moments of each
    component about the common flow u, <(v-u)^2> = s^2 + d^2 and
    <(v-u)^3> = d^3 + 3 s^2 d with d = u_j - u."""
    n = sum(c[0] for c in COMPONENTS)
    u = sum(c[0] * c[1] for c in COMPONENTS) / n
    second = sum(nj * (s * s + (uj - u)**2) for nj, uj, s in COMPONENTS)
    third = sum(nj * ((uj - u)**3 + 3 * s * s * (uj - u)) for nj, uj, s in COMPONENTS)
    return n, u, second / n, 0.5 * third


def plot():
    from si import BLUE, GRAY, ORANGE, figure, label, save

    n, u, temperature, heat = numerical_moments()
    f = distribution(V)
    w = V - u
    panels = [
        (f, r"$f\,v_t/n_0\ [1]$", rf"$\int f\,dv = n = {n:.3f}\,n_0$"),
        (V * f, r"$v f/n_0\ [1]$", rf"$\int v f\,dv = nu = {n * u:.3f}\,n_0 v_t$"),
        (w**2 * f, r"$w^2 f/(n_0 v_t)\ [1]$",
         rf"$\int w^2 f\,dv = n k_B T/m_\alpha = {n * temperature:.3f}\,n_0 v_t^2$"),
        (w**3 * f, r"$w^3 f/(n_0 v_t^2)\ [1]$",
         rf"$\int w^3 f\,dv = 2q/m_\alpha = {2 * heat:.3f}\,n_0 v_t^3$"),
    ]
    fig, _ = figure(6.4, 4.2)
    fig.clf()
    axes = fig.subplots(2, 2, sharex=True).ravel()
    box = dict(boxstyle="square,pad=0.15", fc="white", ec="none", alpha=0.85)
    for k, (ax, (y, ylabel, area)) in enumerate(zip(axes, panels)):
        ax.fill_between(V, 0, y, where=y >= 0, color=BLUE, alpha=0.35, lw=0)
        ax.fill_between(V, 0, y, where=y < 0, facecolor="none", edgecolor=ORANGE,
                        hatch="////", lw=0)
        ax.plot(V, y, color="#1c1f23", lw=1.1)
        if k > 0:
            ax.plot(V, f, color=GRAY, lw=0.9, ls=":")
        ax.axhline(0, color="#333333", lw=0.6)
        ax.axvline(u, color=GRAY, lw=0.9, ls="--")
        top = max(y.max(), f.max())
        bottom = min(y.min(), 0.0)
        pad = 0.12 * (top - bottom)
        ax.set_ylim(bottom - pad, top + 2.4 * pad)
        ax.set_xlim(-4.5, 5.0)
        ax.set_ylabel(ylabel)
        label(ax, -4.3, top + 1.15 * pad, area, "#1c1f23", fontsize=9, bbox=box)
    label(axes[0], u + 0.15, 0.02, r"$u$", GRAY)
    label(axes[3], -4.3, 0.55 * axes[3].get_ylim()[0], "negative", ORANGE, fontsize=9)
    label(axes[1], 1.6, -0.15, r"$f$ (dotted)", GRAY, fontsize=9)
    for ax in axes[2:]:
        ax.set_xlabel(r"$v/v_t\ [1]$")
    save(fig, "moment-weights")
    return n, u, temperature, heat


if __name__ == "__main__":
    got = plot()
    ref = analytic_moments()
    for name, a, b in zip(("n/n_0", "u/v_t", "k_B T/(m v_t^2)", "q/(m n_0 v_t^3)"), got, ref):
        print(f"{name:18s} quadrature {a:.6f}  analytic {b:.6f}  rel. diff {a / b - 1:+.1e}")
