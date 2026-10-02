"""Phase mixing against collisional relaxation in an ensemble of pendulums.

Every member is the same nonlinear pendulum in normalized variables

    theta [1],  p [1],  t omega_0 [1],
    H = p^2/2 + (1 - cos theta),

with small-oscillation frequency 1 and separatrix at H = 2.  The orbit
frequency omega(H) = pi / (2 K(H/2)) falls to zero at the separatrix, so a
small initial blob shears into thin spiral filaments (phase mixing) while the
energy distribution f(H) stays exactly that of the initial blob.

Collisions follow the Kac model: at rate nu per member, random pairs rotate
their momenta by a uniform random angle phi,

    p_i' = p_i cos phi + p_j sin phi,   p_j' = -p_i sin phi + p_j cos phi,

which conserves p_i^2 + p_j^2 and therefore the total energy.  Pair events
form a Poisson process (mean nu N dt / 2 per step), applied after each
Stoermer-Verlet (leapfrog) step; theta is wrapped to [-pi, pi).

Both panels use the same seed and initial blob; only nu differs:
nu = 0.005 (left, nu << omega_0) and nu = 1 (right, nu >~ omega_0).
The lower panels show the histogram of H against the Gibbs density
g(H) exp(-H/T) / Z, with g(H) the density of states (g = 4 K(H/2) inside the
separatrix, 8 K(2/H) / sqrt(2H) outside) and T fixed by requiring that the
canonical <H> equal the conserved mean energy per member.  The ensemble is a
numerical illustration of kinetic relaxation, not a plasma simulation.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, AXIS_WIDTH, CURVE_WIDTH, ELECTRON, EASE, FAINT, GRID, INK, LINEAR, MUTED,
    THIN_WIDTH, StyledScene, axes, axis_labels, math,
)


N_PENDULUMS = 2400
SEED = 20261002
BLOB_CENTER = (0.0, 1.84)      # (theta, p): H = 1.69, librating
BLOB_SPREAD = (0.15, 0.09)     # Gaussian standard deviations in theta and p
TIME_STEP = 0.05
NU_WEAK = 0.004
NU_STRONG = 1.0


def pendulum_energy(theta, p):
    """H = p^2/2 + 1 - cos(theta) in units of the separatrix half-height."""
    return 0.5 * p * p + 1.0 - np.cos(theta)


def wrap_angle(theta):
    """Map angles to [-pi, pi)."""
    return (theta + np.pi) % (2 * np.pi) - np.pi


def leapfrog_step(theta, p, dt):
    """One Stoermer-Verlet step (kick-drift-kick) of dtheta/dt = p, dp/dt = -sin(theta)."""
    p_half = p - 0.5 * dt * np.sin(theta)
    theta_new = theta + dt * p_half
    p_new = p_half - 0.5 * dt * np.sin(theta_new)
    return wrap_angle(theta_new), p_new


def kac_collide(p, first, second, angle):
    """Rotate the momentum pairs (p[first], p[second]) by the given angles."""
    p = np.array(p, dtype=float)
    a, b = p[first], p[second]
    c, s = np.cos(angle), np.sin(angle)
    p[first] = a * c + b * s
    p[second] = -a * s + b * c
    return p


def initial_blob(count=N_PENDULUMS, seed=SEED, center=BLOB_CENTER, spread=BLOB_SPREAD):
    """Seeded Gaussian blob in (theta, p)."""
    rng = np.random.default_rng(seed)
    theta = center[0] + spread[0] * rng.standard_normal(count)
    p = center[1] + spread[1] * rng.standard_normal(count)
    return wrap_angle(theta), p


def simulate_ensemble(nu, sample_times, count=N_PENDULUMS, seed=SEED, dt=TIME_STEP):
    """Leapfrog plus Kac collisions; return (theta, p) at the sample times.

    sample_times must be non-decreasing; each sample is taken at the nearest
    step.  The collision random stream is seeded independently of nu, so the
    two panels share the initial blob and collision random numbers.
    """
    sample_times = np.asarray(sample_times, dtype=float)
    theta, p = initial_blob(count, seed)
    rng = np.random.default_rng(seed + 1)
    sample_steps = np.rint(sample_times / dt).astype(int)
    thetas = np.empty((len(sample_steps), count))
    momenta = np.empty((len(sample_steps), count))
    step = 0
    for k, target in enumerate(sample_steps):
        while step < target:
            theta, p = leapfrog_step(theta, p, dt)
            events = min(rng.poisson(nu * count * dt / 2), count // 2)
            if events:
                members = rng.choice(count, 2 * events, replace=False)
                angle = rng.uniform(0.0, 2 * np.pi, events)
                p = kac_collide(p, members[:events], members[events:], angle)
            step += 1
        thetas[k], momenta[k] = theta, p
    return thetas, momenta


def complete_elliptic_k(m):
    """K(m) = int_0^{pi/2} (1 - m sin^2 x)^(-1/2) dx by the arithmetic-geometric mean."""
    a = np.ones_like(np.asarray(m, dtype=float))
    b = np.sqrt(1.0 - np.asarray(m, dtype=float))
    for _ in range(40):
        a, b = 0.5 * (a + b), np.sqrt(a * b)
    return np.pi / (2 * a)


def density_of_states(h):
    """Phase-space area per unit energy, g(H) = dA/dH (= orbit period inside)."""
    h = np.asarray(h, dtype=float)
    inside = h < 2.0
    m = np.where(inside, h / 2.0, 2.0 / np.maximum(h, 2.0))
    k = complete_elliptic_k(np.minimum(m, 1.0 - 1e-15))
    return np.where(inside, 4.0 * k, 8.0 * k / np.sqrt(2.0 * np.maximum(h, 2.0)))


def canonical_mean_energy(temperature, grid=512):
    """<H> for f ~ exp(-H/T): T/2 from p plus <1 - cos theta> by periodic quadrature."""
    theta = np.linspace(-np.pi, np.pi, grid, endpoint=False)
    weight = np.exp(-(1.0 - np.cos(theta)) / temperature)
    return 0.5 * temperature + np.sum((1.0 - np.cos(theta)) * weight) / np.sum(weight)


def gibbs_temperature(mean_energy):
    """Solve canonical <H>(T) = mean_energy by bisection (<H> rises with T)."""
    low, high = 1e-4, 1e3
    for _ in range(200):
        mid = np.sqrt(low * high)
        if canonical_mean_energy(mid) < mean_energy:
            low = mid
        else:
            high = mid
    return np.sqrt(low * high)


def gibbs_energy_density(h, temperature, grid=512):
    """Normalized Gibbs density of H: g(H) exp(-H/T) / Z."""
    theta = np.linspace(-np.pi, np.pi, grid, endpoint=False)
    z_theta = 2 * np.pi * np.mean(np.exp(-(1.0 - np.cos(theta)) / temperature))
    partition = np.sqrt(2 * np.pi * temperature) * z_theta
    return density_of_states(h) * np.exp(-np.asarray(h) / temperature) / partition


def energy_histogram(theta, p, edges):
    """Normalized histogram of H on the given bin edges (density over all members)."""
    counts, _ = np.histogram(pendulum_energy(theta, p), bins=edges)
    return counts / (len(theta) * np.diff(edges))


# (start, end) in t omega_0 and run time in seconds of each linear segment:
# a slow first segment resolves the shearing, a faster one the slow relaxation.
SEGMENTS = ((0.0, 120.0, 16.0), (120.0, 480.0, 18.0))
H_MAX = 6.0
F_MAX = 1.6
P_MAX = 3.6


class PendulumEnsemble(StyledScene):
    """Same pendulum ensemble, weakly collisional (left) and collisional (right)."""

    def build(self):
        fps = config.frame_rate
        times = np.unique(np.concatenate([
            np.linspace(a, b, int(round(run * fps)) + 1) for a, b, run in SEGMENTS]))
        theta0, p0 = initial_blob()
        temperature = gibbs_temperature(np.mean(pendulum_energy(theta0, p0)))
        edges = np.linspace(0.0, H_MAX, 49)
        runs = [simulate_ensemble(nu, times) for nu in (NU_WEAK, NU_STRONG)]
        tracker = ValueTracker(0.0)

        def index():
            return min(len(times) - 1, int(np.searchsorted(times, tracker.get_value() - 1e-9)))

        panels = Group()
        for column, (x_center, (thetas, momenta), tag) in enumerate(zip(
                (-3.45, 3.45), runs, (r"\nu \ll \omega_0", r"\nu \gtrsim \omega_0"))):
            ph = axes([-PI, PI, PI / 2], [-P_MAX, P_MAX, 1], 5.6, 3.0).move_to([x_center, 1.1, 0])
            ph_labels = axis_labels(ph, r"\theta\ [1]", r"p\ [1]")
            ph_labels[0].next_to(ph, DOWN, buff=0.12)
            ticks = VGroup(*[
                math(t, color=MUTED, size=24).next_to(ph.c2p(x, -P_MAX), DOWN, buff=0.12)
                for t, x in ((r"-\pi", -PI), (r"\pi", PI))])

            def level(h, sign, x_rng):
                return ph.plot(lambda x: sign * np.sqrt(max(2 * (h - 1 + np.cos(x)), 0.0)),
                               x_range=x_rng, color=FAINT, stroke_width=1.3, stroke_opacity=0.6)

            contours = VGroup()
            for h in (0.4, 1.0, 1.5, 2.6, 3.6, 5.0):
                xm = np.arccos(1 - h) if h < 2 else PI
                for s in (1, -1):
                    contours.add(level(h, s, [-xm, xm, xm / 60]))
            separatrix = VGroup(*[
                DashedVMobject(ph.plot(lambda x, s=s: 2 * s * np.cos(x / 2), x_range=[-PI, PI],
                                       color=MUTED, stroke_width=THIN_WIDTH), num_dashes=40)
                for s in (1, -1)])

            hx = axes([0, H_MAX, 1], [0, F_MAX, 0.5], 5.6, 1.75).move_to([x_center, -2.15, 0])
            hx_labels = axis_labels(hx, r"H\ [1]", r"f(H)\ [1]")
            hx_labels[1].next_to(hx.y_axis.get_top(), UP, buff=0.1)
            sep_mark = DashedLine(hx.c2p(2, 0), hx.c2p(2, F_MAX), color=MUTED,
                                  stroke_width=THIN_WIDTH, dash_length=0.08)
            sep_tick = math("2", color=MUTED, size=24).next_to(hx.c2p(2, 0), DOWN, buff=0.12)
            grid_h = np.linspace(0.02, H_MAX, 300)
            gibbs = hx.plot_line_graph(grid_h, np.minimum(gibbs_energy_density(grid_h, temperature), F_MAX),
                                       line_color=ACCENT, stroke_width=THIN_WIDTH, add_vertex_dots=False)
            label_tag = math(tag, size=36).move_to([x_center, 3.22, 0]).align_to(ph, LEFT)

            origin = ph.c2p(0, 0)
            e_theta, e_p = ph.c2p(1, 0) - origin, ph.c2p(0, 1) - origin
            rgba = np.append(color_to_rgb(ELECTRON), 1.0)

            def move_cloud(mob, thetas=thetas, momenta=momenta, origin=origin,
                           e_theta=e_theta, e_p=e_p):
                k = index()
                keep = np.abs(momenta[k]) < P_MAX
                mob.points = (origin + np.outer(thetas[k][keep], e_theta)
                              + np.outer(momenta[k][keep], e_p))
                mob.rgbas = np.tile(rgba, (len(mob.points), 1))

            cloud = PMobject(stroke_width=2.6).add_updater(move_cloud)
            move_cloud(cloud)

            def histogram(thetas=thetas, momenta=momenta, hx=hx):
                k = index()
                f = np.minimum(energy_histogram(thetas[k], momenta[k], edges), F_MAX)
                xs = np.repeat(edges, 2)
                ys = np.concatenate([[0.0], np.repeat(f, 2), [0.0]])
                return Polygon(*[hx.c2p(x, y) for x, y in zip(xs, ys)], color=ELECTRON,
                               stroke_width=1.6, fill_color=ELECTRON, fill_opacity=0.35)

            panels.add(VGroup(ph, hx, ph_labels, hx_labels, ticks, sep_tick, contours, separatrix,
                              sep_mark, gibbs, label_tag),
                       Group(cloud, always_redraw(histogram)))

        readout = VGroup(math(r"\omega_0 t =", color=MUTED, size=30),
                         DecimalNumber(0, num_decimal_places=0, color=MUTED, font_size=30))
        readout.arrange(RIGHT, buff=0.15).move_to([0, 3.22, 0]).align_to(panels[2][0], RIGHT)
        readout[1].add_updater(lambda d: d.set_value(tracker.get_value()))

        dynamics = Group(panels[1], panels[3])
        self.play(*[Create(p[0]) for p in (panels[0], panels[2])],
                  *[Create(p[1]) for p in (panels[0], panels[2])], run_time=1.0, rate_func=EASE)
        self.play(*[FadeIn(VGroup(*p[2:])) for p in (panels[0], panels[2])], FadeIn(readout),
                  run_time=0.8, rate_func=EASE)
        self.add(dynamics)
        self.wait(1.0)
        for _, end, run in SEGMENTS:
            self.play(tracker.animate.set_value(end), run_time=run, rate_func=LINEAR)
        self.wait(1.5)
