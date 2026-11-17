#!/usr/bin/env python3
"""Fourier amplitudes admitted by the derivative bounds of the guiding-centre
ordering.

Model: one Fourier mode B(x) = B(k) cos(kx) of a field that obeys
|B| <= B_*, |dB/dx| <= B_*/L and |d^2B/dx^2| <= B_*/L^2 (unit constants).
The mode has |dB/dx|max = k|B(k)| and |d^2B/dx^2|max = k^2|B(k)|, so in units
of kL [1] and |B(k)|/B_* [1] the three bounds are 1, (kL)^-1 and (kL)^-2.
The admissible amplitudes lie below all three, under
min(1, (kL)^-1, (kL)^-2) = 1 for kL <= 1 and (kL)^-2 for kL > 1: the
first-derivative bound never sets the envelope.

Writes build/fig/amplitude_bounds.{svg,pdf}.
"""
from __future__ import annotations

import numpy as np

KL = np.logspace(-2, 2, 400)                # kL [1]


def bounds(kl):
    """|B(k)|/B_* [1] allowed by the amplitude, first- and second-derivative bounds."""
    return np.ones_like(kl), 1.0 / kl, 1.0 / kl**2


def envelope(kl):
    return np.minimum.reduce(bounds(kl))


def plot():
    from si import BLUE, GRAY, ORANGE, figure, label, log_ticks, save, slide_width

    amplitude, first, second = bounds(KL)
    edge = envelope(KL)
    fig, ax = figure(slide_width(8), 2.6)
    ax.fill_between(KL, 1e-4, edge, color=BLUE, alpha=0.15, lw=0)
    ax.plot(KL, amplitude, color=GRAY, ls="--", lw=1.0)
    ax.plot(KL, first, color=GRAY, ls="-.", lw=1.0)
    ax.plot(KL, second, color=GRAY, ls=":", lw=1.2)
    ax.plot(KL, edge, color=ORANGE, lw=2.0)
    label(ax, 5.0, 1.3, r"$|B(k)| \leq B_*$", GRAY)
    label(ax, 8.0, 0.15, r"$k|B(k)| \leq B_*/L$", GRAY)
    label(ax, 0.15, 80.0, r"$k^2|B(k)| \leq B_*/L^2$", GRAY)
    label(ax, 0.03, 0.02, "admissible", BLUE)
    ax.set(xscale="log", yscale="log", xlim=(1e-2, 1e2), ylim=(1e-4, 1e3),
           xlabel=r"$kL\ [1]$", ylabel=r"$|B(k)|/B_*\ [1]$")
    log_ticks(ax.xaxis, -2, 2)
    log_ticks(ax.yaxis, -4, 2, 2)
    save(fig, "amplitude_bounds")
    return edge


if __name__ == "__main__":
    edge = plot()
    for kl in (0.1, 1.0, 10.0):
        print(f"kL={kl:5.1f}  envelope {float(envelope(np.array([kl]))[0]):.4g}")
