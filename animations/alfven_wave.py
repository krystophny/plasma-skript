"""Shear Alfven wave on a plucked magnetic field line.

Model: linearized ideal MHD about a uniform field B_0 e_x in a uniform plasma
of mass density rho at rest, for a transverse perturbation that depends on x
only (k parallel to B_0, shear polarization along y):

    rho d(du_y)/dt = (B_0/mu_0) d(dB_y)/dx ,      d(dB_y)/dt = B_0 d(du_y)/dx .

The field-line displacement xi_y obeys du_y = d xi_y/dt and
dB_y = B_0 d xi_y/dx, so the field line is the curve y = xi_y(x, t).  The two
equations are integrated on a staggered grid (du_y and xi_y on nodes, dB_y on
cell centres, leapfrog in time, Courant number 0.5), not from the
d'Alembert solution.  The line is tied at x = 0 and x = L (du_y = 0) and is
plucked at t = 0: xi_y = xi_0 exp(-(x - x_0)^2/(2 w^2)), x_0 = 0.3 L,
w = 0.035 L, du_y = 0.  Linear equations: the amplitude xi_0 only scales the
picture.

Normalization: B/B_0, rho/rho_0 and mu_0 = 1, so speeds are in
v_A0 = B_0/(mu_0 rho_0)^(1/2); x/L [1], xi_y/xi_0 [1], t v_A0/L [1].  Two
runs from the same pluck, one after the other: rho = rho_0 and
rho = 4 rho_0 (v_A halves).  The pluck splits into two pulses running at
-+v_A; the pulse reflects inverted at a tied end.

Check (scripts/check-physics.py repeats it): the right-moving pulse peak,
located by a parabola through the three largest grid values, moves with the
least-squares speed v_A = B_0/(mu_0 rho)^(1/2).
"""

from manim import *
import numpy as np

from style import (
    ACCENT, AXIS_WIDTH, B_FIELD, CURVE_WIDTH, EASE, FAINT, GRID, INK, LINEAR,
    MUTED, THIN_WIDTH, StyledScene, axes, axis_labels, label, math,
    MATH_SIZE, MATH_SMALL, SMALL_SIZE,
)


N_CELLS = 800                   # cells between the tied ends
X_PLUCK = 0.3                   # x_0/L [1]
WIDTH = 0.035                   # w/L [1]
T_END = 0.6                     # t v_A0/L [1]
COURANT = 0.5
FRAMES = 121
DENSITIES = (1.0, 4.0)          # rho/rho_0 of the two runs [1]
B0 = 1.0                        # B_0 [B_0]
MU0 = 1.0


def alfven_speed(b0=B0, rho=1.0, mu0=MU0):
    return b0 / np.sqrt(mu0 * rho)


def solve(rho=1.0, b0=B0, n=N_CELLS, t_end=T_END, frames=FRAMES):
    """Staggered leapfrog for du_y (nodes) and dB_y (centres).

    Returns x (nodes), times and xi_y/xi_0 on the nodes, (frames, n + 1).
    The time step is set from the largest admissible speed b0/sqrt(mu0 rho)
    only through the Courant condition.
    """
    x = np.linspace(0.0, 1.0, n + 1)
    dx = x[1] - x[0]
    xi = np.exp(-(x - X_PLUCK) ** 2 / (2 * WIDTH**2))
    xi[0] = xi[-1] = 0.0
    b = b0 * np.diff(xi) / dx                         # dB_y = B_0 d xi/dx
    dt = COURANT * dx / alfven_speed(b0, rho)
    steps = int(np.ceil(t_end / dt))
    dt = t_end / steps
    save = np.round(np.linspace(0, steps, frames)).astype(int)
    accel = b0 / (MU0 * rho)

    def force(bb):
        a = np.zeros(n + 1)
        a[1:-1] = accel * np.diff(bb) / dx
        return a

    u = 0.5 * dt * force(b)                           # u at t = dt/2
    out, k = [], 0
    for step in range(steps + 1):
        if step == save[k]:
            out.append(xi.copy())
            k += 1
            if k == len(save):
                break
        xi = xi + dt * u
        b = b + dt * b0 * np.diff(u) / dx
        u = u + dt * force(b)
    return x, np.linspace(0, t_end, frames), np.array(out)


def pulse_peak(x, xi, x_min):
    """Peak position of the largest positive maximum right of x_min."""
    mask = x > x_min
    i = np.argmax(np.where(mask, xi, -np.inf))
    y0, y1, y2 = xi[i - 1], xi[i], xi[i + 1]
    return x[i] + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2) * (x[1] - x[0])


def measured_speed(rho=1.0, b0=B0):
    """Least-squares speed of the right-moving pulse while it is free."""
    x, t, xi = solve(rho, b0)
    v = alfven_speed(b0, rho)
    use = (t > 3 * WIDTH / v) & (X_PLUCK + v * t < 0.9)
    peaks = np.array([pulse_peak(x, s, X_PLUCK + 0.5 * v * ti) for s, ti in zip(xi[use], t[use])])
    return np.polyfit(t[use], peaks, 1)[0], t[use], peaks


class AlfvenWave(StyledScene):
    """Plucked field line at rho_0, then at 4 rho_0 from the same pluck."""

    def build(self):
        ax = axes([0, 1, 0.1], [-1.2, 1.2, 0.5], 12.4, 3.5, ticks=True).move_to([0, 0.55, 0])
        ax_labels = VGroup(
            math(r"x/L\ [1]", color=MUTED, size=MATH_SMALL)
            .next_to(ax.c2p(1, -1.2), DOWN, buff=0.15).align_to(ax.c2p(1, 0), RIGHT),
            math(r"\xi_y/\xi_0\ [1]", color=MUTED, size=MATH_SMALL)
            .next_to(ax.c2p(0, 1.2), UP, buff=0.15))
        ticks = VGroup(
            *[math(f"{v:g}", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, -1.2), DOWN, buff=0.15)
              for v in (0, 0.5)],
            *[math(t, color=MUTED, size=MATH_SMALL).next_to(ax.c2p(0, v), LEFT, buff=0.15)
              for v, t in ((-1, "-1"), (0, "0"), (1, "1"))])
        ax.x_axis.shift(ax.c2p(0, -1.2) - ax.c2p(0, 0))
        posts = VGroup(*[Line(ax.c2p(v, -0.35), ax.c2p(v, 0.35), color=INK, stroke_width=5)
                         for v in (0, 1)])
        b_arrow = Arrow(ax.c2p(0.17, 1.42), ax.c2p(0.29, 1.42), buff=0, color=B_FIELD,
                        stroke_width=4, max_tip_length_to_length_ratio=0.2)
        b_lab = math(r"\mathbf B_0", color=B_FIELD, size=MATH_SMALL).next_to(b_arrow, RIGHT, buff=0.15)

        law = VGroup(
            math(r"v_A = \frac{B_0}{\sqrt{\mu_0\rho}}", size=MATH_SIZE),
            math(r"\delta B_y = B_0\,\partial_x\xi_y", color=MUTED, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, -2.7, 0])
        key = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=B_FIELD, stroke_width=CURVE_WIDTH),
                   label("field line", size=SMALL_SIZE)).arrange(RIGHT, buff=0.18),
            VGroup(Dot(radius=0.07, color=INK), label("fluid elements", size=SMALL_SIZE))
            .arrange(RIGHT, buff=0.18),
            VGroup(DashedLine(UP * 0.22, DOWN * 0.22, color=ACCENT, stroke_width=THIN_WIDTH),
                   math(r"x_0 \pm v_A t", color=ACCENT, size=MATH_SMALL)).arrange(RIGHT, buff=0.24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-4.6, -2.7, 0])

        runs = [(rho, solve(rho), measured_speed(rho)[0]) for rho in DENSITIES]
        tracker = ValueTracker(0.0)
        x_nodes = runs[0][1][0]
        elements = np.arange(0, len(x_nodes), len(x_nodes) // 40)

        def frame(run):
            _, (_, times, xi), _ = run
            f = tracker.get_value() / T_END * (FRAMES - 1)
            i = min(int(f), FRAMES - 2)
            w = f - i
            return (1 - w) * xi[i] + w * xi[i + 1]

        def field_line(run):
            return always_redraw(lambda: VMobject(stroke_color=B_FIELD, stroke_width=CURVE_WIDTH)
                                 .set_points_as_corners([ax.c2p(a, b) for a, b in
                                                         zip(x_nodes[::2], frame(run)[::2])]))

        def dots(run):
            return always_redraw(lambda: VGroup(*[
                Dot(ax.c2p(x_nodes[j], frame(run)[j]), radius=0.06, color=INK) for j in elements]))

        def markers(run):
            v = alfven_speed(rho=run[0])

            def draw():
                group = VGroup()
                for sign in (1, -1):
                    xm = X_PLUCK + sign * v * tracker.get_value()
                    if 0.0 < xm < 1.0:
                        group.add(DashedLine(ax.c2p(xm, -0.95), ax.c2p(xm, 1.15), color=ACCENT,
                                             stroke_width=THIN_WIDTH, dash_length=0.08))
                return group
            return always_redraw(draw)

        clock = always_redraw(lambda: math(rf"t v_{{A0}}/L = {tracker.get_value():.2f}", color=MUTED,
                                           size=MATH_SMALL).next_to(ax.c2p(1, 1.2), UP, buff=0.15)
                              .align_to(ax.c2p(1, 0), RIGHT))

        self.play(Create(ax), FadeIn(ax_labels, ticks, posts, b_arrow, b_lab), run_time=1.0, rate_func=EASE)
        self.play(FadeIn(law, key), run_time=0.8, rate_func=EASE)
        for r, run in enumerate(runs):
            rho, _, speed = run
            tracker.set_value(0.0)
            case = math(r"\rho = \rho_0" if r == 0 else r"\rho = 4\rho_0", color=INK, size=MATH_SIZE) \
                .next_to(ax.c2p(0.5, 1.2), UP, buff=0.12)
            result = VGroup(
                label("pulse-peak speed", size=SMALL_SIZE),
                math(rf"{speed:.4f}\,v_{{A0}}", color=INK, size=MATH_SIZE),
                math(rf"v_A = {alfven_speed(rho=rho):.4f}\,v_{{A0}}", color=ACCENT, size=MATH_SMALL),
            ).arrange(DOWN, buff=0.2).move_to([0.1, -2.7, 0])
            line, ds, ms = field_line(run), dots(run), markers(run)
            self.play(FadeIn(case), FadeIn(line), FadeIn(ds), FadeIn(clock), run_time=0.6)
            self.add(ms)
            self.wait(0.5)
            self.play(tracker.animate.set_value(T_END), run_time=7.0, rate_func=LINEAR)
            self.play(FadeIn(result), run_time=0.5)
            self.wait(1.8)
            self.play(*[FadeOut(m) for m in (case, line, ds, ms, clock, result)], run_time=0.5) \
                if r == 0 else self.wait(1.0)
