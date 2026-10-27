"""E x B drift seen from the lab and from the frame moving with v_D.

Model: one ion (q_alpha > 0) in uniform B = B e_z (out of the page) and
E = E e_y, E/B = 0.4 v_perp, where v_perp is the gyration speed in the drift
frame (course notation: v = v_D + v_perp(t)); normalized with
q_alpha = m_alpha = B = v_perp = 1, so lengths are in
rho_L = v_perp/|omega_c| [1] and time is omega_c t [1].  The orbit is a Boris push of
dv/dt = (q_alpha/m_alpha)(E + v x B) (drift_models.exb_orbit), started on the
exact discrete gyro-circle of the scheme with the guiding centre at the origin.

First the lab frame: a looped trochoid that drifts along +x.  Then the same
orbit in the frame moving with v_D = E x B/B^2: there
E' = E + v_D x B = 0 and the orbit is a circle.  The velocity arrow on the
particle is drawn as v/omega_c in rho_L: in the lab |v| = |v_D + v_perp| runs
between v_perp - v_D and v_perp + v_D, in the drift frame |v_perp| = v_perp
and the arrow is one rho_L long.  On screen only labels and the clock; the drift velocity against E/B and the constant drift-frame radius
are checked in scripts/check-physics.py (Boris and RK4), not shown.
"""

from manim import *
import numpy as np

from drift_models import exb_orbit
from style import (
    B_FIELD, CURVE_WIDTH, DOT_RADIUS, E_FIELD, EASE, FAINT, INK, ION, LABEL_SIZE, LINEAR,
    GREEN, MATH_SIZE, MATH_SMALL, MUTED, THIN_WIDTH, StyledScene, axes, label, math,
)

GRID = 2400
VELOCITY = GREEN
RUN_TIME = 9.0


def orbit_data():
    t, x, _, v_d, x_frame = exb_orbit()
    # Central differences: velocity at the position time levels (Boris v is staggered).
    v = np.gradient(x, t, axis=0)
    grid = np.linspace(0, t[-1], GRID)

    def on_grid(a):
        return np.array([np.interp(grid, t, a[:, k]) for k in range(2)]).T
    centre = np.outer(grid, v_d[:2])
    return grid, on_grid(x), on_grid(x_frame), centre, on_grid(v), on_grid(v - v_d)


class ExBFrameChange(StyledScene):
    """Lab-frame trochoid, then the circle in the frame moving with v_D."""

    def build(self):
        grid, lab, frame, centre, v_lab, v_frame = orbit_data()

        x_lo, x_hi = -1.6, 9.4
        ax = axes([x_lo, x_hi, 1], [-1.5, 1.5, 1], 12.4, 3.38).move_to([0.2, 0.25, 0])
        x_ticks = VGroup(*[math(f"{v:d}", color=MUTED, size=MATH_SMALL)
                           .next_to(ax.c2p(v, -1.5), DOWN, buff=0.12) for v in (0, 2, 4, 6)])
        y_ticks = VGroup(*[math(f"{v:d}".replace("-", "{-}"), color=MUTED, size=MATH_SMALL)
                           .next_to(ax.c2p(x_lo, v), LEFT, buff=0.12) for v in (-1, 0, 1)])
        y_lab = math(r"y/\rho_L\ [1]", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(x_lo, 1.5), UP, buff=0.18)
        x_lab_lab = math(r"x/\rho_L\ [1]", color=MUTED, size=MATH_SMALL)
        x_lab_frame = math(r"(x-v_Dt)/\rho_L\ [1]", color=MUTED, size=MATH_SMALL)
        for lab_mob in (x_lab_lab, x_lab_frame):
            lab_mob.next_to(ax.c2p(x_hi, -1.5), DOWN, buff=0.12).align_to(ax.c2p(x_hi, 0), RIGHT)

        title_lab = label("lab frame", color=INK, size=LABEL_SIZE).move_to([-3.6, 3.35, 0])
        title_frame = label("frame moving with", color=INK, size=LABEL_SIZE)
        title_frame = VGroup(title_frame, math(r"\mathbf{v}_D", color=INK, size=MATH_SIZE)
                             ).arrange(RIGHT, buff=0.15).move_to([-3.0, 3.35, 0])

        b_marks = VGroup()
        for x in np.arange(-1.0, 7.1, 2.0):
            for y in (-1.25, 1.25):
                b_marks.add(VGroup(Circle(radius=0.09, color=B_FIELD, stroke_width=1.6),
                                   Dot(radius=0.025, color=B_FIELD)).move_to(ax.c2p(x + 2.0, y)))
        b_marks.set_opacity(0.6)
        b_key = VGroup(VGroup(Circle(radius=0.11, color=B_FIELD, stroke_width=2.0),
                              Dot(radius=0.03, color=B_FIELD)),
                       math(r"\mathbf{B}", color=B_FIELD, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)
        b_key.move_to([0.9, 3.35, 0])
        e_key = VGroup(Arrow(ORIGIN, UP * 0.6, buff=0, color=E_FIELD, stroke_width=3,
                             max_tip_length_to_length_ratio=0.25),
                       math(r"\mathbf{E}", color=E_FIELD, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)
        e_key.move_to([4.3, 3.35, 0])
        e_zero = math(r"\mathbf{E}'=\mathbf{E}+\mathbf{v}_D\times\mathbf{B}=0", color=E_FIELD, size=MATH_SMALL)
        e_zero.move_to([4.3, 3.35, 0])
        vd_arrow = Arrow(ax.c2p(4.6, 1.75), ax.c2p(6.6, 1.75), buff=0, color=INK, stroke_width=3,
                         max_tip_length_to_length_ratio=0.15).set_y(2.5)   # above the velocity arrow's reach
        vd_lab = math(r"\mathbf{v}_D=\mathbf{E}\times\mathbf{B}/B^2", color=INK, size=MATH_SMALL
                      ).next_to(vd_arrow, LEFT, buff=0.2)

        # The velocity arrow is named only here, in its colour: tip labels collide with the ticks.
        speed_lab = MathTex(r"v_\perp-v_D\le|", r"\mathbf{v}", r"|\le v_\perp+v_D", color=INK, font_size=MATH_SMALL)
        speed_frame = MathTex(r"|", r"\mathbf{v}_\perp", r"|=v_\perp,\quad \rho_L=v_\perp/|\omega_c|",
                              color=INK, font_size=MATH_SMALL)
        speed_lab[1].set_color(VELOCITY)
        speed_frame[1].set_color(VELOCITY)
        for mob in (speed_lab, speed_frame):
            mob.move_to([-6.4, -3.4, 0], aligned_edge=LEFT)

        clock_label = math(r"\omega_c t=", color=MUTED, size=MATH_SMALL).move_to([5.0, -3.4, 0])
        clock = DecimalNumber(0.0, num_decimal_places=1, color=INK, font_size=MATH_SMALL)
        tracker = ValueTracker(0.0)

        def index():
            return min(int(tracker.get_value() * (GRID - 1)), GRID - 1)

        def place_clock(m):
            m.set_value(grid[index()])
            m.next_to(clock_label, RIGHT, buff=0.12)

        clock.add_updater(place_clock)
        place_clock(clock)

        def scene_parts(points, centres, velocities):
            def velocity():
                i = index()
                tail = np.asarray(points[i])
                tip = tail + velocities[i]          # v/omega_c in rho_L, omega_c = 1
                return Arrow(ax.c2p(*tail), ax.c2p(*tip), buff=0, color=VELOCITY, stroke_width=4,
                             max_tip_length_to_length_ratio=0.2)

            def path():
                i = index()
                if i < 2:
                    return VMobject()
                pts = [ax.c2p(*p) for p in points[:i + 1:2]]
                return VMobject().set_points_as_corners(pts).set_stroke(ION, CURVE_WIDTH - 1.2)

            def track():
                i = index()
                if i < 2:
                    return VMobject()
                return DashedLine(ax.c2p(*centres[0]), ax.c2p(*centres[i]), color=FAINT,
                                  stroke_width=THIN_WIDTH, dash_length=0.1)
            return VGroup(
                always_redraw(track),
                always_redraw(path),
                always_redraw(lambda: Line(ax.c2p(*centres[index()]), ax.c2p(*points[index()]),
                                           color=MUTED, stroke_width=1.6)),
                always_redraw(lambda: Dot(ax.c2p(*centres[index()]), radius=DOT_RADIUS, color=INK)),
                always_redraw(lambda: Dot(ax.c2p(*points[index()]), radius=DOT_RADIUS * 1.7, color=ION)),
                always_redraw(velocity),
            )

        lab_parts = scene_parts(lab, centre, v_lab)
        frame_parts = scene_parts(frame, np.zeros_like(centre), v_frame)

        self.add(ax, x_ticks, y_ticks, y_lab, x_lab_lab, b_marks, b_key, e_key, title_lab,
                 vd_arrow, vd_lab, speed_lab, clock_label, clock)
        self.add(lab_parts)
        self.wait(0.6)
        self.play(tracker.animate.set_value(1.0), run_time=RUN_TIME, rate_func=LINEAR)
        self.wait(1.9)

        # Same orbit, same axes: the frame moving with v_D.
        self.play(FadeOut(lab_parts), FadeOut(title_lab), FadeOut(e_key),
                  FadeOut(x_lab_lab), FadeOut(vd_arrow), FadeOut(vd_lab), FadeOut(speed_lab), run_time=0.8, rate_func=EASE)
        tracker.set_value(0.0)
        self.play(FadeIn(title_frame), FadeIn(e_zero), FadeIn(x_lab_frame), FadeIn(speed_frame), run_time=0.8, rate_func=EASE)
        self.add(frame_parts)
        self.wait(0.4)
        self.play(tracker.animate.set_value(1.0), run_time=RUN_TIME, rate_func=LINEAR)
        self.wait(2.5)
