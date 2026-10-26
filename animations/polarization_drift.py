"""Polarization drift: the guiding centre shifts along E while E grows.

Model: uniform B = B e_z (out of the page) and E = E(t) e_y switched on
smoothly, E/B = (E_1/B)(1 - cos(pi t/T_r))/2 for 0 <= t <= T_r, then constant;
E_1/B = 0.75 v_perp,i, T_r = three ion gyroperiods (omega/omega_ci ~ 0.17).
Ion and electron with |q_alpha| = 1 at equal temperature and the reduced mass
ratio m_i/m_e = 16 of the gyration scenes.  Normalized with the ion: lengths
rho_Li [1], time omega_ci t [1].  The orbits are Boris pushes of
dv/dt = (q_alpha/m_alpha)(E(t) + v x B) (drift_models.pol_orbit).

Both species E x B drift along +x at the same speed E(t)/B; the view
subtracts that common displacement x_D(t) = integral of E/B dt.  What remains
is the polarization drift v_D^pol = (m_alpha/(q_alpha B^2)) dE/dt along E:
the guiding centre R = x + (m_alpha/q_alpha)(v - v_D) x B/B^2 moves by
(m_alpha/(q_alpha B^2)) E_1, up for the ion, 16 times less and down for the
electron.  The lower panel compares R_y(t) with (m_alpha/(q_alpha B^2)) E(t).
"""

from manim import *
import numpy as np

from drift_models import (
    POL_E1, POL_RAMP, QM_ELECTRON, QM_ION, pol_e, pol_exb_shift, pol_formula, pol_orbit,
)
from style import (
    B_FIELD, CURVE_WIDTH, DOT_RADIUS, E_FIELD, ELECTRON, FAINT, GRID as GRID_COLOR, INK, ION,
    LINEAR, MATH_SIZE, MATH_SMALL, MUTED, THIN_WIDTH, StyledScene, axes, dashed, math,
)

N_GRID = 5000
PLAY_TIME = 15.0
OFFSET = {"ion": -1.9, "electron": 1.9}       # screen x offset of each species [rho_Li]


def run_species(qm, v_perp):
    t, x, centre = pol_orbit(qm, v_perp)
    grid = np.linspace(0, t[-1], N_GRID)
    shift = pol_exb_shift(grid)
    pos = np.array([np.interp(grid, t, x[:, k]) for k in range(2)]).T
    gc = np.array([np.interp(grid, t, centre[:, k]) for k in range(2)]).T
    pos[:, 0] -= shift
    gc[:, 0] -= shift
    after = t >= POL_RAMP                     # the last two ion turns, E constant
    measured = centre[after, 1].mean()        # started on the circle about the origin
    return grid, pos, gc, measured, pol_formula(qm, t[-1])


class PolarizationDrift(StyledScene):
    """Ion and electron while E_perp grows: guiding centres shift along +/-E."""

    def build(self):
        grid, ion, ion_gc, ion_meas, ion_form = run_species(QM_ION, 1.0)
        _, ele, ele_gc, ele_meas, ele_form = run_species(QM_ELECTRON, 4.0)
        t_end = grid[-1]

        # Upper panel: the orbits, E x B displacement removed, equal scale.
        unit = 0.92
        top = axes([-3.6, 3.6, 1], [-1.3, 2.0, 1], 7.2 * unit, 3.3 * unit, ticks=False).move_to([-2.4, 1.4, 0])
        top.x_axis.set_opacity(0)
        top.y_axis.set_opacity(0)

        def to_screen(p, sp):
            return top.c2p(p[0] + OFFSET[sp], p[1])

        frame = Rectangle(width=top.x_length, height=top.y_length, color=MUTED, stroke_width=1.2
                          ).move_to(top.get_center())
        zero = DashedLine(top.c2p(-3.6, 0), top.c2p(3.6, 0), color=FAINT, stroke_width=1.2, dash_length=0.08)
        y_ticks = VGroup(*[math(f"{v:d}".replace("-", "{-}"), color=MUTED, size=MATH_SMALL)
                           .next_to(top.c2p(-3.6, v), LEFT, buff=0.12) for v in (-1, 0, 1)])
        y_lab = math(r"y/\rho_{Li}\ [1]", color=MUTED, size=MATH_SMALL).next_to(frame, UP, buff=0.1).align_to(frame, LEFT)
        x_lab = math(r"(x-x_D)/\rho_{Li}\ [1]", color=MUTED, size=MATH_SMALL
                     ).next_to(frame, UP, buff=0.1).align_to(frame, RIGHT)

        b_key = VGroup(VGroup(Circle(radius=0.11, color=B_FIELD, stroke_width=2.0),
                              Dot(radius=0.03, color=B_FIELD)),
                       math(r"\mathbf{B}", color=B_FIELD, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)
        b_key.move_to([3.4, 2.75, 0])

        tracker = ValueTracker(0.0)

        def index():
            return min(int(tracker.get_value() * (N_GRID - 1)), N_GRID - 1)

        e_base = np.array([1.75, 1.0, 0])

        def e_arrow():
            frac = pol_e(grid[index()]) / POL_E1
            if frac < 0.02:
                return VMobject()
            return Arrow(e_base, e_base + UP * 2.0 * frac, buff=0, color=E_FIELD, stroke_width=4,
                         max_tip_length_to_length_ratio=0.15)

        e_vec = always_redraw(e_arrow)
        e_lab = math(r"\mathbf{E}(t)", color=E_FIELD, size=MATH_SIZE).next_to(e_base + UP * 1.0, RIGHT, buff=0.2)

        def path(p, sp, color, width, step, opacity):
            def make():
                i = index()
                if i < 2:
                    return VMobject()
                pts = [to_screen(q, sp) for q in p[:i + 1:step]]
                return VMobject().set_points_as_corners(pts).set_stroke(color, width, opacity)
            return always_redraw(make)

        def gc_dot(gc, sp):
            return always_redraw(lambda: Dot(to_screen(gc[index()], sp), radius=DOT_RADIUS, color=INK))

        ion_path = path(ion, "ion", ION, CURVE_WIDTH - 2.0, 2, 0.8)
        ele_path = path(ele, "electron", ELECTRON, 1.0, 1, 0.5)
        ion_dot = always_redraw(lambda: Dot(to_screen(ion[index()], "ion"), radius=DOT_RADIUS * 1.8, color=ION))
        ele_dot = always_redraw(lambda: Dot(to_screen(ele[index()], "electron"), radius=DOT_RADIUS * 1.8, color=ELECTRON))
        ion_tag = math(r"\mathrm{ion}", color=ION, size=MATH_SMALL).move_to(top.c2p(OFFSET["ion"] - 1.35, -1.0))
        ele_tag = math(r"\mathrm{electron}", color=ELECTRON, size=MATH_SMALL).move_to(top.c2p(OFFSET["electron"], 0.7))

        # Lower panel: guiding-centre R_y against the formula (m/(q B^2)) E(t).
        low = axes([0, t_end, 2 * np.pi], [-0.2, 0.9, 0.25], 7.2 * unit, 1.75, ticks=False).move_to([-2.4, -2.45, 0])
        low_frame = Rectangle(width=low.x_length, height=low.y_length, color=MUTED, stroke_width=1.2
                              ).move_to(low.get_center())
        low.x_axis.set_opacity(0)
        low.y_axis.set_opacity(0)
        low_zero = DashedLine(low.c2p(0, 0), low.c2p(t_end, 0), color=GRID_COLOR, stroke_width=1.0, dash_length=0.06)
        low_y = VGroup(*[math(f"{v:g}", color=MUTED, size=MATH_SMALL).next_to(low.c2p(0, v), LEFT, buff=0.1)
                         for v in (0, 0.5)])
        low_x = VGroup(*[math(tex, color=MUTED, size=MATH_SMALL).next_to(low.c2p(k * 2 * np.pi, -0.2), DOWN, buff=0.08)
                         for k, tex in ((3, r"6\pi"), (5, r"10\pi"))])
        low_lab = math(r"R_y/\rho_{Li}\ [1]", color=MUTED, size=MATH_SMALL
                       ).next_to(low_frame, UP, buff=0.1).align_to(low_frame, LEFT)
        low_xlab = math(r"\omega_{ci}t\ [1]", color=MUTED, size=MATH_SMALL
                        ).next_to(low_frame, UP, buff=0.1).align_to(low_frame, RIGHT)
        ramp_mark = DashedLine(low.c2p(POL_RAMP, -0.2), low.c2p(POL_RAMP, 0.9), color=FAINT,
                               stroke_width=1.0, dash_length=0.06)
        formula_ion = dashed(low.plot(lambda s: pol_formula(QM_ION, s), x_range=[0, t_end, t_end / 200],
                                      color=MUTED, stroke_width=THIN_WIDTH), num_dashes=50)
        formula_ele = dashed(low.plot(lambda s: pol_formula(QM_ELECTRON, s), x_range=[0, t_end, t_end / 200],
                                      color=MUTED, stroke_width=THIN_WIDTH), num_dashes=50)

        def trace(gc, color):
            def make():
                i = index()
                if i < 2:
                    return VMobject()
                pts = [low.c2p(grid[j], gc[j, 1]) for j in range(0, i + 1, 4)]
                return VMobject().set_points_as_corners(pts).set_stroke(color, CURVE_WIDTH - 1.5)
            return always_redraw(make)

        rows = VGroup(
            math(r"\mathbf{v}_D^{\mathrm{pol}}=\tfrac{m_\alpha}{q_\alpha B^2}\tfrac{d\mathbf{E}_\perp}{dt}", color=INK, size=MATH_SMALL),
            math(r"\Delta R_y/\rho_{Li}\ [1]{:}\ \mathrm{orbit}\mid\tfrac{m_\alpha E_1}{q_\alpha B^2}", color=MUTED, size=MATH_SMALL),
            math(rf"\mathrm{{ion}}\ \ {{{ion_meas:+.4f}}}\mid{{{ion_form:+.4f}}}", color=ION, size=MATH_SMALL),
            math(rf"\mathrm{{electron}}\ \ {{{ele_meas:+.4f}}}\mid{{{ele_form:+.4f}}}", color=ELECTRON, size=MATH_SMALL),
            math(r"\mathrm{dashed{:}}\ \tfrac{m_\alpha}{q_\alpha B^2}E(t)", color=MUTED, size=MATH_SMALL),
            math(r"x_D=\textstyle\int_0^t E/B\,dt", color=MUTED, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rows.next_to([1.6, 0.0, 0], RIGHT, buff=0)
        rows.align_to([0, 0.55, 0], UP)
        setup = VGroup(
            math(rf"E_1/B={POL_E1:g}\,v_{{\perp i}}", color=MUTED, size=MATH_SMALL),
            math(r"m_i/m_e=16,\ T_i=T_e", color=MUTED, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        setup.next_to([3.0, 0.0, 0], RIGHT, buff=0).align_to([0, 2.2, 0], UP)

        clock_label = math(r"\omega_{ci}t=", color=MUTED, size=MATH_SMALL).move_to([4.3, 3.45, 0])
        clock = DecimalNumber(0.0, num_decimal_places=1, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            m.set_value(grid[index()])
            m.next_to(clock_label, RIGHT, buff=0.12)

        clock.add_updater(place_clock)
        place_clock(clock)

        self.add(frame, zero, y_ticks, y_lab, x_lab, b_key, e_lab, ion_tag, ele_tag, low_frame, low_zero,
                 low_y, low_x, low_lab, low_xlab, ramp_mark, formula_ion, formula_ele, rows, setup, clock_label, clock,
                 e_vec, ion_path, ele_path, gc_dot(ion_gc, "ion"), gc_dot(ele_gc, "electron"), ion_dot, ele_dot,
                 trace(ion_gc, ION), trace(ele_gc, ELECTRON))
        self.wait(0.5)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(1.5)
