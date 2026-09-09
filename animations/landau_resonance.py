"""Schematic visualization of resonant particle--wave energy exchange.

The scene is a normalized teaching illustration.  A particle close to the
phase velocity rides the wave while the velocity distribution supplies the
sign of the net energy exchange: a negative slope produces Landau damping.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
WAVE = "#72D6C9"
RESONANT = "#F2A65A"
SLOPE = "#4EA8DE"


class LandauResonance(Scene):
    """Show a resonant particle and the slope of an equilibrium distribution."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Landau resonance", color=INK, font_size=34)
        subtitle = Text(
            "normalized phase-space and velocity-space illustration",
            color=MUTED,
            font_size=20,
        )
        heading = VGroup(title, subtitle).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08
        )
        heading.to_edge(UP, buff=0.28).to_edge(LEFT, buff=0.38)

        resonance_formula = MathTex(
            r"\omega-kv_\phi=0",
            color=RESONANT,
            font_size=29,
        )
        resonance_formula.to_corner(UR, buff=0.38)

        phase_axes = Axes(
            x_range=[-4.4, 4.4, 2],
            y_range=[-1.5, 1.5, 1],
            x_length=6.2,
            y_length=3.65,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(LEFT * 2.15 + DOWN * 0.35)
        phase_x = Text("position / L₀ [1]", color=MUTED, font_size=18)
        phase_x.next_to(phase_axes, DOWN, buff=0.14)
        phase_y = Text("velocity / v₀ [1]", color=MUTED, font_size=18)
        phase_y.rotate(PI / 2)
        phase_y.next_to(phase_axes, LEFT, buff=0.12)
        phase_label = Text("wave and resonant particle", color=WAVE, font_size=19)
        phase_label.next_to(phase_axes, UP, buff=0.12)

        phase = ValueTracker(-3.4)
        wave = phase_axes.plot(
            lambda x: 0.42 * np.sin(0.95 * x),
            x_range=[-4.4, 4.4],
            color=WAVE,
            stroke_width=3,
        )
        phase_line = DashedLine(
            phase_axes.c2p(-4.0, 0.0),
            phase_axes.c2p(4.0, 0.0),
            color=GRID,
            dash_length=0.12,
            stroke_width=1.5,
        )
        resonant_particle = always_redraw(
            lambda: Dot(
                phase_axes.c2p(
                    phase.get_value(),
                    0.42 * np.sin(0.95 * phase.get_value()),
                ),
                radius=0.10,
                color=RESONANT,
            )
        )
        velocity_arrow = Arrow(
            phase_axes.c2p(-2.9, -1.05),
            phase_axes.c2p(-1.8, -1.05),
            color=RESONANT,
            stroke_width=3,
            buff=0,
        )
        velocity_label = Text("vφ", color=RESONANT, font_size=19)
        velocity_label.next_to(velocity_arrow, DOWN, buff=0.04)

        distribution_axes = Axes(
            x_range=[-2.8, 2.8, 1],
            y_range=[0, 1.15, 0.5],
            x_length=4.55,
            y_length=3.65,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(RIGHT * 3.15 + DOWN * 0.35)
        distribution_x = Text("v / v₀ [1]", color=MUTED, font_size=18)
        distribution_x.next_to(distribution_axes, DOWN, buff=0.14)
        distribution_y = Text("f₀(v) [1]", color=MUTED, font_size=18)
        distribution_y.rotate(PI / 2)
        distribution_y.next_to(distribution_axes, LEFT, buff=0.10)
        distribution_label = Text(
            "negative slope → damping", color=SLOPE, font_size=19
        )
        distribution_label.next_to(distribution_axes, UP, buff=0.12)

        distribution = distribution_axes.plot(
            lambda x: np.exp(-0.72 * x * x),
            x_range=[-2.8, 2.8],
            color=SLOPE,
            stroke_width=3,
        )
        v_phi = 0.92
        resonance_line = DashedLine(
            distribution_axes.c2p(v_phi, 0),
            distribution_axes.c2p(v_phi, 0.82),
            color=RESONANT,
            dash_length=0.12,
            stroke_width=2.5,
        )
        v_phi_label = MathTex(r"v_\phi", color=RESONANT, font_size=25)
        v_phi_label.next_to(resonance_line, RIGHT, buff=0.08)
        slope_arrow = Arrow(
            distribution_axes.c2p(v_phi + 0.52, 0.40),
            distribution_axes.c2p(v_phi - 0.16, 0.63),
            color=SLOPE,
            stroke_width=3,
            buff=0,
        )
        slope_label = MathTex(
            r"\frac{\partial f_0}{\partial v}<0",
            color=SLOPE,
            font_size=25,
        )
        slope_label.next_to(slope_arrow, RIGHT, buff=0.04)

        lower_notes = VGroup(
            Text("slower particles gain energy", color=RESONANT, font_size=20),
            Text("faster particles lose energy", color=SLOPE, font_size=20),
        ).arrange(RIGHT, buff=0.8)
        lower_notes.to_edge(DOWN, buff=0.36)

        self.play(FadeIn(heading), FadeIn(resonance_formula))
        self.play(
            Create(phase_axes),
            Create(phase_line),
            Create(wave),
            FadeIn(VGroup(phase_x, phase_y, phase_label)),
            Create(distribution_axes),
            Create(distribution),
            FadeIn(VGroup(distribution_x, distribution_y, distribution_label)),
        )
        self.play(
            Create(velocity_arrow),
            FadeIn(velocity_label),
            Create(resonance_line),
            FadeIn(v_phi_label),
            Create(slope_arrow),
            FadeIn(slope_label),
            FadeIn(lower_notes),
            FadeIn(resonant_particle),
        )
        self.play(
            phase.animate.set_value(3.4),
            run_time=4.0,
            rate_func=linear,
        )
        self.play(
            phase.animate.set_value(-1.2),
            run_time=2.5,
            rate_func=linear,
        )
        self.wait(1.5)
