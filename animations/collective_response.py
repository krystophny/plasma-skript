"""Range of the response: contact collisions in a gas against a screened field.

Both cases hold the same seeded particle positions; lengths are measured in
units of lambda_D and time in units of lambda_D / V, where V is the initial
speed of the test particle (V = 1 in the code).

Neutral gas (shown first): hard spheres of equal mass. The test particle moves on a
straight line until its centre comes within the contact distance CONTACT of
a resting neutral, then the pair scatters elastically,

    v_t' = v_t - (v_t . n) n,   v_j' = (v_t . n) n,

with n the unit vector from the test particle to the struck neutral. Struck
neutrals then move freely; collisions among them are not followed.

Plasma (shown second): a positive test charge passes through cold, resting electrons.
Each electron feels the attractive screened force derived from the softened
potential energy U(r_s) = -exp(-r_s)/r_s, r_s = sqrt(r^2 + SOFTENING^2)
(unit coupling), drawn as an arrow toward the test charge of length
ARROW_MAX tanh(|F|/1.2): it grows with the force and saturates near the charge. The test charge feels the opposite
sum of all those forces times COUPLING and is integrated with a leapfrog
step; the electrons are held at rest so that the arrows show the field's
reach, not a self-consistent response. The dashed circle of radius lambda_D
around the test charge is clipped to the panel. The two cases run one after
the other in the same full-width panel and end on a still of both final
states side by side. The scene is an illustration of the interaction range,
not a plasma simulation.
"""

from manim import *
import numpy as np

from style import (
    BG, CURVE_WIDTH, DOT_RADIUS, EASE, ELECTRON, FAINT, GRID, INK, ION, LINEAR,
    MUTED, StyledScene, label, math,
)


HALF_WIDTH = 4.0
HALF_HEIGHT = 2.6
N_PARTICLES = 80
SEED = 5
CONTACT = 0.2
SOFTENING = 0.12
COUPLING = 0.004
DURATION = 8.0
FINAL_HOLD = 3.0
DT = 0.002
ARROW_MAX = 0.45
GAS_START = (-4.0, 0.4)
PLASMA_START = (-4.6, 0.1)


def particle_positions(seed=5, n=80, half_width=4.0, half_height=2.6):
    """Seeded uniform positions in the panel, in units of lambda_D."""
    rng = np.random.default_rng(seed)
    return np.column_stack([rng.uniform(-half_width, half_width, n),
                            rng.uniform(-half_height, half_height, n)])


def screened_force(sep, softening=0.12):
    """Force -grad U on a partner at separation sep (partner minus source).

    U = -exp(-r_s)/r_s with r_s = sqrt(|sep|^2 + softening^2); the force points
    back toward the source (attraction). sep has shape (..., 2).
    """
    sep = np.asarray(sep, dtype=float)
    r_s = np.sqrt(np.sum(sep * sep, axis=-1) + softening * softening)
    magnitude = (1 + r_s) * np.exp(-r_s) / r_s**3
    return -magnitude[..., None] * sep


def plasma_test_path(positions, start=(-4.6, 0.1), velocity=(1.0, 0.0), duration=8.0,
                     dt=0.002, coupling=0.004, softening=0.12):
    """Leapfrog path of the test charge; returns times (k,) and positions (k, 2)."""
    steps = int(round(duration / dt))
    pos = np.array(start, dtype=float)
    vel = np.array(velocity, dtype=float)

    def accel(p):
        forces = screened_force(positions - p, softening)
        return -coupling * np.sum(forces, axis=0)

    path = [pos.copy()]
    acc = accel(pos)
    for _ in range(steps):
        vel_half = vel + 0.5 * dt * acc
        pos = pos + dt * vel_half
        acc = accel(pos)
        vel = vel_half + 0.5 * dt * acc
        path.append(pos.copy())
    return np.arange(steps + 1) * dt, np.array(path), vel


def hard_sphere_events(positions, start=(-4.0, 0.4), velocity=(1.0, 0.0), duration=8.0,
                       contact=0.2):
    """Elastic equal-mass collisions of a test sphere with resting spheres.

    Returns a list of events (time, test position, test velocity after,
    neutral index, neutral velocity after), in time order.
    """
    pos = np.array(start, dtype=float)
    vel = np.array(velocity, dtype=float)
    t = 0.0
    struck = set()
    events = []
    while True:
        best = None
        for j, p in enumerate(positions):
            if j in struck:
                continue
            d = p - pos
            a = vel @ vel
            b = d @ vel
            c = d @ d - contact * contact
            disc = b * b - a * c
            if b <= 0 or disc < 0:
                continue
            tau = (b - np.sqrt(disc)) / a
            if tau > 1e-12 and (best is None or tau < best[0]):
                best = (tau, j)
        if best is None or t + best[0] > duration:
            return events
        tau, j = best
        t += tau
        pos = pos + tau * vel
        n = (positions[j] - pos) / contact
        along = vel @ n
        neutral_vel = along * n
        vel = vel - neutral_vel
        struck.add(j)
        events.append((t, pos.copy(), vel.copy(), j, neutral_vel.copy()))




class CollectiveResponse(StyledScene):
    """Contact collisions in a neutral gas, then the screened reach of a charge, then both."""

    def build(self):
        positions = particle_positions()
        events = hard_sphere_events(positions)
        times, plasma_path, _ = plasma_test_path(positions)

        def inside(xy):
            return abs(xy[0]) <= HALF_WIDTH - 0.05 and abs(xy[1]) <= HALF_HEIGHT - 0.05

        def gas_state(t):
            pos, vel, t0 = np.array(GAS_START), np.array([1.0, 0.0]), 0.0
            moved = {}
            for (te, pe, ve, j, vj) in events:
                if te > t:
                    break
                pos, vel, t0 = pe, ve, te
                moved[j] = (te, vj)
            return pos + (t - t0) * vel, moved

        def panel(center, scale):
            """Frame and lambda_D bar of one view; to_scene maps lambda_D units into it."""
            def to_scene(xy):
                return center + scale * np.array([xy[0], xy[1], 0.0])
            frame = Rectangle(width=2 * HALF_WIDTH * scale, height=2 * HALF_HEIGHT * scale,
                              color=GRID, stroke_width=1.6).move_to(center)
            bar_left = to_scene((HALF_WIDTH - 1.3, -HALF_HEIGHT)) + DOWN * 0.25
            bar = Line(bar_left, bar_left + RIGHT * scale, color=MUTED, stroke_width=3)
            bar_label = math(r"\lambda_D", color=MUTED, size=30).next_to(bar, LEFT, buff=0.15)
            return to_scene, frame, VGroup(bar, bar_label)

        def gas_view(to_scene, scale, clock):
            def gas_group():
                t = clock.get_value()
                test, moved = gas_state(t)
                group = VGroup()
                for j, p in enumerate(positions):
                    xy = p if j not in moved else p + (t - moved[j][0]) * moved[j][1]
                    if inside(xy):
                        group.add(Circle(radius=0.5 * CONTACT * scale, color=INK if j in moved else FAINT,
                                         stroke_width=3.2 if j in moved else 2.2).move_to(to_scene(xy)))
                if inside(test):
                    group.add(Dot(to_scene(test), radius=0.5 * CONTACT * scale, color=INK))
                return group

            def gas_trail():
                t = clock.get_value()
                pts = [np.array(GAS_START)] + [pe for (te, pe, *_rest) in events if te <= t]
                pts.append(gas_state(t)[0])
                pts = [to_scene(np.clip(p, [-HALF_WIDTH, -HALF_HEIGHT], [HALF_WIDTH, HALF_HEIGHT]))
                       for p in pts]
                return VMobject(stroke_color=INK, stroke_width=2.0, stroke_opacity=0.55).set_points_as_corners(pts)

            return VGroup(always_redraw(gas_trail), always_redraw(gas_group))

        def plasma_view(to_scene, scale, clock):
            arrow_max = ARROW_MAX * scale / 0.78

            def screening_ring(test, dashes=28, samples=8):
                """Dashed lambda_D circle around the test charge, clipped to the panel."""
                ring = VGroup()
                for d in range(dashes):
                    phi = 2 * np.pi * (d + np.linspace(0.0, 0.5, samples)) / dashes
                    pts = test + np.column_stack([np.cos(phi), np.sin(phi)])
                    keep = (np.abs(pts[:, 0]) <= HALF_WIDTH) & (np.abs(pts[:, 1]) <= HALF_HEIGHT)
                    if keep.sum() >= 2:
                        ring.add(VMobject(stroke_color=ION, stroke_width=1.8).set_points_as_corners(
                            [to_scene(q) for q in pts[keep]]))
                return ring

            def plasma_index():
                return min(int(round(clock.get_value() / DT)), len(times) - 1)

            def plasma_group():
                k = plasma_index()
                test = plasma_path[k]
                forces = screened_force(positions - test, SOFTENING)
                magnitude = np.linalg.norm(forces, axis=1)
                group = VGroup()
                for p, f, m in zip(positions, forces, magnitude):
                    start = to_scene(p)
                    group.add(Dot(start, radius=DOT_RADIUS, color=ELECTRON))
                    length = arrow_max * np.tanh(m / 1.2)
                    if length > 0.06 and inside(test):
                        tip = start + length * np.array([f[0], f[1], 0.0]) / m
                        group.add(Arrow(start, tip, buff=0, color=ELECTRON, stroke_width=2.2,
                                        max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12))
                if inside(test):
                    tri = Triangle(color=ION, fill_opacity=1, stroke_width=0).scale(0.13)
                    group.add(tri.move_to(to_scene(test)))
                    group.add(screening_ring(test))
                return group

            def plasma_trail():
                k = plasma_index()
                pts = [p for p in plasma_path[:k + 1:50] if inside(p)] + ([plasma_path[k]] if inside(plasma_path[k]) else [])
                if len(pts) < 2:
                    pts = [[-HALF_WIDTH, PLASMA_START[1]]] * 2
                    return VMobject(stroke_opacity=0).set_points_as_corners([to_scene(p) for p in pts])
                return VMobject(stroke_color=ION, stroke_width=2.0, stroke_opacity=0.55).set_points_as_corners(
                    [to_scene(p) for p in pts])

            return VGroup(always_redraw(plasma_trail), always_redraw(plasma_group))

        # Sequential runs: the same full-width panel, the same particle positions.
        scale = 1.1
        to_scene, frame, bar = panel(np.array([0.0, -0.1, 0.0]), scale)
        gas_title = label("neutral gas").next_to(frame, UP, buff=0.2)
        plasma_title = label("plasma").next_to(frame, UP, buff=0.2)
        gas_clock, plasma_clock = ValueTracker(0.0), ValueTracker(0.0)
        gas = gas_view(to_scene, scale, gas_clock)
        plasma = plasma_view(to_scene, scale, plasma_clock)

        self.play(Create(frame), FadeIn(gas_title), FadeIn(bar), run_time=0.8, rate_func=EASE)
        self.play(FadeIn(gas), run_time=0.6, rate_func=EASE)
        self.play(gas_clock.animate.set_value(DURATION), run_time=DURATION, rate_func=LINEAR)
        self.wait(0.6)
        self.play(FadeOut(gas), FadeOut(gas_title), run_time=0.5, rate_func=EASE)
        self.play(FadeIn(plasma), FadeIn(plasma_title), run_time=0.5, rate_func=EASE)
        self.wait(0.4)
        self.play(plasma_clock.animate.set_value(DURATION), run_time=DURATION, rate_func=LINEAR)
        self.wait(0.6)

        # Still pair of both final states; nothing moves.
        small = 0.78
        end = ValueTracker(DURATION)
        left_scene, left_frame, _ = panel(np.array([-3.37, -0.3, 0.0]), small)
        right_scene, right_frame, right_bar = panel(np.array([3.37, -0.3, 0.0]), small)
        still = VGroup(
            left_frame, right_frame, right_bar,
            label("neutral gas").next_to(left_frame, UP, buff=0.2),
            label("plasma").next_to(right_frame, UP, buff=0.2),
            gas_view(left_scene, small, end), plasma_view(right_scene, small, end))
        self.play(*[FadeOut(m) for m in (frame, bar, plasma, plasma_title)], run_time=0.5, rate_func=EASE)
        self.play(FadeIn(still), run_time=0.6, rate_func=EASE)
        self.wait(FINAL_HOLD)
