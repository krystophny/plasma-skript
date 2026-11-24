#!/usr/bin/env python3
"""Deck figures for chapter 6: flows, volume, phase space and distribution functions.

All quantities are dimensionless (lengths, velocities and times in the units
named on each axis). Every trajectory is integrated with fourth-order
Runge-Kutta; the printed areas and the smoothed densities are computed from
those trajectories, not assumed.

flow_lagrange_euler   steady cellular flow u = (sin pi x cos pi y, -cos pi x sin pi y):
                      parcel paths x(t; x0) (left) and the field u(x) on a grid (right).
advection_probe       bump g(x, t) = g0(x - u t), u = 1: profiles at t = 0, 1 with a probe
                      at x_p (left); g at the probe and along one parcel against t (right).
volume_flow           a square patch carried by the incompressible cellular flow (left) and
                      by the compressible flow u = (0.6 sin pi x, 0) (right), area A(t)/A(0).
phase_space_flow      free streaming dx/dt = v, dv/dt = 0 in (x, v) (left); Lorentz force
                      with E = E y, B = B z in (v_x, v_y), rotation about v_E = E/B (right).
distribution_cells    3000 sampled particles in (x, v), one counting cell, and the marginals
                      n(x) = int f dv and int f dx against their exact curves.
vlasov_well           f(z, t) = f0(z0(z, t)) in the pendulum well dv/dt = -sin x, by backward
                      characteristics, at omega0 t = 0, 8, 40; density n(x, t) below.
smoothing_advection   600 particles drawn from f0 and advected to omega0 t = 8 (left), their
                      Gaussian kernel estimate f_h (middle), the exact f (right).
pair_marginal         two particles on a periodic line: F2 = 1 (uncorrelated) and
                      F2 = 1 + c(x1 - x2) with a correlation hole; both marginals f1 = 1.
free_paths            2D rays among random disks (radius a): one path with its collisions, and the
                      free-path histogram against exp(-l/lambda), lambda = 1/(n sigma), sigma = 2a.
coulomb_orbits        repulsive Coulomb orbits off a fixed charge for b = 0.25 .. 4 b_90, and the
                      measured deflection chi(b) against 2 arctan(b_90/b) and its tail 2 b_90/b.
collisionality        electron mean free path v_th/nu_ei over (n_e, T_e), NRL formulary nu_ei and
                      ln Lambda, with the example plasmas of si.py.

Writes build/fig/<name>.{svg,pdf}.
"""
from __future__ import annotations

import numpy as np

from si import BLUE, GRAY, ORANGE, figure, save, slide_width

CMAP = "Blues"
RNG = np.random.default_rng(20261124)


def panels(columns, height, ncols, **kw):
    """Figure spanning `columns` slide columns with `ncols` axes and the course style."""
    import matplotlib.pyplot as plt
    fig, _ = figure(slide_width(columns), height)
    plt.close(fig)
    return plt.subplots(1, ncols, figsize=(slide_width(columns), height), layout="constrained", **kw)


def rk4(rhs, z, t, n):
    """Integrate dz/dt = rhs(z) over time t in n steps; z has shape (2, ...). Returns the path."""
    dt = t / n
    path = [z]
    for _ in range(n):
        k1 = rhs(z)
        k2 = rhs(z + 0.5 * dt * k1)
        k3 = rhs(z + 0.5 * dt * k2)
        k4 = rhs(z + dt * k3)
        z = z + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        path.append(z)
    return np.array(path)


def cellular(z):
    x, y = z
    return np.array([np.sin(np.pi * x) * np.cos(np.pi * y), -np.cos(np.pi * x) * np.sin(np.pi * y)])


def compressible(z):
    x, y = z
    return np.array([0.6 * np.sin(np.pi * x), 0.0 * y])


def pendulum(z):
    x, v = z
    return np.array([v, -np.sin(x)])


def area(poly):
    """Shoelace area of a closed polygon given as (2, n)."""
    x, y = poly
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def square_boundary(x0, y0, side, n=400):
    s = np.linspace(0, 4, n, endpoint=False)
    x = np.where(s < 1, s, np.where(s < 2, 1, np.where(s < 3, 3 - s, 0)))
    y = np.where(s < 1, 0, np.where(s < 2, s - 1, np.where(s < 3, 1, 4 - s)))
    return np.array([x0 + side * x, y0 + side * y])


def mesh_lines(x0, y0, side, k=6, n=120):
    t = np.linspace(0, 1, n)
    lines = []
    for a in np.linspace(0, 1, k):
        lines.append(np.array([x0 + side * t, y0 + side * a + 0 * t]))
        lines.append(np.array([x0 + side * a + 0 * t, y0 + side * t]))
    return lines


def flow_lagrange_euler():
    fig, (a, b) = panels(12, 2.75, 2, sharey=True)
    xs, ys = np.meshgrid(np.linspace(0, 1, 150), np.linspace(0, 1, 150))
    psi = np.sin(np.pi * xs) * np.sin(np.pi * ys) / np.pi
    for ax in (a, b):
        ax.contour(xs, ys, psi, levels=np.linspace(0.03, 0.3, 6), colors="#cccccc", linewidths=0.6)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.set_xlabel("$x$ [1]")
    a.set_ylabel("$y$ [1]")
    for (x0, y0), col in zip([(0.5, 0.08), (0.5, 0.22), (0.5, 0.36)], [BLUE, ORANGE, GRAY]):
        p = rk4(cellular, np.array([x0, y0]), 2.4, 480)
        a.plot(p[:, 0], p[:, 1], color=col, lw=1.4)
        a.plot(p[::40, 0], p[::40, 1], "o", color=col, ms=3.5)
        a.plot(*p[0], "o", color=col, ms=6, mfc="white", mew=1.4)
    gx, gy = np.meshgrid(np.linspace(0.07, 0.93, 8), np.linspace(0.07, 0.93, 8))
    u, v = cellular(np.array([gx, gy]))
    b.quiver(gx, gy, u, v, color=BLUE, scale=9, width=0.007)
    b.plot(0.8, 0.3, "s", color=ORANGE, ms=7)
    b.text(0.8, 0.24, "fixed $\\mathbf{x}$", color=ORANGE, ha="center", va="top",
           bbox=dict(fc="white", ec="none", pad=1))
    save(fig, "flow_lagrange_euler")


def advection_probe():
    fig, (a, b) = panels(12, 2.2, 2)
    g0 = lambda x: np.exp(-x ** 2 / (2 * 0.35 ** 2))  # noqa: E731
    x = np.linspace(-1.5, 3, 400)
    xp, x_parcel = 1.0, -0.4
    a.plot(x, g0(x), color=BLUE, label="$t = 0$")
    a.plot(x, g0(x - 1), color=BLUE, ls="--")
    a.text(-0.05, 1.05, "$t = 0$", color=BLUE, ha="center")
    a.text(0.95, 1.05, "$t = 1$", color=BLUE, ha="center")
    a.annotate("", (0.55, 0.55), (-0.05, 0.55), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
    a.text(0.25, 0.47, "$u$", color=GRAY, ha="center")
    a.axvline(xp, color=ORANGE, lw=1.0)
    a.text(xp + 0.06, 0.15, "probe $x_p$", color=ORANGE)
    a.plot([x_parcel, x_parcel + 1], [g0(x_parcel)] * 2, "o", color=GRAY, ms=5)
    a.annotate("", (x_parcel + 0.95, g0(x_parcel)), (x_parcel + 0.05, g0(x_parcel)),
               arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8, ls=":"))
    a.text(x_parcel - 0.1, g0(x_parcel) + 0.08, "parcel", color=GRAY, ha="center")
    a.set_xlim(-1.5, 3)
    a.set_ylim(0, 1.2)
    a.set_xlabel("$x$ [$L$]")
    a.set_ylabel("$g$ [1]")
    t = np.linspace(0, 3, 300)
    b.plot(t, g0(xp - t), color=ORANGE, label="at the probe: $g(x_p, t)$")
    b.plot(t, g0(x_parcel) + 0 * t, color=GRAY, ls="--", label="along the parcel: $g(x(t), t)$")
    b.text(1.75, 0.75, "fixed $x$: $\\partial g/\\partial t \\neq 0$", color=ORANGE)
    b.text(1.75, g0(x_parcel) + 0.07, "parcel: $\\mathrm{D}g/\\mathrm{D}t = 0$", color=GRAY)
    b.set_xlim(0, 3)
    b.set_ylim(0, 1.2)
    b.set_xlabel("$t$ [$L/u$]")
    b.set_ylabel("$g$ [1]")
    save(fig, "advection_probe")


def patch_panel(ax, rhs, x0, y0, side, times, cols):
    for t, col in zip(times, cols):
        n = max(1, int(t / 0.005))
        bnd = rk4(rhs, square_boundary(x0, y0, side), t, n)[-1] if t > 0 else square_boundary(x0, y0, side)
        for ln in mesh_lines(x0, y0, side):
            p = rk4(rhs, ln, t, n)[-1] if t > 0 else ln
            ax.plot(*p, color=col, lw=0.5, alpha=0.8)
        ax.fill(*bnd, color=col, alpha=0.18, lw=0)
        ax.plot(*np.c_[bnd, bnd[:, :1]], color=col, lw=1.2)
        ax.text(*bnd.mean(axis=1), f"{area(bnd) / side ** 2:.2f}", color=col, ha="center", va="center",
                fontsize=9, bbox=dict(fc="white", ec="none", pad=0.6, alpha=0.8))


def volume_flow():
    fig, (a, b) = panels(12, 2.75, 2, sharey=True)
    xs, ys = np.meshgrid(np.linspace(0, 1, 150), np.linspace(0, 1, 150))
    a.contour(xs, ys, np.sin(np.pi * xs) * np.sin(np.pi * ys), levels=np.linspace(0.1, 1, 6), colors="#cccccc",
              linewidths=0.6)
    patch_panel(a, cellular, 0.12, 0.4, 0.2, [0, 0.6, 1.2], [GRAY, BLUE, ORANGE])
    gx, gy = np.meshgrid(np.linspace(0.05, 0.95, 10), np.linspace(0.1, 0.9, 5))
    u, v = compressible(np.array([gx, gy]))
    b.quiver(gx, gy, u, v, color="#bbbbbb", scale=10, width=0.005)
    patch_panel(b, compressible, 0.1, 0.4, 0.2, [0, 0.9, 2.2], [GRAY, BLUE, ORANGE])
    for ax, txt in ((a, "$\\nabla\\cdot\\mathbf{u} = 0$"), (b, "$\\nabla\\cdot\\mathbf{u} = 0.6\\pi\\cos\\pi x$")):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.set_xlabel("$x$ [1]")
        ax.text(0.98, 0.97, txt, ha="right", va="top", bbox=dict(fc="white", ec="none", pad=1))
    a.set_ylabel("$y$ [1]")
    save(fig, "volume_flow")


def disk(cx, cy, r, n=400):
    s = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.array([cx + r * np.cos(s), cy + r * np.sin(s)])


def phase_space_flow():
    fig, (a, b) = panels(12, 2.6, 2, gridspec_kw=dict(width_ratios=(1.25, 1)))
    cols = [GRAY, BLUE, ORANGE]
    for t, col in zip([0, 1.5, 3], cols):
        d = disk(0.0, 1.0, 0.4)
        d = np.array([d[0] + d[1] * t, d[1]])
        a.fill(*d, color=col, alpha=0.2, lw=0)
        a.plot(*np.c_[d, d[:, :1]], color=col, lw=1.2)
        a.text(t * 1.0, 1.0, f"{area(d) / (np.pi * 0.4 ** 2):.2f}", color=col, ha="center", va="center",
               fontsize=9)
        a.text(t * 1.45 + 0.1, 1.62, f"$t = {t:g}$", color=col, ha="center", fontsize=9)
    a.axhline(0, color="#cccccc", lw=0.6)
    a.set_xlim(-0.6, 5.6)
    a.set_ylim(-0.3, 2.0)
    a.set_xlabel("$x$ [$L_0$]")
    a.set_ylabel("$v$ [$v_0$]")
    # Lorentz force in velocity space, ion, B along +z, E along +y: rotation about v_E = (E/B, 0)
    vE = 1.0
    blob = disk(0.0, 0.0, 0.3)
    th = np.linspace(0, 2 * np.pi, 200)
    b.plot(vE + vE * np.cos(th), vE * np.sin(th), color="#cccccc", lw=0.8, ls="--")
    for k, col in zip(range(4), [GRAY, BLUE, ORANGE, BLUE]):
        phi = -k * np.pi / 2  # clockwise: dv/dt = omega_c (v - v_E) x z
        rel = blob - np.array([[vE], [0.0]])
        rot = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]]) @ rel + np.array([[vE], [0.0]])
        b.fill(*rot, color=col, alpha=0.2 if k < 3 else 0.08, lw=0)
        b.plot(*np.c_[rot, rot[:, :1]], color=col, lw=1.2, ls="-" if k < 3 else ":")
        lab = ["0", "\\pi/2", "\\pi", "3\\pi/2"][k]
        c = rot.mean(axis=1)
        b.text(c[0], c[1] + (0.45 if k != 2 else -0.47), f"$\\omega_c t = {lab}$", color=col, ha="center",
               va="center", fontsize=9)
    b.plot(vE, 0, "+", color=INKC, ms=9, mew=1.4)
    b.text(vE + 0.08, 0.1, "$\\mathbf{v}_E$", color=INKC)
    b.set_xlim(-0.9, 2.9)
    b.set_ylim(-1.5, 1.5)
    b.set_aspect("equal")
    b.set_xlabel("$v_x$ [$E/B$]")
    b.set_ylabel("$v_y$ [$E/B$]")
    save(fig, "phase_space_flow")


INKC = "#1c1f23"


def distribution_cells():
    import matplotlib.pyplot as plt
    fig0, _ = figure(1, 1)
    plt.close(fig0)
    fig = plt.figure(figsize=(slide_width(12), 2.7), layout="constrained")
    gs = fig.add_gridspec(2, 2, width_ratios=(5, 1), height_ratios=(1, 3.2))
    ax = fig.add_subplot(gs[1, 0])
    top = fig.add_subplot(gs[0, 0], sharex=ax)
    side = fig.add_subplot(gs[1, 1], sharey=ax)
    n = 3000
    nx = lambda x: 1 + 0.6 * np.sin(2 * np.pi * x)  # noqa: E731
    xs = []
    while len(xs) < n:
        c = RNG.uniform(0, 1, 4 * n)
        keep = RNG.uniform(0, 1.6, 4 * n) < nx(c)
        xs.extend(c[keep].tolist())
    x = np.array(xs[:n])
    v = RNG.normal(0, 1, n)
    ax.plot(x, v, ".", color=BLUE, ms=1.6, alpha=0.7)
    x0, dx, v0, dv = 0.2, 0.1, 0.5, 0.5
    inside = (x >= x0) & (x < x0 + dx) & (v >= v0) & (v < v0 + dv)
    ax.add_patch(plt.Rectangle((x0, v0), dx, dv, fill=False, ec=ORANGE, lw=1.6))
    ax.plot(x[inside], v[inside], ".", color=ORANGE, ms=2.6)
    ax.annotate(f"$\\Delta N = {inside.sum()}$ in $\\Delta x\\,\\Delta v$", (x0 + dx, v0 + dv),
                xytext=(0.36, 2.6), color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(-3.5, 3.5)
    ax.set_xlabel("$x$ [$L$]")
    ax.set_ylabel("$v$ [$v_\\mathrm{th}$]")
    grid = np.linspace(0, 1, 200)
    top.hist(x, bins=25, range=(0, 1), density=True, color="#c6dbef", ec="white")
    top.plot(grid, nx(grid), color=BLUE)
    top.set_ylabel("$n(x)$")
    top.tick_params(labelbottom=False)
    vg = np.linspace(-3.5, 3.5, 200)
    side.hist(v, bins=28, range=(-3.5, 3.5), density=True, orientation="horizontal", color="#c6dbef", ec="white")
    side.plot(np.exp(-vg ** 2 / 2) / np.sqrt(2 * np.pi), vg, color=BLUE)
    side.set_xlabel("$\\int f\\,\\mathrm{d}x$")
    side.tick_params(labelleft=False)
    save(fig, "distribution_cells")


# phase-space grid of the pendulum figures
XL, VL = np.pi, 2.6
F0 = dict(x=1.4, v=0.0, s=0.3)


def f0(x, v):
    return np.exp(-((x - F0["x"]) ** 2 + (v - F0["v"]) ** 2) / (2 * F0["s"] ** 2)) / (2 * np.pi * F0["s"] ** 2)


def evolved(t, nx=360, nv=300):
    """f(z, t) = f0(z0) with z0 from backward characteristics of the pendulum."""
    x, v = np.meshgrid(np.linspace(-XL, XL, nx), np.linspace(-VL, VL, nv))
    if t > 0:
        z0 = rk4(lambda z: -pendulum(z), np.array([x, v]), t, int(t / 0.02))[-1]
        z0[0] = (z0[0] + np.pi) % (2 * np.pi) - np.pi
    else:
        z0 = np.array([x, v])
    return x, v, f0(*z0)


def well_axes(ax):
    ax.set_xlim(-XL, XL)
    ax.set_ylim(-VL, VL)
    ax.set_xlabel("$x$ [1]")


def vlasov_well():
    import matplotlib.pyplot as plt
    fig0, _ = figure(1, 1)
    plt.close(fig0)
    fig, axs = plt.subplots(2, 3, figsize=(slide_width(12), 2.8), layout="constrained", sharex=True,
                            gridspec_kw=dict(height_ratios=(2.2, 1)))
    sep = np.linspace(-XL, XL, 300)
    for j, t in enumerate([0, 8, 40]):
        x, v, f = evolved(t)
        a = axs[0, j]
        a.pcolormesh(x, v, f, cmap=CMAP, vmin=0, vmax=f0(F0["x"], F0["v"]), shading="auto", rasterized=True)
        a.plot(sep, 2 * np.cos(sep / 2), color=GRAY, lw=0.6, ls="--")
        a.plot(sep, -2 * np.cos(sep / 2), color=GRAY, lw=0.6, ls="--")
        well_axes(a)
        a.set_xlabel("")
        a.set_title(f"$\\omega_0 t = {t}$", fontsize=10)
        dens = f.sum(axis=0) * (v[1, 0] - v[0, 0])
        axs[1, j].plot(x[0], dens, color=BLUE)
        axs[1, j].set_ylim(0, 1.45)
        axs[1, j].set_xlabel("$x$ [1]")
    axs[0, 0].set_ylabel("$v$ [$\\omega_0$]")
    axs[1, 0].set_ylabel("$n(x)$")
    for a in axs[0, 1:]:
        a.tick_params(labelleft=False)
    for a in axs[1, 1:]:
        a.tick_params(labelleft=False)
    save(fig, "vlasov_well")


def smoothing_advection():
    fig, axs = panels(12, 2.2, 3, sharey=True)
    t, n, h = 8.0, 600, 0.18
    z = np.array([RNG.normal(F0["x"], F0["s"], n), RNG.normal(F0["v"], F0["s"], n)])
    z = rk4(pendulum, z, t, int(t / 0.01))[-1]
    z[0] = (z[0] + np.pi) % (2 * np.pi) - np.pi
    x, v, f = evolved(t)
    fh = np.zeros_like(f)
    for shift in (-2 * np.pi, 0, 2 * np.pi):  # periodic images in x
        dx = x[..., None] - (z[0] + shift)
        dv = v[..., None] - z[1]
        fh += np.exp(-(dx ** 2 + dv ** 2) / (2 * h ** 2)).sum(-1)
    fh /= n * 2 * np.pi * h ** 2
    vmax = f0(F0["x"], F0["v"])
    axs[0].plot(z[0], z[1], ".", color=BLUE, ms=2.2)
    axs[1].pcolormesh(x, v, fh, cmap=CMAP, vmin=0, vmax=vmax, shading="auto", rasterized=True)
    axs[2].pcolormesh(x, v, f, cmap=CMAP, vmin=0, vmax=vmax, shading="auto", rasterized=True)
    for a, lab in zip(axs, [f"{n} particles", f"$f_h$, $h = {h}$", "$f$ exact"]):
        well_axes(a)
        a.text(-XL + 0.15, VL - 0.2, lab, va="top", fontsize=9, bbox=dict(fc="white", ec="none", pad=1, alpha=0.8))
    axs[0].set_ylabel("$v$ [$\\omega_0$]")
    save(fig, "smoothing_advection")


def pair_marginal():
    import matplotlib.pyplot as plt
    fig0, _ = figure(1, 1)
    plt.close(fig0)
    fig, axs = plt.subplots(2, 2, figsize=(slide_width(6), 2.9), layout="constrained", sharex=True,
                            gridspec_kw=dict(height_ratios=(1, 3)))
    g = np.linspace(0, 1, 301)
    x1, x2 = np.meshgrid(g, g, indexing="ij")
    d = np.abs(x1 - x2)
    d = np.minimum(d, 1 - d)
    hole = -0.9 * np.exp(-d ** 2 / (2 * 0.06 ** 2))
    c = hole - hole.mean(axis=1, keepdims=True)  # every row integrates to zero: f1 unchanged
    for j, F2 in enumerate([np.ones_like(x1), 1 + c]):
        a = axs[1, j]
        a.pcolormesh(x1, x2, F2.T, cmap=CMAP, vmin=0, vmax=1.4, shading="auto", rasterized=True)
        a.set_xlabel("$x_1$ [$L$]")
        f1 = np.trapezoid(F2, g, axis=1)
        axs[0, j].plot(g, f1, color=BLUE)
        axs[0, j].set_ylim(0, 1.4)
        axs[0, j].set_title(["uncorrelated", "correlated"][j], fontsize=10)
    axs[1, 0].set_ylabel("$x_2$ [$L$]")
    axs[0, 0].set_ylabel("$f_1(x_1)$")
    axs[1, 1].tick_params(labelleft=False)
    axs[0, 1].tick_params(labelleft=False)
    save(fig, "pair_marginal")


def free_paths():
    """2D Monte Carlo: rays among random disks of radius A, density N2; sigma = 2A, lambda = 1/(N2 sigma)."""
    fig, (a, b) = panels(12, 2.6, 2, gridspec_kw=dict(width_ratios=(1.5, 1)))
    box, n_disk, rad = 120.0, 2880, 0.3
    centres = RNG.uniform(0, box, (n_disk, 2))
    lam = 1 / (n_disk / box ** 2 * 2 * rad)

    def first_hit(p, d, skip=None):
        rel = centres - p
        along = rel @ d
        perp2 = (rel ** 2).sum(1) - along ** 2
        ok = (along > 0) & (perp2 < rad ** 2)
        if skip is not None:
            ok[skip] = False  # the disk just left
        if not ok.any():
            return np.inf, None
        t = along[ok] - np.sqrt(rad ** 2 - perp2[ok])
        k = np.argmin(t)
        return t[k], np.flatnonzero(ok)[k]

    def free_start(lo, hi):
        while True:
            p = RNG.uniform(lo, hi, 2)
            if (((centres - p) ** 2).sum(1) > rad ** 2).all():
                return p

    # one zigzag path in the window [40, 80] x [45, 70]
    p = free_start(57, 63)
    path, k = [p], None
    while len(path) < 9:
        ang = RNG.uniform(0, 2 * np.pi)
        d = np.array([np.cos(ang), np.sin(ang)])
        t, hit = first_hit(p, d, k)
        q = p + t * d
        if not (np.isfinite(t) and 42 < q[0] < 78 and 47 < q[1] < 68):
            continue  # keep the drawn path inside the window
        p, k = q, hit
        path.append(p)
    path = np.array(path)
    from matplotlib.patches import Circle
    org = np.array([40.0, 45.0])  # window origin; axes in units of lambda_mfp
    for c in centres:
        if 38 < c[0] < 82 and 43 < c[1] < 72:
            a.add_patch(Circle((c - org) / lam, rad / lam, color=GRAY, alpha=0.55, lw=0))
    w = (path - org) / lam
    a.plot(w[:, 0], w[:, 1], color=BLUE, lw=1.3)
    a.plot(w[1:-1, 0], w[1:-1, 1], "o", color=ORANGE, ms=3.5)
    a.plot(*w[0], "o", color=BLUE, ms=5, mfc="white", mew=1.3)
    a.set_xlim(0, 40 / lam)
    a.set_ylim(0, 25 / lam)
    a.set_aspect("equal")
    a.set_xlabel("$x$ [$\\lambda_\\mathrm{mfp}$]")
    a.set_ylabel("$y$ [$\\lambda_\\mathrm{mfp}$]")
    # free-path statistics
    ells = []
    for _ in range(3000):
        p = free_start(45, box - 45)
        ang = RNG.uniform(0, 2 * np.pi)
        t, _ = first_hit(p, np.array([np.cos(ang), np.sin(ang)]))
        ells.append(t)
    ells = np.array(ells)
    ells = ells[np.isfinite(ells)]  # rays leaving the box unhit (a few per mille)
    b.hist(ells / lam, bins=30, range=(0, 4), density=True, color="#c6dbef", ec="white")
    g = np.linspace(0, 4, 200)
    b.plot(g, np.exp(-g), color=BLUE)
    b.text(1.2, 0.6, "$e^{-\\ell/\\lambda}$", color=BLUE)
    b.text(2.0, 0.85, f"mean {ells.mean() / lam:.2f} $\\lambda$", color=GRAY, fontsize=9)
    b.set_xlim(0, 4)
    b.set_xlabel("$\\ell$ [$\\lambda_\\mathrm{mfp}$]")
    b.set_ylabel("$p(\\ell)$ [$1/\\lambda_\\mathrm{mfp}$]")
    save(fig, "free_paths")


def coulomb_orbits():
    """Repulsive Coulomb scattering off a fixed charge; lengths in b_90, speeds in v: r'' = r/|r|^3."""
    fig, (a, b) = panels(12, 2.6, 2, gridspec_kw=dict(width_ratios=(1.5, 1)))
    rhs = lambda z: np.array([z[2], z[3], *(z[:2] / np.hypot(z[0], z[1]) ** 3)])  # noqa: E731
    bs = np.array([0.25, 0.5, 1.0, 2.0, 4.0])
    measured = []
    for bb in np.geomspace(0.1, 30, 16):
        z = rk4(rhs, np.array([-200.0, bb, 1.0, 0.0]), 400.0, 40000)[-1]
        measured.append((bb, np.arctan2(z[3], z[2])))
    for bb, col in zip(bs, [GRAY, GRAY, ORANGE, BLUE, BLUE]):
        path = rk4(rhs, np.array([-12.0, bb, 1.0, 0.0]), 26.0, 5200)
        keep = (np.abs(path[:, 0]) < 12) & (path[:, 1] < 9) & (path[:, 1] > -1)
        end = path[keep][-1]
        a.plot(path[keep, 0], path[keep, 1], color=col, lw=1.4 if bb == 1 else 1.0)
        a.text(end[0] + (0.3 if end[0] > -11 else 0.2), end[1] - 0.2 if end[1] > 8 else end[1] + 0.3,
               f"$b = {bb:g}$", color=col, fontsize=9, ha="left" if end[0] > -11 else "left", va="top")
    a.plot(0, 0, "o", color=INKC, ms=6)
    a.set_xlim(-12, 12)
    a.set_ylim(-1, 9)
    a.set_aspect("equal")
    a.set_xlabel("$x$ [$b_{90}$]")
    a.set_ylabel("$y$ [$b_{90}$]")
    m = np.array(measured)
    g = np.geomspace(0.1, 30, 200)
    b.loglog(g, np.degrees(2 * np.arctan(1 / g)), color=BLUE)
    b.loglog(m[:, 0], np.degrees(m[:, 1]), "o", color=ORANGE, ms=3.5)
    b.loglog(g[g > 2], np.degrees(2 / g[g > 2]), color=GRAY, ls="--")
    b.axhline(90, color="#cccccc", lw=0.6)
    b.text(0.12, 105, "$90^\\circ$", color=GRAY, fontsize=9)
    b.text(3.0, 60, "$2\\arctan(b_{90}/b)$", color=BLUE, fontsize=9)
    b.text(5.0, 6.0, "$2 b_{90}/b$", color=GRAY, fontsize=9)
    b.set_xlabel("$b$ [$b_{90}$]")
    b.set_ylabel("$\\chi$ [deg]")
    save(fig, "coulomb_orbits")


def collisionality():
    """Electron mean free path lambda = v_th/nu_ei over (n_e, T_e); NRL formulary nu_ei and ln Lambda."""
    import matplotlib.pyplot as plt
    from si import EXAMPLE_PLASMAS
    fig, ax = panels(12, 2.75, 1)

    def ln_lambda(n, t):  # n [m^-3], T [eV]; NRL electron-ion
        ncc = n * 1e-6
        return np.where(t < 10, 23 - np.log(ncc ** 0.5 * t ** -1.5), 24 - np.log(ncc ** 0.5 / t))

    def mfp(n, t):
        nu = 2.91e-12 * n * ln_lambda(n, t) * t ** -1.5  # [s^-1], n in m^-3 (NRL: 2.91e-6 n[cm^-3])
        vth = np.sqrt(2 * t * 1.602176634e-19 / 9.1093837015e-31)
        return vth / nu

    n, t = np.meshgrid(np.geomspace(1e6, 1e28, 300), np.geomspace(1e-2, 1e5, 300))
    ok = ln_lambda(n, t) > 2
    lm = np.where(ok, np.log10(mfp(n, t)), np.nan)
    cs = ax.contourf(n, t, lm, levels=np.arange(-8, 19, 2), cmap=CMAP)
    ax.contour(n, t, lm, levels=np.arange(-8, 19, 2), colors="white", linewidths=0.4)
    cb = fig.colorbar(cs, ax=ax, pad=0.01)
    cb.set_label("$\\log_{10}\\,\\lambda_\\mathrm{mfp}$ [m]")
    for name, (nn, tt) in EXAMPLE_PLASMAS.items():
        ax.plot(nn, tt, "o", color=ORANGE, ms=5)
        val = mfp(nn, tt)
        ax.annotate(f"{name}\n$10^{{{int(round(np.log10(val)))}}}$ m", (nn, tt), xytext=(6, 4),
                    textcoords="offset points", color=INKC, fontsize=9,
                    bbox=dict(fc="white", ec="none", pad=0.8, alpha=0.75))
    ax.fill_between([1e6, 1e28], 1e-2, 1e-2, color="none")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("$n_e$ [m$^{-3}$]")
    ax.set_ylabel("$k_B T_e$ [eV]")
    ax.text(3e25, 2e-2, "$\\ln\\Lambda < 2$", color=GRAY, fontsize=9, ha="center")
    save(fig, "collisionality")


if __name__ == "__main__":
    import sys
    for name in sys.argv[1:] or ["flow_lagrange_euler", "advection_probe", "volume_flow", "phase_space_flow",
                                 "distribution_cells", "vlasov_well", "smoothing_advection", "pair_marginal",
                                 "free_paths", "coulomb_orbits", "collisionality"]:
        globals()[name]()
