#!/usr/bin/env python3
"""Adiabatic invariance of the magnetic moment in a ramped uniform field.

Model, normalized with q_alpha = m_alpha = 1 and the initial field B_0 = 1, so
that time is omega_c0 t [1] and lengths are rho_L0 [1] (omega_c0 = q_alpha
B_0/m_alpha, rho_L0 = v_perp/|omega_c0|):

    B(t) = B(t) e_z,  B: B_0 -> 2 B_0,
    E = -(1/2) dB/dt e_z x r          (Faraday's law, axisymmetric),
    dv/dt = E + v x B.

Two ramps with the same largest slope B_0/(2 tau):

    smooth  B/B_0 = 3/2 + tanh(t/tau)/2,
    linear  B/B_0 = 3/2 + clip(t/tau, -1, 1)/2      (kinks at t = -tau, tau).

The particle starts on the circle of radius rho_L0 centred on the axis, so the
problem is rotationally symmetric and the result does not depend on the
gyrophase. The canonical angular momentum about the axis is then exact, and a
non-adiabatic change only displaces the guiding centre off the axis, which
raises mu: mu_final/mu_initial - 1 >= 0. It falls exponentially with tau for
the smooth ramp and only algebraically for the linear one, whose two kinks
interfere.

Integrator: Boris push. Velocities live on half steps; the start is the exact
discrete circle of the scheme, and E uses the field increment over each step,
(B(t+dt) - B(t))/dt, so the induced flux is exact even across a kink. Before
and after the ramp E = 0 and the Boris rotation keeps |v| exactly, so mu needs
no averaging. An independent DOP853 integration (test_chapters.py) agrees.

Writes build/fig/mu_ramp.{svg,pdf}.
"""
from __future__ import annotations

import numpy as np

STEPS_PER_TURN = 1600              # Boris steps per initial gyroperiod [1]
TAU = np.linspace(0.25, 8.0, 63)   # ramp times omega_c0 tau [1]


def field(t, tau, smooth):
    """B/B_0 [1] at omega_c0 t [1]."""
    x = t / tau
    return 1.5 + 0.5 * (np.tanh(x) if smooth else np.clip(x, -1.0, 1.0))


def boris(taus, smooth, steps_per_turn=STEPS_PER_TURN):
    """mu_final/mu_initial - 1 [1] for every ramp time in `taus`."""
    taus = np.atleast_1d(np.asarray(taus, float))
    half = 8 * taus.max() + 40 * np.pi       # ramp plus 20 turns on each side
    dt = 2 * np.pi / steps_per_turn
    # Exact discrete circle of radius r about the axis: angle per step theta.
    theta = 2 * np.arctan(dt / 2)
    r = dt / (2 * np.sin(theta / 2))
    x = np.tile([r, 0.0], (taus.size, 1))
    v = np.tile([r * (1 - np.cos(theta)) / dt, -r * np.sin(theta) / dt], (taus.size, 1))
    mu_0 = 0.5 * np.sum(v * v, axis=1) / field(-half, taus, smooth)
    t = -half
    for _ in range(int(np.ceil(2 * half / dt))):
        b = field(t + dt / 2, taus, smooth)
        b_dot = (field(t + dt, taus, smooth) - field(t, taus, smooth)) / dt
        e = -0.5 * b_dot[:, None] * np.stack([-x[:, 1], x[:, 0]], axis=1)
        v_minus = v + 0.5 * dt * e
        h = (0.5 * dt * b)[:, None]
        v_prime = v_minus + h * np.stack([v_minus[:, 1], -v_minus[:, 0]], axis=1)
        v = v_minus + 2 * h / (1 + h * h) * np.stack([v_prime[:, 1], -v_prime[:, 0]], axis=1)
        v = v + 0.5 * dt * e
        x = x + dt * v
        t += dt
    mu_1 = 0.5 * np.sum(v * v, axis=1) / field(t, taus, smooth)
    return mu_1 / mu_0 - 1


def plot():
    from si import BLUE, ORANGE, figure, label, save, slide_width

    smooth, linear = boris(TAU, True), boris(TAU, False)
    fig, ax = figure(slide_width(8), 2.3)
    ax.semilogy(TAU, linear, color=ORANGE, ls="--", marker="o", ms=2.2)
    ax.semilogy(TAU, smooth, color=BLUE, marker="o", ms=2.2)
    label(ax, 5.3, 8e-3, "linear ramp", ORANGE)
    label(ax, 3.4, 1e-9, r"$\tanh$ ramp", BLUE)
    ax.set(xlim=(0, 8.2), ylim=(1e-12, 1), xticks=range(0, 9),
           xlabel=r"$|\omega_{c0}|\,\tau\ [1]$",
           ylabel=r"$\mu_\mathrm{final}/\mu_\mathrm{initial}-1\ [1]$")
    ax.set_yticks([10.0**k for k in range(-12, 1, 2)])
    ax.minorticks_off()
    save(fig, "mu_ramp")
    return smooth, linear


if __name__ == "__main__":
    smooth, linear = plot()
    for tau in (0.25, 1.0, 2.0, 4.0, 6.0, 8.0):
        k = int(np.argmin(abs(TAU - tau)))
        print(f"tau={TAU[k]:.3f}  smooth {smooth[k]:.3e}  linear {linear[k]:.3e}")
