"""From particles to a distribution function to fluid moments, in one dimension.

Position is shown as x/L [1] on one period 0 <= x/L < 1 and velocity as
v/v_th [1], with v_th = sqrt(2 k_B T / m) of the background electrons.  The
model distribution, in units of n_0 / v_th, is a density-modulated Maxwellian
at rest plus a uniform, colder beam,

    f = (1 + A cos 2 pi x) exp(-v^2)/sqrt(pi)
        + BEAM exp(-(v - V_B)^2 / S_B^2) / (sqrt(pi) S_B),

so that its first two velocity moments are known exactly:

    n / n_0 = 1 + A cos 2 pi x + BEAM,
    u / v_th = BEAM V_B / (n / n_0).

The scene draws N_PARTICLES seeded samples of f as points in phase space,
replaces them by the smooth f on a grid, and integrates over v to obtain
n(x) and u(x); the binned sample moments appear as markers on the exact
curves.  The density alone no longer shows that part of the particles forms
a beam.  This is an illustration of coarse graining, not a simulation.
"""

from manim import *
import numpy as np

from style import (
    EASE, ELECTRON, FAINT, GREEN, GRID, INK, LINEAR, MUTED, PURPLE, StyledScene,
    axes, math,
    MATH_SIZE, MATH_SMALL,
)


A = 0.5
BEAM = 0.25
V_B = 2.5
S_B = 0.35
N_PARTICLES = 700
SEED = 3
N_BINS = 10


def distribution(x, v, a=0.5, beam=0.25, v_b=2.5, s_b=0.35):
    """f / (n_0 / v_th) at x/L and v/v_th."""
    background = (1 + a * np.cos(2 * np.pi * x)) * np.exp(-v * v) / np.sqrt(np.pi)
    stream = beam * np.exp(-(v - v_b) ** 2 / s_b**2) / (np.sqrt(np.pi) * s_b)
    return background + stream


def density(x, a=0.5, beam=0.25):
    """n / n_0, the zeroth velocity moment of distribution()."""
    return 1 + a * np.cos(2 * np.pi * x) + beam


def bulk_velocity(x, a=0.5, beam=0.25, v_b=2.5):
    """u / v_th, the first velocity moment divided by the density."""
    return beam * v_b / density(x, a, beam)


def sample_particles(seed=3, n=700, a=0.5, beam=0.25, v_b=2.5, s_b=0.35):
    """Seeded samples (x, v) of distribution(); the beam holds beam/(1+beam) of them."""
    rng = np.random.default_rng(seed)
    n_beam = int(round(n * beam / (1 + beam)))
    n_bg = n - n_beam
    xs = []
    while len(xs) < n_bg:
        trial = rng.uniform(0, 1, 4 * n_bg)
        keep = rng.uniform(0, 1 + a, trial.size) < 1 + a * np.cos(2 * np.pi * trial)
        xs.extend(trial[keep].tolist())
    x_bg = np.array(xs[:n_bg])
    v_bg = rng.normal(0, 1 / np.sqrt(2), n_bg)
    x_beam = rng.uniform(0, 1, n_beam)
    v_beam = rng.normal(v_b, s_b / np.sqrt(2), n_beam)
    return np.concatenate([x_bg, x_beam]), np.concatenate([v_bg, v_beam])


def binned_moments(x, v, bins=10, total=1.25):
    """Bin centres, n/n_0 and u/v_th estimated from samples; total = integral of n/n_0."""
    edges = np.linspace(0, 1, bins + 1)
    index = np.minimum((x * bins).astype(int), bins - 1)
    counts = np.bincount(index, minlength=bins).astype(float)
    momentum = np.bincount(index, weights=v, minlength=bins)
    n_est = counts / x.size * total * bins
    u_est = momentum / np.maximum(counts, 1)
    return 0.5 * (edges[:-1] + edges[1:]), n_est, u_est


class ParticlesToMoments(StyledScene):
    """Particles in phase space, their smooth f(x, v), and the moments n(x), u(x)."""

    def build(self):
        width = 7.8
        left = -0.5
        phase = axes([0, 1, 0.25], [-3, 4, 1], width, 3.3).move_to([left + 0.3, 1.55, 0])
        dens = axes([0, 1, 0.25], [0, 2, 1], width, 1.05).move_to([left + 0.3, -1.05, 0])
        flow = axes([0, 1, 0.25], [0, 1, 0.5], width, 1.05).move_to([left + 0.3, -2.6, 0])

        def y_label(ax, tex):
            lab = math(tex, color=MUTED, size=MATH_SMALL)
            return lab.next_to(ax.y_axis, LEFT, buff=0.7)  # clear of the tick labels

        labels = VGroup(
            y_label(phase, r"v/v_\mathrm{th}\ [1]"),
            y_label(dens, r"n/n_0\ [1]"),
            y_label(flow, r"u/v_\mathrm{th}\ [1]"),
        )
        x_label = math(r"x/L\ [1]", color=MUTED, size=MATH_SMALL)
        x_label.next_to(flow.c2p(1, 0), RIGHT, buff=0.3)
        tick_labels = VGroup(*[
            math(text, color=MUTED, size=MATH_SMALL).next_to(flow.c2p(x, 0), DOWN, buff=0.15)
            for x, text in [(0, "0"), (0.5, "0.5"), (1, "1")]])
        for ax, values in [(phase, (-2, 0, 2, 4)), (dens, (0, 1, 2)), (flow, (0, 1))]:
            labels.add(*[math(str(y), color=MUTED, size=MATH_SMALL).next_to(ax.c2p(0, y), LEFT, buff=0.12)
                         for y in values])

        x, v = sample_particles()
        visible = (v > -3) & (v < 4)
        dots = VGroup(*[Dot(phase.c2p(xi, vi), radius=0.035, color=ELECTRON)
                        for xi, vi in zip(x[visible], v[visible])])

        nx, nv = 40, 35
        dx, dv = 1 / nx, 7 / nv
        cell_w = phase.c2p(dx, 0)[0] - phase.c2p(0, 0)[0]
        cell_h = phase.c2p(0, dv)[1] - phase.c2p(0, 0)[1]
        peak = distribution(0.0, 0.0) * 1.0
        cells = VGroup()
        for i in range(nx):
            for j in range(nv):
                xc, vc = (i + 0.5) * dx, -3 + (j + 0.5) * dv
                level = min(distribution(xc, vc) / peak, 1.0)
                if level < 0.003:
                    continue
                cells.add(Rectangle(width=1.04 * cell_w, height=1.04 * cell_h, stroke_width=0,
                                    fill_color=ELECTRON, fill_opacity=0.85 * level ** 0.7)
                          .move_to(phase.c2p(xc, vc)))
        f_label = math(r"f(x, v)", color=INK, size=MATH_SIZE).next_to(phase, RIGHT, buff=0.35)

        integrate = Arrow(f_label.get_bottom() + DOWN * 0.1, [f_label.get_center()[0], -1.05, 0],
                          buff=0.1, color=MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=0.08)
        integrate_label = math(r"\int dv", color=MUTED, size=MATH_SMALL).next_to(integrate, RIGHT, buff=0.12)

        n_curve = dens.plot(lambda s: density(s), x_range=[0, 1, 0.005], color=GREEN, stroke_width=4)
        u_curve = flow.plot(lambda s: bulk_velocity(s), x_range=[0, 1, 0.005], color=PURPLE, stroke_width=4)
        centers, n_est, u_est = binned_moments(x, v)
        n_marks = VGroup(*[Square(0.11, color=GREEN, fill_opacity=1, stroke_width=0).move_to(dens.c2p(c, y))
                           for c, y in zip(centers, n_est)])
        u_marks = VGroup(*[Square(0.11, color=PURPLE, fill_opacity=1, stroke_width=0).move_to(flow.c2p(c, y))
                           for c, y in zip(centers, u_est)])

        self.play(Create(phase), Create(dens), Create(flow), FadeIn(labels), FadeIn(x_label),
                  FadeIn(tick_labels), run_time=1.0, rate_func=EASE)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.004), run_time=2.0, rate_func=LINEAR)
        self.wait(0.8)
        self.play(FadeIn(cells), dots.animate.set_opacity(0.15), FadeIn(f_label), run_time=1.6, rate_func=EASE)
        self.play(FadeOut(dots), run_time=0.5, rate_func=EASE)
        self.play(GrowArrow(integrate), FadeIn(integrate_label), run_time=0.7, rate_func=EASE)
        self.play(Create(n_curve), FadeIn(n_marks), run_time=1.6, rate_func=LINEAR)
        self.play(Create(u_curve), FadeIn(u_marks), run_time=1.6, rate_func=LINEAR)
        self.wait(2.0)
