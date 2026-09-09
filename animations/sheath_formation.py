"""Schematic visualization of a collisionless plasma sheath.

The scene is a normalized teaching illustration.  It shows the wall-side
potential drop, the different electron and ion density responses, and the
qualitative flux imbalance that charges a floating surface.  It is not a
particle-in-cell calculation or a self-consistent numerical sheath solution.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
ELECTRON = "#72D6C9"
ION = "#F2A65A"
POTENTIAL = "#4EA8DE"
WALL = "#D98E5B"


class SheathFormation(Scene):
    """Show density separation and a potential barrier near a wall."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Plasma sheath formation", color=INK, font_size=34)
        subtitle = Text(
            "normalized planar boundary illustration · not a particle simulation",
            color=MUTED,
            font_size=19,
        )
        heading = VGroup(title, subtitle).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08
        )
        heading.to_edge(UP, buff=0.25).to_edge(LEFT, buff=0.38)

        wall = Rectangle(
            width=0.52,
            height=5.0,
            fill_color=WALL,
            fill_opacity=0.85,
            stroke_color=WALL,
            stroke_width=1,
        ).to_edge(RIGHT, buff=0.45)
        wall_label = Text("wall", color=INK, font_size=22).rotate(PI / 2)
        wall_label.next_to(wall, RIGHT, buff=0.14)

        domain = NumberLine(
            x_range=[0, 8, 1],
            length=8.55,
            include_numbers=False,
            include_ticks=False,
            color=GRID,
        ).shift(DOWN * 2.35 + LEFT * 0.45)
        domain_label = Text(
            "distance from wall / λ₍D₎ [1]", color=MUTED, font_size=18
        )
        domain_label.next_to(domain, DOWN, buff=0.12)

        sheath_edge_x = domain.n2p(4.7)[0]
        sheath_edge = DashedLine(
            np.array([sheath_edge_x, -2.52, 0.0]),
            np.array([sheath_edge_x, 2.05, 0.0]),
            color=ION,
            dash_length=0.12,
            stroke_width=2,
        )
        sheath_edge_label = Text(
            "sheath edge", color=ION, font_size=19
        ).next_to(sheath_edge, UP, buff=0.08)
        plasma_label = Text("quasineutral plasma", color=ELECTRON, font_size=21)
        plasma_label.move_to(np.array([domain.n2p(2.0)[0], 1.84, 0.0]))
        sheath_label = Text("charge-separated sheath", color=ION, font_size=21)
        sheath_label.move_to(np.array([domain.n2p(6.1)[0], 1.84, 0.0]))

        profile_axes = Axes(
            x_range=[0, 8, 2],
            y_range=[0, 1.35, 0.5],
            x_length=8.55,
            y_length=2.35,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.65 + LEFT * 0.45)
        profile_y = Text("normalized density [1]", color=MUTED, font_size=18)
        profile_y.rotate(PI / 2)
        profile_y.next_to(profile_axes, LEFT, buff=0.13)

        def electron_density(x):
            return 1.0 if x <= 4.7 else np.exp(-0.72 * (x - 4.7))

        def ion_density(x):
            return 1.0 if x <= 4.7 else 1.0 / np.sqrt(1.0 + 0.55 * (x - 4.7))

        electron_curve = profile_axes.plot(
            electron_density, x_range=[0, 8], color=ELECTRON, stroke_width=4
        )
        ion_curve = profile_axes.plot(
            ion_density, x_range=[0, 8], color=ION, stroke_width=4
        )
        electron_curve_label = Text(
            "electrons", color=ELECTRON, font_size=18
        ).move_to(profile_axes.c2p(6.35, 0.54))
        ion_curve_label = Text("ions", color=ION, font_size=18).move_to(
            profile_axes.c2p(6.4, 0.83)
        )

        potential_axes = Axes(
            x_range=[0, 8, 2],
            y_range=[-1.05, 0.15, 0.5],
            x_length=8.55,
            y_length=1.55,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 2.05 + LEFT * 0.45)
        potential_curve = potential_axes.plot(
            lambda x: -0.93 * (max(x - 4.7, 0.0) / 3.3) ** (4.0 / 3.0),
            x_range=[0, 8],
            color=POTENTIAL,
            stroke_width=4,
        )
        potential_label = Text(
            "−eφ / k₍B₎Tₑ [1]", color=POTENTIAL, font_size=20
        )
        potential_label.next_to(potential_axes, LEFT, buff=0.18)

        flux_e_y = 1.06
        flux_i_y = 0.78
        e_arrow = Arrow(
            np.array([domain.n2p(2.1)[0], flux_e_y, 0.0]),
            np.array([domain.n2p(3.2)[0], flux_e_y, 0.0]),
            color=ELECTRON,
            stroke_width=3,
            buff=0,
        )
        i_arrow = Arrow(
            np.array([domain.n2p(2.1)[0], flux_i_y, 0.0]),
            np.array([domain.n2p(5.7)[0], flux_i_y, 0.0]),
            color=ION,
            stroke_width=3,
            buff=0,
        )
        e_flux_label = Text("fast electrons reflect", color=ELECTRON, font_size=18)
        e_flux_label.next_to(e_arrow, UP, buff=0.06)
        i_flux_label = Text("ions reach the wall", color=ION, font_size=18)
        i_flux_label.next_to(i_arrow, DOWN, buff=0.06)

        self.e_progress = ValueTracker(0.0)
        self.i_progress = ValueTracker(0.0)
        e_particle = Dot(
            np.array([domain.n2p(1.3)[0], flux_e_y, 0.0]),
            radius=0.10,
            color=ELECTRON,
        )
        ion_particle = Dot(
            np.array([domain.n2p(1.3)[0], flux_i_y, 0.0]),
            radius=0.10,
            color=ION,
        )
        e_particle.add_updater(
            lambda dot: dot.move_to(
                np.array(
                    [
                        domain.n2p(
                            1.3 + 2.7 * min(self.e_progress.get_value(), 1.0)
                        )[0],
                        flux_e_y,
                        0.0,
                    ]
                )
            )
        )
        ion_particle.add_updater(
            lambda dot: dot.move_to(
                np.array(
                    [
                        domain.n2p(
                            1.3 + 4.8 * min(self.i_progress.get_value(), 1.0)
                        )[0],
                        flux_i_y,
                        0.0,
                    ]
                )
            )
        )
        charge_note = Text(
            "initial electron loss charges the wall negative",
            color=INK,
            font_size=20,
        ).to_edge(DOWN, buff=0.18)

        self.play(FadeIn(heading), FadeIn(wall), FadeIn(wall_label))
        self.play(
            Create(domain),
            FadeIn(domain_label),
            FadeIn(plasma_label),
            FadeIn(sheath_label),
            Create(sheath_edge),
            FadeIn(sheath_edge_label),
        )
        self.play(
            Create(profile_axes),
            Create(electron_curve),
            Create(ion_curve),
            FadeIn(profile_y),
            FadeIn(electron_curve_label),
            FadeIn(ion_curve_label),
        )
        self.play(
            Create(potential_axes),
            Create(potential_curve),
            FadeIn(potential_label),
            FadeIn(charge_note),
        )
        self.play(
            Create(e_arrow),
            Create(i_arrow),
            FadeIn(e_flux_label),
            FadeIn(i_flux_label),
            FadeIn(e_particle),
            FadeIn(ion_particle),
        )
        self.play(
            self.e_progress.animate.set_value(1.0),
            self.i_progress.animate.set_value(1.0),
            run_time=3.5,
            rate_func=linear,
        )
        self.play(self.e_progress.animate.set_value(0.0), run_time=1.8)
        self.wait(1.0)
