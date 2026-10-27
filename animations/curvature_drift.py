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
toroidal angle phi [1] reached by the ion.  On screen only the field key,
species labels, axes, the drift formula and the clock; the slope of the
guiding-centre Z(t) against the formula is checked in scripts/check-physics.py.

Orientation: (R, phi, Z) is right-handed, e_R x e_phi = e_Z.  With R to the
right and Z up, e_phi = e_Z x e_R points into the page, so B = B_phi e_phi
is drawn as a cross in a circle; e_R x b = e_Z, and the ion drifts up.
"""

from manim import *
import numpy as np

from drift_models import QM_ELECTRON, QM_ION, TORUS_R0, torus_orbit
from style import (
    B_FIELD, DOT_RADIUS, ELECTRON, INK, ION, LINEAR, MATH_SIZE, MATH_SMALL, MUTED,
    StyledScene, axes, math,
)

V_PERP = {"ion": 1.0, "electron": 4.0}    # equal temperature
V_PAR = {"ion": 1.0, "electron": 4.0}     # v_par = v_perp
TURNS = 0.5                               # torus fraction the ion travels
T_RUN = TURNS * 2 * np.pi * TORUS_R0 / 1.0   # both species run for the same time
GRID = 6000
PLAY_TIME = 18.0


def run_species(qm, v_par, v_perp):
    t, x, _, centre = torus_orbit(qm, v_par, v_perp, T_RUN)
    return t, x, centre


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

        # Orbits span |R - R_0| < 1 and -5 < Z < 5.6; equal scale on both axes.
        scale = 0.56
        r_lo, r_hi, z_lo, z_hi = -3.5, 3.5, -5.5, 6.0
        ax = axes([r_lo, r_hi, 1], [z_lo, z_hi, 1], scale * (r_hi - r_lo), scale * (z_hi - z_lo),
                  ticks=False)
        ax.move_to([-1.85, -0.05, 0])
        ax.x_axis.set_opacity(0)
        ax.y_axis.set_opacity(0)

        def to_screen(p):
            return ax.c2p(p[0] - TORUS_R0, p[1])

        def into_page(r, width):
            d = 0.62 * r
            return VGroup(Circle(radius=r, color=B_FIELD, stroke_width=width),
                          Line([-d, -d, 0], [d, d, 0], color=B_FIELD, stroke_width=width),
                          Line([-d, d, 0], [d, -d, 0], color=B_FIELD, stroke_width=width))

        # B along +phi, into the page (R right, Z up): cross in circle, size ~ B ~ 1/R.
        marks = VGroup()
        for dr in np.arange(-3.0, 3.1, 1.5):
            for z in np.arange(-5.0, 5.1, 2.5):
                b = TORUS_R0 / (TORUS_R0 + dr)
                marks.add(into_page(0.1 * b, 1.4).move_to(ax.c2p(dr, z)))
        marks.set_opacity(0.55)
        frame = Rectangle(width=ax.x_length, height=ax.y_length, color=MUTED, stroke_width=1.4
                          ).move_to(ax.get_center())
        z_ticks = VGroup(*[
            VGroup(Line(ax.c2p(r_lo, v), ax.c2p(r_lo + 0.15, v), color=MUTED, stroke_width=1.6),
                   math(f"{v:d}".replace("-", "{-}"), color=MUTED, size=MATH_SMALL
                        ).next_to(ax.c2p(r_lo, v), LEFT, buff=0.12))
            for v in (-4, -2, 0, 2, 4)])
        r_ticks = VGroup(*[
            VGroup(Line(ax.c2p(v, z_lo), ax.c2p(v, z_lo + 0.2), color=MUTED, stroke_width=1.6),
                   math(f"{v:d}".replace("-", "{-}"), color=MUTED, size=MATH_SMALL
                        ).next_to(ax.c2p(v, z_lo), DOWN, buff=0.1))
            for v in (-2, 0, 2)])
        z_lab = math(r"Z/\rho_{Li}\ [1]", color=MUTED, size=MATH_SMALL).next_to(frame, UP, buff=0.12)
        r_lab = math(r"(R-R_0)/\rho_{Li}\ [1]", color=MUTED, size=MATH_SMALL)
        r_lab.next_to(r_ticks[-1][1], RIGHT, buff=0.6)
        b_key = VGroup(into_page(0.11, 2.0),
                       math(r"\mathbf{B}=B_0\frac{R_0}{R}\mathbf{e}_\varphi", color=B_FIELD, size=MATH_SMALL)
                       ).arrange(RIGHT, buff=0.15)
        b_key.move_to([-6.5, 3.3, 0], aligned_edge=LEFT)

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
        ion_tag.next_to(ax.c2p(r_hi, 4.6), RIGHT, buff=0.3)
        ele_tag = math(r"\mathrm{electron}\ \downarrow", color=ELECTRON, size=MATH_SMALL)
        ele_tag.next_to(ax.c2p(r_hi, -4.6), RIGHT, buff=0.3)

        # Vacuum field: R_c = R, curvature and grad-B drift add up.
        formula = math(r"\mathbf{v}_D=\frac{m_\alpha}{q_\alpha BR}\left(v_\parallel^2+\tfrac12 v_\perp^2\right)"
                       r"\mathbf{e}_R\times\mathbf{b}", color=INK, size=MATH_SIZE)
        formula.next_to(ax.c2p(r_hi, 0.25), RIGHT, buff=0.5)
        r_key = math(r"R\ \mathrm{major\ radius}", color=MUTED, size=MATH_SMALL)
        r_key.next_to(formula, DOWN, buff=0.5).align_to(formula, LEFT)
        clock_label = math(r"\varphi_{\mathrm{ion}}=", color=MUTED, size=MATH_SMALL).move_to([3.9, 3.3, 0])
        clock = DecimalNumber(0.0, num_decimal_places=1, color=INK, font_size=MATH_SMALL)
        unit = math(r"\ [1]", color=MUTED, size=MATH_SMALL)

        def place_clock(m):
            m.set_value(abs(ion_phi[index()][0]))
            m.next_to(clock_label, RIGHT, buff=0.12)
            unit.next_to(m, RIGHT, buff=0.18)

        clock.add_updater(place_clock)
        place_clock(clock)

        self.add(marks, frame, z_ticks, r_ticks, r_lab, z_lab, b_key, r_key, ion_tag, ele_tag, formula,
                 clock_label, clock, unit, ion_path, ele_path, ion_gc, ele_gc, ion_dot, ele_dot)
        self.wait(0.5)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(1.5)
