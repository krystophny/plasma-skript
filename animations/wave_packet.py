"""Illustrative dispersive plasma-wave packet.

The scene uses normalized coordinates and a deliberately separated carrier and
envelope:

    A(x, t) = exp(-(x - v_g t)^2 / (2 sigma^2)) cos(k (x - v_phi t))

The carrier phase speed and envelope group speed are dimensionless visual
parameters. This is a deterministic teaching illustration, not a numerical
solution of a plasma boundary-value problem or measured data.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
WAVE_COLOR = "#72D6C9"
ENVELOPE_COLOR = "#F2A65A"
GROUP_COLOR = "#4EA8DE"
PHASE_COLOR = "#D47BFF"


class WavePacketPropagation(Scene):
    """Show a carrier moving faster than its visible wave-packet envelope."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Phase and group velocity", color=INK, font_size=34)
        subtitle = Text(
            "normalized dispersive wave packet",
            color=MUTED,
            font_size=22,
        )
        title_group = VGroup(title, subtitle).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08
        )
        title_group.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.4)

        formula = MathTex(
            r"A = e^{-(x-v_g t)^2/(2\sigma^2)}"
            r"\cos\!\left(k(x-v_\phi t)\right)",
            color=WAVE_COLOR,
            font_size=25,
        )
        formula.to_corner(UR, buff=0.35)

        axes = Axes(
            x_range=[-6.0, 6.0, 2.0],
            y_range=[-1.35, 1.35, 0.5],
            x_length=10.4,
            y_length=4.7,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.35)

        x_label = Text("x / L₀ (dimensionless)", color=MUTED, font_size=19)
        x_label.next_to(axes, DOWN, buff=0.18)
        y_label = Text("field amplitude", color=MUTED, font_size=19)
        y_label.rotate(PI / 2)
        y_label.to_edge(LEFT, buff=0.3).shift(UP * 0.6)

        tracker = ValueTracker(0.0)
        sigma = 1.15
        wave_number = 5.2
        group_speed = 0.42
        phase_speed = 0.90

        def envelope(x, time):
            return np.exp(-((x - group_speed * time) ** 2) / (2 * sigma**2))

        def wave_points(time):
            xs = np.linspace(-6.0, 6.0, 360)
            ys = envelope(xs, time) * np.cos(
                wave_number * (xs - phase_speed * time)
            )
            return [axes.c2p(x, y) for x, y in zip(xs, ys)]

        wave = always_redraw(
            lambda: VMobject(
                stroke_color=WAVE_COLOR,
                stroke_width=3,
            ).set_points_as_corners(wave_points(tracker.get_value()))
        )

        envelope_upper = always_redraw(
            lambda: VMobject(
                stroke_color=ENVELOPE_COLOR,
                stroke_width=2,
                stroke_opacity=0.95,
            ).set_points_as_corners(
                [
                    axes.c2p(
                        x,
                        envelope(x, tracker.get_value()),
                    )
                    for x in np.linspace(-6.0, 6.0, 180)
                ]
            )
        )
        envelope_lower = always_redraw(
            lambda: VMobject(
                stroke_color=ENVELOPE_COLOR,
                stroke_width=2,
                stroke_opacity=0.95,
            ).set_points_as_corners(
                [
                    axes.c2p(
                        x,
                        -envelope(x, tracker.get_value()),
                    )
                    for x in np.linspace(-6.0, 6.0, 180)
                ]
            )
        )

        group_marker = always_redraw(
            lambda: DashedLine(
                axes.c2p(group_speed * tracker.get_value(), -1.15),
                axes.c2p(group_speed * tracker.get_value(), 1.15),
                color=GROUP_COLOR,
                dash_length=0.12,
                stroke_width=3,
            )
        )
        phase_marker = always_redraw(
            lambda: DashedLine(
                axes.c2p(phase_speed * tracker.get_value(), -1.15),
                axes.c2p(phase_speed * tracker.get_value(), 1.15),
                color=PHASE_COLOR,
                dash_length=0.12,
                stroke_width=3,
            )
        )

        group_label = Text("envelope: v_g", color=GROUP_COLOR, font_size=20)
        group_label.to_edge(LEFT, buff=0.42).shift(DOWN * 1.05)
        phase_label = Text("crest: v_phi", color=PHASE_COLOR, font_size=20)
        phase_label.to_edge(RIGHT, buff=0.42).shift(DOWN * 1.05)

        legend = VGroup(
            Text("teal: carrier field", color=WAVE_COLOR, font_size=18),
            Text("orange: envelope", color=ENVELOPE_COLOR, font_size=18),
            Text("markers: normalized speeds", color=MUTED, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        legend.to_corner(DL, buff=0.3)

        observation = Text(
            "the crest outruns the envelope in this dispersive illustration",
            color=INK,
            font_size=19,
        )
        observation.to_edge(DOWN, buff=0.30).to_edge(RIGHT, buff=0.35)

        self.play(
            FadeIn(title_group),
            FadeIn(formula),
            Create(axes),
            FadeIn(VGroup(x_label, y_label)),
        )
        self.play(
            Create(wave),
            Create(envelope_upper),
            Create(envelope_lower),
            Create(group_marker),
            Create(phase_marker),
            FadeIn(group_label),
            FadeIn(phase_label),
            FadeIn(legend),
            FadeIn(observation),
        )
        self.play(
            tracker.animate.set_value(7.0),
            run_time=8,
            rate_func=linear,
        )
        self.wait(1)
