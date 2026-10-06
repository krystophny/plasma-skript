"""Illustrative E x B drift animation.

The plotted quantity is the particle position in normalized coordinates. The
analytic path is

    X = x/L0 = -2.35 + 0.55 tau + 0.65 cos(2 tau)
    Y = y/L0 = -0.65 - 0.65 sin(2 tau),  0 <= tau=t/t0 <= 8.

Here Omega*t0=2, E/B=0.55 L0/t0 (SI), rho=0.65 L0, q>0,
E along +y and B along +z. Thus X''=2Y', Y''=1.1-2X'.

The circular part represents gyromotion and the linear part represents the
guiding-center drift. It is a conceptual visualization, not measured data.
"""

from manim import *
import numpy as np

from style import (
    BG, B_FIELD, CURVE_WIDTH, DOT_RADIUS, E_FIELD, EASE, FAINT, INK, ION, LINEAR,
    MUTED, SMALL_SIZE, THIN_WIDTH, StyledScene, axes, axis_labels, label, math,
    MATH_SIZE,
)


def particle_position(tau):
    """Exact Lorentz orbit in units L0, with tau=t/t0."""
    return np.array([-2.35 + 0.55 * tau + 0.65 * np.cos(2 * tau),
                     -0.65 - 0.65 * np.sin(2 * tau)])


class ExBDrift(StyledScene):
    """Show clockwise ion gyromotion and the rightward E x B drift."""

    def build(self):
        ax = axes([-3.5, 3.5, 1], [-2.0, 1.5, 1], 10.2, 5.1).move_to(DOWN * 0.2)
        ax_labels = axis_labels(ax, r"x/L_0\ [1]", r"y/L_0\ [1]")

        # Uniform B out of the page: a quiet lattice of dot-in-circle symbols.
        b_marks = VGroup()
        for x in np.arange(-2.5, 3.01, 1.0):
            for y in (-1.9, 1.0):
                mark = VGroup(
                    Circle(radius=0.09, color=B_FIELD, stroke_width=1.6),
                    Dot(radius=0.025, color=B_FIELD),
                ).move_to(ax.c2p(x, y))
                b_marks.add(mark)
        b_marks.set_opacity(0.55)
        b_label = math(r"\mathbf{B}\ \odot", color=B_FIELD, size=MATH_SIZE)
        b_label.next_to(ax.c2p(2.5, 1.0), UP, buff=0.18)

        # Uniform E along +y.
        e_arrows = VGroup(*[
            Arrow(ax.c2p(-3.2, y0), ax.c2p(-3.2, y0 + 0.75), buff=0,
                  color=E_FIELD, stroke_width=3, max_tip_length_to_length_ratio=0.22)
            for y0 in (-1.75, -0.85)
        ])
        e_label = math(r"\mathbf{E}", color=E_FIELD, size=MATH_SIZE)
        e_label.next_to(e_arrows, LEFT, buff=0.15)

        tracker = ValueTracker(0)

        def center_point():
            tau = tracker.get_value()
            return ax.c2p(-2.35 + 0.55 * tau, -0.65)

        def particle_point():
            x, y = particle_position(tracker.get_value())
            return ax.c2p(x, y)

        def orbit_curve():
            tau = max(tracker.get_value(), 1e-3)
            return ParametricFunction(
                lambda s: ax.c2p(*particle_position(s)), t_range=[0, tau, 0.02],
                color=ION, stroke_width=CURVE_WIDTH - 1)

        center_track = DashedLine(ax.c2p(-2.35, -0.65), ax.c2p(2.05, -0.65),
                                  color=FAINT, stroke_width=THIN_WIDTH, dash_length=0.1)
        orbit = always_redraw(orbit_curve)
        radius_line = always_redraw(lambda: Line(
            center_point(), particle_point(), color=MUTED, stroke_width=1.6))
        particle = always_redraw(lambda: VGroup(
            Dot(particle_point(), radius=0.14, color=ION),
            math("+", color=BG, size=30).move_to(particle_point()),
        ))
        guiding_center = always_redraw(lambda: Dot(center_point(), radius=DOT_RADIUS, color=INK))

        drift_arrow = Arrow(ax.c2p(-1.0, 0.35), ax.c2p(1.0, 0.35), buff=0,
                            color=INK, stroke_width=3, max_tip_length_to_length_ratio=0.12)
        drift_label = math(r"\mathbf{v}_E", color=INK, size=MATH_SIZE)
        drift_label.next_to(drift_arrow, UP, buff=0.15)

        self.play(Create(ax), FadeIn(ax_labels), run_time=0.8, rate_func=EASE)
        self.play(LaggedStart(FadeIn(b_marks), FadeIn(b_label), GrowFromEdge(e_arrows, DOWN),
                              FadeIn(e_label), GrowArrow(drift_arrow), FadeIn(drift_label),
                              lag_ratio=0.15), run_time=0.9, rate_func=EASE)
        self.play(FadeIn(center_track), FadeIn(guiding_center), FadeIn(radius_line),
                  FadeIn(particle), run_time=0.4, rate_func=EASE)
        self.add(orbit)
        self.play(tracker.animate.set_value(8), run_time=7.5, rate_func=LINEAR)
        self.wait(1.5)
