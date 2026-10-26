#!/usr/bin/env python3
"""Loss cone of a magnetic mirror in velocity space.

Model: mirror field on the axis B(z)/B_0 = 1 + (R_m - 1)(z/L)^2 with the
mirror ratio R_m = B_max/B_0 = 4, the throat at z = L.  An isotropic sample:
velocity components at the midplane drawn from one Maxwellian (seeded), so
that v_par = v_z and v_perp = (v_x^2 + v_y^2)^(1/2) in units of the thermal
speed v_th [1], (v_th = (2 k_B T/m_alpha)^(1/2), each component with variance
v_th^2/2).

Trapped or lost follows from the two constants of the guiding-centre motion,
mu = m_alpha v_perp^2/(2B) and W = m_alpha v^2/2 (no electrostatic
potential): along the field line v_par^2(z) = v^2 - v_perp,0^2 B(z)/B_0.  A
particle is trapped when v_par^2 reaches zero at some |z| <= L, which is
checked on a grid of z, without using the loss-cone formula.  The lines
v_perp = |v_par| tan(alpha_c) with sin^2(alpha_c) = 1/R_m are drawn for
comparison.

Right panel: fraction lost of an isotropic distribution against R_m, from a
larger sample with the same test, against the solid angle of the two cones
1 - cos(alpha_c) = 1 - (1 - 1/R_m)^(1/2).

Writes build/fig/loss_cone.{svg,pdf}.
"""
from __future__ import annotations

import numpy as np

R_M = 4.0                                   # mirror ratio of the left panel [1]
N_SHOW = 1500                               # particles in the left panel
N_FRACTION = 200_000                        # particles per point, right panel
RATIOS = np.array([1.25, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 20.0])
Z = np.linspace(0.0, 1.0, 201)              # z/L from the midplane to the throat


def sample(n, seed):
    """(v_par, v_perp)/v_th [1] of an isotropic Maxwellian sample."""
    v = np.random.default_rng(seed).normal(scale=np.sqrt(0.5), size=(n, 3))
    return v[:, 2], np.hypot(v[:, 0], v[:, 1])


def trapped(v_par, v_perp, ratio):
    """True where v_par^2(z) = v^2 - v_perp^2 B(z)/B_0 vanishes for some z <= L."""
    b = 1.0 + (ratio - 1.0) * Z**2
    v2 = v_par**2 + v_perp**2
    v_par2 = v2[:, None] - (v_perp**2)[:, None] * b[None, :]
    return (v_par2 <= 0.0).any(axis=1)


def lost_fraction(ratio, n=N_FRACTION, seed=2):
    v_par, v_perp = sample(n, seed)
    return 1.0 - trapped(v_par, v_perp, ratio).mean()


def lost_formula(ratio):
    return 1.0 - np.sqrt(1.0 - 1.0 / ratio)


def plot():
    from si import BLUE, GRAY, ORANGE, figure, label, save, slide_width

    v_par, v_perp = sample(N_SHOW, seed=1)
    keep = trapped(v_par, v_perp, R_M)
    tan_c = np.tan(np.arcsin(np.sqrt(1.0 / R_M)))
    fractions = np.array([lost_fraction(r) for r in RATIOS])

    fig, _ = figure(slide_width(11), 2.45)
    fig.clf()
    ax, ax_f = fig.subplots(1, 2, width_ratios=[1.45, 1.0])
    ax.plot(v_par[keep], v_perp[keep], "o", color=BLUE, ms=2.0, mew=0, alpha=0.75)
    ax.plot(v_par[~keep], v_perp[~keep], "^", color=ORANGE, ms=2.8, mew=0)
    v = np.linspace(0.0, 2.6, 2)
    for sign in (-1, 1):
        ax.plot(sign * v, v * tan_c, color=GRAY, ls="--", lw=1.0)
    box = dict(boxstyle="square,pad=0.15", fc="white", ec="none", alpha=0.85)
    ax.plot([-2.45], [2.72], "o", color=BLUE, ms=4)
    label(ax, -2.3, 2.72, "trapped", BLUE, va="center")
    ax.plot([0.75], [2.72], "^", color=ORANGE, ms=4.5)
    label(ax, 0.9, 2.72, "lost", ORANGE, va="center")
    label(ax, 1.3, 1.55, r"$\sin^2\alpha_c=1/R_m$", GRAY, bbox=box)
    ax.set(xlim=(-2.6, 2.6), ylim=(0, 3.0), aspect="equal",
           xlabel=r"$v_\parallel/v_\mathrm{th}\ [1]$", ylabel=r"$v_\perp/v_\mathrm{th}\ [1]$")
    ax.set_title(rf"midplane, $R_m={R_M:g}$", fontsize=10)

    r = np.linspace(1.0, 20.0, 400)
    ax_f.plot(r, lost_formula(r), color=GRAY, ls="--")
    ax_f.plot(RATIOS, fractions, "o", color=BLUE, ms=3.5)
    label(ax_f, 5.5, 0.32, r"$1-\sqrt{1-1/R_m}$", GRAY)
    label(ax_f, 9.0, 0.12, "sample", BLUE)
    ax_f.set(xlim=(1, 20), ylim=(0, 1), xticks=[1, 5, 10, 15, 20],
             xlabel=r"$R_m\ [1]$", ylabel=r"fraction lost $[1]$")
    save(fig, "loss_cone")
    return keep, fractions


if __name__ == "__main__":
    keep, fractions = plot()
    print(f"R_m={R_M:g}: lost {1 - keep.mean():.4f} of {N_SHOW} (formula {lost_formula(R_M):.4f})")
    for ratio, f in zip(RATIOS, fractions):
        print(f"R_m={ratio:5.2f}  lost {f:.4f}  formula {lost_formula(ratio):.4f}  diff {f - lost_formula(ratio):+.4f}")
