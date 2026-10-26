"""Magnetic mirror: bounce, loss cone and the adiabatic invariant mu.

Model: axisymmetric mirror field with B_z = B_0 [1 + (R_m - 1)(z/L)^2] and
B_r = -(r/2) dB_z/dz (div B = 0), R_m = 4, L = 30 rho_L0, where
rho_L0 = v/omega_c0 is the Larmor radius of the full speed v at B_0.  Six ions of equal speed start on the midplane
z = 0 with pitch angles alpha = 18, 26, 29, 31, 45, 70 degrees; their
orbits are full Boris pushes of the Lorentz force (drift_models.mirror_orbit),
not drawn paths.  At the midplane

    sin^2 alpha_c = B(0)/B(L) = 1/R_m  ->  alpha_c = 30 deg.

Particles with sin^2 alpha < 1/R_m reach the mirror throat z = L and leave
(open circle at the throat); the others reflect where B = B_0/sin^2 alpha,
z_b = L sqrt((1/sin^2 alpha - 1)/(R_m - 1)).  The inset shows
mu = m_alpha v_perp^2/(2B) (about the local field direction) divided by its starting
value (first full gyro-period average): constant to 0.3 % for the
reflected ions, 1.6 % for the escaping ones.  Axes are
z/L [1], x/L [1] at equal scale, time v t/L [1].
"""

from manim import *
import numpy as np

from drift_models import (
    MIRROR_L, MIRROR_RATIO, PITCH_DEG, loss_cone_angle, mirror_field, mirror_orbit,
)
from style import (
    B_FIELD, CURVE_WIDTH, DOT_RADIUS, FAINT, INK, ION, LINEAR,
    MATH_SMALL, MUTED, THIN_WIDTH, StyledScene, axes, math,
)

LANES = (-2.0, -1.2, -0.4, 0.4, 1.2, 2.0)       # guiding-centre x at z = 0 (L = 10)
T_END = 60.0                                      # run time [L/v = 10], v = 1
PLAY_TIME = 22.0
N_GRID = 3000


def run_all():
    """All orbits resampled onto a common time grid; fixed-length arrays."""
    grid = np.linspace(0, T_END, N_GRID)
    out = []
    for alpha, x_gc in zip(PITCH_DEG, LANES):
        t, x, _, mu, lost = mirror_orbit(alpha, x_gc, t_end=T_END)
        pos = np.array([np.interp(grid, t, x[:, k]) for k in range(3)]).T
        m = np.interp(grid, t, mu)
        n_valid = int(np.searchsorted(grid, t[-1], side="right"))
        out.append({"alpha": alpha, "pos": pos, "mu": m, "lost": lost, "n": n_valid})
    return grid, out


class MagneticMirror(StyledScene):
    def build(self):
        grid, runs = run_all()
        length = MIRROR_L
        zr = 1.3
        ax_w = 12.0
        ax = axes([-zr, zr, 0.5], [-0.3, 0.3, 0.1], ax_w, 0.6 * ax_w / (2 * zr), ticks=False).move_to([0, 1.85, 0])
        ax.x_axis.set_opacity(0)
        ax.y_axis.set_opacity(0)

        def to_screen(p):
            return ax.c2p(p[2] / length, p[0] / length)

        frame = Rectangle(width=ax.x_length, height=ax.y_length, color=MUTED, stroke_width=1.4
                          ).move_to(ax.get_center())
        # Field lines: flux conservation x^2 B_z(z) = const; one per lane.
        lines = VGroup()
        zz = np.linspace(-1.0, 1.0, 80)
        for x_gc in LANES:
            bz = 1 + (MIRROR_RATIO - 1) * zz**2
            pts = [ax.c2p(z, x_gc / length / np.sqrt(b)) for z, b in zip(zz, bz)]
            lines.add(VMobject().set_points_as_corners(pts).set_stroke(FAINT, 1.2, 0.6))
        coils = VGroup(*[Line(ax.c2p(s, -0.27), ax.c2p(s, 0.27), color=B_FIELD, stroke_width=7)
                         for s in (-1.0, 1.0)])
        z_ticks = VGroup(*[
            VGroup(Line(ax.c2p(v, -0.3), ax.c2p(v, -0.27), color=MUTED, stroke_width=1.6),
                   math(f"{v:g}", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, -0.3), DOWN, buff=0.08))
            for v in (-1, -0.5, 0, 0.5, 1)])
        z_lab = math(r"z/L\ [1]", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(0.77, -0.3), DOWN, buff=0.08)
        x_ticks = VGroup(*[
            VGroup(Line(ax.c2p(-zr, v), ax.c2p(-zr + 0.03, v), color=MUTED, stroke_width=1.6),
                   math(f"{v:g}".replace("-", "{-}"), color=MUTED, size=MATH_SMALL).move_to(ax.c2p(-1.15, v)))
            for v in (-0.2, 0, 0.2)])
        x_lab = math(r"x/L\ [1]", color=MUTED, size=MATH_SMALL).next_to(frame, UP, buff=0.1).align_to(frame, LEFT)

        # B(z)/B0 profile, bottom left.
        prof = axes([-1.0, 1.0, 0.5], [0, 4.4, 1], 5.6, 1.7, ticks=False).move_to([-3.4, -2.1, 0])
        prof.x_axis.set_opacity(0)
        prof.y_axis.set_opacity(0)
        prof_curve = prof.plot(lambda z: 1 + (MIRROR_RATIO - 1) * z**2, x_range=[-1, 1, 0.02],
                               color=B_FIELD, stroke_width=CURVE_WIDTH - 1)
        prof_frame = Rectangle(width=prof.x_length, height=prof.y_length, color=MUTED, stroke_width=1.4
                               ).move_to(prof.get_center())
        prof_y = VGroup(*[
            VGroup(Line(prof.c2p(-1.0, v), prof.c2p(-0.95, v), color=MUTED, stroke_width=1.6),
                   math(f"{v}", color=MUTED, size=MATH_SMALL).next_to(prof.c2p(-1.0, v), LEFT, buff=0.1))
            for v in (1, 4)])
        prof_x = VGroup(*[
            math(f"{v:g}", color=MUTED, size=MATH_SMALL).next_to(prof.c2p(v, 0), DOWN, buff=0.1)
            for v in (-1, 0, 1)])
        prof_lab = math(r"B/B_0\ [1]\ \mathrm{vs}\ z/L\ [1]", color=B_FIELD, size=MATH_SMALL).next_to(prof_frame, UP, buff=0.1)
        rm_mark = DashedLine(prof.c2p(-1.0, MIRROR_RATIO), prof.c2p(1.0, MIRROR_RATIO), color=MUTED,
                             stroke_width=THIN_WIDTH, dash_length=0.1)
        rm_lab = math(r"R_m=4,\ L=30\,\rho_{L0}", color=MUTED, size=MATH_SMALL).move_to(prof.c2p(0, 2.9))

        tracker = ValueTracker(0.0)

        def index():
            return min(int(tracker.get_value() * (N_GRID - 1)), N_GRID - 1)

        # Particle colours: trapped = ION colour, lost = same colour but hollow marker at the end.
        paths, dots = [], []
        for k, run in enumerate(runs):
            def make_path(run=run):
                def make():
                    i = min(index(), run["n"] - 1)
                    if i < 2:
                        return VMobject()
                    pts = [to_screen(q) for q in run["pos"][:i + 1:2]]
                    return VMobject().set_points_as_corners(pts).set_stroke(
                        ION, 1.7 if not run["lost"] else 1.7, 0.9 if not run["lost"] else 0.6)
                return always_redraw(make)

            def make_dot(run=run):
                def make():
                    i = min(index(), run["n"] - 1)
                    gone = run["lost"] and index() >= run["n"] - 1
                    if gone:
                        return Circle(radius=DOT_RADIUS * 1.5, color=ION, stroke_width=2.2
                                      ).move_to(to_screen(run["pos"][i]))
                    return Dot(to_screen(run["pos"][i]), radius=DOT_RADIUS * 1.6, color=ION)
                return always_redraw(make)

            paths.append(make_path())
            dots.append(make_dot())

        lane_labels = VGroup()
        for run, x_gc in zip(runs, LANES):
            lane_labels.add(math(rf"{run['alpha']:g}^\circ", color=INK, size=MATH_SMALL).move_to(
                ax.c2p(1.17, x_gc / length)))

        # mu inset, bottom right.
        inset = axes([0, T_END, 20], [0.9, 1.1, 0.1], 5.0, 1.7, ticks=False).move_to([3.9, -2.1, 0])
        inset.x_axis.set_opacity(0)
        inset.y_axis.set_opacity(0)
        inset_frame = Rectangle(width=inset.x_length, height=inset.y_length, color=MUTED, stroke_width=1.4
                                ).move_to(inset.get_center())
        inset_title = math(r"\mu/\mu_{\mathrm{start}}\ [1]\ \mathrm{vs}\ vt/L\ [1]", color=MUTED,
                           size=MATH_SMALL).next_to(inset_frame, UP, buff=0.1)
        inset_ticks = VGroup(*[
            VGroup(Line(inset.c2p(0, v), inset.c2p(1.5, v), color=MUTED, stroke_width=1.6),
                   math(f"{v:.1f}", color=MUTED, size=MATH_SMALL).next_to(inset.c2p(0, v), LEFT, buff=0.1))
            for v in (0.9, 1.0, 1.1)])
        inset_xt = VGroup(*[
            math(f"{v:g}", color=MUTED, size=MATH_SMALL).next_to(inset.c2p(v * length, 0.9), DOWN, buff=0.1)
            for v in (0, 3, 6)])
        ref = DashedLine(inset.c2p(0, 1.0), inset.c2p(T_END, 1.0), color=FAINT, stroke_width=1.4, dash_length=0.08)

        def mu_curve(run):
            def make():
                i = min(index(), run["n"] - 1)
                if i < 2:
                    return VMobject()
                pts = [inset.c2p(grid[j], min(max(run["mu"][j], 0.9), 1.1)) for j in range(0, i + 1, 3)]
                return VMobject().set_points_as_corners(pts).set_stroke(ION, 1.8, 0.85)
            return always_redraw(make)

        mu_curves = [mu_curve(r) for r in runs]

        a_c = loss_cone_angle()
        key_dot = Dot(radius=DOT_RADIUS * 1.6, color=ION)
        key_ring = Circle(radius=DOT_RADIUS * 1.5, color=ION, stroke_width=2.4)
        rule = VGroup(
            math(rf"\sin^2\alpha_c=1/R_m\ \Rightarrow\ \alpha_c={a_c:.0f}^\circ", color=INK, size=MATH_SMALL),
            key_dot, math(r"\mathrm{reflected}", color=MUTED, size=MATH_SMALL),
            key_ring, math(r"\mathrm{lost\ at\ throat}", color=MUTED, size=MATH_SMALL),
        ).arrange(RIGHT, buff=0.3).move_to([-0.3, -0.32, 0])
        lane_note = math(r"\alpha:\ \mathrm{midplane\ pitch\ angle}", color=MUTED, size=MATH_SMALL)
        lane_note.next_to(frame, UP, buff=0.1).align_to(frame, RIGHT)

        self.add(lines, frame, coils, z_ticks, z_lab, x_lab, x_ticks, lane_note, lane_labels, prof_frame, prof_curve,
                 prof_y, prof_x, prof_lab, rm_mark, rm_lab, inset_frame, inset_title, inset_ticks,
                 inset_xt, ref, rule, *mu_curves, *paths, *dots)
        self.wait(0.5)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(1.5)
