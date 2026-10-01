"""Illustrative one-dimensional random walk for plasma diffusion.

The walkers use normalized coordinates

    xi = x / L_0
    tau = t / tau_0

and take symmetric steps of magnitude 0.34 per unit tau, so the ensemble
variance grows as <xi^2> = 2 D_* tau with D_* = 0.34^2 / 2 = 0.0578.  The
space-time diagram shows every walker path, three highlighted paths, the
finite-sample mean and the envelope +-sqrt(2 D_* tau).  The scene is a
conceptual visualization of diffusive spreading, not a Monte-Carlo transport
calculation or measured data.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, CURVE_WIDTH, EASE, ELECTRON, FAINT, GREEN, INK, LINEAR, MUTED,
    THIN_WIDTH, StyledScene, axes, axis_labels, math, title,
)


STEP = 0.34
N_WALKERS = 36
N_STEPS = 18


def walker_positions(seed=8):
    """Seeded symmetric walks; row i holds xi_i at tau = 0, 1, ..., N_STEPS."""
    rng = np.random.default_rng(seed)
    steps = rng.choice([-1.0, 1.0], size=(36, 18))
    return np.concatenate([np.zeros((36, 1)), 0.34 * np.cumsum(steps, axis=1)], axis=1)


def diffusion_coefficient(step=0.34, duration=1.0):
    """D_* = step^2 / (2 duration) for a symmetric walk."""
    return step * step / (2 * duration)


class DiffusionRandomWalk(StyledScene):
    """Show symmetric walkers spreading while their mean stays near zero."""

    def build(self):
        heading = title("Random walk and diffusion")

        ax = axes([-3.5, 3.5, 1], [0, 18, 3], 8.6, 5.6).move_to([-1.35, -0.45, 0])
        ax_labels = axis_labels(ax, r"\xi = x/L_0\ [1]", r"\tau = t/\tau_0\ [1]")

        d_star = diffusion_coefficient()
        laws = VGroup(
            math(r"\langle \xi \rangle = 0", color=GREEN, size=34),
            math(r"\langle \xi^2 \rangle = 2D_*\tau", color=ACCENT, size=34),
            math(rf"D_* = {d_star:.4f}\ [1]", color=MUTED, size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        laws.move_to([5.0, 0.6, 0])

        positions = walker_positions()
        tracker = ValueTracker(0.0)

        def xi_at(index, tau):
            k = min(int(np.floor(tau)), N_STEPS - 1)
            frac = min(tau - k, 1.0)
            return positions[index, k] + frac * (positions[index, k + 1] - positions[index, k])

        def path(index, color, width, opacity=1.0):
            tau_now = tracker.get_value()
            knots = [k for k in range(N_STEPS + 1) if k < tau_now]
            points = [ax.c2p(positions[index, k], k) for k in knots]
            points.append(ax.c2p(xi_at(index, tau_now), tau_now))
            if len(points) < 2:
                points.insert(0, ax.c2p(0, 0))
            return VMobject(stroke_color=color, stroke_width=width,
                            stroke_opacity=opacity).set_points_as_corners(points)

        highlighted = (3, 15, 27)
        faint_paths = VGroup(*[
            always_redraw(lambda i=i: path(i, ELECTRON, 1.2, 0.25))
            for i in range(N_WALKERS) if i not in highlighted
        ])
        bold_paths = VGroup(*[
            always_redraw(lambda i=i: path(i, INK, 2.6)) for i in highlighted
        ])
        walkers = always_redraw(lambda: VGroup(*[
            Dot(ax.c2p(xi_at(i, tracker.get_value()), tracker.get_value()),
                radius=0.06, color=ELECTRON)
            for i in range(N_WALKERS)
        ]))

        def mean_curve():
            tau_now = max(tracker.get_value(), 1e-3)
            taus = np.linspace(0, tau_now, 120)
            pts = [ax.c2p(np.mean([xi_at(i, t) for i in range(N_WALKERS)]), t) for t in taus]
            return VMobject(stroke_color=GREEN, stroke_width=CURVE_WIDTH - 1).set_points_as_corners(pts)

        def envelope(sign):
            tau_now = max(tracker.get_value(), 1e-3)
            return DashedVMobject(ParametricFunction(
                lambda t: ax.c2p(sign * np.sqrt(2 * d_star * t), t),
                t_range=[0, tau_now, tau_now / 80], color=ACCENT, stroke_width=THIN_WIDTH),
                num_dashes=max(2, int(4 + 1.6 * tau_now)))

        mean_path = always_redraw(mean_curve)
        envelopes = VGroup(always_redraw(lambda: envelope(1)), always_redraw(lambda: envelope(-1)))

        self.play(FadeIn(heading), Create(ax), FadeIn(ax_labels), run_time=0.8, rate_func=EASE)
        self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.1) for m in laws], lag_ratio=0.25),
                  run_time=0.8, rate_func=EASE)
        self.add(faint_paths, envelopes, bold_paths, mean_path, walkers)
        self.play(tracker.animate.set_value(N_STEPS), run_time=9, rate_func=LINEAR)
        self.wait(1.4)

