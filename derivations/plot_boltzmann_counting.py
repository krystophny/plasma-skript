#!/usr/bin/env python3
"""Boltzmann factor from counting microstates of an Einstein-solid reservoir.

A small system, one harmonic oscillator with energy E = n eps (n = 0, 1, ...),
shares Q energy quanta eps with a reservoir of N oscillators.  The reservoir
has

    W_R(N, q) = (q + N - 1)! / (q! (N - 1)!)

microstates with q quanta, and every microstate of the whole is equally
likely, so

    P(n) = W_R(N, Q - n) / W_tot,    W_tot = (Q + N)! / (Q! N!).

At fixed quanta per reservoir oscillator Q/N = 1 the reservoir temperature
from the entropy slope, 1/(k_B T) = d ln W_R/d(q eps) = ln((Q + N)/Q)/eps,
is k_B T = eps/ln 2, and the Boltzmann distribution of the small oscillator
is P_B(n) = (1 - e^{-eps/k_B T}) e^{-n eps/k_B T} = 2^{-(n + 1)}.  The exact
counts approach it as the reservoir grows; the relative deviation at fixed n
falls as 1/N.

Writes build/fig/boltzmann_counting.{svg,pdf}.
"""
from __future__ import annotations

from math import lgamma

import numpy as np

QUANTA_PER_OSCILLATOR = 1          # Q/N [1]
RESERVOIRS = (4, 40, 400)          # N [1]
LEVELS = np.arange(0, 13)          # n = E/eps [1]


def log_states(oscillators, quanta):
    """ln W_R: ways to put `quanta` into `oscillators` oscillators."""
    return lgamma(quanta + oscillators) - lgamma(quanta + 1) - lgamma(oscillators)


def probability(n, oscillators, quanta_per=QUANTA_PER_OSCILLATOR):
    """Exact P(n) for the small oscillator, from the state count."""
    total = quanta_per * oscillators
    log_total = lgamma(total + oscillators + 1) - lgamma(total + 1) - lgamma(oscillators + 1)
    return np.array([np.exp(log_states(oscillators, total - k) - log_total) if k <= total else 0.0
                     for k in np.atleast_1d(n)])


def temperature(quanta_per=QUANTA_PER_OSCILLATOR):
    """k_B T/eps of the large reservoir at Q/N = quanta_per."""
    return 1 / np.log(1 + 1 / quanta_per)


def boltzmann(n, quanta_per=QUANTA_PER_OSCILLATOR):
    beta = 1 / temperature(quanta_per)
    return (1 - np.exp(-beta)) * np.exp(-beta * np.asarray(n, float))


def plot():
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from si import figure, save, slide_width

    fig, ax = figure(slide_width(10), 2.6)
    fig.clear()
    ax, conv = fig.subplots(1, 2, width_ratios=(1.45, 1))
    for a in (ax, conv):
        a.spines[["top", "right"]].set_visible(False)
    n_line = np.linspace(0, LEVELS[-1], 200)
    ax.plot(n_line, boltzmann(n_line), color="#B55000", ls=(0, (4, 3)), lw=1.3, zorder=1)
    styles = {4: ("#9ecae1", "o"), 40: ("#4292c6", "s"), 400: ("#08306b", "^")}
    for oscillators in RESERVOIRS:
        color, marker = styles[oscillators]
        p = probability(LEVELS, oscillators)
        keep = p > 0
        ax.plot(LEVELS[keep], p[keep], marker, color=color, ms=4.5, ls="-", lw=0.8, zorder=2)
    ax.set(yscale="log", xlim=(-0.4, LEVELS[-1] + 0.4), ylim=(1e-5, 1),
           xlabel=r"$E/\varepsilon\ [1]$", ylabel=r"$P(E)\ [1]$")
    ax.set_xticks(range(0, LEVELS[-1] + 1, 2))
    ax.legend(handles=[
        Line2D([], [], color=styles[n][0], marker=styles[n][1], ms=4.5, lw=0.8, label=rf"$N={n}$")
        for n in RESERVOIRS] + [
        Line2D([], [], color="#B55000", ls=(0, (4, 3)), lw=1.3, label=r"$e^{-E/k_BT}$")],
        loc="upper right", fontsize=9)

    sizes = np.geomspace(4, 4000, 13).round().astype(int)
    for level, marker, color, name, shift in ((1, "o", "#2171b5", r"$E=\varepsilon$", 0.45),
                                              (4, "s", "#08306b", r"$E=4\varepsilon$", 2.2)):
        dev = [abs(probability(level, n)[0] / boltzmann(level) - 1) for n in sizes]
        conv.plot(sizes, dev, marker, color=color, ms=4, ls="-", lw=0.8)
        conv.text(sizes[-1] * 1.4, dev[-1] * shift, name, color=color, fontsize=9, va="center", ha="left")
    conv.plot(sizes, 0.05 / sizes, color="#555555", ls=":", lw=1.0)
    conv.text(sizes[4], 0.05 / sizes[4] * 0.3, r"$\propto 1/N$", color="#555555", fontsize=9, ha="right", va="top")
    conv.set(xscale="log", yscale="log", xlim=(3, 4000 * 6), ylim=(1e-5, 1),
             xlabel=r"$N\ [1]$", ylabel=r"$|P/P_B-1|\ [1]$")
    conv.set_xticks([1e1, 1e2, 1e3, 1e4])
    conv.xaxis.set_minor_locator(plt.NullLocator())
    fig.get_layout_engine().set(wspace=0.08)
    save(fig, "boltzmann_counting")


def report():
    for oscillators in RESERVOIRS + (4000,):
        n = np.arange(0, 5)
        dev = probability(n, oscillators) / boltzmann(n) - 1
        print(f"N={oscillators:5d}: P(n)/P_B(n) - 1 for n=0..4: " + ", ".join(f"{d:+.2e}" for d in dev))


if __name__ == "__main__":
    plot()
    report()
