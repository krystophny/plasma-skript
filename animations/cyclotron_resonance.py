"""Cyclotron resonance: a rotating electric field and a gyrating charge.

Model: uniform B = B e_z (out of the page) and a uniform field rotating in the
perpendicular plane, E_x + i E_y = E_0 exp(-i s omega t), with s = +1 for
clockwise and s = -1 for counterclockwise rotation seen from +z.  The
particle starts at rest at the origin; Boris push of
dv/dt = (q_alpha/m_alpha)(E + v x B) (drift_models.boris_em), 400 steps per
gyration.  Each species is normalized with its own gyrofrequency: time
|omega_c| t, speed v B/E_0, lengths (x, y)|omega_c| B/E_0, all [1].  Ions
(omega_c > 0) gyrate clockwise, electrons (omega_c < 0) counterclockwise.

With w = v_x + i v_y the equation is dw/dt = -i omega_c w + (q_alpha/m_alpha) E_0
exp(-i s omega t); from rest

    |w| = (|q_alpha| E_0/m_alpha) |2 sin(Delta t/2)/Delta|,  Delta = omega_c - s omega.

Resonance Delta = 0 (s omega = omega_c): v_perp = |q_alpha| E_0 t/m_alpha grows
linearly, the energy W = q_alpha^2 E_0^2 t^2/(2 m_alpha) quadratically.  Off
resonance v_perp beats with period 2 pi/|Delta| and stays below 2|q_alpha|E_0/(m_alpha|Delta|);
the counter-rotating field (Delta = 2 omega_c) gives at most E_0/B.

Runs, one after the other in the same axes: ion, clockwise, omega = omega_ci;
ion, clockwise, omega = 0.8 omega_ci; ion, counterclockwise, omega = omega_ci;
electron, counterclockwise, omega = |omega_ce|.  scripts/check-physics.py
compares every run with the formula above.
"""

from manim import *
import numpy as np

from drift_models import boris_em, uniform_b
from style import (
    ACCENT, CURVE_WIDTH, E_FIELD, ELECTRON, FAINT, INK, ION, LINEAR, MATH_SIZE, MATH_SMALL, MUTED,
    THIN_WIDTH, B_FIELD, StyledScene, axes, dashed, math,
)

CR_STEPS_PER_TURN = 400
CR_TURNS = 6
CR_DETUNED = 0.8           # omega/|omega_c| of the off-resonant run [1]
# (q/m in units of |omega_c|/B, sense s of E, omega/|omega_c|)
CR_RUNS = (
    (1.0, 1, 1.0),
    (1.0, 1, CR_DETUNED),
    (1.0, -1, 1.0),
    (-1.0, -1, 1.0),
)


def cr_orbit(qm, sense, omega, turns=CR_TURNS, steps_per_turn=CR_STEPS_PER_TURN):
    """Boris orbit from rest; E_0 = B = |omega_c| = 1.  Returns t, x (n, 3),
    the speed |v| (n,) at whole steps (mean of the adjacent half steps)."""
    dt = 2 * np.pi / steps_per_turn

    def accel(x, t):
        return qm * np.array([np.cos(omega * t), -sense * np.sin(omega * t), 0.0])

    steps = turns * steps_per_turn
    t, x, v = boris_em(qm, uniform_b(1.0), accel, np.zeros(3), np.zeros(3), dt, steps)
    # v[n] belongs to t = (n - 1/2) dt; average to the whole steps of x.
    return t[:-1], x[:-1], np.linalg.norm(0.5 * (v[:-1] + v[1:]), axis=1)


def cr_speed_formula(t, qm, sense, omega):
    """|w| = |q|E_0/m |2 sin(Delta t/2)/Delta| with E_0 = B = 1."""
    delta = np.sign(qm) - sense * omega
    if abs(delta) < 1e-12:
        return abs(qm) * t
    return abs(qm) * np.abs(2 * np.sin(delta * t / 2) / delta)


def cr_growth_rate(t, speed):
    """Least-squares slope of v_perp(t) [E_0/B per 1/|omega_c|]."""
    return np.polyfit(t, speed, 1)[0]


V_TOP = 40.0


class CyclotronResonance(StyledScene):
    """Rotating E: resonance, detuning, wrong polarization, electron."""

    def build(self):
        runs = [cr_orbit(*r) for r in CR_RUNS]
        t = runs[0][0]
        frames = len(t)
        top = axes([-V_TOP, V_TOP, 20], [-V_TOP, V_TOP, 20], 6.0, 6.0, ticks=False).move_to([-3.75, -0.25, 0])
        top.x_axis.set_opacity(0.35)
        top.y_axis.set_opacity(0.35)
        frame = Square(6.0, color=MUTED, stroke_width=1.4).move_to(top.c2p(0, 0))
        xy_lab = math(r"(x,y)\,|\omega_c|B/E_0\ [1]", color=MUTED, size=MATH_SMALL)
        xy_lab.next_to(frame, DOWN, buff=0.12).align_to(frame, LEFT)
        b_key = VGroup(VGroup(Circle(radius=0.11, color=B_FIELD, stroke_width=2.0), Dot(radius=0.03, color=B_FIELD)),
                       math(r"\mathbf{B}", color=B_FIELD, size=MATH_SIZE)).arrange(RIGHT, buff=0.12)
        b_key.move_to(frame.get_corner(DR) + np.array([-0.55, 0.4, 0]))

        tr = axes([0, t[-1], 10], [0, V_TOP, 10], 5.6, 4.2).move_to([3.75, 0.45, 0])
        tx_ticks = VGroup(*[math(str(v), color=MUTED, size=MATH_SMALL).next_to(tr.c2p(v, 0), DOWN, buff=0.12)
                            for v in (0, 10, 20)])
        ty_ticks = VGroup(*[math(str(v), color=MUTED, size=MATH_SMALL).next_to(tr.c2p(0, v), LEFT, buff=0.12)
                            for v in (0, 20, 40)])
        tx_lab = math(r"|\omega_c|t\ [1]", color=MUTED, size=MATH_SMALL).next_to(tr.c2p(t[-1], 0), DOWN, buff=0.12)
        tx_lab.align_to(tr.c2p(t[-1], 0), RIGHT)
        ty_lab = math(r"v_\perp B/E_0\ [1]", color=MUTED, size=MATH_SMALL).next_to(tr.c2p(0, V_TOP), UP, buff=0.15)
        ty_lab.align_to(tr.c2p(0, 0), LEFT).shift(0.4 * LEFT)
        theory = VGroup(*[
            dashed(tr.plot_line_graph(t[::8], cr_speed_formula(t[::8], *r), add_vertex_dots=False,
                                      line_color=FAINT, stroke_width=THIN_WIDTH)["line_graph"], num_dashes=60)
            for r in CR_RUNS])

        styles = [
            (ION, 1.0, r"\mathrm{ion},\ \mathbf{E}\ \mathrm{clockwise},\ \omega=\omega_{ci}"),
            (ION, 0.75, rf"\mathrm{{ion}},\ \mathbf{{E}}\ \mathrm{{clockwise}},\ \omega={CR_DETUNED:g}\,\omega_{{ci}}"),
            (ION, 0.75, r"\mathrm{ion},\ \mathbf{E}\ \mathrm{counterclockwise},\ \omega=\omega_{ci}"),
            (ELECTRON, 1.0, r"\mathrm{electron},\ \mathbf{E}\ \mathrm{counterclockwise},\ \omega=|\omega_{ce}|"),
        ]
        # Direct labels of the kept traces: (text, colour, anchor in trace coordinates).
        tags = [
            (r"\mathrm{ion\ cw}", ION, (22.0, 29.0)),
            (rf"{CR_DETUNED:g}\,\omega_{{ci}}", ION, (15.5, 12.5)),
            (r"\mathrm{ion\ ccw}", ION, (20.0, 3.3)),
            (r"\mathrm{electron\ ccw}", ELECTRON, (24.5, 19.5)),
        ]
        tracker = ValueTracker(0.0)

        def index():
            return min(int(round(tracker.get_value() * (frames - 1))), frames - 1)

        def orbit_path(run, color):
            def make():
                i = index()
                if i < 2:
                    return VMobject()
                pts = [top.c2p(p[0], p[1]) for p in run[1][:i + 1:2]]
                return VMobject().set_points_as_corners(pts).set_stroke(color, THIN_WIDTH, 0.9)
            return make

        def speed_path(run, color, opacity):
            def make():
                i = index()
                if i < 2:
                    return VMobject()
                pts = [tr.c2p(a, min(b, V_TOP)) for a, b in zip(run[0][:i + 1:4], run[2][:i + 1:4])]
                return VMobject().set_points_as_corners(pts).set_stroke(color, CURVE_WIDTH - 1.0, opacity)
            return make

        def field_arrow(run_def):
            qm, sense, omega = run_def
            centre = frame.get_corner(UL) + np.array([0.75, -0.75, 0])

            def make():
                tt = t[index()]
                d = np.array([np.cos(omega * tt), -sense * np.sin(omega * tt), 0.0])
                return Arrow(centre - 0.05 * d, centre + 0.55 * d, buff=0, color=E_FIELD, stroke_width=5,
                             max_tip_length_to_length_ratio=0.3)
            return make

        e_lab = math(r"\mathbf{E}(t)", color=E_FIELD, size=MATH_SMALL).move_to(frame.get_corner(UL) + np.array([0.75, -1.55, 0]))
        clock_lab = math(r"|\omega_c|t=", color=MUTED, size=MATH_SMALL).move_to([4.6, 3.35, 0])
        clock = DecimalNumber(0.0, num_decimal_places=1, color=INK, font_size=MATH_SMALL)

        def place(m):
            m.set_value(t[index()])
            m.next_to(clock_lab, RIGHT, buff=0.12)

        clock.add_updater(place)
        place(clock)
        self.add(frame, top, xy_lab, b_key, tr, tx_ticks, ty_ticks, tx_lab, ty_lab, e_lab, clock_lab, clock)
        self.add(theory)

        kept = VGroup()
        for k, (run_def, run, (color, opacity, caption)) in enumerate(zip(CR_RUNS, runs, styles)):
            title = math(caption, color=color, size=MATH_SMALL).move_to([-3.0, 3.35, 0])
            title.align_to([-6.55, 0, 0], LEFT)
            tracker.set_value(0.0)
            orbit = always_redraw(orbit_path(run, color))
            dot = always_redraw(lambda run=run, color=color: Dot(top.c2p(*np.clip(run[1][index(), :2], -V_TOP, V_TOP)),
                                                                 radius=0.07, color=color))
            speed = always_redraw(speed_path(run, color, opacity))
            arrow = always_redraw(field_arrow(run_def))
            self.add(title, orbit, dot, speed, arrow)
            self.play(tracker.animate.set_value(1.0), run_time=6.0, rate_func=LINEAR)
            self.wait(0.6)
            final = speed.copy().clear_updaters()
            tag_tex, tag_color, anchor = tags[k]
            tag = math(tag_tex, color=tag_color, size=MATH_SMALL).move_to(tr.c2p(*anchor))
            kept.add(final, tag)
            self.add(final)
            self.play(FadeIn(tag), run_time=0.4)
            self.remove(speed)
            if k < len(CR_RUNS) - 1:
                self.remove(title, orbit, dot, arrow)

        slope_i = cr_growth_rate(runs[0][0], runs[0][2])
        slope_e = cr_growth_rate(runs[3][0], runs[3][2])
        rows = VGroup(
            math(r"\text{resonance: } dv_\perp/dt\ \text{in}\ |q_\alpha|E_0/m_\alpha", color=MUTED, size=MATH_SMALL),
            math(rf"\mathrm{{ion}}\ {slope_i:.4f},\ \mathrm{{electron}}\ {slope_e:.4f}\ \mid\ 1", color=ACCENT, size=MATH_SMALL),
            math(r"\text{dashed: } 2|\sin(\Delta t/2)/\Delta|,\ \Delta=\omega_c\mp\omega", color=MUTED, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rows.next_to(tr.c2p(0, 0), DOWN, buff=0.6).align_to(tr.c2p(0, 0), LEFT).shift(0.4 * LEFT)
        self.play(FadeIn(rows), run_time=0.8)
        self.wait(2.5)
