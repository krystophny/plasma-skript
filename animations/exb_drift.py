"""Illustrative E x B drift animation.

The plotted quantity is the particle position in normalized coordinates. The
analytic path is

    x / rho = -2.5 + 0.55 t + 0.65 cos(2 t)
    y / rho = -0.8 + 0.65 sin(2 t),  0 <= t <= 8.

The circular part represents gyromotion and the linear part represents the
guiding-center drift. It is a conceptual visualization, not measured data.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
E_COLOR = "#4EA8DE"
B_COLOR = "#F2A65A"
DRIFT_COLOR = "#72D6C9"
PARTICLE_COLOR = "#F4F7FB"


class ExBDrift(Scene):
    """Show gyromotion and the rightward E x B guiding-center drift."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Charged-particle motion", color=INK, font_size=34)
        subtitle = Text("gyromotion plus E × B guiding-center drift", color=MUTED, font_size=22)
        title_group = VGroup(title, subtitle).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        title_group.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.45)

        axes = Axes(
            x_range=[-3.5, 3.8, 1],
            y_range=[-2.3, 2.5, 1],
            x_length=8.5,
            y_length=5.4,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.35 + LEFT * 0.35)
        x_label = Text("x / ρ [1]", color=MUTED, font_size=20).next_to(axes.x_axis, RIGHT, buff=0.15)
        y_label = Text("y / ρ [1]", color=MUTED, font_size=20).next_to(axes.y_axis, UP, buff=0.12)

        e_arrow = Arrow(
            axes.c2p(-2.85, -1.65),
            axes.c2p(-2.85, 0.25),
            color=E_COLOR,
            stroke_width=5,
            buff=0,
        )
        e_label = Text("E", color=E_COLOR, font_size=26).next_to(e_arrow, RIGHT, buff=0.12)

        b_circle = Circle(radius=0.18, color=B_COLOR, stroke_width=3)
        b_dot = Dot(radius=0.055, color=B_COLOR)
        b_marker = VGroup(b_circle, b_dot).move_to(axes.c2p(2.85, 1.65))
        b_label = Text("B out of page", color=B_COLOR, font_size=22).next_to(b_marker, LEFT, buff=0.14)

        drift_arrow = Arrow(
            axes.c2p(-1.8, 1.9),
            axes.c2p(0.1, 1.9),
            color=DRIFT_COLOR,
            stroke_width=5,
            buff=0,
        )
        drift_label = Text("E × B drift", color=DRIFT_COLOR, font_size=22).next_to(
            drift_arrow, UP, buff=0.1
        )

        tracker = ValueTracker(0)
        center_start = np.array([-2.35, -0.65])

        def center_coords():
            return np.array([center_start[0] + 0.55 * tracker.get_value(), center_start[1]])

        def particle_coords():
            t = tracker.get_value()
            center = center_coords()
            return center + 0.65 * np.array([np.cos(2 * t), np.sin(2 * t)])

        def scene_point(coords):
            return axes.c2p(coords[0], coords[1])

        particle_point = lambda: scene_point(particle_coords())
        center_point = lambda: scene_point(center_coords())

        orbit = TracedPath(
            particle_point,
            stroke_color=DRIFT_COLOR,
            stroke_width=4,
        )
        radius_line = always_redraw(
            lambda: DashedLine(
                center_point(),
                particle_point(),
                color=MUTED,
                stroke_width=2,
                dash_length=0.08,
            )
        )
        particle = always_redraw(
            lambda: Dot(particle_point(), radius=0.12, color=PARTICLE_COLOR)
        )
        guiding_center = always_redraw(
            lambda: Dot(center_point(), radius=0.08, color=DRIFT_COLOR)
        )
        center_label = Text("guiding center", color=DRIFT_COLOR, font_size=18)
        center_label.add_updater(
            lambda mob: mob.next_to(center_point(), DOWN + RIGHT, buff=0.12)
        )
        particle_label = Text("q > 0", color=PARTICLE_COLOR, font_size=18)
        particle_label.add_updater(
            lambda mob: mob.next_to(particle_point(), UP + RIGHT, buff=0.1)
        )

        legend = VGroup(
            Text("• circular motion: magnetic force", color=MUTED, font_size=18),
            Text("• translation: crossed-field drift", color=MUTED, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend.to_corner(DL, buff=0.35)

        static = VGroup(
            title_group,
            axes,
            x_label,
            y_label,
            e_arrow,
            e_label,
            b_marker,
            b_label,
            drift_arrow,
            drift_label,
            legend,
        )
        self.play(FadeIn(title_group), Create(axes), FadeIn(VGroup(x_label, y_label)))
        self.play(
            GrowArrow(e_arrow),
            FadeIn(e_label),
            FadeIn(b_marker),
            FadeIn(b_label),
            GrowArrow(drift_arrow),
            FadeIn(drift_label),
            FadeIn(legend),
        )
        self.add(orbit, radius_line, guiding_center, particle, center_label, particle_label)
        self.play(tracker.animate.set_value(8), run_time=8, rate_func=linear)
        self.wait(1)
        self.play(FadeOut(static), FadeOut(orbit), FadeOut(radius_line), FadeOut(guiding_center))
        self.play(FadeOut(particle), FadeOut(center_label), FadeOut(particle_label))
