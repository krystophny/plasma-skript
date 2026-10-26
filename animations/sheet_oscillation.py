"""Cold plasma oscillation and wave breaking in the electron sheet model.

Model (Dawson 1959): N electron sheets of surface density n_0 Delta in a
periodic box of length lambda = 2 pi/k on a fixed uniform ion background;
cold, no collisions.  Gauss's law gives the field at a sheet exactly: it
depends only on how many sheets lie to its left,

    e E(x_j)/(m_e omega_pe^2) = x_j - Delta (r_j + 1/2) - <x - xbar>,

with r_j the number of sheets to the left, Delta = lambda/N and xbar the
equilibrium positions.  While the order of the sheets is unchanged, every
sheet is a harmonic oscillator at omega_pe whatever the amplitude.

Start: sheets at their equilibrium positions with velocity
v_j = v_0 sin(k xbar_j).  Then xi_j = (v_0/omega_pe) sin(k xbar_j) sin(omega_pe t),
and neighbouring sheets first cross (wave breaking) when k v_0/omega_pe > 1,
at omega_pe t = arcsin(omega_pe/(k v_0)).  Small run: k v_0/omega_pe = 0.5;
large run: 1.5.  Leapfrog with the rank-based field, 400 steps per period.

Shown: phase space (x/lambda, k v/omega_pe), the sheets in real space and
k e E/(m_e omega_pe^2) against x/lambda; time omega_pe t.  All [1].
scripts/check-physics.py integrates the same sheets independently with RK4
and the field summed sheet by sheet.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, AXIS_WIDTH, CURVE_WIDTH, E_FIELD, ELECTRON, FAINT, INK, LINEAR, MATH_SIZE, MATH_SMALL,
    MUTED, THIN_WIDTH, StyledScene, axes, dashed, math,
)

SHEETS = 160
SHEET_STEPS = 400                  # leapfrog steps per plasma period
SHEET_PERIODS = 3.0
SMALL_KV = 0.5                     # k v_0/omega_pe [1]
LARGE_KV = 1.5


def sheet_equilibrium(n=SHEETS):
    """Equilibrium positions kx in [0, 2 pi) (k = 1, omega_pe = 1)."""
    return (np.arange(n) + 0.5) * 2 * np.pi / n


def sheet_accel(x):
    """-eE/m_e at every sheet (k = 1, omega_pe = 1), x wrapped to [0, 2 pi)."""
    n = len(x)
    delta = 2 * np.pi / n
    rank = np.empty(n)
    rank[np.argsort(x, kind="stable")] = np.arange(n)
    return -(x - delta * (rank + 0.5)) + (x.mean() - np.pi)


def sheet_field(x, grid):
    """k e E/(m_e omega_pe^2) on `grid` (k = 1) from Gauss's law."""
    n = len(x)
    delta = 2 * np.pi / n
    left = np.searchsorted(np.sort(x), grid)
    return grid - delta * left + np.pi - x.mean()


def sheet_run(kv, n=SHEETS, steps=SHEET_STEPS, periods=SHEET_PERIODS):
    """Leapfrog (kick-drift-kick); returns t, x (k, n) and v (k, n)."""
    dt = 2 * np.pi / steps
    x = sheet_equilibrium(n)
    v = kv * np.sin(x)
    total = int(round(periods * steps))
    xs, vs = [x.copy()], [v.copy()]
    a = sheet_accel(x)
    for _ in range(total):
        v = v + 0.5 * dt * a
        x = np.mod(x + dt * v, 2 * np.pi)
        a = sheet_accel(x)
        v = v + 0.5 * dt * a
        xs.append(x.copy())
        vs.append(v.copy())
    return np.arange(total + 1) * dt, np.array(xs), np.array(vs)


def mode_frequency(t, v, n=SHEETS):
    """omega/omega_pe from the zero crossings of V(t) = sum v_j sin(k xbar_j)."""
    mode = v @ np.sin(sheet_equilibrium(n))
    s = np.sign(mode)
    idx = np.nonzero(s[:-1] * s[1:] < 0)[0]
    zeros = t[idx] - mode[idx] * (t[idx + 1] - t[idx]) / (mode[idx + 1] - mode[idx])
    return np.pi / np.mean(np.diff(zeros))


def first_crossing(t, x):
    """First time at which two neighbouring sheets meet, interpolated linearly
    in the smallest neighbour gap between the stored steps."""
    start = np.argsort(x[0])
    gap = np.diff(x[:, start], axis=1).min(axis=1)
    k = np.argmax(gap < 0)
    if gap[k] >= 0:
        return np.inf
    return t[k - 1] + gap[k - 1] / (gap[k - 1] - gap[k]) * (t[k] - t[k - 1])


class SheetPlasma(StyledScene):
    KV = SMALL_KV
    V_MAX = 1.0
    E_MAX = 1.0

    def build(self):
        t, xs, vs = sheet_run(self.KV)
        frames = len(t)
        lam = 2 * np.pi

        ps = axes([0, 1, 0.25], [-self.V_MAX, self.V_MAX, self.V_MAX / 2], 9.6, 3.0).move_to([0.45, 1.05, 0])
        ef = axes([0, 1, 0.25], [-self.E_MAX, self.E_MAX, self.E_MAX / 2], 9.6, 1.45).move_to([0.45, -2.3, 0])
        strip_y = -0.85
        strip = Line(ps.c2p(0, 0) * [1, 0, 0] + [0, strip_y, 0], ps.c2p(1, 0) * [1, 0, 0] + [0, strip_y, 0],
                     color=FAINT, stroke_width=1.0)

        def y_ticks(ax, vmax):
            return VGroup(*[math(f"{v:g}".replace("-", "{-}"), color=MUTED, size=MATH_SMALL)
                            .next_to(ax.c2p(0, v), LEFT, buff=0.12) for v in (-vmax, 0, vmax)])

        x_ticks = VGroup(*[math(f"{v:g}", color=MUTED, size=MATH_SMALL).next_to(ef.c2p(v, -self.E_MAX), DOWN, buff=0.12)
                           for v in (0, 0.5, 1)])
        x_lab = math(r"x/\lambda\ [1]", color=MUTED, size=MATH_SMALL).next_to(ef.c2p(1, -self.E_MAX), RIGHT, buff=0.25)
        v_lab = math(r"kv/\omega_{pe}\ [1]", color=MUTED, size=MATH_SMALL).next_to(ps.c2p(0, self.V_MAX), UP, buff=0.12)
        v_lab.align_to(ps.c2p(0, 0), LEFT).shift(0.6 * LEFT)
        e_lab = math(r"keE/(m_e\omega_{pe}^2)\ [1]", color=E_FIELD, size=MATH_SMALL).next_to(ef.c2p(0, self.E_MAX), UP, buff=0.12)
        e_lab.align_to(ef.c2p(0, 0), LEFT).shift(0.6 * LEFT)
        s_lab = math(r"\mathrm{sheets}", color=MUTED, size=MATH_SMALL).next_to(strip, RIGHT, buff=0.25)
        ps_ticks, ef_ticks = y_ticks(ps, self.V_MAX), y_ticks(ef, self.E_MAX)
        ps.x_axis.set_opacity(0.0)
        zero_line = Line(ps.c2p(0, 0), ps.c2p(1, 0), color=FAINT, stroke_width=1.0)
        ef.x_axis.set_opacity(0.0)
        ef_zero = Line(ef.c2p(0, 0), ef.c2p(1, 0), color=FAINT, stroke_width=1.0)
        ef_base = Line(ef.c2p(0, -self.E_MAX), ef.c2p(1, -self.E_MAX), color=INK, stroke_width=AXIS_WIDTH)

        tracker = ValueTracker(0.0)

        def index():
            return min(int(round(tracker.get_value() * (frames - 1))), frames - 1)

        dots = VGroup(*[Dot(radius=0.04, color=ELECTRON) for _ in range(xs.shape[1])])

        def move(group):
            i = index()
            for d, x, v in zip(group, xs[i], vs[i]):
                d.move_to(ps.c2p(x / lam, np.clip(v, -self.V_MAX, self.V_MAX)))

        dots.add_updater(move)
        move(dots)
        ticks = VGroup(*[Line(UP * 0.16, DOWN * 0.16, color=ELECTRON, stroke_width=1.6) for _ in range(xs.shape[1])])

        def move_ticks(group):
            i = index()
            for m, x in zip(group, xs[i]):
                m.move_to([ps.c2p(x / lam, 0)[0], strip_y, 0])

        ticks.add_updater(move_ticks)
        move_ticks(ticks)
        grid = np.linspace(0.0, lam, 600)

        def field():
            e = np.clip(sheet_field(xs[index()], grid), -self.E_MAX, self.E_MAX)
            return VMobject().set_points_as_corners([ef.c2p(g / lam, y) for g, y in zip(grid, e)]) \
                .set_stroke(E_FIELD, CURVE_WIDTH - 1.0)

        e_curve = always_redraw(field)

        clock_lab = math(r"\omega_{pe}t=", color=MUTED, size=MATH_SMALL).move_to([4.7, 3.35, 0])
        clock = DecimalNumber(0.0, num_decimal_places=1, color=INK, font_size=MATH_SMALL)

        def place(m):
            m.set_value(t[index()])
            m.next_to(clock_lab, RIGHT, buff=0.12)

        clock.add_updater(place)
        place(clock)
        info = self.info(t, xs, vs)
        self.add(ps, ef, zero_line, ef_zero, ef_base, strip, ps_ticks, ef_ticks, x_ticks, x_lab, v_lab, e_lab,
                 s_lab, ticks, dots, e_curve, clock_lab, clock, *info)
        self.wait(0.8)
        for stop, run in self.SEGMENTS:
            self.play(tracker.animate.set_value(stop), run_time=run, rate_func=LINEAR)
        self.wait(1.5)


class SheetOscillation(SheetPlasma):
    """Small amplitude: every sheet oscillates at omega_pe; no crossing."""
    KV = SMALL_KV
    V_MAX = 0.6
    E_MAX = 0.6
    SEGMENTS = ((1.0, 14.0),)

    def info(self, t, xs, vs):
        omega = mode_frequency(t, vs)
        top = math(rf"kv_0/\omega_{{pe}}={self.KV:g}", color=MUTED, size=MATH_SMALL).move_to([-5.3, 3.35, 0])
        res = math(rf"\mathrm{{measured}}\ \omega/\omega_{{pe}}={omega:.4f}", color=ACCENT, size=MATH_SMALL)
        res.next_to([5.25, 2.95, 0], LEFT, buff=0)
        return [top, res]


class SheetWaveBreaking(SheetPlasma):
    """Large amplitude: sheets overtake their neighbours, phase space folds."""
    KV = LARGE_KV
    V_MAX = 3.2
    E_MAX = 1.6
    SEGMENTS = ((1 / 6, 8.0), (1.0, 9.0))      # first half period slowly

    def info(self, t, xs, vs):
        crossing = first_crossing(t, xs)
        top = math(rf"kv_0/\omega_{{pe}}={self.KV:g}", color=MUTED, size=MATH_SMALL).move_to([-5.3, 3.35, 0])
        res = math(rf"\mathrm{{crossing}}\ \omega_{{pe}}t={crossing:.2f}\ \mid\ \arcsin(\omega_{{pe}}/kv_0)"
                   rf"={np.arcsin(1 / self.KV):.2f}", color=ACCENT, size=MATH_SMALL)
        res.next_to([5.25, 2.95, 0], LEFT, buff=0)
        return [top, res]
