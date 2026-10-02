"""Illustrative cold electron plasma oscillation.

The electrons are shown as a finite slab displaced against fixed ions. The
animation uses the normalized displacement

    xi / xi_0 = cos(t omega_p,e),

where xi_0 is a reference displacement and t omega_p,e has unit [1]. It
is a conceptual visualization of the restoring-field argument, not measured
data and not a particle-in-cell calculation.

For a displacement xi > 0 of the electron slab, a sheet of bare ions is
exposed on the left and a sheet of excess electrons appears on the right, so
the field between them points along +x: E = e n0 xi/epsilon_0 (SI). The electron force
-eE points back toward equilibrium. Positions use L0 with xi_0/L0 = 0.55.
"""

from manim import *
import numpy as np

from style import (
    BG, E_FIELD, EASE, ELECTRON, FAINT, INK, ION, LINEAR, MUTED, CURVE_WIDTH,
    THIN_WIDTH, StyledScene, axes, axis_labels, math,
    MATH_SIZE, MATH_SMALL,
)


def slab_state(tau):
    """Return xi/xi0, E/(e n0 xi0/epsilon_0), F/(e² n0 xi0/epsilon_0)."""
    return np.array([np.cos(tau), np.cos(tau), -np.cos(tau)])


XI0 = 0.55          # xi_0 / L0
HALF_WIDTH = 4.0    # slab half-width in L0
ARROW_SCALE = 1.5   # Manim units per unit of E/E0 or F_e/(e E0)


def _signed_arrow(start, length, color):
    """Horizontal arrow of signed length; empty when the length vanishes."""
    if abs(length) < 0.04:
        return VMobject()
    return Arrow(start, start + RIGHT * length, buff=0, color=color,
                 stroke_width=5, max_tip_length_to_length_ratio=0.3,
                 max_stroke_width_to_length_ratio=12)


class PlasmaOscillation(StyledScene):
    """Show a collective electron displacement and its restoring field."""

    def build(self):
        # --- slab view ---------------------------------------------------
        slab_ax = axes([-5, 5, 1], [0, 1, 1], 10.5, 1.0).move_to(UP * 2.0)
        slab_ax.y_axis.set_opacity(0)
        x_lab = math(r"x/L_0\ [1]", color=MUTED, size=MATH_SMALL)
        x_lab.next_to(slab_ax.x_axis.get_right(), DOWN, buff=0.22).align_to(
            slab_ax.x_axis.get_right(), RIGHT)
        y_ion, y_el = 0.78, 0.38

        def p(x, y):
            return slab_ax.c2p(x, y)

        columns = np.linspace(-HALF_WIDTH + 0.25, HALF_WIDTH - 0.25, 16)
        ions = VGroup(*[
            Triangle(color=ION, fill_color=ION, fill_opacity=1, stroke_width=0)
            .scale(0.12).move_to(p(x, y_ion)) for x in columns
        ])

        tracker = ValueTracker(0.0)

        def xi():
            return XI0 * slab_state(tracker.get_value())[0]

        electrons = VGroup(*[Dot(p(x, y_el), radius=0.1, color=ELECTRON) for x in columns])
        for dot, x0 in zip(electrons, columns):
            dot.add_updater(lambda m, x0=x0: m.move_to(p(x0 + xi(), y_el)))

        def charge_sheets():
            d = xi()
            bottom, top = p(0, 0.15)[1], p(0, 1.0)[1]
            group = VGroup()
            if abs(d) < 0.02:
                return group
            # Uncovered ions (net +) on the trailing side, excess electrons
            # (net -) on the leading side.
            if d > 0:
                plus_span, minus_span = (-HALF_WIDTH, -HALF_WIDTH + d), (HALF_WIDTH, HALF_WIDTH + d)
            else:
                plus_span, minus_span = (HALF_WIDTH + d, HALF_WIDTH), (-HALF_WIDTH + d, -HALF_WIDTH)
            for (a, b), color, sign in ((plus_span, ION, "+"), (minus_span, ELECTRON, "-")):
                left, right = p(a, 0)[0], p(b, 0)[0]
                rect = Rectangle(width=right - left, height=top - bottom, stroke_width=0,
                                 fill_color=color, fill_opacity=0.22)
                rect.move_to([(left + right) / 2, (top + bottom) / 2, 0])
                group.add(rect)
                mark = math(sign, color=color, size=MATH_SIZE)
                mark.next_to(rect, UP, buff=0.08)
                mark.set_opacity(min(1.0, abs(d) / (0.5 * XI0)))
                group.add(mark)
            return group

        sheets = always_redraw(charge_sheets)

        # --- field and force arrows ---------------------------------------
        y_e, y_f = 0.4, -0.2
        e_lab = math(r"E", color=E_FIELD, size=MATH_SIZE)
        e_lab.move_to([-2.0, y_e, 0], aligned_edge=RIGHT)
        f_lab = math(r"F_e", color=ELECTRON, size=MATH_SIZE)
        f_lab.move_to([-2.0, y_f, 0], aligned_edge=RIGHT)
        center_tick = DashedLine([0, y_e + 0.35, 0], [0, y_f - 0.3, 0], color=FAINT,
                                 stroke_width=1.4, dash_length=0.06)
        e_arrow = always_redraw(lambda: _signed_arrow(
            np.array([0, y_e, 0]), ARROW_SCALE * slab_state(tracker.get_value())[1], E_FIELD))
        f_arrow = always_redraw(lambda: _signed_arrow(
            np.array([0, y_f, 0]), ARROW_SCALE * slab_state(tracker.get_value())[2], ELECTRON))

        # --- time trace ----------------------------------------------------
        t_ax = axes([0, 4 * PI, PI], [-1.2, 1.2, 1], 10.0, 1.7).move_to(DOWN * 2.15 + RIGHT * 0.4)
        t_labels = VGroup(
            math(r"\omega_{pe}t\ [1]", color=MUTED, size=MATH_SMALL).next_to(t_ax.x_axis.get_right(), DOWN, buff=0.22)
            .align_to(t_ax.x_axis.get_right(), RIGHT),
            math(r"\xi/\xi_0\ [1]", color=MUTED, size=MATH_SMALL).next_to(t_ax.y_axis, LEFT, buff=0.2),
        )
        trace = always_redraw(lambda: t_ax.plot(
            lambda t: slab_state(t)[0], x_range=[0, max(tracker.get_value(), 1e-3), 0.03],
            color=ELECTRON, stroke_width=CURVE_WIDTH - 1))
        trace_dot = always_redraw(lambda: Dot(
            t_ax.c2p(tracker.get_value(), slab_state(tracker.get_value())[0]),
            radius=0.07, color=ELECTRON))

        self.play(Create(slab_ax.x_axis), FadeIn(x_lab),
                  Create(t_ax), FadeIn(t_labels), run_time=0.8, rate_func=EASE)
        self.play(FadeIn(ions), FadeIn(electrons), FadeIn(e_lab), FadeIn(f_lab),
                  FadeIn(center_tick), FadeIn(sheets), FadeIn(e_arrow), FadeIn(f_arrow),
                  run_time=0.6, rate_func=EASE)
        self.add(trace, trace_dot)
        self.play(tracker.animate.set_value(4 * PI), run_time=8, rate_func=LINEAR)
        self.wait(1.2)
