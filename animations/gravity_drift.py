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
drifts to -x, the electron 16 times slower to +x.  On screen only the field
keys, species labels, the x axis, the drift formula and the clock; the drift of
the orbits against the formula is checked in scripts/check-physics.py, not
shown.
"""

from manim import *
import numpy as np

from drift_models import QM_ELECTRON, QM_ION, gravity_orbit
from style import (
    B_FIELD, CURVE_WIDTH, DOT_RADIUS, ELECTRON, INK, ION, LINEAR, MATH_SIZE, MATH_SMALL,
    MUTED, StyledScene, axes, math,
)

ION_TURNS = 6
T_END = ION_TURNS * 2 * np.pi
GRID = 6000
PLAY_TIME = 12.0
ROWS = {"ion": 1.3, "electron": -1.1}       # y offset of each species on screen [rho_Li]
X_LO, X_HI = -8.7, 1.2                      # x window [rho_Li]
SCALE = 1.2                                 # Manim units per rho_Li, equal on both axes


def run_species(qm, v_perp):
    t, x, _ = gravity_orbit(qm, v_perp, T_END)
    grid = np.linspace(0, t[-1], GRID)
    pos = np.array([np.interp(grid, t, x[:, k]) for k in range(2)]).T
    return grid, pos


class GravityDrift(StyledScene):
    """Ion and electron in uniform B with g perpendicular to B."""

    def build(self):
        grid, ion = run_species(QM_ION, 1.0)
        _, ele = run_species(QM_ELECTRON, 4.0)

        y_lo, y_hi = -1.65, 2.3
        ax = axes([X_LO, X_HI, 1], [y_lo, y_hi, 1], SCALE * (X_HI - X_LO), SCALE * (y_hi - y_lo),
                  ticks=False)
        ax.move_to([-6.55 + ax.width / 2, 0.15, 0])
        ax.x_axis.set_opacity(0)
        ax.y_axis.set_opacity(0)

        def to_screen(p, row):
            return ax.c2p(p[0], p[1] + ROWS[row])

        marks = VGroup()
        for x in np.arange(-8.0, 1.6, 1.6):
            marks.add(VGroup(Circle(radius=0.09, color=B_FIELD, stroke_width=1.5),
                             Dot(radius=0.025, color=B_FIELD)).move_to(ax.c2p(x, -0.1)))
        marks.set_opacity(0.55)
        b_key = VGroup(VGroup(Circle(radius=0.11, color=B_FIELD, stroke_width=2.0),
                              Dot(radius=0.03, color=B_FIELD)),
                       math(r"\mathbf{B}", color=B_FIELD, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)
        g_key = VGroup(Arrow(UP * 0.3, DOWN * 0.3, buff=0, color=INK, stroke_width=3,
                             max_tip_length_to_length_ratio=0.25),
                       math(r"\mathbf{g}", color=INK, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)
        keys = VGroup(b_key, g_key).arrange(RIGHT, buff=0.7).move_to([-5.2, 3.35, 0])

        ion_tag = math(r"\mathrm{ion}\ \leftarrow", color=ION, size=MATH_SMALL
                       ).next_to(ax.c2p(1.15, ROWS["ion"]), RIGHT, buff=0)
        ele_tag = math(r"\mathrm{electron}\ \rightarrow", color=ELECTRON, size=MATH_SMALL
                       ).next_to(ax.c2p(-0.45, ROWS["electron"]), LEFT, buff=0)

        formula = math(r"\mathbf{v}_D=(m_\alpha/q_\alpha)\,(\mathbf{g}\times\mathbf{B})/B^2",
                       color=INK, size=MATH_SIZE).move_to([0, -3.45, 0])

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
            VGroup(Line(ax.c2p(v, y_lo - 0.12), ax.c2p(v, y_lo), color=MUTED, stroke_width=1.6),
                   math(f"{v:d}".replace("-", "{-}"), color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, y_lo - 0.12), DOWN, buff=0.08))
            for v in (-8, -6, -4, -2, 0)])
        base = Line(ax.c2p(X_LO, y_lo), ax.c2p(1.0, y_lo), color=MUTED, stroke_width=1.4)
        x_lab = math(r"x/\rho_{Li}\ [1]", color=MUTED, size=MATH_SMALL)
        x_lab.next_to(ticks[-1][1], RIGHT, buff=0.45)

        self.add(marks, keys, ion_tag, ele_tag, formula, clock_label, clock,
                 start_ion, start_ele, base, ticks, x_lab, ion_path, ele_path, ion_dot, ele_dot)
        self.wait(0.5)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(1.5)
