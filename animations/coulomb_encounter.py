"""Quantum Coulomb encounter of two electrons: classical, distinguishable,
singlet and triplet relative densities (kin6d data).

Data: kin6d ``coulomb_encounter_demo --movie-only --export`` (case Q1, see
animations/data/kin6d/coulomb-encounter-*/README.md and provenance.json).
Two equal-mass electrons with bare Coulomb repulsion, Sommerfeld parameter
eta = 3, Gaussian packets with sigma = 3 reduced de Broglie wavelengths
(sigma = r0/2, r0 = 2 eta / k the head-on classical turning radius), initial
separation z0 = 20/k, impact parameter b = 0 (head-on) or b = 2/k (off-axis).
Each panel shows the y = 0 slice of the probability density of the relative
coordinate r = x1 - x2 times k^-3 on one shared log colour scale (four
decades): top row the classical Wigner-sampled ensemble (spin-unresolved,
thin slab |y| < 1/(2k)) and the spin-unresolved quantum product state, which
behaves as distinguishable particles; bottom row the singlet (even partial
waves) and triplet (odd partial waves).  The top row has no exchange term;
the bottom row adds it with opposite signs, and the average of singlet and
triplet is the top-right panel.  The dashed circle is r = r0.
Hot case (``CoulombEncounterHot``): eta = 0.03, the thermal relative speed of
electrons in a 10 keV plasma (relative energy Ry/(2 eta^2) = 7.6 keV), sigma
= 3/k, b = 0, the same four decades of colour: r0 = 0.06/k lies far below the
wavelength, so the quantum packet passes almost undeflected and sheds only a
faint diffracted wave, while the classical ensemble keeps a sharp (unresolved)
hole and rare large deflections; no r0 circle is drawn.
Positions are k x [1] and k z [1] with k = 1/lambdabar; the clock is the
demo's slow-motion clock (up to 4x slower around closest approach), shown as
t v/z0 [1].  Visualization path of a bounded propagation: no pointwise bound
on the displayed densities; the classical histogram carries counting noise.
"""

from manim import *
import numpy as np

from style import (
    AXIS, AXIS_WIDTH, BG, EASE, FAINT, GRID, INK, LINEAR, MUTED, THIN_WIDTH,
    StyledScene, density_rgb, label, math, MATH_SMALL, SMALL_SIZE,
)
from kin6d_data import Export

PANEL = 2.85            # panel side in Manim units
GAP = 0.30              # gap between panels
NAMES = ["classical", "distinguishable", "singlet", "triplet"]
PLAY_TIME = 11.0        # seconds for the recorded frames
HOLD = 0.8


def _rgba(levels):
    """(z, x) log10 densities -> RGBA image with x up and z to the right."""
    rgb = density_rgb(levels)
    image = np.transpose(rgb, (1, 0, 2))[::-1]
    alpha = np.full(image.shape[:2] + (1,), 255, np.uint8)
    return np.ascontiguousarray(np.concatenate([image, alpha], axis=2))


class _Encounter(StyledScene):
    slug = None

    def build(self):
        data = Export(self.slug)
        maps = data["log10_density"]                      # (z, x, panel, frame)
        lo = data.provenance["arrays"]["log10_density"]["decode"]["lo"]
        hi = data.provenance["arrays"]["log10_density"]["decode"]["hi"]
        edges = data["x_edges"]
        times = data["t"]
        half = edges[-1]
        r0 = data.parameters["r0"]
        frames = maps.shape[3]
        levels = np.where(np.isfinite(maps), (maps - lo) / (hi - lo), -0.02)

        grid_center = LEFT * 0.75 + UP * 0.35
        offsets = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
        centers = [grid_center + np.array([dx * (PANEL + GAP) / 2, dy * (PANEL + GAP) / 2, 0])
                   for dx, dy in offsets]

        def frame_levels(position, p):
            """Linear blend in log density between neighbouring frames."""
            f = position * (frames - 1)
            i = min(int(f), frames - 2)
            w = f - i
            return (1 - w) * levels[..., p, i] + w * levels[..., p, i + 1]

        tracker = ValueTracker(0.0)
        blend = ValueTracker(0.0)       # loop: cross-fade last -> first frame
        first = [_rgba(levels[..., p, 0]).astype(float) for p in range(4)]
        images = []
        for p, c in enumerate(centers):
            img = ImageMobject(_rgba(levels[..., p, 0]))
            img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
            img.height = PANEL
            img.move_to(c)
            images.append(img)

        # Each image carries its own updater, so the renderer treats it as
        # moving (static mobjects are cached in the background frame).
        def updater(p):
            def update(img):
                rgba = _rgba(frame_levels(tracker.get_value(), p))
                b = blend.get_value()
                if b > 0:
                    rgba = np.round((1 - b) * rgba + b * first[p]).astype(np.uint8)
                img.pixel_array = rgba
            return update

        for p, img in enumerate(images):
            img.add_updater(updater(p))

        def to_panel(p, z, x):
            return centers[p] + np.array([z, x, 0]) * PANEL / (2 * half)

        frames_group = VGroup(*[
            Square(PANEL, color=GRID, stroke_width=AXIS_WIDTH).move_to(c) for c in centers])
        circles = VGroup(*[
            DashedVMobject(Circle(radius=r0 * PANEL / (2 * half), color=INK,
                                  stroke_width=THIN_WIDTH, stroke_opacity=0.8),
                           num_dashes=28).move_to(c) for c in centers])
        names = VGroup(*[
            label(n, color=INK, size=SMALL_SIZE).next_to(c + UP * PANEL / 2, DOWN, buff=0.1)
            .align_to(c + LEFT * (PANEL / 2 - 0.12), LEFT)
            for n, c in zip(NAMES, centers)])
        r0_label = VGroup(
            DashedVMobject(Circle(radius=0.16, color=INK, stroke_width=THIN_WIDTH,
                                  stroke_opacity=0.8), num_dashes=10),
            math(r"r=r_0", color=MUTED, size=MATH_SMALL),
        ).arrange(RIGHT, buff=0.15)

        # Shared axes: ticks under the bottom row and left of the left column.
        ticks = VGroup()
        tick_values = [-20, 0, 20]
        for p in (2, 3):
            for v in tick_values:
                pos = to_panel(p, v, -half)
                ticks.add(Line(pos, pos + DOWN * 0.08, color=AXIS, stroke_width=AXIS_WIDTH))
                ticks.add(math(str(v), color=MUTED, size=MATH_SMALL)
                          .next_to(pos, DOWN, buff=0.13))
        for p in (0, 2):
            for v in tick_values:
                pos = to_panel(p, -half, v)
                ticks.add(Line(pos, pos + LEFT * 0.08, color=AXIS, stroke_width=AXIS_WIDTH))
                ticks.add(math(str(v), color=MUTED, size=MATH_SMALL).next_to(pos, LEFT, buff=0.13))
        # Axis names centred between the panels: kz under the tick labels, kx
        # on the tick-label column.
        z_label = math(r"kz\ [1]", color=MUTED, size=MATH_SMALL)
        z_label.move_to([grid_center[0], ticks[1].get_center()[1], 0]).shift(DOWN * 0.36)
        x_label = math(r"kx\ [1]", color=MUTED, size=MATH_SMALL)
        x_label.move_to([0, grid_center[1], 0]).align_to(ticks[-1], RIGHT)

        # Colour bar.
        bar_h, bar_w = 2 * PANEL + GAP - 0.9, 0.28
        bar_center = np.array([grid_center[0] + PANEL + GAP / 2 + 0.9, grid_center[1] - 0.1, 0])
        column = np.linspace(1, 0, 256)[:, None] * np.ones((1, 4))
        bar = ImageMobject(np.concatenate(
            [density_rgb(column), np.full((256, 4, 1), 255, np.uint8)], axis=2))
        bar.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        bar.stretch_to_fit_height(bar_h).stretch_to_fit_width(bar_w).move_to(bar_center)
        bar_frame = Rectangle(width=bar_w, height=bar_h, color=GRID,
                              stroke_width=AXIS_WIDTH).move_to(bar_center)
        bar_ticks = VGroup()
        for v in np.arange(np.ceil(lo), np.floor(hi) + 0.5, 1.0):
            y = bar_center[1] - bar_h / 2 + bar_h * (v - lo) / (hi - lo)
            start = np.array([bar_center[0] + bar_w / 2, y, 0])
            bar_ticks.add(Line(start, start + RIGHT * 0.08, color=AXIS, stroke_width=AXIS_WIDTH))
            bar_ticks.add(math(f"{int(v)}", color=MUTED, size=MATH_SMALL)
                          .next_to(start + RIGHT * 0.08, RIGHT, buff=0.1))
        bar_label = math(r"\log_{10}(\rho/k^3)\ [1]", color=MUTED, size=MATH_SMALL)
        bar_label.next_to(bar_frame, UP, buff=0.18).align_to(bar_frame, LEFT).shift(LEFT * 0.35)

        # Clock: physical time in z0/v (frame clock includes slow motion).
        clock_value = DecimalNumber(0.0, num_decimal_places=2, color=INK, font_size=MATH_SMALL)
        clock_label = math(r"tv/z_0=", color=MUTED, size=MATH_SMALL)

        def place_clock(m):
            f = tracker.get_value() * (frames - 1)
            i = min(int(f), frames - 2)
            value = times[i] + (f - i) * (times[i + 1] - times[i])
            m.set_value(0.0 if blend.get_value() > 0.5 else value)
            m.next_to(clock_label, RIGHT, buff=0.12)

        clock_label.next_to(bar_frame, DOWN, buff=0.35).align_to(bar_label, LEFT)
        clock_value.add_updater(place_clock)
        r0_label.next_to(clock_label, DOWN, buff=0.3).align_to(clock_label, LEFT)
        place_clock(clock_value)

        # The r0 circle is drawn only when it is resolved on the panel grid
        # (not for the hot case, r0 = 0.06/k).
        marks = [circles, r0_label] if r0 > 2 * (edges[1] - edges[0]) else []
        self.add(*images, frames_group, *marks, names, ticks, z_label,
                 x_label, bar, bar_frame, bar_ticks, bar_label, clock_label, clock_value,
                 )
        self.wait(HOLD)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.wait(HOLD)
        # Loop: cross-fade back to the first frame so that the last video
        # frame equals the first.
        self.play(blend.animate.set_value(1.0), run_time=0.9, rate_func=EASE)
        self.wait(0.2)


class CoulombEncounterHeadOn(_Encounter):
    """Head-on encounter (b = 0)."""

    slug = "coulomb-encounter-headon"


class CoulombEncounterOffAxis(_Encounter):
    """Off-axis encounter (kb = 2)."""

    slug = "coulomb-encounter-offaxis"


class CoulombEncounterHot(_Encounter):
    """Hot electrons, eta = 0.03 (relative energy about 7.6 keV): head-on."""

    slug = "coulomb-encounter-hot"
