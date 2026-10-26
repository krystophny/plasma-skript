"""Gravity drift: ions and electrons drift in opposite directions.

Model: uniform B = B e_z (out of the page) and gravity g = -g e_y, no E.
Ion and electron with |q_alpha| = 1 at equal temperature and the reduced mass
ratio m_i/m_e = 16 of the gyration scenes (v_perp,e = 4 v_perp,i,
rho_Le = rho_Li/4).  Normalized with the ion: lengths in rho_Li [1], time
omega_ci t [1], g = 0.2 rho_Li omega_ci^2.  The orbits are Boris pushes of
dv/dt = g + (q_alpha/m_alpha) v x B (drift_models.gravity_orbit), started with
their guiding centres at the origin.  The force m_alpha g does not depend on
the charge, so the drift

    v_D = (m_alpha/q_alpha) g x B/B^2

is opposite for the two signs of q_alpha and proportional to m_alpha: the ion
drifts to -x, the electron 16 times slower to +x.  The measured drift is the
slope of the gyro-period average of the orbit.
"""

from manim import *
import numpy as np

from drift_models import GRAVITY_G, QM_ELECTRON, QM_ION, averaged_drift, gravity_formula, gravity_orbit
from style import (
    B_FIELD, CURVE_WIDTH, DOT_RADIUS, ELECTRON, INK, ION, LINEAR, MATH_SIZE, MATH_SMALL,
    MUTED, THIN_WIDTH, StyledScene, axes, math,
)

ION_TURNS = 6
T_END = ION_TURNS * 2 * np.pi
GRID = 6000
PLAY_TIME = 12.0
ROWS = {"ion": 1.15, "electron": -1.25}      # y offset of each species on screen [rho_Li]


def run_species(qm, v_perp):
    t, x, _ = gravity_orbit(qm, v_perp, T_END)
    measured = averaged_drift(t, x, 2 * np.pi / abs(qm))[0]
    grid = np.linspace(0, t[-1], GRID)
    pos = np.array([np.interp(grid, t, x[:, k]) for k in range(2)]).T
    return grid, pos, measured, gravity_formula(qm)


class GravityDrift(StyledScene):
    """Ion and electron in uniform B with g perpendicular to B."""

    def build(self):
        grid, ion, ion_meas, ion_form = run_species(QM_ION, 1.0)
        _, ele, ele_meas, ele_form = run_species(QM_ELECTRON, 4.0)

        ax = axes([-8.6, 2.0, 1], [-2.0, 2.4, 1], 11.66, 4.84, ticks=False).move_to([0.2, 0.85, 0])
        ax.x_axis.set_opacity(0)
        ax.y_axis.set_opacity(0)

        def to_screen(p, row):
            return ax.c2p(p[0], p[1] + ROWS[row])

        marks = VGroup()
        for x in np.arange(-8.0, 1.6, 1.6):
            for y in (-0.05,):
                marks.add(VGroup(Circle(radius=0.09, color=B_FIELD, stroke_width=1.5),
                                 Dot(radius=0.025, color=B_FIELD)).move_to(ax.c2p(x, y)))
        marks.set_opacity(0.55)
        b_key = VGroup(VGroup(Circle(radius=0.11, color=B_FIELD, stroke_width=2.0),
                              Dot(radius=0.03, color=B_FIELD)),
                       math(r"\mathbf{B}", color=B_FIELD, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)
        b_key.move_to([-5.8, 3.35, 0])
        g_arrow = Arrow(ax.c2p(1.6, 1.4), ax.c2p(1.6, -0.6), buff=0, color=INK, stroke_width=4,
                        max_tip_length_to_length_ratio=0.15)
        g_lab = math(r"\mathbf{g}", color=INK, size=MATH_SIZE).next_to(g_arrow, RIGHT, buff=0.12)

        ion_tag = math(r"\mathrm{ion}\ \leftarrow", color=ION, size=MATH_SMALL).move_to([-3.2, 3.35, 0])
        ele_tag = math(r"\mathrm{electron}\ \rightarrow", color=ELECTRON, size=MATH_SMALL).next_to(ax.c2p(0.75, ROWS["electron"]), RIGHT, buff=0.15)

        rows = VGroup(
            math(r"v_{D,x}/(\rho_{Li}\omega_{ci})\ [1]\quad \mathrm{orbit}\ \mid\ (m_\alpha/q_\alpha)(\mathbf{g}\times\mathbf{B})_x/B^2",
                 color=MUTED, size=MATH_SMALL),
            math(rf"\mathrm{{ion}}\ \ {{{ion_meas:+.5f}}}\ \mid\ {{{ion_form:+.5f}}}", color=ION, size=MATH_SMALL),
            math(rf"\mathrm{{electron}}\ \ {{{ele_meas:+.5f}}}\ \mid\ {{{ele_form:+.5f}}}", color=ELECTRON, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rows.next_to([-6.45, -2.95, 0], RIGHT, buff=0)
        note = VGroup(
            math(r"m_i/m_e=16\ (\mathrm{H}{:}\ 1836),\ T_i=T_e", color=MUTED, size=MATH_SMALL),
            math(rf"g={GRAVITY_G:g}\,\rho_{{Li}}\omega_{{ci}}^2;\ x/\rho_{{Li}}\ [1]", color=MUTED, size=MATH_SMALL),
        )
        note[0].move_to([0.8, 3.35, 0])
        note[1].next_to([2.4, -2.6, 0], RIGHT, buff=0)

        clock_label = math(r"\omega_{ci}t=", color=MUTED, size=MATH_SMALL).move_to([4.6, 3.35, 0])
        clock = DecimalNumber(0.0, num_decimal_places=1, color=INK, font_size=MATH_SMALL)
        tracker = ValueTracker(0.0)

        def index():
            return min(int(tracker.get_value() * (GRID - 1)), GRID - 1)

        def place_clock(m):
            m.set_value(grid[index()])
            m.next_to(clock_label, RIGHT, buff=0.12)

        clock.add_updater(place_clock)
        place_clock(clock)

        def path(p, row, color, width, step, opacity):
            def make():
                i = index()
                if i < 2:
                    return VMobject()
                pts = [to_screen(q, row) for q in p[:i + 1:step]]
                return VMobject().set_points_as_corners(pts).set_stroke(color, width, opacity)
            return always_redraw(make)

        start_ion = Dot(to_screen((0, 0), "ion"), radius=0.045, color=MUTED)
        start_ele = Dot(to_screen((0, 0), "electron"), radius=0.045, color=MUTED)
        ion_path = path(ion, "ion", ION, CURVE_WIDTH - 1.6, 3, 1.0)
        ele_path = path(ele, "electron", ELECTRON, 1.0, 1, 0.5)
        ion_dot = always_redraw(lambda: Dot(to_screen(ion[index()], "ion"), radius=DOT_RADIUS * 1.8, color=ION))
        ele_dot = always_redraw(lambda: Dot(to_screen(ele[index()], "electron"), radius=DOT_RADIUS * 1.8, color=ELECTRON))
        ticks = VGroup(*[
            VGroup(Line(ax.c2p(v, -1.75), ax.c2p(v, -1.6), color=MUTED, stroke_width=1.6),
                   math(f"{v:d}".replace("-", "{-}"), color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, -1.75), DOWN, buff=0.08))
            for v in (-8, -6, -4, -2, 0)])
        base = Line(ax.c2p(-8.6, -1.6), ax.c2p(1.0, -1.6), color=MUTED, stroke_width=1.4)

        self.add(marks, b_key, g_arrow, g_lab, ion_tag, ele_tag, rows, note, clock_label, clock,
                 start_ion, start_ele, base, ticks, ion_path, ele_path, ion_dot, ele_dot)
        self.wait(0.5)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(1.5)
