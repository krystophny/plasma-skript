"""Curvature plus grad-B drift in a toroidal vacuum field, B = B_0 R_0/R e_phi.

Model: ion and electron (m_i/m_e = 16, T_i = T_e, charge +/-1; the
gyration-scene conventions) start on the midplane at R = R_0 = 40 rho_Li with
v_par = v_perp (drift_models.torus_orbit, full Boris push of the Lorentz
force in Cartesian coordinates, E = 0).  The field lines are circles about
the machine axis, so each guiding centre feels the centrifugal force
m_alpha v_par^2/R (curvature drift) and the gradient force -mu grad B; both point
along Z and add up:

    v_Z = (m_alpha/(q_alpha B R)) (v_par^2 + v_perp^2/2),  B R = B_0 R_0 = const.

The sign of q_alpha fixes the direction: ions drift up, electrons down, the charge
separation that a purely toroidal field cannot hold.  The view is the
poloidal plane (R, Z) in units of rho_Li [1]; the particles move around the
torus (out of the plane) at v_par, which is why the clock shows the
toroidal angle phi [1] reached by the ion.  The measured value is the slope
of the guiding-centre Z(t).
"""

from manim import *
import numpy as np

from drift_models import (
    QM_ELECTRON, QM_ION, TORUS_R0, drift_speed, torus_formula, torus_orbit,
)
from style import (
    B_FIELD, CURVE_WIDTH, DOT_RADIUS, ELECTRON, INK, ION, LINEAR, MATH_SIZE, MATH_SMALL,
    MUTED, THIN_WIDTH, StyledScene, axes, math,
)

V_PERP = {"ion": 1.0, "electron": 4.0}    # equal temperature
V_PAR = {"ion": 1.0, "electron": 4.0}     # v_par = v_perp
TURNS = 0.5                               # torus fraction the ion travels
T_RUN = TURNS * 2 * np.pi * TORUS_R0 / 1.0   # both species run for the same time
GRID = 6000
PLAY_TIME = 18.0


def run_species(qm, v_par, v_perp):
    t, x, _, centre = torus_orbit(qm, v_par, v_perp, T_RUN)
    measured = drift_speed(t, centre)[2]
    return t, x, centre, measured, torus_formula(qm, v_par, v_perp)


def poloidal(x):
    """(R, Z) of Cartesian positions (n, 3)."""
    return np.stack([np.hypot(x[:, 0], x[:, 1]), x[:, 2]], axis=1)


def on_grid(t, a, n=GRID):
    grid = np.linspace(0, t[-1], n)
    return grid, np.array([np.interp(grid, t, a[:, k]) for k in range(a.shape[1])]).T


class CurvatureDrift(StyledScene):
    """Poloidal view of ion and electron orbits in B proportional to 1/R."""

    def build(self):
        ion = run_species(QM_ION, V_PAR["ion"], V_PERP["ion"])
        ele = run_species(QM_ELECTRON, V_PAR["electron"], V_PERP["electron"])
        grid, ion_p = on_grid(ion[0], poloidal(ion[1]))
        _, ele_p = on_grid(ele[0], poloidal(ele[1]))
        _, ion_c = on_grid(ion[0], poloidal(ion[2]))
        _, ele_c = on_grid(ele[0], poloidal(ele[2]))
        _, ion_phi = on_grid(ion[0], np.arctan2(ion[1][:, 1], ion[1][:, 0])[:, None])
        t_end = grid[-1]

        # R - R_0 in [-4, 4], Z in [-6, 6] at equal scale (0.5 u per rho_Li).
        scale = 0.5
        ax = axes([-4, 4, 1], [-6, 6, 1], 8 * scale, 12 * scale, ticks=False)
        ax.move_to([-4.2, 0.1, 0])
        ax.x_axis.set_opacity(0)
        ax.y_axis.set_opacity(0)

        def to_screen(p):
            return ax.c2p(p[0] - TORUS_R0, p[1])

        # B along +phi, out of the page: dot-in-circle, size ~ B ~ 1/R.
        marks = VGroup()
        for dr in np.arange(-3.0, 3.1, 1.5):
            for z in np.arange(-5.0, 5.1, 2.5):
                b = TORUS_R0 / (TORUS_R0 + dr)
                marks.add(VGroup(Circle(radius=0.1 * b, color=B_FIELD, stroke_width=1.4),
                                 Dot(radius=0.028 * b, color=B_FIELD)).move_to(ax.c2p(dr, z)))
        marks.set_opacity(0.55)
        r_lab = math(r"(R-R_0)/\rho_{Li}\ [1]", color=MUTED, size=MATH_SMALL).next_to(ax, DOWN, buff=0.2)
        z_ticks = VGroup(*[
            VGroup(Line(ax.c2p(-4, v), ax.c2p(-3.85, v), color=MUTED, stroke_width=1.6),
                   math(f"{v:d}", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(-4, v), LEFT, buff=0.12))
            for v in (-4, -2, 0, 2, 4)])
        r_ticks = VGroup(*[
            VGroup(Line(ax.c2p(v, -6), ax.c2p(v, -5.8), color=MUTED, stroke_width=1.6),
                   math(f"{v:d}", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, -6), DOWN, buff=0.1))
            for v in (-2, 0, 2)])
        frame = Rectangle(width=ax.x_length, height=ax.y_length, color=MUTED, stroke_width=1.4
                          ).move_to(ax.get_center())
        z_lab = math(r"Z/\rho_{Li}\ [1]", color=MUTED, size=MATH_SMALL).next_to(frame, UP, buff=0.12)
        r_lab.next_to(frame, DOWN, buff=0.45)
        torus_axis = DashedLine(ax.c2p(-4, -6), ax.c2p(-4, 6), color=MUTED, stroke_width=THIN_WIDTH, dash_length=0.1)
        b_key = VGroup(VGroup(Circle(radius=0.11, color=B_FIELD, stroke_width=2.0),
                              Dot(radius=0.03, color=B_FIELD)),
                       math(r"\mathbf{B}=B_0\frac{R_0}{R}\mathbf{e}_\varphi", color=B_FIELD, size=MATH_SMALL)
                       ).arrange(RIGHT, buff=0.15).move_to([4.6, 3.05, 0])

        tracker = ValueTracker(0.0)

        def index():
            return min(int(tracker.get_value() * (GRID - 1)), GRID - 1)

        def path(p, color, width, step, opacity):
            def make():
                i = index()
                if i < 2:
                    return VMobject()
                pts = [to_screen(q) for q in p[:i + 1:step]]
                return VMobject().set_points_as_corners(pts).set_stroke(color, width, opacity)
            return always_redraw(make)

        ion_path = path(ion_p, ION, 2.6, 6, 1.0)
        ele_path = path(ele_p, ELECTRON, 0.8, 2, 0.35)
        ion_dot = always_redraw(lambda: Dot(to_screen(ion_p[index()]), radius=DOT_RADIUS * 1.8, color=ION))
        ele_dot = always_redraw(lambda: Dot(to_screen(ele_p[index()]), radius=DOT_RADIUS * 1.8, color=ELECTRON))
        ion_gc = always_redraw(lambda: Dot(to_screen(ion_c[index()]), radius=DOT_RADIUS, color=INK))
        ele_gc = always_redraw(lambda: Dot(to_screen(ele_c[index()]), radius=DOT_RADIUS, color=INK))

        ion_tag = math(r"\mathrm{ion}\ \uparrow", color=ION, size=MATH_SMALL)
        ion_tag.next_to(ax.c2p(4, 4.6), RIGHT, buff=0.3)
        ele_tag = math(r"\mathrm{electron}\ \downarrow", color=ELECTRON, size=MATH_SMALL)
        ele_tag.next_to(ax.c2p(4, -4.6), RIGHT, buff=0.3)

        # Electron turns 4x faster around the torus (v_par,e = 4 v_par,i): same time, 1 turn.
        rows = VGroup(
            math(r"v_{D,Z}/(\rho_{Li}\omega_{ci})\ [1]\ \ \mathrm{orbit}\mid\tfrac{m_\alpha}{q_\alpha BR}(v_\parallel^2+\tfrac12 v_\perp^2)\ (\mathrm{dev.})",
                 color=MUTED, size=MATH_SMALL),
            math(rf"\mathrm{{ion}}\ \ {{{ion[3]:+.4f}}}\ \mid\ {{{ion[4]:+.4f}}}\ \ ({{{100*(ion[3]/ion[4]-1):+.1f}}}\,\%)", color=ION, size=MATH_SMALL),
            math(rf"\mathrm{{electron}}\ \ {{{ele[3]:+.4f}}}\ \mid\ {{{ele[4]:+.4f}}}\ \ ({{{100*(ele[3]/ele[4]-1):+.1f}}}\,\%)", color=ELECTRON, size=MATH_SMALL),
            math(rf"R_0={TORUS_R0:g}\,\rho_{{Li}},\ v_\parallel=v_\perp,\ m_i/m_e=16,\ T_i=T_e",
                 color=MUTED, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([2.6, -0.35, 0])
        clock_label = math(r"\varphi_{\mathrm{ion}}=", color=MUTED, size=MATH_SMALL)
        clock_label.next_to(ax.c2p(4, 2.6), RIGHT, buff=0.3)
        clock = DecimalNumber(0.0, num_decimal_places=2, color=INK, font_size=MATH_SMALL)
        unit = math(r"\ [1]", color=MUTED, size=MATH_SMALL)

        def place_clock(m):
            m.set_value(abs(ion_phi[index()][0]))
            m.next_to(clock_label, RIGHT, buff=0.12)
            unit.next_to(m, RIGHT, buff=0.18)

        clock.add_updater(place_clock)
        place_clock(clock)

        self.add(marks, frame, z_ticks, r_ticks, r_lab, z_lab, b_key, ion_tag, ele_tag, rows,
                 clock_label, clock, unit, ion_path, ele_path, ion_gc, ele_gc, ion_dot, ele_dot)
        self.wait(0.5)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(1.5)
