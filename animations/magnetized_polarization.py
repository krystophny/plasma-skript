"""Illustrative circular-mode decomposition in a cold magnetized plasma.

The scene is a normalized visualization of two circular eigenmodes acquiring
different phase advances. Their superposition is a linearly polarized field
whose polarization plane rotates along the propagation direction, with

    theta_F = (k_+ - k_-) L / 2.

It is a conceptual illustration of Faraday rotation, not a ray-tracing model
or a measurement of a particular plasma.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
PLUS_COLOR = "#72D6C9"
MINUS_COLOR = "#F2A65A"
FIELD_COLOR = "#4EA8DE"


class MagnetizedPolarization(Scene):
    """Show circular eigenmodes and their accumulated polarization rotation."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Circular modes and Faraday rotation", color=INK, font_size=31)
        subtitle = Text(
            "cold magnetized plasma · normalized illustration",
            color=MUTED,
            font_size=21,
        )
        title_group = VGroup(title, subtitle).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08
        )
        title_group.to_edge(UP, buff=0.28).to_edge(LEFT, buff=0.38)

        formula = MathTex(
            r"\theta_F = (k_+ - k_-)L/2",
            color=PLUS_COLOR,
            font_size=28,
        )
        formula.to_corner(UR, buff=0.38)

        tracker = ValueTracker(0.0)

        phasor_center = np.array([-3.9, -0.45, 0.0])
        phasor_circle = Circle(
            radius=1.28,
            color=GRID,
            stroke_width=2,
        ).move_to(phasor_center)
        phasor_x = Line(
            phasor_center + LEFT * 1.45,
            phasor_center + RIGHT * 1.45,
            color=GRID,
            stroke_width=2,
        )
        phasor_y = Line(
            phasor_center + DOWN * 1.45,
            phasor_center + UP * 1.45,
            color=GRID,
            stroke_width=2,
        )
        phasor_label = Text("transverse phasor plane", color=MUTED, font_size=20)
        phasor_label.next_to(phasor_circle, UP, buff=0.12)
        x_label = Text("x [1]", color=MUTED, font_size=18)
        x_label.next_to(phasor_x, RIGHT, buff=0.08)
        y_label = Text("y [1]", color=MUTED, font_size=18)
        y_label.next_to(phasor_y, UP, buff=0.08)

        def endpoint(angle, length=1.1):
            return phasor_center + length * np.array(
                [np.cos(angle), np.sin(angle), 0.0]
            )

        plus_arrow = always_redraw(
            lambda: Arrow(
                phasor_center,
                endpoint(0.92 * tracker.get_value()),
                color=PLUS_COLOR,
                stroke_width=5,
                buff=0,
                max_tip_length_to_length_ratio=0.22,
            )
        )
        minus_arrow = always_redraw(
            lambda: Arrow(
                phasor_center,
                endpoint(-0.61 * tracker.get_value()),
                color=MINUS_COLOR,
                stroke_width=5,
                buff=0,
                max_tip_length_to_length_ratio=0.22,
            )
        )
        plus_label = Text("+ circular mode", color=PLUS_COLOR, font_size=18)
        plus_label.move_to([-5.05, -2.35, 0.0])
        minus_label = Text("− circular mode", color=MINUS_COLOR, font_size=18)
        minus_label.move_to([-2.65, -2.35, 0.0])

        propagation_label = Text(
            "different phase advances along z",
            color=MUTED,
            font_size=19,
        )
        propagation_label.move_to([1.8, 1.35, 0])

        z_positions = np.linspace(-0.1, 5.7, 7)
        section_centers = [np.array([z, -0.48, 0.0]) for z in z_positions]
        section_circles = VGroup(
            *[
                Circle(radius=0.42, color=GRID, stroke_width=2).move_to(center)
                for center in section_centers
            ]
        )
        section_vectors = VGroup()
        for index, center in enumerate(section_centers):
            phase_offset = 0.20 * index

            def section_arrow(mob_center=center, offset=phase_offset):
                angle = 0.18 * tracker.get_value() + offset
                return Arrow(
                    mob_center,
                    mob_center
                    + 0.34 * np.array([np.cos(angle), np.sin(angle), 0.0]),
                    color=FIELD_COLOR,
                    stroke_width=4,
                    buff=0,
                    max_tip_length_to_length_ratio=0.3,
                )

            section_vectors.add(always_redraw(section_arrow))

        z_axis = Arrow(
            np.array([-0.35, -1.45, 0.0]),
            np.array([5.95, -1.45, 0.0]),
            color=GRID,
            stroke_width=2,
            buff=0,
        )
        z_label = Text("propagation z [1]", color=MUTED, font_size=19)
        z_label.next_to(z_axis, DOWN, buff=0.12)
        input_label = Text("linear input", color=FIELD_COLOR, font_size=17)
        input_label.next_to(section_circles[0], LEFT, buff=0.12)
        output_label = Text("rotated output", color=FIELD_COLOR, font_size=17)
        output_label.next_to(section_circles[-1], UP, buff=0.12)

        observation = Text(
            "superposition rotates the polarization plane",
            color=INK,
            font_size=21,
        )
        observation.to_edge(DOWN, buff=0.28)

        self.play(
            FadeIn(title_group),
            FadeIn(formula),
            Create(VGroup(phasor_circle, phasor_x, phasor_y)),
            FadeIn(VGroup(phasor_label, x_label, y_label)),
        )
        self.play(
            GrowArrow(plus_arrow),
            GrowArrow(minus_arrow),
            FadeIn(plus_label),
            FadeIn(minus_label),
            FadeIn(propagation_label),
            Create(section_circles),
            Create(z_axis),
            FadeIn(VGroup(z_label, input_label, output_label)),
            FadeIn(observation),
        )
        self.add(plus_arrow, minus_arrow, section_vectors)
        self.play(tracker.animate.set_value(2 * PI), run_time=8, rate_func=linear)
        self.wait(1)
