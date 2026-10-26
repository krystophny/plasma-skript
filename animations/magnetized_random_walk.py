"""Magnetized random walk: collisions make the guiding centre jump across B.

Model: ions (charge q_alpha > 0, mass m_alpha) in a uniform magnetic field
B = B e_z out of the page, E = 0, motion in the perpendicular plane only.
Between collisions each ion moves on its exact Lorentz-force circle with the
signed gyrofrequency omega_c = q_alpha B/m_alpha > 0 (clockwise) and the fixed
perpendicular speed v_perp, so the guiding centre
R = x + (m_alpha/q_alpha) v x B/B^2 is at rest.  Collisions are a Poisson
process of rate nu; each one redraws the velocity direction uniformly and
keeps the speed (an elastic, isotropic scattering model).  The guiding centre
then jumps by Delta R = (m_alpha/q_alpha) Delta v x B/B^2, of mean square
2 rho_L^2 with rho_L = v_perp/omega_c.  Event-driven and exact: the code draws
collision times and new directions and evaluates the circles in closed form.

Analytic result for this model (velocity autocorrelation
<v(0).v(t)> = v_perp^2 exp(-nu t) cos(omega_c t), Green-Kubo in two
dimensions):

    D_perp = (v_perp^2/2) nu/(nu^2 + omega_c^2)
           = (nu rho_L^2/2)/(1 + nu^2/omega_c^2)  ->  nu rho_L^2/2  ~  1/B^2,

the strongly magnetized limit of the script's D_perp = D/(1 + omega_c^2/nu^2)
with the unmagnetized D = v_perp^2/(2 nu); motion along B is not slowed by B,
D_par ~ v_th^2/nu.  The measured D_perp is a quarter of the least-squares slope
of the ensemble mean <|R(t) - R(0)|^2> over 0.25 t_end <= t <= t_end.

Normalization: B_0 the reference field, omega_c0 = q_alpha B_0/m_alpha,
rho_L0 = v_perp/omega_c0; lengths in rho_L0 [1], time omega_c0 t [1],
D in rho_L0^2 omega_c0 [1].  Parameters: nu = 0.1 omega_c0, B/B_0 = 1, 2, 4,
4000 ions per field (the same seeded collision sequence for every B),
t_end = 400/omega_c0, i.e. about 40 collisions per ion.
scripts/check-physics.py compares the measured D_perp with a Green-Kubo
quadrature and checks the 1/B^2 scaling and the free-gyration invariants.
"""

from manim import *
import numpy as np

from style import (
    BLUE, CURVE_WIDTH, EASE, FAINT, GREEN, INK, ION, LINEAR, MATH_SIZE, MATH_SMALL,
    MUTED, ORANGE, PURPLE, THIN_WIDTH, B_FIELD, StyledScene, axes, axis_labels, label, math,
    SMALL_SIZE,
)

V_PERP = 1.0                    # perpendicular speed [rho_L0 omega_c0]
NU = 0.1                        # collision rate [omega_c0]
B_VALUES = (1.0, 2.0, 4.0)      # B/B_0 [1]
N_ENSEMBLE = 4000
T_END = 400.0                   # omega_c0 t_end [1]
N_SAMPLES = 201                 # sample times of the mean square displacement
SEED = 11
SINGLE_SEED = 3                 # the ion followed in the first part
SINGLE_T = 120.0                # omega_c0 t of the single-ion part


def collision_sequence(n=N_ENSEMBLE, nu=NU, t_end=T_END, seed=SEED):
    """Collision times (n, K) and velocity directions (n, K + 1) after each collision."""
    rng = np.random.default_rng(seed)
    k = int(nu * t_end + 10 * np.sqrt(nu * t_end) + 10)
    times = np.cumsum(rng.exponential(1.0 / nu, size=(n, k)), axis=1)
    if np.any(times[:, -1] <= t_end):
        raise ValueError("too few collisions drawn")
    angles = rng.uniform(0.0, 2 * np.pi, size=(n, k + 1))
    return times, angles


def jumps(times, angles, omega):
    """Guiding-centre jumps (n, K, 2) at the collisions for gyrofrequency omega > 0."""
    start = np.concatenate([np.zeros((times.shape[0], 1)), times[:, :-1]], axis=1)
    before = angles[:, :-1] - omega * (times - start)      # clockwise rotation
    after = angles[:, 1:]
    r = V_PERP / omega
    return r * np.stack([np.sin(after) - np.sin(before),
                         -(np.cos(after) - np.cos(before))], axis=-1)


def centre_at(times, steps, t):
    """Guiding centres (n, len(t), 2) at times t, starting from R = 0."""
    out = np.zeros((times.shape[0], len(t), 2))
    for j, tj in enumerate(t):
        mask = (times <= tj)[..., None]
        out[:, j] = np.sum(steps * mask, axis=1)
    return out


def mean_square(omega, n=N_ENSEMBLE, seed=SEED):
    """Sample times and the ensemble mean <|R(t) - R(0)|^2>."""
    times, angles = collision_sequence(n, seed=seed)
    t = np.linspace(0.0, T_END, N_SAMPLES)
    r = centre_at(times, jumps(times, angles, omega), t)
    return t, np.mean(np.sum(r * r, axis=-1), axis=0)


def measured_diffusion(omega, n=N_ENSEMBLE, seed=SEED):
    """D_perp = slope/4 of the mean square displacement over the last 3/4 of the run."""
    t, msd = mean_square(omega, n, seed)
    fit = t >= 0.25 * T_END
    return np.polyfit(t[fit], msd[fit], 1)[0] / 4.0


def diffusion_formula(omega, nu=NU):
    """D_perp = (v_perp^2/2) nu/(nu^2 + omega^2)."""
    return 0.5 * V_PERP**2 * nu / (nu**2 + omega**2)


def single_ion(t_end=SINGLE_T, omega=1.0, steps=4000, seed=SINGLE_SEED):
    """One ion: times, positions (steps, 2), guiding centres (steps, 2), collision indices."""
    times, angles = collision_sequence(1, t_end=t_end, seed=seed)
    times, angles = times[0], angles[0]
    t = np.linspace(0.0, t_end, steps)
    k = np.searchsorted(times, t, side="right")             # collisions so far
    start = np.concatenate([[0.0], times])[k]
    theta = angles[k] - omega * (t - start)
    steps_r = jumps(times[None], angles[None], omega)[0]
    centre = np.concatenate([np.zeros((1, 2)), np.cumsum(steps_r, axis=0)])[k]
    r = V_PERP / omega
    x = centre - r * np.stack([np.sin(theta), -np.cos(theta)], axis=-1)
    hits = times[times <= t_end]
    return t, x, centre, hits


PLAY_SINGLE = 9.0
PLAY_MSD = 6.0


class MagnetizedRandomWalk(StyledScene):
    """One ion's guiding-centre walk, then D_perp ~ 1/B^2 from an ensemble."""

    def build(self):
        # ---- part 1: one ion at B = B_0 --------------------------------
        t1, x1, c1, hits = single_ion()
        ax = axes([-5, 5, 1], [-5, 5, 1], 6.2, 6.2).move_to([-3.4, -0.3, 0])
        ax_lab = axis_labels(ax, r"x/\rho_{L0}\ [1]", r"y/\rho_{L0}\ [1]")
        ax_lab[1].align_to(ax.y_axis, LEFT).shift(LEFT * 0.4)
        ax_lab[0].next_to(ax.x_axis.get_right(), RIGHT, buff=0.15)
        tracker = ValueTracker(0.0)

        def idx():
            return min(int(tracker.get_value() / SINGLE_T * (len(t1) - 1)), len(t1) - 1)

        def orbit_path():
            i = idx()
            if i < 2:
                return VMobject()
            lo = max(0, i - 400)
            faint = VMobject().set_points_as_corners([ax.c2p(*p) for p in x1[:lo + 1:3]]) \
                if lo > 3 else VMobject()
            faint.set_stroke(ION, 1.0, 0.25)
            bright = VMobject().set_points_as_corners([ax.c2p(*p) for p in x1[lo:i + 1:2]])
            bright.set_stroke(ION, 2.2, 0.9)
            return VGroup(faint, bright)

        def centre_path():
            i = idx()
            k = int(np.searchsorted(hits, t1[i], side="right"))
            nodes = [np.zeros(2)]
            for h in hits[:k]:
                j = min(int(np.searchsorted(t1, h)) + 1, len(t1) - 1)
                nodes.append(c1[j])
            group = VGroup()
            if len(nodes) > 1:
                group.add(VMobject().set_points_as_corners([ax.c2p(*p) for p in nodes])
                          .set_stroke(INK, THIN_WIDTH + 0.4))
            group.add(*[Dot(ax.c2p(*p), radius=0.05, color=INK) for p in nodes])
            return group

        def particle():
            i = idx()
            tri = Triangle(color=ION, fill_opacity=1.0, stroke_width=0).scale(0.11)
            return tri.move_to(ax.c2p(*x1[i]))

        def flash():
            t = tracker.get_value()
            near = hits[(hits <= t) & (hits > t - 2.5)]
            group = VGroup()
            for h in near:
                j = int(np.searchsorted(t1, h))
                fade = 1.0 - (t - h) / 2.5
                group.add(Star(n=6, outer_radius=0.22, inner_radius=0.09, color=GREEN,
                               fill_opacity=0.9 * fade, stroke_width=0).move_to(ax.c2p(*x1[j])))
            return group

        orbit = always_redraw(orbit_path)
        walk = always_redraw(centre_path)
        ion = always_redraw(particle)
        sparks = always_redraw(flash)

        b_key = VGroup(VGroup(Circle(radius=0.11, color=B_FIELD, stroke_width=2.0),
                              Dot(radius=0.03, color=B_FIELD)),
                       math(r"\mathbf{B}=B_0", color=B_FIELD, size=MATH_SMALL)).arrange(RIGHT, buff=0.15)
        keys = VGroup(
            b_key,
            VGroup(Triangle(color=ION, fill_opacity=1, stroke_width=0).scale(0.1),
                   label("ion orbit", color=ION, size=SMALL_SIZE)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(radius=0.06, color=INK), label("guiding centre", color=INK, size=SMALL_SIZE))
            .arrange(RIGHT, buff=0.15),
            VGroup(Star(n=6, outer_radius=0.15, inner_radius=0.06, color=GREEN, fill_opacity=0.9,
                        stroke_width=0), label("collision", color=GREEN, size=SMALL_SIZE))
            .arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.6, 2.0, 0])
        laws = VGroup(
            math(r"\Delta\mathbf{R}=\frac{m_\alpha}{q_\alpha}\frac{\Delta\mathbf{v}\times\mathbf{B}}{B^2}",
                 color=INK, size=MATH_SMALL),
            math(r"\langle|\Delta\mathbf{R}|^2\rangle=2\rho_L^2", color=INK, size=MATH_SMALL),
            math(r"\nu=0.1\,\omega_{c0}", color=MUTED, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(keys, DOWN, buff=0.5).align_to(keys, LEFT)
        clock_lab = math(r"\omega_{c0}t=", color=MUTED, size=MATH_SMALL).move_to([4.2, -3.1, 0])
        clock = DecimalNumber(0, num_decimal_places=0, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            m.set_value(tracker.get_value())
            m.next_to(clock_lab, RIGHT, buff=0.12)

        clock.add_updater(place_clock)
        place_clock(clock)

        self.play(Create(ax), FadeIn(ax_lab), FadeIn(keys), FadeIn(laws), run_time=0.8, rate_func=EASE)
        self.add(orbit, walk, sparks, ion, clock_lab, clock)
        self.play(tracker.animate.set_value(SINGLE_T), run_time=PLAY_SINGLE, rate_func=LINEAR)
        self.wait(0.6)
        clock.clear_updaters()
        part1 = VGroup(ax, ax_lab, keys, laws, clock_lab, clock, orbit, walk, sparks, ion)
        self.play(FadeOut(part1), run_time=0.6, rate_func=EASE)

        # ---- part 2: ensemble mean square displacement for three fields --
        styles = [(BLUE, "o", 1.0), (ORANGE, "s", 2.0), (PURPLE, "t", 4.0)]
        curves = [mean_square(b) for b in B_VALUES]
        d_meas = [measured_diffusion(b) for b in B_VALUES]
        d_form = [diffusion_formula(b) for b in B_VALUES]

        mx = axes([0, 400, 100], [0, 100, 20], 5.2, 4.6).move_to([-3.6, 0.0, 0])
        mx_lab = axis_labels(mx, r"\omega_{c0}t\ [1]", r"\langle|\Delta\mathbf{R}|^2\rangle/\rho_{L0}^2\ [1]")
        mx_lab[1].align_to(mx.y_axis, LEFT).shift(LEFT * 0.3)
        mx_lab[0].next_to(mx.x_axis.get_right(), RIGHT, buff=0.15).shift(UP * 0.22)
        nums = VGroup()
        for v in (0, 200, 400):
            nums.add(math(str(v), color=MUTED, size=MATH_SMALL).next_to(mx.c2p(v, 0), DOWN, buff=0.15))
        for v in (0, 50, 100):
            nums.add(math(str(v), color=MUTED, size=MATH_SMALL).next_to(mx.c2p(0, v), LEFT, buff=0.15))
        t_now = ValueTracker(0.0)

        def marker(kind, color, at):
            if kind == "o":
                return Dot(at, radius=0.07, color=color)
            if kind == "s":
                return Square(0.14, color=color, fill_opacity=1, stroke_width=0).move_to(at)
            return Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.09).move_to(at)

        def msd_curve(k):
            def make():
                t, msd = curves[k]
                color, kind, _ = styles[k]
                n = max(2, int(np.searchsorted(t, t_now.get_value(), side="right")))
                line = VMobject().set_points_as_corners([mx.c2p(a, b) for a, b in zip(t[:n], msd[:n])])
                line.set_stroke(color, CURVE_WIDTH - 1)
                return VGroup(line, marker(kind, color, mx.c2p(t[n - 1], msd[n - 1])))
            return always_redraw(make)

        theory = VGroup(*[
            DashedLine(mx.c2p(0, 0), mx.c2p(400, 4 * d * 400) if 4 * d * 400 <= 100
                       else mx.c2p(100 / (4 * d), 100), color=FAINT, stroke_width=THIN_WIDTH,
                       dash_length=0.1) for d in d_form])
        legend = VGroup(*[
            VGroup(marker(kind, color, ORIGIN),
                   math(rf"B={b:g}B_0" if b != 1 else r"B=B_0", color=color, size=MATH_SMALL)).arrange(RIGHT, buff=0.15)
            for color, kind, b in styles],
            VGroup(DashedLine(ORIGIN, RIGHT * 0.4, color=FAINT, stroke_width=THIN_WIDTH, dash_length=0.1),
                   math(r"4D_\perp t", color=FAINT, size=MATH_SMALL)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(mx.c2p(110, 78))
        ens = math(r"4000\ \mathrm{ions\ per\ field},\ \nu=0.1\,\omega_{c0}", color=MUTED,
                   size=MATH_SMALL).next_to(mx, DOWN, buff=0.75)

        self.play(Create(mx), FadeIn(mx_lab), FadeIn(nums), FadeIn(legend), FadeIn(ens),
                  run_time=0.8, rate_func=EASE)
        self.add(theory, *[msd_curve(k) for k in range(3)])
        self.play(t_now.animate.set_value(T_END), run_time=PLAY_MSD, rate_func=LINEAR)

        # Scaling panel: D_perp against B on log axes (u = log10 B/B_0 + 0.15,
        # w = log10 D + 3, so that the axes meet in the lower left corner).
        def lp(b, d):
            return lx.c2p(np.log10(b) + 0.15, np.log10(d) + 3)

        lx = axes([0, 0.9, 0.3], [0, 2, 1], 3.2, 2.8, ticks=False).move_to([3.4, 1.15, 0])
        lx_nums = VGroup()
        for b in (1, 2, 4):
            lx_nums.add(math(str(b), color=MUTED, size=MATH_SMALL).next_to(lp(b, 1e-3), DOWN, buff=0.15))
        for e in (-3, -2, -1):
            lx_nums.add(math(rf"10^{{{e}}}", color=MUTED, size=MATH_SMALL)
                        .next_to(lx.c2p(0, e + 3), LEFT, buff=0.12))
        lx_lab = VGroup(
            math(r"B/B_0\ [1]", color=MUTED, size=MATH_SMALL).next_to(lx.x_axis.get_right(), RIGHT, buff=0.15),
            math(r"D_\perp/(\rho_{L0}^2\omega_{c0})\ [1]", color=MUTED, size=MATH_SMALL)
            .next_to(lx.y_axis.get_top(), UP, buff=0.18).align_to(lx.y_axis, LEFT).shift(LEFT * 0.5))
        bb = np.array([10 ** -0.12, 10 ** 0.72])
        law = DashedLine(lp(bb[0], 0.5 * NU / bb[0] ** 2), lp(bb[1], 0.5 * NU / bb[1] ** 2),
                         color=FAINT, stroke_width=THIN_WIDTH, dash_length=0.1)
        law_lab = math(r"\nu\rho_L^2/2\propto B^{-2}", color=FAINT, size=MATH_SMALL)
        law_lab.move_to(lx.c2p(0.33, 0.35))
        points = VGroup(*[marker(kind, color, lp(b, d))
                          for (color, kind, b), d in zip(styles, d_meas)])
        slope = np.polyfit(np.log10(B_VALUES), np.log10(d_meas), 1)[0]
        table = VGroup(
            math(r"D_\perp:\ \mathrm{walk}\ \mid\ v_\perp^2\nu/[2(\nu^2+\omega_c^2)]",
                 color=MUTED, size=MATH_SMALL),
            *[math((rf"B={b:g}B_0" if b != 1 else r"B=B_0") + rf":\ {dm:.4f}\ \mid\ {df:.4f}", color=styles[k][0], size=MATH_SMALL)
              for k, (b, dm, df) in enumerate(zip(B_VALUES, d_meas, d_form))],
            math(rf"\mathrm{{fitted\ slope}}\ {slope:.2f}", color=INK, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        table.move_to([0, -2.15, 0]).align_to([0.85, 0, 0], LEFT)
        self.play(FadeOut(ens), Create(lx), FadeIn(lx_nums), FadeIn(lx_lab), Create(law), FadeIn(law_lab),
                  run_time=0.8, rate_func=EASE)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in points], lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(table), run_time=0.6)
        self.wait(3.0)
