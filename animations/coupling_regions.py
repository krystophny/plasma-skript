"""Weak and strong coupling at equal density: charge regions and a test electron.

Data: two kin6d ``ocp_shielding_demo --export`` runs without impurity (case
C4, kappa = 0; see animations/data/kin6d/coupling-regions/README.md and the
provenance.json of each run).  Classical electron one-component plasma in a
periodic cube with a uniform neutralizing background +e n_0, bare Coulomb
interaction (particle-mesh Ewald, no softening), in thermal equilibrium.
Both runs hold N = 5832 electrons in the same cube of edge 18 a, so the
density n_0 = a^(-3) and the plasma frequency omega_p are the same; only the
temperature differs.  kin6d works in lambda_D, so the temperature enters
through Lambda = n_0 lambda_D^3 = (lambda_D/a)^3:

    strong (T_e = T_0):    Lambda = 1,  lambda_D = a,   Gamma_e = 1/(4 pi)  = 0.080
    weak   (T_e = 9 T_0):  Lambda = 27, lambda_D = 3 a, Gamma_e = 1/(36 pi) = 0.0088

with Gamma_e = a^2/(4 pi lambda_D^2) and lambda_D^2 proportional to T_e at
fixed n_0, as on the coupling slide.  Here the scene works in a and 1/omega_p.

Colour field: the net charge density rho = e (n_0 - n_e) in the plane z = 0
from the electrons of the same realization, smoothed by the three-dimensional
Gaussian of the thermal-fluctuation scene (charge_density, its colour map and
red/blue convention), with width sigma = lambda_D/2.  The smoothing scale is
tied to lambda_D on purpose: the Debye-Hueckel structure factor
S(k) = k^2/(k^2 + 1/lambda_D^2) suppresses net charge on scales above lambda_D,
so lambda_D is the largest scale on which the thermal motion separates charge
(page 2: r_0 ~ sqrt(3) lambda_D).  The region size is therefore set by this
choice of display scale, while the field itself is the measured charge of
the simulated electrons.  sigma = lambda_D/2 holds (2 pi)^(3/2) (sigma/a)^3 =
2 electrons at strong and 53 at weak coupling.  Relative fluctuations are
much larger at strong coupling (rms 0.37 versus 0.065 e n_0), so each panel
has its own colour limit, COLOUR_RMS times the rms of its field over all
frames; colour shows the sign and the relative strength within a panel.

Dots: the electrons of the slab |z| < a/2 (areal density 1/a^2), projected,
fading at the slab faces; positions and fields between the exported samples,
0.1/omega_p apart, are interpolated linearly.

Sequence: the electrons move for 12/omega_p; then the picture freezes
(Lorentz-gas picture: the other electrons stay where they are and do not
screen further).  One electron of the frozen frame near z = 0 at the left
edge becomes the test electron: it is launched along +x at the thermal speed
v_th = sqrt(2 k_B T_e/m_e) = sqrt(2) lambda_D omega_p of its panel, and moves
in the field of all other frozen electrons and the background,

    d^2 x/dt^2 = (1/(4 pi)) sum_j (x - x_j)/|x - x_j|^3 - x/3   [a omega_p^2],

since e^2/(4 pi eps_0 m_e) = omega_p^2 a^3/(4 pi).  The periodic cube is
replaced by its images inside a sphere of radius TILE_RADIUS with a uniform
background sphere of the same total charge.  The electron moves in three
dimensions; its path is drawn in projection, and its own Gaussian charge moves
with it in the colour field.  LAUNCH lists the chosen electrons: among the
frozen electrons with |z| < 0.25 a, -8.5 a < x < -6.5 a, |y| < 6 a, the one
per panel closest to the mid-line y = 0 whose drawn path stays within
|z| < a of the plane (and, at strong coupling, inside the window for the
whole flight); scripts/check-physics.py checks this choice and the
deflection statistics of the candidates.  The flight ends early once the
electron is a past the window edge.  The orbits are
integrated with the adaptive Dormand-Prince 5(4) scheme of the
coupling-test-particle scene.
"""

from manim import *
import numpy as np

from kin6d_data import Export
from thermal_charge_fluctuations import charge_density, NEGATIVE, POSITIVE
from coupling_test_particle import DP_A, DP_B4, DP_B5
from style import (
    AXIS_WIDTH, BG, EASE, GRID, INK, LINEAR, MUTED, THIN_WIDTH, StyledScene, math,
    MATH_SMALL,
)

RUNS = (("coupling-regions/strong", 1.0), ("coupling-regions/weak", 3.0))  # lambda_D/a
TEMPERATURES = ("T_0", "9T_0")
BOX = 18.0              # periodic cube edge in a (both runs)
SIGMA_DEBYE = 0.5       # Gaussian smoothing width in lambda_D
GRID_POINTS = 180       # field samples per box edge
SLAB = 0.5              # drawn electrons |z| < SLAB a
FADE = 0.1              # dot fade width at the slab faces, a
COLOUR_RMS = 2.5        # colour limit in units of the panel's field rms
LAUNCH = (1150, 327)    # test electrons (indices in the exported arrays)
LAUNCH_BOX = (-8.5, -6.5, 6.0, 0.25)   # x_min, x_max, |y| max, |z| max of candidates
WINDOW_MARGIN = 0.4     # the strong path stays this far inside the window, a
Z_LIMIT = 1.0           # |z| of the drawn test path, a
T_TEST = 8.0            # test-electron flight time, 1/omega_p
DT_OUT = 0.05           # trajectory samples, 1/omega_p
TOLERANCE = 1e-9
TILE_RADIUS = 20.0      # radius of the frozen image sphere, a

PANEL = 5.6
PANEL_GAP = 0.7
PLAY_TIME = 9.0         # seconds for the 12/omega_p of recorded dynamics
TEST_TIME = 8.0         # seconds for the T_TEST of test-electron flight
HOLD = 3.0


def coupling(lam):
    """Gamma_e = a^2/(4 pi lambda_D^2) for lambda_D/a = lam."""
    return 1.0 / (4 * np.pi * lam * lam)


def debye_length(gamma):
    """lambda_D/a = 1/sqrt(4 pi Gamma_e)."""
    return 1.0 / np.sqrt(4 * np.pi * gamma)


def load_run(slug, lam):
    """Electron positions (3, N, frames) in units of a and times in 1/omega_p."""
    data = Export(slug)
    if abs(data.parameters["Lambda"] - lam ** 3) > 1e-9 or \
            abs(data.parameters["box"] * lam - BOX) > 1e-9:
        raise ValueError(f"{slug}: export does not match lambda_D/a = {lam}")
    return data["positions"] * lam, data["t"]


def run_fields(pos, lam, grid=GRID_POINTS):
    """rho/(e n_0) on z = 0 for every frame, (grid, grid, frames)."""
    return np.stack([charge_density(pos[:, :, f], BOX, SIGMA_DEBYE * lam, 1.0, grid)
                     for f in range(pos.shape[2])], axis=-1)


def colour_limit(fields):
    """Panel colour limit: COLOUR_RMS times the rms of rho/(e n_0)."""
    return COLOUR_RMS * float(np.sqrt(np.mean(fields * fields)))


def field_rgb(level, base):
    """level in [-1, 1] -> uint8 RGB: base at 0, POSITIVE > 0, NEGATIVE < 0."""
    def rgb(c):
        return np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)

    level = np.clip(np.asarray(level, float), -1.0, 1.0)[..., None]
    colour = np.where(level > 0, rgb(POSITIVE), rgb(NEGATIVE))
    return np.round(rgb(base) + np.abs(level) * (colour - rgb(base))).astype(np.uint8)


def slab_alpha(z):
    """Dot opacity of electrons at height z: 1 inside, fading at |z| = SLAB."""
    return np.clip((SLAB - np.abs(z)) / FADE, 0.0, 1.0)


def launch_candidates(points):
    """Indices of frozen electrons eligible as test electrons (points (3, N))."""
    x_lo, x_hi, y_max, z_max = LAUNCH_BOX
    return np.nonzero((points[0] > x_lo) & (points[0] < x_hi)
                      & (np.abs(points[1]) < y_max) & (np.abs(points[2]) < z_max))[0]


def frozen_images(points, skip, radius=TILE_RADIUS):
    """Periodic images (M, 3) of all electrons except `skip` within `radius`."""
    rest = np.delete(points.T, skip, axis=0)
    shifts = BOX * np.array(np.meshgrid(*(np.arange(-1, 2),) * 3, indexing="ij")).reshape(3, -1).T
    images = (rest[None] + shifts[:, None]).reshape(-1, 3)
    return images[np.linalg.norm(images, axis=1) < radius]


def background_radius(charges):
    """Radius R of the uniform background sphere with (4 pi/3) R^3 = M."""
    return (3 * len(charges) / (4 * np.pi)) ** (1 / 3)


def test_acceleration(x, charges):
    """d^2 x/dt^2 in a omega_p^2 at x (3,): frozen electrons plus background."""
    d = x[None, :] - charges
    r2 = np.sum(d * d, axis=1)
    coulomb = np.sum(d / (r2 * np.sqrt(r2))[:, None], axis=0)
    density = len(charges) / (4 * np.pi / 3 * background_radius(charges) ** 3)
    return coulomb / (4 * np.pi) - density * x / 3


def test_energy(x, v, charges):
    """Energy per mass in (a omega_p)^2: |v|^2/2 + potential (sphere background)."""
    d = x[None, :] - charges
    radius = background_radius(charges)
    coulomb = np.sum(1 / np.sqrt(np.sum(d * d, axis=1)))
    return 0.5 * v @ v + (coulomb - 2 * np.pi / 3 * (3 * radius ** 2 - x @ x)) / (4 * np.pi)


def test_trajectory(points, index, lam, t_end=T_TEST, dt_out=DT_OUT,
                    tol=TOLERANCE):
    """Adaptive Dormand-Prince orbit of electron `index`, launched along +x.

    points (3, N) in a; speed v_th = sqrt(2) lambda_D omega_p.  Returns times
    (K,), positions (K, 3) and velocities (K, 3), sampled every dt_out, and
    the frozen charges used.  The flight stops at the first sample more
    than a outside the window |x|, |y| < BOX/2.
    """
    charges = frozen_images(points, index)
    y = np.concatenate([points[:, index], [np.sqrt(2) * lam, 0.0, 0.0]])

    def rhs(state):
        return np.concatenate([state[3:], test_acceleration(state[:3], charges)])

    times = np.arange(0.0, t_end + 0.5 * dt_out, dt_out)
    out = np.empty((len(times), 6))
    out[0] = y
    t, h = 0.0, 1e-3
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
            err = np.max(np.abs(y5 - y4) / (1.0 + np.maximum(np.abs(y), np.abs(y5)))) / tol
            if err <= 1.0:
                t += h_try
                y = y5
            h = h_try * min(5.0, max(0.2, 0.9 * (err + 1e-300) ** -0.2))
        out[k] = y
        if np.max(np.abs(y[:2])) > BOX / 2 + 1.0:
            times, out = times[:k + 1], out[:k + 1]
            break
    return times, out[:, :3], out[:, 3:], charges


def drawn_samples(path, margin=0.0):
    """Number of leading samples of path (K, 3) inside the window |x|, |y| < BOX/2."""
    inside = np.all(np.abs(path[:, :2]) < BOX / 2 - margin, axis=1)
    return len(inside) if inside.all() else int(np.argmin(inside))


def deflection(v, count):
    """Angle (rad) between the velocity at sample count - 1 and the launch (+x)."""
    w = v[count - 1]
    return float(np.arccos(np.clip(w[0] / np.linalg.norm(w), -1.0, 1.0)))


def still_data(grid=2 * GRID_POINTS, base="#FFFFFF"):
    """Frozen frame of both panels for the coupling slide.

    Returns the JSON record (window, per-panel temperature label, Gamma_e,
    lambda_D/a, colour limit and the drawn electrons [x, y, opacity] in a)
    and the two field images (grid, grid, 3) uint8 on the slide `base`
    colour, row 0 at the top, with the animation's colour limits.
    """
    record = {"window": [-BOX / 2, BOX / 2, -BOX / 2, BOX / 2], "panels": []}
    images = []
    for p, (slug, lam) in enumerate(RUNS):
        pos, _ = load_run(slug, lam)
        limit = colour_limit(run_fields(pos, lam))
        points = pos[:, :, -1]
        rho = charge_density(points, BOX, SIGMA_DEBYE * lam, 1.0, grid)
        images.append(field_rgb(rho / limit, base).transpose(1, 0, 2)[::-1])
        shown = np.abs(points[2]) < SLAB
        record["panels"].append({
            "temperature": TEMPERATURES[p], "gamma": round(float(coupling(lam)), 4),
            "lambda": lam, "limit": round(limit, 4),
            "points": [[round(float(x), 3), round(float(y), 3), round(float(a), 3)]
                       for x, y, a in zip(points[0, shown], points[1, shown],
                                          slab_alpha(points[2, shown]))]})
    return record, images


def panel_title(p):
    """T_e, Gamma_e and lambda_D of panel p as a LaTeX string."""
    lam = RUNS[p][1]
    length = "a" if lam == 1 else f"{lam:g}a"
    return rf"T_e={TEMPERATURES[p]},\ \Gamma_e={coupling(lam):.1g},\ \lambda_D={length}"


class CouplingRegions(StyledScene):
    """Equal density, two temperatures: charge regions, freeze, one test electron."""

    def build(self):
        runs = [load_run(slug, lam) for slug, lam in RUNS]
        times = runs[0][1]
        frames = len(times)
        fields = [run_fields(pos, lam) for (pos, _), (_, lam) in zip(runs, RUNS)]
        limits = [colour_limit(f) for f in fields]
        frozen = [pos[:, :, -1] for pos, _ in runs]
        flights = [test_trajectory(frozen[p], LAUNCH[p], RUNS[p][1]) for p in range(2)]
        drawn = [drawn_samples(x) for _, x, _, _ in flights]
        others = [charge_density(np.delete(frozen[p], LAUNCH[p], axis=1), BOX,
                                 SIGMA_DEBYE * RUNS[p][1], 1.0, GRID_POINTS) for p in range(2)]
        samples = int(round(T_TEST / DT_OUT)) + 1

        scale = PANEL / BOX
        centers = [np.array([-(PANEL + PANEL_GAP) / 2, 0.03, 0]),
                   np.array([(PANEL + PANEL_GAP) / 2, 0.03, 0])]

        def pp(p, x, y):
            return centers[p] + np.array([x, y, 0.0]) * scale

        tracker = ValueTracker(0.0)      # recorded dynamics, 0..1
        flight = ValueTracker(0.0)       # test-electron flight, 0..1
        frozen_on = ValueTracker(0.0)    # 1 once the test electron is singled out

        def frame_pos(u):
            f = u * (frames - 1)
            i = min(int(f), frames - 2)
            return i, f - i

        def positions(p, u):
            pos = runs[p][0]
            i, w = frame_pos(u)
            step = pos[:, :, i + 1] - pos[:, :, i]
            step -= BOX * np.round(step / BOX)
            q = pos[:, :, i] + w * step
            return q - BOX * np.round(q / BOX)

        def flight_index(p):
            k = flight.get_value() * (samples - 1)
            return min(k, len(flights[p][0]) - 1)

        def test_xyz(p):
            path = flights[p][1]
            k = flight_index(p)
            i = min(int(k), len(path) - 2)
            w = k - i
            return (1 - w) * path[i] + w * path[i + 1]

        def field(p):
            if flight.get_value() > 0:
                own = charge_density(test_xyz(p)[:, None], BOX, SIGMA_DEBYE * RUNS[p][1],
                                     1.0, GRID_POINTS) - 1.0
                return others[p] + own
            i, w = frame_pos(tracker.get_value())
            return (1 - w) * fields[p][..., i] + w * fields[p][..., i + 1]

        def rgba(p):
            image = field_rgb(field(p) / limits[p], BG).transpose(1, 0, 2)[::-1]
            alpha = np.full(image.shape[:2] + (1,), 255, np.uint8)
            return np.ascontiguousarray(np.concatenate([image, alpha], axis=2))

        images, frames_drawn, pools = Group(), VGroup(), VGroup()
        dot_opacity = ValueTracker(0.0)
        for p in range(2):
            image = ImageMobject(rgba(p))
            image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
            image.height = PANEL
            image.move_to(centers[p])
            image.add_updater(lambda m, p=p: setattr(m, "pixel_array", rgba(p)))
            images.add(image)
            frames_drawn.add(Square(PANEL, color=GRID, stroke_width=AXIS_WIDTH)
                             .move_to(centers[p]))
            count = int((np.abs(runs[p][0][2]) < SLAB).sum(axis=0).max() * 1.15) + 20
            pool = VGroup(*[Dot(centers[p], radius=0.03, color=INK, fill_opacity=0)
                            for _ in range(count)])

            def update_pool(group, p=p):
                q = positions(p, tracker.get_value())
                idx = np.nonzero(np.abs(q[2]) < SLAB)[0]
                if frozen_on.get_value() > 0:
                    idx = idx[idx != LAUNCH[p]]
                alpha = slab_alpha(q[2, idx]) * dot_opacity.get_value()
                for k, dot in enumerate(group):
                    if k < len(idx):
                        dot.move_to(pp(p, q[0, idx[k]], q[1, idx[k]]))
                        dot.set_fill(opacity=alpha[k])
                    else:
                        dot.set_fill(opacity=0)

            pool.add_updater(update_pool)
            update_pool(pool)
            pools.add(pool)

        def trace(p):
            path = flights[p][1]
            k = min(flight_index(p), drawn[p] - 1)
            i = int(k)
            pts = [pp(p, *path[j, :2]) for j in range(i + 1)]
            if k > i:
                w = k - i
                pts.append(pp(p, *((1 - w) * path[i, :2] + w * path[i + 1, :2])))
            line = VMobject(stroke_color=INK, stroke_width=THIN_WIDTH)
            if len(pts) > 1:
                line.set_points_as_corners(pts)
            return line

        def marker(p):
            visible = drawn[p] == len(flights[p][0]) or flight_index(p) < drawn[p] - 1
            return Dot(pp(p, *test_xyz(p)[:2]), radius=0.07, color=INK, stroke_color=BG,
                       stroke_width=2.0, fill_opacity=1.0 if visible else 0.0,
                       stroke_opacity=1.0 if visible else 0.0)

        titles = VGroup(*[math(panel_title(p), color=INK, size=MATH_SMALL + 4)
                          .next_to(centers[p] + UP * PANEL / 2, UP, buff=0.18)
                          for p in range(2)])

        # Bottom row: scale bar a, colour key, clock.
        bottom = centers[0][1] - PANEL / 2 - 0.42
        start = np.array([centers[0][0] - PANEL / 2, bottom, 0])
        bar = VGroup(
            Line(start, start + RIGHT * scale, color=INK, stroke_width=4),
            Line(start + UP * 0.09, start + DOWN * 0.09, color=INK, stroke_width=AXIS_WIDTH),
            Line(start + RIGHT * scale + UP * 0.09, start + RIGHT * scale + DOWN * 0.09,
                 color=INK, stroke_width=AXIS_WIDTH))
        bar_label = math("a", color=MUTED, size=MATH_SMALL).next_to(bar, RIGHT, buff=0.15)
        key = VGroup(
            VGroup(Square(0.24, stroke_width=0, fill_color=POSITIVE, fill_opacity=1),
                   math(r"\rho>0", color=MUTED, size=MATH_SMALL)).arrange(RIGHT, buff=0.12),
            VGroup(Square(0.24, stroke_width=0, fill_color=NEGATIVE, fill_opacity=1),
                   math(r"\rho<0", color=MUTED, size=MATH_SMALL)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.45).move_to([0, bottom, 0])
        clock_label = math(r"\omega_p t=", color=MUTED, size=MATH_SMALL)
        clock_label.move_to([0, bottom, 0]).align_to(
            centers[1] + RIGHT * (PANEL / 2 - 0.75), RIGHT)
        clock = DecimalNumber(times[0], num_decimal_places=1, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            i, w = frame_pos(tracker.get_value())
            now = times[i] + w * (times[i + 1] - times[i])
            m.set_value(now + flight.get_value() * T_TEST)
            m.next_to(clock_label, RIGHT, buff=0.12).match_y(clock_label[0][-1])

        clock.add_updater(place_clock)
        place_clock(clock)

        self.add(images, frames_drawn, pools, titles, bar, bar_label, key, clock_label, clock)
        self.play(dot_opacity.animate.set_value(1.0), run_time=0.6, rate_func=EASE)
        self.wait(0.4)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(0.8)                                   # the picture freezes
        markers = VGroup(*[marker(p) for p in range(2)])
        self.play(FadeIn(markers, scale=2.0), run_time=0.6, rate_func=EASE)
        frozen_on.set_value(1.0)
        self.remove(markers)
        moving = VGroup(*[always_redraw(lambda p=p: trace(p)) for p in range(2)],
                        *[always_redraw(lambda p=p: marker(p)) for p in range(2)])
        self.add(moving)
        self.wait(0.4)
        self.play(flight.animate.set_value(1.0), run_time=TEST_TIME, rate_func=LINEAR)
        self.audit_layout()
        self.wait(HOLD)
