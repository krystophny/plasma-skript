"""Illustrative circular-mode decomposition in a cold magnetized plasma.

The scene is a normalized visualization of two circular eigenmodes acquiring
different phase advances. Their superposition is a linearly polarized field
whose polarization plane rotates along the propagation direction, with

    theta_F = (k_+ - k_-) L / 2.

Normalization: z/L0, tau = t/t0, E/E0 with k_+ L0 = 1.2, k_- L0 = 0.8,
omega t0 = 1 and component amplitude 1/2 (all unit [1]). The view looks
along +z (propagation out of the page): at fixed z the + mode rotates
clockwise and the - mode counterclockwise in time, and the polarization axis
turns counterclockwise by 0.2 rad per unit z/L0. It is a conceptual
illustration of Faraday rotation, not a ray-tracing model or a measurement of
a particular plasma.
"""

from manim import *
import numpy as np

from style import (
    CURVE_WIDTH, E_FIELD, EASE, FAINT, GREEN, GRID, INK, LINEAR, MUTED, BLUE,
    THIN_WIDTH, StyledScene, label, math,
)


def circular_modes(z, tau, k_plus=1.2, k_minus=0.8, omega=1.0):
    """Return real transverse E+/E0, E-/E0, and their sum (each mode amplitude 1/2).

    z means z/L0, tau=t/t0; k values are k L0 and omega is omega t0.
    E+=(cos p+,sin p+)/2, E-=(cos p-,-sin p-)/2, p±=k±z-omega tau.
    Sum=cos(kmean z-omega tau)*(cos theta,sin theta), theta=(k+-k-)z/2.
    """
    plus_phase, minus_phase = k_plus*z - omega*tau, k_minus*z - omega*tau
    plus = 0.5 * np.array([np.cos(plus_phase), np.sin(plus_phase)])
    minus = 0.5 * np.array([np.cos(minus_phase), -np.sin(minus_phase)])
    return plus, minus, plus + minus


Z_PANEL = 3.0
Z_SAMPLES = (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)


def _tip_vector(start, end, color, tip):
    """Thin vector with a circle or square tip marker (shape encodes the mode)."""
    marker = Dot(end, radius=0.085, color=color) if tip == "circle" else \
        Square(side_length=0.16, color=color, fill_opacity=1, stroke_width=0).move_to(end)
    return VGroup(Line(start, end, color=color, stroke_width=THIN_WIDTH + 0.6), marker)


class MagnetizedPolarization(StyledScene):
    """Show circular eigenmodes and their accumulated polarization rotation."""

    def build(self):
        tracker = ValueTracker(0.0)

        # --- left: transverse plane at one fixed position ---------------
        center = np.array([-4.2, 0.1, 0.0])
        radius = 1.75  # screen length of |E|/E0 = 1
        frame = Circle(radius=radius, color=GRID, stroke_width=THIN_WIDTH - 0.8).move_to(center)
        half = DashedVMobject(Circle(radius=radius / 2, color=FAINT, stroke_width=1.4)
                              .move_to(center), num_dashes=36)
        cross = VGroup(
            Line(center + LEFT * (radius + 0.2), center + RIGHT * (radius + 0.2), color=GRID, stroke_width=1.4),
            Line(center + DOWN * (radius + 0.2), center + UP * (radius + 0.2), color=GRID, stroke_width=1.4),
        )
        ex_lab = math(r"E_x/E_0\ [1]", color=MUTED, size=28).next_to(cross[0], RIGHT, buff=0.1)
        ey_lab = math(r"E_y/E_0\ [1]", color=MUTED, size=28).next_to(cross[1].get_top(), RIGHT, buff=0.15)
        theta_p = (1.2 - 0.8) * Z_PANEL / 2
        axis_dir = np.array([np.cos(theta_p), np.sin(theta_p), 0.0])
        panel_axis = DashedLine(center - axis_dir * radius, center + axis_dir * radius,
                                color=MUTED, stroke_width=1.6, dash_length=0.1)

        def to_screen(vec, c, r):
            return c + r * np.array([vec[0], vec[1], 0.0])

        def panel_vectors():
            plus, minus, total = circular_modes(Z_PANEL, tracker.get_value())
            return VGroup(
                _tip_vector(center, to_screen(plus, center, radius), GREEN, "circle"),
                _tip_vector(center, to_screen(minus, center, radius), BLUE, "square"),
                Line(center, to_screen(total, center, radius), color=E_FIELD,
                     stroke_width=CURVE_WIDTH + 1),
            )

        vectors = always_redraw(panel_vectors)

        key = VGroup(
            VGroup(_tip_vector(ORIGIN, RIGHT * 0.45, GREEN, "circle"), math(r"E_+", color=GREEN, size=30)).arrange(RIGHT, buff=0.15),
            VGroup(_tip_vector(ORIGIN, RIGHT * 0.45, BLUE, "square"), math(r"E_-", color=BLUE, size=30)).arrange(RIGHT, buff=0.15),
            VGroup(Line(ORIGIN, RIGHT * 0.45, color=E_FIELD, stroke_width=CURVE_WIDTH + 1), math(r"E", color=E_FIELD, size=30)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.5).next_to(frame, DOWN, buff=0.45)

        # --- right: the summed field at a row of positions --------------
        small = 0.42
        xs = np.linspace(-0.2, 6.05, len(Z_SAMPLES))
        row_y = 0.1
        row_centers = [np.array([x, row_y, 0.0]) for x in xs]
        rings, axes_lines, ticks = VGroup(), VGroup(), VGroup()
        for z, c in zip(Z_SAMPLES, row_centers):
            is_panel = abs(z - Z_PANEL) < 1e-9
            rings.add(Circle(radius=small, color=INK if is_panel else GRID,
                             stroke_width=2.2 if is_panel else 1.4).move_to(c))
            th = (1.2 - 0.8) * z / 2
            d = np.array([np.cos(th), np.sin(th), 0.0])
            axes_lines.add(DashedLine(c - d * small, c + d * small, color=MUTED,
                                      stroke_width=1.3, dash_length=0.06))
            ticks.add(math(f"{int(z)}", color=MUTED, size=28).next_to(c, DOWN, buff=small + 0.18))

        def row_vectors():
            group = VGroup()
            for z, c in zip(Z_SAMPLES, row_centers):
                total = circular_modes(z, tracker.get_value())[2]
                group.add(Line(c, to_screen(total, c, small), color=E_FIELD, stroke_width=CURVE_WIDTH))
            return group

        row = always_redraw(row_vectors)
        z_arrow = Arrow(np.array([xs[0] - 0.3, row_y - 1.45, 0]), np.array([xs[-1] + 0.45, row_y - 1.45, 0]),
                        buff=0, color=MUTED, stroke_width=2, max_tip_length_to_length_ratio=0.03)
        z_axis_lab = math(r"z/L_0\ [1]", color=MUTED, size=30).next_to(z_arrow, DOWN, buff=0.15).align_to(z_arrow, RIGHT)

        self.play(Create(frame), FadeIn(cross), FadeIn(half), FadeIn(ex_lab), FadeIn(ey_lab),
                  FadeIn(rings), FadeIn(ticks), GrowArrow(z_arrow), FadeIn(z_axis_lab),
                  run_time=0.9, rate_func=EASE)
        self.play(FadeIn(vectors), FadeIn(key), FadeIn(row), FadeIn(panel_axis), FadeIn(axes_lines),
                  run_time=0.5, rate_func=EASE)
        self.play(tracker.animate.set_value(4 * PI), run_time=8.0, rate_func=LINEAR)
        self.wait(1.2)
