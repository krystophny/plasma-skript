"""Schematic visualization of a Langmuir-probe characteristic.

The curve is a normalized idealized current--voltage characteristic.  The
right-hand panel identifies the probe and its surrounding sheath.  It is a
teaching map of the diagnostic regimes, not a fit to experimental data.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
GRID = "#51627A"
ELECTRON = "#72D6C9"
ION = "#F2A65A"
PROBE = "#D98E5B"
HIGHLIGHT = "#4EA8DE"


class LangmuirProbe(Scene):
    """Show the three useful regions of an idealized probe I--V curve."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("Langmuir-probe I–V characteristic", color=INK, font_size=32)
        subtitle = Text(
            "normalized idealized response · region labels guide the fit",
            color=MUTED,
            font_size=19,
        )
        heading = VGroup(title, subtitle).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08
        )
        heading.to_edge(UP, buff=0.25).to_edge(LEFT, buff=0.38)

        formula = MathTex(
            r"u=\frac{e(\phi_p-\phi_{pl})}{k_B T_e}",
            color=HIGHLIGHT,
            font_size=27,
        ).to_corner(UR, buff=0.36)

        axes = Axes(
            x_range=[-4.2, 2.6, 1],
            y_range=[-1.35, 0.35, 0.5],
            x_length=6.15,
            y_length=4.35,
            axis_config={"color": GRID, "stroke_width": 2},
            tips=False,
        ).shift(LEFT * 2.25 + DOWN * 0.2)
        x_label = Text("probe bias u", color=MUTED, font_size=18)
        x_label.next_to(axes, DOWN, buff=0.12)
        y_label = Text("I / (e Γₑ₀ A)", color=MUTED, font_size=18)
        y_label.rotate(PI / 2)
        y_label.next_to(axes, LEFT, buff=0.12)

        def current(u):
            if u <= 0:
                return 0.058 - np.exp(u)
            return -1.0 - 0.22 * u

        curve = axes.plot(current, x_range=[-4.2, 2.6], color=HIGHLIGHT, stroke_width=4)
        floating_u = np.log(0.058)
        floating_line = DashedLine(
            axes.c2p(floating_u, -1.35),
            axes.c2p(floating_u, 0.02),
            color=ION,
            dash_length=0.12,
            stroke_width=2.5,
        )
        floating_label = MathTex(r"u_f", color=ION, font_size=25)
        floating_label.next_to(floating_line, UP, buff=0.05)
        zero_line = DashedLine(
            axes.c2p(-4.2, 0), axes.c2p(2.6, 0), color=GRID, dash_length=0.1
        )

        region_labels = VGroup(
            Text("ion saturation", color=ION, font_size=19),
            Text("electron retardation", color=ELECTRON, font_size=19),
            Text("electron saturation", color=PROBE, font_size=19),
        )
        region_labels[0].move_to(axes.c2p(-3.25, -0.18))
        region_labels[1].move_to(axes.c2p(-1.05, -1.14))
        region_labels[2].move_to(axes.c2p(1.25, -1.17))

        probe_panel = RoundedRectangle(
            width=4.0,
            height=4.25,
            corner_radius=0.18,
            stroke_color=GRID,
            stroke_width=2,
            fill_color=BG,
            fill_opacity=0.45,
        ).shift(RIGHT * 3.25 + DOWN * 0.2)
        panel_title = Text("probe in plasma", color=INK, font_size=22)
        panel_title.next_to(probe_panel, UP, buff=0.14)
        probe = RoundedRectangle(
            width=0.60,
            height=2.55,
            corner_radius=0.22,
            stroke_color=PROBE,
            stroke_width=3,
            fill_color=PROBE,
            fill_opacity=0.78,
        ).move_to(probe_panel.get_center())
        sheath = RoundedRectangle(
            width=1.35,
            height=3.15,
            corner_radius=0.38,
            stroke_color=ION,
            stroke_width=2,
            stroke_opacity=0.9,
            fill_color=ION,
            fill_opacity=0.10,
        ).move_to(probe_panel.get_center())
        sheath_label = Text("sheath", color=ION, font_size=18).next_to(
            sheath, RIGHT, buff=0.1
        )

        particles = VGroup()
        particle_arrows = VGroup()
        for y in [-1.15, -0.55, 0.1, 0.78, 1.35]:
            start = probe_panel.get_left() + RIGHT * 0.25 + UP * y
            end = start + RIGHT * 0.86
            particles.add(Dot(start, radius=0.065, color=ELECTRON))
            particle_arrows.add(
                Arrow(start, end, color=ELECTRON, stroke_width=2, buff=0.04)
            )
        ion_arrow = Arrow(
            probe_panel.get_left() + RIGHT * 0.12 + DOWN * 1.64,
            probe_panel.get_center() + DOWN * 1.0,
            color=ION,
            stroke_width=3,
            buff=0.04,
        )
        ion_arrow_label = Text("ions", color=ION, font_size=18).next_to(
            ion_arrow, DOWN, buff=0.04
        )
        electron_arrow_label = Text("electrons", color=ELECTRON, font_size=18)
        electron_arrow_label.next_to(probe_panel, RIGHT, buff=0.08)

        tracker = ValueTracker(-3.2)
        probe_marker = always_redraw(
            lambda: Dot(
                axes.c2p(tracker.get_value(), current(tracker.get_value())),
                radius=0.10,
                color=ION,
            )
        )
        bias_label = always_redraw(
            lambda: MathTex(
                rf"u={tracker.get_value():.1f}", color=ION, font_size=24
            ).next_to(probe_marker, UR, buff=0.08)
        )
        measurement_note = Text(
            "slope of ln |Iₑ| gives Tₑ; scale gives nₑ",
            color=INK,
            font_size=19,
        ).to_edge(DOWN, buff=0.22)

        self.play(FadeIn(heading), FadeIn(formula))
        self.play(
            Create(axes),
            Create(zero_line),
            Create(curve),
            FadeIn(VGroup(x_label, y_label)),
            FadeIn(region_labels),
        )
        self.play(
            Create(probe_panel),
            FadeIn(panel_title),
            FadeIn(sheath),
            FadeIn(probe),
            FadeIn(sheath_label),
            Create(particle_arrows),
            FadeIn(particles),
            Create(ion_arrow),
            FadeIn(ion_arrow_label),
            FadeIn(electron_arrow_label),
        )
        self.play(
            Create(floating_line),
            FadeIn(floating_label),
            FadeIn(measurement_note),
            FadeIn(probe_marker),
            FadeIn(bias_label),
        )
        self.play(tracker.animate.set_value(1.9), run_time=4.5, rate_func=linear)
        self.play(tracker.animate.set_value(-3.2), run_time=3.0, rate_func=linear)
        self.wait(1.0)
