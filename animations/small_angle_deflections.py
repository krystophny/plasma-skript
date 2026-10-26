"""Many small Coulomb deflections against the rare large one.

Model: a test electron (charge q_alpha = -e, mass m_alpha) crosses a field of
fixed singly charged ions (q_beta = e, infinitely heavy, density n) at speed
v along a straight path of length s.  Each ion it passes has an impact
parameter b drawn uniformly in area from 0 to b_max, and deflects the
electron by the exact Rutherford angle

    tan(theta/2) = b_90/b,    b_90 = |q_alpha q_beta|/(4 pi eps_0 m_alpha v^2),

in a random azimuth phi.  The accumulated deflection is the vector sum
Delta theta = sum_k theta_k (cos phi_k, sin phi_k), valid while it stays
small; the number of encounters in s is Poisson with mean n pi b_max^2 s.

Normalization: impact parameters in b_90, path length in the 90-degree mean
free path lambda_90 = 1/(n pi b_90^2), so s/lambda_90 [1] and b/b_90 [1];
angles in rad.  Parameters: b_max = 10^3 b_90 (ln Lambda = ln(b_max/b_90)
= 6.91), 12000 electrons, s/lambda_90 up to 0.005, about 5000 encounters per
electron and one strong encounter (b < b_90) per 200 electrons; 70 of them are
drawn.

Check (scripts/check-physics.py): the small-angle Coulomb-logarithm rate

    d<Delta theta^2>/ds = 8 pi n b_90^2 ln(b_max/b_90),  i.e. 8 ln Lambda per lambda_90,

plus the order-one strong-encounter constant C of the exact Rutherford
angle, d<Delta theta^2>/d(s/lambda_90) = 8 (ln Lambda + C), C = 0.266 from
quadrature; every decade of b with b >> b_90 contributes 8 ln 10, the strong
encounters b < b_90 together only 8 x 0.515.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, AXIS, AXIS_WIDTH, CURVE_WIDTH, EASE, ELECTRON, FAINT, GREEN, INK,
    LINEAR, MATH_SIZE, MATH_SMALL, MUTED, SMALL_SIZE, THIN_WIDTH, StyledScene,
    axes, label, math,
)

B_MAX = 1.0e3                 # b_max/b_90 [1]
S_END = 5.0e-3                # s/lambda_90 [1] at the end of the run
N_ELECTRONS = 12000
N_S = 200                     # path-length samples
EDGES = [0.0, 1.0, 10.0, 100.0, 1000.0]   # impact-parameter bins b/b_90 [1]
SEED = 11
N_SHOWN = 70                  # electrons drawn in the deflection plane


def rutherford_angle(b):
    """Exact Coulomb deflection with b in units of b_90."""
    return 2.0 * np.arctan(1.0 / b)


def simulate(n_electrons=N_ELECTRONS, s_end=S_END, b_max=B_MAX, n_s=N_S, seed=SEED):
    """Monte Carlo deflections.

    Returns s (n_s+1,), deflection vectors (n_electrons, n_s+1, 2), the
    per-bin cumulative mean of theta^2 (len(EDGES)-1, n_s+1) and the largest
    single angle of each electron.
    """
    rng = np.random.default_rng(seed)
    s = np.linspace(0.0, s_end, n_s + 1)
    vec = np.zeros((n_electrons, n_s + 1, 2))
    bins = np.zeros((len(EDGES) - 1, n_s + 1))
    largest = np.zeros(n_electrons)
    mean_count = s_end * b_max**2        # n pi b_max^2 s with s in lambda_90
    chunk = 250
    for start in range(0, n_electrons, chunk):
        stop = min(start + chunk, n_electrons)
        counts = rng.poisson(mean_count, stop - start)
        owner = np.repeat(np.arange(stop - start), counts)
        total = counts.sum()
        b = b_max * np.sqrt(rng.random(total))
        theta = rutherford_angle(b)
        phi = 2 * np.pi * rng.random(total)
        where = np.minimum((rng.random(total) * n_s).astype(int), n_s - 1) + 1
        key = owner * (n_s + 1) + where
        size = (stop - start) * (n_s + 1)
        for k, comp in enumerate((np.cos(phi), np.sin(phi))):
            step = np.bincount(key, theta * comp, size).reshape(stop - start, n_s + 1)
            vec[start:stop, :, k] = np.cumsum(step, axis=1)
        which = np.digitize(b, EDGES) - 1
        for j in range(len(EDGES) - 1):
            sel = which == j
            step = np.bincount(where[sel], theta[sel] ** 2, n_s + 1)
            bins[j] += np.cumsum(step)
        big = np.zeros(stop - start)
        np.maximum.at(big, owner, theta)
        largest[start:stop] = big
    return s, vec, bins / n_electrons, largest


def strong_constant():
    """C in rate = 8 (ln b_max/b_90 + C), from trapezoidal quadrature in ln b."""
    u = np.linspace(np.log(1e-6), np.log(1e6), 400001)
    x = np.exp(u)
    integrand = rutherford_angle(x) ** 2 * 2 * x * x - 8.0 * (x > 1.0)
    return float(np.sum((integrand[1:] + integrand[:-1]) / 2 * np.diff(u)) / 8.0)


def bin_rate(lo, hi):
    """Exact contribution of b/b_90 in [lo, hi] per unit s/lambda_90."""
    u = np.linspace(np.log(max(lo, 1e-8)), np.log(hi), 200001)
    x = np.exp(u)
    integrand = rutherford_angle(x) ** 2 * 2 * x * x
    return float(np.sum((integrand[1:] + integrand[:-1]) / 2 * np.diff(u)))


def log_rate(b_max=B_MAX):
    """Leading-log small-angle rate 8 ln(b_max/b_90) per lambda_90."""
    return 8.0 * np.log(b_max)


def measured_rate(s, vec):
    """Least-squares slope through the origin of <|Delta theta|^2>(s)."""
    msd = np.mean(np.sum(vec**2, axis=2), axis=0)
    return float(np.sum(s * msd) / np.sum(s * s)), msd


class SmallAngleDeflections(StyledScene):
    """Deflection plane, mean-square growth and contribution by decade of b."""

    def build(self):
        s, vec, bins, largest = simulate()
        rate, msd = measured_rate(s, vec)
        exact = 8.0 * (np.log(B_MAX) + strong_constant())
        bin_exact = [bin_rate(lo, hi) for lo, hi in zip(EDGES[:-1], EDGES[1:])]

        # Drawn: the first N_SHOWN-1 electrons plus the first one whose
        # strongest encounter deflected it by 90 to 103 degrees (b just below b_90).
        strong = np.where((largest > np.pi / 2) & (largest < 1.8))[0]
        hit = int(strong[0]) if len(strong) else int(np.argmax(largest))
        shown = list(range(N_SHOWN - 1)) + [hit]
        trails = [3, 17, hit]

        tracker = ValueTracker(0.0)

        def index():
            return int(round(tracker.get_value() * N_S))

        # --- left: deflection plane ------------------------------------------
        lim = 2.0
        plane = axes([-lim, lim, 1.0], [-lim, lim, 1.0], 5.0, 5.0).move_to([-3.9, -0.55, 0])
        plane_lab = VGroup(
            math(r"\Delta\theta_x\ [\mathrm{rad}]", color=MUTED, size=MATH_SMALL)
            .next_to(plane.x_axis.get_right(), DOWN, buff=0.2).align_to(plane.x_axis.get_right(), RIGHT),
            math(r"\Delta\theta_y\ [\mathrm{rad}]", color=MUTED, size=MATH_SMALL)
            .next_to(plane.y_axis.get_top(), RIGHT, buff=0.12).shift(DOWN * 0.2),
        )
        plane_lab.add(*[math(txt, color=MUTED, size=MATH_SMALL).next_to(plane.c2p(0, v), LEFT, buff=0.1)
                        for v, txt in [(1, "1"), (-1, "-1")]])
        law = math(r"\tan\frac{\theta}{2} = \frac{b_{90}}{b}", color=INK, size=MATH_SIZE)
        law.move_to([-5.4, 3.0, 0])
        key = VGroup(
            VGroup(Dot(radius=0.06, color=ELECTRON),
                   label("one electron", color=ELECTRON, size=SMALL_SIZE)).arrange(RIGHT, buff=0.15),
            VGroup(Circle(radius=0.13, color=ACCENT, stroke_width=THIN_WIDTH),
                   label("met b < b", color=ACCENT, size=SMALL_SIZE)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-2.4, 3.05, 0])
        # subscript of b_90 in the key as math, so it matches the axes
        key[1][1].become(math(r"\text{met } b < b_{90}", color=ACCENT, size=MATH_SMALL)
                         .next_to(key[1][0], RIGHT, buff=0.12))

        def clip(p):
            return np.clip(p, -lim, lim)

        def dots():
            i = index()
            return VGroup(*[Dot(plane.c2p(*clip(vec[e, i])), radius=0.05,
                                color=ACCENT if e == hit else ELECTRON) for e in shown])

        def trail(e, color, width):
            i = max(index(), 1)
            pts = [plane.c2p(*clip(vec[e, k])) for k in range(i + 1)]
            return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)

        trail_mobs = VGroup(*[
            always_redraw(lambda e=e: trail(e, ACCENT if e == hit else INK,
                                            THIN_WIDTH if e == hit else 1.6))
            for e in trails])
        dot_mobs = always_redraw(dots)
        hit_ring = always_redraw(lambda: Circle(radius=0.16, color=ACCENT, stroke_width=THIN_WIDTH)
                                 .move_to(plane.c2p(*clip(vec[hit, index()]))))

        # --- right top: mean-square deflection --------------------------------
        y_top = 0.4
        msd_ax = axes([0, S_END, S_END / 5], [0, y_top, 0.1], 5.2, 2.2).move_to([3.75, 1.8, 0])
        x_lab = math(r"s/\lambda_{90}\ [1]", color=MUTED, size=MATH_SMALL)
        x_lab.next_to(msd_ax.x_axis.get_right(), DOWN, buff=0.14).align_to(msd_ax.x_axis.get_right(), RIGHT)
        y_lab = math(r"\langle\Delta\theta^2\rangle\ [\mathrm{rad}^2]", color=MUTED, size=MATH_SMALL)
        y_lab.next_to(msd_ax.y_axis.get_top(), UP, buff=0.12).align_to(msd_ax.y_axis, LEFT)
        ticks = VGroup(
            math("0", color=MUTED, size=MATH_SMALL).next_to(msd_ax.c2p(0, 0), DOWN, buff=0.14),
            math("0.0025", color=MUTED, size=MATH_SMALL).next_to(msd_ax.c2p(0.0025, 0), DOWN, buff=0.14),
            math("0.2", color=MUTED, size=MATH_SMALL).next_to(msd_ax.c2p(0, 0.2), LEFT, buff=0.1),
            math("0.4", color=MUTED, size=MATH_SMALL).next_to(msd_ax.c2p(0, 0.4), LEFT, buff=0.1),
        )
        theory = DashedVMobject(Line(msd_ax.c2p(0, 0), msd_ax.c2p(S_END, exact * S_END),
                                     color=GREEN, stroke_width=THIN_WIDTH), num_dashes=24)
        theory_key = VGroup(
            DashedVMobject(Line(ORIGIN, RIGHT * 0.5, color=GREEN, stroke_width=THIN_WIDTH), num_dashes=3),
            math(r"8(\ln\Lambda + C)\,s/\lambda_{90}", color=GREEN, size=MATH_SMALL),
        ).arrange(RIGHT, buff=0.12)
        sim_key = VGroup(
            Line(ORIGIN, RIGHT * 0.5, color=ELECTRON, stroke_width=CURVE_WIDTH),
            label("12 000 electrons", color=ELECTRON, size=SMALL_SIZE),
        ).arrange(RIGHT, buff=0.12)
        keys = VGroup(theory_key, sim_key).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        keys.next_to(msd_ax.c2p(0, y_top), RIGHT, buff=0.3).align_to(msd_ax.c2p(0, y_top), UP)

        def msd_curve():
            i = max(index(), 1)
            pts = [msd_ax.c2p(s[k], msd[k]) for k in range(i + 1)]
            return VMobject(stroke_color=ELECTRON, stroke_width=CURVE_WIDTH).set_points_as_corners(pts)

        msd_mob = always_redraw(msd_curve)
        msd_dot = always_redraw(lambda: Dot(msd_ax.c2p(s[index()], msd[index()]),
                                            radius=0.07, color=ELECTRON))

        # --- right bottom: contribution per decade of b -------------------------
        bar_w, step, bar_h = 0.75, 1.48, 1.45
        base = np.array([0.7, -3.0, 0])
        scale = bar_h / (bin_exact[3] * S_END)
        bar_x = [base[0] + 0.45 + j * step for j in range(4)]
        floor = Line(base, base + RIGHT * (4 * step + 0.05), color=AXIS, stroke_width=AXIS_WIDTH)
        names = [r"0\!-\!1", r"1\!-\!10", r"10\!-\!10^2", r"10^2\!-\!10^3"]
        bar_names = VGroup(*[
            math(n, color=MUTED, size=MATH_SMALL).move_to([x, base[1] - 0.28, 0])
            for n, x in zip(names, bar_x)])
        bar_axis = math(r"b/b_{90}\ [1]", color=MUTED, size=MATH_SMALL)
        bar_axis.next_to(bar_names, LEFT, buff=0.3)
        bar_title = label("contribution by decade of b", color=MUTED, size=SMALL_SIZE)
        bar_title.move_to([3.75, base[1] + bar_h + 0.5, 0])

        def bars():
            i = index()
            group = VGroup()
            for j, x in enumerate(bar_x):
                h = max(bins[j, i] * scale, 0.001)
                group.add(Rectangle(width=bar_w, height=h, stroke_width=0,
                                    fill_color=ACCENT if j == 0 else ELECTRON,
                                    fill_opacity=0.85).move_to([x, base[1] + h / 2, 0]))
                target = bin_exact[j] * s[i] * scale
                group.add(Line([x - bar_w / 2 - 0.1, base[1] + target, 0],
                               [x + bar_w / 2 + 0.1, base[1] + target, 0],
                               color=GREEN, stroke_width=THIN_WIDTH))
            return group

        bar_mob = always_redraw(bars)
        strong_tag = label("strong", color=ACCENT, size=SMALL_SIZE)
        strong_tag.move_to([bar_x[0], base[1] + 0.95, 0])

        self.play(Create(plane), FadeIn(plane_lab), FadeIn(law), FadeIn(key),
                  run_time=1.0, rate_func=EASE)
        self.play(Create(msd_ax), FadeIn(x_lab), FadeIn(y_lab), FadeIn(ticks), FadeIn(theory),
                  FadeIn(keys), Create(floor), FadeIn(bar_names), FadeIn(bar_axis),
                  FadeIn(bar_title), FadeIn(strong_tag), run_time=1.0, rate_func=EASE)
        self.add(trail_mobs, dot_mobs, hit_ring, msd_mob, msd_dot, bar_mob)
        self.play(tracker.animate.set_value(1.0), run_time=14.0, rate_func=LINEAR)

        numbers = VGroup(
            math(rf"\text{{slope: }}{rate:.1f}", color=ELECTRON, size=MATH_SMALL),
            math(rf"8({np.log(B_MAX):.2f} + {exact / 8 - np.log(B_MAX):.2f}) = {exact:.1f}",
                 color=GREEN, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        numbers.arrange(RIGHT, buff=0.5).move_to([3.75, -0.45, 0])
        self.play(FadeIn(numbers), run_time=0.8, rate_func=EASE)
        self.wait(3.0)
