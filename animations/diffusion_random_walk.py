"""Illustrative one-dimensional random walk for plasma diffusion.

The walkers use normalized coordinates

    xi = x / L_0
    tau = t / tau_0

and take symmetric steps.  The scene is a conceptual visualization of
diffusive spreading, not a Monte-Carlo transport calculation or measured data.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
WALKER_COLOR = "#4EA8DE"
TRACE_COLOR = "#72D6C9"
FORMULA_COLOR = "#F2A65A"


class DiffusionRandomWalk(Scene):
    """Show symmetric walkers spreading while their mean stays near zero."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Random walk to diffusion", color=INK, font_size=34)
        subtitle = Text(
            "normalized one-dimensional transport",
            color=MUTED,
            font_size=22,
        )
        title_group = VGroup(title, subtitle).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08
        )
        title_group.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.45)

        formula = MathTex(
            r"\langle x\rangle = 0,\qquad "
            r"\langle x^2\rangle = 2D t",
            color=FORMULA_COLOR,
            font_size=28,
        )
        formula.to_corner(UR, buff=0.42)

        axes = Axes(
            x_range=[-5.2, 5.2, 1.0],
            y_range=[-1.0, 1.0, 1.0],
            x_length=10.0,
            y_length=1.3,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.1)
        x_label = Text("x / L₀ (dimensionless)", color=MUTED, font_size=20)
        x_label.next_to(axes.x_axis, DOWN, buff=0.25)

        rng = np.random.default_rng(8)
        n_walkers = 36
        n_steps = 18
        steps = rng.choice([-1.0, 1.0], size=(n_walkers, n_steps))
        positions = np.concatenate(
            [np.zeros((n_walkers, 1)), 0.34 * np.cumsum(steps, axis=1)],
            axis=1,
        )
        y_offsets = np.linspace(-0.45, 0.45, n_walkers)
        step_tracker = ValueTracker(0.0)

        def current_position(index):
            step = min(int(round(step_tracker.get_value())), n_steps)
            return axes.c2p(positions[index, step], y_offsets[index])

        walkers = VGroup()
        for index in range(n_walkers):
            walker = Dot(
                current_position(index),
                radius=0.055,
                color=WALKER_COLOR,
            )
            walker.add_updater(
                lambda mob, index=index: mob.move_to(current_position(index))
            )
            walkers.add(walker)

        traces = VGroup()
        for index in (3, 15, 27):
            traces.add(
                TracedPath(
                    lambda index=index: walkers[index].get_center(),
                    stroke_color=TRACE_COLOR,
                    stroke_width=3,
                    dissipating_time=None,
                )
            )

        origin = DashedLine(
            axes.c2p(0, -0.72),
            axes.c2p(0, 0.72),
            color=MUTED,
            stroke_width=2,
        )
        origin_label = Text("initial position", color=MUTED, font_size=18)
        origin_label.next_to(origin, UP, buff=0.1)

        time_label = always_redraw(
            lambda: Text(
                f"step {min(int(round(step_tracker.get_value())), n_steps)} / {n_steps}",
                color=INK,
                font_size=21,
            ).to_corner(DR, buff=0.38)
        )
        observation = Text(
            "symmetric steps: displacement cancels, variance grows",
            color=TRACE_COLOR,
            font_size=21,
        )
        observation.to_edge(DOWN, buff=0.52)

        legend = VGroup(
            Text("blue dots: walkers", color=MUTED, font_size=18),
            Text("teal traces: selected paths", color=MUTED, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend.to_corner(DL, buff=0.35)

        self.play(
            FadeIn(title_group),
            FadeIn(formula),
            Create(axes),
            FadeIn(x_label),
            Create(origin),
            FadeIn(origin_label),
        )
        self.play(
            FadeIn(walkers),
            FadeIn(legend),
            FadeIn(observation),
            FadeIn(time_label),
        )
        self.add(*traces)
        self.play(
            step_tracker.animate.set_value(n_steps),
            run_time=9,
            rate_func=linear,
        )
        self.wait(1)
