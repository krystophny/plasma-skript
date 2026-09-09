"""Illustrative free streaming in one-dimensional phase space.

The scene uses the normalized variables

    xi = x / L_0, eta = v / v_0, tau = t v_0 / L_0.

Each sample follows the collisionless characteristic

    xi(tau) = xi_0 + eta tau, eta(tau) = eta_0.

The samples are a deterministic illustration of a distribution, not a
particle-in-cell calculation and not measured data.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
SAMPLE_COLOR = "#F2A65A"
TRACE_COLOR = "#72D6C9"
CHARACTERISTIC_COLOR = "#4EA8DE"


class PhaseSpaceAdvection(Scene):
    """Show a phase-space cloud shearing under collisionless free streaming."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Free streaming in phase space", color=INK, font_size=32)
        subtitle = Text(
            "normalized one-dimensional illustration",
            color=MUTED,
            font_size=21,
        )
        title_group = VGroup(title, subtitle).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08
        )
        title_group.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.4)

        formula = MathTex(
            r"\frac{\partial f}{\partial \tau}"
            r"+\eta\frac{\partial f}{\partial \xi}=0",
            color=TRACE_COLOR,
            font_size=27,
        )
        formula.to_corner(UR, buff=0.38)

        axes = Axes(
            x_range=[-4.5, 4.5, 1.0],
            y_range=[-0.4, 1.2, 0.4],
            x_length=8.6,
            y_length=4.8,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.35 + LEFT * 0.25)

        x_label = Text("x / L₀ [1]", color=MUTED, font_size=19)
        x_label.next_to(axes.x_axis, DOWN, buff=0.22)
        v_label = Text("v / v₀ [1]", color=MUTED, font_size=19)
        v_label.rotate(PI / 2)
        v_label.next_to(axes.y_axis, LEFT, buff=0.2)

        # A fixed random seed makes the visual reproducible across builds.
        rng = np.random.default_rng(12)
        samples = rng.normal(loc=(0.0, 0.0), scale=(0.38, 0.12), size=(42, 2))
        x0_values = -2.3 + samples[:, 0]
        v0_values = 0.45 + samples[:, 1]
        tracker = ValueTracker(0.0)

        def sample_point(x0, v0):
            tau = tracker.get_value()
            return axes.c2p(x0 + v0 * tau, v0)

        dots = VGroup()
        for x0, v0 in zip(x0_values, v0_values):
            dot = Dot(
                axes.c2p(x0, v0),
                radius=0.055,
                color=SAMPLE_COLOR,
            )
            dot.add_updater(
                lambda mob, x0=x0, v0=v0: mob.move_to(sample_point(x0, v0))
            )
            dots.add(dot)

        traces = VGroup()
        for index in (8, 20, 32):
            traces.add(
                TracedPath(
                    lambda index=index: dots[index].get_center(),
                    stroke_color=TRACE_COLOR,
                    stroke_width=3,
                    dissipating_time=None,
                )
            )

        flow_arrows = VGroup()
        for velocity in (0.25, 0.45, 0.65):
            arrow = Arrow(
                axes.c2p(-3.8, velocity),
                axes.c2p(-2.8, velocity),
                color=CHARACTERISTIC_COLOR,
                stroke_width=3,
                buff=0,
            )
            flow_arrows.add(arrow)

        arrow_label = Text(
            "characteristics: faster v moves farther",
            color=CHARACTERISTIC_COLOR,
            font_size=18,
        )
        arrow_label.next_to(flow_arrows[2], UP, buff=0.08)

        initial_outline = Ellipse(
            width=1.0,
            height=0.7,
            color=MUTED,
            stroke_width=2,
        ).move_to(axes.c2p(-2.3, 0.45))
        initial_label = Text("initial support", color=MUTED, font_size=18)
        initial_label.move_to(axes.c2p(-3.25, 0.95))

        observation = Text(
            "velocity stays fixed along each characteristic",
            color=INK,
            font_size=19,
        )
        observation.to_edge(DOWN, buff=0.32).to_edge(RIGHT, buff=0.35)

        legend = VGroup(
            Text("dots: samples of f", color=MUTED, font_size=17),
            Text("teal traces: selected characteristics", color=MUTED, font_size=17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        legend.to_corner(DL, buff=0.3)

        self.play(
            FadeIn(title_group),
            FadeIn(formula),
            Create(axes),
            FadeIn(VGroup(x_label, v_label)),
        )
        self.play(
            FadeIn(initial_outline),
            FadeIn(initial_label),
            FadeIn(dots),
            FadeIn(flow_arrows),
            FadeIn(arrow_label),
            FadeIn(observation),
            FadeIn(legend),
        )
        self.add(*traces)
        self.play(tracker.animate.set_value(5.0), run_time=8, rate_func=linear)
        self.wait(1)
