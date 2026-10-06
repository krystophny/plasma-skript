"""Schematic visualization of a Langmuir-probe characteristic.

The curve is a normalized idealized current--voltage characteristic.  The
right-hand panel identifies the probe and its surrounding sheath.  It is a
teaching map of the diagnostic regimes, not a fit to experimental data.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, CURVE_WIDTH, DOT_RADIUS, EASE, ELECTRON, FAINT, GRID, INK, ION,
    LINEAR, MUTED, POTENTIAL, SMALL_SIZE, THIN_WIDTH, StyledScene, axes,
    label, math,
    MATH_SMALL,
)


def probe_current(u):
    """Ideal planar collection: ion-positive current / (e Gamma_e0 A).

    Constant ion contribution 0.058 and electron exp(u) below plasma
    potential, capped at one above it. Continuous, with a model corner at 0.
    """
    return 0.058 - np.exp(np.minimum(u, 0.0))


U_FLOAT = np.log(0.058)


class LangmuirProbe(StyledScene):
    """Sweep the probe bias across the three regions of an ideal I-V curve."""

    def build(self):
        ax = axes([-6, 2.5, 1], [-1.1, 0.25, 0.5], 7.2, 5.0).move_to([-2.75, -0.1, 0])
        xlab = math(r"e(\phi_p-\phi_{pl})/k_BT_e\ [1]", color=MUTED, size=MATH_SMALL)
        xlab.next_to(ax.c2p(2.5, -1.1), DOWN, buff=0.15).align_to(ax.c2p(2.5, 0), RIGHT)
        ylab = math(r"I_p/(e\,\Gamma_{e0}A)\ [1]", color=MUTED, size=MATH_SMALL)
        ylab.next_to(ax.y_axis.get_top(), UP, buff=0.15)

        curve = ax.plot(probe_current, x_range=[-6, 2.5, 0.01], color=INK, stroke_width=CURVE_WIDTH)
        ion_sat = label("ion saturation", color=ION, size=SMALL_SIZE)
        ion_sat.next_to(ax.c2p(-4.6, 0.058), UP, buff=0.18)
        retard = label("retardation", color=ELECTRON, size=SMALL_SIZE)
        retard.move_to(ax.c2p(-3.3, -0.55))
        e_sat = label("electron saturation", color=ELECTRON, size=SMALL_SIZE)
        e_sat.next_to(ax.c2p(0.15, -0.942), DOWN + RIGHT, buff=0.2)
        knee = Dot(ax.c2p(0, -0.942), radius=0.06, color=MUTED)
        knee_lab = math(r"\phi_p=\phi_{pl}", color=MUTED, size=MATH_SMALL).next_to(knee, LEFT, buff=0.18)
        f_dot = Dot(ax.c2p(U_FLOAT, 0), radius=0.07, color=MUTED)
        f_lab = math(r"\phi_f", color=MUTED, size=MATH_SMALL).next_to(f_dot, DOWN + LEFT, buff=0.08)

        u = ValueTracker(-5.5)
        point = always_redraw(lambda: Dot(ax.c2p(u.get_value(), probe_current(u.get_value())),
                                          radius=0.11, color=ACCENT))

        # Probe sketch: electrons arrive from the left, ions from the right.
        center = np.array([4.6, -0.1, 0])
        frame = RoundedRectangle(width=3.6, height=5.0, corner_radius=0.15,
                                 stroke_color=GRID, stroke_width=1.6).move_to(center)
        sheath = RoundedRectangle(width=1.35, height=3.2, corner_radius=0.5, stroke_width=0,
                                  fill_color=POTENTIAL, fill_opacity=0.14).move_to(center)
        sheath_edge = DashedVMobject(RoundedRectangle(width=1.35, height=3.2, corner_radius=0.5,
                                                      stroke_color=POTENTIAL, stroke_width=1.6)
                                     .move_to(center), num_dashes=40)
        probe = RoundedRectangle(width=0.36, height=2.3, corner_radius=0.16, stroke_width=0,
                                 fill_color=MUTED, fill_opacity=1).move_to(center)
        probe_lab = label("probe", color=MUTED, size=SMALL_SIZE).next_to(sheath, UP, buff=0.2)
        sheath_lab = label("sheath", color=POTENTIAL, size=SMALL_SIZE).next_to(sheath, DOWN, buff=0.2)

        heights = (-0.9, 0.0, 0.9)
        left_x, right_x = center[0] - 0.68, center[0] + 0.68

        def flux_arrows(side, flux, color, marker):
            def make():
                length = 0.3 + 1.0 * flux()
                group = VGroup()
                for h in heights:
                    end = np.array([left_x if side < 0 else right_x, center[1] + h, 0])
                    start = end + np.array([side * length, 0, 0])
                    group.add(Arrow(start, end, buff=0, color=color, stroke_width=3,
                                    max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12))
                    group.add(marker().move_to(start + np.array([side * 0.14, 0, 0])))
                return group
            return always_redraw(make)

        e_arrows = flux_arrows(-1, lambda: np.exp(min(u.get_value(), 0.0)), ELECTRON,
                               lambda: Dot(radius=DOT_RADIUS, color=ELECTRON))
        i_arrows = flux_arrows(1, lambda: 0.058, ION,
                               lambda: Triangle(color=ION, fill_opacity=1, stroke_width=0).scale(0.09))

        self.play(Create(ax), FadeIn(xlab), FadeIn(ylab), run_time=0.9, rate_func=EASE)
        self.play(Create(curve), FadeIn(frame), FadeIn(sheath), FadeIn(sheath_edge), FadeIn(probe),
                  run_time=1.2, rate_func=EASE)
        self.play(FadeIn(VGroup(ion_sat, retard, e_sat, knee, knee_lab, f_dot, f_lab,
                                probe_lab, sheath_lab)),
                  FadeIn(point), FadeIn(e_arrows), FadeIn(i_arrows),
                  run_time=0.7, rate_func=EASE)
        self.play(u.animate.set_value(2.0), run_time=4.5, rate_func=LINEAR)
        self.play(u.animate.set_value(U_FLOAT), run_time=2.2, rate_func=EASE)
        self.wait(1.5)
