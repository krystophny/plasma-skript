"""Ambipolar expansion of a one-dimensional electron-ion slab.

Model: drift-diffusion fluids for ions and electrons with Poisson's equation,

    dn_alpha/dt + dGamma_alpha/dx = 0,
    Gamma_i = mu_i n_i E - D_i dn_i/dx,   Gamma_e = -mu_e n_e E - D_e dn_e/dx,
    dE/dx = e (n_i - n_e)/eps_0,

with Einstein relations D_alpha = mu_alpha k_B T_alpha/e and constant
temperatures.  Normalization: x' = x/L with L the initial slab half-width,
n' = n/n_0 with n_0 the initial density, t' = t D_i/L^2, E' = e E L/(k_B T_e).
Then

    Gamma_i' = theta n_i' E' - dn_i'/dx',   Gamma_e' = (D_e/D_i)(-n_e' E' - dn_e'/dx'),
    dE'/dx' = (L/lambda_De)^2 (n_i' - n_e'),

with theta = T_e/T_i and lambda_De = (eps_0 k_B T_e/(n_0 e^2))^(1/2).
Parameters: mu_e/mu_i = 50, T_e/T_i = 2 (D_e/D_i = 100), L/lambda_De = 10,
initial n_e = n_i = smoothed top hat |x| < L, closed box |x| < 10 L.
Numerics: finite volumes, Scharfetter-Gummel fluxes (exact for a constant
field between cells), explicit time steps, E from integrating Poisson's
equation from the wall where E = 0.

Check (scripts/check-physics.py): for linear diffusion of any profile the
variance grows as sigma^2(t) = sigma^2(0) + 2 D t.  The variance slope of the
ions once the electrons are locked is compared with

    D_a = (mu_i D_e + mu_e D_i)/(mu_i + mu_e) = 2.94 D_i  (~ D_i (1 + T_e/T_i) = 3 D_i),

and the field in the core with the ambipolar field
E_a = (D_i - D_e)/(mu_i + mu_e) (dn/dx)/n.
"""

from manim import *
import numpy as np

from style import (
    AXIS, CURVE_WIDTH, E_FIELD, EASE, ELECTRON, FAINT, GREEN, INK, ION, LINEAR,
    MATH_SIZE, MATH_SMALL, MUTED, SMALL_SIZE, THIN_WIDTH, StyledScene, axes,
    label, math,
)

MU_RATIO = 50.0              # mu_e/mu_i [1]
THETA = 2.0                  # T_e/T_i [1]
L_DEBYE = 10.0               # L/lambda_De [1]
HALF_BOX = 10.0              # box half-width / L [1]
CELLS = 500
EDGE = 0.05                  # initial edge width / L [1]
T_END = 1.5                  # t D_i/L^2 [1]
T_FIRST = 1e-5
N_SNAP = 140


def d_electron(mu_ratio=MU_RATIO, theta=THETA):
    """D_e/D_i from the Einstein relations."""
    return mu_ratio * theta


def d_ambipolar(mu_ratio=MU_RATIO, theta=THETA):
    """D_a/D_i = (mu_i D_e + mu_e D_i)/((mu_i + mu_e) D_i)."""
    return (d_electron(mu_ratio, theta) + mu_ratio) / (1.0 + mu_ratio)


def bernoulli(u):
    """B(u) = u/(e^u - 1) with B(0) = 1."""
    u = np.asarray(u, float)
    small = np.abs(u) < 1e-6
    safe = np.where(small, 1.0, u)
    return np.where(small, 1.0 - u / 2, safe / np.expm1(safe))


def sg_flux(n, drift, diff, dx):
    """Scharfetter-Gummel face flux of Gamma = diff (drift n - dn/dx).

    `drift` is the drift factor on the interior faces (len(n) - 1)."""
    u = drift * dx
    return diff / dx * (bernoulli(-u) * n[:-1] - bernoulli(u) * n[1:])


def field(n_i, n_e, dx, l_debye=L_DEBYE):
    """E' on the interior faces from Poisson with E'(left wall) = 0."""
    return np.cumsum(l_debye**2 * (n_i - n_e) * dx)[:-1]


def initial(cells=CELLS, half_box=HALF_BOX, edge=EDGE):
    dx = 2 * half_box / cells
    x = -half_box + dx * (np.arange(cells) + 0.5)
    n = 0.5 * (np.tanh((x + 1) / edge) - np.tanh((x - 1) / edge))
    return x, dx, n


def snapshot_times(t_first=T_FIRST, t_end=T_END, n=N_SNAP):
    return np.geomspace(t_first, t_end, n)


def simulate(times=None, cells=CELLS, mu_ratio=MU_RATIO, theta=THETA, l_debye=L_DEBYE):
    """Return x, snapshot times, n_i, n_e (snapshots x cells) and E' on faces."""
    times = snapshot_times() if times is None else np.asarray(times)
    x, dx, n0 = initial(cells)
    d_e = d_electron(mu_ratio, theta)
    n_i, n_e = n0.copy(), n0.copy()
    # stability: diffusion and dielectric relaxation (rate l_debye^2 (d_e + theta))
    dt_max = min(0.4 * dx * dx / d_e, 0.5 / (l_debye**2 * (d_e + theta)))
    out_i, out_e, out_E = [], [], []
    t = 0.0
    for target in times:
        while t < target - 1e-15:
            dt = min(dt_max, target - t)
            e_face = field(n_i, n_e, dx, l_debye)
            g_i = sg_flux(n_i, theta * e_face, 1.0, dx)
            g_e = sg_flux(n_e, -e_face, d_e, dx)
            n_i[:-1] -= dt * g_i / dx
            n_i[1:] += dt * g_i / dx
            n_e[:-1] -= dt * g_e / dx
            n_e[1:] += dt * g_e / dx
            t += dt
        out_i.append(n_i.copy())
        out_e.append(n_e.copy())
        out_E.append(field(n_i, n_e, dx, l_debye))
    return x, times, np.array(out_i), np.array(out_e), np.array(out_E)


def variance(x, n):
    """Second moment about the centre, per snapshot (rows of n)."""
    mass = n.sum(axis=-1)
    mean = (n * x).sum(axis=-1) / mass
    return (n * x**2).sum(axis=-1) / mass - mean**2


def measured_diffusion(times, x, n, t_from=0.3):
    """D/D_i from the least-squares slope of sigma^2(t) for t >= t_from."""
    sel = times >= t_from
    return 0.5 * np.polyfit(times[sel], variance(x, n[sel]), 1)[0]


def ambipolar_field(x, n, mu_ratio=MU_RATIO, theta=THETA):
    """E_a' = e E_a L/(k_B T_e) at the faces from the quasi-neutral profile n."""
    dx = x[1] - x[0]
    d_e = d_electron(mu_ratio, theta)
    # (D_i - D_e)/(mu_i + mu_e) in units of k_B T_e/(e) : divide by D_e/mu_e = T_e
    coeff = (1.0 - d_e) / (1.0 + mu_ratio) * mu_ratio / d_e
    n_face = 0.5 * (n[1:] + n[:-1])
    return coeff * np.diff(n) / dx / n_face


X_VIEW = 6.0                 # shown |x|/L [1]
LOG_T = (-5.0, 0.5)          # log10 of t D_i/L^2 on the clock axis
LOG_S = (-5.0, 2.5)          # log10 of the variance growth / L^2


class AmbipolarExpansion(StyledScene):
    """Densities, field and variance growth of one expanding slab."""

    def build(self):
        x, times, n_i, n_e, e_face = simulate()
        x0, _, n0 = initial()
        s0 = variance(x0, n0)
        grow_i = variance(x, n_i) - s0
        grow_e = variance(x, n_e) - s0
        d_a, d_e = d_ambipolar(), d_electron()
        d_meas = measured_diffusion(times, x, n_i)
        xf = 0.5 * (x[1:] + x[:-1])
        view = np.abs(x) <= X_VIEW
        view_f = np.abs(xf) <= X_VIEW
        last = len(times) - 1
        e_max = 6.0

        tracker = ValueTracker(0.0)

        def blend(arr):
            f = tracker.get_value() * last
            k = min(int(f), last - 1)
            return (1 - (f - k)) * arr[k] + (f - k) * arr[k + 1]

        def now():
            f = tracker.get_value() * last
            k = min(int(f), last - 1)
            w = f - k
            return float(np.exp((1 - w) * np.log(times[k]) + w * np.log(times[k + 1])))

        def tick_x(ax, to, values, y0):
            return VGroup(*[math(t, color=MUTED, size=MATH_SMALL).next_to(to(ax, v, y0), DOWN, buff=0.12)
                            for v, t in values])

        def tick_y(ax, to, values, x0):
            return VGroup(*[math(t, color=MUTED, size=MATH_SMALL).next_to(to(ax, x0, v), LEFT, buff=0.1)
                            for v, t in values])

        # Axes with the origin at the lower-left corner; data are shifted.
        def at_d(ax, a, b):
            return ax.c2p(a + X_VIEW, b)

        def at_e(ax, a, b):
            return ax.c2p(a + X_VIEW, np.clip(b, -e_max, e_max) + e_max)

        def at_v(ax, a, b):
            return ax.c2p(a - LOG_T[0], b - LOG_S[0])

        # --- densities -------------------------------------------------------
        dens = axes([0, 2 * X_VIEW, 1], [0, 1.2, 0.5], 5.4, 2.0).move_to([-3.55, 1.5, 0])
        x_vals = [(-4, "-4"), (0, "0"), (4, "4")]
        dens_txt = VGroup(
            math(r"n_\alpha/n_0\ [1]", color=MUTED, size=MATH_SMALL)
            .next_to(dens.c2p(0, 1.2), UP, buff=0.12).align_to(dens.c2p(0, 0), LEFT),
            tick_y(dens, at_d, [(0, "0"), (1, "1")], -X_VIEW),
            tick_x(dens, at_d, x_vals, 0),
        )
        marks_x = np.arange(-X_VIEW + 0.5, X_VIEW, 1.0)

        def density_curves():
            ni, ne = blend(n_i), blend(n_e)
            ion = DashedVMobject(VMobject(stroke_color=ION, stroke_width=CURVE_WIDTH).set_points_as_corners(
                [at_d(dens, a, b) for a, b in zip(x[view], ni[view])]), num_dashes=60)
            ele = VMobject(stroke_color=ELECTRON, stroke_width=CURVE_WIDTH - 1).set_points_as_corners(
                [at_d(dens, a, b) for a, b in zip(x[view], ne[view])])
            group = VGroup(ele, ion)
            for xm in marks_x:
                group.add(Dot(at_d(dens, xm, np.interp(xm, x, ne)), radius=0.06, color=ELECTRON))
                group.add(Triangle(color=ION, fill_opacity=1, stroke_width=0).scale(0.08)
                          .move_to(at_d(dens, xm + 0.5, np.interp(xm + 0.5, x, ni))))
            return group

        # --- electric field ----------------------------------------------------
        efa = axes([0, 2 * X_VIEW, 1], [0, 2 * e_max, 3], 5.4, 2.0).move_to([-3.55, -1.6, 0])
        zero = DashedVMobject(Line(at_e(efa, -X_VIEW, 0), at_e(efa, X_VIEW, 0), color=FAINT,
                                   stroke_width=1.2), num_dashes=40)
        efa_txt = VGroup(
            math(r"eEL/(k_BT_e)\ [1]", color=MUTED, size=MATH_SMALL)
            .next_to(efa.c2p(0, 2 * e_max), UP, buff=0.12).align_to(efa.c2p(0, 0), LEFT),
            tick_y(efa, at_e, [(-6, "-6"), (0, "0"), (6, "6")], -X_VIEW),
            tick_x(efa, at_e, x_vals, -e_max),
        )
        efa_txt.add(math(r"x/L\ [1]", color=MUTED, size=MATH_SMALL)
                    .next_to(efa_txt[2], DOWN, buff=0.1).align_to(efa.c2p(2 * X_VIEW, 0), RIGHT))

        def field_curve():
            ef = blend(e_face)
            return VMobject(stroke_color=E_FIELD, stroke_width=CURVE_WIDTH - 1).set_points_as_corners(
                [at_e(efa, a, b) for a, b in zip(xf[view_f], ef[view_f])])

        # --- variance growth, log-log ----------------------------------------
        var = axes([0, LOG_T[1] - LOG_T[0], 1], [0, LOG_S[1] - LOG_S[0], 1], 4.9, 4.9).move_to([4.0, -0.5, 0])
        var_txt = VGroup(
            math(r"(\sigma^2-\sigma_0^2)/L^2\ [1]", color=MUTED, size=MATH_SMALL)
            .next_to(var.c2p(0, LOG_S[1] - LOG_S[0]), UP, buff=0.12).align_to(var.c2p(0, 0), LEFT)
            .shift(LEFT * 0.9),
            tick_x(var, at_v, [(-4, r"10^{-4}"), (-2, r"10^{-2}"), (0, r"10^{0}")], LOG_S[0]),
            tick_y(var, at_v, [(-4, r"10^{-4}"), (-2, r"10^{-2}"), (0, r"10^{0}"), (2, r"10^{2}")], LOG_T[0]),
        )
        var_txt.add(math(r"tD_i/L^2\ [1]", color=MUTED, size=MATH_SMALL)
                    .next_to(var_txt[1], DOWN, buff=0.12).align_to(var.c2p(LOG_T[1] - LOG_T[0], 0), RIGHT))

        def ref_line(d, style, color):
            lo = LOG_T[0]
            hi = min(LOG_T[1], LOG_S[1] - np.log10(2 * d))
            line = Line(at_v(var, lo, np.log10(2 * d) + lo), at_v(var, hi, np.log10(2 * d) + hi),
                        color=color, stroke_width=THIN_WIDTH)
            if style == "dash":
                return DashedVMobject(line, num_dashes=28)
            return DashedVMobject(line, num_dashes=60, dashed_ratio=0.25)

        lines = VGroup(ref_line(d_e, "dot", MUTED), ref_line(d_a, "dash", GREEN), ref_line(1.0, "dot", MUTED))
        tags = VGroup(
            math(r"2D_e t", color=MUTED, size=MATH_SMALL)
            .next_to(at_v(var, -3.2, -3.2 + np.log10(2 * d_e)), UP + LEFT, buff=0.02),
            math(r"2D_a t", color=GREEN, size=MATH_SMALL)
            .next_to(at_v(var, -3.8, -3.8 + np.log10(2 * d_a)), UP + LEFT, buff=0.02),
            math(r"2D_i t", color=MUTED, size=MATH_SMALL)
            .next_to(at_v(var, -1.2, -1.2 + np.log10(2.0)), DOWN + RIGHT, buff=0.05),
        )

        lt = np.log10(times)

        def growth_curves():
            k = min(int(tracker.get_value() * last) + 1, last)
            group = VGroup()
            for g, color, kind in ((grow_e, ELECTRON, "dot"), (grow_i, ION, "tri")):
                pts = [at_v(var, lt[j], np.log10(g[j])) for j in range(k + 1)]
                group.add(VMobject(stroke_color=color, stroke_width=CURVE_WIDTH - 1).set_points_as_corners(pts))
                group.add(Dot(pts[-1], radius=0.08, color=color) if kind == "dot" else
                          Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.11).move_to(pts[-1]))
            return group

        keys = VGroup(
            VGroup(Dot(radius=0.07, color=ELECTRON),
                   math(r"\text{electrons}", color=ELECTRON, size=MATH_SMALL)).arrange(RIGHT, buff=0.12),
            VGroup(Triangle(color=ION, fill_opacity=1, stroke_width=0).scale(0.1),
                   math(r"\text{ions}", color=ION, size=MATH_SMALL)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.45).move_to([-3.2, 3.3, 0])

        clock = always_redraw(lambda: math(
            rf"tD_i/L^2 = {now():.5f}" if now() < 1e-2 else rf"tD_i/L^2 = {now():.3f}",
            color=INK, size=MATH_SMALL).move_to([2.6, 3.3, 0]).align_to([0.9, 0, 0], LEFT))

        self.play(Create(dens), Create(efa), Create(var), FadeIn(dens_txt), FadeIn(efa_txt),
                  FadeIn(var_txt), FadeIn(keys), FadeIn(zero), run_time=1.0, rate_func=EASE)
        self.play(Create(lines), FadeIn(tags), run_time=1.0, rate_func=EASE)
        self.add(always_redraw(density_curves), always_redraw(field_curve),
                 always_redraw(growth_curves), clock)
        self.wait(0.5)
        self.play(tracker.animate.set_value(1.0), run_time=16.0, rate_func=LINEAR)
        result = VGroup(
            math(rf"\text{{slab: }} D/D_i = {d_meas:.2f}", color=ION, size=MATH_SMALL),
            math(rf"D_a/D_i = {d_a:.2f}", color=GREEN, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)
        result.next_to(var.c2p(LOG_T[1] - LOG_T[0], 0), UP + LEFT, buff=0.15)
        self.play(FadeIn(result), run_time=0.8, rate_func=EASE)
        self.wait(3.0)
