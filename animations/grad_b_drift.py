"""Grad-B drift of an ion and an electron from full Lorentz-force orbits.

Model: B = B_0 (1 + y/L) e_z (out of the page), L = 10 r_Li, E = 0.  Both
species start with their guiding centre at the origin, equal temperature,
reduced mass ratio m_i/m_e = 16 (gyration scenes); the orbits are Boris
pushes of dv/dt = (q/m) v x B (drift_models.grad_b_orbit), not drawn paths.
Drift formula (first order in r_L/L):

    v_gradB = (m v_perp^2/(2 q B)) (B x grad B)/B^2 = -mu B'/(q B^2) e_x,

mu = m v_perp^2/(2B); at equal temperature mu is the same for both species,
so the speeds are equal and the directions opposite.  Velocities are shown in
units of r_Li Omega_i [1], lengths in r_Li [1], time as Omega_i t [1].
The measured value is the slope of the guiding centre
R = x + (m/q) v x B/B^2 over the whole run.
"""

from manim import *
import numpy as np

from drift_models import (
    GRAD_B_L, QM_ELECTRON, QM_ION, drift_speed, grad_b_formula, grad_b_orbit,
)
from style import (
    B_FIELD, CURVE_WIDTH, DOT_RADIUS, ELECTRON, FAINT, INK, ION, LINEAR, MATH_SIZE,
    MATH_SMALL, MUTED, THIN_WIDTH, StyledScene, axes, axis_labels, math,
)

ION_PERIODS = 10
V_PERP_ION = 1.0
V_PERP_ELECTRON = 4.0            # equal temperature, m_e = m_i/16
GRID = 7200                      # common animation samples
PLAY_TIME = 18.0


def run_species(qm, v_perp, periods):
    """Orbit, guiding centre, measured and formula drift velocity (x)."""
    t, x, _, centre = grad_b_orbit(qm, v_perp, periods=periods, length=GRAD_B_L)
    measured = drift_speed(t, centre)[0]
    return t, x, centre, measured, grad_b_formula(qm, v_perp, GRAD_B_L)


def on_grid(t, x, n=GRID):
    """Linear resampling of an orbit onto n equally spaced times."""
    grid = np.linspace(0, t[-1], n)
    return grid, np.array([np.interp(grid, t, x[:, k]) for k in range(3)]).T


class GradBDrift(StyledScene):
    """Ion and electron orbits in B(y): opposite drifts of equal speed."""

    def build(self):
        ion = run_species(QM_ION, V_PERP_ION, ION_PERIODS)
        ele = run_species(QM_ELECTRON, V_PERP_ELECTRON, ION_PERIODS)
        grid, ion_x = on_grid(ion[0], ion[1])
        _, ion_c = on_grid(ion[0], ion[2])
        _, ele_x = on_grid(ele[0], ele[1])
        _, ele_c = on_grid(ele[0], ele[2])
        t_end = grid[-1]

        ax = axes([-5, 5, 1], [-2, 2, 1], 11.0, 4.4, ticks=False).move_to([0, 0.75, 0])
        ax.x_axis.set_opacity(0)
        ax.y_axis.set_opacity(0)

        def to_screen(p):
            return ax.c2p(p[0], p[1])

        # B out of the page; the circle grows with |B| (B = 1 + y/L).
        marks = VGroup()
        for x in np.arange(-4.5, 4.6, 1.5):
            for y in np.arange(-1.6, 1.7, 0.8):
                b = 1 + y / GRAD_B_L
                marks.add(VGroup(Circle(radius=0.12 * b, color=B_FIELD, stroke_width=1.5),
                                 Dot(radius=0.033 * b, color=B_FIELD)).move_to(to_screen([x, y])))
        marks.set_opacity(0.6)
        grad_arrow = Arrow(ax.c2p(-4.9, -1.5), ax.c2p(-4.9, 1.2), buff=0, color=INK, stroke_width=3,
                           max_tip_length_to_length_ratio=0.12)
        grad_lab = math(r"\nabla B", color=INK, size=MATH_SIZE).next_to(grad_arrow, RIGHT, buff=0.08)
        b_lab = math(r"\mathbf{B}\ \odot", color=B_FIELD, size=MATH_SIZE).move_to(ax.c2p(-4.2, 1.85))

        tracker = ValueTracker(0.0)          # fraction of the run

        def index():
            return min(int(tracker.get_value() * (GRID - 1)), GRID - 1)

        def path(xs, color, width, step, opacity=1.0):
            def make():
                i = index()
                if i < 2:
                    return VMobject()
                pts = [to_screen(p) for p in xs[:i + 1:step]]
                return VMobject().set_points_as_corners(pts).set_stroke(color, width, opacity)
            return always_redraw(make)

        ion_path = path(ion_x, ION, CURVE_WIDTH - 1.6, 8)
        ele_path = path(ele_x, ELECTRON, 1.1, 2, 0.45)
        ion_dot = always_redraw(lambda: Dot(to_screen(ion_x[index()]), radius=DOT_RADIUS * 1.8, color=ION))
        ele_dot = always_redraw(lambda: Dot(to_screen(ele_x[index()]), radius=DOT_RADIUS * 1.8, color=ELECTRON))
        ion_gc = always_redraw(lambda: VGroup(
            DashedLine(to_screen(ion_c[0]), to_screen(ion_c[index()]), color=INK, stroke_width=THIN_WIDTH,
                       dash_length=0.1) if index() > 3 else VMobject(),
            Dot(to_screen(ion_c[index()]), radius=DOT_RADIUS, color=INK)))
        ele_gc = always_redraw(lambda: VGroup(
            DashedLine(to_screen(ele_c[0]), to_screen(ele_c[index()]), color=INK, stroke_width=THIN_WIDTH,
                       dash_length=0.1) if index() > 3 else VMobject(),
            Dot(to_screen(ele_c[index()]), radius=DOT_RADIUS, color=INK)))

        ion_tag = math(r"\mathrm{ion}\ (q>0)", color=ION, size=MATH_SMALL).move_to(ax.c2p(-1.6, 1.85))
        ele_tag = math(r"\mathrm{electron}\ (q<0)", color=ELECTRON, size=MATH_SMALL).move_to(ax.c2p(3.2, 1.85))

        unit_note = math(r"x/r_{Li},\ y/r_{Li}\ [1];\quad B=B_0\,(1+y/10r_{Li});\quad m_i/m_e=16,\ T_i=T_e",
                         color=MUTED, size=MATH_SMALL).move_to([0, -1.75, 0])
        rows = VGroup(
            math(r"v_{\nabla B,x}/(r_{Li}\Omega_i)\ [1]\quad \mathrm{orbit}\ \mid\ -\mu\,\partial_yB/(qB^2)\ \ (\mathrm{dev.})",
                 color=MUTED, size=MATH_SMALL),
            math(rf"\mathrm{{ion}}\ \ {{{ion[3]:+.4f}}}\ \mid\ {{{ion[4]:+.4f}}}\ \ ({{{100*(ion[3]/ion[4]-1):+.1f}}}\,\%)", color=ION, size=MATH_SMALL),
            math(rf"\mathrm{{electron}}\ \ {{{ele[3]:+.4f}}}\ \mid\ {{{ele[4]:+.4f}}}\ \ ({{{100*(ele[3]/ele[4]-1):+.1f}}}\,\%)",
                 color=ELECTRON, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([0, -2.85, 0])
        clock_label = math(r"\Omega_i t=", color=MUTED, size=MATH_SMALL).move_to([4.7, 3.3, 0])
        clock = DecimalNumber(0.0, num_decimal_places=1, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            m.set_value(tracker.get_value() * t_end)
            m.next_to(clock_label, RIGHT, buff=0.12)

        clock.add_updater(place_clock)
        place_clock(clock)

        self.add(marks, grad_arrow, grad_lab, b_lab, ion_tag, ele_tag, unit_note, rows,
                 clock_label, clock, ion_path, ele_path, ion_gc, ele_gc, ion_dot, ele_dot)
        self.wait(0.5)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(1.5)
