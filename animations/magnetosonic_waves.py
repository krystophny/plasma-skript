"""Schematic warm magnetized-wave comparison.

The scene compares three normalized patterns rather than solving a particular
boundary-value problem: a compressive sound wave, a transverse shear Alfvén
wave, and a compressional magnetosonic wave.  The warm-fluid speed relation

    v_m^2 = v_A^2 + v_s^2

is shown as a model connection, not as dimensional simulation data.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
PRESSURE = "#F2A65A"
FIELD = "#72D6C9"
MAGNETIC = "#4EA8DE"


class MagnetosonicWaves(Scene):
    """Compare pressure, shear-Alfvén, and magnetosonic wave patterns."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Warm magnetized-wave patterns", color=INK, font_size=32)
        subtitle = Text(
            "schematic normalized illustration · coordinates [1] · patterns are not measurements",
            color=MUTED,
            font_size=19,
        )
        heading = VGroup(title, subtitle).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        heading.to_edge(UP, buff=0.25).to_edge(LEFT, buff=0.38)

        formula = MathTex(
            r"v_m^2 = v_A^2 + v_s^2",
            color=FIELD,
            font_size=30,
        )
        formula.to_corner(UR, buff=0.38)

        tracker = ValueTracker(0.0)
        x_values = np.linspace(-5.0, 5.0, 260)
        row_y = [1.75, 0.0, -1.75]
        row_titles = [
            ("sound", PRESSURE),
            ("shear Alfvén", FIELD),
            ("magnetosonic", MAGNETIC),
        ]

        separators = VGroup(
            *[
                Line(
                    np.array([-5.45, y - 0.78, 0.0]),
                    np.array([5.45, y - 0.78, 0.0]),
                    color=GRID,
                    stroke_width=1,
                    stroke_opacity=0.55,
                )
                for y in [1.0, -0.75]
            ]
        )

        labels = VGroup()
        for (label, color), y in zip(row_titles, row_y):
            label_text = Text(label, color=color, font_size=22)
            label_text.to_edge(LEFT, buff=0.4).move_to(
                np.array([label_text.get_center()[0], y + 0.56, 0.0])
            )
            labels.add(label_text)

        def graph(points, color, width=3):
            return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
                points
            )

        def sound_points(time):
            y0 = row_y[0]
            return [
                np.array([x, y0 + 0.42 * np.cos(1.25 * x - 0.72 * time), 0.0])
                for x in x_values
            ]

        def magnetic_points(time):
            y0 = row_y[2]
            return [
                np.array([x, y0 + 0.50 * np.cos(0.86 * x - 0.43 * time), 0.0])
                for x in x_values
            ]

        sound_wave = always_redraw(
            lambda: graph(sound_points(tracker.get_value()), PRESSURE)
        )
        sound_reference = DashedLine(
            np.array([-5.0, row_y[0], 0.0]),
            np.array([5.0, row_y[0], 0.0]),
            color=GRID,
            dash_length=0.12,
            stroke_width=2,
        )
        magnetic_wave = always_redraw(
            lambda: graph(magnetic_points(tracker.get_value()), MAGNETIC)
        )
        magnetic_reference = DashedLine(
            np.array([-5.0, row_y[2], 0.0]),
            np.array([5.0, row_y[2], 0.0]),
            color=GRID,
            dash_length=0.12,
            stroke_width=2,
        )

        field_lines = VGroup()
        for base_x in np.linspace(-4.6, 4.6, 8):
            def line_points(time, x0=base_x):
                ys = np.linspace(-0.52, 0.52, 90)
                xs = x0 + 0.48 * np.sin(2.6 * ys + 0.55 * x0 - 0.58 * time)
                return [
                    np.array([x, row_y[1] + y, 0.0])
                    for x, y in zip(xs, ys)
                ]

            field_lines.add(
                always_redraw(
                    lambda time_tracker=tracker, fn=line_points: graph(
                        fn(time_tracker.get_value()), FIELD, width=2.5
                    )
                )
            )

        k_arrows = VGroup()
        for y in row_y:
            arrow = Arrow(
                np.array([-4.8, y - 0.52, 0.0]),
                np.array([-4.0, y - 0.52, 0.0]),
                color=GRID,
                stroke_width=2,
                buff=0,
            )
            arrow_label = Text("k", color=MUTED, font_size=17)
            arrow_label.next_to(arrow, DOWN, buff=0.04)
            k_arrows.add(VGroup(arrow, arrow_label))

        notes = VGroup(
            Text("pressure / density compression", color=MUTED, font_size=17),
            Text("field-line displacement; nearly incompressible", color=MUTED, font_size=17),
            Text("pressure and magnetic compression add", color=MUTED, font_size=17),
        )
        for note, y in zip(notes, row_y):
            note.to_edge(RIGHT, buff=0.4).move_to(
                np.array([note.get_center()[0], y - 0.58, 0.0])
            )

        observation = Text(
            "finite temperature supplies pressure restoring force",
            color=INK,
            font_size=20,
        )
        observation.to_edge(DOWN, buff=0.25)

        self.play(FadeIn(heading), FadeIn(formula), Create(separators), FadeIn(labels))
        self.play(
            Create(sound_reference),
            Create(sound_wave),
            Create(magnetic_reference),
            Create(magnetic_wave),
            Create(field_lines),
            FadeIn(k_arrows),
            FadeIn(notes),
            FadeIn(observation),
        )
        self.play(tracker.animate.set_value(2 * PI), run_time=8, rate_func=linear)
        self.wait(1)
