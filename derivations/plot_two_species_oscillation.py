#!/usr/bin/env python3
"""Electrons and ions oscillating together: omega_p^2 = omega_pe^2 + omega_pi^2.

Model: cold, collisionless, one-dimensional, periodic box of length
lambda = 2 pi/k.  Electrons (charge -e, mass m_e) and singly charged ions
(+e, m_i) of equal density n_0, each represented by N particles; charge
deposited on M grid cells with linear weighting, Gauss's law solved by FFT
with zero mean field, field interpolated back with the same weights
(1D electrostatic particle-in-cell), leapfrog.  Normalized: k = 1,
omega_pe = 1, so omega_pi^2 = m_e/m_i.

Start: both species at their uniform positions, velocities
v_e = v_0 sin(kx), v_i = -(m_e/m_i) v_0 sin(kx) (no net momentum).  Linear
cold theory: the electron and ion displacements oscillate in antiphase,
xi_i = -(m_e/m_i) xi_e, at omega_p = (omega_pe^2 + omega_pi^2)^(1/2).  The
frequency is measured from the zero crossings of the electron velocity mode
sum_j v_j sin(k x_j(0)) over four periods.

The amplitude is small, k v_0/omega_pe = 0.005: at larger amplitude the ion
density perturbation makes the local frequency vary in space and the mode
phase-mixes (its zero crossings drift apart within a few periods at
k v_0/omega_pe = 0.05 and m_i = m_e), a nonlinear effect absent for immobile ions.

Writes build/fig/two_species_oscillation.{svg,pdf}.
"""
from __future__ import annotations

import numpy as np

BOX = 2 * np.pi            # k lambda [1]
PARTICLES = 4096           # per species
CELLS = 256
KV = 0.005                 # k v_0/omega_pe [1]
STEPS = 200                # leapfrog steps per period 2 pi/omega_p
RATIOS = (1, 2, 4, 10, 30, 100, 1836)   # m_i/m_e [1]
TRACE_RATIO = 4


def field(x, charge, cells=CELLS):
    """e E/(m_e omega_pe^2) k at the particles from linear-weighted charge."""
    h = BOX / cells
    g = x / h
    j = np.floor(g).astype(int)
    f = g - j
    j %= cells
    rho = (np.bincount(j, charge * (1 - f), cells) + np.bincount((j + 1) % cells, charge * f, cells)) / h
    k = 2 * np.pi * np.fft.rfftfreq(cells, h)
    rho_k = np.fft.rfft(rho)
    e_k = np.zeros_like(rho_k)
    e_k[1:] = rho_k[1:] / (1j * k[1:])
    e = np.fft.irfft(e_k, cells)
    return e[j] * (1 - f) + e[(j + 1) % cells] * f


def run(ratio, n=PARTICLES, kv=KV, periods=4.0, steps=STEPS):
    """Returns t, electron and ion displacement modes, electron velocity mode."""
    mu = 1.0 / ratio
    start = (np.arange(n) + 0.5) * BOX / n
    x = np.concatenate([start, start])
    charge = np.concatenate([-np.ones(n), np.ones(n)]) * BOX / n
    qm = np.concatenate([-np.ones(n), mu * np.ones(n)])
    v = np.concatenate([kv * np.sin(start), -mu * kv * np.sin(start)])
    dt = 2 * np.pi / np.sqrt(1 + mu) / steps
    shape = np.sin(start) * 2 / n
    a = qm * field(x, charge)
    t, xi_e, xi_i, v_e = [0.0], [0.0], [0.0], [kv]
    for i in range(int(round(periods * steps))):
        v += 0.5 * dt * a
        x = np.mod(x + dt * v, BOX)
        a = qm * field(x, charge)
        v += 0.5 * dt * a
        disp = np.mod(x - np.concatenate([start, start]) + BOX / 2, BOX) - BOX / 2
        t.append((i + 1) * dt)
        xi_e.append(disp[:n] @ shape)
        xi_i.append(disp[n:] @ shape)
        v_e.append(v[:n] @ shape)
    return np.array(t), np.array(xi_e), np.array(xi_i), np.array(v_e)


def measured_frequency(t, mode):
    s = np.sign(mode)
    idx = np.nonzero(s[:-1] * s[1:] < 0)[0]
    zeros = t[idx] - mode[idx] * (t[idx + 1] - t[idx]) / (mode[idx + 1] - mode[idx])
    return np.pi / np.mean(np.diff(zeros))


def theory(ratio):
    return np.sqrt(1 + 1 / np.asarray(ratio, float))


def plot():
    import matplotlib.pyplot as plt
    from si import BLUE, figure, save, slide_width

    fig, ax = figure(slide_width(10), 2.5)
    fig.clear()
    trace, freq = fig.subplots(1, 2, width_ratios=(1.35, 1))
    for a in (trace, freq):
        a.spines[["top", "right"]].set_visible(False)

    t, xi_e, xi_i, _ = run(TRACE_RATIO, periods=2.0)
    trace.plot(t, xi_e / KV, color=BLUE, lw=1.8)
    trace.plot(t, xi_i / KV, color="#B55000", lw=1.8, ls=(0, (4, 2)))
    trace.axhline(0, color="#999999", lw=0.6, zorder=0)
    trace.text(t[len(t) // 8], xi_e.max() / KV * 1.04, "electrons", color=BLUE, fontsize=9, va="bottom")
    trace.text(t[len(t) * 3 // 8], xi_i.max() / KV * 1.25, "ions", color="#B55000", fontsize=9, va="bottom")
    trace.set(xlabel=r"$\omega_{pe}t\ [1]$", ylabel=r"$\omega_{pe}\xi_\alpha/v_0\ [1]$",
              xlim=(0, t[-1]), ylim=(-1.05, 1.15))
    trace.set_title(rf"$m_i/m_e={TRACE_RATIO}$", fontsize=10, loc="left")

    ratios = np.geomspace(1, 3000, 200)
    freq.plot(ratios, theory(ratios), color="#B55000", ls=(0, (4, 3)), lw=1.3)
    measured = [measured_frequency(*run(r)[::3]) for r in RATIOS]
    freq.plot(RATIOS, measured, "o", color=BLUE, ms=4.5)
    freq.text(60, 1.3, r"$\sqrt{1+m_e/m_i}$", color="#B55000", fontsize=9, ha="center")
    freq.text(150, 1.05, "measured", color=BLUE, fontsize=9, ha="center")
    freq.set(xscale="log", xlabel=r"$m_i/m_e\ [1]$", ylabel=r"$\omega/\omega_{pe}\ [1]$",
             ylim=(0.98, 1.45), xlim=(0.7, 4000))
    freq.set_xticks([1, 10, 100, 1000])
    freq.xaxis.set_minor_locator(plt.NullLocator())
    save(fig, "two_species_oscillation")
    return dict(zip(RATIOS, measured))


if __name__ == "__main__":
    for ratio, omega in plot().items():
        print(f"m_i/m_e={ratio:5d}: omega/omega_pe = {omega:.6f}, theory {theory(ratio):.6f}, "
              f"rel. dev. {omega / theory(ratio) - 1:+.1e}")
