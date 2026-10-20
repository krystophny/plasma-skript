"""Weak and strong coupling: a test electron and its Debye circle.

Model (classical, nonrelativistic): a one-component plasma of electrons with
a uniform positive neutralizing background, frozen in place (Lorentz-gas
picture; the frozen charges do not move and do not screen).  Lengths are in
units of the mean spacing a = n_0^(-1/3), time in a/v_th with the thermal
speed v_th = sqrt(2 k_B T_e/m_e) of the script, energies in k_B T_e.  The
coupling parameter Gamma_e = e^2/(4 pi epsilon_0 a k_B T_e) = a^2/(4 pi
lambda_D^2) is the only parameter; it fixes the Debye length
lambda_D/a = 1/sqrt(4 pi Gamma_e).  A test electron at x then moves with

    d^2 x/dt^2 = (Gamma_e/2) [sum_j (x - x_j)/|x - x_j|^3 - (4 pi/3) x]

(bare Coulomb repulsion by every frozen electron, no softening, and the
attraction of the uniform background sphere), and conserves
E/(k_B T_e) = |v|^2 + Gamma_e [sum_j 1/|x - x_j| - (2 pi/3)(3 R^2 - |x|^2)].

Frozen positions: one electron at a seeded uniform random point of every
cubic cell of side a with 0 < z < a, ..., whose centre lies inside radius
RADIUS_CELLS, plus the mirror images z -> -z.  The density is exactly 1/a^3
and the cells are neutral on the scale a, so the frozen configuration has no
long-wavelength charge fluctuations.  The background is the uniform sphere
of the same total charge, (4 pi/3) R^3 = N.  The mirror symmetry makes the
force on a particle in the plane z = 0 lie in that plane, so the path stays
exactly in the drawing plane.  One test electron starts at the thermal
speed along +x from a point in a potential valley (U <= 0, at least 0.5 a
from every frozen electron, as for an electron with its own correlation
hole); SEED and LAUNCH_Y were chosen among such launch points whose paths
stay inside the drawn window and do not run back over the launch arrow,
with no drawn electron within 0.4 a of the
launch point in projection or on the launch arrow, and with a free spot for
the lambda_D label of the still.

Both panels use the same frozen positions, launch point, window and clock;
only Gamma_e differs: Gamma_e = 0.08 (lambda_D = 1.00 a, strong coupling:
single neighbours deflect the electron by radians) and Gamma_e = 0.009
(lambda_D = 2.97 a, weak coupling: a nearly straight path).  The drawn
frozen electrons are those of the slab 0 < z < a (areal density 1/a^2);
deeper ones act but are not drawn.  A circle of radius lambda_D moves with
the test electron; drawn electrons inside it (in projection) are blue, the
others grey, so about pi (lambda_D/a)^2 electrons are blue: about 3 versus
about 28.  The same frame at t = 0 is the still on the coupling slide
(slides/coupling-still.json, scripts/export-coupling-still.py).  The orbits
are integrated with an adaptive Dormand-Prince 5(4) scheme to a relative
tolerance of 1e-10 and sampled every DT_OUT; the drawn trace is a polyline
through these samples.
"""

from manim import *
import numpy as np

from style import (
    AXIS_WIDTH, CURVE_WIDTH, EASE, ELECTRON, GRID, INK, ION, LINEAR, MUTED, THIN_WIDTH,
    StyledScene, label, math, MATH_SMALL, SMALL_SIZE,
)

SEED = 14
RADIUS_CELLS = 9.0
LAUNCH_X = -3.5
LAUNCH_Y = (0.65,)
T_END = 7.0
DT_OUT = 0.02
TOLERANCE = 1e-10
GAMMAS = (0.08, 0.009)
WINDOW = (-7.6, 4.4, -4.5, 4.5)     # x_min, x_max, y_min, y_max in units of a
SHOWN_MARGIN = 0.12                 # drawn frozen electrons keep this distance to the frame
# lambda_D label of the still (slides at 125 mm per 12 a): half size and clearance in a.
LABEL_HALF = (0.36, 0.36)
LABEL_CLEAR = 0.12

PANEL_W = 6.2
PANEL_GAP = 0.5
PLAY_TIME = 10.5
HOLD = 2.5


def frozen_charges(seed=SEED, radius_cells=RADIUS_CELLS):
    """Seeded frozen electrons, one per cubic cell of side a, mirror-symmetric in z.

    Every lattice cell [i, i+1] x [j, j+1] x [k, k+1] with k >= 0 and centre
    inside radius_cells holds one electron at a uniform random point; the
    mirror images z -> -z fill k < 0.  Returns positions (N, 3) in units of a
    and the radius R of the neutralizing sphere, (4 pi/3) R^3 = N.
    """
    rng = np.random.default_rng(seed)
    m = int(np.ceil(radius_cells))
    i, j, k = np.meshgrid(np.arange(-m, m), np.arange(-m, m), np.arange(0, m), indexing="ij")
    corner = np.column_stack([i.ravel(), j.ravel(), k.ravel()]).astype(float)
    corner = corner[np.linalg.norm(corner + 0.5, axis=1) < radius_cells]
    upper = corner + rng.uniform(size=corner.shape)
    charges = np.concatenate([upper, upper * [1.0, 1.0, -1.0]])
    radius = (3 * len(charges) / (4 * np.pi)) ** (1 / 3)
    return charges, radius


def debye_radius(gamma):
    """lambda_D/a from Gamma_e = a^2/(4 pi lambda_D^2)."""
    return 1.0 / np.sqrt(4 * np.pi * gamma)


def shown_charges(charges, window=WINDOW, margin=SHOWN_MARGIN):
    """Drawn frozen electrons: the slab 0 < z < a inside the window, as (M, 2)."""
    x_min, x_max, y_min, y_max = window
    keep = ((charges[:, 2] > 0) & (charges[:, 2] < 1)
            & (charges[:, 0] > x_min + margin) & (charges[:, 0] < x_max - margin)
            & (charges[:, 1] > y_min + margin) & (charges[:, 1] < y_max - margin))
    return charges[keep, :2]


def inside_debye_circle(points, centre, gamma):
    """Drawn electrons within lambda_D of the test electron, in projection."""
    return np.hypot(points[:, 0] - centre[0], points[:, 1] - centre[1]) < debye_radius(gamma)


def label_angle(points, centre, gamma, window=WINDOW, half=LABEL_HALF, clear=LABEL_CLEAR):
    """Direction (degrees) of the drawn radius whose outer label touches no dot.

    The label box (half sizes `half`) sits just outside the circle along the
    radius; no drawn electron may lie within `clear` of the box or of the
    radius line, and the box stays inside the window.  Among the free
    directions the one closest to 45 degrees is returned.
    """
    lam = debye_radius(gamma)
    x_min, x_max, y_min, y_max = window
    for step in range(0, 181):
        for theta in sorted({45 + step, 45 - step}):
            u = np.array([np.cos(np.radians(theta)), np.sin(np.radians(theta))])
            reach = lam + half[0] * abs(u[0]) + half[1] * abs(u[1]) + 0.08
            c = np.asarray(centre) + reach * u
            if not (x_min + half[0] < c[0] < x_max - half[0]
                    and y_min + half[1] < c[1] < y_max - half[1]):
                continue
            box = np.all(np.abs(points - c) < np.array(half) + clear, axis=1)
            d = points - np.asarray(centre)
            along = d @ u
            across = np.abs(d[:, 0] * u[1] - d[:, 1] * u[0])
            line = (along > 0) & (along < lam) & (across < clear)
            if not box.any() and not line.any():
                return float(theta % 360)
    raise ValueError(f"Gamma_e = {gamma}: no free direction for the lambda_D label")


def still_data(seed=SEED):
    """Launch frame shared by the animation and the coupling slide (units of a)."""
    charges, _ = frozen_charges(seed)
    points = shown_charges(charges)
    centre = (LAUNCH_X, LAUNCH_Y[0])
    panels = []
    for gamma in GAMMAS:
        panels.append({
            "gamma": gamma,
            "lambda": round(float(debye_radius(gamma)), 4),
            "angle": label_angle(points, centre, gamma),
            "inside": [bool(b) for b in inside_debye_circle(points, centre, gamma)],
        })
    return {"window": list(WINDOW), "centre": list(centre),
            "points": [[round(float(x), 4), round(float(y), 4)] for x, y in points],
            "panels": panels}


def potential_energy(x, charges, radius, gamma):
    """U/(k_B T) of test electrons at x (P, 3): bare Coulomb + uniform sphere."""
    d = x[:, None, :] - charges[None, :, :]
    r = np.sqrt(np.sum(d * d, axis=2))
    background = -gamma * (2 * np.pi / 3) * (3 * radius**2 - np.sum(x * x, axis=1))
    return gamma * np.sum(1 / r, axis=1) + background


def acceleration(x, charges, gamma):
    """d^2 x/dt^2 in units of a (v_th/a)^2, equal to -grad(U/k_B T)/2."""
    dx = x[:, 0:1] - charges[None, :, 0]
    dy = x[:, 1:2] - charges[None, :, 1]
    dz = x[:, 2:3] - charges[None, :, 2]
    r2 = dx * dx + dy * dy + dz * dz
    w = 1.0 / (r2 * np.sqrt(r2))
    coulomb = np.column_stack([(dx * w).sum(axis=1), (dy * w).sum(axis=1), (dz * w).sum(axis=1)])
    return 0.5 * gamma * (coulomb - (4 * np.pi / 3) * x)


def energy(x, v, charges, radius, gamma):
    """E/(k_B T) = |v/v_th|^2 + U/(k_B T)."""
    return np.sum(v * v, axis=1) + potential_energy(x, charges, radius, gamma)


# Dormand-Prince 5(4) tableau.
DP_A = (
    (),
    (1 / 5,),
    (3 / 40, 9 / 40),
    (44 / 45, -56 / 15, 32 / 9),
    (19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729),
    (9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656),
    (35 / 384, 0.0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84),
)
DP_B5 = (35 / 384, 0.0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0.0)
DP_B4 = (5179 / 57600, 0.0, 7571 / 16695, 393 / 640, -92097 / 339200, 187 / 2100, 1 / 40)


def trajectories(gamma, launch_y=LAUNCH_Y, t_end=T_END, dt_out=DT_OUT, tol=TOLERANCE,
                 seed=SEED, launch_x=LAUNCH_X):
    """Adaptive Dormand-Prince orbits of test electrons, sampled every dt_out.

    Launch at (launch_x, y, 0) with velocity v_th along +x.  All test
    electrons share the step size (error norm over all of them); steps end on
    the sample times.  Returns times (K,), positions (K, P, 3), velocities
    (K, P, 3) and the number of accepted steps.
    """
    charges, _ = frozen_charges(seed)
    p = len(launch_y)
    y = np.column_stack([np.full(p, launch_x), np.asarray(launch_y, float), np.zeros(p),
                         np.ones(p), np.zeros(p), np.zeros(p)])

    def rhs(state):
        return np.concatenate([state[:, 3:], acceleration(state[:, :3], charges, gamma)], axis=1)

    times = np.arange(0.0, t_end + 0.5 * dt_out, dt_out)
    out = np.empty((len(times), p, 6))
    out[0] = y
    t, h, steps = 0.0, 1e-3, 0
    for k in range(1, len(times)):
        while t < times[k]:
            h_try = min(h, times[k] - t)
            stages = []
            for row in DP_A:
                s = y.copy()
                for a, kk in zip(row, stages):
                    s += h_try * a * kk
                stages.append(rhs(s))
            y5 = y + h_try * sum(b * kk for b, kk in zip(DP_B5, stages))
            y4 = y + h_try * sum(b * kk for b, kk in zip(DP_B4, stages))
            scale = 1.0 + np.maximum(np.abs(y), np.abs(y5))
            err = np.max(np.abs(y5 - y4) / scale) / tol
            if err <= 1.0:
                t += h_try
                y = y5
                steps += 1
            h = h_try * min(5.0, max(0.2, 0.9 * (err + 1e-300) ** -0.2))
        out[k] = y
    return times, out[:, :, :3], out[:, :, 3:], steps


def deflection_angles(v):
    """Angle between the final and the initial (+x) velocity, radians, per particle."""
    final = v[-1]
    return np.arccos(np.clip(final[:, 0] / np.linalg.norm(final, axis=1), -1.0, 1.0))


class CouplingTestParticle(StyledScene):
    """Gamma_e = 0.08 and 0.009 side by side: same electrons, launch point and clock."""

    def build(self):
        charges, _ = frozen_charges()
        still = still_data()
        x_min, x_max, y_min, y_max = WINDOW
        scale = PANEL_W / (x_max - x_min)
        panel_h = (y_max - y_min) * scale
        centers = [np.array([-(PANEL_W + PANEL_GAP) / 2, 0.15, 0]),
                   np.array([(PANEL_W + PANEL_GAP) / 2, 0.15, 0])]
        points = shown_charges(charges)
        lams = [debye_radius(g) for g in GAMMAS]
        angles = [np.radians(panel["angle"]) for panel in still["panels"]]

        runs = []
        for gamma, lam in zip(GAMMAS, lams):
            times, pos, _, _ = trajectories(gamma)
            inside = ((pos[..., 0] > x_min + 0.2) & (pos[..., 0] < x_max - 0.2)
                      & (pos[..., 1] > y_min + 0.2) & (pos[..., 1] < y_max - 0.2))
            if not inside.all():
                raise ValueError(f"Gamma_e = {gamma}: the path leaves the drawn window")
            runs.append(pos[:, 0, :2])
        samples = len(times)

        def to_panel(p, x, y):
            mid = np.array([(x_min + x_max) / 2, (y_min + y_max) / 2])
            return centers[p] + np.array([x - mid[0], y - mid[1], 0.0]) * scale

        def in_window(xy):
            return (x_min <= xy[0] <= x_max) and (y_min <= xy[1] <= y_max)

        # Static layer: background, frame.
        panels = VGroup()
        for p in range(2):
            background = Rectangle(width=PANEL_W, height=panel_h, stroke_width=0,
                                   fill_color=ION, fill_opacity=0.10).move_to(centers[p])
            frame = Rectangle(width=PANEL_W, height=panel_h, color=GRID,
                              stroke_width=AXIS_WIDTH).move_to(centers[p])
            panels.add(VGroup(background, frame))

        titles = VGroup()
        for p, (gamma, lam, name) in enumerate(zip(GAMMAS, lams, ("strong", "weak"))):
            n = int(round(lam))
            length = "a" if n == 1 else f"{n}a"
            title = MathTex(rf"\Gamma_e={gamma:g},\ \lambda_D\approx {length}",
                            rf"\quad\text{{{name}}}", color=INK, font_size=MATH_SMALL + 4)
            title[1].set_color(MUTED)
            titles.add(title.next_to(centers[p] + UP * panel_h / 2, UP, buff=0.18))

        # Test electron at a sample position (fractional index f).
        tracker = ValueTracker(0.0)

        def index():
            return tracker.get_value() * (samples - 1)

        def head_xy(p, f):
            i = min(int(f), samples - 2)
            w = f - i
            return (1 - w) * runs[p][i] + w * runs[p][i + 1]

        def dots(p, f):
            """Drawn frozen electrons, blue inside the Debye circle and grey outside."""
            inside = inside_debye_circle(points, head_xy(p, f), GAMMAS[p])
            return VGroup(*[
                Dot(to_panel(p, x, y), radius=0.05, color=ELECTRON if hit else GRID,
                    stroke_width=0)
                for (x, y), hit in zip(points, inside)])

        def debye_circle(p, f):
            """Circle of radius lambda_D and its radius line, clipped to the window."""
            c = head_xy(p, f)
            group = VGroup()
            phi = np.linspace(0.0, 2 * np.pi, 361)
            ring = c + lams[p] * np.column_stack([np.cos(phi), np.sin(phi)])
            run = []
            for xy in list(ring) + [None]:
                if xy is not None and in_window(xy):
                    run.append(to_panel(p, *xy))
                    continue
                if len(run) > 1:
                    group.add(VMobject(stroke_color=INK, stroke_width=THIN_WIDTH)
                              .set_points_as_corners(run))
                run = []
            u = np.array([np.cos(angles[p]), np.sin(angles[p])])
            ends = [c + s * lams[p] * u for s in np.linspace(0.0, 1.0, 41)]
            ends = [e for e in ends if in_window(e)]
            if len(ends) > 1:
                group.add(Line(to_panel(p, *ends[0]), to_panel(p, *ends[-1]), color=INK,
                               stroke_width=AXIS_WIDTH))
            return group

        def marker(p, f):
            xy = head_xy(p, f)
            return Dot(to_panel(p, *xy), radius=0.085, color=ELECTRON, stroke_color=INK,
                       stroke_width=2.0)

        def trace(p, f):
            i = min(int(f), samples - 2)
            pts = [to_panel(p, *runs[p][k]) for k in range(i + 1)]
            pts.append(to_panel(p, *head_xy(p, f)))
            path = VMobject(stroke_color=INK, stroke_width=THIN_WIDTH, stroke_opacity=0.9)
            if len(pts) > 1:
                path.set_points_as_corners(pts)
            return path

        def layer(f, moving):
            """Frozen electrons, Debye circles and test electrons at index f."""
            if moving:
                return VGroup(
                    *[always_redraw(lambda p=p: dots(p, index())) for p in range(2)],
                    *[always_redraw(lambda p=p: trace(p, index())) for p in range(2)],
                    *[always_redraw(lambda p=p: debye_circle(p, index())) for p in range(2)],
                    *[always_redraw(lambda p=p: marker(p, index())) for p in range(2)])
            return VGroup(*[dots(p, f) for p in range(2)],
                          *[debye_circle(p, f) for p in range(2)],
                          *[marker(p, f) for p in range(2)])

        launch_arrows = VGroup(*[
            Arrow(to_panel(p, LAUNCH_X - 1.35, LAUNCH_Y[0]),
                  to_panel(p, LAUNCH_X - 0.25, LAUNCH_Y[0]), buff=0,
                  color=MUTED, stroke_width=THIN_WIDTH, max_tip_length_to_length_ratio=0.3)
            for p in range(2)])

        # Bottom row: scale bar, legend, clock.
        bottom = centers[0][1] - panel_h / 2 - 0.55
        bar_start = np.array([centers[0][0] - PANEL_W / 2, bottom, 0])
        bar = VGroup(
            Line(bar_start, bar_start + RIGHT * scale, color=INK, stroke_width=CURVE_WIDTH),
            Line(bar_start + UP * 0.09, bar_start + DOWN * 0.09, color=INK, stroke_width=AXIS_WIDTH),
            Line(bar_start + RIGHT * scale + UP * 0.09, bar_start + RIGHT * scale + DOWN * 0.09,
                 color=INK, stroke_width=AXIS_WIDTH))
        bar_label = math("a", color=INK, size=MATH_SMALL).next_to(bar, RIGHT, buff=0.15)

        icon_r = 0.17
        legend = VGroup(
            VGroup(Dot(radius=0.085, color=ELECTRON, stroke_color=INK, stroke_width=2.0),
                   label("test electron", size=SMALL_SIZE)).arrange(RIGHT, buff=0.12),
            VGroup(VGroup(Dot(radius=0.05, color=ELECTRON), Dot(radius=0.05, color=GRID))
                   .arrange(RIGHT, buff=0.08),
                   label("frozen electron", size=SMALL_SIZE)).arrange(RIGHT, buff=0.12),
            VGroup(VGroup(Circle(radius=icon_r, color=INK, stroke_width=THIN_WIDTH),
                          Line(ORIGIN, icon_r * RIGHT, color=INK, stroke_width=AXIS_WIDTH)),
                   math(r"\lambda_D", color=INK, size=MATH_SMALL)).arrange(RIGHT, buff=0.12),
            VGroup(Square(0.24, stroke_width=0, fill_color=ION, fill_opacity=0.35),
                   math(r"+en_0", color=MUTED, size=MATH_SMALL)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.4)
        legend.next_to(bar_label, RIGHT, buff=0.5).set_y(bottom)

        # Clock right-aligned with the right panel (room for "7.0").
        clock_label = math(r"t\,v_{\mathrm{th}}/a=", color=MUTED, size=MATH_SMALL)
        clock_label.move_to([0, bottom, 0]).align_to(
            centers[1] + RIGHT * (PANEL_W / 2 - 0.62), RIGHT)
        clock = DecimalNumber(0.0, num_decimal_places=1, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            m.set_value(index() * DT_OUT)
            m.next_to(clock_label, RIGHT, buff=0.12)

        clock.add_updater(place_clock)
        place_clock(clock)

        launch = layer(0.0, moving=False)
        moving = layer(0.0, moving=True)

        # The first and last frames are the launch state, so the video loops.
        self.add(panels, launch, titles, bar, bar_label, legend, clock_label, clock,
                 launch_arrows)
        self.wait(1.0)
        self.remove(launch)
        self.add(moving)
        self.bring_to_front(titles)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.audit_layout()
        self.wait(HOLD)
        for mob in moving:
            mob.clear_updaters()
        clock.clear_updaters()
        self.play(FadeOut(moving), FadeIn(launch), clock.animate.set_value(0.0),
                  run_time=0.8, rate_func=EASE)
        self.wait(0.2)
