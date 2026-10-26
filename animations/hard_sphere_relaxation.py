"""Relaxation of a hard-disk gas to the two-dimensional Maxwellian.

Model: N equal hard disks of radius a in the unit square with elastic walls.
All start with the same speed v_0 in random directions, far from equilibrium.
Free flight over a time step dt, then every overlapping and approaching pair
exchanges the normal component of its relative velocity (equal masses,
elastic), and particles at a wall reverse the normal velocity.  Every such
event conserves the kinetic energy exactly, so the total energy stays at its
initial value N m v_0^2/2 to round-off.

Equilibrium at the same energy, 2D equipartition <m v^2/2> = k_B T:
k_B T = m v_0^2/2, and the speed distribution is

    f(v) = (m v/(k_B T)) exp(-m v^2/(2 k_B T)) = (2 v/v_0^2) exp(-v^2/v_0^2).

The entropy of the velocity distribution per particle,
s/k_B = -int F ln F d^2v with F(v_x, v_y) = f(v)/(2 pi v) and v in v_0,
is estimated from the speed histogram (Miller-Madow correction for the
finite sample); for the Maxwellian it is 1 + ln(pi) = 2.145.  Speeds in v_0,
time t/tau_c, with tau_c the mean time between two collisions of one disk
(measured: t/tau_c is the number of collisions per disk), both with unit [1].
scripts/check-physics.py repeats the energy, histogram and entropy checks.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, AXIS_WIDTH, CURVE_WIDTH, ELECTRON, FAINT, INK, LINEAR, MATH_SIZE, MATH_SMALL, MUTED,
    THIN_WIDTH, StyledScene, axes, dashed, math,
)

HS_N = 600                 # disks
HS_RADIUS = 0.005          # disk radius / box side [1]
HS_DT = 0.0008             # time step [box side / v_0]
HS_STEPS = 640
HS_SAMPLE = 2              # store every 2nd step
HS_SEED = 3
HS_BINS = np.linspace(0.0, 3.0, 31)     # speed bins [v_0]
HS_ENTROPY_MAXWELL = 1.0 + np.log(np.pi)   # -int F ln F d^2v, k_B T = m v_0^2/2


def hs_initial(n=HS_N, seed=HS_SEED):
    """Jittered square lattice, unit speed in uniformly random directions."""
    rng = np.random.default_rng(seed)
    side = int(np.ceil(np.sqrt(n)))
    g = (np.arange(side) + 0.5) / side
    xx, yy = np.meshgrid(g, g)
    pos = np.column_stack([xx.ravel(), yy.ravel()])[:n]
    pos = pos + rng.uniform(-0.25, 0.25, pos.shape) / side
    angle = rng.uniform(0.0, 2 * np.pi, n)
    return pos, np.column_stack([np.cos(angle), np.sin(angle)])


def hs_step(pos, vel, radius=HS_RADIUS, dt=HS_DT):
    """One step: free flight, pair collisions, wall reflections.

    Returns the new arrays and the number of pair collisions.
    """
    pos = pos + dt * vel
    vel = vel.copy()
    d = pos[:, None, :] - pos[None, :, :]
    close = np.triu(np.einsum("ijk,ijk->ij", d, d) < (2 * radius) ** 2, 1)
    hits = 0
    for a, b in zip(*np.nonzero(close)):
        dx = pos[a] - pos[b]
        approach = dx @ (vel[a] - vel[b])
        if approach < 0:
            impulse = approach / (dx @ dx) * dx
            vel[a] -= impulse
            vel[b] += impulse
            hits += 1
    for k in range(2):
        out = ((pos[:, k] < radius) & (vel[:, k] < 0)) | ((pos[:, k] > 1 - radius) & (vel[:, k] > 0))
        vel[out, k] *= -1
    return pos, vel, hits


def hs_run(n=HS_N, steps=HS_STEPS, sample=HS_SAMPLE, seed=HS_SEED):
    """Stored states: positions (k, n, 2), velocities (k, n, 2) and the
    cumulative collisions per particle (k,) at every `sample`-th step."""
    pos, vel = hs_initial(n, seed)
    positions, velocities, clock = [pos], [vel], [0.0]
    hits = 0
    for i in range(1, steps + 1):
        pos, vel, h = hs_step(pos, vel)
        hits += h
        if i % sample == 0:
            positions.append(pos)
            velocities.append(vel)
            clock.append(2.0 * hits / n)
    return np.array(positions), np.array(velocities), np.array(clock)


def maxwell_2d(v):
    """Speed density at k_B T = m v_0^2/2, v in v_0."""
    return 2 * v * np.exp(-v ** 2)


def speed_density(speed, bins=HS_BINS):
    counts, _ = np.histogram(speed, bins)
    return counts / (len(speed) * np.diff(bins))


def velocity_entropy(speed, bins=HS_BINS):
    """-int F ln F d^2v from the speed histogram, Miller-Madow corrected."""
    width = np.diff(bins)
    centre = 0.5 * (bins[1:] + bins[:-1])
    f = speed_density(speed, bins)
    m = f > 0
    s = -np.sum(f[m] * np.log(f[m] / (2 * np.pi * centre[m])) * width[m])
    return s + (m.sum() - 1) / (2 * len(speed))


HIST_TOP = 1.2


class HardSphereRelaxation(StyledScene):
    """Hard disks from one speed to the 2D Maxwellian; histogram and entropy."""

    def build(self):
        positions, velocities, clock = hs_run()
        speeds = np.linalg.norm(velocities, axis=2)
        entropy = np.array([velocity_entropy(s) for s in speeds])
        frames = len(clock)

        # --- the gas ---------------------------------------------------
        side = 5.5
        box = Square(side, color=MUTED, stroke_width=AXIS_WIDTH).move_to([-3.75, -0.15, 0])
        origin = box.get_corner(DL)

        def to_box(p):
            return origin + np.array([p[0] * side, p[1] * side, 0.0])

        dots = VGroup(*[Dot(to_box(p), radius=0.03, color=ELECTRON) for p in positions[0]])
        tracker = ValueTracker(0.0)

        def index():
            return min(int(round(tracker.get_value() * (frames - 1))), frames - 1)

        def move_dots(group):
            for dot, p in zip(group, positions[index()]):
                dot.move_to(to_box(p))

        dots.add_updater(move_dots)

        def y_label(ax, tex, top):
            lab = math(tex, color=MUTED, size=MATH_SMALL).next_to(ax.c2p(0, top), UP, buff=0.15)
            return lab.align_to(ax.c2p(0, top), LEFT).shift(0.35 * LEFT)

        def x_label(ax, tex, right):
            lab = math(tex, color=MUTED, size=MATH_SMALL).next_to(ax.c2p(right, 0), DOWN, buff=0.12)
            return lab.align_to(ax.c2p(right, 0), RIGHT)

        def ticks(ax, values, axis):
            if axis == "x":
                return VGroup(*[math(str(v), color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                                for v in values])
            return VGroup(*[math(str(v), color=MUTED, size=MATH_SMALL).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                            for v in values])

        # --- speed histogram -----------------------------------------
        hx = axes([0, 3, 1], [0, HIST_TOP, 0.5], 5.3, 2.3).move_to([3.65, 1.35, 0])
        hx_ticks = ticks(hx, (0, 1, 2), "x")
        hy_ticks = ticks(hx, (0, 1), "y")
        hx_lab = x_label(hx, r"v/v_0\ [1]", 3)
        hy_lab = y_label(hx, r"f(v)\,v_0\ [1]", HIST_TOP)
        maxwell = dashed(hx.plot(maxwell_2d, x_range=[0.0, 3.0, 0.02], color=ACCENT,
                                 stroke_width=CURVE_WIDTH), num_dashes=45)
        maxwell_lab = math(r"2v\,e^{-v^2/v_0^2}/v_0^2", color=ACCENT, size=MATH_SMALL).move_to(hx.c2p(2.2, 0.85))
        bins = HS_BINS

        def histogram():
            f = speed_density(speeds[index()])
            bars = VGroup()
            for k, h in enumerate(f):
                if h <= 0:
                    continue
                lo, hi = hx.c2p(bins[k], 0), hx.c2p(bins[k + 1], min(h, HIST_TOP))
                bars.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=1.0,
                                   stroke_color=ELECTRON, fill_color=ELECTRON, fill_opacity=0.45)
                         .move_to((lo + hi) / 2))
            return bars

        bars = always_redraw(histogram)

        # --- entropy trace ------------------------------------------
        c_max = float(np.ceil(clock[-1]))
        sx = axes([0, c_max, 1], [0, 2.4, 1], 5.3, 1.75).move_to([3.65, -2.0, 0])
        sx_ticks = ticks(sx, (0, int(c_max)), "x")
        sy_ticks = ticks(sx, (0, 1, 2), "y")
        sx_lab = math(r"t/\tau_c\ [1]", color=MUTED, size=MATH_SMALL).next_to(sx.c2p(c_max / 2, 0), DOWN, buff=0.12)
        sy_lab = y_label(sx, r"\textstyle -\!\int F\ln F\,d^2v\ [1]", 2.4)
        level = dashed(Line(sx.c2p(0, HS_ENTROPY_MAXWELL), sx.c2p(c_max, HS_ENTROPY_MAXWELL),
                            color=ACCENT, stroke_width=THIN_WIDTH), num_dashes=40)
        level_lab = math(r"1+\ln\pi", color=ACCENT, size=MATH_SMALL).next_to(sx.c2p(c_max, HS_ENTROPY_MAXWELL), DOWN, buff=0.12).shift(0.55 * LEFT)

        def trace():
            i = index()
            if i < 1:
                return VMobject()
            pts = [sx.c2p(clock[k], entropy[k]) for k in range(i + 1)]
            return VMobject().set_points_as_corners(pts).set_stroke(ELECTRON, CURVE_WIDTH - 1.0)

        s_trace = always_redraw(trace)

        # --- labels -------------------------------------------------
        title = math(r"\mathrm{hard\ disks,}\ |\mathbf{v}|=v_0\ \mathrm{at}\ t=0", color=MUTED, size=MATH_SMALL)
        title.next_to(box, UP, buff=0.15).align_to(box, LEFT)
        e_total = 0.5 * np.sum(speeds ** 2, axis=1)
        drift = np.abs(e_total / e_total[0] - 1).max()
        energy = math(rf"|E/E_0-1|<10^{{{int(np.ceil(np.log10(max(drift, 1e-16))))}}}",
                      color=MUTED, size=MATH_SMALL).next_to(box, DOWN, buff=0.15).align_to(box, LEFT)
        clock_lab = math(r"t/\tau_c=", color=MUTED, size=MATH_SMALL)
        clock_lab.next_to(box, DOWN, buff=0.15).align_to(box, RIGHT).shift(0.75 * LEFT)
        clock_num = DecimalNumber(0.0, num_decimal_places=1, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            m.set_value(clock[index()])
            m.next_to(clock_lab, RIGHT, buff=0.12)

        clock_num.add_updater(place_clock)
        place_clock(clock_num)

        self.add(box, dots, title, energy, clock_lab, clock_num,
                 hx, hx_ticks, hx_lab, hy_lab, hy_ticks, bars,
                 sx, sx_ticks, sx_lab, sy_ticks, sy_lab, s_trace)
        self.wait(1.0)
        self.play(tracker.animate.set_value(0.5), run_time=10.0, rate_func=LINEAR)
        self.play(Create(maxwell), FadeIn(maxwell_lab), Create(level), FadeIn(level_lab), run_time=1.0)
        self.play(tracker.animate.set_value(1.0), run_time=7.0, rate_func=LINEAR)
        self.wait(1.5)
