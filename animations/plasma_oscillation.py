"""Illustrative cold electron plasma oscillation.

The electrons are shown as a finite slab displaced against fixed ions. The
animation uses the normalized displacement

    xi / xi_0 = cos(t omega_p,e),

where xi_0 is a reference displacement and t omega_p,e has unit [1]. It
is a conceptual visualization of the restoring-field argument, not measured
data and not a particle-in-cell calculation.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
ION_COLOR = "#4EA8DE"
ELECTRON_COLOR = "#F2A65A"
FIELD_COLOR = "#72D6C9"


class PlasmaOscillation(Scene):
    """Show a collective electron displacement and its restoring field."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Electron plasma oscillation", color=INK, font_size=34)
        subtitle = Text(
            "normalized displacement against fixed ions",
            color=MUTED,
            font_size=22,
        )
        title_group = VGroup(title, subtitle).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08
        )
        title_group.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.45)

        formula = MathTex(
            r"\xi/\xi_0 = \cos(t\,\omega_{p,e})",
            color=FIELD_COLOR,
            font_size=28,
        )
        formula.to_corner(UR, buff=0.42)

        axes = Axes(
            x_range=[-5.0, 5.0, 1.0],
            y_range=[-1.0, 1.0, 1.0],
            x_length=9.0,
            y_length=1.2,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.55)
        x_label = Text("x / L₀ [1]", color=MUTED, font_size=20)
        x_label.next_to(axes.x_axis, DOWN, buff=0.25)

        x_positions = np.linspace(-4.0, 4.0, 9)
        ions = VGroup(
            *[
                Triangle(
                    color=ION_COLOR,
                    fill_color=ION_COLOR,
                    fill_opacity=1,
                    stroke_width=1,
                ).scale(0.11).move_to(axes.c2p(x, 0.18))
                for x in x_positions
            ]
        )
        electrons = VGroup(
            *[
                Dot(axes.c2p(x, -0.18), radius=0.09, color=ELECTRON_COLOR)
                for x in x_positions
            ]
        )

        tracker = ValueTracker(0.0)

        def displacement():
            return 0.55 * np.cos(tracker.get_value())

        for dot, x0 in zip(electrons, x_positions):
            dot.add_updater(
                lambda mob, x0=x0: mob.move_to(
                    axes.c2p(x0 + displacement(), -0.18)
                )
            )

        restoring_arrow = always_redraw(
            lambda: Arrow(
                axes.c2p(displacement(), -0.45),
                axes.c2p(
                    displacement() - (0.85 if displacement() >= 0 else -0.85),
                    -0.45,
                ),
                color=FIELD_COLOR,
                stroke_width=5,
                buff=0,
            )
        )
        # Keep labels in fixed, separated zones so the static poster remains
        # legible at every phase of the oscillation.
        field_label = Text("restoring field", color=FIELD_COLOR, font_size=20)
        field_label.move_to(axes.c2p(3.0, -0.85))

        ions_label = Text("fixed ions", color=ION_COLOR, font_size=20)
        ions_label.move_to(axes.c2p(-3.25, 0.65))
        electrons_label = Text("electron slab", color=ELECTRON_COLOR, font_size=20)
        electrons_label.move_to(axes.c2p(-3.25, -0.65))

        legend = VGroup(
            Text("triangles: fixed positive ions", color=MUTED, font_size=18),
            Text("dots: electrons move together", color=MUTED, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend.to_corner(DL, buff=0.35)

        self.play(
            FadeIn(title_group),
            FadeIn(formula),
            Create(axes),
            FadeIn(x_label),
        )
        self.play(
            FadeIn(ions),
            FadeIn(electrons),
            FadeIn(ions_label),
            FadeIn(electrons_label),
            GrowArrow(restoring_arrow),
            FadeIn(field_label),
            FadeIn(legend),
        )
        self.add(*electrons, restoring_arrow, field_label)
        self.play(tracker.animate.set_value(4 * PI), run_time=8, rate_func=linear)
        self.wait(1)
