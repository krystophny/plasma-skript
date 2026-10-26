"""Frozen-in flux against magnetic diffusion: a magnetic loop in a vortex.

Model: two-dimensional resistive induction for an in-plane field
B = grad A_z x e_z, written for the flux function A_z,

    dA_z/dt + u . grad A_z = D_B laplacian A_z ,      D_B = eta/mu_0 ,

on a periodic square of side 2 pi L, solved pseudo-spectrally (2/3
dealiasing, RK4 for advection, exact integrating factor for diffusion).  The
flow is prescribed and incompressible, the cellular vortex
u = curl(psi e_z) with stream function psi = U L sin(x/L) sin(y/L), which
turns faster near the cell centre than further out and so winds up whatever
it carries.  Initial state: a Gaussian A_z = A_0 exp(-r^2/(2 sigma^2)) of
width sigma = 0.35 L centred 0.55 L to the right of the cell centre, i.e. a
loop of closed circular field lines (an O-point).  The contours of A_z are
the field lines, and A_z(p_2) - A_z(p_1) is the magnetic flux (per unit
length in z) between the field lines through p_1 and p_2.

Normalization: x/L, y/L and t U/L carry unit [1]; A_z/A_0 [1].  The magnetic
Reynolds number R_m = U L/D_B is 10^4 in the first run and 10 in the second,
from the same initial state.  Twenty-four fluid elements start on the field
line A_z = A_0/2 and are moved with u (RK4, analytic velocity).

Checks (scripts/check-physics.py repeats them independently):
* R_m = 10^4: A_z interpolated spectrally at the fluid elements stays at
  A_0/2 (flux between each element and the O-point is conserved), and the
  O-point value max A_z stays at A_0.
* u = 0 with a single Fourier mode: the amplitude decays as
  exp(-D_B k^2 t); the measured e-folding time equals 1/(D_B k^2).
"""

from manim import *
import numpy as np

from style import (
    ACCENT, AXIS, AXIS_WIDTH, B_FIELD, CURVE_WIDTH, EASE, FAINT, GRID, INK,
    LINEAR, MUTED, THIN_WIDTH, StyledScene, axes, axis_labels, label, math,
    MATH_SIZE, MATH_SMALL, SMALL_SIZE,
)


N_GRID = 192                    # grid points per side of the 2 pi L box
SIGMA = 0.35                    # loop width / L [1]
OFFSET = 0.55                   # loop centre right of the cell centre / L [1]
T_END = 8.0                     # run time t U/L [1]
DT = 0.01                       # time step t U/L [1]
FRAMES = 81                     # stored states per run
REYNOLDS = (1.0e4, 10.0)       # R_m = U L/D_B of the two runs [1]
N_TRACERS = 24
TRACER_LEVEL = 0.5              # A_z/A_0 on the traced field line [1]
LEVELS = (0.03, 0.1, 0.3, 0.5, 0.8)    # drawn field lines A_z/A_0 [1]


def grid(n=N_GRID):
    """Periodic grid x/L in [0, 2 pi) and integer wave numbers k L."""
    x = 2 * np.pi * np.arange(n) / n
    k = np.fft.fftfreq(n, 1.0 / n)
    return x, k


def velocity(x, y):
    """u/U = curl(sin x sin y e_z) = (sin x cos y, -cos x sin y)."""
    return np.sin(x) * np.cos(y), -np.cos(x) * np.sin(y)


def initial_flux(x, y, sigma=SIGMA, offset=OFFSET):
    """Gaussian A_z/A_0 centred at (pi/2 + offset, pi/2)."""
    r2 = (x - np.pi / 2 - offset) ** 2 + (y - np.pi / 2) ** 2
    return np.exp(-r2 / (2 * sigma**2))


def tracer_start(n=N_TRACERS, level=TRACER_LEVEL, sigma=SIGMA, offset=OFFSET):
    """Fluid elements on the initial field line A_z = level A_0."""
    r = sigma * np.sqrt(-2 * np.log(level))
    phi = 2 * np.pi * np.arange(n) / n
    return np.stack([np.pi / 2 + offset + r * np.cos(phi), np.pi / 2 + r * np.sin(phi)], axis=1)


def interpolate(a_hat, points):
    """Spectral (exact trigonometric) interpolation of A_z at points (m, 2)."""
    n = a_hat.shape[0]
    _, k = grid(n)
    ex = np.exp(1j * np.outer(points[:, 0], k))           # (m, n)
    ey = np.exp(1j * np.outer(points[:, 1], k))
    return np.real(np.einsum("mi,ij,mj->m", ey, a_hat, ex)) / n**2


def advance_tracers(p, dt, flow=1.0):
    """One RK4 step of dx/dt = u(x)."""
    def f(q):
        return flow * np.stack(velocity(q[:, 0], q[:, 1]), axis=1)
    k1 = f(p)
    k2 = f(p + 0.5 * dt * k1)
    k3 = f(p + 0.5 * dt * k2)
    k4 = f(p + dt * k3)
    return p + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6


def solve(diffusivity, a0=None, flow=1.0, t_end=T_END, dt=DT, frames=FRAMES, n=N_GRID,
          tracers=None):
    """Integrate the induction equation for A_z.

    diffusivity is D_B/(U L) = 1/R_m, flow scales the vortex (0 switches it
    off).  Returns times, A_z frames (frames, n, n) indexed [y, x], tracer
    positions (frames, m, 2) and A_z/A_0 at the tracers (frames, m).
    """
    x, k = grid(n)
    xx, yy = np.meshgrid(x, x)
    kx, ky = np.meshgrid(k, k)
    k2 = kx**2 + ky**2
    dealias = (np.abs(kx) < n / 3) & (np.abs(ky) < n / 3)
    ux, uy = velocity(xx, yy)
    ux, uy = flow * ux, flow * uy
    a_hat = np.fft.fft2(initial_flux(xx, yy) if a0 is None else a0)
    p = tracer_start() if tracers is None else tracers.copy()
    decay_half = np.exp(-diffusivity * k2 * dt / 2)

    def rhs(h):
        ax = np.real(np.fft.ifft2(1j * kx * h))
        ay = np.real(np.fft.ifft2(1j * ky * h))
        return -np.fft.fft2(ux * ax + uy * ay) * dealias

    steps = int(round(t_end / dt))
    save_every = steps // (frames - 1)
    times, states, paths, values = [], [], [], []
    for step in range(steps + 1):
        if step % save_every == 0:
            times.append(step * dt)
            states.append(np.real(np.fft.ifft2(a_hat)))
            paths.append(p.copy())
            values.append(interpolate(a_hat, p))
        if step == steps:
            break
        # Integrating factor: exact diffusion over half steps around RK4 advection.
        if flow:
            h = a_hat * decay_half
            k1 = rhs(h)
            k2 = rhs(h + 0.5 * dt * k1)
            k3 = rhs(h + 0.5 * dt * k2)
            k4 = rhs(h + dt * k3)
            a_hat = (h + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6) * decay_half
            p = advance_tracers(p, dt, flow)
        else:
            a_hat = a_hat * decay_half**2
    return np.array(times), np.array(states), np.array(paths), np.array(values)


def mode_decay_time(diffusivity, mode=(2, 1), t_end=2.0, n=32):
    """e-folding time of a single Fourier mode of A_z without flow."""
    x, _ = grid(n)
    xx, yy = np.meshgrid(x, x)
    a0 = np.cos(mode[0] * xx + mode[1] * yy)
    t, states, _, _ = solve(diffusivity, a0=a0, flow=0.0, t_end=t_end, dt=0.01,
                            frames=21, n=n, tracers=np.zeros((1, 2)))
    amplitude = np.array([np.max(np.abs(s)) for s in states])
    slope = np.polyfit(t, np.log(amplitude), 1)[0]
    return -1.0 / slope


def contour_paths(field, level, x):
    """Field-line polylines A_z = level (marching squares, field[y, x]).

    Each crossing lies on a grid edge, found by linear interpolation; cells
    link the crossings on their edges, and chains of links are the lines.
    """
    f = field - level
    ny, nx = f.shape
    points, index = [], {}

    def crossing(key):
        if key not in index:
            kind, j, i = key
            if kind == 0:                                   # edge (j, i)-(j, i+1)
                a, b = f[j, i], f[j, i + 1]
                s = a / (a - b)
                points.append((x[i] + s * (x[i + 1] - x[i]), x[j]))
            else:                                           # edge (j, i)-(j+1, i)
                a, b = f[j, i], f[j + 1, i]
                s = a / (a - b)
                points.append((x[i], x[j] + s * (x[j + 1] - x[j])))
            index[key] = len(points) - 1
        return index[key]

    above = f > 0
    links = {}
    corners = above[:-1, :-1].astype(int) + above[:-1, 1:] + above[1:, :-1] + above[1:, 1:]
    for j, i in zip(*np.nonzero((corners > 0) & (corners < 4))):
            edges = []
            if above[j, i] != above[j, i + 1]:
                edges.append((0, j, i))
            if above[j + 1, i] != above[j + 1, i + 1]:
                edges.append((0, j + 1, i))
            if above[j, i] != above[j + 1, i]:
                edges.append((1, j, i))
            if above[j, i + 1] != above[j + 1, i + 1]:
                edges.append((1, j, i + 1))
            if len(edges) == 2:
                pairs = [edges]
            elif len(edges) == 4:                           # saddle: pair by centre value
                centre = f[j:j + 2, i:i + 2].mean() > 0
                bottom, top, left, right = edges
                pairs = [[bottom, left], [top, right]] if centre != above[j, i] else \
                    [[bottom, right], [top, left]]
            else:
                pairs = []
            for a, b in pairs:
                ia, ib = crossing(a), crossing(b)
                links.setdefault(ia, []).append(ib)
                links.setdefault(ib, []).append(ia)
    lines, seen = [], set()
    ends = [p for p, n in links.items() if len(n) == 1]
    for start in ends + list(links):
        if start in seen:
            continue
        chain, prev, cur = [start], None, start
        seen.add(start)
        while True:
            nxt = [n for n in links[cur] if n != prev and n not in seen]
            if not nxt:
                if len(chain) > 2 and start in links[cur]:
                    chain.append(start)                     # closed line
                break
            prev, cur = cur, nxt[0]
            seen.add(cur)
            chain.append(cur)
        lines.append(np.array([points[c] for c in chain]))
    return lines


def stream_line(level, n=160):
    """Closed streamline sin x sin y = level in the cell [0, pi]^2."""
    x0 = np.arcsin(level)
    x = x0 + (np.pi - 2 * x0) * 0.5 * (1 - np.cos(np.linspace(0, np.pi, n)))
    y = np.arcsin(np.clip(level / np.sin(x), -1, 1))
    return np.concatenate([np.stack([x, y], 1), np.stack([x[::-1], np.pi - y[::-1]], 1)])


class FrozenFlux(StyledScene):
    """Same loop, same vortex: R_m = 10^4 (frozen) then R_m = 10 (diffusing)."""

    def build(self):
        x, _ = grid()
        cell = x <= np.pi + 1e-9
        xc = x[cell]
        side = 6.2
        origin = np.array([-6.05, -3.45, 0])          # lower left of the cell

        def to_scene(px, py):
            return origin + np.array([px, py, 0]) * side / np.pi

        frame = Square(side, color=GRID, stroke_width=AXIS_WIDTH).move_to(to_scene(np.pi / 2, np.pi / 2))
        ticks = VGroup()
        for v, txt in ((0, "0"), (np.pi / 2, r"\pi/2"), (np.pi, r"\pi")):
            ticks.add(math(txt, color=MUTED, size=MATH_SMALL).next_to(to_scene(v, 0), DOWN, buff=0.14))
            ticks.add(math(txt, color=MUTED, size=MATH_SMALL).next_to(to_scene(0, v), LEFT, buff=0.14))
        x_lab = math(r"x/L\ [1]", color=MUTED, size=MATH_SMALL).next_to(to_scene(np.pi * 0.78, 0), DOWN, buff=0.14)
        y_lab = math(r"y/L\ [1]", color=MUTED, size=MATH_SMALL).rotate(PI / 2).next_to(to_scene(0, np.pi * 0.78), LEFT, buff=0.16)

        # Dashed streamlines of the prescribed vortex (psi = const).
        streams = VGroup()
        for level in (0.2, 0.5, 0.8):
            pts = [to_scene(*q) for q in stream_line(level)]
            streams.add(DashedVMobject(VMobject(stroke_color=FAINT, stroke_width=1.6,
                                                stroke_opacity=0.7).set_points_as_corners(pts),
                                       num_dashes=40))
        arrow = Arrow(to_scene(0.55, 1.9), to_scene(0.55, 1.2), buff=0, color=FAINT,
                      stroke_width=3, max_tip_length_to_length_ratio=0.25)
        u_lab = math(r"\mathbf u", color=FAINT, size=MATH_SMALL).next_to(arrow, LEFT, buff=0.1)

        # Right panel: A_z at the fluid elements against time.
        ax = axes([0, T_END, 2], [0, 1.2, 0.5], 4.4, 2.2).move_to([4.15, -2.05, 0])
        ax_labels = axis_labels(ax, r"tU/L\ [1]", r"\langle A_z\rangle_{\rm elements}/A_z^{(0)}\ [1]")
        tick_labels = VGroup(
            *[math(str(v), color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
              for v in (0, 4)],
            *[math(t, color=MUTED, size=MATH_SMALL).next_to(ax.c2p(0, v), LEFT, buff=0.12)
              for v, t in ((0, "0"), (1, "1"))])
        one = DashedLine(ax.c2p(0, 1), ax.c2p(T_END, 1), color=GRID, stroke_width=THIN_WIDTH)

        law = math(r"\partial_t A_z + \mathbf u\cdot\nabla A_z = D_B\nabla^2 A_z",
                   size=MATH_SMALL).move_to([3.95, 3.15, 0])
        rm_def = math(r"R_m = UL/D_B", color=MUTED, size=MATH_SMALL).next_to(law, DOWN, buff=0.2)
        key = VGroup(
            Line(ORIGIN, RIGHT * 0.5, color=B_FIELD, stroke_width=THIN_WIDTH + 0.6),
            label("field lines", size=SMALL_SIZE),
            Triangle(color=ACCENT, fill_opacity=1, stroke_width=0).scale(0.09),
            label("fluid elements", size=SMALL_SIZE),
        )
        key = VGroup(VGroup(key[0], key[1]).arrange(RIGHT, buff=0.18),
                     VGroup(key[2], key[3]).arrange(RIGHT, buff=0.18)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(rm_def, DOWN, buff=0.22)
        key[1][0].match_x(key[0][0])
        key[1][1].next_to(key[1][0], RIGHT, buff=0.18).align_to(key[0][1], LEFT)

        runs = [solve(1.0 / rm) for rm in REYNOLDS]
        styles = [(INK, 1.0), (ACCENT, 0.0)]
        tracker = ValueTracker(0.0)

        def frame_index():
            return min(int(round(tracker.get_value() / T_END * (FRAMES - 1))), FRAMES - 1)

        def field_lines(run):
            def draw():
                _, states, _, _ = run
                f = states[frame_index()][np.ix_(cell, cell)]
                group = VGroup()
                for level in LEVELS:
                    width = CURVE_WIDTH if level == TRACER_LEVEL else THIN_WIDTH
                    for line in contour_paths(f, level, xc):
                        if len(line) < 3:
                            continue
                        group.add(VMobject(stroke_color=B_FIELD, stroke_width=width)
                                  .set_points_as_corners([to_scene(*q) for q in line]))
                return group
            return always_redraw(draw)

        def elements(run):
            def draw():
                _, _, paths, _ = run
                return VGroup(*[Triangle(color=ACCENT, fill_opacity=1, stroke_color=BLACK, stroke_width=1)
                                .scale(0.085).move_to(to_scene(*q)) for q in paths[frame_index()]])
            return always_redraw(draw)

        def history(run, color, dash):
            def draw():
                times, _, _, values = run
                i = frame_index()
                mean = values[: i + 1].mean(axis=1) / TRACER_LEVEL
                pts = [ax.c2p(t, v) for t, v in zip(times[: i + 1], mean)]
                if len(pts) < 2:
                    pts = [ax.c2p(0, 1), ax.c2p(1e-3, 1)]
                curve = VMobject(stroke_color=color, stroke_width=CURVE_WIDTH - 0.5).set_points_as_corners(pts)
                return DashedVMobject(curve, num_dashes=max(2, 3 * i // 4 + 2)) if dash else curve
            return always_redraw(draw)

        def clock():
            return math(rf"tU/L = {tracker.get_value():.1f}", color=MUTED, size=MATH_SMALL) \
                .next_to(frame, UP, buff=0.18).align_to(frame, RIGHT)

        self.play(Create(frame), FadeIn(ticks, x_lab, y_lab, streams, arrow, u_lab),
                  run_time=1.0, rate_func=EASE)
        self.play(FadeIn(law, rm_def, key), Create(ax), FadeIn(ax_labels, tick_labels, one),
                  run_time=1.0, rate_func=EASE)
        clock_mob = always_redraw(clock)

        def peak(run):
            def draw():
                value = run[1][frame_index()].max()
                return math(rf"\max A_z/A_0 = {value:.2f}", color=MUTED, size=MATH_SMALL) \
                    .move_to([4.15, 0.3, 0])
            return always_redraw(draw)
        finished = []
        for r, (run, rm) in enumerate(zip(runs, REYNOLDS)):
            tracker.set_value(0.0)
            case = VGroup(
                math(r"R_m = 10^4" if r == 0 else r"R_m = 10", color=INK, size=MATH_SIZE)
                .next_to(frame, UP, buff=0.12).align_to(frame, LEFT),
                label("field lines move with the fluid" if r == 0 else "field slips and diffuses",
                      color=INK, size=SMALL_SIZE).move_to([4.15, 0.85, 0]))
            lines, dots = field_lines(run), elements(run)
            curve = history(run, *(INK, False) if r == 0 else (ACCENT, True))
            peak_mob = peak(run)
            self.play(FadeIn(case), FadeIn(lines), FadeIn(dots), FadeIn(clock_mob), FadeIn(peak_mob),
                      run_time=0.6)
            self.add(curve)
            self.wait(0.6)
            self.play(tracker.animate.set_value(T_END), run_time=8.0, rate_func=LINEAR)
            self.wait(1.2)
            curve.clear_updaters()
            finished.append(curve)
            if r == 0:
                end_label = math(r"R_m=10^4", color=INK, size=MATH_SMALL) \
                    .next_to(ax.c2p(T_END, 1), UP, buff=0.12).align_to(ax.c2p(T_END, 0), RIGHT)
                self.play(FadeOut(case), FadeOut(lines), FadeOut(dots), FadeOut(clock_mob), FadeOut(peak_mob),
                          curve.animate.set_stroke(opacity=0.8), FadeIn(end_label), run_time=0.6)
            else:
                values = run[3]
                end_val = values[-1].mean() / TRACER_LEVEL
                low_label = math(r"R_m=10", color=ACCENT, size=MATH_SMALL) \
                    .next_to(ax.c2p(T_END, end_val), UP, buff=0.12).align_to(ax.c2p(T_END, 0), RIGHT)
                self.play(FadeIn(low_label), run_time=0.5)
                self.wait(1.5)
