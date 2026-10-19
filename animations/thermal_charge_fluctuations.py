"""Thermal charge-density fluctuations of a neutral plasma (kin6d particle data).

Data: kin6d ``ocp_shielding_demo --export`` without impurity (case C4,
kappa = 0; see animations/data/kin6d/thermal-charge-fluctuations/README.md and
provenance.json).  Classical electron one-component plasma in a periodic cube
of edge L = 6 lambda_D with a uniform neutralizing background +e n_0, bare
Coulomb interaction (particle-mesh Ewald, no softening),
Lambda = n lambda_D^3 = 30 (N = 6480 electrons), in thermal equilibrium; no
test charge.  Plasma units: lambda_D, omega_p, k_B T.

The colour field is the net charge density rho = e (n_0 - n_e) in the plane
z = 0, with n_e the electron density of the same realization smoothed by a
three-dimensional Gaussian kernel of width SIGMA (periodic images included):
red where electrons are missing (rho > 0), blue where they crowd (rho < 0).
The dots are the electrons of the slab |z| < SIGMA projected onto (x, y)
(markers fade at the slab faces; positions and fields between the exported
samples, 0.2/omega_p apart, are interpolated linearly for display).  Every
quantity is computed here from the exported electron positions only.  The
scene loops: equilibrium fluctuations have no beginning or end.
"""

from manim import *
import numpy as np

from kin6d_data import Export
from style import (
    AXIS_WIDTH, BG, EASE, FAINT, GRID, INK, LINEAR, MUTED, StyledScene, label, math,
    MATH_SMALL, SMALL_SIZE,
)

SIGMA = 0.4             # Gaussian smoothing width of the charge density, lambda_D
GRID_POINTS = 180       # field samples per box edge
FADE = 0.1              # dot fade width at the slab faces, lambda_D
RHO_MAX = 0.3           # colour scale limit of rho/(e n_0)
PANEL = 6.8             # field panel side in Manim units
PLAY_TIME = 26.0        # seconds for the 40/omega_p of recorded dynamics
POSITIVE = "#E5533F"    # net positive charge (electron deficit)
NEGATIVE = "#3C8FE0"    # net negative charge (electron excess)


def charge_density(points, box, sigma, n0, grid):
    """Net charge density rho/(e n_0) = 1 - n_sigma/n_0 on the plane z = 0.

    points: (3, N) electron positions in [-L/2, L/2]^3 (periodic cube).
    n_sigma is the electron density convolved with the normalized 3D Gaussian
    of width sigma, using minimum-image distances (sigma << L/2).  Returns
    (grid, grid) samples at the cell centres, index [i_x, i_y].
    """
    centres = -box / 2 + (np.arange(grid) + 0.5) * box / grid
    near = np.abs(points[2]) < 6 * sigma
    x, y, z = points[0, near], points[1, near], points[2, near]

    def kernel(d):
        d = d - box * np.round(d / box)
        return np.exp(-d * d / (2 * sigma * sigma))

    gx = kernel(centres[:, None] - x[None, :]) * kernel(z)[None, :]
    gy = kernel(centres[:, None] - y[None, :])
    density = gx @ gy.T / (2 * np.pi * sigma * sigma) ** 1.5
    return 1 - density / n0


def debye_hueckel_variance(box, sigma, n0, structure=lambda k2: k2 / (k2 + 1)):
    """Variance of charge_density in equilibrium, sum over the box modes.

    <(rho/(e n_0))^2> = (1/(n_0 L^3)) sum_{k != 0} exp(-k^2 sigma^2) S(k), with
    the Debye-Hueckel structure factor S = k^2/(k^2 + 1) (lambda_D = 1) by
    default; S = 1 is the uncorrelated ideal gas.
    """
    m = np.arange(-int(6 * box / (2 * np.pi * sigma)) - 1,
                  int(6 * box / (2 * np.pi * sigma)) + 2)
    kx, ky, kz = np.meshgrid(*(2 * np.pi * m / box,) * 3, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    k2 = k2[k2 > 0]
    return float(np.sum(np.exp(-k2 * sigma * sigma) * structure(k2)) / (n0 * box ** 3))


def charge_rgb(level):
    """rho/(e n_0)/RHO_MAX in [-1, 1] -> uint8 RGB: BG at 0, red > 0, blue < 0."""
    def rgb(c):
        return np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)

    level = np.clip(np.asarray(level, float), -1.0, 1.0)[..., None]
    base = rgb(BG)
    colour = np.where(level > 0, rgb(POSITIVE), rgb(NEGATIVE))
    return np.round(base + np.abs(level) * (colour - base)).astype(np.uint8)


def _rgba(field):
    """(x, y) field -> RGBA image with y up and x to the right."""
    image = charge_rgb(field / RHO_MAX).transpose(1, 0, 2)[::-1]
    alpha = np.full(image.shape[:2] + (1,), 255, np.uint8)
    return np.ascontiguousarray(np.concatenate([image, alpha], axis=2))


class ThermalChargeFluctuations(StyledScene):
    """Electrons of a neutral plasma and their smoothed net charge density."""

    def build(self):
        data = Export("thermal-charge-fluctuations")
        pos = data["positions"]                    # (3, N, frames)
        times = data["t"]
        box = data.parameters["box"]
        n0 = data.parameters["electrons"] / box ** 3
        frames = len(times)
        fields = np.stack([charge_density(pos[:, :, f], box, SIGMA, n0, GRID_POINTS)
                           for f in range(frames)], axis=-1)

        tracker = ValueTracker(0.0)
        blend = ValueTracker(0.0)        # loop: cross-fade last -> first field

        def frame_pos(u):
            f = u * (frames - 1)
            i = min(int(f), frames - 2)
            return f, i, f - i

        def positions(u):
            _, i, w = frame_pos(u)
            a, b = pos[:, :, i], pos[:, :, i + 1]
            step = b - a
            step -= box * np.round(step / box)     # minimum image between samples
            p = a + w * step
            return p - box * np.round(p / box)

        def field(u):
            _, i, w = frame_pos(u)
            f = (1 - w) * fields[..., i] + w * fields[..., i + 1]
            b = blend.get_value()
            return (1 - b) * f + b * fields[..., 0] if b > 0 else f

        # --- left: field and electrons of the slab ------------------------
        center = np.array([-3.05, 0.0, 0.0])
        scale = PANEL / box

        def pp(x, y):
            return center + np.array([x, y, 0.0]) * scale

        image = ImageMobject(_rgba(field(0.0)))
        image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        image.height = PANEL
        image.move_to(center)
        image.add_updater(lambda m: setattr(m, "pixel_array", _rgba(field(tracker.get_value()))))
        frame = Square(PANEL, color=GRID, stroke_width=AXIS_WIDTH).move_to(center)

        in_slab = np.abs(pos[2]) < SIGMA + 0.05
        pool = int(in_slab.sum(axis=0).max() * 1.15) + 20
        dots = VGroup(*[Dot(center, radius=0.032, color=INK, fill_opacity=0)
                        for _ in range(pool)])
        dot_opacity = ValueTracker(0.0)

        def update_dots(group):
            p = positions(tracker.get_value())
            z = np.abs(p[2])
            idx = np.nonzero(z < SIGMA)[0]
            alpha = np.clip((SIGMA - z[idx]) / FADE, 0.0, 1.0) * dot_opacity.get_value()
            for k, dot in enumerate(group):
                if k < len(idx):
                    j = idx[k]
                    dot.move_to(pp(p[0, j], p[1, j]))
                    dot.set_fill(opacity=alpha[k])
                else:
                    dot.set_fill(opacity=0)

        dots.add_updater(update_dots)
        update_dots(dots)

        # --- right: colour bar, legend, scale bar, clock ------------------
        col = 1.25
        bar_h, bar_w = 2.7, 0.3
        bar_center = np.array([col + bar_w / 2, 1.5, 0])
        column = np.linspace(1, -1, 256)[:, None] * np.ones((1, 4))
        bar = ImageMobject(np.concatenate(
            [charge_rgb(column), np.full((256, 4, 1), 255, np.uint8)], axis=2))
        bar.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        bar.stretch_to_fit_height(bar_h).stretch_to_fit_width(bar_w).move_to(bar_center)
        bar_frame = Rectangle(width=bar_w, height=bar_h, color=GRID,
                              stroke_width=AXIS_WIDTH).move_to(bar_center)
        bar_ticks = VGroup()
        tick_x = bar_center[0] + bar_w / 2
        for v, tex in ((RHO_MAX, f"+{RHO_MAX:g}"), (0.0, "0"), (-RHO_MAX, f"-{RHO_MAX:g}")):
            start = np.array([tick_x, bar_center[1] + bar_h / 2 * v / RHO_MAX, 0])
            bar_ticks.add(Line(start, start + RIGHT * 0.08, color=INK, stroke_width=AXIS_WIDTH))
            bar_ticks.add(math(tex, color=MUTED, size=MATH_SMALL)
                          .next_to(start + RIGHT * 0.08, RIGHT, buff=0.1))
        bar_label = math(r"\rho/(e n_0)\ [1]", color=MUTED, size=MATH_SMALL)
        bar_label.next_to(bar_frame, UP, buff=0.2).align_to(bar_frame, LEFT)
        text_x = tick_x + 1.25
        deficit = VGroup(label("electron deficit", color=POSITIVE, size=SMALL_SIZE),
                         label("net positive", color=MUTED, size=SMALL_SIZE)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        deficit.move_to([text_x, bar_center[1] + bar_h / 2, 0], aligned_edge=UP + LEFT)
        excess = VGroup(label("electron excess", color=NEGATIVE, size=SMALL_SIZE),
                        label("net negative", color=MUTED, size=SMALL_SIZE)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        excess.move_to([text_x, bar_center[1] - bar_h / 2, 0], aligned_edge=DOWN + LEFT)

        electron_key = VGroup(Dot(radius=0.075, color=INK),
                              label("electron,", color=MUTED, size=SMALL_SIZE),
                              math(rf"|z|<{SIGMA:g}\,\lambda_D", color=MUTED, size=MATH_SMALL)
                              ).arrange(RIGHT, buff=0.14)
        kernel_key = VGroup(label("smoothing", color=MUTED, size=SMALL_SIZE),
                            math(rf"\sigma={SIGMA:g}\,\lambda_D", color=MUTED, size=MATH_SMALL)
                            ).arrange(RIGHT, buff=0.14)
        bar_len = scale
        scale_bar = VGroup(
            Line(ORIGIN, RIGHT * bar_len, color=INK, stroke_width=4),
            Line(UP * 0.09, DOWN * 0.09, color=INK, stroke_width=AXIS_WIDTH),
            Line(UP * 0.09, DOWN * 0.09, color=INK, stroke_width=AXIS_WIDTH).shift(RIGHT * bar_len),
        )
        scale_key = VGroup(scale_bar, math(r"\lambda_D", color=MUTED, size=MATH_SMALL)
                           ).arrange(RIGHT, buff=0.18)
        plasma_key = math(rf"n\lambda_D^3={data.parameters['Lambda']:g}", color=MUTED,
                          size=MATH_SMALL)
        clock_label = math(r"\omega_p t=", color=MUTED, size=MATH_SMALL)
        legend = VGroup(electron_key, kernel_key, scale_key, plasma_key, clock_label
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        legend.move_to([col, -1.75, 0], aligned_edge=LEFT)
        clock = DecimalNumber(times[0], num_decimal_places=1, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            f, i, w = frame_pos(tracker.get_value())
            now = times[i] + w * (times[i + 1] - times[i])
            m.set_value(times[0] if blend.get_value() > 0.5 else now)
            m.next_to(clock_label, RIGHT, buff=0.12).match_y(clock_label[0][-1])

        clock.add_updater(place_clock)
        place_clock(clock)

        self.add(image, frame, dots, bar, bar_frame, bar_ticks, bar_label, deficit, excess,
                 legend, clock)
        self.play(dot_opacity.animate.set_value(1.0), run_time=0.6, rate_func=EASE)
        self.wait(0.4)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(0.4)
        self.play(blend.animate.set_value(1.0), dot_opacity.animate.set_value(0.0),
                  run_time=0.6, rate_func=EASE)
