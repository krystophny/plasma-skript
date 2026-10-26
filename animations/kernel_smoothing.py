"""Kernel smoothing: from particles (sum of deltas) to a smooth density.

Model (1D, periodic domain of length L = 80 Delta, Delta = mean particle
spacing, all lengths in Delta [1], densities n Delta [1] with mean 1):

* particles x_i are an ideal-gas (Poisson) sample of a known density
  n(x) Delta = c [1 + 0.4 sin(2 pi x/L) + 1.5 exp(-(x - 52)^2/(2 * 4^2))],
  c normalizing the mean to 1; one fixed realization is shown;
* the Klimontovich density is N(x) = sum_i delta(x - x_i);
* the Gaussian kernel K_h(u) = exp(-u^2/(2 h^2))/(sqrt(2 pi) h), periodic
  images included, gives the smoothed density
      n_h(x) = sum_i K_h(x - x_i) = (K_h * N)(x) = int K_h(x - x') N(x') dx'.

Statistics (exact for Poisson particles): E n_h = K_h * n (the bias
K_h * n - n grows with h), Var n_h(x) = (K_h^2 * n)(x).  Averaged over the
periodic domain the variance is n_bar int K_h^2 = n_bar/(2 sqrt(pi) h)
(times an image sum), so the relative noise is 1/sqrt(N_h) with
N_h = 2 sqrt(pi) n h particles per kernel width.

KernelSmoothing builds n_h kernel by kernel and then as a sliding
convolution; KernelWidth varies h from 0.25 to 20 Delta against the true
n(x) and shows the measured noise and bias.
"""

from manim import *
import numpy as np

from style import (
    BLUE, CURVE_WIDTH, DOT_RADIUS, EASE, ELECTRON, FAINT, GREEN, GRID, INK, LINEAR,
    MATH_SIZE, MATH_SMALL, MUTED, THIN_WIDTH, VERMILION, StyledScene, axes, math,
)

DOMAIN = 80.0                    # L/Delta [1]
N_MEAN = 80                      # mean particle number (n_bar Delta = 1)
WAVE_A = 0.4                     # broad modulation, wavelength L
BUMP_X = 52.0                    # narrow structure: centre, Delta [1]
BUMP_W = 4.0                     # width, Delta [1]
BUMP_A = 1.5                     # amplitude relative to the background
NORM = 1.0 / (1.0 + BUMP_A * BUMP_W * np.sqrt(2 * np.pi) / DOMAIN)
SEED = 7                         # displayed realization
STAT_SEED = 2026                 # Monte Carlo of the error statistics
H_DEMO = 1.5                     # kernel width of the build-up scene, Delta [1]
IMAGES = (-2, -1, 0, 1, 2)       # periodic images of the kernel


def true_density(x):
    """n(x) Delta [1], mean 1 over the period."""
    d = (x - BUMP_X + DOMAIN / 2) % DOMAIN - DOMAIN / 2
    return NORM * (1 + WAVE_A * np.sin(2 * np.pi * x / DOMAIN)
                   + BUMP_A * np.exp(-d * d / (2 * BUMP_W**2)))


def sample(rng, n_mean=N_MEAN):
    """Poisson number of iid positions drawn from true_density (rejection)."""
    count = rng.poisson(n_mean)
    top = NORM * (1 + WAVE_A + BUMP_A)
    out = np.empty(0)
    while out.size < count:
        x = rng.uniform(0, DOMAIN, 4 * count + 16)
        keep = rng.uniform(0, top, x.size) < true_density(x)
        out = np.concatenate([out, x[keep]])
    return np.sort(out[:count])


def kernel(u, h):
    """Periodic Gaussian K_h(u) [1/Delta], normalized to 1 over the period."""
    u = np.asarray(u, float)
    return sum(np.exp(-(u + m * DOMAIN) ** 2 / (2 * h * h)) for m in IMAGES) / (np.sqrt(2 * np.pi) * h)


def smoothed(x, particles, h):
    """n_h(x) Delta = sum_i K_h(x - x_i)."""
    x = np.asarray(x, float)
    return kernel(x[:, None] - np.asarray(particles)[None, :], h).sum(axis=1)


def smoothed_truth(x, h):
    """E n_h = K_h * n, analytic for the sine plus Gaussian profile."""
    k = 2 * np.pi / DOMAIN
    s2 = BUMP_W**2 + h * h
    bump = sum(np.exp(-(x - BUMP_X + m * DOMAIN) ** 2 / (2 * s2)) for m in IMAGES)
    return NORM * (1 + WAVE_A * np.exp(-0.5 * (k * h) ** 2) * np.sin(k * x)
                   + BUMP_A * BUMP_W / np.sqrt(s2) * bump)


def noise_theory(h):
    """RMS over x of the noise of n_h Delta: sqrt(n_bar int K_h^2), periodic."""
    images = sum(np.exp(-(m * DOMAIN) ** 2 / (4 * h * h)) for m in IMAGES)
    return np.sqrt(images / (2 * np.sqrt(np.pi) * h))


def bias_rms(h, points=1600):
    """RMS over x of K_h * n - n (exact, no particles)."""
    x = (np.arange(points) + 0.5) * DOMAIN / points
    return float(np.sqrt(np.mean((smoothed_truth(x, h) - true_density(x)) ** 2)))


def error_statistics(widths, realizations=300, points=400, seed=STAT_SEED):
    """Monte Carlo rms noise and rms total error of n_h for each width h."""
    rng = np.random.default_rng(seed)
    x = (np.arange(points) + 0.5) * DOMAIN / points
    noise2 = np.zeros(len(widths))
    total2 = np.zeros(len(widths))
    truth = true_density(x)
    for _ in range(realizations):
        p = sample(rng)
        for j, h in enumerate(widths):
            n_h = smoothed(x, p, h)
            noise2[j] += np.mean((n_h - smoothed_truth(x, h)) ** 2)
            total2[j] += np.mean((n_h - truth) ** 2)
    return np.sqrt(noise2 / realizations), np.sqrt(total2 / realizations)




# ---------------------------------------------------------------------------

X_SCREEN = 12.6                  # main axes width in Manim units


def main_axes(y_max, height, centre, y_tex):
    """Particle axis x/Delta [1] with a density axis; labels clear of the data."""
    ax = axes([0, DOMAIN, 10], [0, y_max, 1], X_SCREEN, height, ticks=False).move_to(centre)
    ax.y_axis.set_opacity(0)
    ticks = VGroup(*[
        VGroup(Line(ax.c2p(v, 0), ax.c2p(v, 0) + DOWN * 0.08, color=MUTED, stroke_width=1.6),
               math(f"{v:d}", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, 0), DOWN, buff=0.14))
        for v in range(0, int(DOMAIN), 20)])
    y_ticks = VGroup(*[
        VGroup(Line(ax.c2p(0, v), ax.c2p(0, v) + LEFT * 0.08, color=MUTED, stroke_width=1.6),
               math(f"{v:d}", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(0, v), LEFT, buff=0.14))
        for v in range(0, int(y_max) + 1)])
    y_line = Line(ax.c2p(0, 0), ax.c2p(0, y_max), color=INK, stroke_width=1.6)
    end_tick = Line(ax.c2p(DOMAIN, 0), ax.c2p(DOMAIN, 0) + DOWN * 0.08, color=MUTED, stroke_width=1.6)
    x_lab = math(r"x/\Delta\ [1]", color=MUTED, size=MATH_SMALL)
    x_lab.next_to(ax.c2p(DOMAIN, 0), DOWN, buff=0.14).align_to(ax.c2p(DOMAIN, 0), RIGHT)
    y_lab = math(y_tex, color=MUTED, size=MATH_SMALL).next_to(ax.c2p(0, y_max), RIGHT, buff=0.2)
    return ax, VGroup(ticks, y_ticks, y_line, end_tick, x_lab, y_lab)


def curve(ax, x, y, color, width, y_max=None, opacity=1.0):
    y = np.asarray(y) if y_max is None else np.minimum(y, y_max)
    pts = [ax.c2p(a, b) for a, b in zip(x, y)]
    return VMobject().set_points_as_corners(pts).set_stroke(color, width, opacity)


class KernelSmoothing(StyledScene):
    """Delta spikes, one Gaussian per particle, and the sliding convolution."""

    def build(self):
        rng = np.random.default_rng(SEED)
        particles = sample(rng)
        n = len(particles)
        h = H_DEMO
        y_max = 3.2
        ax, frame = main_axes(y_max, 4.0, [0.25, 0.45, 0], r"n_h\Delta\ [1]")
        grid_x = np.linspace(0, DOMAIN, 1200)
        kernels = kernel(grid_x[None, :] - particles[:, None], h)       # (n, grid)
        total = kernels.sum(axis=0)

        spike_h = 0.9
        dots = VGroup(*[Dot(ax.c2p(p, 0), radius=DOT_RADIUS, color=ELECTRON) for p in particles])
        spikes = VGroup(*[Arrow(ax.c2p(p, 0), ax.c2p(p, 0) + UP * spike_h, buff=0, color=ELECTRON,
                                stroke_width=1.6, max_tip_length_to_length_ratio=0.12,
                                max_stroke_width_to_length_ratio=10) for p in particles])
        title = math(r"N(x)=\sum_i\delta(x-x_i)\quad\mathrm{(Klimontovich;\ arrows:\ }\delta\mathrm{,\ weight\ 1)}",
                     color=INK, size=MATH_SIZE).to_edge(UP, buff=0.4)
        params = math(rf"N={n}\ \mathrm{{particles}},\ \Delta=\mathrm{{mean\ spacing}},\ h={h:g}\,\Delta",
                      color=MUTED, size=MATH_SMALL).to_edge(DOWN, buff=0.45)

        self.add(frame, params)
        self.play(FadeIn(title), LaggedStart(*[AnimationGroup(FadeIn(d), GrowArrow(s))
                                               for d, s in zip(dots, spikes)], lag_ratio=0.03),
                  run_time=2.5, rate_func=LINEAR)
        self.wait(1.0)

        # --- one kernel per particle, summed left to right ------------------
        build_title = math(r"n_h(x)=\sum_i K_h(x-x_i),\qquad K_h(u)=\frac{e^{-u^2/2h^2}}{\sqrt{2\pi}\,h}",
                           color=INK, size=MATH_SIZE).to_edge(UP, buff=0.3)
        count = ValueTracker(0.0)

        def added():
            return int(np.clip(round(count.get_value()), 0, n))

        def make_kernels():
            k = added()
            group = VGroup()
            for i in range(k):
                near = np.abs(grid_x - particles[i]) < 4 * h
                group.add(curve(ax, grid_x[near], kernels[i, near], FAINT, 1.6))
            return group

        def make_sum():
            k = added()
            if k == 0:
                return VMobject()
            return curve(ax, grid_x, kernels[:k].sum(axis=0), VERMILION, CURVE_WIDTH - 0.8)

        kernel_lines = always_redraw(make_kernels)
        sum_line = always_redraw(make_sum)
        self.play(FadeOut(title, shift=UP * 0.2), FadeIn(build_title, shift=UP * 0.2),
                  spikes.animate.set_opacity(0.25), run_time=1.0, rate_func=EASE)
        self.add(kernel_lines, sum_line)
        self.play(count.animate.set_value(n), run_time=9.0, rate_func=LINEAR)
        self.wait(1.5)
        kernel_lines.clear_updaters()
        sum_line.clear_updaters()

        # --- the same sum as a sliding convolution --------------------------
        conv_title = math(r"n_h(x)=(K_h*N)(x)=\int K_h(x-x')\,N(x')\,dx'=\sum_i K_h(x-x_i)",
                          color=INK, size=MATH_SIZE).to_edge(UP, buff=0.3)
        note = math(r"K_h\ \mathrm{is\ even:\ the\ flipped\ kernel}\ K_h(x-x')\ \mathrm{looks\ the\ same}",
                    color=MUTED, size=MATH_SMALL).next_to(conv_title, DOWN, buff=0.12).shift(RIGHT * 1.2)
        self.play(FadeOut(build_title, shift=UP * 0.2), FadeIn(conv_title, shift=UP * 0.2), FadeIn(note),
                  FadeOut(kernel_lines), FadeOut(sum_line), spikes.animate.set_opacity(0.18),
                  run_time=1.2, rate_func=EASE)

        probe = ValueTracker(0.0)

        def make_window():
            # K_h(x - x') as a function of x', drawn to the scale of the density axis
            x0 = probe.get_value()
            xs = np.linspace(max(x0 - 4 * h, 0), min(x0 + 4 * h, DOMAIN), 100)
            pts = [ax.c2p(a, b) for a, b in zip(xs, kernel(x0 - xs, h))]
            area = Polygon(ax.c2p(xs[0], 0), *pts, ax.c2p(xs[-1], 0), stroke_width=0,
                           fill_color=GREEN, fill_opacity=0.28)
            edge = VMobject().set_points_as_corners(pts).set_stroke(GREEN, 2.2)
            return VGroup(area, edge)

        def make_weights():
            # each particle in the window contributes K_h(x - x_i); the same bars stacked at x
            x0 = probe.get_value()
            w = kernel(x0 - particles, h)
            inside = [i for i in np.argsort(-w) if w[i] > 2e-3]
            bars = VGroup(*[Line(ax.c2p(particles[i], 0), ax.c2p(particles[i], w[i]), color=GREEN,
                                 stroke_width=5) for i in inside])
            stack = VGroup()
            base = 0.0
            for k, i in enumerate(inside):
                stack.add(Line(ax.c2p(x0, base), ax.c2p(x0, base + w[i]),
                               color=GREEN if k % 2 == 0 else INK, stroke_width=7))
                base += w[i]
            return VGroup(bars, stack)

        def make_trace():
            x0 = probe.get_value()
            if x0 < 0.05:
                return VMobject()
            keep = grid_x <= x0
            return curve(ax, grid_x[keep], total[keep], VERMILION, CURVE_WIDTH - 0.8)

        window = always_redraw(make_window)
        weights = always_redraw(make_weights)
        trace = always_redraw(make_trace)
        tip = always_redraw(lambda: Dot(ax.c2p(probe.get_value(),
                                               smoothed(np.array([probe.get_value()]), particles, h)[0]),
                                        radius=DOT_RADIUS * 1.3, color=VERMILION))
        key = VGroup(
            Rectangle(width=0.35, height=0.2, fill_color=GREEN, fill_opacity=0.35, stroke_color=GREEN,
                      stroke_width=2),
            math(r"K_h(x-x')", color=MUTED, size=MATH_SMALL),
            Line(ORIGIN, UP * 0.3, color=GREEN, stroke_width=5),
            math(r"K_h(x-x_i)\ \mathrm{at\ each\ particle,\ stacked\ at}\ x", color=MUTED, size=MATH_SMALL),
            Line(ORIGIN, RIGHT * 0.45, color=VERMILION, stroke_width=CURVE_WIDTH - 0.8),
            math(r"n_h(x)", color=MUTED, size=MATH_SMALL),
        ).arrange(RIGHT, buff=0.18).next_to(params, UP, buff=0.3)
        self.add(window, trace, weights, tip)
        self.play(FadeIn(key), run_time=0.6)
        self.wait(1.5)
        # the note would cover the tallest peak; it has been read by now
        self.play(FadeOut(note), run_time=0.5, rate_func=EASE)
        self.play(probe.animate.set_value(DOMAIN), run_time=14.0, rate_func=LINEAR)
        self.wait(2.0)


class KernelWidth(StyledScene):
    """The same particles smoothed with h from 0.25 to 20 Delta: noise vs bias."""

    def build(self):
        rng = np.random.default_rng(SEED)
        particles = sample(rng)
        y_max = 4
        ax, frame = main_axes(y_max, 2.6, [0.25, 1.2, 0], r"n\Delta\ [1]")
        grid_x = np.linspace(0, DOMAIN, 1600)
        truth = curve(ax, grid_x, true_density(grid_x), INK, THIN_WIDTH)
        truth = DashedVMobject(truth, num_dashes=90, dashed_ratio=0.55)
        dots = VGroup(*[Dot(ax.c2p(p, 0), radius=DOT_RADIUS, color=ELECTRON) for p in particles])

        log_h = ValueTracker(np.log10(0.25))

        def h_now():
            return 10 ** log_h.get_value()

        def make_estimate():
            y = smoothed(grid_x, particles, h_now())
            return curve(ax, grid_x, y, VERMILION, CURVE_WIDTH - 1.0, y_max=y_max)

        def make_clip_marks():
            y = smoothed(grid_x, particles, h_now())
            over = y > y_max
            group = VGroup()
            if over.any():
                edges = np.flatnonzero(np.diff(np.r_[0, over.astype(int), 0]))
                for a, b in zip(edges[::2], edges[1::2]):
                    xm = grid_x[(a + b - 1) // 2]
                    group.add(Triangle(color=VERMILION, fill_opacity=1, stroke_width=0)
                              .scale(0.07).move_to(ax.c2p(xm, y_max) + UP * 0.1))
            return group

        estimate = always_redraw(make_estimate)
        clip_marks = always_redraw(make_clip_marks)

        legend = VGroup(
            DashedLine(ORIGIN, RIGHT * 0.5, color=INK, stroke_width=THIN_WIDTH, dash_length=0.08),
            math(r"\mathrm{true}\ n(x)", color=MUTED, size=MATH_SMALL),
            Line(ORIGIN, RIGHT * 0.5, color=VERMILION, stroke_width=CURVE_WIDTH - 1.0),
            math(r"n_h=K_h*N", color=MUTED, size=MATH_SMALL),
            Dot(radius=DOT_RADIUS, color=ELECTRON),
            math(rf"{len(particles)}\ \mathrm{{particles}}", color=MUTED, size=MATH_SMALL),
            Triangle(color=VERMILION, fill_opacity=1, stroke_width=0).scale(0.07),
            math(r"\mathrm{off\ scale}", color=MUTED, size=MATH_SMALL),
        ).arrange(RIGHT, buff=0.18)
        legend.to_edge(UP, buff=0.4).to_edge(RIGHT, buff=0.55)
        h_label = math(r"h/\Delta=", color=INK, size=MATH_SIZE).to_edge(UP, buff=0.38).to_edge(LEFT, buff=0.6)
        h_value = DecimalNumber(0.25, num_decimal_places=2, color=INK, font_size=MATH_SIZE)

        def place_h(m):
            m.set_value(h_now())
            m.next_to(h_label, RIGHT, buff=0.15)

        h_value.add_updater(place_h)
        place_h(h_value)

        # --- error panel: rms over x, in units of the mean density ---------
        widths = np.geomspace(0.25, 20, 13)
        noise, total = error_statistics(widths)
        lo_h, hi_h = np.log10(0.25), np.log10(20)
        lo_e, hi_e = -1.5, 0.3
        err = axes([lo_h, hi_h, 1], [lo_e, hi_e, 1], 4.7, 1.3, ticks=False).move_to([-3.6, -2.45, 0])
        err.x_axis.set_opacity(0)
        err.y_axis.set_opacity(0)
        err_frame = Rectangle(width=err.x_length, height=err.y_length, color=MUTED, stroke_width=1.4
                              ).move_to(err.get_center())
        x_vals = (0.3, 1, 3, 10)
        x_ticks = VGroup(*[math(f"{v:g}", color=MUTED, size=MATH_SMALL)
                           .next_to(err.c2p(np.log10(v), lo_e), DOWN, buff=0.08) for v in x_vals])
        y_ticks = VGroup(*[math(t, color=MUTED, size=MATH_SMALL).next_to(err.c2p(lo_h, v), LEFT, buff=0.1)
                           for v, t in ((-1, "0.1"), (0, "1"))])
        tick_lines = VGroup(*[Line(err.c2p(np.log10(v), lo_e), err.c2p(np.log10(v), lo_e + 0.07),
                                   color=MUTED, stroke_width=1.4) for v in x_vals],
                            *[Line(err.c2p(lo_h, v), err.c2p(lo_h + 0.04, v), color=MUTED, stroke_width=1.4)
                              for v in (-1, 0)])
        err_x = math(r"h/\Delta\ [1]", color=MUTED, size=MATH_SMALL).next_to(err_frame, RIGHT, buff=0.12
                                                                           ).align_to(err_frame, DOWN)
        err_y = math(r"\mathrm{rms\ error\ of}\ n_h\Delta\ [1]", color=MUTED,
                     size=MATH_SMALL).next_to(err_frame, UP, buff=0.1).align_to(err_frame, LEFT)
        hs = np.geomspace(0.25, 20, 200)
        theory = VMobject().set_points_as_corners(
            [err.c2p(np.log10(x), np.log10(noise_theory(x))) for x in hs]
        ).set_stroke(BLUE, 2.2)
        theory = DashedVMobject(theory, num_dashes=40, dashed_ratio=0.6)
        bias = np.array([bias_rms(x) for x in hs])
        show = bias > 10 ** lo_e
        bias_line = VMobject().set_points_as_corners(
            [err.c2p(np.log10(x), np.log10(b)) for x, b in zip(hs[show], bias[show])]
        ).set_stroke(GREEN, 2.8)
        noise_pts = VGroup(*[Dot(err.c2p(np.log10(x), np.log10(s)), radius=0.06, color=BLUE)
                             for x, s in zip(widths, noise)])
        total_pts = VGroup(*[Square(side_length=0.12, color=INK, fill_opacity=1, stroke_width=0)
                             .move_to(err.c2p(np.log10(x), np.log10(s))) for x, s in zip(widths, total)])
        marker = always_redraw(lambda: DashedLine(err.c2p(log_h.get_value(), lo_e),
                                                  err.c2p(log_h.get_value(), hi_e),
                                                  color=INK, stroke_width=1.6, dash_length=0.06))
        err_key = VGroup(
            VGroup(Dot(radius=0.06, color=BLUE),
                   math(r"\mathrm{noise}\ n_h-K_h*n,\ 300\ \mathrm{samples}", color=MUTED, size=MATH_SMALL)
                   ).arrange(RIGHT, buff=0.15),
            VGroup(DashedLine(ORIGIN, RIGHT * 0.45, color=BLUE, stroke_width=2.2, dash_length=0.07),
                   math(r"1/\sqrt{N_h},\ N_h=2\sqrt{\pi}\,\bar n h", color=MUTED,
                        size=MATH_SMALL)).arrange(RIGHT, buff=0.15),
            VGroup(Line(ORIGIN, RIGHT * 0.45, color=GREEN, stroke_width=2.8),
                   math(r"\mathrm{bias}\ K_h*n-n", color=MUTED, size=MATH_SMALL)).arrange(RIGHT, buff=0.15),
            VGroup(Square(side_length=0.12, color=INK, fill_opacity=1, stroke_width=0),
                   math(r"\mathrm{total}\ n_h-n", color=MUTED, size=MATH_SMALL)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        err_key.to_edge(RIGHT, buff=0.6).to_edge(DOWN, buff=0.55)

        cue = math(r"h\ll\Delta:\ \mathrm{spikes\ return}", color=INK, size=MATH_SMALL).move_to([0.25, -0.95, 0])

        def show_cue(text):
            new = math(text, color=INK, size=MATH_SMALL).move_to(cue.get_center())
            return Transform(cue, new)

        fine = np.geomspace(0.25, 20, 400)
        best = fine[np.argmin(np.hypot(noise_theory(fine), [bias_rms(x) for x in fine]))]

        self.add(frame, truth, dots, estimate, clip_marks, legend, h_label, h_value,
                 err_frame, x_ticks, y_ticks, tick_lines, err_x, err_y, theory, bias_line, noise_pts,
                 total_pts, marker, err_key, cue)
        self.wait(2.0)
        self.play(log_h.animate.set_value(np.log10(1.5)), show_cue(
            rf"h=1.5\,\Delta:\ \mathrm{{bump\ resolved,\ rms\ noise}}\approx{noise_theory(1.5):.2f}\,\bar n"),
            run_time=6.0, rate_func=LINEAR)
        self.wait(2.5)
        self.play(log_h.animate.set_value(np.log10(20.0)), show_cue(
            r"h\gg\mathrm{bump\ width}:\ \mathrm{smooth,\ bump\ washed\ out\ (bias)}"),
            run_time=7.0, rate_func=LINEAR)
        self.wait(2.0)
        self.play(log_h.animate.set_value(np.log10(best)), show_cue(
            rf"\mathrm{{least\ rms\ error:}}\ h\approx{best:.0f}\,\Delta,\ \mathrm{{noise}}\approx\mathrm{{bias,\ bump\ flattened}}"),
            run_time=3.0, rate_func=EASE)
        self.wait(3.0)
