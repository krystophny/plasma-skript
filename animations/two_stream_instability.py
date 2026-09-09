"""Schematic visualization of the cold symmetric two-stream instability.

The growth curve uses the normalized cold-beam dispersion relation.  The
phase-space panel is intentionally schematic; it highlights counter-streaming
beams and the growing electrostatic perturbation rather than simulating a
particle-in-cell system.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
BEAM_A = "#4EA8DE"
BEAM_B = "#F2A65A"
GROWTH = "#72D6C9"


class TwoStreamInstability(Scene):
    """Show counter-streaming beams and their unstable wave-number band."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Two-stream instability", color=INK, font_size=34)
        subtitle = Text(
            "cold symmetric beams · normalized dispersion",
            color=MUTED,
            font_size=20,
        )
        heading = VGroup(title, subtitle).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08
        )
        heading.to_edge(UP, buff=0.28).to_edge(LEFT, buff=0.38)

        dispersion_formula = MathTex(
            r"D(\omega,k)=0",
            color=GROWTH,
            font_size=30,
        )
        dispersion_formula.to_corner(UR, buff=0.38)

        phase_axes = Axes(
            x_range=[-4.2, 4.2, 2],
            y_range=[-1.6, 1.6, 1],
            x_length=5.6,
            y_length=3.9,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(LEFT * 2.55 + DOWN * 0.25)
        phase_x = Text("position / L₀ [1]", color=MUTED, font_size=18)
        phase_x.next_to(phase_axes, DOWN, buff=0.14)
        phase_y = Text("velocity / v₀ [1]", color=MUTED, font_size=18)
        phase_y.rotate(PI / 2)
        phase_y.next_to(phase_axes, LEFT, buff=0.10)
        phase_label = Text("counter-streaming beams", color=INK, font_size=20)
        phase_label.next_to(phase_axes, UP, buff=0.12)

        stream_phase = ValueTracker(0.0)
        beam_x = np.linspace(-3.8, 3.8, 11)
        upper_dots = VGroup(
            *[
                Dot(phase_axes.c2p(x, 0.86), radius=0.075, color=BEAM_A)
                for x in beam_x
            ]
        )
        lower_dots = VGroup(
            *[
                Dot(phase_axes.c2p(x, -0.86), radius=0.075, color=BEAM_B)
                for x in beam_x
            ]
        )
        upper_label = Text("+1 [1]", color=BEAM_A, font_size=20)
        upper_label.next_to(phase_axes.c2p(3.0, 0.86), RIGHT, buff=0.08)
        lower_label = Text("−1 [1]", color=BEAM_B, font_size=20)
        lower_label.next_to(phase_axes.c2p(3.0, -0.86), RIGHT, buff=0.08)

        def perturbation_points(amplitude, phase):
            return [
                phase_axes.c2p(
                    x,
                    amplitude * np.sin(1.12 * x - phase),
                )
                for x in np.linspace(-3.8, 3.8, 220)
            ]

        amplitude = ValueTracker(0.10)
        wave = always_redraw(
            lambda: VMobject(
                stroke_color=GROWTH,
                stroke_width=3,
            ).set_points_as_corners(
                perturbation_points(
                    amplitude.get_value(), stream_phase.get_value()
                )
            )
        )
        perturbation_label = Text(
            "electrostatic perturbation", color=GROWTH, font_size=18
        )
        perturbation_label.next_to(phase_axes.c2p(-2.6, 0.0), DOWN, buff=0.12)

        growth_axes = Axes(
            x_range=[0, 1.25, 0.25],
            y_range=[0, 0.42, 0.1],
            x_length=4.45,
            y_length=3.9,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(RIGHT * 3.0 + DOWN * 0.25)
        growth_x = MathTex(
            r"kv_0/\omega_p\ [1]", color=MUTED, font_size=22
        )
        growth_x.next_to(growth_axes, DOWN, buff=0.14)
        growth_y = MathTex(
            r"\gamma/\omega_p\ [1]", color=MUTED, font_size=22
        )
        growth_y.rotate(PI / 2)
        growth_y.next_to(growth_axes, LEFT, buff=0.08)
        growth_label = Text("unstable band", color=GROWTH, font_size=20)
        growth_label.next_to(growth_axes, UP, buff=0.12)

        def growth_rate(x):
            y = x * x
            value = 0.5 * np.sqrt(1.0 + 8.0 * y) - y - 0.5
            return np.sqrt(max(0.0, value))

        curve = growth_axes.plot(
            growth_rate,
            x_range=[0.0, 1.0],
            color=GROWTH,
            stroke_width=4,
        )
        stable_line = DashedLine(
            growth_axes.c2p(1.0, 0.0),
            growth_axes.c2p(1.0, 0.40),
            color=BEAM_B,
            dash_length=0.10,
            stroke_width=2,
        )
        boundary_label = Text("boundary", color=BEAM_B, font_size=17)
        boundary_label.next_to(stable_line, RIGHT, buff=0.06)
        maximum = Dot(
            growth_axes.c2p(np.sqrt(3.0 / 8.0), 1.0 / (2.0 * np.sqrt(2.0))),
            radius=0.09,
            color=BEAM_A,
        )
        maximum_label = MathTex(
            r"\gamma_{\max}=\omega_p/(2\sqrt{2})",
            color=BEAM_A,
            font_size=20,
        )
        maximum_label.next_to(maximum, UP, buff=0.08)

        footer = Text(
            "growth occurs when the lower branch has ω² < 0",
            color=INK,
            font_size=20,
        )
        footer.to_edge(DOWN, buff=0.30)

        self.play(FadeIn(heading), FadeIn(dispersion_formula))
        self.play(
            Create(phase_axes),
            FadeIn(VGroup(phase_x, phase_y, phase_label)),
            FadeIn(upper_dots),
            FadeIn(lower_dots),
            FadeIn(upper_label),
            FadeIn(lower_label),
            Create(wave),
            FadeIn(perturbation_label),
            Create(growth_axes),
            FadeIn(VGroup(growth_x, growth_y, growth_label)),
            Create(curve),
            Create(stable_line),
            FadeIn(boundary_label),
            FadeIn(maximum),
            FadeIn(maximum_label),
            FadeIn(footer),
        )
        self.play(
            amplitude.animate.set_value(0.82),
            stream_phase.animate.set_value(2.5 * PI),
            run_time=7.0,
            rate_func=linear,
        )
        self.wait(1.5)
