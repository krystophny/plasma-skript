"""Diamagnetic current from gyrating ions whose guiding centres are at rest.

Model: one ion species (charge q_alpha > 0, mass m_alpha) in a uniform magnetic
field B = B e_z out of the page, E = 0.  Every ion moves on its exact
Lorentz-force circle x(t) = X + rho_L (cos(omega_c t + phi), -sin(omega_c t +
phi)) with the signed gyrofrequency omega_c = q_alpha B/m_alpha > 0 (clockwise
seen from +z), the same perpendicular speed v_perp and Larmor radius rho_L =
v_perp/omega_c.  The guiding centres R = x + (m_alpha/q_alpha) v x B/B^2 = X
are fixed: nothing drifts.  They fill the plane with the density gradient

    n(y) = n_0 (1 + y/L),   L = 5 rho_L,   n_0 = 12 per rho_L^2,

placed on a low-discrepancy (Fibonacci) lattice: X from the golden-ratio
sequence, Y from the inverse cumulative distribution of n, gyrophases from the
sqrt(2) sequence (deterministic, no random seed).

Measurement: six vertical lines x = -2.5, -1.5, ..., 2.5 rho_L are cut into
bins of height 1 rho_L.  Each sign change of x(t) - x_line on a time grid of
400 steps per gyration counts +1 (moving right) or -1 (moving left) in the bin
of its crossing height; the bars show the net count per line.  The net count
per gyration period T = 2 pi/omega_c and unit length is j_x T/q_alpha.  Every
ion crosses a line it reaches twice per period, so the counts do not average
down in time; their scatter between bins (about 12 %) is the finite number of
ions, and the mean over bins and lines is the measured current.  The
magnetization (diamagnetic) current of a ring distribution with perpendicular
pressure p = n m_alpha v_perp^2/2 is

    j_dia = B x grad p / B^2,   j_x = -p'(y)/B = -q_alpha (rho_L^2 omega_c/2) n'(y),

so the expected net count per period and bin height Dy is -pi rho_L^2 n' Dy =
-pi n_0 rho_L/L Dy = -7.54, and j_x/(q_alpha n_0 v_perp) = -rho_L/(2L) = -0.1,
independent of y although n changes by a factor 9 across the box.
Lengths are in rho_L [1], time in 1/omega_c (omega_c t [1]), current in
q_alpha n_0 v_perp [1].  scripts/check-physics.py checks the orbits against the
Lorentz force and the counts against the formula.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, B_FIELD, BLUE, CURVE_WIDTH, EASE, FAINT, GREEN, GRID, INK, ION, LINEAR,
    MATH_SIZE, MATH_SMALL, MUTED, THIN_WIDTH, StyledScene, axes, label, math, SMALL_SIZE,
)

RHO_L = 1.0                     # Larmor radius, the length unit
OMEGA_C = 1.0                   # signed gyrofrequency q_alpha B/m_alpha > 0 (ion)
L_GRAD = 5.0                    # density gradient length L/rho_L [1]
N0 = 12.0                       # guiding centres per rho_L^2 at y = 0
X_HALF = 3.6                    # sampled and shown box |x| <= 3.6 rho_L
Y_FILL = 4.0                    # guiding centres for |y| <= 4 rho_L
Y_SHOW = 3.0                    # shown |y| <= 3 rho_L
BIN_EDGES = np.arange(-2.5, 2.51, 1.0)   # counting bins on each line
LINES = np.arange(-2.5, 2.51, 1.0)       # counting lines x = const
PERIODS = 2                     # counted gyration periods
STEPS_PER_PERIOD = 400


def density(y):
    """n(y)/n_0 times N0: guiding centres per rho_L^2."""
    return N0 * (1.0 + y / L_GRAD)


def guiding_centres():
    """Fibonacci-lattice guiding centres (X, Y) and gyrophases phi."""
    area = 2 * X_HALF * 2 * Y_FILL
    n = int(round(N0 * area))               # mean density is N0 on |y| <= Y_FILL
    k = np.arange(n)
    golden = (np.sqrt(5.0) - 1.0) / 2.0
    x = -X_HALF + 2 * X_HALF * ((k * golden) % 1.0)
    u = (k + 0.5) / n
    a, ell = Y_FILL, L_GRAD
    # Inverse CDF of the linear density on [-a, a].
    y = ell * (-1.0 + np.sqrt(1.0 - 2.0 * (a - a * a / (2 * ell) - 2 * a * u) / ell))
    phase = 2 * np.pi * ((k * np.sqrt(2.0)) % 1.0)
    return x, y, phase


def orbit(x0, y0, phase, t):
    """Exact positions (n, len(t), 2) and velocities on the clockwise ion circles."""
    angle = OMEGA_C * np.asarray(t)[None, :] + phase[:, None]
    pos = np.stack([x0[:, None] + RHO_L * np.cos(angle),
                    y0[:, None] - RHO_L * np.sin(angle)], axis=-1)
    vel = np.stack([-RHO_L * OMEGA_C * np.sin(angle),
                    -RHO_L * OMEGA_C * np.cos(angle)], axis=-1)
    return pos, vel


def crossings(periods=PERIODS, steps=STEPS_PER_PERIOD):
    """Crossings of the lines x = LINES: arrays of time, height y and direction (+1 right)."""
    x0, y0, phase = guiding_centres()
    t = np.linspace(0.0, periods * 2 * np.pi / OMEGA_C, periods * steps + 1)
    out = [[], [], []]
    for x_line in LINES:
        near = np.abs(x0 - x_line) < 1.05 * RHO_L
        pos, _ = orbit(x0[near], y0[near], phase[near], t)
        xs, ys = pos[..., 0] - x_line, pos[..., 1]
        flip = np.signbit(xs[:, 1:]) != np.signbit(xs[:, :-1])
        p, i = np.nonzero(flip)
        w = xs[p, i] / (xs[p, i] - xs[p, i + 1])          # linear interpolation
        out[0].append(t[i] + w * (t[i + 1] - t[i]))
        out[1].append(ys[p, i] + w * (ys[p, i + 1] - ys[p, i]))
        out[2].append(np.where(xs[p, i + 1] > xs[p, i], 1, -1))
    times, heights, direction = (np.concatenate(a) for a in out)
    order = np.argsort(times)
    return times[order], heights[order], direction[order]


def binned_counts(t_max=None, periods=PERIODS):
    """Net crossing counts per bin and line up to time t_max (all by default)."""
    times, heights, direction = crossings(periods)
    if t_max is not None:
        keep = times <= t_max
        heights, direction = heights[keep], direction[keep]
    net, _ = np.histogram(heights, BIN_EDGES, weights=direction)
    return net / len(LINES)


def measured_current(periods=PERIODS):
    """j_x/(q_alpha n_0 v_perp) [1] per bin: net count/(time * bin height * n_0 v_perp)."""
    net = binned_counts(periods=periods)
    duration = periods * 2 * np.pi / OMEGA_C
    return net / (duration * np.diff(BIN_EDGES) * N0 * RHO_L * OMEGA_C)


def formula_current():
    """j_x = -p'/B with p = n m v_perp^2/2, in units of q_alpha n_0 v_perp: -rho_L/(2L)."""
    return -RHO_L / (2.0 * L_GRAD)


PLAY_GYRATE = 4.0               # seconds for the first, uncounted gyration
PLAY_COUNT = 11.0               # seconds for the counted periods


class DiamagneticDrift(StyledScene):
    """Gyrating ions with fixed guiding centres carry a net current."""

    def build(self):
        x0, y0, phase = guiding_centres()
        times, heights, direction = crossings()
        period = 2 * np.pi / OMEGA_C
        t_end = PERIODS * period
        currents = measured_current()
        j_formula = formula_current()
        net_expected = j_formula * period * N0 * RHO_L * OMEGA_C  # per bin height 1, per period

        scale = 0.8
        ax = axes([-X_HALF, X_HALF, 1], [-Y_SHOW, Y_SHOW, 1], 2 * X_HALF * scale,
                  2 * Y_SHOW * scale, ticks=False).move_to([-2.95, 0.15, 0])
        ax.x_axis.set_opacity(0)
        ax.y_axis.set_opacity(0)
        box = Rectangle(width=2 * X_HALF * scale, height=2 * Y_SHOW * scale, color=GRID,
                        stroke_width=1.6).move_to(ax.c2p(0, 0))

        def screen(x, y):
            return ax.c2p(x, y)

        # Ion markers (triangles), kept inside the shown box.
        show = np.abs(y0) < Y_SHOW + RHO_L
        sx, sy, sp = x0[show], y0[show], phase[show]
        tri = Triangle(color=ION, fill_opacity=0.85, stroke_width=0).scale(0.055)
        ions = VGroup(*[tri.copy() for _ in range(len(sx))])
        clock = ValueTracker(0.0)

        def place(group):
            t = clock.get_value()
            pos, _ = orbit(sx, sy, sp, np.array([t]))
            for m, (px, py) in zip(group, pos[:, 0, :]):
                inside = abs(px) <= X_HALF and abs(py) <= Y_SHOW
                m.move_to(screen(px, py))
                m.set_fill(opacity=0.85 if inside else 0.0)

        ions.add_updater(place)
        place(ions)

        # Four highlighted ions: their orbit circle and fixed guiding centre.
        picks = [int(np.argmin((sx - xx) ** 2 + (sy - yy) ** 2))
                 for xx, yy in ((-2.4, 1.6), (-0.4, -1.2), (2.2, 0.4), (1.0, 2.0))]
        rings = VGroup(*[DashedVMobject(Circle(radius=RHO_L * scale, color=INK, stroke_width=THIN_WIDTH),
                                        num_dashes=24).move_to(screen(sx[i], sy[i])) for i in picks])
        centres = VGroup(*[Cross(scale_factor=0.09, stroke_color=INK, stroke_width=3)
                           .move_to(screen(sx[i], sy[i])) for i in picks])

        b_key = VGroup(VGroup(Circle(radius=0.11, color=B_FIELD, stroke_width=2.0),
                              Dot(radius=0.03, color=B_FIELD)),
                       math(r"\mathbf{B}", color=B_FIELD, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)
        b_key.next_to(box, UP, buff=0.18).align_to(box, LEFT)
        grad = Arrow(box.get_corner(DR) + RIGHT * 0.45 + UP * 0.9, box.get_corner(UR) + RIGHT * 0.45 + DOWN * 0.9,
                     buff=0, color=INK, stroke_width=3, max_tip_length_to_length_ratio=0.1)
        grad_lab = math(r"\nabla n", color=INK, size=MATH_SMALL).next_to(grad, RIGHT, buff=0.08)
        ion_key = VGroup(tri.copy().scale(1.6).set_fill(opacity=1),
                         math(r"\mathrm{ion},\ \omega_{c\alpha}>0", color=ION, size=MATH_SMALL)
                         ).arrange(RIGHT, buff=0.15)
        ion_key.next_to(b_key, RIGHT, buff=0.6)
        gc_key = VGroup(Cross(scale_factor=0.09, stroke_color=INK, stroke_width=3),
                        label("guiding centre at rest", color=MUTED, size=SMALL_SIZE)).arrange(RIGHT, buff=0.15)
        gc_key.next_to(box, DOWN, buff=0.2).align_to(box, LEFT)
        units = math(r"x/\rho_L,\ y/\rho_L\ [1]", color=MUTED, size=MATH_SMALL)
        units.next_to(gc_key, DOWN, buff=0.15).align_to(box, LEFT)

        # Counting line and bins on x = 0.
        line = VGroup(*[DashedLine(screen(xl, BIN_EDGES[0]), screen(xl, BIN_EDGES[-1]), color=GREEN,
                                   stroke_width=THIN_WIDTH, dash_length=0.12) for xl in LINES])
        ticks = VGroup(*[Line(screen(xl - 0.1, e), screen(xl + 0.1, e), color=GREEN, stroke_width=THIN_WIDTH)
                         for xl in LINES for e in BIN_EDGES])

        # Right panel: net count per bin against y, same vertical scale.
        lo_count = -24.0
        hist = axes([lo_count, 3.0, 5],
                    [-Y_SHOW, Y_SHOW, 1], 3.9, 2 * Y_SHOW * scale, ticks=False)
        hist.move_to([4.3, 0.15, 0])
        hist.shift(UP * (ax.c2p(0, 0)[1] - hist.c2p(0, 0)[1]))
        zero = Line(hist.c2p(0, BIN_EDGES[0]), hist.c2p(0, BIN_EDGES[-1]), color=INK, stroke_width=1.6)
        count_lab = math(r"N_\rightarrow-N_\leftarrow", color=MUTED, size=MATH_SMALL)
        count_lab.next_to(hist.c2p(lo_count / 2, BIN_EDGES[-1]), UP, buff=0.25)
        count_unit = label("net crossings per line and bin", color=MUTED, size=SMALL_SIZE)
        count_unit.next_to(count_lab, UP, buff=0.1)
        tick_vals = VGroup()
        for v in (-20, -10, 0):
            if v >= lo_count:
                p = hist.c2p(v, BIN_EDGES[0])
                tick_vals.add(Line(p, p + DOWN * 0.08, color=INK, stroke_width=1.6))
                tick_vals.add(math(str(v), color=MUTED, size=MATH_SMALL).next_to(p, DOWN, buff=0.12))

        def bars():
            t = clock.get_value() - PLAY_GYRATE_T
            group = VGroup()
            if t <= 0:
                return group
            keep = times <= t
            net, _ = np.histogram(heights[keep], BIN_EDGES, weights=direction[keep])
            for k, v in enumerate(net / len(LINES)):
                if v == 0:
                    continue
                lo, hi = BIN_EDGES[k] + 0.12, BIN_EDGES[k + 1] - 0.12
                group.add(Polygon(hist.c2p(0, lo), hist.c2p(v, lo), hist.c2p(v, hi), hist.c2p(0, hi),
                                  color=BLUE, fill_opacity=0.75, stroke_width=1.2))
            return group

        def expected_line():
            t = clock.get_value() - PLAY_GYRATE_T
            v = net_expected * max(t, 0.0) / period
            return DashedLine(hist.c2p(v, BIN_EDGES[0]), hist.c2p(v, BIN_EDGES[-1]), color=ACCENT,
                              stroke_width=THIN_WIDTH + 0.6, dash_length=0.1)

        PLAY_GYRATE_T = period             # first period: gyration only, not counted
        bar_group = always_redraw(bars)
        exp_line = always_redraw(expected_line)
        exp_key = VGroup(DashedLine(ORIGIN, RIGHT * 0.45, color=ACCENT, stroke_width=THIN_WIDTH + 0.6,
                                    dash_length=0.1),
                         math(r"-\pi\rho_L^2\,\partial_y n\,\Delta y\ \omega_c t/2\pi", color=ACCENT,
                              size=MATH_SMALL)).arrange(RIGHT, buff=0.15)
        exp_key.next_to(hist.c2p(lo_count / 2, BIN_EDGES[0]), DOWN, buff=0.7)

        clock_lab = math(r"\omega_c t/2\pi=", color=MUTED, size=MATH_SMALL)
        clock_lab.move_to([-0.7, 3.0, 0])
        clock_num = DecimalNumber(0.0, num_decimal_places=2, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            m.set_value(clock.get_value() / period)
            m.next_to(clock_lab, RIGHT, buff=0.12)

        clock_num.add_updater(place_clock)
        place_clock(clock_num)

        # 1. Gyration only.
        self.play(Create(box), FadeIn(b_key), FadeIn(ion_key), FadeIn(grad), FadeIn(grad_lab),
                  FadeIn(units), run_time=0.8, rate_func=EASE)
        self.add(ions, clock_lab, clock_num)
        self.play(FadeIn(rings), FadeIn(centres), FadeIn(gc_key), run_time=0.6, rate_func=EASE)
        self.play(clock.animate.set_value(period), run_time=PLAY_GYRATE, rate_func=LINEAR)

        # 2. Count crossings of x = 0 for PERIODS periods.
        self.play(Create(line), FadeIn(ticks), Create(zero), FadeIn(count_lab), FadeIn(count_unit),
                  FadeIn(tick_vals), FadeIn(exp_key), run_time=0.8, rate_func=EASE)
        self.add(bar_group, exp_line)
        self.play(clock.animate.set_value(period + t_end), run_time=PLAY_COUNT, rate_func=LINEAR)
        ions.clear_updaters()

        # 3. Result.
        mean = float(np.mean(currents))
        result = VGroup(
            math(r"\mathbf{j}_{\rm dia}=\frac{\mathbf{B}\times\nabla p}{B^2},\quad p=\frac{n m_\alpha v_\perp^2}{2}",
                 color=INK, size=MATH_SMALL),
            math(rf"j_x/(q_\alpha n_0 v_\perp)\ [1]:\ \ \mathrm{{count}}\ {mean:+.3f}\ \mid\ "
                 rf"-\rho_L/2L={j_formula:+.3f}", color=INK, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        result.move_to([-1.6, -3.0, 0])
        self.play(FadeOut(gc_key), FadeOut(units), FadeIn(result),
                  run_time=0.8, rate_func=EASE)
        self.wait(3.0)
