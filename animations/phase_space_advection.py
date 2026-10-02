"""Illustrative free streaming in one-dimensional phase space.

The scene uses the normalized variables

    xi = x / L_0, eta = v / v_0, tau = t v_0 / L_0.

Each sample follows the collisionless characteristic

    xi(tau) = xi_0 + eta tau, eta(tau) = eta_0.

The samples are a deterministic illustration of a distribution, not a
particle-in-cell calculation and not measured data.  The solid contour is the
exact image of the initial elliptical support under the same shear map.
"""

from manim import *
import numpy as np

from style import (
    CURVE_WIDTH, EASE, ELECTRON, FAINT, INK, LINEAR, MUTED, THIN_WIDTH,
    StyledScene, axes, axis_labels, math,
)


def streamed_position(xi0, eta0, tau):
    """Free-streaming characteristic xi(tau) = xi0 + eta0 tau."""
    return xi0 + eta0 * tau


class PhaseSpaceAdvection(StyledScene):
    """Show a phase-space cloud shearing under collisionless free streaming."""

    def build(self):
        ax = axes([-4.5, 3.5, 1.0], [0.0, 1.0, 0.2], 12.0, 4.7).move_to(DOWN * 0.1)
        ax_labels = axis_labels(ax, r"\xi = x/L_0\ [1]", r"\eta = v/v_0\ [1]")

        # A fixed random seed makes the visual reproducible across builds.
        rng = np.random.default_rng(12)
        samples = rng.normal(loc=(0.0, 0.0), scale=(0.38, 0.12), size=(42, 2))
        x0_values = -2.3 + samples[:, 0]
        v0_values = 0.45 + samples[:, 1]
        tracker = ValueTracker(0.0)

        def sample_point(x0, v0):
            return ax.c2p(streamed_position(x0, v0, tracker.get_value()), v0)

        dots = VGroup()
        for x0, v0 in zip(x0_values, v0_values):
            dot = Dot(ax.c2p(x0, v0), radius=0.06, color=ELECTRON)
            dot.add_updater(lambda mob, x0=x0, v0=v0: mob.move_to(sample_point(x0, v0)))
            dots.add(dot)

        # Initial support (ghost) and its exact sheared image.
        def support(tau):
            return ParametricFunction(
                lambda s: ax.c2p(
                    streamed_position(-2.3 + 0.9 * np.cos(s), 0.45 + 0.31 * np.sin(s), tau),
                    0.45 + 0.31 * np.sin(s)),
                t_range=[0, TAU, TAU / 120], color=INK, stroke_width=THIN_WIDTH)

        ghost = DashedVMobject(support(0.0), num_dashes=36).set_stroke(FAINT, THIN_WIDTH)
        contour = always_redraw(lambda: support(tracker.get_value()))

        # Straight characteristics of three selected samples.
        chosen = [int(np.argmin(v0_values)), int(np.argsort(v0_values)[21]), int(np.argmax(v0_values))]

        def characteristic(i):
            return Line(ax.c2p(x0_values[i], v0_values[i]),
                        sample_point(x0_values[i], v0_values[i]),
                        color=MUTED, stroke_width=1.8)

        traces = VGroup(*[always_redraw(lambda i=i: characteristic(i)) for i in chosen])

        # Characteristic speed key: horizontal arrows of length proportional to eta.
        flow_arrows = VGroup(*[
            Arrow(ax.c2p(-4.35, v), ax.c2p(-4.35 + 1.5 * v, v), buff=0, color=FAINT,
                  stroke_width=3, max_tip_length_to_length_ratio=0.3)
            for v in (0.25, 0.45, 0.65)
        ])

        self.play(Create(ax), FadeIn(ax_labels),
                  run_time=0.8, rate_func=EASE)
        self.play(LaggedStart(FadeIn(ghost), FadeIn(dots), FadeIn(flow_arrows), lag_ratio=0.2),
                  run_time=0.8, rate_func=EASE)
        self.add(traces, contour)
        self.bring_to_front(dots)
        self.play(tracker.animate.set_value(6.0), run_time=8, rate_func=LINEAR)
        self.wait(1.4)
